import React, { useState } from "react";
import { Link } from "react-router-dom";
import { api, formatApiError } from "@/lib/api";
import Lumi from "@/components/Lumi";
import { Copy, Check, Mail } from "lucide-react";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState(null);
  const [err, setErr] = useState("");
  const [copied, setCopied] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true); setErr("");
    try {
      const { data } = await api.post("/auth/forgot-password", { email });
      // Build the full reset URL on the frontend so it matches our public origin.
      const reset_url = data.reset_path ? window.location.origin + data.reset_path : null;
      setResult({ ...data, reset_url });
    } catch (e) {
      setErr(formatApiError(e));
    } finally { setBusy(false); }
  };

  const copy = () => {
    if (!result?.reset_url) return;
    navigator.clipboard.writeText(result.reset_url);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <div className="min-h-screen grid place-items-center bg-[#FAFAFA] font-[Manrope] p-6">
      <div className="w-full max-w-md bg-white border border-zinc-200 rounded-3xl p-8 shadow-[0_30px_60px_-30px_rgba(0,0,0,0.15)]">
        <div className="flex justify-center mb-3"><Lumi size={64} mood="think"/></div>
        <h1 className="font-[Outfit] font-black text-3xl tracking-tight text-center">Forgot password?</h1>
        <p className="text-zinc-500 text-sm text-center mt-1 mb-6">Enter your email and we'll generate a reset link.</p>

        {!result ? (
          <form onSubmit={submit}>
            <label className="block mb-4">
              <span className="text-xs uppercase tracking-[0.2em] font-semibold text-zinc-500 mb-1.5 block">Email</span>
              <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)}
                data-testid="forgot-email"
                placeholder="you@work.com"
                className="w-full px-4 py-3 rounded-xl border border-zinc-200 outline-none focus:border-[#FF6B35] focus:ring-2 focus:ring-[#FF6B35]/20"/>
            </label>
            {err && <div className="text-sm text-red-600 mb-3" data-testid="forgot-error">{err}</div>}
            <button type="submit" disabled={busy} data-testid="btn-forgot-submit"
              className="w-full py-3 rounded-xl bg-[#FF6B35] hover:bg-[#FF5618] text-white font-[Outfit] font-bold disabled:opacity-60 transition active:scale-[0.98]">
              {busy ? "Generating…" : "Send reset link"}
            </button>
          </form>
        ) : (
          <div data-testid="forgot-result">
            <div className="bg-[#10B981]/10 border border-[#10B981]/30 rounded-2xl p-4 mb-4 flex gap-3">
              <Mail className="w-5 h-5 text-[#10B981] mt-0.5 shrink-0"/>
              <div>
                <p className="font-bold text-sm">{result.message}</p>
                {result.reset_url && (
                  <p className="text-xs text-zinc-500 mt-1">
                    Dev mode: copy the link below to reset your password.
                  </p>
                )}
              </div>
            </div>
            {result.reset_url && (
              <div className="bg-zinc-50 border border-zinc-200 rounded-xl p-3 mb-4 flex items-center gap-2">
                <code data-testid="dev-reset-url" className="text-xs text-zinc-700 truncate flex-1 font-mono">{result.reset_url}</code>
                <button onClick={copy} data-testid="btn-copy-reset"
                  className="shrink-0 px-3 py-1.5 rounded-lg bg-zinc-900 text-white text-xs font-bold inline-flex items-center gap-1">
                  {copied ? <><Check className="w-3 h-3"/> Copied</> : <><Copy className="w-3 h-3"/> Copy</>}
                </button>
              </div>
            )}
            {result.reset_path && (
              <Link to={result.reset_path} data-testid="link-reset"
                className="block w-full text-center py-3 rounded-xl bg-zinc-900 text-white font-[Outfit] font-bold">
                Open reset link →
              </Link>
            )}
          </div>
        )}

        <p className="text-sm text-zinc-500 text-center mt-5">
          Remembered it? <Link to="/login" data-testid="back-to-login" className="text-[#FF6B35] font-semibold">Back to login</Link>
        </p>
      </div>
    </div>
  );
}
