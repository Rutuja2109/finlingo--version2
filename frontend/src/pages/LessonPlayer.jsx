import React, { useEffect, useMemo, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import Lumi from "@/components/Lumi";
import { sound } from "@/lib/sound";
import { haptics } from "@/lib/haptics";
import { Check, X, ChevronLeft, Sparkles, Trophy, RotateCcw, Repeat } from "lucide-react";
import { trackLessonCompleted, trackConceptCompleted, trackCaseStudyViewed } from "@/lib/firebase";

// ----------------------------------------------------------------------
// Duolingo-style lesson player
// - Lessons are processed via a QUEUE (array of lesson indices).
// - Wrong MCQ/scenario answers are appended back to the queue.
// - User MUST keep going until queue is empty (every question answered correctly at least once).
// - Continue button is ALWAYS enabled after the learner has answered (correct or wrong).
// - Score = (questions answered correctly on first try) / total scoreable questions.
// ----------------------------------------------------------------------

export default function LessonPlayer() {
  const { conceptId } = useParams();
  const nav = useNavigate();
  const { refreshStats } = useAuth();
  const [concept, setConcept] = useState(null);
  const [queue, setQueue] = useState([]);                 // array of lesson indices
  const [wrongFirstTry, setWrongFirstTry] = useState(new Set()); // indices the learner got wrong at least once
  const [picked, setPicked] = useState(null);             // chosen option on current lesson
  const [answered, setAnswered] = useState(null);         // {correct: bool} for the current attempt
  const [done, setDone] = useState(null);
  const [totalAttempted, setTotalAttempted] = useState(0);
  const [lumiMood, setLumiMood] = useState("happy");
  const [lumiAnim, setLumiAnim] = useState("lumi-float");
  const [lumiKey,  setLumiKey]  = useState(0);

  useEffect(() => {
    api.get(`/concepts/${conceptId}`).then(({ data }) => {
      const lessons = expandIntro(data);
      setConcept({ ...data, lessons });
      // Initialize queue with all lesson indices in order
      setQueue(lessons.map((_, i) => i));
    }).catch((e) => { if (e?.response?.status === 402) nav("/pro", { replace: true }); });
  }, [conceptId]);

  if (!concept) return <div className="text-center py-20 text-zinc-500">Loading…</div>;
  if (done) {
    return <ResultScreen result={done} concept={concept} onAgain={() => {
      setDone(null);
      setQueue(concept.lessons.map((_, i) => i));
      setWrongFirstTry(new Set());
      setPicked(null); setAnswered(null);
      setTotalAttempted(0);
    }} />;
  }

  const lessons = concept.lessons || [];
  const total = lessons.length;
  const currentIdx = queue[0];
  const current = lessons[currentIdx];

  // Progress = remaining queue length vs original total (counts re-queues)
  const initialQueueLen = total;
  const progressPct = Math.max(0, Math.min(100, ((initialQueueLen - queue.length + (answered ? 1 : 0)) / initialQueueLen) * 100));

  const scoreable = (lessons || []).filter((l) => l.type === "mcq" || l.type === "scenario").length || 1;
  const needsAnswerTypes = ["mcq", "scenario"];

  // --- Answer handlers ---
  const handleAnswer = (isCorrect) => {
    setPicked(true);
    setAnswered({ correct: isCorrect });
    trackLessonCompleted({ conceptId, lessonType: current.type, correct: isCorrect, xpEarned: 0 });
    if (isCorrect) {
      sound.correct();
      haptics.success();
      setLumiMood("cheer");
      setLumiAnim("lumi-bounce");
    } else {
      sound.wrong();
      haptics.error();
      setLumiMood("sad");
      setLumiAnim("shake");
      setWrongFirstTry((prev) => {
        const n = new Set(prev); n.add(currentIdx); return n;
      });
    }
    setLumiKey((k) => k + 1);
    setTotalAttempted((t) => t + 1);
  };

  // For intro / flashcard, advance without an answer step
  const advance = async () => {
    setLumiMood("happy");
    setLumiAnim("lumi-float");
    setLumiKey((k) => k + 1);
    let newQueue = queue.slice(1);
    if (answered && answered.correct === false) {
      // Re-queue the wrong question at the end
      newQueue = [...newQueue, currentIdx];
    }
    setPicked(null);
    setAnswered(null);

    if (newQueue.length === 0) {
      // Done — submit progress
      const correctFirstTry = scoreable - Array.from(wrongFirstTry).filter((i) =>
        lessons[i] && (lessons[i].type === "mcq" || lessons[i].type === "scenario")
      ).length;
      const score = Math.round((correctFirstTry / scoreable) * 100);
      try {
        const { data } = await api.post("/progress/complete-concept", {
          concept_id: conceptId, score, duration_sec: 0,
        });
        await refreshStats();
        trackConceptCompleted({ conceptId, conceptTitle: concept.title, chapterId: "", score, xpEarned: data.xp_earned || 0 });
        setDone(data);
      } catch (e) {
        setDone({ status: "completed", mastery: score, xp_earned: 0, coins_earned: 0, new_achievements: [] });
      }
      return;
    }
    setQueue(newQueue);
  };

  // ---- Render ----
  const needsAnswer = current.type === "mcq" || current.type === "scenario";
  const continueEnabled = !needsAnswer || answered !== null;
  const isFinalShift = queue.length === 1 && (!needsAnswer || (answered && answered.correct === true));

  return (
    <div className="max-w-3xl mx-auto pb-2 flex flex-col" style={{ minHeight: "calc(100dvh - 1.5rem)" }}>
      <div className="flex items-center gap-3 mb-5">
        <button onClick={() => nav(-1)} data-testid="lesson-exit" aria-label="Exit lesson" className="w-10 h-10 rounded-full bg-zinc-100 hover:bg-zinc-200 grid place-items-center">
          <ChevronLeft className="w-5 h-5"/>
        </button>
        <div className="flex-1 h-2.5 rounded-full bg-zinc-100 overflow-hidden">
          <div data-testid="lesson-progress-bar"
            className="h-full bg-gradient-to-r from-[#FF6B35] to-[#EC4899] transition-all duration-500"
            style={{ width: `${progressPct}%` }}/>
        </div>
        <div className="flex flex-col items-center">
          <Lumi key={lumiKey} size={42} mood={lumiMood} className={lumiAnim} />
          <span className="text-[10px] font-bold tabular-nums text-zinc-500 mt-0.5">
            {Math.max(1, initialQueueLen - queue.length + 1)}/{initialQueueLen}{queue.length > initialQueueLen ? "+" : ""}
          </span>
        </div>
      </div>

      <p className="uppercase tracking-[0.25em] text-[11px] font-bold text-zinc-500">Concept</p>
      <h1 className="font-[Outfit] font-black text-2xl md:text-3xl tracking-tight mb-6">{concept.title}</h1>

      {/* Re-queue indicator: shown when user is on a repeat question */}
      {answered === null && wrongFirstTry.has(currentIdx) && (
        <div className="mb-4 inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#FBBF24]/15 text-[#92400E] text-xs font-bold uppercase tracking-wider" data-testid="repeat-banner">
          <Repeat className="w-3.5 h-3.5"/> One more shot — you'll nail it this time
        </div>
      )}

      <div data-testid="lesson-card" className="bg-white border border-zinc-200 rounded-3xl p-6 md:p-8 min-h-[320px] mb-4">
        {current.type === "intro" && <IntroLesson l={current} concept={concept}/>}
        {current.type === "info" && <InfoLesson l={current}/>}
        {current.type === "teach" && <TeachLesson l={current}/>}
        {current.type === "example" && <ExampleLesson l={current}/>}
        {current.type === "case_study" && <CaseStudyLesson l={current} conceptId={conceptId} onShown={() => { if (!answered) handleAnswer(true); }}/>}
        {current.type === "mcq" && <McqLesson l={current} picked={picked} answered={answered} onAnswer={handleAnswer}/>}
        {current.type === "flashcard" && <FlashLesson l={current} onShown={() => { if (!answered) handleAnswer(true); }}/>}
        {current.type === "match" && <MatchLesson l={current} picked={picked} answered={answered} onAnswer={handleAnswer}/>}
        {current.type === "scenario" && <ScenarioLesson l={current} picked={picked} answered={answered} onAnswer={handleAnswer}/>}
      </div>

      {/* Always-visible action bar: Continue never hides below the content */}
      <div className="sticky bottom-0 z-30 -mx-5 px-5 mt-auto pt-3 pb-3 bg-[#FAFAFA]/95 backdrop-blur border-t border-zinc-200 flex justify-between items-center gap-3">
        <span className="text-xs text-zinc-500">
          {wrongFirstTry.size > 0 && `${wrongFirstTry.size} question${wrongFirstTry.size>1?"s":""} to revisit`}
        </span>
        <button
          data-testid="btn-next-lesson"
          disabled={!continueEnabled}
          onClick={advance}
          className={`px-7 py-3 rounded-2xl font-[Outfit] font-bold tracking-tight transition active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed ${
            answered && !answered.correct
              ? "bg-zinc-900 hover:bg-zinc-800 text-white"
              : "bg-[#FF6B35] hover:bg-[#FF5618] text-white"
          }`}
        >
          {isFinalShift && queue.length === 1 ? "Finish" : (answered && !answered.correct ? "Got it — try later" : "Continue")}
        </button>
      </div>
    </div>
  );
}

// ---------- Lesson types ----------
function TeachLesson({ l }) {
  const c = l.content || {};
  return (
    <div className="fade-up">
      <p className="uppercase tracking-[0.25em] text-[11px] font-bold text-[#10B981] mb-2">Learn</p>
      <h2 className="font-[Outfit] font-black text-2xl tracking-tight mb-4">{c.heading}</h2>
      <p className="text-zinc-700 leading-relaxed mb-4 text-[15px]">{c.body}</p>
      {Array.isArray(c.bullets) && c.bullets.length > 0 && (
        <ul className="space-y-2 mt-4 bg-zinc-50 rounded-2xl p-4">
          {c.bullets.map((b, i) => (
            <li key={i} className="flex gap-2 text-sm text-zinc-700">
              <span className="w-1.5 h-1.5 rounded-full bg-[#FF6B35] mt-2 shrink-0"/>
              <span>{b}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function ExampleLesson({ l }) {
  const c = l.content || {};
  return (
    <div className="fade-up">
      <p className="uppercase tracking-[0.25em] text-[11px] font-bold text-[#2563EB] mb-2">Real-world example</p>
      <h2 className="font-[Outfit] font-black text-2xl tracking-tight mb-4">{c.heading}</h2>
      <div className="bg-gradient-to-br from-[#2563EB]/5 to-[#EC4899]/5 border-l-4 border-[#2563EB] p-5 rounded-r-2xl mb-4">
        <p className="text-zinc-700 leading-relaxed italic">{c.scenario}</p>
      </div>
      {c.lesson && (
        <div className="bg-[#FBBF24]/15 border border-[#FBBF24]/30 rounded-2xl p-4">
          <p className="text-xs uppercase tracking-[0.25em] font-bold text-[#92400E] mb-1">The lesson</p>
          <p className="text-zinc-800 font-semibold">{c.lesson}</p>
        </div>
      )}
    </div>
  );
}

function IntroLesson({ l, concept }) {
  return (
    <div className="text-center fade-up">
      <div className="flex justify-center mb-5"><Lumi size={120} mood="happy"/></div>
      <h2 className="font-[Outfit] font-black text-3xl tracking-tight mb-3">{l.content.heading}</h2>
      <p className="text-zinc-600 max-w-xl mx-auto text-lg leading-relaxed">{l.content.body}</p>
    </div>
  );
}

// The intro's extra material (plain-English summary, real-world example, takeaways) is shown as its own
// short card after the intro, so each screen carries one idea.
function expandIntro(concept) {
  const out = [];
  for (const l of concept.lessons || []) {
    out.push(l);
    if (l.type !== "intro") continue;
    if (concept.simple_explanation) {
      out.push({ id: `${l.id}-plain`, type: "info", content: { kind: "plain", text: concept.simple_explanation } });
    }
    if (concept.real_world_example) {
      out.push({ id: `${l.id}-example`, type: "info", content: { kind: "example", text: concept.real_world_example } });
    }
    if (concept.key_takeaways?.length > 0) {
      out.push({ id: `${l.id}-takeaways`, type: "info", content: { kind: "takeaways", items: concept.key_takeaways } });
    }
  }
  return out;
}

function InfoLesson({ l }) {
  const c = l.content;
  if (c.kind === "plain") {
    return (
      <div className="fade-up">
        <p className="uppercase tracking-[0.25em] text-[11px] font-bold text-[#FF6B35] mb-2">In plain English</p>
        <div className="bg-gradient-to-br from-[#FF6B35]/5 to-[#EC4899]/5 border border-[#FF6B35]/15 rounded-2xl p-5">
          <p className="text-zinc-800 text-lg leading-relaxed">{c.text}</p>
        </div>
      </div>
    );
  }
  if (c.kind === "example") {
    return (
      <div className="fade-up">
        <p className="uppercase tracking-[0.25em] text-[11px] font-bold text-[#2563EB] mb-2">Real-life example</p>
        <div className="bg-[#2563EB]/5 border-l-4 border-[#2563EB] p-5 rounded-r-2xl">
          <p className="text-zinc-800 text-lg leading-relaxed">{c.text}</p>
        </div>
      </div>
    );
  }
  return (
    <div className="fade-up">
      <p className="uppercase tracking-[0.25em] text-[11px] font-bold text-[#10B981] mb-2">Key takeaways</p>
      <ul className="space-y-3">
        {(c.items || []).map((k, i) => (
          <li key={i} className="flex gap-3 text-zinc-800 leading-relaxed">
            <Check className="w-5 h-5 text-[#10B981] mt-0.5 shrink-0"/>
            <span>{k}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

function McqLesson({ l, picked, answered, onAnswer }) {
  const [pickedIdx, setPickedIdx] = useState(null);

  // Reset local pickedIdx when the parent clears answered (i.e., on advance)
  useEffect(() => {
    if (answered === null) setPickedIdx(null);
  }, [answered]);

  const choose = (i) => {
    if (answered !== null) return;
    setPickedIdx(i);
    onAnswer(i === l.content.correct);
  };

  return (
    <div className="fade-up">
      <p className="uppercase tracking-[0.25em] text-[11px] font-bold text-[#FF6B35] mb-2">Quick check</p>
      <h2 className="font-[Outfit] font-black text-2xl tracking-tight mb-6">{l.content.question}</h2>
      <div className="grid gap-3">
        {l.content.options.map((opt, i) => {
          const isCorrect = i === l.content.correct;
          const isPicked = i === pickedIdx;
          const showResult = pickedIdx !== null;
          let cls = "border-zinc-200 hover:border-zinc-400 bg-white";
          if (showResult && isPicked && isCorrect) cls = "border-[#10B981] bg-[#10B981]/10";
          else if (showResult && isPicked && !isCorrect) cls = "border-[#EF4444] bg-[#EF4444]/10 shake";
          else if (showResult && isCorrect) cls = "border-[#10B981] bg-[#10B981]/5";
          return (
            <button key={i} data-testid={`mcq-option-${i}`} onClick={() => choose(i)} disabled={answered !== null}
              className={`text-left px-5 py-4 rounded-2xl border-2 font-semibold transition-all duration-200 flex items-center justify-between ${cls} ${!showResult && "active:scale-[0.98]"}`}>
              <span>{opt}</span>
              {showResult && isPicked && isCorrect && <Check className="w-5 h-5 text-[#10B981]"/>}
              {showResult && isPicked && !isCorrect && <X className="w-5 h-5 text-[#EF4444]"/>}
              {showResult && !isPicked && isCorrect && <Check className="w-5 h-5 text-[#10B981]/60"/>}
            </button>
          );
        })}
      </div>
      {answered !== null && (
        <div className={`mt-5 p-4 rounded-2xl fade-up ${answered.correct ? "bg-[#10B981]/10 text-[#065F46]" : "bg-[#EF4444]/10 text-[#7F1D1D]"}`} data-testid="mcq-feedback">
          <strong className="font-[Outfit]">{answered.correct ? "Nailed it! " : "Not quite. "}</strong>
          {l.content.explanation}
          {!answered.correct && (
            <p className="mt-2 text-xs font-semibold opacity-80">↻ We'll ask this again later in the lesson.</p>
          )}
        </div>
      )}
    </div>
  );
}

function FlashLesson({ l, onShown }) {
  const [flipped, setFlipped] = useState(false);
  return (
    <div className="fade-up">
      <p className="uppercase tracking-[0.25em] text-[11px] font-bold text-[#2563EB] mb-2">Flashcard</p>
      <div
        data-testid="flashcard"
        onClick={() => { setFlipped(!flipped); sound.flip(); if (!flipped) onShown(); }}
        className="cursor-pointer bg-gradient-to-br from-zinc-50 to-white border-2 border-zinc-200 rounded-3xl p-10 min-h-[220px] grid place-items-center text-center hover:border-[#FF6B35] transition"
      >
        <div>
          <p className="uppercase text-[10px] tracking-[0.3em] font-bold text-zinc-500 mb-3">
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
  const pairs = l.content.pairs || [];
  const [shuffledRight] = useState(() => [...pairs].sort(() => Math.random() - 0.5));
  const [selectedLeft, setSelectedLeft] = useState(null);
  const [matches, setMatches] = useState({});
  const isAnswered = answered !== null;

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
    <div className="fade-up">
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
          {answered.correct ? "All matched correctly!" : "Some pairs are off — we'll ask again later."}
        </p>
      )}
    </div>
  );
}

function CaseStudyLesson({ l, onShown, conceptId }) {
  const c = l.content || {};
  const [step, setStep] = useState(0);
  const steps = c.steps || [];
  const isLast = step >= steps.length - 1;

  useEffect(() => { trackCaseStudyViewed({ title: c.title || "", conceptId: conceptId || "" }); }, []); // eslint-disable-line
  useEffect(() => { if (isLast) onShown(); }, [isLast]); // eslint-disable-line

  const current = steps[step] || {};

  return (
    <div className="fade-up">
      <div className="flex items-center gap-2 mb-3">
        <span className="uppercase tracking-[0.25em] text-[11px] font-bold text-[#8B5CF6]">Case Study</span>
        <span className="text-[10px] text-zinc-500 font-bold">{step + 1} / {steps.length}</span>
      </div>

      {step === 0 && (
        <div className="mb-4 bg-gradient-to-br from-[#8B5CF6]/10 to-[#EC4899]/10 border border-[#8B5CF6]/20 rounded-2xl p-4">
          <p className="font-[Outfit] font-black text-lg tracking-tight">{c.title}</p>
          {c.context && <p className="text-sm text-zinc-500 mt-1">{c.context}</p>}
        </div>
      )}

      <div className="bg-white border-2 border-zinc-100 rounded-2xl p-5 min-h-[140px]">
        {current.label && (
          <p className="text-[10px] uppercase tracking-[0.3em] font-bold text-[#8B5CF6] mb-2">{current.label}</p>
        )}
        <p className="text-zinc-800 leading-relaxed text-[15px]">{current.text}</p>
        {current.highlight && (
          <div className="mt-3 bg-[#FBBF24]/15 border-l-4 border-[#FBBF24] px-4 py-3 rounded-r-xl">
            <p className="text-sm font-semibold text-zinc-800">{current.highlight}</p>
          </div>
        )}
      </div>

      {!isLast && (
        <button onClick={() => setStep(step + 1)}
          className="mt-4 px-5 py-2.5 rounded-xl bg-[#8B5CF6] text-white font-bold text-sm hover:bg-[#7C3AED] transition">
          Next →
        </button>
      )}

      {isLast && c.lesson && (
        <div className="mt-4 bg-[#10B981]/10 border border-[#10B981]/30 rounded-2xl p-4">
          <p className="text-xs uppercase tracking-[0.25em] font-bold text-[#065F46] mb-1">The Lesson</p>
          <p className="text-zinc-800 font-semibold">{c.lesson}</p>
        </div>
      )}
    </div>
  );
}

// verdict: "good" (best), "ok" (safe but not best), "bad" (wrong). Older content only has `correct`.
const VERDICT_STYLE = {
  good: { box: "bg-[#10B981]/10 border-[#10B981]/40 text-[#065F46]", title: "Smart move", Icon: Check, color: "text-[#10B981]" },
  ok:   { box: "bg-[#F59E0B]/10 border-[#F59E0B]/40 text-[#92400E]", title: "Safe, but not the best", Icon: Check, color: "text-[#F59E0B]" },
  bad:  { box: "bg-[#EF4444]/10 border-[#EF4444]/40 text-[#7F1D1D]", title: "Not this one", Icon: X, color: "text-[#EF4444]" },
};
const rupees = (n) => `₹${Math.round(n).toLocaleString("en-IN")}`;

function OutcomeBars({ outcome }) {
  const [bLabel, bVal] = outcome.before;
  const [aLabel, aVal] = outcome.after;
  const max = Math.max(bVal, aVal, 1);
  const lost = aVal < bVal;
  return (
    <div className="mt-4 bg-white border border-zinc-200 rounded-2xl p-4 fade-up" data-testid="scenario-outcome">
      <p className="uppercase tracking-[0.2em] text-[10px] font-bold text-zinc-500 mb-3">What happened next</p>
      <div className="flex justify-between text-sm mb-1"><span>{bLabel}</span><b className="font-[Outfit]">{rupees(bVal)}</b></div>
      <div className="h-3 rounded-full bg-zinc-100 overflow-hidden mb-3">
        <div className="h-full rounded-full bg-zinc-300 transition-all duration-700" style={{ width: `${(bVal / max) * 100}%` }} />
      </div>
      <div className="flex justify-between text-sm mb-1"><span>{aLabel}</span><b className="font-[Outfit]">{rupees(aVal)}</b></div>
      <div className="h-3 rounded-full bg-zinc-100 overflow-hidden mb-2">
        <div className="h-full rounded-full transition-all duration-700"
          style={{ width: `${(aVal / max) * 100}%`, background: lost ? "#EF4444" : "#10B981" }} />
      </div>
      {outcome.note && <p className="text-xs text-zinc-500">{outcome.note}</p>}
    </div>
  );
}

function ScenarioLesson({ l, answered, onAnswer }) {
  const [pickedIdx, setPickedIdx] = useState(null);

  useEffect(() => { if (answered === null) setPickedIdx(null); }, [answered]);

  const pick = (i) => {
    if (answered !== null) return;
    setPickedIdx(i);
    onAnswer(l.content.choices[i].correct);
  };

  const choices = l.content.choices || [];
  const picked = pickedIdx !== null ? choices[pickedIdx] : null;
  const verdict = picked ? (picked.verdict || (picked.correct ? "good" : "bad")) : null;
  const vs = verdict ? VERDICT_STYLE[verdict] : null;

  return (
    <div className="fade-up">
      <p className="uppercase tracking-[0.25em] text-[11px] font-bold text-[#EC4899] mb-2">Real-life situation</p>
      <div className="bg-zinc-50 border-l-4 border-[#EC4899] p-4 rounded-r-2xl mb-5">
        <p className="text-zinc-700 italic">{l.content.scene}</p>
      </div>
      <h2 className="font-[Outfit] font-black text-xl tracking-tight mb-5">{l.content.question}</h2>
      <div className="space-y-3">
        {choices.map((c, i) => {
          const showResult = pickedIdx !== null;
          const cv = c.verdict || (c.correct ? "good" : "bad");
          let cls = "border-zinc-200 hover:border-[#FF6B35] bg-white";
          if (showResult && i === pickedIdx) {
            cls = cv === "good" ? "border-[#10B981] bg-[#10B981]/10"
              : cv === "ok" ? "border-[#F59E0B] bg-[#F59E0B]/10"
              : "border-[#EF4444] bg-[#EF4444]/10 shake";
          } else if (showResult && cv === "good") {
            cls = "border-[#10B981] bg-[#10B981]/5";
          }
          return (
            <button key={i} data-testid={`scenario-choice-${i}`} onClick={() => pick(i)} disabled={answered !== null}
              className={`w-full text-left px-5 py-4 rounded-2xl border-2 font-semibold transition active:scale-[0.98] ${cls}`}>
              <span>{c.text}</span>
            </button>
          );
        })}
      </div>

      {picked && vs && (
        <div className={`mt-5 p-4 rounded-2xl border fade-up ${vs.box}`} data-testid="scenario-feedback">
          <p className="font-[Outfit] font-extrabold flex items-center gap-2 mb-1">
            <vs.Icon className={`w-5 h-5 ${vs.color}`} /> {vs.title}
          </p>
          <p className="text-sm leading-relaxed">{picked.feedback}</p>
        </div>
      )}
      {picked && picked.outcome && <OutcomeBars outcome={picked.outcome} />}

      {answered !== null && !answered.correct && (
        <p className="mt-3 text-xs font-semibold text-[#7F1D1D] opacity-80">↻ We'll ask this again later in the lesson.</p>
      )}
    </div>
  );
}

// ---------- Result ----------
function ResultScreen({ result, concept, onAgain }) {
  const nav = useNavigate();
  const isMastered = result.status === "mastered";

  useEffect(() => {
    if (!isMastered) return;
    sound.complete();
    haptics.celebrate();
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
        <Lumi size={160} mood={isMastered ? "celebrate" : "happy"} className={isMastered ? "lumi-celebrate" : "lumi-float"} />
      </div>
      <h1 className="font-[Outfit] font-black text-4xl tracking-tight mb-2">
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
          className="flex-1 px-3 py-3 rounded-2xl bg-white border border-zinc-200 hover:border-zinc-400 font-bold inline-flex items-center justify-center gap-2 whitespace-nowrap">
          <RotateCcw className="w-4 h-4"/> Practice again
        </button>
        <button onClick={() => nav(-1)} data-testid="btn-continue-path"
          className="flex-1 px-3 py-3 rounded-2xl bg-[#FF6B35] hover:bg-[#FF5618] text-white font-[Outfit] font-bold inline-flex items-center justify-center gap-2 whitespace-nowrap">
          <Sparkles className="w-4 h-4"/> Continue path
        </button>
      </div>
    </div>
  );
}

function Pill({ label, value, color }) {
  return (
    <div className="bg-white border border-zinc-200 rounded-2xl p-4">
      <p className="text-xs uppercase tracking-[0.2em] font-bold text-zinc-500">{label}</p>
      <p className="font-[Outfit] font-black text-2xl tabular-nums" style={{ color }}>{value}</p>
    </div>
  );
}
