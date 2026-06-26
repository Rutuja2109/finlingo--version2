import React, { useEffect, useState } from "react";
import { useNavigate, useSearchParams, Link } from "react-router-dom";
import { api, formatApiError } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import Lumi from "@/components/Lumi";

export default function ResetPassword() {
  const [params] = useSearchParams();
  const nav = useNavigate();
  const { setUser, refreshStats } = useAuth();
  const token = params.get("token") || "";
  const [pw, setPw] = useState("");
  const [pw2, setPw2] = useState("");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");

  useEffect(() => { if (!token) setErr("No reset token in URL"); }, [token]);

  const submit = async (e) => {
    e.preventDefault();
    setErr("");
    if (pw.length < 6) { setErr("Password must be at least 6 characters"); return; }
    if (pw !== pw2) { setErr("Passwords don't match"); return; }
    setBusy(true);
    try {
      const { data } = await api.post("/auth/reset-password", { token, new_password: pw });
      if (data.access_token) localStorage.setItem("fl_token", data.access_token);
      if (setUser) setUser(data);
      if (refreshStats) await refreshStats();
      nav("/dashboard", { replace: true });
    } catch (e) {
      setErr(formatApiError(e));
    } finally { setBusy(false); }
  };

  return (
    <div className="min-h-screen grid place-items-center bg-[#FAFAFA] font-[Manrope] p-6">
      <div className="w-full max-w-md bg-white border border-zinc-200 rounded-3xl p-8 shadow-[0_30px_60px_-30px_rgba(0,0,0,0.15)]">
        <div className="flex justify-center mb-3"><Lumi size={64} mood="happy"/></div>
        <h1 className="font-[Outfit] font-black text-3xl tracking-tight text-center">Set a new password</h1>
        <p className="text-zinc-500 text-sm text-center mt-1 mb-6">Pick something memorable and strong.</p>

        <form onSubmit={submit}>
          <Field label="New password">
            <input type="password" required minLength={6} value={pw} onChange={(e) => setPw(e.target.value)}
              data-testid="reset-pw" placeholder="Min 6 characters"
              className="w-full px-4 py-3 rounded-xl border border-zinc-200 outline-none focus:border-[#FF6B35] focus:ring-2 focus:ring-[#FF6B35]/20"/>
          </Field>
          <Field label="Confirm password">
            <input type="password" required minLength={6} value={pw2} onChange={(e) => setPw2(e.target.value)}
              data-testid="reset-pw2"
              className="w-full px-4 py-3 rounded-xl border border-zinc-200 outline-none focus:border-[#FF6B35] focus:ring-2 focus:ring-[#FF6B35]/20"/>
          </Field>
          {err && <div className="text-sm text-red-600 mb-3" data-testid="reset-error">{err}</div>}
          <button type="submit" disabled={busy || !token} data-testid="btn-reset-submit"
            className="w-full py-3 rounded-xl bg-[#FF6B35] hover:bg-[#FF5618] text-white font-[Outfit] font-bold disabled:opacity-60 transition active:scale-[0.98]">
            {busy ? "Resetting…" : "Reset password & sign in"}
          </button>
        </form>

        <p className="text-sm text-zinc-500 text-center mt-5">
          <Link to="/login" className="text-[#FF6B35] font-semibold">Back to login</Link>
        </p>
      </div>
    </div>
  );
}

function Field({ label, children }) {
  return (
    <label className="block mb-4">
      <span className="text-xs uppercase tracking-[0.2em] font-semibold text-zinc-500 mb-1.5 block">{label}</span>
      {children}
    </label>
  );
}
