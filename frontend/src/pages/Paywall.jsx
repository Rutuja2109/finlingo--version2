import React, { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Crown, Check, X, LineChart, Wallet, Target, Calculator, BookOpen, Skull, Gift, Snowflake, Award, ShieldCheck, ChevronDown } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { buy, restore, cancelled, manage, isNative } from "@/lib/billing";
import { formatApiError, PRIVACY_URL, TERMS_URL } from "@/lib/api";
import Lumi from "@/components/Lumi";
import ProWelcome from "@/components/ProWelcome";

// What the learner just tried to open decides the headline and the first benefit (the pitch matches the moment).
const WHY = {
  lessons: { h: "Keep learning without limits", first: "Every lesson", Icon: BookOpen },
  courses: { h: "Keep learning without limits", first: "Every lesson", Icon: BookOpen },
  wall: { h: "You finished the free lessons!", first: "Every lesson", Icon: BookOpen },
  streak: { h: "Protect your streak and keep going", first: "5 streak freezes", Icon: Snowflake },
  trial: { h: "Keep everything you tried", first: "Practice trading", Icon: LineChart },
  practice: { h: "Trade with ₹1,00,000 of virtual money", first: "Practice trading", Icon: LineChart },
  money: { h: "Know where every rupee goes", first: "My money", Icon: Wallet },
  missions: { h: "Turn learning into real money habits", first: "Real-life missions", Icon: Target },
  calculators: { h: "Plan your money with real numbers", first: "Calculators", Icon: Calculator },
  boss: { h: "Prove you have got it", first: "Boss battles", Icon: Skull },
};
const CHIPS = [
  { Icon: BookOpen, t: "Every lesson" },
  { Icon: LineChart, t: "Practice trading" },
  { Icon: Wallet, t: "My money" },
  { Icon: Target, t: "Missions" },
  { Icon: Calculator, t: "Calculators" },
  { Icon: Skull, t: "Boss battles" },
];
const EVERYTHING = [
  { Icon: BookOpen, t: "Every lesson in every course" },
  { Icon: LineChart, t: "Practice trading with virtual money" },
  { Icon: Wallet, t: "My money: budgets and goals" },
  { Icon: Target, t: "Real-life missions" },
  { Icon: Calculator, t: "SIP, EMI and savings calculators" },
  { Icon: Skull, t: "Boss battles after each chapter" },
  { Icon: Snowflake, t: "5 streak freezes (free accounts get 2)" },
  { Icon: Award, t: "A Pro badge on the leaderboard" },
];

export default function Paywall() {
  const nav = useNavigate();
  const [params] = useSearchParams();
  const { sub, isPro, stats, refreshSub } = useAuth();
  const [plan, setPlan] = useState("yearly");
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  const [welcome, setWelcome] = useState(false);
  const [more, setMore] = useState(false);
  const why = WHY[params.get("from")];

  useEffect(() => { refreshSub(); }, [refreshSub]);

  const plans = sub?.plans || [];
  const chosen = plans.find((p) => p.id === plan) || plans[0];
  const native = isNative();
  const ready = native && sub?.billing_ready;
  const t = sub?.trial || {};
  const paid = isPro && !t.active; // a real (paid or granted) Pro, not a trial
  const perDay = chosen ? (chosen.price / (chosen.per === "year" ? 365 : 30)).toFixed(1) : null;
  const lessons = stats?.lessons_completed || 0;
  const streak = stats?.streak_days || 0;

  const start = async () => {
    if (!chosen || busy) return;
    setBusy(true); setMsg("");
    try {
      await buy(sub.product_id, chosen.base_plan);
      await refreshSub();
      setWelcome(true);
    } catch (e) {
      if (!cancelled(e)) setMsg(formatApiError(e) || "The purchase did not go through. You were not charged unless Google says so.");
    }
    setBusy(false);
  };
  const doRestore = async () => {
    setBusy(true); setMsg("");
    try {
      const found = await restore(sub.product_id);
      await refreshSub();
      if (found) setWelcome(true); else setMsg("No active purchase found for this Google account.");
    } catch { setMsg("Could not check Google Play. Please try again."); }
    setBusy(false);
  };

  const headline = t.active ? `${t.days_left} day${t.days_left === 1 ? "" : "s"} of Pro left. Keep it?`
    : why ? why.h : t.ended ? "Welcome back. Get Pro again" : "Learn all of money, for about ₹1 a day";
  // The first chip matches what they just tried; the rest follow.
  const chips = why ? [{ Icon: why.Icon, t: why.first }, ...CHIPS.filter((c) => c.t !== why.first)].slice(0, 4) : CHIPS.slice(0, 4);
  const personal = lessons > 0 || streak > 0
    ? `You have done ${lessons} lesson${lessons === 1 ? "" : "s"}${streak > 0 ? ` and kept a ${streak}-day streak` : ""}. Keep it going.` : null;

  return (
    <div className="max-w-lg mx-auto pb-52" data-testid="paywall">
      {welcome && <ProWelcome onDone={() => nav("/dashboard", { replace: true })} />}

      <div className="flex items-center justify-between mb-2">
        <button onClick={() => nav(-1)} data-testid="paywall-close" aria-label="Close" className="w-9 h-9 rounded-full bg-zinc-100 grid place-items-center"><X className="w-4 h-4" /></button>
        <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-50 text-emerald-700 text-[11.5px] font-extrabold px-3 py-1" data-testid="one-plan-note"><ShieldCheck className="w-3.5 h-3.5" />One plan · every feature included</span>
      </div>

      <div className="rounded-3xl bg-gradient-to-br from-[#FF6B35] via-[#F59E0B] to-[#EC4899] text-white p-4 relative overflow-hidden mb-3">
        <div className="absolute -right-1 -bottom-2 opacity-35 pointer-events-none"><Lumi size={84} mood="cheer" /></div>
        <p className="uppercase tracking-[0.2em] text-[10.5px] font-bold text-white/95 mb-0.5">
          {t.active ? <Gift className="w-3.5 h-3.5 inline -mt-0.5 mr-1" /> : <Crown className="w-3.5 h-3.5 inline -mt-0.5 mr-1" />}FinLearn Pro
        </p>
        <h1 className="font-[Outfit] font-black text-[22px] leading-tight max-w-[78%]" data-testid="paywall-headline">{headline}</h1>
        {personal && !paid && <p className="text-[12.5px] text-white/95 mt-1 max-w-[80%]" data-testid="paywall-personal">{personal}</p>}
      </div>

      {paid ? (
        <div className="bg-emerald-50 border-2 border-emerald-300 rounded-3xl p-5 text-center" data-testid="pro-active">
          <p className="font-[Outfit] font-extrabold text-xl mb-1">You are Pro</p>
          <p className="text-sm text-zinc-600 mb-4">{sub?.admin ? "Admin access" : sub?.until ? `Active until ${new Date(sub.until).toLocaleDateString()}` : ""}</p>
          {native && !sub?.admin && <button onClick={manage} className="rounded-xl border border-zinc-300 bg-white px-4 py-2 font-bold text-sm">Manage or cancel in Google Play</button>}
        </div>
      ) : (
        <>
          {t.active && (
            <div className="rounded-2xl bg-violet-50 border-2 border-violet-200 px-3 py-2 mb-3 text-[12.5px] text-zinc-700" data-testid="trial-note">
              <b>Your free trial is running.</b> Everything is open until {new Date(t.ends_at).toLocaleDateString()}. Subscribe to keep it.
            </div>
          )}

          <div className="flex flex-wrap gap-1.5 mb-3" data-testid="benefit-chips">
            {chips.map(({ Icon, t: label }, i) => (
              <span key={label} className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-[12.5px] font-bold ${i === 0 && why ? "bg-orange-100 text-[#C2410C]" : "bg-zinc-100 text-zinc-700"}`}><Icon className="w-3.5 h-3.5" />{label}</span>
            ))}
            <button onClick={() => setMore((m) => !m)} data-testid="see-everything" className="inline-flex items-center gap-1 rounded-full px-3 py-1.5 text-[12.5px] font-extrabold text-[#FF6B35]">+ more<ChevronDown className={`w-3.5 h-3.5 transition ${more ? "rotate-180" : ""}`} /></button>
          </div>
          {more && (
            <ul className="bg-white border border-zinc-200 rounded-2xl p-3 mb-3 space-y-2" data-testid="everything-list">
              {EVERYTHING.map(({ Icon, t: label }) => (
                <li key={label} className="flex items-center gap-2.5 text-[13.5px] font-semibold"><Icon className="w-4 h-4 text-amber-600 shrink-0" />{label}<Check className="w-4 h-4 text-emerald-500 ml-auto shrink-0" strokeWidth={3} /></li>
              ))}
              <li className="text-[12px] text-zinc-600 pt-0.5">Free forever: {sub?.free_concepts || 2} lessons per course, daily quests and the idea of the day.</li>
            </ul>
          )}

          <div className="grid gap-2.5 mb-2" role="radiogroup" aria-label="Plan">
            {plans.map((p) => (
              <button key={p.id} role="radio" aria-checked={plan === p.id} onClick={() => setPlan(p.id)} data-testid={`plan-${p.id}`}
                className={`relative text-left rounded-2xl border-2 px-3.5 py-3 flex items-center gap-3 ${plan === p.id ? "border-[#FF6B35] bg-orange-50" : "border-zinc-200 bg-white"}`}>
                {p.badge && <span className="absolute -top-2.5 right-4 rounded-full bg-[#FF6B35] text-white text-[10px] font-black px-2.5 py-0.5">{p.badge} · SAVE {p.save_pct}%</span>}
                <span className={`w-6 h-6 rounded-full border-2 grid place-items-center shrink-0 ${plan === p.id ? "border-[#FF6B35] bg-[#FF6B35] text-white" : "border-zinc-300"}`}>{plan === p.id && <Check className="w-4 h-4" strokeWidth={3} />}</span>
                <span className="flex-1">
                  <span className="block font-[Outfit] font-extrabold text-[17px] leading-tight">{p.label}</span>
                  <span className="block text-[12.5px] text-zinc-600">{p.note}</span>
                </span>
                <span className="text-right">
                  {p.was && <span className="block text-[12px] text-zinc-500 line-through">₹{p.was}</span>}
                  <span className="block font-[Outfit] font-extrabold text-xl leading-tight">₹{p.price}<span className="text-[12px] text-zinc-600 font-bold">/{p.per}</span></span>
                </span>
              </button>
            ))}
          </div>
          {perDay && <p className="text-center text-[13px] font-bold text-zinc-700 mb-2" data-testid="per-day">That is about ₹{perDay} a day</p>}

          <p className="flex flex-wrap items-center justify-center gap-x-3 gap-y-1 text-[12px] font-bold text-zinc-600 mb-3" data-testid="trust-row">
            <span>Cancel any time</span><span aria-hidden="true">·</span><span>Billed by Google Play</span><span aria-hidden="true">·</span><span>UPI AutoPay or card</span>
          </p>

          <div className="text-[11.5px] text-zinc-600 leading-relaxed space-y-1" data-testid="pro-terms">
            <p>Renews automatically every {chosen?.per || "period"} at ₹{chosen?.price} until you cancel. Payment is charged to your Google Play account.</p>
            <p>Cancel in Google Play, then Payments and subscriptions, then Subscriptions, then FinLearn. You keep Pro until the end of the period you paid for.</p>
            <p><a href={TERMS_URL} target="_blank" rel="noopener noreferrer" className="underline font-semibold" data-testid="paywall-terms-link">Terms</a> · <a href={PRIVACY_URL} target="_blank" rel="noopener noreferrer" className="underline font-semibold">Privacy policy</a></p>
          </div>
          {native && <button onClick={doRestore} disabled={busy} className="block mx-auto mt-3 text-sm font-bold text-[#FF6B35] underline">Restore my purchase</button>}
        </>
      )}
      {msg && <p className="text-center font-bold text-sm mt-4" role="status" data-testid="pro-msg">{msg}</p>}

      {!paid && (
        <div className="fixed bottom-[64px] lg:bottom-0 inset-x-0 z-30 bg-white/95 backdrop-blur border-t border-zinc-200 px-5 pt-3 pb-3">
          <div className="max-w-lg mx-auto">
            <button onClick={start} disabled={!ready || busy} data-testid="btn-subscribe"
              className="w-full rounded-2xl bg-[#FF6B35] disabled:bg-zinc-300 text-white font-[Outfit] font-extrabold text-lg py-3.5 active:scale-[0.98]">
              {busy ? "Please wait…" : chosen ? `Get Pro · ₹${chosen.price}/${chosen.per}` : "Get Pro"}
            </button>
            {!native && <p className="text-[12px] text-zinc-600 text-center mt-1.5">To subscribe, open FinLearn in the Android app.</p>}
            {native && sub && !sub.billing_ready && <p className="text-[12px] text-zinc-600 text-center mt-1.5">Purchases are not switched on yet. Please check back soon.</p>}
            <button onClick={() => nav(-1)} className="block mx-auto mt-1 text-[13px] font-semibold text-zinc-600">{t.active ? "Keep using my trial" : "Not now"}</button>
          </div>
        </div>
      )}
    </div>
  );
}
