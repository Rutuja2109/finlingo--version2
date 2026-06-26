import React, { useEffect, useMemo, useState } from "react";import { useParams, useNavigate } from "react-router-dom";
import { api } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import Lumi from "@/components/Lumi";
import { Check, X, ChevronLeft, Sparkles, Trophy, RotateCcw } from "lucide-react";

export default function LessonPlayer() {
  const { conceptId } = useParams();
  const nav = useNavigate();
  const { refreshStats } = useAuth();
  const [concept, setConcept] = useState(null);
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState({}); // step idx -> {correct}
  const [done, setDone] = useState(null); // result payload

  useEffect(() => {
    api.get(`/concepts/${conceptId}`).then(({ data }) => setConcept(data));
  }, [conceptId]);

  const lessons = concept?.lessons || [];
  const total = lessons.length;
  const current = lessons[step];

  const correctCount = useMemo(
    () => Object.values(answers).filter((a) => a.correct).length,
    [answers]
  );
  const totalScored = useMemo(
    () => Object.keys(answers).length,
    [answers]
  );

  const onAnswer = (correct) => {
    setAnswers((a) => ({ ...a, [step]: { correct } }));
  };

  const goNext = async () => {
    if (step < total - 1) {
      setStep(step + 1);
    } else {
      // submit
      const scoreable = lessons.filter((l) => l.type !== "intro" && l.type !== "flashcard").length || 1;
      const score = Math.round((correctCount / Math.max(1, scoreable)) * 100);
      const { data } = await api.post("/progress/complete-concept", {
        concept_id: conceptId, score, duration_sec: 0,
      });
      setDone(data);
      refreshStats();
    }
  };

  if (!concept) return <div className="text-center py-20 text-zinc-500">Loading…</div>;
  if (done) return <ResultScreen result={done} concept={concept} onAgain={() => { setDone(null); setStep(0); setAnswers({}); }} />;

  const answered = answers[step]?.correct !== undefined;
  const progressPct = ((step + 1) / total) * 100;

  return (
    <div className="max-w-3xl mx-auto pb-24">
      <div className="flex items-center gap-3 mb-6">
        <button onClick={() => nav(-1)} data-testid="lesson-exit" className="w-10 h-10 rounded-full bg-zinc-100 hover:bg-zinc-200 grid place-items-center">
          <ChevronLeft className="w-5 h-5"/>
        </button>
        <div className="flex-1 h-2.5 rounded-full bg-zinc-100 overflow-hidden">
          <div data-testid="lesson-progress-bar"
            className="h-full bg-gradient-to-r from-[#FF6B35] to-[#EC4899] transition-all duration-500"
            style={{ width: `${progressPct}%` }}/>
        </div>
        <span className="text-sm font-bold tabular-nums text-zinc-500">{step+1}/{total}</span>
      </div>

      <p className="uppercase tracking-[0.25em] text-[11px] font-bold text-zinc-400">Concept</p>
      <h1 className="font-[Outfit] font-black text-2xl md:text-3xl tracking-tight mb-6">{concept.title}</h1>

      <div data-testid="lesson-card" className="bg-white border border-zinc-200 rounded-3xl p-6 md:p-8 min-h-[320px]">
        {current.type === "intro" && <IntroLesson l={current}/>}
        {current.type === "mcq" && <McqLesson l={current} answered={answers[step]} onAnswer={onAnswer}/>}
        {current.type === "flashcard" && <FlashLesson l={current} onShown={() => onAnswer(true)}/>}
        {current.type === "match" && <MatchLesson l={current} answered={answers[step]} onAnswer={onAnswer}/>}
        {current.type === "scenario" && <ScenarioLesson l={current} answered={answers[step]} onAnswer={onAnswer}/>}
      </div>

      <div className="mt-6 flex justify-end">
        <button
          data-testid="btn-next-lesson"
          disabled={!(current.type === "intro" || current.type === "flashcard" || (answered && answered.correct === true))}
          onClick={goNext}
          className="px-7 py-3 rounded-2xl bg-[#FF6B35] hover:bg-[#FF5618] text-white font-[Outfit] font-bold tracking-tight transition active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {step === total - 1 ? "Finish" : "Continue"}
        </button>
      </div>
    </div>
  );
}

// ---------- Lesson types ----------
function IntroLesson({ l, concept }) {
  return (
    <div className="text-center fade-up">
      <div className="flex justify-center mb-5"><Lumi size={120} mood="happy"/></div>
      <h2 className="font-[Outfit] font-black text-3xl tracking-tighter mb-3">{l.content.heading}</h2>
      <p className="text-zinc-600 max-w-xl mx-auto text-lg leading-relaxed mb-6">{l.content.body}</p>

      {concept?.simple_explanation && (
        <div className="bg-gradient-to-br from-[#FF6B35]/5 to-[#EC4899]/5 border border-[#FF6B35]/15 rounded-2xl p-5 text-left max-w-xl mx-auto mb-4">
          <p className="text-xs uppercase tracking-[0.25em] font-bold text-[#FF6B35] mb-2">In plain English</p>
          <p className="text-zinc-700 leading-relaxed">{concept.simple_explanation}</p>
        </div>
      )}

      {concept?.real_world_example && (
        <div className="bg-[#2563EB]/5 border-l-4 border-[#2563EB] p-4 rounded-r-2xl text-left max-w-xl mx-auto mb-4">
          <p className="text-xs uppercase tracking-[0.25em] font-bold text-[#2563EB] mb-1">Real-world example</p>
          <p className="text-zinc-700 text-sm">{concept.real_world_example}</p>
        </div>
      )}

      {concept?.key_takeaways?.length > 0 && (
        <div className="text-left max-w-xl mx-auto">
          <p className="text-xs uppercase tracking-[0.25em] font-bold text-zinc-500 mb-2">Key takeaways</p>
          <ul className="space-y-1.5">
            {concept.key_takeaways.map((k, i) => (
              <li key={i} className="flex gap-2 text-sm text-zinc-700">
                <Check className="w-4 h-4 text-[#10B981] mt-0.5 shrink-0"/>
                <span>{k}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

function McqLesson({ l, answered, onAnswer }) {
  const [picked, setPicked] = useState(null);
  const [attempts, setAttempts] = useState(0);
  const isAnswered = answered !== undefined && answered.correct === true;

  const choose = (i) => {
    if (isAnswered) return;
    setPicked(i);
    setAttempts((a) => a + 1);
    const correct = i === l.content.correct;
    if (correct) {
      onAnswer(true);
    } else {
      // wrong — let them retry (don't lock answer)
      onAnswer(false);
    }
  };

  const tryAgain = () => {
    setPicked(null);
    // Reset 'correct' flag so they can answer again
    onAnswer(undefined);
  };

  return (
    <div className="fade-up">
      <p className="uppercase tracking-[0.25em] text-[11px] font-bold text-[#FF6B35] mb-2">Quick check</p>
      <h2 className="font-[Outfit] font-black text-2xl tracking-tight mb-6">{l.content.question}</h2>
      <div className="grid gap-3">
        {l.content.options.map((opt, i) => {
          const isCorrect = i === l.content.correct;
          const isPicked = i === picked;
          const showResult = picked !== null;
          let cls = "border-zinc-200 hover:border-zinc-400 bg-white";
          if (showResult && isAnswered && isCorrect) cls = "border-[#10B981] bg-[#10B981]/10";
          else if (showResult && isPicked && !isCorrect) cls = "border-[#EF4444] bg-[#EF4444]/10 shake";
          else if (showResult && isCorrect && answered?.correct === true) cls = "border-[#10B981] bg-[#10B981]/10";
          return (
            <button key={i} data-testid={`mcq-option-${i}`} onClick={() => choose(i)} disabled={isAnswered}
              className={`text-left px-5 py-4 rounded-2xl border-2 font-semibold transition-all duration-200 flex items-center justify-between ${cls} ${!isAnswered && "active:scale-[0.98]"}`}>
              <span>{opt}</span>
              {showResult && isAnswered && isCorrect && <Check className="w-5 h-5 text-[#10B981] pulse-glow"/>}
              {showResult && isPicked && !isCorrect && <X className="w-5 h-5 text-[#EF4444]"/>}
            </button>
          );
        })}
      </div>
      {picked !== null && (
        <div className={`mt-5 p-4 rounded-2xl fade-up ${answered?.correct ? "bg-[#10B981]/10 text-[#065F46]" : "bg-[#EF4444]/10 text-[#7F1D1D]"}`} data-testid="mcq-feedback">
          <strong className="font-[Outfit]">{answered?.correct ? "Nailed it! " : `Not quite${attempts > 1 ? ` (attempt ${attempts})` : ""}. `}</strong>
          {l.content.explanation}
          {!answered?.correct && (
            <button onClick={tryAgain} data-testid="btn-try-again"
              className="ml-2 inline-flex items-center gap-1 text-[#EF4444] underline font-bold text-sm hover:no-underline">
              Try again →
            </button>
          )}
        </div>
      )}
    </div>
  );
}

function FlashLesson({ l, onShown }) {
  const [flipped, setFlipped] = useState(false);
  return (
    <div>
      <p className="uppercase tracking-[0.25em] text-[11px] font-bold text-[#2563EB] mb-2">Flashcard</p>
      <div
        data-testid="flashcard"
        onClick={() => { setFlipped(!flipped); if (!flipped) onShown(); }}
        className="cursor-pointer bg-gradient-to-br from-zinc-50 to-white border-2 border-zinc-200 rounded-3xl p-10 min-h-[220px] grid place-items-center text-center hover:border-[#FF6B35] transition"
      >
        <div>
          <p className="uppercase text-[10px] tracking-[0.3em] font-bold text-zinc-400 mb-3">
            {flipped ? "Answer" : "Question · tap to reveal"}
          </p>
          <p className="font-[Outfit] font-bold text-xl md:text-2xl tracking-tight">
            {flipped ? l.content.back : l.content.front}
          </p>
        </div>
      </div>
    </div>
  );
}

function MatchLesson({ l, answered, onAnswer }) {
  const pairs = l.content.pairs;
  const [shuffledRight] = useState(() => [...pairs].sort(() => Math.random() - 0.5));
  const [selectedLeft, setSelectedLeft] = useState(null);
  const [matches, setMatches] = useState({}); // leftIdx -> rightIdx
  const isAnswered = answered !== undefined;

  const pickLeft = (i) => { if (!isAnswered && !matches[i]) setSelectedLeft(i); };
  const pickRight = (j) => {
    if (selectedLeft === null) return;
    const newMatches = { ...matches, [selectedLeft]: j };
    setMatches(newMatches);
    setSelectedLeft(null);
    if (Object.keys(newMatches).length === pairs.length) {
      const allCorrect = pairs.every((p, idx) => shuffledRight[newMatches[idx]].right === p.right);
      onAnswer(allCorrect);
    }
  };
  const usedRights = new Set(Object.values(matches));

  return (
    <div>
      <p className="uppercase tracking-[0.25em] text-[11px] font-bold text-[#8B5CF6] mb-2">Match the pairs</p>
      <h2 className="font-[Outfit] font-black text-2xl tracking-tight mb-6">{l.content.instruction}</h2>
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          {pairs.map((p, i) => {
            const matched = matches[i] !== undefined;
            const correct = matched && shuffledRight[matches[i]].right === p.right;
            return (
              <button key={i} data-testid={`match-left-${i}`} onClick={() => pickLeft(i)} disabled={matched || isAnswered}
                className={`w-full px-4 py-3 rounded-xl border-2 text-left font-semibold transition
                  ${selectedLeft === i ? "border-[#FF6B35] bg-[#FF6B35]/10" : matched ? (correct ? "border-[#10B981] bg-[#10B981]/10" : "border-[#EF4444] bg-[#EF4444]/10") : "border-zinc-200 hover:border-zinc-400"}`}>
                {p.left}
              </button>
            );
          })}
        </div>
        <div className="space-y-2">
          {shuffledRight.map((p, j) => {
            const isUsed = usedRights.has(j);
            return (
              <button key={j} data-testid={`match-right-${j}`} onClick={() => pickRight(j)} disabled={isUsed || isAnswered}
                className={`w-full px-4 py-3 rounded-xl border-2 text-left font-semibold transition
                  ${isUsed ? "opacity-50 border-zinc-200" : "border-zinc-200 hover:border-[#FF6B35]"}`}>
                {p.right}
              </button>
            );
          })}
        </div>
      </div>
      {isAnswered && (
        <p className={`mt-4 font-bold ${answered.correct ? "text-[#10B981]" : "text-[#EF4444]"}`} data-testid="match-feedback">
          {answered.correct ? "All matched correctly!" : "Some pairs are off — review and continue."}
        </p>
      )}
    </div>
  );
}

function ScenarioLesson({ l, answered, onAnswer }) {
  const [picked, setPicked] = useState(null);
  const [attempts, setAttempts] = useState(0);
  const isAnswered = answered !== undefined && answered.correct === true;

  const pick = (i) => {
    if (isAnswered) return;
    setPicked(i);
    setAttempts((a) => a + 1);
    onAnswer(l.content.choices[i].correct);
  };
  const tryAgain = () => { setPicked(null); onAnswer(undefined); };

  return (
    <div className="fade-up">
      <p className="uppercase tracking-[0.25em] text-[11px] font-bold text-[#EC4899] mb-2">Real-world Scenario</p>
      <div className="bg-zinc-50 border-l-4 border-[#EC4899] p-4 rounded-r-2xl mb-5">
        <p className="text-zinc-700 italic">{l.content.scene}</p>
      </div>
      <h2 className="font-[Outfit] font-black text-xl tracking-tight mb-5">{l.content.question}</h2>
      <div className="space-y-3">
        {l.content.choices.map((c, i) => {
          const showResult = picked !== null;
          let cls = "border-zinc-200 hover:border-zinc-400";
          if (showResult && i === picked && c.correct) cls = "border-[#10B981] bg-[#10B981]/10";
          else if (showResult && i === picked && !c.correct) cls = "border-[#EF4444] bg-[#EF4444]/10 shake";
          else if (showResult && isAnswered && c.correct) cls = "border-[#10B981] bg-[#10B981]/5";
          return (
            <button key={i} data-testid={`scenario-choice-${i}`} onClick={() => pick(i)} disabled={isAnswered}
              className={`w-full text-left px-5 py-4 rounded-2xl border-2 font-semibold transition ${cls}`}>
              <span>{c.text}</span>
              {showResult && i === picked && (
                <p className="text-sm font-normal mt-2 text-zinc-600">{c.feedback}</p>
              )}
            </button>
          );
        })}
      </div>
      {picked !== null && !answered?.correct && (
        <button onClick={tryAgain} data-testid="btn-try-again-scenario"
          className="mt-4 inline-flex items-center gap-1 text-[#EF4444] underline font-bold text-sm hover:no-underline">
          Try again (attempt {attempts}) →
        </button>
      )}
    </div>
  );
}

// ---------- Result ----------
function ResultScreen({ result, concept, onAgain }) {
  const nav = useNavigate();
  const isMastered = result.status === "mastered";

  useEffect(() => {
    // Confetti burst on mastery
    if (!isMastered) return;
    const colors = ["#FF6B35", "#EC4899", "#FBBF24", "#10B981", "#2563EB"];
    const pieces = [];
    for (let i = 0; i < 40; i++) {
      const el = document.createElement("div");
      el.className = "confetti-piece";
      el.style.left = Math.random() * 100 + "vw";
      el.style.background = colors[i % colors.length];
      el.style.animationDuration = (1.6 + Math.random() * 1.2) + "s";
      el.style.animationDelay = (Math.random() * 0.4) + "s";
      el.style.borderRadius = Math.random() > 0.5 ? "50%" : "2px";
      document.body.appendChild(el);
      pieces.push(el);
    }
    const t = setTimeout(() => pieces.forEach((p) => p.remove()), 3500);
    return () => { clearTimeout(t); pieces.forEach((p) => p.remove()); };
  }, [isMastered]);

  return (
    <div className="max-w-xl mx-auto text-center pb-24 fade-up">
      <div className="mt-8 mb-4 flex justify-center">
        <Lumi size={160} mood={isMastered ? "cheer" : "happy"}/>
      </div>
      <h1 className="font-[Outfit] font-black text-4xl tracking-tighter mb-2">
        {isMastered ? "Concept mastered!" : result.status === "completed" ? "Nicely done!" : "Keep going!"}
      </h1>
      <p className="text-zinc-500 mb-8">{concept.title}</p>

      <div className="grid grid-cols-3 gap-3 mb-8">
        <Pill label="XP earned" value={`+${result.xp_earned}`} color="#FBBF24"/>
        <Pill label="Coins" value={`+${result.coins_earned}`} color="#F59E0B"/>
        <Pill label="Mastery" value={`${result.mastery}%`} color="#10B981"/>
      </div>

      {result.new_achievements?.length > 0 && (
        <div className="mb-6 bg-gradient-to-br from-[#FBBF24]/15 to-[#FF6B35]/15 rounded-3xl p-5 border border-[#FBBF24]/40" data-testid="achievement-unlock">
          <Trophy className="w-7 h-7 mx-auto text-[#FF6B35] mb-2"/>
          <p className="font-[Outfit] font-black text-lg">Achievement unlocked!</p>
          {result.new_achievements.map((a) => (
            <p key={a.code} className="text-sm font-semibold text-zinc-700">🏆 {a.title}</p>
          ))}
        </div>
      )}

      <div className="flex gap-3 justify-center">
        <button onClick={onAgain} data-testid="btn-redo"
          className="px-5 py-3 rounded-2xl bg-white border border-zinc-200 hover:border-zinc-400 font-bold inline-flex items-center gap-2">
          <RotateCcw className="w-4 h-4"/> Practice again
        </button>
        <button onClick={() => nav(-1)} data-testid="btn-continue-path"
          className="px-6 py-3 rounded-2xl bg-[#FF6B35] hover:bg-[#FF5618] text-white font-[Outfit] font-bold inline-flex items-center gap-2">
          <Sparkles className="w-4 h-4"/> Continue path
        </button>
      </div>
    </div>
  );
}

function Pill({ label, value, color }) {
  return (
    <div className="bg-white border border-zinc-200 rounded-2xl p-4">
      <p className="text-xs uppercase tracking-[0.2em] font-bold text-zinc-400">{label}</p>
      <p className="font-[Outfit] font-black text-2xl tabular-nums" style={{ color }}>{value}</p>
    </div>
  );
}
