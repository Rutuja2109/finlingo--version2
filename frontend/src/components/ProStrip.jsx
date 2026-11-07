import React from "react";
import { Link, useLocation } from "react-router-dom";
import { Crown, Gift, ArrowRight } from "lucide-react";
import { useAuth } from "@/context/AuthContext";

// Slim bar under the header on every screen: shows trial days left, or invites free accounts to go Pro.
export default function ProStrip() {
  const { sub } = useAuth();
  const loc = useLocation();
  if (!sub || sub.admin || loc.pathname.startsWith("/pro")) return null;
  const t = sub.trial || {};
  let text, Icon = Crown, grad = "from-[#FF6B35] to-[#EC4899]";
  if (t.active) { Icon = Gift; text = `Pro trial: ${t.days_left} day${t.days_left === 1 ? "" : "s"} left. Keep it for ₹33 a month`; grad = t.days_left <= 2 ? "from-[#E5484D] to-[#EC4899]" : "from-[#8B5CF6] to-[#EC4899]"; }
  else if (sub.pro) return null;
  else if (t.ended) text = "Your Pro trial ended. Get Pro back from ₹49 a month";
  else text = "Unlock every lesson and tool. Go Pro from ₹49 a month";
  return (
    <Link to="/pro?from=strip" data-testid="pro-strip" className={`flex items-center justify-center gap-2 bg-gradient-to-r ${grad} text-white text-[12.5px] font-bold px-3 py-1.5`}>
      <Icon className="w-3.5 h-3.5 shrink-0" /><span className="truncate">{text}</span><ArrowRight className="w-3.5 h-3.5 shrink-0" />
    </Link>
  );
}
