import React, { createContext, useContext, useEffect, useRef, useState, useCallback } from "react";
import { api, formatApiError } from "@/lib/api";
import { requestNotificationPermission, scheduleReminders, cancelReminders, scheduleTrialReminders, cancelTrialReminders } from "@/lib/notifications";
import { restore, isNative } from "@/lib/billing";
import { identifyUser, trackLogin, trackSignUp } from "@/lib/firebase";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null); // null = loading, false = logged out
  const [stats, setStats] = useState(null);
  // Pro status from the server. The last known value is kept so tabs open instantly; it is refreshed in the background.
  const [sub, setSub] = useState(() => { try { return JSON.parse(localStorage.getItem("fl_sub") || "null"); } catch { return null; } });
  const saveSub = (d) => { try { localStorage.setItem("fl_sub", JSON.stringify(d)); } catch { /* ignore */ } };
  const [subFailed, setSubFailed] = useState(false);

  // Reminders are scheduled one after another (never two at once) and re-planned whenever the learner's day changes,
  // so practising today cancels today's nudges.
  const queue = useRef(Promise.resolve());
  const lastPlan = useRef("");
  const localDay = () => { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`; };
  const syncReminders = useCallback((s, force = false) => {
    if (!s) return;
    const practiced = s.last_active_date === localDay();
    const key = `${localDay()}|${s.streak_days || 0}|${practiced}`;
    if (!force && key === lastPlan.current) return;
    lastPlan.current = key;
    queue.current = queue.current.then(() => scheduleReminders(s.streak_days || 0, 8, practiced)).catch(() => {});
  }, []);

  const refreshStats = useCallback(async () => {
    try {
      const { data } = await api.get("/stats/me");
      setStats(data);
      return data;
    } catch (e) {
      return null;
    }
  }, []);

  // Heads-ups before the free trial ends; removed as soon as the learner subscribes.
  const syncTrialReminders = useCallback((d) => {
    try {
      if (!d || localStorage.getItem("fl_notif") !== "granted") return;
      if (d.trial?.active && !d.admin) scheduleTrialReminders(d.trial.ends_at);
      else cancelTrialReminders();
    } catch { /* reminders are optional */ }
  }, []);

  const refreshSub = useCallback(async () => {
    try {
      let { data } = await api.get("/subscription/status");
      // Not Pro here but Google may already know a purchase (new phone, reinstall, failed earlier check).
      if (!data.pro && !data.admin && isNative() && data.billing_ready) {
        try { if (await restore(data.product_id)) data = (await api.get("/subscription/status")).data; } catch { /* ignore */ }
      }
      setSub(data);
      saveSub(data);
      setSubFailed(false);
      syncTrialReminders(data);
      return data;
    } catch { setSubFailed(true); return null; }
  }, [syncTrialReminders]);

  // Practising (or a new day) changes which reminders still make sense.
  useEffect(() => {
    try {
      if (stats && user && localStorage.getItem("fl_notif") === "granted") syncReminders(stats);
    } catch {
      // storage unavailable: skip
    }
  }, [stats, user, syncReminders]);

  const reminderPermission = useCallback(async (s) => {
    try {
      const granted = await requestNotificationPermission();
      if (granted) {
        try { localStorage.setItem("fl_notif", "granted"); } catch { /* ignore */ }
        syncReminders(s, true);
      }
    } catch {
      // reminders are optional; never let them break the session
    }
  }, [syncReminders]);

  const loadMe = useCallback(async () => {
    try {
      // Three requests at once instead of one after another (each round trip to the server costs about half a second).
      const [me, s, plan] = await Promise.all([api.get("/auth/me"), api.get("/stats/me"), api.get("/subscription/status").catch(() => null)]);
      const data = me.data;
      setUser(data);
      setStats(s.data);
      if (plan) {
        setSub(plan.data); saveSub(plan.data); setSubFailed(false);
        syncTrialReminders(plan.data);
        if (!plan.data.pro && !plan.data.admin && plan.data.billing_ready) refreshSub(); // may find a purchase Google already knows
      } else {
        refreshSub();
      }
      identifyUser(data.id, data.name, data.email);
      await reminderPermission(s.data);
    } catch {
      setUser(false);
      setStats(null);
      setSub(null);
      try { localStorage.removeItem("fl_sub"); } catch { /* ignore */ }
    }
  }, [reminderPermission, refreshSub, syncTrialReminders]);

  useEffect(() => {
    loadMe();
  }, [loadMe]);

  const login = async (email, password) => {
    try {
      const { data } = await api.post("/auth/login", { email, password });
      if (data.access_token) localStorage.setItem("fl_token", data.access_token);
      setUser(data);
      const st = await refreshStats();
      refreshSub();
      identifyUser(data.id, data.name, data.email);
      trackLogin("email");
      await reminderPermission(st);
      return { ok: true };
    } catch (e) {
      return { ok: false, error: formatApiError(e) };
    }
  };

  // Sign in (or sign up) with a Google ID token. The server verifies it and returns our own login.
  const loginWithGoogle = async (idToken) => {
    try {
      const { data } = await api.post("/auth/google", { id_token: idToken });
      if (data.access_token) localStorage.setItem("fl_token", data.access_token);
      setUser(data);
      const st = await refreshStats();
      refreshSub();
      identifyUser(data.id, data.name, data.email);
      if (data.new_account) trackSignUp("google"); else trackLogin("google");
      await reminderPermission(st);
      return { ok: true };
    } catch (e) {
      return { ok: false, error: formatApiError(e) };
    }
  };

  const register = async (email, password, name) => {
    try {
      const { data } = await api.post("/auth/register", { email, password, name });
      if (data.access_token) localStorage.setItem("fl_token", data.access_token);
      setUser(data);
      await refreshStats();
      refreshSub();
      identifyUser(data.id, data.name, data.email);
      trackSignUp("email");
      return { ok: true };
    } catch (e) {
      return { ok: false, error: formatApiError(e) };
    }
  };

  const logout = () => {
    try { localStorage.removeItem("fl_notif"); } catch { /* ignore */ }
    lastPlan.current = "";
    cancelReminders().catch(() => {});
    api.post("/auth/logout").catch(() => {});
    localStorage.removeItem("fl_token");
    setUser(false);
    setStats(null);
    setSub(null);
    try { localStorage.removeItem("fl_sub"); } catch { /* ignore */ }
  };

  const deleteAccount = async (password) => {
    try {
      await api.delete("/auth/account", { data: { password } });
      cancelReminders().catch(() => {});
      localStorage.removeItem("fl_token");
      setUser(false);
      setStats(null);
      setSub(null);
      try { localStorage.removeItem("fl_sub"); } catch { /* ignore */ }
      return { ok: true };
    } catch (e) {
      return { ok: false, error: formatApiError(e) };
    }
  };

  return (
    <AuthContext.Provider value={{ user, stats, sub, subFailed, isPro: !!(sub && sub.pro), refreshSub, login, loginWithGoogle, register, logout, deleteAccount,refreshStats, setStats, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
