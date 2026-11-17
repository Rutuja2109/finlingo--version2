import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Snowflake } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import Lumi from "@/components/Lumi";
import { useTranslation, Trans } from "react-i18next";

const MILESTONES = [3, 7, 14, 30];

// A proud moment (a streak milestone) is the best time to mention Pro: once per milestone, easy to dismiss, honest about the price.
export default function MilestoneModal() {
  const { t } = useTranslation();
  const { stats, sub, isPro } = useAuth();
  const nav = useNavigate();
  const [n, setN] = useState(null);
  const streak = stats?.streak_days || 0;

  useEffect(() => {
    if (!sub || isPro || sub.admin || stats?.streak_broken || !MILESTONES.includes(streak)) return;
    try { if (localStorage.getItem(`fl_ms_${streak}`)) return; } catch { return; }
    setN(streak);
  }, [sub, isPro, streak, stats?.streak_broken]);

  if (!n) return null;
  const close = () => { try { localStorage.setItem(`fl_ms_${n}`, "1"); } catch { /* ignore */ } setN(null); };
  return (
    <div className="fixed inset-0 z-[60] grid place-items-end sm:place-items-center bg-black/50 px-4 pb-6" role="dialog" aria-modal="true" aria-label={`${n}-day streak`} data-testid="milestone-modal">
      <div className="w-full max-w-sm rounded-3xl bg-white p-5 text-center fade-up">
        <div className="flex justify-center -mt-14 mb-1"><Lumi size={96} mood="celebrate" /></div>
        <p className="uppercase tracking-[0.2em] text-[11px] font-bold text-[#FF6B35]">{t("milestoneModal.streak_milestone")}</p>
        <h2 className="font-[Outfit] font-black text-3xl leading-tight mt-1">{t("milestoneModal.n_day_streak", { n })}</h2>
        <p className="text-[14px] text-zinc-700 mt-2"><Trans i18nKey="milestoneModal.protect_it" components={{ b: <b /> }} /></p>
        <p className="mt-2 inline-flex items-center gap-1.5 rounded-full bg-blue-50 text-blue-700 text-[12px] font-bold px-3 py-1"><Snowflake className="w-3.5 h-3.5" />{t("milestoneModal.plus_every_lesson_and_tool_49")}</p>
        <button onClick={() => { close(); nav("/pro?from=streak"); }} data-testid="milestone-see-pro" className="mt-4 w-full rounded-2xl bg-[#FF6B35] text-white font-[Outfit] font-extrabold py-3.5 active:scale-[0.98]">{t("milestoneModal.see_pro")}</button>
        <button onClick={close} data-testid="milestone-later" className="mt-2 text-[13px] font-semibold text-zinc-500">{t("milestoneModal.maybe_later")}</button>
      </div>
    </div>
  );
}
