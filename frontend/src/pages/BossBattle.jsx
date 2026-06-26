import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import Lumi from "@/components/Lumi";
import { Crown, Skull, Sparkles, Zap, Lock, X, Check } from "lucide-react";

export default function BossBattle() {
  const { chapterId } = useParams();
  const nav = useNavigate();
  const { refreshStats } = useAuth();
  const [data, setData] = useState(null);
  const [idx, setIdx] = useState(0);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);

  useEffect(() => { api.get(`/boss-battles/${chapterId}`).then(({ data }) => setData(data)); }, [chapterId]);

  if (!data) return <div className="text-center py-20 text-zinc-500">Loading…</div>;

  if (!data.unlocked) {
    return (
      <div className="min-h-[80vh] grid place-items-center bg-zinc-950 text-white rounded-3xl p-10 border border-zinc-800 -m-2">
        <div className="text-center max-w-md">
          <Lock className="w-12 h-12 mx-auto text-[#EC4899] mb-3"/>
          <h1 className="font-[Outfit] font-black text-3xl tracking-tighter mb-2">Boss locked</h1>
          <p className="text-zinc-400">Master all {data.concepts_total} concepts of this chapter to challenge the boss. You're at {data.concepts_done}/{data.concepts_total}.</p>
          <button onClick={() => nav(-1)} className="mt-5 px-5 py-3 rounded-2xl bg-white text-zinc-900 font-[Outfit] font-bold">Back</button>
        </div>
      </div>
    );
  }

  const q = data.questions[idx];

  const choose = (i) => {
    if (answers[idx] !== undefined) return;
    setAnswers({ ...answers, [idx]: i });
  };

  const next = async () => {
    if (idx + 1 < data.questions.length) {
      setIdx(idx + 1);
      return;
    }
    // submit
    let correct = 0;
    data.questions.forEach((qq, i) => { if (answers[i] === qq.content.correct) correct++; });
    const { data: res } = await api.post("/boss-battles/submit", {
      chapter_id: chapterId, correct_count: correct, total: data.questions.length,
    });
    setResult(res);
    refreshStats();
  };

  if (result) {
    return (
      <div className="min-h-[80vh] bg-gradient-to-br from-zinc-950 via-zinc-900 to-[#1a0a2e] text-white rounded-3xl p-10 -m-2 grid place-items-center relative overflow-hidden">
        <div className="absolute inset-0 opacity-30" style={{
          background: "radial-gradient(circle at 30% 20%, rgba(236,72,153,0.4), transparent 50%), radial-gradient(circle at 70% 80%, rgba(255,107,53,0.4), transparent 50%)"
        }}/>
        <div className="relative text-center max-w-md">
          {result.passed ? <Crown className="w-16 h-16 mx-auto text-[#FBBF24] mb-3"/> : <Skull className="w-16 h-16 mx-auto text-[#EF4444] mb-3"/>}
          <h1 className="font-[Outfit] font-black text-5xl tracking-tighter mb-2">{result.passed ? "Victory!" : "Defeated"}</h1>
          <p className="text-zinc-300 mb-7">Score: <span className="text-[#FBBF24] font-bold text-2xl">{result.score}%</span></p>
          <div className="grid grid-cols-2 gap-3 mb-6">
            <div className="bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-4">
              <p className="text-[10px] uppercase tracking-wider text-white/60">XP earned</p>
              <p className="font-[Outfit] font-black text-2xl text-[#FBBF24]">+{result.xp_earned}</p>
            </div>
            <div className="bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-4">
              <p className="text-[10px] uppercase tracking-wider text-white/60">Coins</p>
              <p className="font-[Outfit] font-black text-2xl text-[#F59E0B]">+{result.coins_earned}</p>
            </div>
          </div>
          {result.new_achievements?.length > 0 && (
            <div data-testid="boss-achievement" className="bg-gradient-to-br from-[#FBBF24]/20 to-[#EC4899]/20 border border-[#FBBF24]/40 rounded-2xl p-4 mb-5">
              <Crown className="w-5 h-5 mx-auto text-[#FBBF24] mb-1"/>
              {result.new_achievements.map((a) => <p key={a.code} className="font-bold">🏆 {a.title}</p>)}
            </div>
          )}
          <button onClick={() => nav(-1)} data-testid="boss-exit"
            className="px-7 py-3 rounded-2xl bg-white text-zinc-900 font-[Outfit] font-bold inline-flex items-center gap-2">
            <Sparkles className="w-4 h-4"/> Return
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-[85vh] bg-gradient-to-br from-zinc-950 via-zinc-900 to-[#1a0a2e] text-white rounded-3xl p-6 md:p-10 -m-2 relative overflow-hidden">
      <div className="absolute inset-0 opacity-40" style={{
        background: "radial-gradient(circle at 30% 20%, rgba(236,72,153,0.3), transparent 50%), radial-gradient(circle at 70% 80%, rgba(255,107,53,0.3), transparent 50%)"
      }}/>

      <div className="relative max-w-2xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <button onClick={() => nav(-1)} data-testid="boss-exit-btn" className="w-10 h-10 rounded-full bg-white/10 grid place-items-center hover:bg-white/20">
            <X className="w-5 h-5"/>
          </button>
          <div className="flex-1 mx-4 h-2 rounded-full bg-white/10 overflow-hidden">
            <div className="h-full bg-gradient-to-r from-[#FBBF24] via-[#EC4899] to-[#FF6B35] transition-all"
              style={{ width: `${((idx+1)/data.questions.length)*100}%`}}/>
          </div>
          <span className="font-bold tabular-nums text-[#FBBF24]">{idx+1}/{data.questions.length}</span>
        </div>

        <div className="flex items-center gap-3 mb-6">
          <Skull className="w-6 h-6 text-[#EC4899]"/>
          <div>
            <p className="text-[10px] uppercase tracking-[0.3em] font-bold text-[#EC4899]">Boss Battle</p>
            <h1 className="font-[Outfit] font-black text-2xl tracking-tight">{data.chapter.title}</h1>
          </div>
        </div>

        <div data-testid="boss-question" className="bg-white/5 backdrop-blur-xl border border-white/15 rounded-3xl p-6 md:p-8">
          <h2 className="font-[Outfit] font-bold text-xl md:text-2xl tracking-tight mb-6">{q.content.question}</h2>
          <div className="grid gap-3">
            {q.content.options.map((opt, i) => {
              const picked = answers[idx];
              const isPicked = picked === i;
              const isCorrect = picked !== undefined && i === q.content.correct;
              const isWrong = picked !== undefined && isPicked && i !== q.content.correct;
              let cls = "border-white/15 bg-white/5 hover:border-white/40";
              if (isCorrect) cls = "border-[#10B981] bg-[#10B981]/20";
              else if (isWrong) cls = "border-[#EF4444] bg-[#EF4444]/20";
              return (
                <button key={i} data-testid={`boss-opt-${i}`} onClick={() => choose(i)} disabled={picked !== undefined}
                  className={`text-left px-5 py-4 rounded-2xl border-2 font-semibold transition flex justify-between items-center ${cls}`}>
                  <span>{opt}</span>
                  {isCorrect && <Check className="w-5 h-5 text-[#10B981]"/>}
                  {isWrong && <X className="w-5 h-5 text-[#EF4444]"/>}
                </button>
              );
            })}
          </div>
          {answers[idx] !== undefined && q.content.explanation && (
            <p className="mt-5 text-sm text-white/70 italic" data-testid="boss-explanation">{q.content.explanation}</p>
          )}
        </div>

        <div className="flex justify-end mt-6">
          <button onClick={next} disabled={answers[idx] === undefined} data-testid="btn-boss-next"
            className="px-7 py-3 rounded-2xl bg-[#FBBF24] hover:bg-[#F59E0B] text-zinc-900 font-[Outfit] font-bold tracking-tight inline-flex items-center gap-2 disabled:opacity-30 transition active:scale-[0.98]">
            {idx + 1 === data.questions.length ? "Finish battle" : "Next"}
            <Zap className="w-4 h-4"/>
          </button>
        </div>
      </div>
    </div>
  );
}
