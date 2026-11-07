import React from "react";
import { Link } from "react-router-dom";
import { Crown, ArrowRight } from "lucide-react";
import { useAuth } from "@/context/AuthContext";

// Dashboard card for free accounts: what Pro adds and what it costs.
export default function ProBanner() {
  const { sub, isPro } = useAuth();
  if (!sub || isPro) return null;
  return (
    <Link to="/pro" data-testid="pro-banner" className="flex items-center gap-3 rounded-3xl p-4 mb-6 text-white bg-gradient-to-br from-[#FF6B35] via-[#F59E0B] to-[#EC4899] active:scale-[0.99] transition">
      <span className="w-11 h-11 rounded-2xl grid place-items-center bg-white/25 shrink-0"><Crown className="w-6 h-6" /></span>
      <span className="flex-1 min-w-0">
        <span className="block font-[Outfit] font-black text-[16px] leading-tight">Go Pro: every lesson and tool</span>
        <span className="block text-[12px] text-white/90">Trading practice, My money, missions, calculators. From ₹49 a month.</span>
      </span>
      <ArrowRight className="w-5 h-5 shrink-0" />
    </Link>
  );
}
