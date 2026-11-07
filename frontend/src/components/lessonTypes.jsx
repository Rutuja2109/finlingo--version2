import React, { useEffect, useMemo, useRef, useState } from "react";
import { Check, X, Sparkles, MessageCircle, Hand, ThumbsUp } from "lucide-react";
import Lumi from "@/components/Lumi";
import { sipFuture, inflate, doublingYears, inr } from "@/lib/growth";

// Interactive lesson types: chat story, myth-or-fact swipe, "what if" slider, budget splitter.
// Each takes the lesson `l`; scored ones also take onAnswer(isCorrect), the rest call onShown() when finished.

const Label = ({ color, children }) => <p className="uppercase tracking-[0.25em] text-[11px] font-bold mb-2" style={{ color }}>{children}</p>;

// ---------------------------------------------------------------- chat story
export function ChatLesson({ l, onShown }) {
  const c = l.content || {};
  const msgs = c.messages || [];
  const [shown, setShown] = useState(1);
  const [typing, setTyping] = useState(false);
  const end = useRef(null);
  const finished = shown >= msgs.length;

  useEffect(() => { if (finished) onShown?.(); }, [finished]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { end.current?.scrollIntoView({ behavior: "smooth", block: "nearest" }); }, [shown, typing]);

  const next = () => {
    if (finished || typing) return;
    setTyping(true);
    setTimeout(() => { setShown((s) => s + 1); setTyping(false); }, 450);
  };

  return (
    <div className="fade-up" onClick={next} data-testid="chat-lesson">
      <Label color="#EC4899"><MessageCircle className="w-3.5 h-3.5 inline -mt-0.5 mr-1" />Story time</Label>
      <h2 className="font-[Outfit] font-black text-2xl tracking-tight mb-1">{c.title}</h2>
      {c.scene && <p className="text-[13px] text-zinc-500 mb-4">{c.scene}</p>}
      <div className="space-y-3 mb-3">
        {msgs.slice(0, shown).map((m, i) => {
          const me = m.who === "you";
          return (
            <div key={i} className={`flex items-end gap-2 fade-up ${me ? "flex-row-reverse" : ""}`}>
              {m.who === "lumi" ? <span className="shrink-0"><Lumi size={34} mood="happy" /></span>
                : <span className="w-8 h-8 shrink-0 rounded-full grid place-items-center text-white text-xs font-black" style={{ background: me ? "#FF6B35" : "#6366F1" }}>{me ? "You" : (m.name || "F")[0]}</span>}
              <div className={`max-w-[78%] rounded-2xl px-3.5 py-2.5 text-[14.5px] leading-snug ${me ? "bg-[#FF6B35] text-white rounded-br-md" : "bg-zinc-100 text-zinc-900 rounded-bl-md"}`}>{m.text}</div>
            </div>
          );
        })}
        {typing && <div className="flex items-center gap-1.5 pl-10 text-zinc-400" aria-label="typing"><span className="w-2 h-2 rounded-full bg-current animate-bounce" /><span className="w-2 h-2 rounded-full bg-current animate-bounce [animation-delay:120ms]" /><span className="w-2 h-2 rounded-full bg-current animate-bounce [animation-delay:240ms]" /></div>}
        <div ref={end} />
      </div>
      {!finished && <p className="text-center text-[13px] font-bold text-zinc-400" data-testid="chat-tap">Tap to continue</p>}
      {finished && c.takeaway && (
        <div className="rounded-2xl bg-amber-50 border-2 border-amber-200 p-3.5 text-[14px] fade-up"><b>Remember:</b> {c.takeaway}</div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------- myth or fact
export function SwipeLesson({ l, picked, answered, onAnswer }) {
  const c = l.content || {};
  const cards = c.cards || [];
  const [i, setI] = useState(0);
  const [pick, setPick] = useState(null);
  const [firstTryAll, setFirstTryAll] = useState(true);
  const card = cards[Math.min(i, cards.length - 1)];
  const done = answered !== null;

  const choose = (ans) => {
    if (pick || done) return;
    setPick(ans);
    if (ans !== card.answer) setFirstTryAll(false);
  };
  const next = () => {
    if (i + 1 >= cards.length) { onAnswer(firstTryAll); return; }
    setI(i + 1); setPick(null);
  };
  const right = pick && pick === card.answer;

  return (
    <div className="fade-up" data-testid="swipe-lesson">
      <Label color="#F59E0B"><Hand className="w-3.5 h-3.5 inline -mt-0.5 mr-1" />Myth or fact?</Label>
      <h2 className="font-[Outfit] font-black text-xl tracking-tight mb-4">{c.instruction || "Is each statement a myth or a fact?"}</h2>
      <div className="flex gap-1.5 mb-3" aria-label="progress">
        {cards.map((_, k) => <span key={k} className={`h-1.5 flex-1 rounded-full ${k < i || (k === i && pick) ? "bg-[#FF6B35]" : "bg-zinc-200"}`} />)}
      </div>
      <div className={`rounded-3xl border-2 p-5 min-h-[120px] grid place-items-center text-center font-[Outfit] font-extrabold text-xl leading-snug transition ${pick ? (right ? "border-emerald-400 bg-emerald-50" : "border-rose-400 bg-rose-50") : "border-zinc-200 bg-white"}`} data-testid="swipe-card">
        {card?.text}
      </div>
      {!pick ? (
        <div className="grid grid-cols-2 gap-3 mt-4">
          <button onClick={() => choose("myth")} data-testid="swipe-myth" className="rounded-2xl bg-rose-500 text-white font-[Outfit] font-extrabold text-lg py-4 active:scale-[0.97]"><X className="w-5 h-5 inline -mt-1 mr-1" />Myth</button>
          <button onClick={() => choose("fact")} data-testid="swipe-fact" className="rounded-2xl bg-emerald-500 text-white font-[Outfit] font-extrabold text-lg py-4 active:scale-[0.97]"><Check className="w-5 h-5 inline -mt-1 mr-1" />Fact</button>
        </div>
      ) : (
        <div className="mt-4 fade-up" data-testid="swipe-why">
          <p className={`font-[Outfit] font-extrabold mb-1 ${right ? "text-emerald-600" : "text-rose-600"}`}>{right ? "Right!" : `Not quite. It is a ${card.answer}.`}</p>
          <p className="text-[14.5px] text-zinc-700 leading-relaxed mb-3">{card.why}</p>
          <button onClick={next} data-testid="swipe-next" className="rounded-xl bg-zinc-900 text-white font-bold px-5 py-2.5">{i + 1 >= cards.length ? "Done" : "Next"}</button>
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------- what-if slider
const Slider = ({ c, value, onChange }) => (
  <div className="mb-4">
    <div className="flex justify-between text-[13px] font-bold text-zinc-500 mb-1"><span>{c.label}</span><span className="text-zinc-900 font-black tabular-nums">{c.prefix || ""}{Number(value).toLocaleString("en-IN")}{c.suffix || ""}</span></div>
    <input type="range" min={c.min} max={c.max} step={c.step} value={value} onChange={(e) => onChange(Number(e.target.value))}
      aria-label={c.label} className="w-full h-3 accent-[#10B981]" style={{ touchAction: "pan-y" }} />
  </div>
);

export function SliderLesson({ l }) {
  const c = l.content || {};
  const [vals, setVals] = useState(() => Object.fromEntries((c.controls || []).map((k) => [k.key, k.value])));
  const set = (k) => (v) => setVals((o) => ({ ...o, [k]: v }));
  const out = useMemo(() => {
    if (c.kind === "inflation") return { kind: "inflation", ...inflate({ price: vals.price, years: vals.years, ratePct: vals.rate }) };
    const r = sipFuture({ monthly: vals.monthly || 0, lump: vals.lump || 0, years: vals.years, ratePct: vals.rate });
    return { kind: "growth", ...r };
  }, [vals, c.kind]);
  const pct = out.kind === "growth" && out.value > 0 ? Math.round((out.invested / out.value) * 100) : 0;

  return (
    <div className="fade-up" data-testid="slider-lesson">
      <Label color="#10B981"><Sparkles className="w-3.5 h-3.5 inline -mt-0.5 mr-1" />What if?</Label>
      <h2 className="font-[Outfit] font-black text-2xl tracking-tight mb-1">{c.title}</h2>
      {c.intro && <p className="text-[14px] text-zinc-600 mb-4">{c.intro}</p>}
      {(c.controls || []).map((k) => <Slider key={k.key} c={k} value={vals[k.key]} onChange={set(k.key)} />)}

      {out.kind === "growth" ? (
        <div className="rounded-2xl bg-emerald-50 border-2 border-emerald-200 p-4" data-testid="slider-result">
          <p className="text-[12px] font-bold text-zinc-500">{c.resultLabel || "It could grow to"}</p>
          <p className="font-[Outfit] font-black text-3xl text-emerald-700 tabular-nums">{inr(out.value)}</p>
          <div className="h-3 rounded-full bg-emerald-200 overflow-hidden mt-2 flex"><div className="h-full bg-zinc-400" style={{ width: `${pct}%` }} /><div className="h-full bg-emerald-500 flex-1" /></div>
          <div className="flex justify-between text-[12px] mt-1.5 text-zinc-600"><span>You put in {inr(out.invested)}</span><span className="font-bold text-emerald-700">Growth {inr(out.gain)}</span></div>
          <p className="text-[12px] text-zinc-500 mt-2">Doubles about every {doublingYears(vals.rate || 1)} years at {vals.rate}% (rule of 72).</p>
        </div>
      ) : (
        <div className="rounded-2xl bg-rose-50 border-2 border-rose-200 p-4" data-testid="slider-result">
          <p className="text-[12px] font-bold text-zinc-500">The same thing will cost</p>
          <p className="font-[Outfit] font-black text-3xl text-rose-600 tabular-nums">{inr(out.future)}</p>
          <p className="text-[13px] text-zinc-700 mt-1">Or: {inr(vals.price)} saved today will only buy about <b>{inr(out.worth)}</b> worth of things.</p>
        </div>
      )}
      <p className="text-[11.5px] text-zinc-400 mt-2">An illustration with an assumed rate, not a promise of returns.</p>
      {c.takeaway && <div className="rounded-2xl bg-amber-50 border-2 border-amber-200 p-3.5 text-[14px] mt-3"><b>Remember:</b> {c.takeaway}</div>}
    </div>
  );
}

// ---------------------------------------------------------------- budget splitter
export function BudgetLesson({ l, onShown }) {
  const c = l.content || {};
  const income = c.income || 25000;
  const [needs, setNeeds] = useState(c.start?.needs ?? 70);
  const [wants, setWants] = useState(c.start?.wants ?? 25);
  const [checked, setChecked] = useState(false);
  const savings = Math.max(0, 100 - needs - wants);
  const amt = (p) => Math.round((income * p) / 100);
  const msg = savings >= 20 ? ["Strong. That is the 20% starter target.", "text-emerald-600"]
    : savings >= 10 ? ["Okay start. Try to move toward 20% as your income grows.", "text-amber-600"]
      : ["Savings are squeezed. Even 10% paid first changes the picture.", "text-rose-600"];
  const bars = [["Needs", needs, "#2563EB"], ["Wants", wants, "#EC4899"], ["Savings", savings, "#10B981"]];

  return (
    <div className="fade-up" data-testid="budget-lesson">
      <Label color="#2563EB">Build your budget</Label>
      <h2 className="font-[Outfit] font-black text-2xl tracking-tight mb-1">{c.title || "Split your salary"}</h2>
      <p className="text-[14px] text-zinc-600 mb-4">{c.intro || `Your salary is ${inr(income)}. Drag to decide where it goes.`}</p>
      <div className="h-5 rounded-full overflow-hidden flex mb-3" aria-label="split">
        {bars.map(([n, p, col]) => <div key={n} style={{ width: `${p}%`, background: col }} className="h-full transition-all" />)}
      </div>
      <div className="space-y-4 mb-3">
        <div>
          <div className="flex justify-between text-[13px] font-bold mb-1"><span className="text-blue-600">Needs: rent, food, travel</span><span className="tabular-nums">{needs}% · {inr(amt(needs))}</span></div>
          <input type="range" min={20} max={80} step={1} value={needs} aria-label="Needs percent" className="w-full h-3 accent-blue-600" style={{ touchAction: "pan-y" }}
            onChange={(e) => { const v = Number(e.target.value); setNeeds(v); if (v + wants > 100) setWants(100 - v); setChecked(false); }} />
        </div>
        <div>
          <div className="flex justify-between text-[13px] font-bold mb-1"><span className="text-pink-600">Wants: fun, eating out</span><span className="tabular-nums">{wants}% · {inr(amt(wants))}</span></div>
          <input type="range" min={0} max={60} step={1} value={wants} aria-label="Wants percent" className="w-full h-3 accent-pink-600" style={{ touchAction: "pan-y" }}
            onChange={(e) => { const v = Number(e.target.value); setWants(Math.min(v, 100 - needs)); setChecked(false); }} />
        </div>
        <div className="flex justify-between text-[13px] font-bold"><span className="text-emerald-600">Savings: what is left</span><span className="tabular-nums">{savings}% · {inr(amt(savings))}</span></div>
      </div>
      {!checked ? (
        <button onClick={() => { setChecked(true); onShown?.(); }} data-testid="budget-check" className="rounded-xl bg-[#FF6B35] text-white font-bold px-5 py-2.5">Check my budget</button>
      ) : (
        <div className="fade-up rounded-2xl bg-zinc-50 border border-zinc-200 p-3.5" data-testid="budget-feedback">
          <p className={`font-[Outfit] font-extrabold ${msg[1]}`}>{msg[0]}</p>
          <p className="text-[13px] text-zinc-600 mt-1">{c.takeaway || "A common starting point is 50% needs, 30% wants and 20% savings. Change it to fit your life."}</p>
        </div>
      )}
    </div>
  );
}
