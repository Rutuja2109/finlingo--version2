import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Check, ArrowRight, Gift, Hourglass, LineChart, Wallet, Flag } from "lucide-react";
import { api } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";

const STEPS = [
  { key: "trades", label: "Make a practice trade", to: "/practice", Icon: LineChart },
  { key: "spends", label: "Log a spend in My money", to: "/money", Icon: Wallet },
  { key: "missions", label: "Start a real-life mission", to: "/missions", Icon: Flag },
];

// During the free week: a short "try these" list (people subscribe after using a Pro feature, not after reading about it).
// In the last 2 days and after the trial: what they made and that it is saved, with a clear way to keep it.
export default function TrialCard() {
  const { sub } = useAuth();
  const [u, setU] = useState(null);
  const t = sub?.trial;
  const on = !!(t && (t.active || t.ended)) && !sub?.admin && !(sub?.pro && !t.active);

  useEffect(() => {
    if (on) api.get("/subscription/usage").then((r) => setU(r.data)).catch(() => {});
  }, [on]);
  if (!on || !u) return null;

  const tried = STEPS.filter((s) => u[s.key] > 0).length;
  const parts = [];
  if (u.trades > 0) parts.push(`${u.trades} practice trade${u.trades === 1 ? "" : "s"}`);
  if (u.spends > 0) parts.push(`${u.spends} spend${u.spends === 1 ? "" : "s"} logged`);
  if (u.goals > 0) parts.push(`${u.goals} savings goal${u.goals === 1 ? "" : "s"}`);
  if (u.missions > 0) parts.push(`${u.missions} mission${u.missions === 1 ? "" : "s"}`);
  const made = parts.join(", ");

  // Last 2 days, or over: say what they would keep.
  if (t.ended || t.days_left <= 2) {
    return (
      <section className="mb-6 rounded-3xl border-2 border-violet-200 bg-gradient-to-br from-violet-50 to-pink-50 p-4" data-testid="trial-card-ending">
        <div className="flex items-center gap-3">
          <span className="w-11 h-11 rounded-2xl grid place-items-center bg-violet-600 text-white shrink-0"><Hourglass className="w-5 h-5" /></span>
          <div className="flex-1 min-w-0">
            <p className="font-[Outfit] font-black text-[17px] leading-tight">{t.ended ? "Your Pro trial has ended" : `Your Pro trial ends in ${t.days_left} day${t.days_left === 1 ? "" : "s"}`}</p>
            <p className="text-[13px] text-zinc-700 mt-0.5">
              {made ? <>You made <b>{made}</b>. {t.ended ? "It is saved and comes back the moment you subscribe." : "It stays saved, and every Pro tool stays open if you keep Pro."}</>
                : "You have not tried the Pro tools yet. Try one before the trial is over."}
            </p>
          </div>
        </div>
        <Link to="/pro?from=trial" data-testid="trial-keep" className="mt-3 flex items-center justify-center gap-2 rounded-2xl bg-[#FF6B35] text-white font-[Outfit] font-extrabold py-3 active:scale-[0.98]">
          {t.ended ? "Get Pro back" : "Keep everything"} · ₹49/month <ArrowRight className="w-4 h-4" />
        </Link>
        <p className="text-[11.5px] text-zinc-600 text-center mt-1.5">One plan covers every feature. Cancel any time.</p>
      </section>
    );
  }

  if (tried === STEPS.length) return null; // they have tried everything; nothing left to nudge

  return (
    <section className="mb-6 rounded-3xl border-2 border-violet-200 bg-white p-4" data-testid="trial-checklist">
      <div className="flex items-center gap-3 mb-2.5">
        <span className="w-11 h-11 rounded-2xl grid place-items-center bg-gradient-to-br from-[#8B5CF6] to-[#EC4899] text-white shrink-0"><Gift className="w-5 h-5" /></span>
        <div className="flex-1 min-w-0">
          <p className="font-[Outfit] font-black text-[17px] leading-tight">Try these in your free week</p>
          <p className="text-[12.5px] text-zinc-600">{t.days_left} days of Pro left · {tried} of {STEPS.length} tried</p>
        </div>
      </div>
      <div className="space-y-1.5">
        {STEPS.map(({ key, label, to, Icon }) => {
          const done = u[key] > 0;
          return (
            <Link key={key} to={to} data-testid={`trial-step-${key}`} data-done={done}
              className={`flex items-center gap-3 rounded-2xl px-3 py-2.5 ${done ? "bg-emerald-50" : "bg-zinc-50 active:bg-zinc-100"}`}>
              <span className={`w-7 h-7 rounded-full grid place-items-center shrink-0 ${done ? "bg-emerald-500 text-white" : "bg-white border border-zinc-300 text-zinc-500"}`}>
                {done ? <Check className="w-4 h-4" strokeWidth={3} /> : <Icon className="w-3.5 h-3.5" />}
              </span>
              <span className={`flex-1 text-[14px] font-bold ${done ? "text-emerald-700 line-through decoration-emerald-300" : ""}`}>{label}</span>
              {!done && <ArrowRight className="w-4 h-4 text-zinc-400" />}
            </Link>
          );
        })}
      </div>
    </section>
  );
}
