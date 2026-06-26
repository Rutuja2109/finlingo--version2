import React, { createContext, useContext, useEffect, useState, useCallback } from "react";
import { api, formatApiError } from "@/lib/api";

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
    } catch {
      setUser(false);
      setStats(null);
    }
  }, []);

  useEffect(() => {
    // CRITICAL: If returning from Google OAuth callback, skip /auth/me check.
    // AuthCallback will exchange the session_id and establish the session first.
    if (typeof window !== "undefined" && window.location.hash?.includes("session_id=")) {
      return;
    }
    loadMe();
  }, [loadMe]);

  const login = async (email, password) => {
    try {
      const { data } = await api.post("/auth/login", { email, password });
      if (data.access_token) localStorage.setItem("fl_token", data.access_token);
      setUser(data);
      await refreshStats();
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
      return { ok: true };
    } catch (e) {
      return { ok: false, error: formatApiError(e) };
    }
  };

  const logout = async () => {
    try { await api.post("/auth/logout"); } catch {}
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
