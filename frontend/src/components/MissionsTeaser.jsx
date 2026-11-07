import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Flag, ArrowRight } from "lucide-react";
import { api } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";

// Small dashboard card that points to the real-life missions page.
export default function MissionsTeaser() {
  const [d, setD] = useState(null);
  const { isPro } = useAuth();
  useEffect(() => { if (isPro) api.get("/missions").then((r) => setD(r.data)).catch(() => {}); }, [isPro]);
  if (!d) return null;
  const f = d.missions.find((m) => m.featured);
  return (
    <Link to="/missions" data-testid="missions-teaser" className="flex items-center gap-3 bg-rose-50 border-2 border-rose-300 rounded-3xl p-4 mb-10">
      <span className="w-11 h-11 rounded-2xl grid place-items-center bg-rose-500 text-white shrink-0"><Flag className="w-5 h-5" /></span>
      <span className="flex-1 min-w-0">
        <span className="block text-[11px] font-bold tracking-[.2em] uppercase text-zinc-500">Real-life missions · {d.done_count} of {d.total} done</span>
        <span className="block font-[Outfit] font-extrabold text-[15px] truncate">{f ? `This week: ${f.title}` : "All missions done!"}</span>
      </span>
      <ArrowRight className="w-5 h-5 text-zinc-400 shrink-0" />
    </Link>
  );
}
