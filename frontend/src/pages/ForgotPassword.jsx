import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api, formatApiError } from "@/lib/api";
import Lumi from "@/components/Lumi";
import { ArrowRight } from "lucide-react";

export default function ForgotPassword() {
  const nav = useNavigate();
  const [email, setEmail] = useState("");
  const [busy, setBusy] = useState(false);
  const [resetPath, setResetPath] = useState(null);
  const [err, setErr] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true); setErr("");
    try {
      const { data } = await api.post("/auth/forgot-password", { email });
      if (data.reset_path) {
        setResetPath(data.reset_path);
      } else {
        // Email not found — show generic message but don't reveal it
        setResetPath("__not_found__");
      }
    } catch (e) {
      setErr(formatApiError(e));
    } finally { setBusy(false); }
  };

  return (
    <div className="min-h-screen grid place-items-center bg-[#FAFAFA] font-[Manrope] p-6">
      <div className="w-full max-w-md bg-white border border-zinc-200 rounded-3xl p-8 shadow-[0_30px_60px_-30px_rgba(0,0,0,0.15)]">

        {!resetPath ? (
          <>
            <div className="flex justify-center mb-4"><Lumi size={72} mood="think"/></div>
            <h1 className="font-[Outfit] font-black text-3xl tracking-tight text-center">Forgot password?</h1>
            <p className="text-zinc-500 text-sm text-center mt-1 mb-6">
              Enter the email you signed up with and we'll get you back in.
            </p>

            <form onSubmit={submit}>
              <label className="block mb-4">
                <span className="text-xs uppercase tracking-[0.2em] font-semibold text-zinc-500 mb-1.5 block">Email</span>
                <input type="email" required value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  data-testid="forgot-email"
                  placeholder="you@work.com"
                  className="w-full px-4 py-3 rounded-xl border border-zinc-200 outline-none focus:border-[#FF6B35] focus:ring-2 focus:ring-[#FF6B35]/20"/>
              </label>

              {err && (
                <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-xl px-3 py-2 mb-3"
                  data-testid="forgot-error">{err}</div>
              )}

              <button type="submit" disabled={busy} data-testid="btn-forgot-submit"
                className="w-full py-3 rounded-xl bg-[#FF6B35] hover:bg-[#FF5618] text-white font-[Outfit] font-bold disabled:opacity-60 transition active:scale-[0.98]">
                {busy ? "Please wait…" : "Continue"}
              </button>
            </form>
          </>
        ) : resetPath === "__not_found__" ? (
          <>
            <div className="flex justify-center mb-4"><Lumi size={72} mood="happy"/></div>
            <h1 className="font-[Outfit] font-black text-2xl tracking-tight text-center">Check your email</h1>
            <p className="text-zinc-500 text-sm text-center mt-2 mb-6">
              If an account with <strong>{email}</strong> exists, a reset link has been sent.
            </p>
            <button onClick={() => { setResetPath(null); setEmail(""); }}
              className="w-full py-3 rounded-xl bg-zinc-100 hover:bg-zinc-200 text-zinc-800 font-[Outfit] font-bold transition">
              Try a different email
            </button>
          </>
        ) : (
          <>
            <div className="flex justify-center mb-4"><Lumi size={72} mood="cheer"/></div>
            <h1 className="font-[Outfit] font-black text-2xl tracking-tight text-center">Ready to reset!</h1>
            <p className="text-zinc-500 text-sm text-center mt-2 mb-6">
              Tap the button below to set a new password for <strong>{email}</strong>.
            </p>

            <button onClick={() => nav(resetPath)} data-testid="btn-go-reset"
              className="w-full py-4 rounded-xl bg-[#FF6B35] hover:bg-[#FF5618] text-white font-[Outfit] font-bold text-lg inline-flex items-center justify-center gap-2 transition active:scale-[0.98]">
              Set new password <ArrowRight className="w-5 h-5"/>
            </button>

            <p className="text-xs text-zinc-400 text-center mt-4">
              This link expires in 1 hour.
            </p>
          </>
        )}

        <p className="text-sm text-zinc-500 text-center mt-6">
          Remembered it?{" "}
          <Link to="/login" data-testid="back-to-login" className="text-[#FF6B35] font-semibold">
            Back to login
          </Link>
        </p>
      </div>
    </div>
  );
}
