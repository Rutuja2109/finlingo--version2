import React, { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { api } from "@/lib/api";
import { Lock, Check, Sparkles, ChevronLeft, Skull } from "lucide-react";
import Lumi from "@/components/Lumi";

export default function CoursePath() {
  const { courseId } = useParams();
  const nav = useNavigate();
  const [course, setCourse] = useState(null);

  useEffect(() => {
    api.get(`/courses/${courseId}/full`).then(({ data }) => setCourse(data));
  }, [courseId]);

  if (!course) return <div className="text-center py-20 text-zinc-500">Loading…</div>;

  return (
    <div className="pb-24">
      <Link to="/dashboard" data-testid="back-dashboard" className="inline-flex items-center gap-1 text-sm text-zinc-500 hover:text-zinc-900 mb-4">
        <ChevronLeft className="w-4 h-4"/> Dashboard
      </Link>

      <div className="rounded-3xl p-7 md:p-10 mb-8 text-white relative overflow-hidden"
        style={{ background: `linear-gradient(135deg, ${course.color}, #1B1B1F)` }}>
        <div className="relative">
          <p className="uppercase tracking-[0.25em] text-xs font-bold text-white/80">{course.certification}</p>
          <h1 className="font-[Outfit] font-black text-3xl md:text-5xl tracking-tighter">{course.name}</h1>
          <p className="text-white/85 mt-1">{course.title}</p>
        </div>
      </div>

      {course.chapters.map((ch, ci) => {
        const allConcepts = ch.modules.flatMap((m) => m.concepts);
        const doneCount = allConcepts.filter((c) => ["completed","mastered"].includes(c.progress?.status)).length;
        const bossReady = doneCount === allConcepts.length && allConcepts.length > 0;
        return (
        <section key={ch.id} className="mb-10" data-testid={`chapter-${ci+1}`}>
          <div className="flex items-baseline justify-between mb-3">
            <div>
              <p className="uppercase tracking-[0.25em] text-[11px] font-bold text-zinc-400">Chapter {ci+1}</p>
              <h2 className="font-[Outfit] font-black text-2xl tracking-tight">{ch.title}</h2>
            </div>
            <span className="text-xs font-bold text-zinc-500">{doneCount}/{allConcepts.length} done</span>
          </div>
          <p className="text-zinc-500 mb-6 max-w-2xl">{ch.description}</p>

          {ch.modules.map((m) => (
            <div key={m.id} className="mb-8">
              <h3 className="font-[Outfit] font-bold text-lg mb-4 text-zinc-700">{m.title}</h3>
              <div className="relative">
                {/* winding nodes */}
                <ul className="flex flex-col gap-5">
                  {m.concepts.map((concept, idx) => (
                    <li key={concept.id} className="flex" style={{ paddingLeft: `${(idx % 3) * 56}px` }}>
                      <ConceptNode concept={concept} color={course.color}
                        onClick={() => nav(`/concept/${concept.id}`)}
                        index={idx + 1}/>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}

          {/* Boss Battle CTA */}
          <button
            data-testid={`boss-cta-${ch.id}`}
            disabled={!bossReady}
            onClick={() => nav(`/boss/${ch.id}`)}
            className={`mt-2 w-full md:w-auto flex items-center gap-4 px-6 py-5 rounded-3xl text-left transition group ${
              bossReady
                ? "bg-gradient-to-r from-zinc-950 via-zinc-900 to-[#1a0a2e] text-white hover:scale-[1.01] hover:shadow-2xl"
                : "bg-zinc-100 text-zinc-400 cursor-not-allowed"
            }`}>
            <div className={`w-14 h-14 rounded-2xl grid place-items-center ${bossReady ? "bg-[#EC4899]/30 text-[#EC4899]" : "bg-zinc-200 text-zinc-400"}`}>
              {bossReady ? <Skull className="w-7 h-7"/> : <Lock className="w-6 h-6"/>}
            </div>
            <div className="flex-1">
              <p className="text-[10px] uppercase tracking-[0.3em] font-bold" style={{ color: bossReady ? "#EC4899" : "" }}>Boss Battle</p>
              <p className="font-[Outfit] font-black text-lg">{bossReady ? "Challenge the boss" : "Master all concepts to unlock"}</p>
              <p className="text-xs opacity-80">{bossReady ? "+50 XP · Mixed quiz from this chapter" : `${doneCount}/${allConcepts.length} concepts complete`}</p>
            </div>
          </button>
        </section>
        );
      })}
    </div>
  );
}

function ConceptNode({ concept, color, onClick, index }) {
  const status = concept.progress?.status || "locked";
  const isLocked = status === "locked";
  const isDone = status === "completed" || status === "mastered";
  const isMastered = status === "mastered";

  return (
    <button
      data-testid={`concept-node-${concept.id}`}
      disabled={isLocked}
      onClick={onClick}
      className="group flex items-center gap-4 text-left disabled:cursor-not-allowed"
    >
      <div
        className={`relative w-20 h-20 rounded-3xl grid place-items-center shadow-lg transition-all duration-300
          ${isLocked ? "bg-zinc-200" : ""}
          ${isDone ? "" : ""}
          ${!isLocked ? "group-hover:scale-105 group-hover:-translate-y-1" : ""}`}
        style={{
          background: isLocked ? "#E4E4E7" : isDone ? "#10B981" : color,
          boxShadow: isLocked
            ? "0 8px 16px -10px rgba(0,0,0,0.2)"
            : `0 18px 30px -12px ${isDone ? "#10B981" : color}80`,
        }}
      >
        {isLocked && <Lock className="w-7 h-7 text-zinc-500"/>}
        {isDone && <Check className="w-9 h-9 text-white"/>}
        {!isLocked && !isDone && (
          <Lumi size={56} mood="happy" />
        )}
        {isMastered && (
          <span className="absolute -top-2 -right-2 text-[10px] uppercase tracking-wider font-bold bg-[#FBBF24] text-zinc-900 px-1.5 py-0.5 rounded-full">
            Mastered
          </span>
        )}
      </div>
      <div>
        <p className="text-xs uppercase tracking-[0.2em] text-zinc-400 font-bold">Concept {index}</p>
        <p className="font-[Outfit] font-bold text-lg tracking-tight">{concept.title}</p>
        <p className="text-sm text-zinc-500 line-clamp-1">{concept.learning_objective}</p>
        {!isLocked && (
          <span className="inline-flex items-center gap-1 mt-1 text-xs font-bold text-[#FF6B35]">
            <Sparkles className="w-3 h-3"/> +{concept.xp_reward} XP
          </span>
        )}
      </div>
    </button>
  );
}
