import React, { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Zap, BookOpen, Star, Repeat, LineChart, Wallet, Gift, Lock, CheckCircle2, Target, Coins } from "lucide-react";
import { api, formatApiError } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import Lumi from "@/components/Lumi";

const META = {
  xp: { Icon: Zap, bg: "#FFFBEB", fg: "#F59E0B" },
  lesson: { Icon: BookOpen, bg: "#EFF6FF", fg: "#2563EB" },
  perfect: { Icon: Star, bg: "#FEF3C7", fg: "#D97706" },
  revise: { Icon: Repeat, bg: "#ECFDF5", fg: "#10B981", to: "/revise" },
  trade: { Icon: LineChart, bg: "#FDF2F8", fg: "#EC4899", to: "/practice" },
  log: { Icon: Wallet, bg: "#EEF2FF", fg: "#6366F1", to: "/money" },
};
const hm = (s) => `${Math.floor(s / 3600)}h ${Math.floor((s % 3600) / 60)}m`;

export default function DailyQuests() {
  const { refreshStats } = useAuth();
  const [d, setD] = useState(null);
  const [msg, setMsg] = useState("");
  const [busy, setBusy] = useState(false);

  const load = useCallback(async () => {
    try { setD((await api.get("/quests/today")).data); } catch { /* quests are optional, hide on failure */ }
  }, []);
  useEffect(() => { load(); }, [load]);

  const act = async (call, text) => {
    if (busy) return;
    setBusy(true);
    try {
      const { data } = await call();
      setMsg(text(data));
      setTimeout(() => setMsg(""), 2500);
      await Promise.all([load(), refreshStats?.()]);
    } catch (e) { setMsg(formatApiError(e)); setTimeout(() => setMsg(""), 3000); }
    setBusy(false);
  };

  if (!d) return null;
  const n = d.done_count;
  const allDone = d.claimed_count === 3 && d.chest.opened;
  const mood = allDone || n === 3 ? "cheer" : "happy";

  return (
    <section className="mb-10" data-testid="daily-quests">
      <div className="rounded-3xl bg-gradient-to-br from-[#6366F1] via-[#8B5CF6] to-[#EC4899] text-white p-5 relative overflow-hidden mb-3">
        <div className="absolute -right-1 -top-1 opacity-40 pointer-events-none"><Lumi size={96} mood={mood} /></div>
        <p className="uppercase tracking-[0.2em] text-[11px] font-bold text-white/90 mb-1 relative"><Target className="w-3.5 h-3.5 inline -mt-0.5 mr-1" />Daily quests</p>
        <h2 className="font-[Outfit] font-black text-2xl leading-tight max-w-[70%] relative" data-testid="quests-headline">
          {allDone ? "All done. See you tomorrow!" : n === 3 ? "All quests done. Claim your rewards!" : `${n} of 3 done today`}
        </h2>
        <div className="h-3 rounded-full bg-white/30 overflow-hidden mt-3 relative"><div className="h-full bg-white rounded-full transition-all duration-500" style={{ width: `${Math.round((n / 3) * 100)}%` }} /></div>
        <p className="text-[12px] text-white/90 mt-2 relative">Resets in {hm(d.resets_in_seconds)}</p>
      </div>

      <div className="bg-white border border-zinc-200 rounded-3xl px-4">
        {d.quests.map((q) => {
          const m = META[q.id], pct = Math.round((q.progress / q.goal) * 100);
          return (
            <div key={q.id} className="flex items-center gap-3 py-3 border-t first:border-t-0 border-zinc-100" data-testid={`quest-${q.id}`}>
              <div className="w-11 h-11 rounded-[14px] grid place-items-center shrink-0" style={{ background: m.bg, color: m.fg }}><m.Icon className="w-5 h-5" /></div>
              <div className="flex-1 min-w-0">
                {m.to && !q.done
                  ? <Link to={m.to} className="font-[Outfit] font-extrabold text-[15px] underline decoration-zinc-300 underline-offset-2">{q.title}</Link>
                  : <div className="font-[Outfit] font-extrabold text-[15px]">{q.title}</div>}
                <div className="h-2 rounded-full bg-zinc-100 overflow-hidden mt-1.5"><div className="h-full rounded-full transition-all duration-500" style={{ width: `${pct}%`, background: m.fg }} /></div>
                <div className="text-[12px] text-zinc-500 mt-1">{q.progress} / {q.goal}</div>
              </div>
              {q.claimed
                ? <CheckCircle2 className="w-6 h-6 text-emerald-500 shrink-0" aria-label="Claimed" />
                : q.done
                  ? <button onClick={() => act(() => api.post("/quests/claim", { id: q.id }), (r) => `+${r.coins} coins`)} disabled={busy} data-testid={`claim-${q.id}`}
                    className="rounded-xl bg-[#FF6B35] text-white font-[Outfit] font-extrabold text-[13px] px-3.5 py-2 shrink-0 active:scale-95">Claim +{q.reward}</button>
                  : <span className="flex items-center gap-1 rounded-full bg-zinc-100 px-2.5 py-1 text-[12px] font-extrabold font-[Outfit] shrink-0"><Coins className="w-3.5 h-3.5 text-amber-500" />+{q.reward}</span>}
            </div>
          );
        })}
      </div>

      <div className="bg-white border border-zinc-200 rounded-3xl p-4 mt-3 flex items-center gap-3.5" data-testid="quest-chest">
        <div className="w-16 h-16 rounded-[20px] grid place-items-center shrink-0" style={{ background: d.chest.opened ? "#ECFDF5" : "#FFF7ED", color: d.chest.opened ? "#10B981" : "#FF6B35" }}><Gift className="w-8 h-8" /></div>
        <div className="flex-1">
          <div className="font-[Outfit] font-extrabold text-base">Daily chest</div>
          <div className="text-[13px] text-zinc-500">{d.chest.opened ? `Opened: +${d.chest.reward} coins` : `Claim all 3 quests to open it for +${d.chest.reward} coins`}</div>
        </div>
        {d.chest.ready
          ? <button onClick={() => act(() => api.post("/quests/chest"), (r) => `Chest opened: +${r.coins} coins`)} disabled={busy} data-testid="open-chest" className="rounded-xl bg-[#FF6B35] text-white font-[Outfit] font-extrabold text-[13px] px-3.5 py-2 active:scale-95">Open</button>
          : d.chest.opened ? <CheckCircle2 className="w-6 h-6 text-emerald-500" /> : <Lock className="w-5 h-5 text-zinc-400" aria-label="Locked" />}
      </div>

      <div className="bg-white border border-zinc-200 rounded-3xl p-4 mt-3">
        <p className="uppercase tracking-[0.22em] text-[11px] font-bold text-zinc-500 mb-2">This week</p>
        <div className="grid grid-cols-7 gap-1.5 text-center text-[11px] font-bold text-zinc-500">
          {d.week.map((w) => (
            <div key={w.date}>{w.label}
              <div className={`w-[30px] h-[30px] rounded-full grid place-items-center mx-auto mt-1 ${w.on ? "bg-[#FF6B35] text-white" : "bg-zinc-100 text-zinc-300"} ${w.today ? "outline outline-2 outline-offset-2 outline-[#FF6B35]" : ""}`}>
                {w.on && <CheckCircle2 className="w-4 h-4" />}
              </div>
            </div>
          ))}
        </div>
        <p className="text-[12px] text-zinc-500 mt-3">A day lights up when you claim at least one quest.</p>
      </div>

      {msg && <div className="fixed bottom-24 inset-x-4 z-50 mx-auto max-w-sm bg-zinc-900 text-white text-center rounded-2xl py-3 font-bold text-sm" role="status" data-testid="quest-toast">{msg}</div>}
    </section>
  );
}
