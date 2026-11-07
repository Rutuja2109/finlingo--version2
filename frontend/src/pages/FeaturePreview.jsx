import React from "react";
import { Link, Navigate, useNavigate, useParams } from "react-router-dom";
import { X, Crown, Check, LineChart, Wallet, Flag, Calculator, Skull, Heart, Target, TrendingUp, TrendingDown } from "lucide-react";
import { useAuth } from "@/context/AuthContext";

// What a free learner sees when they tap a Pro feature: a sample of the real screen and what it gives them,
// then a clear way to unlock it. (Sample numbers only, never the learner's own data.)

const Card = ({ children, className = "" }) => <div className={`bg-white border border-zinc-200 rounded-2xl p-3.5 ${className}`}>{children}</div>;

function PracticeMock() {
  return (
    <div className="space-y-2.5">
      <Card>
        <p className="text-[11px] font-bold tracking-widest text-zinc-500 uppercase">Practice money, not real money</p>
        <p className="font-[Outfit] font-black text-2xl">₹1,00,000</p>
        <div className="flex gap-1.5 mt-2 overflow-hidden">
          {["Nifty 50", "Gold", "Bitcoin", "Rocket Tech"].map((a, i) => (
            <span key={a} className={`px-2.5 py-1 rounded-full text-[11px] font-bold whitespace-nowrap ${i === 0 ? "bg-[#FF6B35] text-white" : "bg-zinc-100 text-zinc-600"}`}>{a}</span>
          ))}
        </div>
      </Card>
      <Card>
        <div className="flex items-center justify-between mb-1"><span className="font-bold text-sm">Nifty 50 Index Fund</span><span className="text-emerald-600 text-sm font-bold flex items-center gap-1"><TrendingUp className="w-4 h-4" />+2.4%</span></div>
        <svg viewBox="0 0 200 70" className="w-full h-16"><polyline fill="none" stroke="#10B981" strokeWidth="3" strokeLinejoin="round" strokeLinecap="round" points="0,52 20,48 40,54 60,38 80,42 100,30 120,34 140,22 160,26 180,14 200,18" /></svg>
        <div className="grid grid-cols-2 gap-2 mt-1"><span className="rounded-xl bg-emerald-500 text-white text-center font-bold text-sm py-2">Buy</span><span className="rounded-xl bg-zinc-100 text-zinc-500 text-center font-bold text-sm py-2">Sell</span></div>
      </Card>
      <Card className="flex items-center gap-2 text-[13px] text-zinc-600"><TrendingDown className="w-4 h-4 text-rose-500 shrink-0" />Replay a market crash and see what really happens to your money.</Card>
    </div>
  );
}

function MoneyMock() {
  const rows = [["Food", 4200, 6000, "#F59E0B"], ["Travel", 1800, 3000, "#2563EB"], ["Fun", 2500, 2500, "#EC4899"]];
  return (
    <div className="space-y-2.5">
      <Card>
        <div className="flex justify-between text-sm"><span className="text-zinc-500 font-bold">Income</span><span className="font-black">₹25,000</span></div>
        <div className="flex justify-between text-sm"><span className="text-zinc-500 font-bold">Spent</span><span className="font-black text-rose-600">₹8,500</span></div>
        <div className="flex justify-between text-sm"><span className="text-zinc-500 font-bold">Left</span><span className="font-black text-emerald-600">₹16,500</span></div>
      </Card>
      <Card className="space-y-2.5">
        {rows.map(([n, v, cap, c]) => (
          <div key={n}><div className="flex justify-between text-[13px] font-bold"><span>{n}</span><span className="text-zinc-500">₹{v.toLocaleString("en-IN")} of ₹{cap.toLocaleString("en-IN")}</span></div>
            <div className="h-2 rounded-full bg-zinc-100 mt-1 overflow-hidden"><div className="h-full rounded-full" style={{ width: `${(v / cap) * 100}%`, background: c }} /></div></div>
        ))}
      </Card>
      <Card><div className="flex items-center gap-2 text-sm font-bold"><Target className="w-4 h-4 text-indigo-500" />Goa trip</div>
        <div className="h-2 rounded-full bg-zinc-100 mt-2 overflow-hidden"><div className="h-full rounded-full bg-indigo-500" style={{ width: "40%" }} /></div>
        <p className="text-[12px] text-zinc-500 mt-1">₹6,000 saved of ₹15,000</p></Card>
    </div>
  );
}

function MissionsMock() {
  const rows = [["Check your last 5 bank spends", true, "+30 XP"], ["Start a ₹500 SIP in a demo app", false, "+60 XP"], ["Ask a parent what an FD is", false, "+40 XP"]];
  return (
    <div className="space-y-2.5">
      {rows.map(([t, done, xp]) => (
        <Card key={t} className="flex items-center gap-3">
          <span className={`w-9 h-9 rounded-xl grid place-items-center shrink-0 ${done ? "bg-emerald-500 text-white" : "bg-rose-50 text-rose-500"}`}>{done ? <Check className="w-5 h-5" strokeWidth={3} /> : <Flag className="w-5 h-5" />}</span>
          <span className="flex-1 font-bold text-[14px] leading-snug">{t}</span>
          <span className="text-[12px] font-black text-amber-600">{xp}</span>
        </Card>
      ))}
      <Card className="text-[13px] text-zinc-600">Do it in real life, mark it done, earn XP and coins. Learning that actually changes your habits.</Card>
    </div>
  );
}

function CalcMock() {
  return (
    <div className="space-y-2.5">
      <Card>
        <p className="font-[Outfit] font-extrabold text-[15px] mb-2">SIP calculator</p>
        {[["Monthly amount", "₹5,000", 25], ["Years", "10", 50], ["Expected return", "12%", 60]].map(([l, v, p]) => (
          <div key={l} className="mb-2.5"><div className="flex justify-between text-[12px] font-bold text-zinc-500"><span>{l}</span><span className="text-zinc-900">{v}</span></div>
            <div className="h-1.5 rounded-full bg-zinc-100 mt-1.5 relative"><div className="h-full rounded-full bg-[#10B981]" style={{ width: `${p}%` }} /><span className="absolute -top-1.5 w-4.5 h-4.5 w-[18px] h-[18px] rounded-full bg-white border-2 border-[#10B981]" style={{ left: `calc(${p}% - 9px)` }} /></div></div>
        ))}
      </Card>
      <Card className="bg-emerald-50 border-emerald-200"><p className="text-[12px] text-zinc-500 font-bold">You invest ₹6,00,000 and it can grow to</p><p className="font-[Outfit] font-black text-3xl text-emerald-700">₹11.6 lakh</p></Card>
      <Card className="text-[13px] text-zinc-600">Also: EMI calculator and emergency-fund calculator.</Card>
    </div>
  );
}

function BossMock() {
  return (
    <div className="space-y-2.5">
      <Card className="bg-gradient-to-br from-zinc-950 to-[#1a0a2e] text-white border-0 flex items-center gap-3">
        <span className="w-12 h-12 rounded-2xl bg-[#EC4899]/25 text-[#EC4899] grid place-items-center"><Skull className="w-7 h-7" /></span>
        <span className="flex-1"><span className="block text-[10px] tracking-[0.3em] font-bold text-[#EC4899]">BOSS BATTLE</span><span className="block font-[Outfit] font-black">Chapter 1 final test</span></span>
        <span className="flex gap-0.5 text-rose-400"><Heart className="w-4 h-4" fill="currentColor" /><Heart className="w-4 h-4" fill="currentColor" /><Heart className="w-4 h-4" /></span>
      </Card>
      <Card>
        <p className="font-bold text-[14px] mb-2">Your salary rose 30%. What protects your savings most?</p>
        {["Spend the extra on upgrades", "Save half of every raise first", "Wait and see"].map((o, i) => (
          <div key={o} className={`rounded-xl border-2 px-3 py-2 text-[13px] font-semibold mb-1.5 ${i === 1 ? "border-emerald-400 bg-emerald-50" : "border-zinc-200"}`}>{o}</div>
        ))}
      </Card>
      <Card className="text-[13px] text-zinc-600">20 mixed questions after each chapter. Beat the boss for +200 XP.</Card>
    </div>
  );
}

const FEATURES = {
  practice: { Icon: LineChart, color: "#EC4899", title: "Practice trading", tag: "Trade with ₹1,00,000 of virtual money. No real risk.", Mock: PracticeMock,
    points: ["Buy and sell Nifty, gold, Bitcoin and a made-up stock", "Replay a market crash and learn what really happens", "Charts that move like a real market"] },
  money: { Icon: Wallet, color: "#6366F1", title: "My money", tag: "Know where every rupee goes.", Mock: MoneyMock,
    points: ["Log spends and income in seconds", "Monthly budgets by category", "Savings goals with progress"] },
  missions: { Icon: Flag, color: "#F43F5E", title: "Real-life missions", tag: "Turn what you learn into money habits.", Mock: MissionsMock,
    points: ["18 small real-world actions, from easy to bold", "Earn XP and coins for each one", "A new featured mission every week"] },
  calculators: { Icon: Calculator, color: "#10B981", title: "Calculators", tag: "Plan your money with real numbers.", Mock: CalcMock,
    points: ["SIP: see what monthly investing can grow into", "EMI: know the true cost of a loan", "Emergency fund: how much cushion you need"] },
  boss: { Icon: Skull, color: "#7C3AED", title: "Boss battles", tag: "Prove you have got it, chapter by chapter.", Mock: BossMock,
    points: ["20 mixed questions after every chapter", "Real-life situations, not memorising", "Beat the boss for big XP"] },
};

export default function FeaturePreview() {
  const { feature } = useParams();
  const nav = useNavigate();
  const { isPro, sub } = useAuth();
  const f = FEATURES[feature];
  if (!f) return <Navigate to="/pro" replace />;
  if (sub && isPro) return <Navigate to={`/${feature === "boss" ? "courses" : feature}`} replace />;
  const { Icon, Mock } = f;
  return (
    <div className="max-w-lg mx-auto pb-52" data-testid={`preview-${feature}`}>
      <button onClick={() => nav(-1)} aria-label="Close" data-testid="preview-close" className="mb-3 w-9 h-9 rounded-full bg-zinc-100 grid place-items-center"><X className="w-4 h-4" /></button>

      <div className="flex items-center gap-3 mb-1">
        <span className="w-12 h-12 rounded-2xl grid place-items-center text-white" style={{ background: f.color }}><Icon className="w-6 h-6" /></span>
        <div>
          <span className="inline-flex items-center gap-1 rounded-full bg-zinc-900 text-white text-[10px] font-black px-2 py-0.5"><Crown className="w-3 h-3" />PRO</span>
          <h1 className="font-[Outfit] font-black text-2xl leading-tight">{f.title}</h1>
        </div>
      </div>
      <p className="text-[15px] text-zinc-600 mb-4">{f.tag}</p>

      <p className="uppercase tracking-[0.2em] text-[11px] font-bold text-zinc-500 mb-2">A look inside</p>
      <div className="rounded-3xl bg-zinc-100 p-3 mb-4 relative" aria-label="Sample of the screen">
        <Mock />
        <span className="absolute top-2 right-3 text-[10px] font-bold text-zinc-400">SAMPLE</span>
      </div>

      <ul className="space-y-2.5 mb-4">
        {f.points.map((p) => (
          <li key={p} className="flex items-start gap-2.5 text-[14.5px] font-semibold"><span className="w-5 h-5 rounded-full bg-emerald-500 text-white grid place-items-center shrink-0 mt-0.5"><Check className="w-3 h-3" strokeWidth={4} /></span>{p}</li>
        ))}
      </ul>
      <p className="text-[12.5px] text-zinc-500">Included in the one FinLearn Pro plan. ₹49 a month unlocks everything together (every lesson, practice trading, My money, missions, calculators and boss battles). No extra charge for any feature.</p>

      <div className="fixed bottom-[64px] lg:bottom-0 inset-x-0 z-30 bg-white/95 backdrop-blur border-t border-zinc-200 px-5 pt-3 pb-3">
        <div className="max-w-lg mx-auto">
          <Link to={`/pro?from=${feature}`} data-testid="preview-unlock" className="block text-center w-full rounded-2xl bg-[#FF6B35] text-white font-[Outfit] font-extrabold text-lg py-3.5 active:scale-[0.98]">
            Unlock everything · ₹49/month
          </Link>
          <button onClick={() => nav(-1)} className="block mx-auto mt-1.5 text-[13px] font-semibold text-zinc-500">Maybe later</button>
        </div>
      </div>
    </div>
  );
}
