import React, { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { CheckCircle2, ChevronDown, ChevronUp, Flag, ArrowRight } from "lucide-react";
import { api, formatApiError } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import Lumi from "@/components/Lumi";
import { useTranslation } from "react-i18next";

const THEME_COLOR = { spend: "#EC4899", save: "#10B981", protect: "#7C3AED", invest: "#2563EB", tax: "#F59E0B" };

export default function Missions() {
  const { t: tx } = useTranslation();
  const { refreshStats } = useAuth();
  const [data, setData] = useState(null);
  const [open, setOpen] = useState(null);
  const [notes, setNotes] = useState({});
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");

  const load = useCallback(async () => {
    try { setData((await api.get("/missions")).data); setErr(""); } catch (e) { setErr(formatApiError(e)); }
  }, []);
  useEffect(() => { load(); }, [load]);

  const complete = async (m) => {
    if (busy) return;
    setBusy(true); setMsg("");
    try {
      const { data: r } = await api.post(`/missions/${m.id}/complete`, { note: notes[m.id] || "" });
      setMsg(`Mission done! +${r.xp} XP and +${r.coins} coins`);
      setOpen(null);
      await Promise.all([load(), refreshStats?.()]);
      setTimeout(() => setMsg(""), 3500);
    } catch (e) { setMsg(formatApiError(e)); setTimeout(() => setMsg(""), 4000); }
    setBusy(false);
  };

  if (!data) return <div className="py-20 text-center text-zinc-500">{err || tx("missions.loading_missions")}</div>;
  const featured = data.missions.find((m) => m.featured);
  const allDone = data.done_count === data.total;
  const themes = Object.keys(data.themes);

  const Card = ({ m }) => {
  const { t: tx } = useTranslation();
    const isOpen = open === m.id, color = THEME_COLOR[m.theme];
    return (
      <div className={`bg-white border rounded-2xl mb-2.5 ${m.done ? "border-emerald-200" : "border-zinc-200"}`} data-testid={`mission-${m.id}`}>
        <button onClick={() => setOpen(isOpen ? null : m.id)} className="w-full flex items-center gap-3 px-3.5 py-3 text-left">
          <span className="w-9 h-9 rounded-xl grid place-items-center shrink-0" style={{ background: `${color}1A`, color }}>
            {m.done ? <CheckCircle2 className="w-5 h-5 text-emerald-500" /> : <Flag className="w-5 h-5" />}
          </span>
          <span className="flex-1 min-w-0">
            <span className={`block font-[Outfit] font-extrabold text-[15px] ${m.done ? "text-zinc-400 line-through" : ""}`}>{m.title}</span>
            <span className="block text-[12px] text-zinc-500">{m.done ? tx("missions.done") : `+${m.xp} XP · +${m.coins} coins`}{m.kind === "auto" && !m.done ? ` · ${tx("missions.checks_itself").trim().replace(/^·\s*/, "")}` : ""}</span>
          </span>
          {isOpen ? <ChevronUp className="w-5 h-5 text-zinc-400" /> : <ChevronDown className="w-5 h-5 text-zinc-400" />}
        </button>
        {isOpen && (
          <div className="px-3.5 pb-3.5 -mt-1">
            <p className="text-[13px] text-zinc-600 mb-2">{m.why}</p>
            <ol className="text-[13px] text-zinc-700 list-decimal pl-5 space-y-1 mb-3">{m.steps.map((s, i) => <li key={i}>{s}</li>)}</ol>
            {m.link && !m.done && <Link to={m.link} className="inline-flex items-center gap-1 text-[13px] font-extrabold text-[#FF6B35] mb-3">{tx("missions.go_there")} <ArrowRight className="w-4 h-4" /></Link>}
            {m.done ? (m.note && <p className="text-[13px] bg-zinc-50 rounded-xl px-3 py-2">{tx("missions.your_note_note", { note: m.note })}</p>) : (
              <>
                {m.kind === "self" && (
                  <textarea value={notes[m.id] || ""} onChange={(e) => setNotes({ ...notes, [m.id]: e.target.value })} maxLength={140} rows={2} data-testid={`note-${m.id}`}
                    placeholder={`${m.note_prompt || "Anything to remember?"} (optional)`} className="w-full border-2 border-zinc-200 rounded-xl px-3 py-2 text-[13px] mb-2 outline-none focus:border-[#FF6B35]" />
                )}
                <button onClick={() => complete(m)} disabled={busy} data-testid={`done-${m.id}`}
                  className="w-full rounded-2xl py-3 bg-[#FF6B35] text-white font-[Outfit] font-black text-[15px] disabled:opacity-60">{m.kind === "auto" ? "Check my progress" : "I did it"}</button>
                {m.kind === "self" && <p className="text-[11.5px] text-zinc-400 mt-1.5 text-center">{tx("missions.on_the_honour_system_only_tick")}</p>}
              </>
            )}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="max-w-md mx-auto pb-24" data-testid="missions-page">
      <h1 className="font-[Outfit] font-black text-2xl tracking-tight">{tx("missions.real_life_missions")}</h1>
      <p className="text-[13px] text-zinc-500 mt-1 mb-3">{tx("missions.small_actions_in_your_own_money")}</p>
      <div className="bg-white border border-zinc-200 rounded-2xl p-3.5 mb-3">
        <div className="flex justify-between text-[13px] font-bold mb-1.5"><span>{tx("missions.your_progress")}</span><span data-testid="missions-count">{tx("missions.done_count_of_total_done", { done_count: data.done_count, total: data.total })}</span></div>
        <div className="h-2.5 rounded-full bg-zinc-100 overflow-hidden"><div className="h-full bg-emerald-500 transition-all" style={{ width: `${Math.round((data.done_count / data.total) * 100)}%` }} /></div>
      </div>

      {featured && (
        <div className="rounded-3xl text-white p-4 bg-gradient-to-br from-[#FF6B35] via-[#FF8A4C] to-[#EC4899] mb-4 relative overflow-hidden" data-testid="mission-featured">
          <div className="absolute -right-1 -top-1 opacity-40 pointer-events-none"><Lumi size={84} mood="cheer" /></div>
          <p className="uppercase tracking-[0.2em] text-[11px] font-bold text-white/90 relative">{tx("missions.mission_of_the_week")}</p>
          <h2 className="font-[Outfit] font-black text-xl mt-1 max-w-[72%] relative">{featured.title}</h2>
          <button onClick={() => setOpen(featured.id)} className="mt-3 bg-white text-[#FF6B35] font-[Outfit] font-extrabold text-sm rounded-xl px-4 py-2 relative">{tx("missions.see_the_steps")}</button>
        </div>
      )}
      {allDone && <div className="rounded-2xl bg-emerald-50 border border-emerald-200 p-3.5 text-[13px] mb-4 flex gap-3"><Lumi size={44} mood="cheer" /><div><b className="font-[Outfit]">{tx("missions.all_missions_done")}</b><br />{tx("missions.you_have_done_more_with_your")}</div></div>}

      {themes.map((t) => (
        <section key={t} className="mb-4">
          <p className="text-[11px] font-bold tracking-[.2em] uppercase text-zinc-500 mb-2 px-1">{data.themes[t]}</p>
          {data.missions.filter((m) => m.theme === t).map((m) => <Card key={m.id} m={m} />)}
        </section>
      ))}
      <p className="text-[11.5px] text-zinc-400 text-center">{tx("missions.finlearn_never_asks_you_to_buy")}</p>

      {msg && <div className="fixed bottom-24 inset-x-4 z-50 mx-auto max-w-sm bg-zinc-900 text-white text-center rounded-2xl py-3 font-bold text-sm" role="status" data-testid="mission-toast">{msg}</div>}
    </div>
  );
}
