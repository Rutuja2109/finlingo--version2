import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "@/lib/api";
import Lumi from "@/components/Lumi";

// Password reset by email needs an email service, which the app does not have yet. Instead of a form that cannot
// deliver anything, this page says what to do. (The server never returns reset links to the person asking.)
export default function ForgotPassword() {
  const [cfg, setCfg] = useState(null);
  useEffect(() => { api.get("/auth/config").then((r) => setCfg(r.data)).catch(() => setCfg({})); }, []);

  return (
    <div className="min-h-screen grid place-items-center bg-[#FAFAFA] font-[Manrope] p-6">
      <div className="w-full max-w-md bg-white border border-zinc-200 rounded-3xl p-8 shadow-[0_30px_60px_-30px_rgba(0,0,0,0.15)]" data-testid="forgot-page">
        <div className="flex justify-center mb-4"><Lumi size={72} mood="nervous" /></div>
        <h1 className="font-[Outfit] font-black text-3xl tracking-tight text-center">Forgot your password?</h1>
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

        <div className="flex gap-3 mt-6">
          <Link to="/login" data-testid="back-to-login" className="flex-1 text-center py-3 rounded-xl bg-[#FF6B35] text-white font-[Outfit] font-bold">Back to login</Link>
          <Link to="/signup" className="flex-1 text-center py-3 rounded-xl bg-zinc-100 text-zinc-800 font-[Outfit] font-bold">Create account</Link>
        </div>
      </div>
    </div>
  );
}
