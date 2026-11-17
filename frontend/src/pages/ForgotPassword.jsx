import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, formatApiError } from "@/lib/api";
import Lumi from "@/components/Lumi";
import { useTranslation, Trans } from "react-i18next";

// When the server can send email, this is a normal "send me a reset link" form. When it cannot, it says what to do instead.
// (The server never returns a reset link to the person asking: the link only goes to the email's owner.)
export default function ForgotPassword() {
  const { t } = useTranslation();
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
        <h1 className="font-[Outfit] font-black text-3xl tracking-tight text-center">{t("forgotPassword.forgot_your_password")}</h1>

        {cfg?.email_reset ? (
          sent ? (
            <div className="mt-5" data-testid="forgot-sent">
              <div className="rounded-2xl bg-emerald-50 border border-emerald-200 p-4 text-sm text-emerald-900">
                <b className="font-[Outfit]">{t("forgotPassword.check_your_email")}</b> {t("forgotPassword.if_that_address_has_a_finlearn")} </div>
              <p className="text-zinc-600 text-sm mt-3">{t("forgotPassword.opened_the_link_on_this_phone")}</p>
            </div>
          ) : (
            <form onSubmit={submit} className="mt-4" data-testid="forgot-form">
              <p className="text-zinc-500 text-sm text-center mb-4">{t("forgotPassword.type_the_email_you_signed_up")}</p>
              <label htmlFor="fp-email" className="block text-sm font-semibold mb-1">{t("forgotPassword.email")}</label>
              <input id="fp-email" type="email" required autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} data-testid="forgot-email"
                className="w-full rounded-xl border border-zinc-300 px-4 py-3 text-base" placeholder={t("forgotPassword.you_example_com")} />
              {err && <p className="text-sm text-red-600 mt-2" role="alert" data-testid="forgot-error">{err}</p>}
              <button type="submit" disabled={busy} data-testid="forgot-submit" className="mt-4 w-full py-3 rounded-xl bg-[#FF6B35] text-white font-[Outfit] font-bold disabled:opacity-60">{busy ? t("forgotPassword.sending") : t("forgotPassword.send_reset_link")}</button>
              {cfg?.google_client_id && <p className="text-xs text-zinc-500 mt-3 text-center"><Trans i18nKey="forgotPassword.google_hint_long" components={{ b: <b /> }} /></p>}
            </form>
          )
        ) : (
          <>
            <p className="text-zinc-500 text-sm text-center mt-2 mb-6">{t("forgotPassword.we_cannot_email_reset_links_yet")}</p>
            {cfg?.google_client_id && (
              <div className="rounded-2xl border border-zinc-200 p-4 mb-3 text-sm" data-testid="forgot-google">
                <b className="font-[Outfit]">{t("forgotPassword.did_you_sign_up_with_google")}</b>
                <p className="text-zinc-600 mt-1"><Trans i18nKey="forgotPassword.google_hint" components={{ b: <b /> }} /></p>
              </div>
            )}
            <div className="rounded-2xl border border-zinc-200 p-4 mb-3 text-sm">
              <b className="font-[Outfit]">{t("forgotPassword.signed_up_with_email_and_password")}</b>
              <p className="text-zinc-600 mt-1">
                {cfg?.support_email
                  ? <>Write to <a href={`mailto:${cfg.support_email}?subject=FinLearn%20password%20help`} className="text-[#FF6B35] font-semibold underline" data-testid="forgot-support">{cfg.support_email}</a> from the email you signed up with and we will help you get back in.</>
                  : t("forgotPassword.please_contact_support_from_the_email")}
              </p>
            </div>
            <div className="rounded-2xl border border-zinc-200 p-4 text-sm">
              <b className="font-[Outfit]">{t("forgotPassword.just_starting_out")}</b>
              <p className="text-zinc-600 mt-1">{t("forgotPassword.you_can_also_create_a_new")}</p>
            </div>
          </>
        )}

        <div className="flex gap-3 mt-6">
          <Link to="/login" data-testid="back-to-login" className="flex-1 text-center py-3 rounded-xl bg-[#FF6B35] text-white font-[Outfit] font-bold">{t("forgotPassword.back_to_login")}</Link>
          <Link to="/signup" className="flex-1 text-center py-3 rounded-xl bg-zinc-100 text-zinc-800 font-[Outfit] font-bold">{t("forgotPassword.create_account")}</Link>
        </div>
      </div>
    </div>
  );
}
