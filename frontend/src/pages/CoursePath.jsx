import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "@/lib/api";
import { Lock, Check, Sparkles, ChevronLeft, Skull, Star, BookOpen, Zap } from "lucide-react";
import Lumi from "@/components/Lumi";

export default function CoursePath() {
  const { courseId } = useParams();
  const nav = useNavigate();
  const [course, setCourse] = useState(null);

  useEffect(() => {
    api.get(`/courses/${courseId}/full`).then(({ data }) => setCourse(data));
  }, [courseId]);

  if (!course) return (
    <div className="flex flex-col items-center justify-center py-20 gap-3">
      <Lumi size={80} mood="happy" className="lumi-float" />
      <p className="text-zinc-400 font-semibold">Loading your path…</p>
    </div>
  );

  // Flatten all nodes across chapters for the winding path
  const allNodes = [];
  course.chapters.forEach((ch, ci) => {
    // Chapter banner node
    allNodes.push({ type: "chapter_banner", ch, ci });
    const allConcepts = ch.modules.flatMap((m) => m.concepts);
    allConcepts.forEach((concept, idx) => {
      allNodes.push({ type: "concept", concept, ch, ci, idx });
    });
    // Boss battle node
    const doneCount = allConcepts.filter((c) => ["completed", "mastered"].includes(c.progress?.status)).length;
    const bossReady = doneCount === allConcepts.length && allConcepts.length > 0;
    allNodes.push({ type: "boss", ch, ci, bossReady, total: allConcepts.length, done: doneCount });
  });

  return (
    <div className="pb-32 max-w-lg mx-auto">
      {/* Header */}
      <button onClick={() => nav("/courses")}
        className="inline-flex items-center gap-1 text-sm text-zinc-500 hover:text-zinc-900 mb-5">
        <ChevronLeft className="w-4 h-4" /> All courses
      </button>

      <div className="rounded-3xl p-6 mb-8 text-white relative overflow-hidden"
        style={{ background: `linear-gradient(135deg, ${course.color}dd, #1B1B1F)` }}>
        <div className="absolute inset-0 opacity-10"
          style={{ backgroundImage: "radial-gradient(circle, white 1px, transparent 1px)", backgroundSize: "24px 24px" }} />
        <div className="relative">
          <p className="uppercase tracking-[0.25em] text-xs font-bold text-white/70">{course.certification}</p>
          <h1 className="font-[Outfit] font-black text-3xl tracking-tighter">{course.name}</h1>
          <p className="text-white/80 text-sm mt-1">{course.title}</p>
        </div>
      </div>

      {/* Winding path */}
      <div className="relative px-4">
        {/* Vertical dashed spine */}
        <div className="absolute left-1/2 top-0 bottom-0 w-0.5 border-l-2 border-dashed border-zinc-200 -translate-x-1/2 z-0" />

        <div className="flex flex-col gap-0">
          {allNodes.map((node, ni) => {
            if (node.type === "chapter_banner") {
              return <ChapterBanner key={`ch-${node.ci}`} ch={node.ch} ci={node.ci} color={course.color} />;
            }
            if (node.type === "boss") {
              return (
                <BossNode key={`boss-${node.ci}`} ch={node.ch} bossReady={node.bossReady}
                  done={node.done} total={node.total} onPress={() => nav(`/boss/${node.ch.id}`)} />
              );
            }
            // concept node — alternate left/right in a zigzag
            const side = node.idx % 2 === 0 ? "left" : "right";
            return (
              <ConceptNode key={node.concept.id} concept={node.concept} color={course.color}
                side={side} index={node.idx + 1}
                onClick={() => nav(`/concept/${node.concept.id}`)} />
            );
          })}
        </div>
      </div>
    </div>
  );
}

function ChapterBanner({ ch, ci, color }) {
  return (
    <div className="relative z-10 flex justify-center my-6">
      <div className="px-5 py-3 rounded-2xl text-center shadow-lg border border-white"
        style={{ background: `linear-gradient(135deg, ${color}20, ${color}08)`, borderColor: `${color}30` }}>
        <p className="text-[10px] uppercase tracking-[0.3em] font-bold text-zinc-400">Chapter {ci + 1}</p>
        <p className="font-[Outfit] font-black text-base tracking-tight text-zinc-900">{ch.title}</p>
      </div>
    </div>
  );
}

function ConceptNode({ concept, color, side, index, onClick }) {
  const status = concept.progress?.status || "locked";
  const isLocked = status === "locked";
  const isDone = status === "completed" || status === "mastered";
  const isMastered = status === "mastered";
  const isAvailable = !isLocked && !isDone;

  return (
    <div className={`relative z-10 flex items-center my-3 ${side === "right" ? "flex-row-reverse" : "flex-row"}`}>
      {/* Node bubble */}
      <button
        data-testid={`concept-node-${concept.id}`}
        disabled={isLocked}
        onClick={onClick}
        className={`relative w-[72px] h-[72px] rounded-[22px] grid place-items-center shadow-xl transition-all duration-300 shrink-0
          ${!isLocked ? "active:scale-95 hover:scale-105 hover:-translate-y-1" : "cursor-not-allowed"}
        `}
        style={{
          background: isLocked
            ? "#E4E4E7"
            : isDone
            ? "linear-gradient(135deg, #10B981, #059669)"
            : `linear-gradient(135deg, ${color}, ${color}bb)`,
          boxShadow: isLocked
            ? "0 6px 14px -6px rgba(0,0,0,0.15)"
            : isDone
            ? "0 14px 28px -10px #10B98160"
            : `0 14px 28px -10px ${color}70`,
        }}
      >
        {isLocked && <Lock className="w-6 h-6 text-zinc-400" />}
        {isDone && <Check className="w-8 h-8 text-white" strokeWidth={3} />}
        {isAvailable && <Lumi size={48} mood="happy" />}

        {isMastered && (
          <span className="absolute -top-2 -right-2 w-5 h-5 bg-[#FBBF24] rounded-full grid place-items-center">
            <Star className="w-3 h-3 text-zinc-900" fill="currentColor" />
          </span>
        )}

        {isAvailable && (
          <span className="absolute -bottom-2 left-1/2 -translate-x-1/2 bg-[#FF6B35] text-white text-[9px] font-black px-1.5 py-0.5 rounded-full whitespace-nowrap">
            +{concept.xp_reward} XP
          </span>
        )}
      </button>

      {/* Connector line to spine */}
      <div className={`h-0.5 flex-1 max-w-[56px] ${isLocked ? "bg-zinc-200" : isDone ? "bg-[#10B981]" : `bg-[${color}]`}`}
        style={{ background: isLocked ? "#E4E4E7" : isDone ? "#10B981" : color }} />

      {/* Label card */}
      <div className={`flex-1 ${side === "right" ? "text-right pr-2" : "pl-2"}`}>
        <p className="text-[10px] uppercase tracking-[0.2em] text-zinc-400 font-bold">Concept {index}</p>
        <p className="font-[Outfit] font-bold text-[15px] tracking-tight text-zinc-900 leading-tight">{concept.title}</p>
        {!isLocked && (
          <p className="text-xs text-zinc-500 mt-0.5 line-clamp-1">{concept.learning_objective}</p>
        )}
      </div>
    </div>
  );
}

function BossNode({ ch, bossReady, done, total, onPress }) {
  return (
    <div className="relative z-10 flex justify-center my-6">
      <button
        data-testid={`boss-cta-${ch.id}`}
        disabled={!bossReady}
        onClick={onPress}
        className={`w-full max-w-xs rounded-3xl p-5 flex items-center gap-4 transition-all duration-200 shadow-xl
          ${bossReady
            ? "bg-gradient-to-br from-zinc-950 via-zinc-900 to-[#1a0a2e] text-white hover:scale-[1.02] hover:shadow-2xl active:scale-[0.98]"
            : "bg-zinc-100 text-zinc-400 cursor-not-allowed"}`}
      >
        <div className={`w-14 h-14 rounded-2xl grid place-items-center shrink-0
          ${bossReady ? "bg-[#EC4899]/25 text-[#EC4899]" : "bg-zinc-200 text-zinc-400"}`}>
          {bossReady ? <Skull className="w-7 h-7" /> : <Lock className="w-6 h-6" />}
        </div>
        <div className="text-left">
          <p className={`text-[9px] uppercase tracking-[0.35em] font-bold ${bossReady ? "text-[#EC4899]" : "text-zinc-400"}`}>
            Boss Battle
          </p>
          <p className="font-[Outfit] font-black text-base leading-tight">
            {bossReady ? "Challenge the Boss" : "Complete all concepts first"}
          </p>
          <p className={`text-xs mt-0.5 ${bossReady ? "text-white/60" : "text-zinc-400"}`}>
            {bossReady
              ? "20 mixed questions · +200 XP"
              : `${done} / ${total} concepts done`}
          </p>
        </div>
        {bossReady && <Zap className="w-5 h-5 text-[#FBBF24] ml-auto" />}
      </button>
    </div>
  );
}
