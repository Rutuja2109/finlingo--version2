import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ChevronLeft } from "lucide-react";
import { api } from "@/lib/api";
import Lumi from "@/components/Lumi";
import { sip, sipNeeded, emi, monthsToPayOff, loanBalances, emergency, inrShort } from "@/lib/calc";

const inr = (n) => "₹" + Math.round(Math.abs(n)).toLocaleString("en-IN");
const clean = (v) => v.replace(/[^\d.]/g, "").replace(/(\..*)\./g, "$1");

function Field({ label, value, set, min, max, step, unit, testid }) {
  const n = parseFloat(value);
  return (
    <div className="mb-3.5">
      <div className="flex items-center justify-between mb-1">
        <label className="text-[12.5px] font-bold text-zinc-500">{label}</label>
        <div className="flex items-center gap-1 border-2 border-zinc-200 rounded-xl px-2 py-1 focus-within:border-[#FF6B35]">
          {unit === "₹" && <span className="text-sm font-bold text-zinc-400">₹</span>}
          <input value={value} onChange={(e) => set(clean(e.target.value))} inputMode="decimal" data-testid={testid}
            className="w-24 text-right font-[Outfit] font-extrabold text-base outline-none bg-transparent" />
          {unit && unit !== "₹" && <span className="text-sm font-bold text-zinc-400">{unit}</span>}
        </div>
      </div>
      <input type="range" min={min} max={max} step={step} value={Number.isFinite(n) ? Math.min(max, Math.max(min, n)) : min}
        onChange={(e) => set(String(e.target.value))} className="fl-range w-full" aria-label={label}
        style={{ "--fill": `${Number.isFinite(n) ? Math.round(((Math.min(max, Math.max(min, n)) - min) / (max - min)) * 100) : 0}%` }} />
    </div>
  );
}

function Tip({ mood = "happy", title, children }) {
  return (
    <div className="flex gap-3 items-start border border-zinc-200 bg-white rounded-2xl px-3 py-2.5 mt-3 text-[13px] leading-relaxed">
      <Lumi size={44} mood={mood} className="shrink-0" />
      <div><b className="font-[Outfit]">{title}</b><br />{children}</div>
    </div>
  );
}

function Stat({ label, value, sub, color, testid }) {
  return (
    <div className="text-center">
      <div className="text-[11px] font-semibold opacity-90">{label}</div>
      <div className="font-[Outfit] font-black text-xl" style={color ? { color } : {}} data-testid={testid}>{value}</div>
      {sub && <div className="text-[11px] opacity-80">{sub}</div>}
    </div>
  );
}

function GrowthChart({ rows }) {
  const W = 340, H = 150, pl = 4, pb = 18, pt = 8;
  const max = Math.max(...rows.map((r) => r.value));
  const bw = (W - pl) / rows.length;
  const y = (v) => pt + (H - pt - pb) * (1 - v / max);
  const every = Math.ceil(rows.length / 6);
  return (
    <svg viewBox={`0 0 ${W} ${H}`} width="100%" role="img" aria-label="Growth of your SIP by year">
      {rows.map((r, i) => {
        const x = pl + i * bw + bw * 0.15, w = bw * 0.7;
        return (
          <g key={r.year}>
            <rect x={x} y={y(r.value)} width={w} height={y(r.invested) - y(r.value)} fill="#10B981" rx="2" />
            <rect x={x} y={y(r.invested)} width={w} height={H - pb - y(r.invested)} fill="#93C5FD" rx="2" />
            {(i % every === 0 || i === rows.length - 1) && <text x={x + w / 2} y={H - 4} fontSize="10.5" textAnchor="middle" fill="#71717a" fontWeight="700" fontFamily="Arial, sans-serif">{`${r.year}y`}</text>}
          </g>
        );
      })}
    </svg>
  );
}

function Sip() {
  const [mode, setMode] = useState("grow");
  const [monthly, setMonthly] = useState("5000");
  const [rate, setRate] = useState("12");
  const [years, setYears] = useState("10");
  const [target, setTarget] = useState("1000000");
  const m = parseFloat(monthly) || 0, r = parseFloat(rate) || 0, y = Math.max(1, Math.min(40, Math.round(parseFloat(years) || 0)));
  const res = sip(m, r, y);
  const need = sipNeeded(parseFloat(target) || 0, r, y);
  const late = sip(m, r, Math.max(1, y - 3)).total;
  return (
    <div data-testid="calc-sip">
      <div className="grid grid-cols-2 gap-1 bg-zinc-100 rounded-2xl p-1 mb-3">
        {[["grow", "What will I get?"], ["need", "What do I need to save?"]].map(([k, l]) => (
          <button key={k} onClick={() => setMode(k)} data-testid={`sip-mode-${k}`} className={`py-2 rounded-xl text-[12.5px] font-bold ${mode === k ? "bg-white shadow text-[#FF6B35]" : "text-zinc-500"}`}>{l}</button>
        ))}
      </div>
      {mode === "grow"
        ? <Field label="Invest every month" value={monthly} set={setMonthly} min={500} max={100000} step={500} unit="₹" testid="sip-monthly" />
        : <Field label="Money I want" value={target} set={setTarget} min={50000} max={10000000} step={50000} unit="₹" testid="sip-target" />}
      <Field label="Expected return a year" value={rate} set={setRate} min={1} max={20} step={0.5} unit="%" testid="sip-rate" />
      <Field label="For how many years" value={String(y)} set={setYears} min={1} max={40} step={1} unit="yrs" testid="sip-years" />

      {mode === "grow" ? (
        <>
          <div className="rounded-3xl text-white p-4 bg-gradient-to-br from-[#10B981] to-[#2563EB]">
            <div className="text-center text-[12px] opacity-90">You could have about</div>
            <div className="text-center font-[Outfit] font-black text-3xl" data-testid="sip-total">{inrShort(res.total)}</div>
            <div className="grid grid-cols-2 mt-2">
              <Stat label="You put in" value={inrShort(res.invested)} testid="sip-invested" />
              <Stat label="Growth" value={inrShort(res.gain)} testid="sip-gain" />
            </div>
          </div>
          <div className="bg-white border border-zinc-200 rounded-2xl p-3 mt-3">
            <GrowthChart rows={res.rows} />
            <div className="flex gap-4 text-[11.5px] text-zinc-500 justify-center mt-1"><span><b style={{ color: "#93C5FD" }}>■</b> Your money</span><span><b style={{ color: "#10B981" }}>■</b> Growth</span></div>
          </div>
          {y > 3 && <Tip mood="cheer" title="Start early">Waiting 3 years to start the same SIP would leave you with about {inrShort(late)}, which is {inrShort(res.total - late)} less. Time does most of the work.</Tip>}
        </>
      ) : (
        <div className="rounded-3xl text-white p-4 bg-gradient-to-br from-[#10B981] to-[#2563EB] text-center">
          <div className="text-[12px] opacity-90">To reach {inrShort(parseFloat(target) || 0)} in {y} years, invest about</div>
          <div className="font-[Outfit] font-black text-3xl" data-testid="sip-need">{inr(need)} <span className="text-base font-bold">a month</span></div>
        </div>
      )}
      <Tip mood="nervous" title="An estimate, not a promise">Markets go up and down. Nobody can guarantee a return. Use a cautious rate (8 to 12%) and treat the result as a rough guide.</Tip>
    </div>
  );
}

function Emi() {
  const [loan, setLoan] = useState("1000000");
  const [rate, setRate] = useState("10");
  const [years, setYears] = useState("5");
  const p = parseFloat(loan) || 0, r = parseFloat(rate) || 0, months = Math.max(1, Math.round((parseFloat(years) || 0) * 12));
  const e = emi(p, r, months);
  const plus = Math.ceil(e.emi * 1.1);
  const fast = monthsToPayOff(p, r, plus);
  const saved = Number.isFinite(fast) ? e.interest - (plus * fast - p) : 0;
  const pctInterest = e.total ? Math.round((e.interest / e.total) * 100) : 0;
  const bal = loanBalances(p, r, months);
  return (
    <div data-testid="calc-emi">
      <Field label="Loan amount" value={loan} set={setLoan} min={10000} max={10000000} step={10000} unit="₹" testid="emi-loan" />
      <Field label="Interest rate a year" value={rate} set={setRate} min={1} max={30} step={0.25} unit="%" testid="emi-rate" />
      <Field label="Loan period" value={years} set={setYears} min={1} max={30} step={1} unit="yrs" testid="emi-years" />
      <div className="rounded-3xl text-white p-4 bg-gradient-to-br from-[#2563EB] to-[#6366F1]">
        <div className="text-center text-[12px] opacity-90">Your monthly EMI</div>
        <div className="text-center font-[Outfit] font-black text-3xl" data-testid="emi-emi">{inr(e.emi)}</div>
        <div className="grid grid-cols-2 mt-2">
          <Stat label="Total interest" value={inrShort(e.interest)} testid="emi-interest" />
          <Stat label="Total you pay" value={inrShort(e.total)} testid="emi-total" />
        </div>
      </div>
      <div className="bg-white border border-zinc-200 rounded-2xl p-3 mt-3">
        <div className="flex h-3.5 rounded-full overflow-hidden bg-zinc-100 mb-2"><div style={{ width: `${100 - pctInterest}%`, background: "#2563EB" }} /><div style={{ width: `${pctInterest}%`, background: "#EF4444" }} /></div>
        <div className="flex justify-between text-[12.5px] text-zinc-500"><span><b style={{ color: "#2563EB" }}>■</b> Loan {inrShort(p)}</span><span><b style={{ color: "#EF4444" }}>■</b> Interest {pctInterest}%</span></div>
        <p className="text-[12px] text-zinc-500 mt-2">What you still owe after: {bal.filter((_, i) => i % Math.ceil(bal.length / 4) === 0 || i === bal.length - 1).map((b) => `year ${Math.round(b.month / 12 * 10) / 10}: ${inrShort(b.balance)}`).join(" · ")}</p>
      </div>
      {Number.isFinite(fast) && saved > 0 && fast < months && (
        <Tip mood="cheer" title="Pay a little extra">Paying {inr(plus)} instead of {inr(e.emi)} (about 10% more) clears the loan {months - fast} {months - fast === 1 ? "month" : "months"} sooner and saves about {inrShort(saved)} in interest.</Tip>
      )}
      <Tip mood="nervous" title="Before you borrow">A good rule: all your EMIs together should stay under 40% of your monthly income. Check whether you really need the loan, and look at the total you pay, not just the EMI.</Tip>
    </div>
  );
}

function Emergency() {
  const [needs, setNeeds] = useState("20000");
  const [cover, setCover] = useState("6");
  const [saved, setSaved] = useState("0");
  const [build, setBuild] = useState("12");
  const [fromMoney, setFromMoney] = useState(null);
  useEffect(() => {
    api.get("/money/summary").then(({ data }) => { const n = data.summary?.buckets?.needs; if (n > 0) setFromMoney(Math.round(n)); }).catch(() => {});
  }, []);
  const f = emergency(parseFloat(needs) || 0, parseFloat(cover) || 0, parseFloat(saved) || 0, Math.max(1, parseInt(build, 10) || 1));
  return (
    <div data-testid="calc-emergency">
      <Field label="Needs every month (rent, food, bills, EMIs)" value={needs} set={setNeeds} min={2000} max={200000} step={1000} unit="₹" testid="em-needs" />
      {fromMoney && <button onClick={() => setNeeds(String(fromMoney))} className="-mt-2 mb-3 text-[12.5px] font-extrabold text-[#FF6B35]" data-testid="em-use-money">Use my needs this month from My money ({inr(fromMoney)})</button>}
      <Field label="Months you want covered" value={cover} set={setCover} min={3} max={12} step={1} unit="months" testid="em-cover" />
      <Field label="Already saved for this" value={saved} set={setSaved} min={0} max={1000000} step={5000} unit="₹" testid="em-saved" />
      <Field label="Build it within" value={build} set={setBuild} min={1} max={60} step={1} unit="months" testid="em-build" />
      <div className="rounded-3xl text-white p-4 bg-gradient-to-br from-[#F59E0B] to-[#EF4444]">
        <div className="text-center text-[12px] opacity-90">Your emergency fund goal</div>
        <div className="text-center font-[Outfit] font-black text-3xl" data-testid="em-target">{inr(f.target)}</div>
        <div className="h-2.5 rounded-full bg-white/30 overflow-hidden my-2"><div className="h-full bg-white" style={{ width: `${f.pct}%` }} /></div>
        <div className="text-center text-[13px]" data-testid="em-plan">
          {f.gap === 0 ? "You are fully covered. Well done!" : <>Save <b className="font-[Outfit] text-lg">{inr(f.monthly)}</b> a month for {Math.max(1, parseInt(build, 10) || 1)} months to close the {inr(f.gap)} gap.</>}
        </div>
      </div>
      <Tip mood="happy" title="What it is for">An emergency fund pays for surprises like a job loss, a medical bill or a broken phone, so you do not need to borrow. Keep it somewhere safe and easy to reach, such as a savings account, not in shares.</Tip>
    </div>
  );
}

export default function Calculators() {
  const [tab, setTab] = useState("sip");
  return (
    <div className="max-w-md mx-auto pb-24" data-testid="calculators-page">
      <Link to="/money" className="inline-flex items-center gap-1 text-[13px] font-bold text-zinc-500 mb-2"><ChevronLeft className="w-4 h-4" />My money</Link>
      <h1 className="font-[Outfit] font-black text-2xl tracking-tight mb-3">Calculators</h1>
      <div className="grid grid-cols-3 gap-1 bg-zinc-100 rounded-2xl p-1 mb-4">
        {[["sip", "SIP"], ["emi", "Loan EMI"], ["emergency", "Emergency fund"]].map(([k, l]) => (
          <button key={k} onClick={() => setTab(k)} data-testid={`tab-${k}`} className={`py-2 rounded-xl text-[12.5px] font-bold ${tab === k ? "bg-white shadow text-[#FF6B35]" : "text-zinc-500"}`}>{l}</button>
        ))}
      </div>
      {tab === "sip" && <Sip />}
      {tab === "emi" && <Emi />}
      {tab === "emergency" && <Emergency />}
    </div>
  );
}
