import React, { useEffect } from "react";
import { Check } from "lucide-react";
import Lumi from "@/components/Lumi";

// Full-screen "You're Pro!" after a successful purchase: confetti, Lumi, and what is now open. Makes the purchase feel good.
export default function ProWelcome({ onDone }) {
  useEffect(() => {
    const colors = ["#FF6B35", "#EC4899", "#FBBF24", "#10B981", "#2563EB"];
    const pieces = [];
    for (let i = 0; i < 46; i++) {
      const el = document.createElement("div");
      el.className = "confetti-piece";
      el.style.left = Math.random() * 100 + "vw";
      el.style.background = colors[i % colors.length];
      el.style.animationDuration = (1.8 + Math.random() * 1.4) + "s";
      el.style.animationDelay = (Math.random() * 0.5) + "s";
      el.style.borderRadius = Math.random() > 0.5 ? "50%" : "2px";
      document.body.appendChild(el);
      pieces.push(el);
    }
    const t = setTimeout(() => pieces.forEach((p) => p.remove()), 4200);
    return () => { clearTimeout(t); pieces.forEach((p) => p.remove()); };
  }, []);

  return (
    <div className="fixed inset-0 z-[70] bg-gradient-to-br from-[#FF6B35] via-[#F59E0B] to-[#EC4899] text-white grid place-items-center px-6 text-center" role="dialog" aria-label="You are Pro" data-testid="pro-welcome">
      <div className="max-w-sm">
        <div className="flex justify-center"><Lumi size={150} mood="celebrate" className="lumi-celebrate" /></div>
        <h1 className="font-[Outfit] font-black text-4xl mt-2">You're Pro!</h1>
        <p className="text-white/95 mt-1.5">Thank you. Everything in FinLearn is open now.</p>
        <ul className="mt-5 text-left bg-white/20 rounded-3xl p-4 space-y-2 text-[14.5px] font-semibold">
          {["Every lesson in every course", "Practice trading, My money and missions", "Calculators and boss battles", "5 streak freezes and your Pro badge"].map((t) => (
            <li key={t} className="flex items-center gap-2.5"><span className="w-5 h-5 rounded-full bg-white text-emerald-600 grid place-items-center shrink-0"><Check className="w-3.5 h-3.5" strokeWidth={4} /></span>{t}</li>
          ))}
        </ul>
        <button onClick={onDone} data-testid="pro-welcome-start" className="mt-6 w-full rounded-2xl bg-white text-[#FF6B35] font-[Outfit] font-extrabold text-lg py-3.5 active:scale-[0.98]">Start exploring</button>
        <p className="text-[12px] text-white/90 mt-3">Manage or cancel any time in Google Play.</p>
      </div>
    </div>
  );
}
