import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, formatApiError } from "@/lib/api";
import Lumi from "@/components/Lumi";

// When the server can send email, this is a normal "send me a reset link" form. When it cannot, it says what to do instead.
// (The server never returns a reset link to the person asking: the link only goes to the email's owner.)
export default function ForgotPassword() {
  const [cfg, setCfg] = useState(null);
  const [email, setEmail] = useState("");
  const [busy, setBusy] = useState(false);
  const [sent, setSent] = useState(false);
  const [err, setErr] = useState("");
  useEffect(() => { api.get("/auth/config").then((r) => setCfg(r.data)).catch(() => setCfg({})); }, []);

  const submit = async (e) => {
    e.preventDefault();
    setErr(""); setBusy(true);
    try { await api.post("/auth/forgot-password", { email: email.trim() }); setSent(true); }
    catch (ex) { setErr(formatApiError(ex)); }
    setBusy(false);
  };

  return (
    <div className="min-h-screen grid place-items-center bg-[#FAFAFA] font-[Manrope] p-6">
      <div className="w-full max-w-md bg-white border border-zinc-200 rounded-3xl p-8 shadow-[0_30px_60px_-30px_rgba(0,0,0,0.15)]" data-testid="forgot-page">
        <div className="flex justify-center mb-4"><Lumi size={72} mood="nervous" /></div>
        <h1 className="font-[Outfit] font-black text-3xl tracking-tight text-center">Forgot your password?</h1>

        {cfg?.email_reset ? (
          sent ? (
            <div className="mt-5" data-testid="forgot-sent">
              <div className="rounded-2xl bg-emerald-50 border border-emerald-200 p-4 text-sm text-emerald-900">
                <b className="font-[Outfit]">Check your email.</b> If that address has a FinLearn account, we have sent a message with the next step. It may take a minute, and it can land in spam. The link works for one hour.
              </div>
              <p className="text-zinc-600 text-sm mt-3">Opened the link on this phone? Choose your new password there, then come back here and log in.</p>
            </div>
          ) : (
            <form onSubmit={submit} className="mt-4" data-testid="forgot-form">
              <p className="text-zinc-500 text-sm text-center mb-4">Type the email you signed up with. We will send you a link to choose a new password.</p>
              <label htmlFor="fp-email" className="block text-sm font-semibold mb-1">Email</label>
              <input id="fp-email" type="email" required autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} data-testid="forgot-email"
                className="w-full rounded-xl border border-zinc-300 px-4 py-3 text-base" placeholder="you@example.com" />
              {err && <p className="text-sm text-red-600 mt-2" role="alert" data-testid="forgot-error">{err}</p>}
              <button type="submit" disabled={busy} data-testid="forgot-submit" className="mt-4 w-full py-3 rounded-xl bg-[#FF6B35] text-white font-[Outfit] font-bold disabled:opacity-60">{busy ? "Sending…" : "Send reset link"}</button>
              {cfg?.google_client_id && <p className="text-xs text-zinc-500 mt-3 text-center">Signed up with Google? Go back and tap <b>Continue with Google</b>. You do not need a password.</p>}
            </form>
          )
        ) : (
          <>
            <p className="text-zinc-500 text-sm text-center mt-2 mb-6">We cannot email reset links yet. Here is what you can do.</p>
            {cfg?.google_client_id && (
              <div className="rounded-2xl border border-zinc-200 p-4 mb-3 text-sm" data-testid="forgot-google">
                <b className="font-[Outfit]">Did you sign up with Google?</b>
                <p className="text-zinc-600 mt-1">Go back and tap <b>Continue with Google</b>. You do not need a password.</p>
              </div>
            )}
            <div className="rounded-2xl border border-zinc-200 p-4 mb-3 text-sm">
              <b className="font-[Outfit]">Signed up with email and password?</b>
              <p className="text-zinc-600 mt-1">
                {cfg?.support_email
                  ? <>Write to <a href={`mailto:${cfg.support_email}?subject=FinLearn%20password%20help`} className="text-[#FF6B35] font-semibold underline" data-testid="forgot-support">{cfg.support_email}</a> from the email you signed up with and we will help you get back in.</>
                  : "Please contact support from the email you signed up with and we will help you get back in."}
              </p>
            </div>
            <div className="rounded-2xl border border-zinc-200 p-4 text-sm">
              <b className="font-[Outfit]">Just starting out?</b>
              <p className="text-zinc-600 mt-1">You can also create a new account. It takes 30 seconds.</p>
            </div>
          </>
        )}

        <div className="flex gap-3 mt-6">
          <Link to="/login" data-testid="back-to-login" className="flex-1 text-center py-3 rounded-xl bg-[#FF6B35] text-white font-[Outfit] font-bold">Back to login</Link>
          <Link to="/signup" className="flex-1 text-center py-3 rounded-xl bg-zinc-100 text-zinc-800 font-[Outfit] font-bold">Create account</Link>
        </div>
      </div>
    </div>
  );
}
