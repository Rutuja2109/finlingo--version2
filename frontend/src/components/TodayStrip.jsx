import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Lightbulb, Target, Repeat, Flag, ArrowRight, Crown } from "lucide-react";
import { api } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import Lumi from "@/components/Lumi";

// Three bright tiles under the hero: what is waiting for the learner today (idea, quests, revision).
export default function TodayStrip() {
  const { isPro } = useAuth();
  const [d, setD] = useState({});
  useEffect(() => {
    api.get("/explainer/today").then((r) => setD((o) => ({ ...o, ex: r.data }))).catch(() => {});
    api.get("/quests/today").then((r) => setD((o) => ({ ...o, q: r.data }))).catch(() => {});
    api.get("/revisions/due").then((r) => setD((o) => ({ ...o, due: (r.data || []).length }))).catch(() => {});
    api.get("/missions/featured").then((r) => setD((o) => ({ ...o, m: r.data }))).catch(() => {});
  }, []);
  if (!d.ex && !d.q && d.due === undefined && !d.m) return null;

  const claimable = d.q ? d.q.quests.filter((x) => x.done && !x.claimed).length + (d.q.chest?.ready ? 1 : 0) : 0;
  const goQuests = (e) => {
    e.preventDefault();
    document.getElementById("quests")?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const Tile = ({ to, onClick, grad, Icon, title, sub, badge, testid }) => (
    <Link to={to} onClick={onClick} data-testid={testid}
      className={`relative rounded-2xl p-3 text-white bg-gradient-to-br ${grad} min-h-[112px] flex flex-col justify-between shadow-sm active:scale-[0.97] transition`}>
      {badge && <span className="absolute -top-2 right-2 rounded-full bg-white text-[#E5484D] text-[10px] font-black px-2 py-0.5 shadow" data-testid={`${testid}-badge`}>{badge}</span>}
      <Icon className="w-6 h-6" />
      <div>
        <div className="font-[Outfit] font-black text-[14px] leading-tight">{title}</div>
        <div className="text-[11px] text-white/90 leading-snug mt-0.5">{sub}</div>
      </div>
    </Link>
  );

  return (
    <section className="mb-6" data-testid="today-strip">
      <p className="uppercase tracking-[0.2em] text-[11px] font-bold text-zinc-600 mb-2.5 px-1">Today for you</p>
      <div className="grid grid-cols-3 gap-2.5">
        <Tile to="/explainer" testid="tile-explainer" grad="from-[#F59E0B] to-[#F97316]" Icon={Lightbulb}
          title="Idea of the day" sub={d.ex?.done ? "Done today" : "60 seconds · +XP"} badge={d.ex && !d.ex.done ? "NEW" : null} />
        <Tile to="/dashboard" onClick={goQuests} testid="tile-quests" grad="from-[#6366F1] to-[#8B5CF6]" Icon={Target}
          title="Daily quests" sub={d.q ? `${d.q.claimed_count} of 3 done` : "3 small goals"} badge={claimable > 0 ? "CLAIM!" : null} />
        <Tile to="/revise" testid="tile-revision" grad="from-[#2563EB] to-[#06B6D4]" Icon={Repeat}
          title="Revision" sub={d.due > 0 ? `${d.due} due now` : "All caught up"} badge={d.due > 0 ? `${d.due}` : null} />
      </div>
      {d.m?.mission && <MissionCard data={d.m} pro={isPro} />}
    </section>
  );
}

// This week's real-life mission: the one habit-building action, shown big so learners see it every day.
function MissionCard({ data, pro }) {
  const { mission: m, done_count: done, total } = data;
  return (
    <Link to="/missions" data-testid="home-mission"
      className="relative mt-2.5 block overflow-hidden rounded-3xl p-4 text-white bg-gradient-to-br from-[#F43F5E] via-[#FB7185] to-[#F97316] shadow-[0_12px_30px_-12px_rgba(244,63,94,0.6)] active:scale-[0.98] transition">
      <div className="absolute -right-3 -bottom-4 opacity-90 pointer-events-none"><Lumi size={92} mood="cheer" /></div>
      <div className="relative max-w-[74%]">
        <div className="flex items-center gap-1.5 text-[11px] font-black tracking-[0.18em] uppercase text-white/95">
          <Flag className="w-3.5 h-3.5" /> Mission of the week
          {!pro && <span className="ml-1 inline-flex items-center gap-0.5 rounded-full bg-zinc-900/80 px-1.5 py-0.5 text-[9px] tracking-normal"><Crown className="w-2.5 h-2.5" />PRO</span>}
        </div>
        <h3 className="font-[Outfit] font-black text-[19px] leading-tight mt-1.5" data-testid="home-mission-title">{m.title}</h3>
        <p className="text-[12.5px] text-white/90 leading-snug mt-1">{m.why}</p>
        <div className="flex items-center gap-2 mt-3">
          <span className="inline-flex items-center gap-1.5 rounded-xl bg-white text-[#E11D48] font-[Outfit] font-extrabold text-[13px] px-3 py-2">
            Start mission <ArrowRight className="w-4 h-4" />
          </span>
          <span className="text-[12px] font-bold text-white/95">+{m.xp} XP · +{m.coins} coins</span>
        </div>
        <div className="mt-3">
          <div className="flex justify-between text-[11px] font-bold text-white/90 mb-1"><span>Real-life progress</span><span>{done} of {total} done</span></div>
          <div className="h-1.5 rounded-full bg-white/30 overflow-hidden"><div className="h-full bg-white rounded-full" style={{ width: `${Math.max(4, Math.round((done / total) * 100))}%` }} /></div>
        </div>
      </div>
    </Link>
  );
}
