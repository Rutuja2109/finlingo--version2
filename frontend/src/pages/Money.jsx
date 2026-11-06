import React, { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ChevronLeft, ChevronRight, Plus, Trash2, Target, PiggyBank, Calculator } from "lucide-react";
import { api, formatApiError } from "@/lib/api";
import Lumi from "@/components/Lumi";

const inr = (n, d = 0) => "₹" + Math.abs(Number(n)).toLocaleString("en-IN", { minimumFractionDigits: d, maximumFractionDigits: d });
const BUCKET = {
  needs: { label: "Needs", color: "#2563EB", target: 50 },
  wants: { label: "Wants", color: "#EC4899", target: 30 },
  savings: { label: "Savings", color: "#10B981", target: 20 },
};
const CATS = [
  ["rent", "Rent and home", "needs"], ["food", "Groceries and food", "needs"], ["transport", "Transport", "needs"], ["bills", "Bills and recharge", "needs"],
  ["education", "Education", "needs"], ["health", "Health", "needs"], ["emi", "EMI and loans", "needs"],
  ["eating_out", "Eating out", "wants"], ["shopping", "Shopping", "wants"], ["fun", "Movies and fun", "wants"], ["subs", "Subscriptions", "wants"], ["travel", "Trips", "wants"],
  ["sip", "SIP and investing", "savings"], ["savings", "Savings", "savings"], ["emergency", "Emergency fund", "savings"],
];
const CAT_LABEL = Object.fromEntries(CATS.map((c) => [c[0], c[1]]));
const monthLabel = (m) => new Date(`${m}-01T00:00:00`).toLocaleDateString("en-IN", { month: "long", year: "numeric" });
const shiftMonth = (m, n) => { const [y, mo] = m.split("-").map(Number); const d = new Date(y, mo - 1 + n, 1); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`; };
const localToday = () => { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`; };
const dayLabel = (d) => new Date(`${d}T00:00:00`).toLocaleDateString("en-IN", { weekday: "short", day: "numeric", month: "short" });
const cleanNum = (v) => v.replace(/[^\d.]/g, "").replace(/(\..*)\./g, "$1");

function Sheet({ title, onClose, children, testid }) {
  return (
    <div className="fixed inset-0 z-50 bg-black/45 flex items-end justify-center" onClick={onClose}>
      <div className="bg-white rounded-t-[26px] w-full max-w-md px-4 pt-4 pb-6 max-h-[92vh] overflow-y-auto" onClick={(e) => e.stopPropagation()} data-testid={testid}>
        <h3 className="font-[Outfit] font-black text-xl mb-3">{title}</h3>
        {children}
      </div>
    </div>
  );
}

const toneCls = { warn: "bg-amber-50 border-amber-300", bad: "bg-red-50 border-red-300", good: "bg-emerald-50 border-emerald-300", "": "bg-white border-zinc-200" };

export default function Money() {
  const [month, setMonth] = useState(localToday().slice(0, 7));
  const [data, setData] = useState(null);
  const [goals, setGoals] = useState([]);
  const [err, setErr] = useState("");
  const [sheet, setSheet] = useState(null); // "entry" | "goal" | {addTo: goal}

  const load = useCallback(async () => {
    try {
      const [s, g] = await Promise.all([api.get("/money/summary", { params: { month } }), api.get("/money/goals")]);
      setData(s.data); setGoals(g.data); setErr("");
    } catch (e) { setErr(formatApiError(e)); }
  }, [month]);
  useEffect(() => { setData(null); load(); }, [load]);

  const removeEntry = async (id) => {
    if (!window.confirm("Delete this entry?")) return;
    try { await api.delete(`/money/entries/${id}`); load(); } catch (e) { setErr(formatApiError(e)); }
  };
  const removeGoal = async (id) => {
    if (!window.confirm("Delete this goal?")) return;
    try { await api.delete(`/money/goals/${id}`); load(); } catch (e) { setErr(formatApiError(e)); }
  };

  const s = data?.summary;
  const byDay = {};
  (data?.entries || []).forEach((e) => { (byDay[e.date] = byDay[e.date] || []).push(e); });

  return (
    <div className="max-w-md mx-auto pb-24" data-testid="money-page">
      <div className="flex items-center justify-between mb-3">
        <button onClick={() => setMonth(shiftMonth(month, -1))} aria-label="Previous month" className="w-10 h-10 grid place-items-center rounded-full bg-zinc-100"><ChevronLeft className="w-5 h-5" /></button>
        <h1 className="font-[Outfit] font-black text-xl" data-testid="money-month">{monthLabel(month)}</h1>
        <button onClick={() => setMonth(shiftMonth(month, 1))} aria-label="Next month" className="w-10 h-10 grid place-items-center rounded-full bg-zinc-100"><ChevronRight className="w-5 h-5" /></button>
      </div>

      <Link to="/calculators" data-testid="money-calculators" className="flex items-center justify-between bg-white border border-zinc-200 rounded-2xl px-3.5 py-2.5 mb-3 text-[13px] font-bold">
        <span className="flex items-center gap-2"><Calculator className="w-4 h-4 text-[#FF6B35]" />SIP, loan EMI and emergency fund calculators</span><ChevronRight className="w-4 h-4 text-zinc-400" />
      </Link>
      {err && <div className="mb-2 text-[12.5px] text-red-700 bg-red-50 rounded-xl px-3 py-2">{err}</div>}
      {!data && !err && <div className="py-16 text-center text-zinc-500">Loading your money…</div>}

      {data && (
        <>
          <div className="rounded-3xl text-white p-4 bg-gradient-to-br from-[#2563EB] via-[#6366F1] to-[#EC4899]">
            <div className="grid grid-cols-3 text-center gap-2">
              <div><div className="text-[11px] font-semibold opacity-90">Income</div><div className="font-[Outfit] font-black text-lg" data-testid="money-income">{inr(s.income)}</div></div>
              <div><div className="text-[11px] font-semibold opacity-90">Spent</div><div className="font-[Outfit] font-black text-lg" data-testid="money-spent">{inr(s.spent)}</div></div>
              <div><div className="text-[11px] font-semibold opacity-90">Left</div><div className="font-[Outfit] font-black text-lg" data-testid="money-left">{s.left < 0 ? "−" : ""}{inr(s.left)}</div></div>
            </div>
            <p className="text-center text-[11.5px] opacity-90 mt-2">Savings you set aside are not counted as spent.</p>
          </div>

          <div className="mt-3 bg-white border border-zinc-200 rounded-[20px] p-3.5" data-testid="money-split">
            <p className="text-[11px] font-bold tracking-[.2em] uppercase text-zinc-500 mb-2">Your 50 / 30 / 20 split</p>
            <div className="flex h-3.5 rounded-full overflow-hidden bg-zinc-100 mb-3">
              {Object.keys(BUCKET).map((k) => <div key={k} style={{ width: `${Math.min(100, s.pct[k])}%`, background: BUCKET[k].color }} />)}
            </div>
            {Object.keys(BUCKET).map((k) => {
              const b = BUCKET[k], p = s.pct[k], over = k !== "savings" ? p > b.target : p < b.target && s.has_income;
              return (
                <div key={k} className="flex items-center justify-between py-1.5 text-sm" data-testid={`split-${k}`}>
                  <span className="flex items-center gap-2"><span className="w-3 h-3 rounded-full" style={{ background: b.color }} /><b>{b.label}</b></span>
                  <span className="text-zinc-500">{inr(s.buckets[k])} · <b className={over ? "text-amber-600" : "text-emerald-700"}>{Math.round(p)}%</b> of {b.target}%</span>
                </div>
              );
            })}
            {!s.has_income && <p className="text-[12px] text-zinc-500 mt-1">Percentages use your total logged money until you add income.</p>}
          </div>

          <div className={`flex gap-3 items-start border rounded-2xl px-3 py-2.5 mt-3 text-[13px] leading-relaxed ${toneCls[data.coach.tone]}`} data-testid="money-coach">
            <Lumi size={44} mood={data.coach.mood} className="shrink-0" />
            <div><b className="font-[Outfit]">{data.coach.title}</b><br />{data.coach.text}</div>
          </div>

          <button onClick={() => setSheet("entry")} data-testid="money-add"
            className="w-full mt-3 rounded-2xl py-3.5 bg-[#FF6B35] text-white font-[Outfit] font-black text-base flex items-center justify-center gap-2 active:scale-[.98]"><Plus className="w-5 h-5" />Add money in or out</button>

          {/* Entries */}
          <div className="mt-4">
            <p className="text-[11px] font-bold tracking-[.2em] uppercase text-zinc-500 mb-1.5 px-1">This month</p>
            {data.entries.length === 0 && <p className="text-[13px] text-zinc-500 px-1">Nothing logged yet. Add what you spend, it takes five seconds.</p>}
            {Object.keys(byDay).map((d) => (
              <div key={d} className="mb-2">
                <div className="text-[12px] font-bold text-zinc-400 px-1 mb-1">{dayLabel(d)}</div>
                <div className="bg-white border border-zinc-200 rounded-2xl px-3">
                  {byDay[d].map((e) => (
                    <div key={e.id} className="flex items-center gap-2 py-2.5 border-t first:border-t-0 border-zinc-100 text-sm" data-testid="money-entry">
                      <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ background: e.bucket ? BUCKET[e.bucket].color : "#10B981" }} />
                      <div className="flex-1 min-w-0"><b>{e.kind === "income" ? "Income" : CAT_LABEL[e.category]}</b>{e.note && <div className="text-[12px] text-zinc-500 truncate">{e.note}</div>}</div>
                      <b className={e.kind === "income" ? "text-emerald-700" : ""}>{e.kind === "income" ? "+" : "−"}{inr(e.amount)}</b>
                      <button onClick={() => removeEntry(e.id)} aria-label="Delete entry" className="p-1.5 text-zinc-400"><Trash2 className="w-4 h-4" /></button>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      {/* Goals */}
      <div className="mt-6" data-testid="money-goals">
        <div className="flex items-center justify-between px-1 mb-2">
          <p className="text-[11px] font-bold tracking-[.2em] uppercase text-zinc-500">Savings goals</p>
          <button onClick={() => setSheet("goal")} data-testid="goal-new" className="text-[13px] font-extrabold text-[#FF6B35] flex items-center gap-1"><Plus className="w-4 h-4" />New goal</button>
        </div>
        {goals.length === 0 && (
          <div className="bg-white border border-zinc-200 rounded-2xl p-3.5 text-[13px] text-zinc-600 flex gap-3"><Target className="w-5 h-5 text-[#FF6B35] shrink-0 mt-0.5" />Want a ₹50,000 phone in 6 months? Add it as a goal and I will tell you how much to save each month.</div>
        )}
        {goals.map((g) => (
          <div key={g.id} className="bg-white border border-zinc-200 rounded-2xl p-3.5 mb-2.5" data-testid="goal-card">
            <div className="flex items-start justify-between gap-2">
              <div><b className="font-[Outfit] text-base">{g.name}</b><div className="text-[12.5px] text-zinc-500">{inr(g.saved)} of {inr(g.target)}</div></div>
              <button onClick={() => removeGoal(g.id)} aria-label="Delete goal" className="p-1.5 text-zinc-400"><Trash2 className="w-4 h-4" /></button>
            </div>
            <div className="h-2.5 rounded-full bg-zinc-100 overflow-hidden my-2"><div className="h-full bg-emerald-500" style={{ width: `${g.pct}%` }} /></div>
            <div className="flex items-center justify-between gap-2">
              <div className="text-[13px]" data-testid="goal-monthly">
                {g.done ? <b className="text-emerald-700">Goal reached! 🎉</b>
                  : g.overdue ? <b className="text-amber-700">Deadline passed, {inr(g.left)} to go</b>
                    : <>Save <b>{inr(g.monthly)}</b> a month for {g.months_left} {g.months_left === 1 ? "month" : "months"}</>}
              </div>
              {!g.done && <button onClick={() => setSheet({ addTo: g })} className="rounded-xl bg-emerald-50 text-emerald-700 font-[Outfit] font-extrabold text-[13px] px-3 py-1.5 flex items-center gap-1 shrink-0"><PiggyBank className="w-4 h-4" />Add</button>}
            </div>
          </div>
        ))}
      </div>

      {sheet === "entry" && <EntrySheet onClose={() => setSheet(null)} onSaved={(d) => { setSheet(null); if (d && d.slice(0, 7) !== month) setMonth(d.slice(0, 7)); else load(); }} />}
      {sheet === "goal" && <GoalSheet onClose={() => setSheet(null)} onSaved={() => { setSheet(null); load(); }} />}
      {sheet?.addTo && <AddSavedSheet goal={sheet.addTo} onClose={() => setSheet(null)} onSaved={() => { setSheet(null); load(); }} />}
    </div>
  );
}

function EntrySheet({ onClose, onSaved }) {
  const [kind, setKind] = useState("expense");
  const [amount, setAmount] = useState("");
  const [cat, setCat] = useState("food");
  const [note, setNote] = useState("");
  const [date, setDate] = useState(localToday());
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  const amt = parseFloat(amount);
  const valid = amt > 0 && (kind === "income" || cat);
  const save = async () => {
    setBusy(true); setErr("");
    try {
      await api.post("/money/entries", { kind, amount: amt, category: kind === "expense" ? cat : null, note, date });
      onSaved(date);
    } catch (e) { setErr(formatApiError(e)); setBusy(false); }
  };
  return (
    <Sheet title="Add to your money" onClose={onClose} testid="entry-sheet">
      <div className="grid grid-cols-2 gap-1 bg-zinc-100 rounded-2xl p-1 mb-3">
        {[["expense", "Money out"], ["income", "Money in"]].map(([k, l]) => (
          <button key={k} onClick={() => setKind(k)} data-testid={`kind-${k}`} className={`py-2 rounded-xl text-[13px] font-bold ${kind === k ? "bg-white shadow text-[#FF6B35]" : "text-zinc-500"}`}>{l}</button>
        ))}
      </div>
      <label className="text-[12px] font-bold text-zinc-500">Amount (₹)</label>
      <input value={amount} onChange={(e) => setAmount(cleanNum(e.target.value))} inputMode="decimal" placeholder="0" autoFocus data-testid="entry-amount"
        className="w-full border-2 border-zinc-200 rounded-2xl px-3 py-2.5 font-[Outfit] font-black text-2xl mb-3 focus:border-[#FF6B35] outline-none" />
      {kind === "expense" && (
        <>
          <label className="text-[12px] font-bold text-zinc-500">What was it for?</label>
          <div className="flex flex-wrap gap-2 my-2 mb-3">
            {CATS.map(([id, label, b]) => (
              <button key={id} onClick={() => setCat(id)} data-testid={`cat-${id}`}
                className={`rounded-full border-2 px-3 py-1.5 text-[13px] font-bold ${cat === id ? "text-white" : "bg-white text-zinc-700 border-zinc-200"}`}
                style={cat === id ? { background: BUCKET[b].color, borderColor: BUCKET[b].color } : {}}>{label}</button>
            ))}
          </div>
          <p className="text-[12px] text-zinc-500 -mt-1 mb-3">Colors: <b style={{ color: BUCKET.needs.color }}>needs</b>, <b style={{ color: BUCKET.wants.color }}>wants</b>, <b style={{ color: BUCKET.savings.color }}>savings</b>.</p>
        </>
      )}
      <label className="text-[12px] font-bold text-zinc-500">Note (optional)</label>
      <input value={note} onChange={(e) => setNote(e.target.value)} maxLength={80} placeholder={kind === "income" ? "Pocket money, salary…" : "Lunch with friends…"}
        className="w-full border-2 border-zinc-200 rounded-2xl px-3 py-2.5 mb-3 text-sm outline-none focus:border-[#FF6B35]" />
      <label className="text-[12px] font-bold text-zinc-500">Date</label>
      <input type="date" value={date} max={localToday()} onChange={(e) => setDate(e.target.value || localToday())}
        className="w-full border-2 border-zinc-200 rounded-2xl px-3 py-2.5 mb-3 text-sm outline-none focus:border-[#FF6B35]" />
      {err && <p className="text-red-700 text-[13px] mb-2">{err}</p>}
      <button onClick={save} disabled={!valid || busy} data-testid="entry-save" className="w-full rounded-2xl py-3.5 font-[Outfit] font-black text-base text-white bg-[#FF6B35] disabled:opacity-50">Save</button>
      <button onClick={onClose} className="w-full rounded-2xl py-3 mt-2 bg-zinc-100 font-[Outfit] font-extrabold">Cancel</button>
    </Sheet>
  );
}

function GoalSheet({ onClose, onSaved }) {
  const [name, setName] = useState("");
  const [target, setTarget] = useState("");
  const [months, setMonths] = useState("6");
  const [saved, setSaved] = useState("");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  const t = parseFloat(target) || 0, m = parseInt(months, 10) || 0, sv = parseFloat(saved) || 0;
  const monthly = m > 0 && t > sv ? (t - sv) / m : 0;
  const valid = name.trim() && t > 0 && m >= 1 && m <= 120 && sv <= t;
  const save = async () => {
    setBusy(true); setErr("");
    try { await api.post("/money/goals", { name, target: t, months: m, saved: sv }); onSaved(); }
    catch (e) { setErr(formatApiError(e)); setBusy(false); }
  };
  return (
    <Sheet title="New savings goal" onClose={onClose} testid="goal-sheet">
      <label className="text-[12px] font-bold text-zinc-500">What are you saving for?</label>
      <input value={name} onChange={(e) => setName(e.target.value)} maxLength={40} placeholder="New phone, trip, laptop…" data-testid="goal-name" autoFocus
        className="w-full border-2 border-zinc-200 rounded-2xl px-3 py-2.5 mb-3 text-sm outline-none focus:border-[#FF6B35]" />
      <label className="text-[12px] font-bold text-zinc-500">How much does it cost? (₹)</label>
      <input value={target} onChange={(e) => setTarget(cleanNum(e.target.value))} inputMode="decimal" placeholder="50000" data-testid="goal-target"
        className="w-full border-2 border-zinc-200 rounded-2xl px-3 py-2.5 mb-3 font-[Outfit] font-black text-xl outline-none focus:border-[#FF6B35]" />
      <label className="text-[12px] font-bold text-zinc-500">In how many months?</label>
      <div className="flex gap-2 my-2">
        {["3", "6", "12", "24"].map((x) => <button key={x} onClick={() => setMonths(x)} className={`border-2 rounded-[14px] px-3.5 py-2 font-[Outfit] font-extrabold text-sm ${months === x ? "border-[#FF6B35] bg-[#FF6B35]/10" : "border-zinc-200"}`}>{x}</button>)}
        <input value={months} onChange={(e) => setMonths(e.target.value.replace(/\D/g, "").slice(0, 3))} inputMode="numeric" aria-label="Months" data-testid="goal-months"
          className="w-16 border-2 border-zinc-200 rounded-[14px] px-2 text-center font-[Outfit] font-extrabold text-sm outline-none focus:border-[#FF6B35]" />
      </div>
      <label className="text-[12px] font-bold text-zinc-500">Already saved (optional, ₹)</label>
      <input value={saved} onChange={(e) => setSaved(cleanNum(e.target.value))} inputMode="decimal" placeholder="0"
        className="w-full border-2 border-zinc-200 rounded-2xl px-3 py-2.5 mb-3 text-sm outline-none focus:border-[#FF6B35]" />
      <div className="rounded-2xl bg-emerald-50 border border-emerald-200 px-3 py-2.5 mb-3 text-[13.5px]" data-testid="goal-preview">
        {monthly > 0 ? <>Save <b className="font-[Outfit] text-lg">{inr(monthly)}</b> a month for {m} months.</> : "Fill in the cost and months to see how much to save."}
      </div>
      {err && <p className="text-red-700 text-[13px] mb-2">{err}</p>}
      <button onClick={save} disabled={!valid || busy} data-testid="goal-save" className="w-full rounded-2xl py-3.5 font-[Outfit] font-black text-base text-white bg-[#FF6B35] disabled:opacity-50">Create goal</button>
      <button onClick={onClose} className="w-full rounded-2xl py-3 mt-2 bg-zinc-100 font-[Outfit] font-extrabold">Cancel</button>
    </Sheet>
  );
}

function AddSavedSheet({ goal, onClose, onSaved }) {
  const [amount, setAmount] = useState(String(Math.round(goal.monthly) || ""));
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  const amt = parseFloat(amount);
  const save = async () => {
    setBusy(true); setErr("");
    try { await api.post(`/money/goals/${goal.id}/add`, { amount: amt }); onSaved(); }
    catch (e) { setErr(formatApiError(e)); setBusy(false); }
  };
  return (
    <Sheet title={`Add to ${goal.name}`} onClose={onClose} testid="addsaved-sheet">
      <p className="text-[13px] text-zinc-500 mb-2">You have {inr(goal.saved)} of {inr(goal.target)}. Put the amount you just set aside.</p>
      <input value={amount} onChange={(e) => setAmount(cleanNum(e.target.value))} inputMode="decimal" autoFocus data-testid="addsaved-amount"
        className="w-full border-2 border-zinc-200 rounded-2xl px-3 py-2.5 mb-3 font-[Outfit] font-black text-2xl outline-none focus:border-[#FF6B35]" />
      {err && <p className="text-red-700 text-[13px] mb-2">{err}</p>}
      <button onClick={save} disabled={!(amt > 0) || busy} data-testid="addsaved-save" className="w-full rounded-2xl py-3.5 font-[Outfit] font-black text-base text-white bg-emerald-500 disabled:opacity-50">Add to goal</button>
      <button onClick={onClose} className="w-full rounded-2xl py-3 mt-2 bg-zinc-100 font-[Outfit] font-extrabold">Cancel</button>
    </Sheet>
  );
}
