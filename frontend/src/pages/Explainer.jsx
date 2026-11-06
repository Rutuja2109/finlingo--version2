import React, { useCallback, useEffect, useState } from "react";
import { ExternalLink, Newspaper, Lightbulb, BookMarked } from "lucide-react";
import { api, formatApiError } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import Lumi from "@/components/Lumi";

export default function Explainer() {
  const { refreshStats } = useAuth();
  const [e, setE] = useState(null);
  const [res, setRes] = useState(null); // {correct, correct_index, chosen, explanation, xp}
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");

  const load = useCallback(async () => {
    try {
      const { data } = await api.get("/explainer/today");
      setE(data); setErr("");
      if (data.done && data.result) setRes(data.result);
    } catch (x) { setErr(formatApiError(x)); }
  }, []);
  useEffect(() => { load(); }, [load]);

  const answer = async (i) => {
    if (busy || res) return;
    setBusy(true);
    try {
      const { data } = await api.post("/explainer/read", { answer: i });
      setRes({ ...data, chosen: i });
      refreshStats?.();
    } catch (x) { setErr(formatApiError(x)); }
    setBusy(false);
  };

  if (!e) return <div className="py-20 text-center text-zinc-500">{err || "Loading today's explainer…"}</div>;
  const news = e.kind === "news";
  return (
    <div className="max-w-md mx-auto pb-24" data-testid="explainer-page">
      <div className="flex items-center gap-2 mb-2">
        <span className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-[11px] font-extrabold tracking-wide uppercase ${news ? "bg-red-50 text-red-600" : "bg-amber-50 text-amber-700"}`}>
          {news ? <Newspaper className="w-3.5 h-3.5" /> : <Lightbulb className="w-3.5 h-3.5" />}{news ? "In the news" : "Idea of the day"}
        </span>
        <span className="text-[12px] text-zinc-400">60 seconds</span>
      </div>
      <h1 className="font-[Outfit] font-black text-2xl tracking-tight leading-tight" data-testid="explainer-headline">{e.headline}</h1>

      <div className="bg-white border border-zinc-200 rounded-3xl p-4 mt-4">
        <p className="text-[11px] font-bold tracking-[.2em] uppercase text-zinc-500 mb-1.5">In plain words</p>
        <p className="text-[15px] leading-relaxed">{e.summary}</p>
        {e.points.length > 0 && <ul className="mt-3 space-y-2 text-[14px] leading-relaxed list-disc pl-5 text-zinc-700">{e.points.map((p, i) => <li key={i}>{p}</li>)}</ul>}
      </div>

      <div className="rounded-3xl p-4 mt-3 text-white bg-gradient-to-br from-[#FF6B35] to-[#EC4899]">
        <p className="text-[11px] font-bold tracking-[.2em] uppercase text-white/90 mb-1">Why it matters to you</p>
        <p className="text-[14.5px] leading-relaxed">{e.why}</p>
      </div>

      <div className="bg-white border border-zinc-200 rounded-2xl p-3.5 mt-3 flex gap-3">
        <BookMarked className="w-5 h-5 text-[#7C3AED] shrink-0 mt-0.5" />
        <div className="text-[13.5px]"><b className="font-[Outfit]">{e.term.word}</b><br /><span className="text-zinc-600">{e.term.meaning}</span></div>
      </div>

      <div className="bg-white border border-zinc-200 rounded-3xl p-4 mt-3" data-testid="explainer-quiz">
        <p className="text-[11px] font-bold tracking-[.2em] uppercase text-zinc-500 mb-1.5">Quick check</p>
        <p className="font-[Outfit] font-extrabold text-[16px] mb-3">{e.quiz.question}</p>
        {e.quiz.options.map((o, i) => {
          const state = !res ? "" : i === res.correct_index ? "ok" : i === res.chosen ? "no" : "";
          return (
            <button key={i} onClick={() => answer(i)} disabled={!!res || busy} data-testid={`explainer-opt-${i}`}
              className={`block w-full text-left border-2 rounded-xl px-3 py-2.5 mb-2 text-[14px] font-semibold ${state === "ok" ? "border-emerald-500 bg-emerald-50" : state === "no" ? "border-red-500 bg-red-50" : "border-zinc-200 bg-white"}`}>{o}</button>
          );
        })}
        {res && (
          <div className="flex gap-3 items-start mt-2" data-testid="explainer-result">
            <Lumi size={48} mood={res.correct ? "cheer" : "nervous"} className="shrink-0" />
            <div className="text-[13.5px] leading-relaxed"><b className="font-[Outfit]">{res.correct ? "Right!" : "Not quite."}</b> {res.explanation}
              {res.xp ? <div className="text-[12.5px] font-bold text-emerald-700 mt-1">+{res.xp} XP earned today</div> : null}</div>
          </div>
        )}
        {err && <p className="text-red-700 text-[13px] mt-2">{err}</p>}
      </div>

      {news && e.source_url && (
        <a href={e.source_url} target="_blank" rel="noopener noreferrer" className="flex items-center gap-1.5 text-[13px] font-bold text-zinc-500 mt-3 justify-center" data-testid="explainer-source">
          Source: {e.source_name} <ExternalLink className="w-3.5 h-3.5" />
        </a>
      )}
      <p className="text-[11.5px] text-zinc-400 text-center mt-3">Education only, not investment, tax or legal advice. Come back tomorrow for a new one.</p>
    </div>
  );
}
