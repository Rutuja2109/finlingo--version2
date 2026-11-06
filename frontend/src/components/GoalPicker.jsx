import React, { useState } from "react";
import { api, formatApiError } from "@/lib/api";
import { GOAL_CHOICES } from "@/lib/streak";
import Lumi from "@/components/Lumi";
import { Clock } from "lucide-react";

// Bottom sheet that lets the learner pick a daily time goal (shown once after sign-up, and from the daily goal card).
export default function GoalPicker({ current, onSaved, onClose }) {
  const [picked, setPicked] = useState(current || 5);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");

  const save = async () => {
    setBusy(true); setErr("");
    try {
      await api.put("/me/goal", { minutes: picked });
      onSaved(picked);
    } catch (e) {
      setErr(formatApiError(e));
      setBusy(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/40 flex items-end md:items-center justify-center" role="dialog" aria-modal="true" aria-label="Choose your daily goal">
      <div className="w-full max-w-md bg-white rounded-t-3xl md:rounded-3xl p-6 pb-8 fade-up">
        <div className="flex items-center gap-3 mb-4">
          <Lumi size={56} mood="cheer" />
          <div>
            <h2 className="font-[Outfit] font-black text-2xl tracking-tight leading-tight">How much time can you give each day?</h2>
            <p className="text-sm text-zinc-500">You can change this any time.</p>
          </div>
        </div>
        <div className="space-y-3">
          {GOAL_CHOICES.map((g) => (
            <button key={g.minutes} onClick={() => setPicked(g.minutes)} data-testid={`goal-${g.minutes}`}
              className={`w-full text-left px-4 py-3.5 rounded-2xl border-2 transition flex items-center gap-3 ${
                picked === g.minutes ? "border-[#FF6B35] bg-[#FF6B35]/8" : "border-zinc-200 hover:border-zinc-400"
              }`}>
              <span className="w-11 h-11 rounded-xl bg-zinc-100 grid place-items-center shrink-0"><Clock className="w-5 h-5 text-[#FF6B35]" /></span>
              <span className="flex-1">
                <span className="block font-[Outfit] font-extrabold">{g.minutes} min a day <span className="text-zinc-500 font-semibold text-sm">· {g.label}</span></span>
                <span className="block text-xs text-zinc-500">{g.note} Goal: {g.xp} XP.</span>
              </span>
            </button>
          ))}
        </div>
        {err && <p className="text-sm text-red-600 mt-3">{err}</p>}
        <div className="flex gap-3 mt-5">
          {onClose && (
            <button onClick={onClose} className="px-5 py-3 rounded-2xl bg-zinc-100 font-[Outfit] font-bold">Later</button>
          )}
          <button onClick={save} disabled={busy} data-testid="goal-save"
            className="flex-1 py-3 rounded-2xl bg-[#FF6B35] hover:bg-[#FF5618] text-white font-[Outfit] font-bold disabled:opacity-60">
            {busy ? "Saving…" : "Set my goal"}
          </button>
        </div>
      </div>
    </div>
  );
}
