import React, { useCallback, useEffect, useState } from "react";
import { Flame, Snowflake } from "lucide-react";
import { api, formatApiError } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { streakState } from "@/lib/streak";

const FREEZE_COST = 30;
const FREEZE_MAX_FREE = 2;
const FREEZE_MAX_PRO = 5; // Pro members can hold more freezes
const WEEK_GOAL = 5;

// Streak and the seven days of this week in one warm card: done days glow, today pulses, missed days stay neutral, future days are dashed.
export default function StreakWeek() {
  const { user, stats, refreshStats, isPro } = useAuth();
  const FREEZE_MAX = isPro ? FREEZE_MAX_PRO : FREEZE_MAX_FREE;
  const [week, setWeek] = useState(null);
  const [buying, setBuying] = useState(false);
  const [msg, setMsg] = useState("");

  const load = useCallback(() => { api.get("/quests/today").then((r) => setWeek(r.data.week)).catch(() => {}); }, []);
  useEffect(() => {
    load();
    window.addEventListener("fl-quests-changed", load);
    return () => window.removeEventListener("fl-quests-changed", load);
  }, [load]);

  const streak = stats?.streak_days || 0;
  const freezes = stats?.streak_freezes || 0;
  const st = streakState(stats, stats?.daily_goal_minutes || 5);
  const buyFreeze = async () => {
    setBuying(true); setMsg("");
    try { await api.post("/shop/streak-freeze"); await refreshStats(); setMsg("Streak freeze added."); }
    catch (e) { setMsg(formatApiError(e)); }
    setBuying(false);
  };

  // Days inside the current streak count as practised even if no quest was claimed that day.
  const streakDates = new Set();
  if (streak > 0 && !stats?.streak_broken && stats?.last_active_date) {
    const base = new Date(`${stats.last_active_date}T12:00:00Z`);
    for (let k = 0; k < streak; k++) streakDates.add(new Date(base.getTime() - k * 86400000).toISOString().slice(0, 10));
  }
  const practised = (w) => !!w.on || streakDates.has(String(w.date));
  const todayIdx = week ? week.findIndex((w) => w.today) : -1;
  // Days before sign-up are not "missed" (compare in the learner's own timezone, like the week itself).
  const joined = (() => {
    const d = user?.created_at ? new Date(user.created_at) : null;
    return d && !isNaN(d) ? `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}` : "";
  })();
  const doneDays = week ? week.filter(practised).length : 0;
  const canBuy = !buying && freezes < FREEZE_MAX && (stats?.coins || 0) >= FREEZE_COST;

  return (
    <section className="mb-6 rounded-3xl border-2 border-[#FFD2B3] bg-gradient-to-br from-[#FFF6EC] to-[#FFE7D6] p-4" data-testid="streak-week">
      <div className="flex items-center gap-3">
        <span className="w-14 h-14 rounded-2xl grid place-items-center bg-gradient-to-br from-[#FF6B35] to-[#FBBF24] text-white shadow-md shrink-0"><Flame className="w-8 h-8" fill="currentColor" /></span>
        <div className="flex-1 min-w-0">
          <p className="font-[Outfit] font-black text-3xl leading-none tabular-nums" data-testid="streak-count">{streak}<span className="text-base font-extrabold text-zinc-700 ml-1.5">day streak</span></p>
          {st.atRisk
            ? <p className="text-[12.5px] font-bold text-[#E5484D] mt-1" data-testid="streak-risk">Your streak is at risk tonight</p>
            : <p className="text-[12.5px] text-zinc-600 mt-1">Practise every day to keep the flame.</p>}
        </div>
        <button onClick={buyFreeze} disabled={!canBuy} data-testid="btn-buy-freeze" aria-label="Get a streak freeze"
          className="shrink-0 rounded-2xl bg-white border border-blue-200 px-2.5 py-1.5 text-center disabled:opacity-60 active:scale-95">
          <span className="flex items-center justify-center gap-1 text-[12px] font-extrabold text-blue-700"><Snowflake className="w-3.5 h-3.5" /><span data-testid="freeze-count">{freezes}</span>/{FREEZE_MAX}</span>
          <span className="block text-[10.5px] font-bold text-blue-600 leading-tight">{freezes >= FREEZE_MAX ? "Max" : `Get · ${FREEZE_COST}`}</span>
        </button>
      </div>
      {msg && <p className="text-[12px] text-zinc-600 mt-2" role="status">{msg}</p>}

      <div className="grid grid-cols-7 gap-1.5 text-center mt-4" aria-label="This week">
        {(week || Array.from({ length: 7 }, (_, i) => ({ date: i, label: "·" }))).map((w, i) => {
          const today = i === todayIdx;
          const future = todayIdx >= 0 && i > todayIdx;
          const on = practised(w);
          const before = !on && !today && !future && joined && String(w.date) < joined;
          let cls = "bg-[#FFE3D0]"; // missed: warm and quiet, never red
          if (on) cls = "bg-gradient-to-br from-[#FF6B35] to-[#FBBF24] text-white shadow";
          else if (today) cls = "bg-white border-2 border-[#FF6B35] ring-4 ring-[#FF6B35]/20 animate-pulse";
          else if (future) cls = "bg-transparent border-2 border-dashed border-[#F2BE9B]";
          else if (before) cls = "bg-transparent border-2 border-dotted border-[#F2D5BF]";
          return (
            <div key={w.date}>
              <div className={`w-9 h-9 rounded-full grid place-items-center mx-auto ${cls}`} data-testid={`week-day-${i}`} data-state={on ? "done" : today ? "today" : future ? "future" : before ? "before" : "missed"}>
                {on && <Flame className="w-4 h-4" fill="currentColor" />}
              </div>
              <p className={`text-[11px] mt-1 font-bold ${today ? "text-[#FF6B35]" : "text-zinc-600"}`}>{w.label}</p>
            </div>
          );
        })}
      </div>

      <div className="mt-3.5">
        <div className="flex justify-between text-[12px] font-bold text-zinc-700 mb-1"><span>Aim for {WEEK_GOAL} days this week</span><span className="tabular-nums" data-testid="week-goal">{Math.min(doneDays, WEEK_GOAL)} / {WEEK_GOAL}</span></div>
        <div className="h-2.5 rounded-full bg-white/80 overflow-hidden"><div className="h-full rounded-full bg-gradient-to-r from-[#FF6B35] to-[#FBBF24] transition-all duration-700" style={{ width: `${Math.min(100, (doneDays / WEEK_GOAL) * 100)}%` }} /></div>
        <p className="text-[11.5px] text-zinc-600 mt-1.5">A day lights up when you practise or claim a quest. A freeze saves your streak if you miss a day.</p>
      </div>
    </section>
  );
}
