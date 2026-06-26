import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import Lumi from "@/components/Lumi";
import { ArrowRight, Sparkles, Target, Flame, Repeat } from "lucide-react";

const ICONS_SVG = {
  Shield: "M12 2l8 4v6c0 5-3.5 9-8 10-4.5-1-8-5-8-10V6l8-4z",
  TrendingUp: "M3 17l6-6 4 4 8-8M21 7h-5M21 7v5",
  Briefcase: "M3 7h18v13H3zM8 7V5a2 2 0 012-2h4a2 2 0 012 2v2",
};

export default function Dashboard() {
  const { user, stats } = useAuth();
  const [courses, setCourses] = useState([]);
  const [enrolled, setEnrolled] = useState([]);
  const [dueCount, setDueCount] = useState(0);
  const [busy, setBusy] = useState({});

  useEffect(() => {
    (async () => {
      const [c, e, r] = await Promise.all([
        api.get("/courses"),
        api.get("/enrollments/me"),
        api.get("/revisions/due").catch(() => ({ data: [] })),
      ]);
      setCourses(c.data);
      setEnrolled(e.data);
      setDueCount((r.data || []).length);
    })();
  }, []);

  const enroll = async (courseId) => {
    setBusy((b) => ({ ...b, [courseId]: true }));
    await api.post("/enrollments", { course_id: courseId });
    const e = await api.get("/enrollments/me");
    setEnrolled(e.data);
    setBusy((b) => ({ ...b, [courseId]: false }));
  };

  const isEnrolled = (id) => enrolled.some((c) => c.id === id);
  const xpToNext = 100 - (stats?.total_xp || 0) % 100;
  const dailyGoal = 30;
  const todayXp = Math.min(stats?.total_xp || 0, dailyGoal);
  const dailyPct = Math.min(100, ((todayXp % dailyGoal) / dailyGoal) * 100);

  return (
    <div className="pb-24">
      {/* Hero */}
      <section className="bg-gradient-to-br from-[#FF6B35] via-[#FF8A4C] to-[#EC4899] rounded-3xl p-7 md:p-10 text-white mb-8 relative overflow-hidden">
        <div className="absolute -right-10 -top-10 opacity-40"><Lumi size={220} mood="cheer"/></div>
        <div className="relative">
          <p className="uppercase tracking-[0.25em] text-xs font-bold text-white/85 mb-2">
            <Sparkles className="w-3.5 h-3.5 inline -mt-0.5 mr-1"/>
            {greeting()}, {user?.name?.split(" ")[0] || "learner"}
          </p>
          <h1 className="font-[Outfit] font-black text-3xl md:text-5xl tracking-tighter leading-tight max-w-2xl">
            {(stats?.streak_days || 0) > 0
              ? <>You're on a <span className="underline decoration-white/40">{stats.streak_days}-day streak</span>. Keep it alive.</>
              : "Let's start your streak today."}
          </h1>
          <div className="mt-6 grid sm:grid-cols-3 gap-3 max-w-2xl">
            <HeroStat label="Level" value={stats?.level || 1} sub={`${xpToNext} XP to next`}/>
            <HeroStat label="Total XP" value={stats?.total_xp || 0} sub={`Lifetime points`}/>
            <HeroStat label="Mastered" value={stats?.concepts_mastered || 0} sub={`Concepts`}/>
          </div>
        </div>
      </section>

      {/* Daily goal + Continue */}
      <section className="grid md:grid-cols-3 gap-5 mb-10">
        <div className="md:col-span-2 bg-white border border-zinc-200 rounded-3xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <p className="uppercase tracking-[0.2em] text-xs font-bold text-zinc-500">Daily Goal</p>
              <h3 className="font-[Outfit] font-black text-2xl tracking-tight">Earn {dailyGoal} XP today</h3>
            </div>
            <Target className="w-6 h-6 text-[#FF6B35]"/>
          </div>
          <div className="h-3 rounded-full bg-zinc-100 overflow-hidden">
            <div className="h-full bg-gradient-to-r from-[#FF6B35] to-[#EC4899] transition-all duration-700"
              style={{ width: `${dailyPct}%` }} data-testid="daily-progress-bar"/>
          </div>
          <p className="text-sm text-zinc-500 mt-2">{Math.round(dailyPct)}% complete</p>

          {dueCount > 0 && (
            <Link to="/revise" data-testid="revise-cta"
              className="mt-5 flex items-center justify-between gap-3 p-4 rounded-2xl bg-gradient-to-r from-[#2563EB]/10 to-[#EC4899]/10 border border-[#2563EB]/20 hover:border-[#2563EB]/50 transition">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-[#2563EB] grid place-items-center text-white">
                  <Repeat className="w-5 h-5"/>
                </div>
                <div>
                  <p className="font-[Outfit] font-bold">Revision queue ready</p>
                  <p className="text-xs text-zinc-500">{dueCount} concept{dueCount>1?"s":""} due for review</p>
                </div>
              </div>
              <ArrowRight className="w-5 h-5 text-[#2563EB]"/>
            </Link>
          )}
        </div>
        <div className="bg-white border border-zinc-200 rounded-3xl p-6 flex flex-col items-center text-center">
          <Flame className="w-8 h-8 text-[#FF5C00] mb-2"/>
          <p className="font-[Outfit] font-black text-4xl tabular-nums">{stats?.streak_days || 0}</p>
          <p className="text-sm text-zinc-500">Day streak</p>
          <p className="text-xs text-zinc-400 mt-2">Practice every day to keep the flame.</p>
        </div>
      </section>

      {/* Courses */}
      <section>
        <div className="flex items-end justify-between mb-5">
          <h2 className="font-[Outfit] font-black text-2xl tracking-tight">Your courses</h2>
          <Link to="/courses" data-testid="link-all-courses" className="text-sm font-semibold text-[#FF6B35] hover:underline">
            Browse all →
          </Link>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {courses.map((c) => (
            <CourseCard key={c.id} c={c}
              enrolled={isEnrolled(c.id)}
              busy={!!busy[c.id]}
              onEnroll={() => enroll(c.id)}/>
          ))}
        </div>
      </section>
    </div>
  );
}

function greeting() {
  const h = new Date().getHours();
  if (h < 12) return "Good morning";
  if (h < 17) return "Good afternoon";
  return "Good evening";
}

function HeroStat({ label, value, sub }) {
  return (
    <div className="bg-white/15 backdrop-blur-sm rounded-2xl p-4 border border-white/20">
      <p className="uppercase tracking-[0.2em] text-[10px] font-bold text-white/80">{label}</p>
      <p className="font-[Outfit] font-black text-3xl tabular-nums">{value}</p>
      <p className="text-xs text-white/75">{sub}</p>
    </div>
  );
}

function CourseCard({ c, enrolled, busy, onEnroll }) {
  return (
    <div data-testid={`course-card-${c.slug}`}
      className="group bg-white border border-zinc-200 rounded-3xl p-6 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
      <div className="flex items-start justify-between mb-4">
        <div className="w-12 h-12 rounded-2xl grid place-items-center text-white"
          style={{ background: c.color }}>
          <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
            <path d={ICONS_SVG[c.icon] || ICONS_SVG.Shield}/>
          </svg>
        </div>
        <span className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-400">{c.certification}</span>
      </div>
      <h3 className="font-[Outfit] font-black text-xl tracking-tight">{c.name}</h3>
      <p className="text-sm text-zinc-500 mt-1">{c.title}</p>
      <p className="text-sm text-zinc-600 mt-3 line-clamp-2">{c.description}</p>
      <div className="mt-5">
        {enrolled ? (
          <Link to={`/learn/${c.id}`} data-testid={`btn-continue-${c.slug}`}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-zinc-900 text-white text-sm font-bold hover:bg-zinc-800 transition">
            Continue <ArrowRight className="w-4 h-4"/>
          </Link>
        ) : (
          <button onClick={onEnroll} disabled={busy} data-testid={`btn-enroll-${c.slug}`}
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold transition active:scale-95 disabled:opacity-60"
            style={{ background: `${c.color}1A`, color: c.color }}>
            {busy ? "Enrolling…" : "Start course"} <ArrowRight className="w-4 h-4"/>
          </button>
        )}
      </div>
    </div>
  );
}
