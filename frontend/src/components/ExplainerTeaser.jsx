import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Newspaper, Lightbulb, ArrowRight, CheckCircle2 } from "lucide-react";
import { api } from "@/lib/api";

// Dashboard card for today's 60-second explainer.
export default function ExplainerTeaser() {
  const [e, setE] = useState(null);
  useEffect(() => { api.get("/explainer/today").then((r) => setE(r.data)).catch(() => {}); }, []);
  if (!e) return null;
  const Icon = e.kind === "news" ? Newspaper : Lightbulb;
  return (
    <Link to="/explainer" data-testid="explainer-teaser" className="flex items-center gap-3 bg-white border border-zinc-200 rounded-3xl p-4 mb-4">
      <span className="w-11 h-11 rounded-2xl grid place-items-center bg-amber-50 text-amber-600 shrink-0"><Icon className="w-5 h-5" /></span>
      <span className="flex-1 min-w-0">
        <span className="block text-[11px] font-bold tracking-[.2em] uppercase text-zinc-500">{e.kind === "news" ? "In the news" : "Idea of the day"} · 60 seconds</span>
        <span className="block font-[Outfit] font-extrabold text-[15px] leading-snug line-clamp-2">{e.headline}</span>
      </span>
      {e.done ? <CheckCircle2 className="w-5 h-5 text-emerald-500 shrink-0" aria-label="Read" /> : <ArrowRight className="w-5 h-5 text-zinc-400 shrink-0" />}
    </Link>
  );
}
