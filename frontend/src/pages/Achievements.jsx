import React from "react";
import { useAuth } from "@/context/AuthContext";
import { Footprints, Flame, GraduationCap, Trophy, Star, Lock } from "lucide-react";

const ALL = [
  { code: "first_step", title: "First Step", desc: "Complete your first concept", icon: Footprints, color: "#10B981" },
  { code: "streak_3", title: "3-Day Streak", desc: "Practice 3 days in a row", icon: Flame, color: "#FF5C00" },
  { code: "streak_7", title: "Week Warrior", desc: "7-day streak", icon: Flame, color: "#EF4444" },
  { code: "level_5", title: "Rising Scholar", desc: "Reach level 5", icon: GraduationCap, color: "#2563EB" },
  { code: "master_5", title: "Mastery x5", desc: "Master 5 concepts", icon: Trophy, color: "#FBBF24" },
  { code: "perfect", title: "Perfect Score", desc: "Score 100% on a concept", icon: Star, color: "#EC4899" },
];

export default function Achievements() {
  const { stats } = useAuth();
  const earned = new Set(stats?.achievements || []);

  return (
    <div className="pb-24">
      <div className="mb-7">
        <p className="uppercase tracking-[0.25em] text-xs font-bold text-zinc-400">Your trophies</p>
        <h1 className="font-[Outfit] font-black text-3xl md:text-4xl tracking-tighter">Achievements</h1>
        <p className="text-zinc-500 mt-1">{earned.size} of {ALL.length} unlocked.</p>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {ALL.map((a) => {
          const got = earned.has(a.code);
          const Ic = got ? a.icon : Lock;
          return (
            <div key={a.code} data-testid={`achv-${a.code}`}
              className={`relative rounded-3xl p-6 border-2 transition ${got ? "bg-white border-zinc-200" : "bg-zinc-50 border-dashed border-zinc-200 opacity-70"}`}>
              <div className="w-14 h-14 rounded-2xl grid place-items-center mb-3"
                style={{ background: got ? `${a.color}1A` : "#E4E4E7" }}>
                <Ic className="w-7 h-7" style={{ color: got ? a.color : "#71717A" }}/>
              </div>
              <h3 className="font-[Outfit] font-black text-lg tracking-tight">{a.title}</h3>
              <p className="text-sm text-zinc-500">{a.desc}</p>
              {got && (
                <span className="absolute top-4 right-4 text-[10px] uppercase tracking-wider font-bold px-2 py-1 rounded-full text-white"
                  style={{ background: a.color }}>Unlocked</span>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
