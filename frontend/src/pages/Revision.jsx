import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import Lumi from "@/components/Lumi";
import { Repeat, Sparkles } from "lucide-react";

const QUALITY = [
  { v: 0, label: "Again",  color: "#EF4444", note: "Didn't recall" },
  { v: 1, label: "Hard",   color: "#F59E0B", note: "Struggled" },
  { v: 2, label: "Good",   color: "#10B981", note: "Recalled" },
  { v: 3, label: "Easy",   color: "#2563EB", note: "Effortless" },
];

export default function Revision() {
  const { refreshStats } = useAuth();
  const [items, setItems] = useState([]);
  const [idx, setIdx] = useState(0);
  const [reveal, setReveal] = useState(false);
  const [done, setDone] = useState(false);
  const [earned, setEarned] = useState(0);

  useEffect(() => { api.get("/revisions/due").then(({ data }) => setItems(data)); }, []);

  const current = items[idx];

  const grade = async (quality) => {
    await api.post("/revisions/grade", { concept_id: current.concept.id, quality });
    setEarned((e) => e + [0,2,5,8][quality]);
    setReveal(false);
    if (idx + 1 < items.length) {
      setIdx(idx + 1);
    } else {
      setDone(true);
      refreshStats();
    }
  };

  if (items.length === 0) {
    return (
      <div className="pb-24 max-w-2xl" data-testid="revision-empty">
        <Header/>
        <div className="bg-white border border-zinc-200 rounded-3xl p-10 text-center">
          <Lumi size={120} mood="happy" className="mx-auto mb-3"/>
          <h2 className="font-[Outfit] font-black text-2xl">Nothing due yet</h2>
          <p className="text-zinc-500 mt-1">Complete more concepts and check back tomorrow. Spaced repetition keeps knowledge sharp.</p>
          <Link to="/dashboard" className="inline-block mt-5 px-5 py-2.5 rounded-xl bg-zinc-900 text-white font-bold">Back to dashboard</Link>
        </div>
      </div>
    );
  }

  if (done) {
    return (
      <div className="pb-24 max-w-2xl text-center">
        <div className="mt-8 mb-4 flex justify-center"><Lumi size={160} mood="cheer"/></div>
        <h1 className="font-[Outfit] font-black text-4xl tracking-tighter mb-2">Daily revision complete</h1>
        <p className="text-zinc-500 mb-6">{items.length} concept{items.length>1?"s":""} reviewed · +{earned} XP</p>
        <Link to="/dashboard" data-testid="revision-done" className="inline-flex items-center gap-2 px-6 py-3 rounded-2xl bg-[#FF6B35] text-white font-[Outfit] font-bold">
          <Sparkles className="w-4 h-4"/> Done
        </Link>
      </div>
    );
  }

  return (
    <div className="pb-24 max-w-2xl">
      <Header/>
      <p className="text-xs text-zinc-500 mb-2">{idx + 1} / {items.length} · {current.concept.title}</p>
      <div className="h-2 rounded-full bg-zinc-100 overflow-hidden mb-6">
        <div className="h-full bg-gradient-to-r from-[#FF6B35] to-[#EC4899] transition-all"
          style={{ width: `${((idx+1)/items.length)*100}%`}}/>
      </div>

      <div data-testid="revision-card" className="bg-white border border-zinc-200 rounded-3xl p-7 md:p-9">
        <p className="text-xs uppercase tracking-[0.25em] font-bold text-[#2563EB] mb-2">Recall prompt</p>
        <h2 className="font-[Outfit] font-black text-2xl tracking-tight mb-2">{current.concept.title}</h2>
        <p className="text-zinc-700">{current.concept.learning_objective}</p>

        {!reveal ? (
          <button onClick={() => setReveal(true)} data-testid="btn-reveal"
            className="mt-6 px-5 py-3 rounded-2xl bg-zinc-900 text-white font-bold">
            Reveal answer
          </button>
        ) : (
          <div className="mt-6 p-5 bg-zinc-50 rounded-2xl">
            <p className="text-zinc-800 leading-relaxed">{current.concept.simple_explanation}</p>
            {current.concept.key_takeaways?.length > 0 && (
              <ul className="mt-3 space-y-1">
                {current.concept.key_takeaways.map((k, i) => (
                  <li key={i} className="text-sm text-zinc-600">• {k}</li>
                ))}
              </ul>
            )}
          </div>
        )}

        {reveal && (
          <div className="mt-6">
            <p className="text-xs uppercase tracking-[0.2em] font-bold text-zinc-500 mb-2">How well did you recall?</p>
            <div className="grid grid-cols-4 gap-2">
              {QUALITY.map((q) => (
                <button key={q.v} onClick={() => grade(q.v)} data-testid={`grade-${q.label.toLowerCase()}`}
                  className="rounded-2xl py-3 text-white font-[Outfit] font-bold text-sm transition active:scale-95"
                  style={{ background: q.color }}>
                  <div>{q.label}</div>
                  <div className="text-[10px] font-normal opacity-90">{q.note}</div>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function Header() {
  return (
    <div className="mb-6">
      <p className="uppercase tracking-[0.25em] text-xs font-bold text-zinc-400">Daily Revision</p>
      <h1 className="font-[Outfit] font-black text-3xl md:text-4xl tracking-tighter flex items-center gap-2">
        <Repeat className="w-7 h-7 text-[#FF6B35]"/> Reinforce
      </h1>
    </div>
  );
}
