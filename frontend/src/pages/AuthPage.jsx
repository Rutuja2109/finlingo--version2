import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import Lumi from "@/components/Lumi";

export default function AuthPage({ mode = "login" }) {
  const { login, register } = useAuth();
  const nav = useNavigate();
  const isLogin = mode === "login";
  const [form, setForm] = useState({ email: isLogin ? "demo@finlingo.com" : "", password: isLogin ? "Demo@123" : "", name: "" });
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setErr(""); setBusy(true);
    const res = isLogin
      ? await login(form.email, form.password)
      : await register(form.email, form.password, form.name);
    setBusy(false);
    if (res.ok) nav("/dashboard");
    else setErr(res.error);
  };

  return (
    <div className="min-h-screen flex flex-col md:flex-row bg-[#FAFAFA] font-[Manrope]">
      {/* Left visual */}
      <div className="hidden md:flex md:w-1/2 relative bg-gradient-to-br from-[#FF6B35] via-[#FF8A4C] to-[#FFB088] p-12 text-white overflow-hidden">
        <div className="absolute -top-20 -left-20 w-96 h-96 rounded-full bg-white/10 blur-3xl" />
        <div className="absolute bottom-0 right-0 w-[28rem] h-[28rem] rounded-full bg-[#EC4899]/30 blur-3xl" />
        <div className="relative z-10 flex flex-col justify-between h-full">
          <Link to="/" className="flex items-center gap-3" data-testid="auth-brand">
            <Lumi size={44} />
            <span className="font-[Outfit] font-black text-2xl tracking-tight">FinLingo</span>
          </Link>
          <div>
            <h1 className="font-[Outfit] font-black text-5xl leading-tight tracking-tighter mb-4">
              Master certifications.<br/>One concept at a time.
            </h1>
            <p className="text-white/85 max-w-md">
              Built for LOMA, CFA, FRM, PMP, AWS and beyond. Interactive lessons,
              real XP, real progress — no more PDFs.
            </p>
          </div>
          <div className="text-xs uppercase tracking-[0.3em] text-white/70">Phase 1 · Platform Shell</div>
        </div>
      </div>

      {/* Right form */}
      <div className="flex-1 grid place-items-center p-6">
        <form onSubmit={submit} className="w-full max-w-md bg-white border border-zinc-200 rounded-3xl p-8 shadow-[0_30px_60px_-30px_rgba(0,0,0,0.15)]">
          <div className="flex md:hidden justify-center mb-4"><Lumi size={56}/></div>
          <h2 className="font-[Outfit] font-black text-3xl tracking-tight">
            {isLogin ? "Welcome back" : "Create your account"}
          </h2>
          <p className="text-zinc-500 text-sm mt-1 mb-6">
            {isLogin ? "Continue your mastery journey." : "Start learning in 30 seconds."}
          </p>

          {!isLogin && (
            <Field label="Name" testid="input-name">
              <input
                required minLength={1}
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                placeholder="Ada Lovelace"
                className="w-full px-4 py-3 rounded-xl border border-zinc-200 outline-none focus:border-[#FF6B35] focus:ring-2 focus:ring-[#FF6B35]/20"
              />
            </Field>
          )}

          <Field label="Email" testid="input-email">
            <input
              type="email" required
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              placeholder="you@work.com"
              className="w-full px-4 py-3 rounded-xl border border-zinc-200 outline-none focus:border-[#FF6B35] focus:ring-2 focus:ring-[#FF6B35]/20"
            />
          </Field>

          <Field label="Password" testid="input-password">
            <input
              type="password" required minLength={6}
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              placeholder="Min 6 characters"
              className="w-full px-4 py-3 rounded-xl border border-zinc-200 outline-none focus:border-[#FF6B35] focus:ring-2 focus:ring-[#FF6B35]/20"
            />
          </Field>

          {err && (
            <div data-testid="auth-error" className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-xl px-3 py-2 mb-3">
              {err}
            </div>
          )}

          <button
            type="submit" disabled={busy}
            data-testid="btn-submit-auth"
            className="w-full py-3 rounded-xl bg-[#FF6B35] hover:bg-[#FF5618] text-white font-[Outfit] font-bold tracking-tight transition active:scale-[0.98] disabled:opacity-60"
          >
            {busy ? "Please wait…" : isLogin ? "Log in" : "Sign up"}
          </button>

          {isLogin && (
            <div className="mt-2 text-right">
              <Link to="/forgot-password" data-testid="link-forgot" className="text-xs text-zinc-500 hover:text-[#FF6B35] font-semibold">
                Forgot password?
              </Link>
            </div>
          )}

          {/* Divider */}
          <div className="flex items-center gap-3 my-5">
            <div className="h-px flex-1 bg-zinc-200"/>
            <span className="text-xs uppercase tracking-[0.2em] font-bold text-zinc-400">or</span>
            <div className="h-px flex-1 bg-zinc-200"/>
          </div>

          {/* REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH */}
          <button type="button" data-testid="btn-google"
            onClick={() => {
              const redirectUrl = window.location.origin + "/dashboard";
              window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
            }}
            className="w-full py-3 rounded-xl border-2 border-zinc-200 hover:border-zinc-400 bg-white font-[Outfit] font-bold tracking-tight inline-flex items-center justify-center gap-2.5 transition active:scale-[0.98]">
            <GoogleG/>
            Continue with Google
          </button>

          <p className="text-sm text-zinc-500 text-center mt-5">
            {isLogin ? "New here? " : "Have an account? "}
            <Link to={isLogin ? "/signup" : "/login"} data-testid="auth-switch" className="text-[#FF6B35] font-semibold">
              {isLogin ? "Create account" : "Log in"}
            </Link>
          </p>

          {isLogin && (
            <p className="text-xs text-zinc-400 text-center mt-3">
              Demo credentials prefilled · demo@finlingo.com / Demo@123
            </p>
          )}
        </form>
      </div>
    </div>
  );
}

function Field({ label, children, testid }) {
  return (
    <label className="block mb-4" data-testid={testid}>
      <span className="text-xs uppercase tracking-[0.2em] font-semibold text-zinc-500 mb-1.5 block">{label}</span>
      {children}
    </label>
  );
}

function GoogleG() {
  return (
    <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden>
      <path d="M17.64 9.2c0-.64-.06-1.25-.16-1.84H9v3.48h4.84a4.14 4.14 0 01-1.8 2.72v2.26h2.92c1.71-1.58 2.68-3.91 2.68-6.62z" fill="#4285F4"/>
      <path d="M9 18c2.43 0 4.47-.81 5.96-2.18l-2.92-2.26c-.81.54-1.84.86-3.04.86-2.34 0-4.32-1.58-5.03-3.7H.96v2.32A9 9 0 009 18z" fill="#34A853"/>
      <path d="M3.97 10.72A5.4 5.4 0 013.68 9c0-.6.1-1.18.29-1.72V4.96H.96A9 9 0 000 9c0 1.45.35 2.83.96 4.04l3.01-2.32z" fill="#FBBC04"/>
      <path d="M9 3.58c1.32 0 2.5.45 3.44 1.35l2.58-2.58A9 9 0 009 0 9 9 0 00.96 4.96l3.01 2.32C4.68 5.16 6.66 3.58 9 3.58z" fill="#EA4335"/>
    </svg>
  );
}
