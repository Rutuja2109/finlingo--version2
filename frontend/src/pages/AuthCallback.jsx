import React, { useEffect, useRef, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { api } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import Lumi from "@/components/Lumi";

// REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
export default function AuthCallback() {
  const nav = useNavigate();
  const loc = useLocation();
  const { setUser, refreshStats } = useAuth();
  const processed = useRef(false);
  const [err, setErr] = useState("");

  useEffect(() => {
    if (processed.current) return;
    processed.current = true;
    (async () => {
      try {
        const hash = window.location.hash || loc.hash || "";
        const m = hash.match(/session_id=([^&]+)/);
        if (!m) { setErr("No session in callback URL"); return; }
        const session_id = decodeURIComponent(m[1]);
        const { data } = await api.post("/auth/google/session", { session_id });
        if (data.access_token) localStorage.setItem("fl_token", data.access_token);
        if (setUser) setUser(data);
        if (refreshStats) await refreshStats();
        // Clear the hash and go to dashboard
        window.history.replaceState({}, "", "/dashboard");
        nav("/dashboard", { replace: true });
      } catch (e) {
        const msg = e?.response?.data?.detail || e?.message || "Google sign-in failed";
        setErr(String(msg));
      }
    })();
  }, [nav, loc.hash, setUser, refreshStats]);

  return (
    <div className="min-h-screen grid place-items-center bg-[#FAFAFA] font-[Manrope] p-6">
      <div className="text-center max-w-sm">
        <div className="flex justify-center mb-4"><Lumi size={88} mood="cheer"/></div>
        {!err ? (
          <>
            <h1 className="font-[Outfit] font-black text-2xl tracking-tight">Signing you in…</h1>
            <p className="text-zinc-500 mt-1">Almost there.</p>
          </>
        ) : (
          <>
            <h1 className="font-[Outfit] font-black text-2xl tracking-tight text-red-600">Sign-in failed</h1>
            <p className="text-zinc-500 mt-1" data-testid="callback-error">{err}</p>
            <button onClick={() => nav("/login", { replace: true })} data-testid="callback-back"
              className="mt-5 px-5 py-2.5 rounded-xl bg-zinc-900 text-white font-bold">Back to login</button>
          </>
        )}
      </div>
    </div>
  );
}
