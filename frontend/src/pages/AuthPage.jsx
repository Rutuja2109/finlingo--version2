import React, { useEffect, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import Lumi from "@/components/Lumi";
import { Eye, EyeOff } from "lucide-react";
import { api, PRIVACY_URL } from "@/lib/api";
import { googleIdToken, wasCancelled, failureHint } from "@/lib/googleLogin";

export default function AuthPage({ mode = "login" }) {
  const { login, register, loginWithGoogle } = useAuth();
  const nav = useNavigate();
  const isLogin = mode === "login";
  const [params] = useSearchParams();
  const isDemo = isLogin && params.get("demo") === "1";
  const [form, setForm] = useState({ email: isDemo ? "demo@finlingo.com" : "", password: isDemo ? "Demo@123" : "", name: "" });
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);
  const [showPw, setShowPw] = useState(false);
  const [googleId, setGoogleId] = useState(null); // set when the server has Google sign-in configured

  useEffect(() => {
    let alive = true;
    api.get("/auth/config").then((r) => { if (alive) setGoogleId(r.data?.google_client_id || null); }).catch(() => {});
    return () => { alive = false; };
  }, []);

  const google = async () => {
    setErr(""); setBusy(true);
    try {
      const idToken = await googleIdToken(googleId);
      const res = await loginWithGoogle(idToken);
      if (res.ok) nav("/dashboard"); else setErr(res.error);
    } catch (e) {
      if (!wasCancelled(e)) setErr(`Google sign-in did not work. Please try again, or use your email.${failureHint(e) ? ` (${failureHint(e)})` : ""}`);
    }
    setBusy(false);
  };

  // Login and signup share this component, so reset the form when switching screens
  // (otherwise the demo credentials carry over into the sign-up form).
  useEffect(() => {
    setForm({ email: isDemo ? "demo@finlingo.com" : "", password: isDemo ? "Demo@123" : "", name: "" });
    setErr("");
  }, [mode, isDemo]);

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
            <span className="font-[Outfit] font-black text-2xl tracking-tight">FinLearn</span>
          </Link>
          <div>
            <h1 className="font-[Outfit] font-black text-5xl leading-tight tracking-tight mb-4">
              Learn money.<br/>One choice at a time.
            </h1>
            <p className="text-white/85 max-w-md">
              Budgeting, stocks and Bitcoin through real-life situations.
              Make the call, see what happens, learn why.
            </p>
          </div>
          <div className="text-xs uppercase tracking-[0.3em] text-white/70">Master what matters</div>
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

          {googleId && (
            <>
              <button type="button" onClick={google} disabled={busy} data-testid="btn-google"
                className="w-full flex items-center justify-center gap-3 py-3 rounded-xl border border-zinc-300 bg-white hover:bg-zinc-50 font-[Outfit] font-bold tracking-tight transition active:scale-[0.98] disabled:opacity-60">
                <GoogleG /> Continue with Google
              </button>
              <div className="flex items-center gap-3 my-5 text-xs text-zinc-400 font-semibold uppercase tracking-widest">
                <span className="flex-1 h-px bg-zinc-200" />or use email<span className="flex-1 h-px bg-zinc-200" />
              </div>
            </>
          )}

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
            <div className="relative">
              <input
                type={showPw ? "text" : "password"} required minLength={6}
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                placeholder="Min 6 characters"
                autoComplete={isLogin ? "current-password" : "new-password"}
                className="w-full pl-4 pr-12 py-3 rounded-xl border border-zinc-200 outline-none focus:border-[#FF6B35] focus:ring-2 focus:ring-[#FF6B35]/20"
              />
              <button type="button" onClick={() => setShowPw((s) => !s)}
                aria-label={showPw ? "Hide password" : "Show password"} data-testid="btn-toggle-password"
                className="absolute right-1.5 top-1/2 -translate-y-1/2 w-10 h-10 grid place-items-center rounded-full text-zinc-500 hover:text-zinc-800">
                {showPw ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
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

          <p className="text-sm text-zinc-500 text-center mt-5">
            {isLogin ? "New here? " : "Have an account? "}
            <Link to={isLogin ? "/signup" : "/login"} data-testid="auth-switch" className="text-[#FF6B35] font-semibold">
              {isLogin ? "Create account" : "Log in"}
            </Link>
          </p>

          {!isLogin && (
            <p className="text-xs text-zinc-500 text-center mt-3">
              By signing up you agree to our{" "}
              <a href={PRIVACY_URL} target="_blank" rel="noopener noreferrer" className="underline hover:text-[#FF6B35]">privacy policy</a>.
            </p>
          )}

          {isDemo && (
            <p className="text-xs text-zinc-500 text-center mt-3">
              Demo account prefilled — just tap Log in.
            </p>
          )}
        </form>
      </div>
    </div>
  );
}

// Google's multicolour "G" (brand guidelines: keep the colours as they are)
function GoogleG() {
  return (
    <svg width="20" height="20" viewBox="0 0 48 48" aria-hidden="true">
      <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
      <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
      <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
      <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
    </svg>
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
