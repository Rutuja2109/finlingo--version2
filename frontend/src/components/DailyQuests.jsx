import React, { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Newspaper, Zap, BookOpen, Star, Repeat, LineChart, Wallet, Gift, Lock, CheckCircle2, Target, Coins, ChevronDown } from "lucide-react";
import { api, formatApiError } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";

const META = {
  xp: { Icon: Zap, bg: "#FFFBEB", fg: "#F59E0B" },
  lesson: { Icon: BookOpen, bg: "#EFF6FF", fg: "#2563EB" },
  perfect: { Icon: Star, bg: "#FEF3C7", fg: "#D97706" },
  revise: { Icon: Repeat, bg: "#ECFDF5", fg: "#10B981", to: "/revise" },
  explainer: { Icon: Newspaper, bg: "#FEF3C7", fg: "#D97706", to: "/explainer" },
  trade: { Icon: LineChart, bg: "#FDF2F8", fg: "#EC4899", to: "/practice" },
  log: { Icon: Wallet, bg: "#EEF2FF", fg: "#6366F1", to: "/money" },
};
const hm = (s) => `${Math.floor(s / 3600)}h ${Math.floor((s % 3600) / 60)}m`;

// Three small goals a day. Collapsed to the next goal so Home stays short; the chest is the reward for all three.
export default function DailyQuests() {
  const { refreshStats } = useAuth();
  const [d, setD] = useState(null);
  const [msg, setMsg] = useState("");
  const [busy, setBusy] = useState(false);
  const [open, setOpen] = useState(false);

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
      window.dispatchEvent(new Event("fl-quests-changed"));
    } catch (e) { setMsg(formatApiError(e)); setTimeout(() => setMsg(""), 3000); }
    setBusy(false);
  };

  if (!d) return null;
  const n = d.done_count;
  const allDone = d.claimed_count === 3 && d.chest.opened;
  // Collapsed view shows the quest that needs attention: something to claim first, then the first one still open.
  const lead = d.quests.find((q) => q.done && !q.claimed) || d.quests.find((q) => !q.done) || d.quests[0];
  const shown = open ? d.quests : [lead];

  return (
    <section id="quests" className="mb-6 scroll-mt-20" data-testid="daily-quests">
      <div className="bg-white border border-zinc-200 rounded-3xl overflow-hidden">
        <div className="p-4 pb-3 flex items-center gap-3">
          <span className="w-11 h-11 rounded-2xl grid place-items-center bg-gradient-to-br from-[#6366F1] to-[#8B5CF6] text-white shrink-0"><Target className="w-5 h-5" /></span>
          <div className="flex-1 min-w-0">
            <p className="uppercase tracking-[0.18em] text-[10.5px] font-bold text-zinc-500">Daily quests</p>
            <h2 className="font-[Outfit] font-black text-[19px] leading-tight" data-testid="quests-headline">
              {allDone ? "All done. See you tomorrow!" : n === 3 ? "Claim your rewards!" : `${n} of 3 done today`}
            </h2>
          </div>
          <span className="text-[12px] font-bold text-zinc-600 shrink-0">Resets in {hm(d.resets_in_seconds)}</span>
        </div>
        <div className="h-2 mx-4 mb-2 rounded-full bg-zinc-100 overflow-hidden"><div className="h-full rounded-full bg-gradient-to-r from-[#6366F1] to-[#EC4899] transition-all duration-500" style={{ width: `${Math.round((n / 3) * 100)}%` }} /></div>

        <div className="px-4">
          {shown.map((q) => {
            const m = META[q.id], pct = Math.round((q.progress / q.goal) * 100);
            return (
              <div key={q.id} className="flex items-center gap-3 py-3 border-t border-zinc-100" data-testid={`quest-${q.id}`}>
                <div className="w-11 h-11 rounded-[14px] grid place-items-center shrink-0" style={{ background: m.bg, color: m.fg }}><m.Icon className="w-5 h-5" /></div>
                <div className="flex-1 min-w-0">
                  {m.to && !q.done
                    ? <Link to={m.to} className="font-[Outfit] font-extrabold text-[15px] underline decoration-zinc-300 underline-offset-2">{q.title}</Link>
                    : <div className="font-[Outfit] font-extrabold text-[15px]">{q.title}</div>}
                  <div className="h-2 rounded-full bg-zinc-100 overflow-hidden mt-1.5"><div className="h-full rounded-full transition-all duration-500" style={{ width: `${pct}%`, background: m.fg }} /></div>
                  <div className="text-[12px] text-zinc-600 mt-1">{q.progress} / {q.goal}</div>
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
        <button onClick={() => setOpen((o) => !o)} data-testid="quests-toggle" aria-expanded={open}
          className="w-full border-t border-zinc-100 py-2.5 text-[13px] font-bold text-[#6366F1] flex items-center justify-center gap-1">
          {open ? "Show less" : "Show all 3 quests"}<ChevronDown className={`w-4 h-4 transition ${open ? "rotate-180" : ""}`} />
        </button>

        <div className="border-t border-zinc-100 p-4 flex items-center gap-3" data-testid="quest-chest">
          <div className="w-11 h-11 rounded-2xl grid place-items-center shrink-0" style={{ background: d.chest.opened ? "#ECFDF5" : "#FFF7ED", color: d.chest.opened ? "#10B981" : "#FF6B35" }}><Gift className="w-6 h-6" /></div>
          <div className="flex-1">
            <div className="font-[Outfit] font-extrabold text-[15px]">Daily chest</div>
            <div className="text-[12.5px] text-zinc-600">{d.chest.opened ? `Opened: +${d.chest.reward} coins` : `Claim all 3 quests to open it for +${d.chest.reward} coins`}</div>
          </div>
          {d.chest.ready
            ? <button onClick={() => act(() => api.post("/quests/chest"), (r) => `Chest opened: +${r.coins} coins`)} disabled={busy} data-testid="open-chest" className="rounded-xl bg-[#FF6B35] text-white font-[Outfit] font-extrabold text-[13px] px-3.5 py-2 active:scale-95">Open</button>
            : d.chest.opened ? <CheckCircle2 className="w-6 h-6 text-emerald-500" /> : <Lock className="w-5 h-5 text-zinc-500" aria-label="Locked" />}
        </div>
      </div>

      {msg && <div className="fixed bottom-24 inset-x-4 z-50 mx-auto max-w-sm bg-zinc-900 text-white text-center rounded-2xl py-3 font-bold text-sm" role="status" data-testid="quest-toast">{msg}</div>}
    </section>
  );
}
