import React from "react";
import { Link } from "react-router-dom";
import { BookOpen, LineChart, Wallet, Flag, Calculator, Skull, Target, Lightbulb, Lock } from "lucide-react";
import { useAuth } from "@/context/AuthContext";

// "Everything in FinLearn": every feature in one scroll row, so nothing stays hidden. Free vs Pro is visible at a glance.
const ITEMS = [
  { to: "/courses", Icon: BookOpen, t: "Courses", d: "Money, stocks, tax, investing", c: "#2563EB", pro: false, note: "2 lessons free per course" },
  { key: "practice", to: "/practice", Icon: LineChart, t: "Practice trading", d: "₹1,00,000 of virtual money", c: "#EC4899", pro: true },
  { key: "money", to: "/money", Icon: Wallet, t: "My money", d: "Budgets, spends and goals", c: "#6366F1", pro: true },
  { key: "missions", to: "/missions", Icon: Flag, t: "Missions", d: "Real-life money actions", c: "#F43F5E", pro: true },
  { key: "calculators", to: "/calculators", Icon: Calculator, t: "Calculators", d: "SIP, EMI, emergency fund", c: "#10B981", pro: true },
  { key: "boss", to: "/courses", Icon: Skull, t: "Boss battles", d: "Test yourself each chapter", c: "#7C3AED", pro: true },
  { to: "/explainer", Icon: Lightbulb, t: "Idea of the day", d: "60 seconds, every day", c: "#F59E0B", pro: false },
  { to: "/dashboard", Icon: Target, t: "Daily quests", d: "Earn coins and a chest", c: "#8B5CF6", pro: false },
];

export default function ProFeatures() {
  const { isPro, sub } = useAuth();
  if (!sub) return null;
  return (
    <section className="mb-8" data-testid="feature-showcase">
      <p className="uppercase tracking-[0.2em] text-[11px] font-bold text-zinc-500 mb-2.5 px-1">Everything in FinLearn</p>
      <div className="flex gap-3 overflow-x-auto -mx-5 px-5 pb-2 snap-x">
        {ITEMS.map(({ key, to, Icon, t, d, c, pro, note }) => {
          const locked = pro && !isPro;
          return (
            <Link key={t} to={locked ? `/preview/${key}` : to} data-testid={`feature-${t}`}
              className="snap-start shrink-0 w-[148px] rounded-3xl bg-white border border-zinc-200 p-3.5 relative active:scale-[0.97] transition">
              <span className={`absolute top-2.5 right-2.5 rounded-full text-[10px] font-black px-2 py-0.5 ${pro ? "bg-zinc-900 text-white" : "bg-emerald-100 text-emerald-700"}`}>
                {pro ? "PRO" : "FREE"}
              </span>
              <span className="w-11 h-11 rounded-2xl grid place-items-center text-white mb-3" style={{ background: c }}>{locked ? <Lock className="w-5 h-5" /> : <Icon className="w-5 h-5" />}</span>
              <span className="block font-[Outfit] font-extrabold text-[15px] leading-tight">{t}</span>
              <span className="block text-[12px] text-zinc-500 leading-snug mt-0.5">{note && !isPro ? note : d}</span>
            </Link>
          );
        })}
      </div>
    </section>
  );
}
