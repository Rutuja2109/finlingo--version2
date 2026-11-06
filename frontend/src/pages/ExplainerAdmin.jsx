import React, { useCallback, useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import { api, formatApiError } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";

const today = () => { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`; };
const blank = () => ({ date: today(), headline: "", summary: "", p1: "", p2: "", why: "", term_word: "", term_meaning: "", quiz_question: "", o1: "", o2: "", o3: "", o4: "", quiz_correct: 0, quiz_explanation: "", source_name: "", source_url: "https://" });

// Admin-only: write and publish a news explainer for a date. Only publish after you have checked the facts against the source.
export default function ExplainerAdmin() {
  const { user } = useAuth();
  const [f, setF] = useState(blank());
  const [list, setList] = useState([]);
  const [msg, setMsg] = useState("");
  const load = useCallback(async () => { try { setList((await api.get("/explainer/admin")).data); } catch { /* not admin */ } }, []);
  useEffect(() => { load(); }, [load]);
  if (user && user.role !== "admin") return <Navigate to="/dashboard" replace />;

  const set = (k) => (e) => setF({ ...f, [k]: e.target.value });
  const save = async () => {
    setMsg("");
    const options = [f.o1, f.o2, f.o3, f.o4].filter((x) => x.trim());
    try {
      await api.post("/explainer/admin", {
        date: f.date, headline: f.headline, summary: f.summary, points: [f.p1, f.p2], why: f.why, term_word: f.term_word, term_meaning: f.term_meaning,
        quiz_question: f.quiz_question, quiz_options: options, quiz_correct: Number(f.quiz_correct), quiz_explanation: f.quiz_explanation,
        source_name: f.source_name, source_url: f.source_url,
      });
      setMsg(`Published for ${f.date}.`); setF(blank()); load();
    } catch (e) { setMsg(formatApiError(e)); }
  };
  const del = async (d) => { if (window.confirm(`Delete the explainer for ${d}?`)) { await api.delete(`/explainer/admin/${d}`); load(); } };

  const inp = "w-full border-2 border-zinc-200 rounded-xl px-3 py-2 text-sm mb-2 outline-none focus:border-[#FF6B35]";
  return (
    <div className="max-w-xl mx-auto pb-24" data-testid="explainer-admin">
      <h1 className="font-[Outfit] font-black text-2xl mb-1">News explainer (admin)</h1>
      <p className="text-[13px] text-zinc-500 mb-4">Write your own plain-words explainer about a real headline and link the source. Check every fact against the source before you publish. Publishing replaces the built-in idea of the day for that date.</p>
      <label className="text-[12px] font-bold text-zinc-500">Date shown</label>
      <input type="date" value={f.date} onChange={set("date")} className={inp} data-testid="ea-date" />
      <input value={f.headline} onChange={set("headline")} placeholder="Headline in your own words (10 to 140 characters)" className={inp} data-testid="ea-headline" />
      <textarea value={f.summary} onChange={set("summary")} rows={3} placeholder="In plain words (about 2 to 3 sentences)" className={inp} data-testid="ea-summary" />
      <input value={f.p1} onChange={set("p1")} placeholder="Point 1 (optional, a worked example helps)" className={inp} />
      <input value={f.p2} onChange={set("p2")} placeholder="Point 2 (optional)" className={inp} />
      <textarea value={f.why} onChange={set("why")} rows={2} placeholder="Why it matters to a young earner" className={inp} data-testid="ea-why" />
      <input value={f.term_word} onChange={set("term_word")} placeholder="Word to know" className={inp} data-testid="ea-word" />
      <input value={f.term_meaning} onChange={set("term_meaning")} placeholder="What it means" className={inp} data-testid="ea-meaning" />
      <input value={f.quiz_question} onChange={set("quiz_question")} placeholder="Quick-check question" className={inp} data-testid="ea-question" />
      {["o1", "o2", "o3", "o4"].map((k, i) => (
        <div key={k} className="flex items-center gap-2"><input type="radio" name="correct" checked={Number(f.quiz_correct) === i} onChange={() => setF({ ...f, quiz_correct: i })} aria-label={`Option ${i + 1} is correct`} />
          <input value={f[k]} onChange={set(k)} placeholder={`Option ${i + 1}${i < 3 ? "" : " (optional)"}`} className={inp} data-testid={`ea-${k}`} /></div>
      ))}
      <input value={f.quiz_explanation} onChange={set("quiz_explanation")} placeholder="Why the right answer is right" className={inp} data-testid="ea-explanation" />
      <input value={f.source_name} onChange={set("source_name")} placeholder="Source name (e.g. RBI press release)" className={inp} data-testid="ea-source-name" />
      <input value={f.source_url} onChange={set("source_url")} placeholder="https:// source link" className={inp} data-testid="ea-source-url" />
      <button onClick={save} data-testid="ea-save" className="w-full rounded-2xl py-3 bg-[#FF6B35] text-white font-[Outfit] font-black">Publish</button>
      {msg && <p className="text-[13px] mt-2" data-testid="ea-msg">{msg}</p>}

      <h2 className="font-[Outfit] font-black text-lg mt-6 mb-2">Published</h2>
      {list.length === 0 && <p className="text-[13px] text-zinc-500">Nothing yet. Until you publish one, learners see the built-in idea of the day.</p>}
      {list.map((x) => (
        <div key={x.date} className="flex items-center justify-between gap-2 bg-white border border-zinc-200 rounded-xl px-3 py-2 mb-2 text-sm">
          <span><b>{x.date}</b> · {x.headline}</span><button onClick={() => del(x.date)} className="text-red-600 font-bold text-[13px]">Delete</button>
        </div>
      ))}
    </div>
  );
}
