import React, { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Crown, Check, X, LineChart, Wallet, Target, Calculator, BookOpen, Skull, Gift } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { buy, restore, cancelled, manage, isNative } from "@/lib/billing";
import { formatApiError } from "@/lib/api";
import Lumi from "@/components/Lumi";

// What the learner just tried to open decides the headline and the first benefit (the pitch matches the moment).
const WHY = {
  lessons: { h: "Keep learning without limits", first: "Every lesson in every course", Icon: BookOpen },
  courses: { h: "Keep learning without limits", first: "Every lesson in every course", Icon: BookOpen },
  practice: { h: "Trade with ₹1,00,000 of virtual money", first: "Practice trading with virtual money", Icon: LineChart },
  money: { h: "Know where every rupee goes", first: "My money: budgets and goals", Icon: Wallet },
  missions: { h: "Turn learning into real money habits", first: "Real-life missions", Icon: Target },
  calculators: { h: "Plan your money with real numbers", first: "SIP, EMI and savings calculators", Icon: Calculator },
  boss: { h: "Prove you have got it", first: "Boss battles after each chapter", Icon: Skull },
};
const PERKS = [
  { Icon: BookOpen, t: "Every lesson in every course" },
  { Icon: LineChart, t: "Practice trading with virtual money" },
  { Icon: Wallet, t: "My money: budgets and goals" },
  { Icon: Target, t: "Real-life missions" },
  { Icon: Calculator, t: "SIP, EMI and savings calculators" },
  { Icon: Skull, t: "Boss battles after each chapter" },
];

export default function Paywall() {
  const nav = useNavigate();
  const [params] = useSearchParams();
  const { sub, isPro, refreshSub } = useAuth();
  const [plan, setPlan] = useState("yearly");
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  const why = WHY[params.get("from")];

  useEffect(() => { refreshSub(); }, [refreshSub]);

  const plans = sub?.plans || [];
  const chosen = plans.find((p) => p.id === plan) || plans[0];
  const native = isNative();
  const ready = native && sub?.billing_ready;
  const t = sub?.trial || {};
  const paid = isPro && !t.active; // a real (paid or granted) Pro, not a trial

  const start = async () => {
    if (!chosen || busy) return;
    setBusy(true); setMsg("");
    try {
      await buy(sub.product_id, chosen.base_plan);
      await refreshSub();
      setMsg("You are Pro now. Enjoy!");
    } catch (e) {
      if (!cancelled(e)) setMsg(formatApiError(e) || "The purchase did not go through. You were not charged unless Google says so.");
    }
    setBusy(false);
  };
  const doRestore = async () => {
    setBusy(true); setMsg("");
    try { setMsg((await restore(sub.product_id)) ? "Your Pro plan is back." : "No active purchase found for this Google account."); await refreshSub(); }
    catch { setMsg("Could not check Google Play. Please try again."); }
    setBusy(false);
  };

  const headline = t.active ? `${t.days_left} day${t.days_left === 1 ? "" : "s"} of Pro left. Keep it?`
    : why ? why.h : t.ended ? "Welcome back. Get Pro again" : "Learn all of money, for less than a chai a day";
  const perks = why ? [{ Icon: why.Icon, t: why.first }, ...PERKS.filter((p) => p.t !== why.first)] : PERKS;

  return (
    <div className="max-w-lg mx-auto pb-56" data-testid="paywall">
      <button onClick={() => nav(-1)} data-testid="paywall-close" aria-label="Close" className="mb-3 w-9 h-9 rounded-full bg-zinc-100 grid place-items-center"><X className="w-4 h-4" /></button>

      <div className="rounded-3xl bg-gradient-to-br from-[#FF6B35] via-[#F59E0B] to-[#EC4899] text-white p-6 relative overflow-hidden mb-5">
        <div className="absolute -right-2 -bottom-2 opacity-40 pointer-events-none"><Lumi size={110} mood="cheer" /></div>
        <p className="uppercase tracking-[0.2em] text-[11px] font-bold text-white/90 mb-1">
          {t.active ? <Gift className="w-3.5 h-3.5 inline -mt-0.5 mr-1" /> : <Crown className="w-3.5 h-3.5 inline -mt-0.5 mr-1" />}FinLearn Pro
        </p>
        <h1 className="font-[Outfit] font-black text-[28px] leading-tight max-w-[78%]" data-testid="paywall-headline">{headline}</h1>
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
            <div className="rounded-2xl bg-violet-50 border-2 border-violet-200 p-3.5 mb-4 text-[13.5px] text-zinc-700" data-testid="trial-note">
              <b>Your free trial is running.</b> Everything is unlocked until {new Date(t.ends_at).toLocaleDateString()}. Subscribe now so you do not lose your lessons, trades and goals.
            </div>
          )}

          <ul className="bg-white border border-zinc-200 rounded-3xl p-4 mb-5 space-y-3">
            {perks.map(({ Icon, t: label }, i) => (
              <li key={label} className={`flex items-center gap-3 font-semibold text-[15px] ${i === 0 && why ? "text-[#FF6B35]" : ""}`}>
                <span className="w-9 h-9 rounded-xl bg-amber-50 text-amber-600 grid place-items-center shrink-0"><Icon className="w-5 h-5" /></span>{label}
                <Check className="w-4 h-4 text-emerald-500 ml-auto shrink-0" strokeWidth={3} />
              </li>
            ))}
            <li className="text-[13px] text-zinc-500 pt-1">Free forever: {sub?.free_concepts || 2} lessons per course, daily quests and the idea of the day.</li>
          </ul>

          <div className="grid gap-3 mb-4" role="radiogroup" aria-label="Plan">
            {plans.map((p) => (
              <button key={p.id} role="radio" aria-checked={plan === p.id} onClick={() => setPlan(p.id)} data-testid={`plan-${p.id}`}
                className={`relative text-left rounded-2xl border-2 p-4 flex items-center gap-3 ${plan === p.id ? "border-[#FF6B35] bg-orange-50" : "border-zinc-200 bg-white"}`}>
                {p.badge && <span className="absolute -top-2.5 right-4 rounded-full bg-[#FF6B35] text-white text-[10px] font-black px-2.5 py-0.5">{p.badge} · SAVE {p.save_pct}%</span>}
                <span className={`w-6 h-6 rounded-full border-2 grid place-items-center shrink-0 ${plan === p.id ? "border-[#FF6B35] bg-[#FF6B35] text-white" : "border-zinc-300"}`}>{plan === p.id && <Check className="w-4 h-4" strokeWidth={3} />}</span>
                <span className="flex-1">
                  <span className="block font-[Outfit] font-extrabold text-lg">{p.label}</span>
                  <span className="block text-[13px] text-zinc-600">{p.note}</span>
                </span>
                <span className="text-right">
                  {p.was && <span className="block text-[12px] text-zinc-400 line-through">₹{p.was}</span>}
                  <span className="block font-[Outfit] font-extrabold text-xl">₹{p.price}<span className="text-[12px] text-zinc-500 font-bold">/{p.per}</span></span>
                </span>
              </button>
            ))}
          </div>

          <div className="text-[12px] text-zinc-500 leading-relaxed space-y-1.5" data-testid="pro-terms">
            <p>Renews automatically every {chosen?.per || "period"} at ₹{chosen?.price} until you cancel. Payment is charged to your Google Play account (UPI AutoPay or card).</p>
            <p>Cancel any time: Google Play, then Payments and subscriptions, then Subscriptions, then FinLearn. You keep Pro until the end of the period you paid for.</p>
          </div>
          {native && <button onClick={doRestore} disabled={busy} className="block mx-auto mt-4 text-sm font-bold text-[#FF6B35] underline">Restore my purchase</button>}
        </>
      )}
      {msg && <p className="text-center font-bold text-sm mt-4" role="status" data-testid="pro-msg">{msg}</p>}

      {!paid && (
        <div className="fixed bottom-[64px] lg:bottom-0 inset-x-0 z-30 bg-white/95 backdrop-blur border-t border-zinc-200 px-5 pt-3 pb-3">
          <div className="max-w-lg mx-auto">
            <button onClick={start} disabled={!ready || busy} data-testid="btn-subscribe"
              className="w-full rounded-2xl bg-[#FF6B35] disabled:bg-zinc-300 text-white font-[Outfit] font-extrabold text-lg py-4 active:scale-[0.98]">
              {busy ? "Please wait…" : chosen ? `Get Pro · ₹${chosen.price}/${chosen.per}` : "Get Pro"}
            </button>
            {!native && <p className="text-[12px] text-zinc-600 text-center mt-1.5">To subscribe, open FinLearn in the Android app.</p>}
            {native && sub && !sub.billing_ready && <p className="text-[12px] text-zinc-600 text-center mt-1.5">Purchases are not switched on yet. Please check back soon.</p>}
            <button onClick={() => nav(-1)} className="block mx-auto mt-1.5 text-[13px] font-semibold text-zinc-500">{t.active ? "Keep using my trial" : "Not now"}</button>
          </div>
        </div>
      )}
    </div>
  );
}
