import React from "react";
import { Link, Navigate, useNavigate, useParams } from "react-router-dom";
import { X, Crown, Check, LineChart, Wallet, Flag, Calculator, Skull, Heart, Target, History as HistoryIcon, BarChart3, Coins, Bitcoin, Rocket, ArrowUp, ArrowDown, Flame, Plus, ChevronLeft, ChevronRight, ChevronDown, ChevronUp, CheckCircle2 } from "lucide-react";
import Lumi from "@/components/Lumi";
import { useAuth } from "@/context/AuthContext";

// What a free learner sees when they tap a Pro feature: a sample of the real screen and what it gives them,
// then a clear way to unlock it. (Sample numbers only, never the learner's own data.)

const Card = ({ children, className = "" }) => <div className={`bg-white border border-zinc-200 rounded-2xl p-3.5 ${className}`}>{children}</div>;

const inr = (n) => "₹" + Number(n).toLocaleString("en-IN");
const Lbl = ({ children }) => <p className="text-[11px] font-bold tracking-[.2em] uppercase text-zinc-500 mb-1.5 px-1">{children}</p>;
const Coach = ({ title, tone = "", children }) => {
  const cls = { warn: "bg-amber-50 border-amber-300", good: "bg-emerald-50 border-emerald-300" }[tone] || "bg-white border-zinc-200";
  return (
    <div className={`flex gap-3 items-start border rounded-2xl px-3 py-2.5 mt-2.5 text-[13px] leading-relaxed ${cls}`}>
      <Lumi size={44} mood="happy" className="shrink-0" />
      <div><b className="font-[Outfit]">{title}</b><br />{children}</div>
    </div>
  );
};

// Same layout as the real Practice screen, filled with sample numbers.
function PracticeMock() {
  const assets = [["NIFTY", "#2563EB", BarChart3, true], ["GOLD", "#F59E0B", Coins], ["BTC", "#FF9500", Bitcoin], ["RKT", "#EC4899", Rocket]];
  return (
    <div>
      <div className="rounded-3xl text-white p-4 bg-gradient-to-br from-[#FF6B35] via-[#FF8A4C] to-[#EC4899] text-center">
        <div className="font-[Outfit] font-black text-2xl tracking-tight">₹90,000</div>
        <div className="text-[11.5px] font-semibold opacity-90">Practice money, not real money</div>
      </div>
      <div className="grid grid-cols-3 gap-1 bg-zinc-200/70 rounded-2xl p-1 mt-3">
        {[["Trade", LineChart, true], ["Portfolio", Wallet], ["History", HistoryIcon]].map(([l, I, on]) => (
          <span key={l} className={`flex items-center justify-center gap-1.5 py-2 rounded-xl text-[13px] font-bold ${on ? "bg-white shadow text-[#FF6B35]" : "text-zinc-500"}`}><I className="w-4 h-4" />{l}</span>
        ))}
      </div>
      <div className="flex gap-3 px-2 pt-3 pb-2">
        {assets.map(([s, c, I, on]) => (
          <div key={s} className="shrink-0 w-14 text-center">
            <div className={`w-[48px] h-[48px] rounded-full grid place-items-center text-white mx-auto mb-1 border-[3px] ${on ? "border-zinc-900" : "border-transparent"}`} style={{ background: c }}><I className="w-5 h-5" /></div>
            <span className={`text-[11px] font-bold ${on ? "text-zinc-900" : "text-zinc-500"}`}>{s}</span>
          </div>
        ))}
      </div>
      <div className="flex items-end justify-between mb-1">
        <div><div className="text-[12.5px] font-bold text-zinc-500">Nifty 50 Index Fund</div><div className="font-[Outfit] font-black text-[26px] tracking-tight leading-tight">₹252.40</div></div>
        <span className="font-[Outfit] font-extrabold text-[13px] px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700">+2.41%</span>
      </div>
      <div className="bg-white border border-zinc-200 rounded-[20px] px-2 pt-2 pb-1">
        <svg viewBox="0 0 200 80" preserveAspectRatio="none" className="w-full h-20"><polyline fill="none" stroke="#10B981" strokeWidth="2.5" strokeLinejoin="round" strokeLinecap="round" points="0,58 14,54 28,60 42,44 56,48 70,36 84,42 98,28 112,34 126,22 140,30 154,18 168,24 184,12 200,16" /></svg>
      </div>
      <div className="flex justify-between my-2">
        {["1MIN", "5MIN", "15MIN", "1H", "1D", "1W"].map((k) => <span key={k} className={`font-[Outfit] font-extrabold text-xs px-2 py-1.5 rounded-[10px] ${k === "1D" ? "bg-zinc-900 text-white" : "text-zinc-400"}`}>{k}</span>)}
      </div>
      <p className="text-[12.5px] text-zinc-500 mx-1 mb-2">You hold <b>₹10,240</b> of NIFTY · profit/loss <b className="text-emerald-700">+₹240</b></p>
      <div className="grid grid-cols-2 gap-2.5">
        <span className="rounded-2xl py-3 text-white font-[Outfit] font-black text-base flex items-center justify-center gap-1.5 bg-red-500"><ArrowDown className="w-4 h-4" />Sell</span>
        <span className="rounded-2xl py-3 text-white font-[Outfit] font-black text-base flex items-center justify-center gap-1.5 bg-emerald-500"><ArrowUp className="w-4 h-4" />Buy</span>
      </div>
      <Coach title="Lumi says">An index fund holds 50 big companies at once, so one bad company cannot sink you.</Coach>
      <span className="mx-auto mt-3 flex w-fit items-center gap-1.5 border-2 border-red-500 text-red-700 bg-white rounded-2xl px-3 py-2 font-[Outfit] font-extrabold text-[13px]"><Flame className="w-4 h-4" />Replay a market crash</span>
    </div>
  );
}

// Same layout as the real My money screen, with sample numbers.
function MoneyMock() {
  const B = { needs: ["Needs", "#2563EB", 50, 8200, 48], wants: ["Wants", "#EC4899", 30, 5100, 30], savings: ["Savings", "#10B981", 20, 3700, 22] };
  const rows = [["Wed 5 Nov", [["Groceries and food", "Weekly vegetables", 640, "#2563EB"], ["Eating out", "Lunch with friends", 420, "#EC4899"]]],
    ["Tue 4 Nov", [["Income", "Pocket money", 5000, null], ["SIP and investing", "", 500, "#10B981"]]]];
  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <span className="w-9 h-9 grid place-items-center rounded-full bg-white"><ChevronLeft className="w-5 h-5" /></span>
        <span className="font-[Outfit] font-black text-lg">November 2026</span>
        <span className="w-9 h-9 grid place-items-center rounded-full bg-white"><ChevronRight className="w-5 h-5" /></span>
      </div>
      <div className="rounded-3xl text-white p-4 bg-gradient-to-br from-[#2563EB] via-[#6366F1] to-[#EC4899]">
        <div className="grid grid-cols-3 text-center gap-2">
          {[["Income", "₹17,000"], ["Spent", "₹13,300"], ["Left", "₹3,700"]].map(([l, v]) => <div key={l}><div className="text-[11px] font-semibold opacity-90">{l}</div><div className="font-[Outfit] font-black text-lg">{v}</div></div>)}
        </div>
        <p className="text-center text-[11.5px] opacity-90 mt-2">Savings you set aside are not counted as spent.</p>
      </div>
      <div className="mt-3 bg-white border border-zinc-200 rounded-[20px] p-3.5">
        <Lbl>Your 50 / 30 / 20 split</Lbl>
        <div className="flex h-3.5 rounded-full overflow-hidden bg-zinc-100 mb-3">{Object.values(B).map(([, c, , , p]) => <div key={c} style={{ width: `${p}%`, background: c }} />)}</div>
        {Object.values(B).map(([l, c, t, v, p]) => (
          <div key={l} className="flex items-center justify-between py-1.5 text-sm">
            <span className="flex items-center gap-2"><span className="w-3 h-3 rounded-full" style={{ background: c }} /><b>{l}</b></span>
            <span className="text-zinc-500">{inr(v)} · <b className="text-emerald-700">{p}%</b> of {t}%</span>
          </div>
        ))}
      </div>
      <Coach title="Nicely balanced" tone="good">Your split is close to 50 / 30 / 20. Keep saving before you spend.</Coach>
      <span className="w-full mt-3 rounded-2xl py-3.5 bg-[#FF6B35] text-white font-[Outfit] font-black text-base flex items-center justify-center gap-2"><Plus className="w-5 h-5" />Add money in or out</span>
      <div className="mt-4"><Lbl>This month</Lbl>
        {rows.map(([d, list]) => (
          <div key={d} className="mb-2"><div className="text-[12px] font-bold text-zinc-400 px-1 mb-1">{d}</div>
            <div className="bg-white border border-zinc-200 rounded-2xl px-3">
              {list.map(([n, note, amt, c], i) => (
                <div key={n + i} className="flex items-center gap-2 py-2.5 border-t first:border-t-0 border-zinc-100 text-sm">
                  <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ background: c || "#10B981" }} />
                  <div className="flex-1 min-w-0"><b>{n}</b>{note && <div className="text-[12px] text-zinc-500 truncate">{note}</div>}</div>
                  <b className={c ? "" : "text-emerald-700"}>{c ? "−" : "+"}{inr(amt)}</b>
                </div>
              ))}
            </div></div>
        ))}
      </div>
      <div className="mt-4"><Lbl>Savings goals</Lbl>
        <div className="bg-white border border-zinc-200 rounded-2xl p-3.5">
          <b className="font-[Outfit] text-base">New phone</b><div className="text-[12.5px] text-zinc-500">₹12,000 of ₹30,000</div>
          <div className="h-2.5 rounded-full bg-zinc-100 overflow-hidden my-2"><div className="h-full bg-emerald-500" style={{ width: "40%" }} /></div>
          <div className="text-[13px]">Save <b>₹3,000</b> a month for 6 months</div>
        </div>
      </div>
    </div>
  );
}

// Same cards as the real Real-life missions screen, with real mission examples.
function MissionsMock() {
  const Row = ({ t, xp, color, done, open, children, auto }) => (
    <div className={`bg-white border rounded-2xl mb-2.5 ${done ? "border-emerald-200" : "border-zinc-200"}`}>
      <div className="flex items-center gap-3 px-3.5 py-3">
        <span className="w-9 h-9 rounded-xl grid place-items-center shrink-0" style={{ background: `${color}1A`, color }}>{done ? <CheckCircle2 className="w-5 h-5 text-emerald-500" /> : <Flag className="w-5 h-5" />}</span>
        <span className="flex-1 min-w-0"><span className={`block font-[Outfit] font-extrabold text-[15px] ${done ? "text-zinc-400 line-through" : ""}`}>{t}</span>
          <span className="block text-[12px] text-zinc-500">{done ? "Done" : `+${xp} XP · +${Math.round(xp / 2)} coins`}{auto && !done ? " · checks itself" : ""}</span></span>
        {open ? <ChevronUp className="w-5 h-5 text-zinc-400" /> : <ChevronDown className="w-5 h-5 text-zinc-400" />}
      </div>
      {open && <div className="px-3.5 pb-3.5 -mt-1">{children}</div>}
    </div>
  );
  return (
    <div>
      <div className="bg-white border border-zinc-200 rounded-2xl p-3.5 mb-3">
        <div className="flex justify-between text-[13px] font-bold mb-1.5"><span>Your progress</span><span>3 of 18 done</span></div>
        <div className="h-2.5 rounded-full bg-zinc-100 overflow-hidden"><div className="h-full bg-emerald-500" style={{ width: "17%" }} /></div>
      </div>
      <div className="rounded-3xl text-white p-4 bg-gradient-to-br from-[#FF6B35] via-[#FF8A4C] to-[#EC4899] mb-4 relative overflow-hidden">
        <div className="absolute -right-1 -top-1 opacity-40 pointer-events-none"><Lumi size={84} mood="cheer" /></div>
        <p className="uppercase tracking-[0.2em] text-[11px] font-bold text-white/90 relative">Mission of the week</p>
        <h2 className="font-[Outfit] font-black text-xl mt-1 max-w-[72%] relative">Find one subscription you can cancel</h2>
      </div>
      <Lbl>Know your spending</Lbl>
      <Row t="Check your UPI history" xp={20} color="#EC4899" open>
        <p className="text-[13px] text-zinc-600 mb-2">Small UPI payments hide where your money really goes.</p>
        <ol className="text-[13px] text-zinc-700 list-decimal pl-5 space-y-1 mb-3"><li>Open your UPI app and look at the last 7 days of payments.</li><li>Find your three biggest spends.</li><li>Ask yourself: need or want?</li></ol>
        <div className="w-full border-2 border-zinc-200 rounded-xl px-3 py-2 text-[13px] text-zinc-400 mb-2">What surprised you? (optional)</div>
        <div className="w-full rounded-2xl py-3 bg-[#FF6B35] text-white font-[Outfit] font-black text-[15px] text-center">I did it</div>
      </Row>
      <Row t="Log 5 spends in My money this week" xp={30} color="#EC4899" auto />
      <Row t="Find one subscription you can cancel" xp={20} color="#EC4899" />
      <Lbl>Build savings</Lbl>
      <Row t="Set up an automatic transfer to savings" xp={30} color="#10B981" />
      <Row t="Put your first ₹1,000 in an emergency fund" xp={30} color="#10B981" done />
      <Lbl>Protect yourself</Lbl>
      <Row t="Turn on two-step verification" xp={25} color="#7C3AED" />
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
        <span className="absolute top-2 right-3 text-[10px] font-bold text-zinc-400 bg-white/80 rounded px-1">SAMPLE</span>
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
