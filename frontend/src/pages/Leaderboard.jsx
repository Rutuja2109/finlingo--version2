import React, { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Trophy, Flame, Zap } from "lucide-react";

export default function Leaderboard() {
  const [rows, setRows] = useState([]);
  useEffect(() => { api.get("/leaderboard").then(({ data }) => setRows(data)); }, []);

  return (
    <div className="pb-24">
      <div className="mb-7">
        <p className="uppercase tracking-[0.25em] text-xs font-bold text-zinc-400">Real-time</p>
        <h1 className="font-[Outfit] font-black text-3xl md:text-4xl tracking-tighter">Leaderboard</h1>
        <p className="text-zinc-500 mt-1">Top FinLingo learners by XP — no fake data, ever.</p>
      </div>

      {rows.length === 0 && (
        <div className="bg-white border border-zinc-200 rounded-3xl p-10 text-center text-zinc-500">
          Be the first on the board — complete a lesson to appear here.
        </div>
      )}

      <div className="bg-white border border-zinc-200 rounded-3xl overflow-hidden">
        {rows.map((r) => (
          <div key={r.user_id} data-testid={`lb-row-${r.rank}`}
            className={`flex items-center gap-4 px-5 py-4 border-b border-zinc-100 last:border-0 ${r.is_me ? "bg-[#FF6B35]/8" : ""}`}>
            <RankBadge rank={r.rank}/>
            <div className="w-10 h-10 rounded-full grid place-items-center text-white font-[Outfit] font-black"
              style={{ background: r.avatar_color }}>
              {r.name?.[0]?.toUpperCase() || "?"}
            </div>
            <div className="flex-1">
              <p className="font-[Outfit] font-bold tracking-tight">
                {r.name} {r.is_me && <span className="ml-2 text-xs uppercase tracking-wider font-bold text-[#FF6B35]">You</span>}
              </p>
              <p className="text-xs text-zinc-500">Level {r.level}</p>
            </div>
            <div className="flex items-center gap-1 text-sm font-bold text-[#FF5C00]">
              <Flame className="w-4 h-4"/> {r.streak_days}
            </div>
            <div className="flex items-center gap-1 text-sm font-bold text-[#F59E0B] tabular-nums w-20 justify-end">
              <Zap className="w-4 h-4"/> {r.total_xp}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function RankBadge({ rank }) {
  const styles = {
    1: "bg-gradient-to-br from-[#FBBF24] to-[#F59E0B] text-white",
    2: "bg-gradient-to-br from-zinc-300 to-zinc-400 text-white",
    3: "bg-gradient-to-br from-[#FB923C] to-[#C2410C] text-white",
  };
  const cls = styles[rank] || "bg-zinc-100 text-zinc-600";
  return (
    <div className={`w-9 h-9 rounded-full grid place-items-center font-[Outfit] font-black text-sm ${cls}`}>
      {rank <= 3 ? <Trophy className="w-4 h-4"/> : rank}
    </div>
  );
}
