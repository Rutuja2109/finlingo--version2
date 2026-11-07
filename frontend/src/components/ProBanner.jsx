import React from "react";
import { Link } from "react-router-dom";
import { Crown, ArrowRight } from "lucide-react";
import { useAuth } from "@/context/AuthContext";

// Dashboard card for free accounts: what Pro adds and what it costs.
export default function ProBanner() {
  const { sub, isPro } = useAuth();
  if (!sub || (isPro && !sub.trial?.active)) return null;
  const t = sub.trial || {};
  const head = t.active ? `Your Pro trial: ${t.days_left} day${t.days_left === 1 ? "" : "s"} left` : t.ended ? "Your trial ended. Want it back?" : "Go Pro: every lesson and tool";
  const sub2 = t.active ? "Keep trading practice, My money and missions for just ₹33 a month." : "Trading practice, My money, missions, calculators. From ₹49 a month.";
  return (
    <Link to="/pro" data-testid="pro-banner" className="flex items-center gap-3 rounded-3xl p-4 mb-6 text-white bg-gradient-to-br from-[#FF6B35] via-[#F59E0B] to-[#EC4899] active:scale-[0.99] transition">
      <span className="w-11 h-11 rounded-2xl grid place-items-center bg-white/25 shrink-0"><Crown className="w-6 h-6" /></span>
      <span className="flex-1 min-w-0">
        <span className="block font-[Outfit] font-black text-[16px] leading-tight">{head}</span>
        <span className="block text-[12px] text-white/90">{sub2}</span>
      </span>
      <ArrowRight className="w-5 h-5 shrink-0" />
    </Link>
  );
}
