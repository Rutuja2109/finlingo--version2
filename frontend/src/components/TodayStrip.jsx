import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Lightbulb, Target, Repeat } from "lucide-react";
import { api } from "@/lib/api";

// Three bright tiles under the hero: what is waiting for the learner today (idea, quests, revision).
export default function TodayStrip() {
  const [d, setD] = useState({});
  useEffect(() => {
    api.get("/explainer/today").then((r) => setD((o) => ({ ...o, ex: r.data }))).catch(() => {});
    api.get("/quests/today").then((r) => setD((o) => ({ ...o, q: r.data }))).catch(() => {});
    api.get("/revisions/due").then((r) => setD((o) => ({ ...o, due: (r.data || []).length }))).catch(() => {});
  }, []);
  if (!d.ex && !d.q && d.due === undefined) return null;

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
    </section>
  );
}
