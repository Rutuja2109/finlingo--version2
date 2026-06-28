import React, { createContext, useContext, useEffect, useState, useCallback } from "react";
import { Capacitor } from "@capacitor/core";
import { App as CapApp } from "@capacitor/app";
import { Browser } from "@capacitor/browser";
import { api, formatApiError } from "@/lib/api";
import { requestNotificationPermission, scheduleReminders, cancelReminders } from "@/lib/notifications";
import { identifyUser, trackLogin, trackSignUp } from "@/lib/firebase";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null); // null = loading, false = logged out
  const [stats, setStats] = useState(null);

  const refreshStats = useCallback(async () => {
    try {
      const { data } = await api.get("/stats/me");
      setStats(data);
    } catch (e) {
      // ignore
    }
  }, []);

  const loadMe = useCallback(async () => {
    try {
      const { data } = await api.get("/auth/me");
      setUser(data);
      const s = await api.get("/stats/me");
      setStats(s.data);
      identifyUser(data.id, data.name, data.email);
      const granted = await requestNotificationPermission();
      if (granted) scheduleReminders(s.data?.streak_days || 0);
    } catch {
      setUser(false);
      setStats(null);
    }
  }, []);

  // Initial load — skip if web OAuth callback hash is present
  useEffect(() => {
    if (typeof window !== "undefined" && window.location.hash?.includes("session_id=")) {
      return;
    }
    loadMe();
  }, [loadMe]);

  // Native deep-link OAuth callback: finlingo://callback#session_id=xxx
  useEffect(() => {
    if (!Capacitor.isNativePlatform()) return;
    let handle;
    CapApp.addListener("appUrlOpen", async (event) => {
      const url = event.url || "";
      if (!url.includes("session_id=")) return;
      try { await Browser.close(); } catch {}
      const fragment = url.split("#")[1] || url.split("?")[1] || "";
      const m = fragment.match(/session_id=([^&]+)/);
      if (!m) return;
      const session_id = decodeURIComponent(m[1]);
      try {
        const { data } = await api.post("/auth/google/session", { session_id });
        if (data.access_token) localStorage.setItem("fl_token", data.access_token);
        identifyUser(data.id, data.name, data.email);
        trackLogin("google");
        setUser(data);
        await refreshStats();
        const granted = await requestNotificationPermission();
        if (granted) scheduleReminders(0);
      } catch (e) {
        console.error("Google sign-in failed", e);
      }
    }).then((h) => { handle = h; });
    return () => { handle?.remove(); };
  }, [refreshStats]);

  const login = async (email, password) => {
    try {
      const { data } = await api.post("/auth/login", { email, password });
      if (data.access_token) localStorage.setItem("fl_token", data.access_token);
      setUser(data);
      await refreshStats();
      identifyUser(data.id, data.name, data.email);
      // Track demo logins separately so reports show real vs demo users
      trackLogin(email === "demo@finlingo.com" ? "demo" : "email");
      const granted = await requestNotificationPermission();
      if (granted) scheduleReminders(0);
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
      identifyUser(data.id, data.name, data.email);
      trackSignUp("email");
      return { ok: true };
    } catch (e) {
      return { ok: false, error: formatApiError(e) };
    }
  };

  const logout = () => {
    cancelReminders().catch(() => {});
    api.post("/auth/logout").catch(() => {});
    localStorage.removeItem("fl_token");
    setUser(false);
    setStats(null);
  };

  return (
    <AuthContext.Provider value={{ user, stats, login, register, logout, refreshStats, setStats, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
