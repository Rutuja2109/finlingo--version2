import React from "react";
import { Link } from "react-router-dom";
import Lumi from "@/components/Lumi";
import { ArrowRight, Sparkles, Target, Trophy, Brain, Layers } from "lucide-react";

export default function Landing() {
  return (
    <div className="min-h-screen bg-[#FAFAFA] text-zinc-900 font-[Manrope] overflow-x-hidden">
      <header className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <Lumi size={40} />
          <span className="font-[Outfit] font-black text-xl tracking-tight">FinLearn</span>
        </div>
        <div className="flex items-center gap-3">
          <Link to="/login" data-testid="landing-login" className="px-4 py-2 text-sm font-semibold text-zinc-700 hover:text-zinc-900">Log in</Link>
          <Link to="/signup" data-testid="landing-signup" className="px-4 py-2 rounded-full bg-zinc-900 text-white text-sm font-semibold hover:bg-zinc-800 transition">Get started</Link>
        </div>
      </header>

      <section className="max-w-6xl mx-auto px-6 pt-12 pb-24 grid lg:grid-cols-2 gap-12 items-center">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#FF6B35]/10 text-[#FF6B35] text-xs font-bold uppercase tracking-[0.2em] mb-6">
            <Sparkles className="w-3.5 h-3.5"/> AI-Powered Mastery Learning
          </div>
          <h1 className="font-[Outfit] font-black text-5xl md:text-6xl lg:text-7xl leading-[1.02] tracking-tighter mb-6">
            Certifications,<br/>
            <span className="bg-gradient-to-r from-[#FF6B35] via-[#EC4899] to-[#FF6B35] bg-clip-text text-transparent">finally</span> bingeable.
          </h1>
          <p className="text-lg text-zinc-600 max-w-xl mb-8 leading-relaxed">
            FinLearn turns 800-page certification books into bite-sized interactive
            journeys. Built for LOMA, CFA, FRM, PMP, AWS — and every cert after.
          </p>
          <div className="flex flex-col sm:flex-row gap-3">
            <Link to="/signup" data-testid="hero-cta-start"
              className="inline-flex items-center justify-center gap-2 px-7 py-4 rounded-2xl bg-[#FF6B35] hover:bg-[#FF5618] text-white font-[Outfit] font-bold text-lg transition active:scale-[0.98]">
              Start learning free <ArrowRight className="w-5 h-5" />
            </Link>
            <Link to="/login" data-testid="hero-cta-demo"
              className="inline-flex items-center justify-center gap-2 px-7 py-4 rounded-2xl bg-white border border-zinc-200 hover:border-zinc-300 font-[Outfit] font-bold text-lg transition">
              Try the demo
            </Link>
          </div>
          <p className="text-xs text-zinc-500 mt-4">No credit card · Real XP · Real leaderboards</p>
        </div>

        <div className="relative">
          <div className="absolute -inset-8 bg-gradient-to-br from-[#FF6B35]/20 via-[#EC4899]/20 to-transparent blur-3xl rounded-full"/>
          <div className="relative bg-white rounded-3xl border border-zinc-200 p-8 shadow-[0_30px_60px_-30px_rgba(0,0,0,0.2)]">
            <div className="flex items-center justify-center mb-6"><Lumi size={130} mood="cheer"/></div>
            <div className="space-y-3">
              {[
                { icon: Brain, txt: "Active recall · Mastery learning · Spaced repetition", c:"#2563EB" },
                { icon: Target, txt: "Daily goals, streaks & real XP rewards", c:"#10B981" },
                { icon: Trophy, txt: "Boss battles & live leaderboards", c:"#EC4899" },
                { icon: Layers, txt: "Works for LOMA, CFA, FRM, PMP, AWS & beyond", c:"#FF6B35" },
              ].map(({icon:Ic, txt, c}, i) => (
                <div key={i} className="flex items-center gap-3 p-3 rounded-xl bg-zinc-50">
                  <div className="w-9 h-9 rounded-lg grid place-items-center" style={{background: `${c}1A`}}>
                    <Ic className="w-5 h-5" style={{color: c}} />
                  </div>
                  <span className="text-sm font-semibold text-zinc-700">{txt}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <footer className="max-w-6xl mx-auto px-6 py-10 border-t border-zinc-200 text-sm text-zinc-500 flex justify-between">
        <span>© 2026 FinLearn · Master what matters.</span>
        <span>Meet Lumi, your guide.</span>
      </footer>
    </div>
  );
}
