import React, { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { Crown, Check, ChevronLeft, LineChart, Wallet, Target, Calculator, BookOpen, Skull } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { buy, restore, cancelled, manage, isNative, livePrices } from "@/lib/billing";
import { formatApiError } from "@/lib/api";
import Lumi from "@/components/Lumi";

const PERKS = [
  { Icon: BookOpen, t: "Every lesson in every course" },
  { Icon: LineChart, t: "Practice trading with virtual money" },
  { Icon: Wallet, t: "My money: budgets and goals" },
  { Icon: Target, t: "Real-life missions" },
  { Icon: Calculator, t: "All the calculators" },
  { Icon: Skull, t: "Boss battles after each chapter" },
];
const FROM = { practice: "Practice trading", money: "My money", missions: "Missions", calculators: "Calculators", boss: "Boss battles" };

export default function Paywall() {
  const nav = useNavigate();
  const [params] = useSearchParams();
  const { sub, isPro, refreshSub } = useAuth();
  const [plan, setPlan] = useState("yearly");
  const [live, setLive] = useState({});
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  const from = FROM[params.get("from")];

  useEffect(() => { refreshSub(); }, [refreshSub]);
  useEffect(() => {
    if (!sub || !isNative()) return;
    livePrices(sub.product_id).then((ps) => {
      // Google returns the localised price text; keep it only when it is plainly there.
      const p = ps[0]; if (p?.priceString) setLive({ any: p.priceString });
    });
  }, [sub]);

  const plans = sub?.plans || [];
  const chosen = plans.find((p) => p.id === plan) || plans[0];
  const native = isNative();
  const ready = native && sub?.billing_ready;

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

  return (
    <div className="max-w-lg mx-auto pb-28" data-testid="paywall">
      <button onClick={() => nav(-1)} className="inline-flex items-center gap-1 text-sm text-zinc-500 mb-4"><ChevronLeft className="w-4 h-4" /> Back</button>

      <div className="rounded-3xl bg-gradient-to-br from-[#FF6B35] via-[#F59E0B] to-[#EC4899] text-white p-6 relative overflow-hidden mb-5">
        <div className="absolute -right-2 -bottom-2 opacity-40 pointer-events-none"><Lumi size={110} mood="cheer" /></div>
        <p className="uppercase tracking-[0.2em] text-[11px] font-bold text-white/90 mb-1"><Crown className="w-3.5 h-3.5 inline -mt-0.5 mr-1" />FinLearn Pro</p>
        <h1 className="font-[Outfit] font-black text-3xl leading-tight max-w-[75%]">{from ? `${from} is a Pro feature` : "Learn all of money, for less than a chai a day"}</h1>
      </div>

      {isPro ? (
        <div className="bg-emerald-50 border-2 border-emerald-300 rounded-3xl p-5 text-center" data-testid="pro-active">
          <p className="font-[Outfit] font-extrabold text-xl mb-1">You are Pro</p>
          <p className="text-sm text-zinc-600 mb-4">{sub?.admin ? "Admin access" : sub?.until ? `Active until ${new Date(sub.until).toLocaleDateString()}` : ""}</p>
          {native && !sub?.admin && <button onClick={manage} className="rounded-xl border border-zinc-300 bg-white px-4 py-2 font-bold text-sm">Manage or cancel in Google Play</button>}
        </div>
      ) : (
        <>
          <ul className="bg-white border border-zinc-200 rounded-3xl p-4 mb-5 space-y-3">
            {PERKS.map(({ Icon, t }) => (
              <li key={t} className="flex items-center gap-3 font-semibold text-[15px]">
                <span className="w-9 h-9 rounded-xl bg-amber-50 text-amber-600 grid place-items-center shrink-0"><Icon className="w-5 h-5" /></span>{t}
              </li>
            ))}
            <li className="text-[13px] text-zinc-500 pt-1">Free forever: {sub?.free_concepts || 2} lessons per course, daily quests and the idea of the day.</li>
          </ul>

          <div className="grid gap-3 mb-4" role="radiogroup" aria-label="Plan">
            {plans.map((p) => (
              <button key={p.id} role="radio" aria-checked={plan === p.id} onClick={() => setPlan(p.id)} data-testid={`plan-${p.id}`}
                className={`text-left rounded-2xl border-2 p-4 flex items-center gap-3 ${plan === p.id ? "border-[#FF6B35] bg-orange-50" : "border-zinc-200 bg-white"}`}>
                <span className={`w-6 h-6 rounded-full border-2 grid place-items-center shrink-0 ${plan === p.id ? "border-[#FF6B35] bg-[#FF6B35] text-white" : "border-zinc-300"}`}>{plan === p.id && <Check className="w-4 h-4" strokeWidth={3} />}</span>
                <span className="flex-1">
                  <span className="block font-[Outfit] font-extrabold text-lg">{p.label} <span className="text-zinc-500 font-bold text-base">₹{p.price}/{p.per}</span></span>
                  <span className="block text-[13px] text-zinc-600">{p.note}</span>
                </span>
              </button>
            ))}
          </div>

          <button onClick={start} disabled={!ready || busy} data-testid="btn-subscribe"
            className="w-full rounded-2xl bg-[#FF6B35] disabled:bg-zinc-300 text-white font-[Outfit] font-extrabold text-lg py-4 active:scale-[0.98]">
            {busy ? "Please wait…" : chosen ? `Go Pro · ₹${chosen.price}/${chosen.per}` : "Go Pro"}
          </button>
          {!native && <p className="text-[13px] text-zinc-600 text-center mt-2">To subscribe, open FinLearn in the Android app.</p>}
          {native && sub && !sub.billing_ready && <p className="text-[13px] text-zinc-600 text-center mt-2">Purchases are not switched on yet. Please check back soon.</p>}
          {live.any && <p className="text-[12px] text-zinc-500 text-center mt-2">Google Play shows the final price for your country before you pay.</p>}

          <div className="text-[12px] text-zinc-500 leading-relaxed mt-4 space-y-1.5" data-testid="pro-terms">
            <p>Your subscription renews automatically every {chosen?.per || "period"} at ₹{chosen?.price} until you cancel. Payment is charged to your Google Play account (UPI AutoPay or card).</p>
            <p>Cancel any time: Google Play, then Payments and subscriptions, then Subscriptions, then FinLearn. You keep Pro until the end of the period you paid for.</p>
          </div>
          {native && <button onClick={doRestore} disabled={busy} className="block mx-auto mt-4 text-sm font-bold text-[#FF6B35] underline">Restore my purchase</button>}
        </>
      )}
      {msg && <p className="text-center font-bold text-sm mt-4" role="status" data-testid="pro-msg">{msg}</p>}
    </div>
  );
}
