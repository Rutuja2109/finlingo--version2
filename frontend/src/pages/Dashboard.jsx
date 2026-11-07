import React, { useEffect, useState } from "react";
import { courseSubtitle } from "@/lib/course";
import { Link, useNavigate } from "react-router-dom";
import { api } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import Lumi from "@/components/Lumi";
import { ArrowRight, Sparkles, Target, Play, Crown } from "lucide-react";
import { trackCourseEnrolled } from "@/lib/firebase";
import GoalPicker from "@/components/GoalPicker";
import DailyQuests from "@/components/DailyQuests";
import TodayStrip from "@/components/TodayStrip";
import StreakWeek from "@/components/StreakWeek";
import TrialCard from "@/components/TrialCard";
import MilestoneModal from "@/components/MilestoneModal";
import ProFeatures from "@/components/ProFeatures";
import { streakState } from "@/lib/streak";

const ICONS_SVG = {
  Wallet: "M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4",
  Bitcoin: "M11.767 19.089c4.924.868 6.14-6.025 1.216-6.894m-1.216 6.894L5.86 18.047m5.908 1.042-.347 1.97m1.563-8.864c4.924.869 6.14-6.025 1.215-6.893m-1.215 6.893-3.94-.694m5.155-6.2L8.29 4.26m5.908 1.042.348-1.97M7.48 20.364l3.126-17.727",
  Calculator: "M6 2h12a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zM8 6h8M16 14v4M16 10h.01M12 10h.01M8 10h.01M12 14h.01M8 14h.01M12 18h.01M8 18h.01",
  Shield: "M12 2l8 4v6c0 5-3.5 9-8 10-4.5-1-8-5-8-10V6l8-4z",
  TrendingUp: "M3 17l6-6 4 4 8-8M21 7h-5M21 7v5",
  Briefcase: "M3 7h18v13H3zM8 7V5a2 2 0 012-2h4a2 2 0 012 2v2",
};

export default function Dashboard() {
  const { user, stats, refreshStats } = useAuth();
  const nav = useNavigate();
  const [courses, setCourses] = useState([]);
  const [enrolled, setEnrolled] = useState([]);
  const [next, setNext] = useState(null); // the lesson to continue with
  const [busy, setBusy] = useState({});
  const [starting, setStarting] = useState(false);
  const [showGoal, setShowGoal] = useState(false);

  // Ask for a daily goal once, when the learner has not chosen one yet.
  useEffect(() => {
    let later = false;
    try { later = !!sessionStorage.getItem("fl_goal_later"); } catch { /* storage unavailable */ }
    if (stats && stats.daily_goal_minutes == null && !later) setShowGoal(true);
  }, [stats]);

  useEffect(() => {
    (async () => {
      const [c, e, n] = await Promise.all([
        api.get("/courses"),
        api.get("/enrollments/me"),
        api.get("/progress/next").catch(() => ({ data: null })),
      ]);
      setCourses(c.data);
      setEnrolled(e.data);
      setNext(n.data);
    })();
  }, []);

  const enroll = async (courseId) => {
    setBusy((b) => ({ ...b, [courseId]: true }));
    await api.post("/enrollments", { course_id: courseId });
    const course = courses.find((c) => c.id === courseId);
    trackCourseEnrolled({ courseId, courseName: course?.name || "" });
    const e = await api.get("/enrollments/me");
    setEnrolled(e.data);
    setBusy((b) => ({ ...b, [courseId]: false }));
  };

  // The big button: open the next lesson (enrolling first if needed), or go to the paywall if that lesson is Pro.
  const startNext = async () => {
    if (!next || next.all_done || starting) return;
    if (next.locked) { nav("/pro?from=lessons"); return; }
    setStarting(true);
    if (!next.enrolled) {
      try { await api.post("/enrollments", { course_id: next.course.id }); trackCourseEnrolled({ courseId: next.course.id, courseName: next.course.name }); } catch { /* enrolling is a convenience */ }
    }
    nav(`/concept/${next.concept.id}`);
  };

  const isEnrolled = (id) => enrolled.some((c) => c.id === id);
  const xpToNext = 100 - (stats?.total_xp || 0) % 100;
  const dailyGoal = stats?.daily_goal_xp || 20;
  const goalMinutes = stats?.daily_goal_minutes || 5;
  const todayXp = stats?.xp_today || 0;
  const dailyPct = Math.min(100, (todayXp / dailyGoal) * 100);
  const st = streakState(stats, goalMinutes);
  const hasNext = next && !next.all_done;

  return (
    <div className="pb-24">
      <MilestoneModal />
      {showGoal && (
        <GoalPicker
          current={stats?.daily_goal_minutes}
          onClose={() => { try { sessionStorage.setItem("fl_goal_later", "1"); } catch { /* ignore */ } setShowGoal(false); }}
          onSaved={async () => { await refreshStats(); setShowGoal(false); }}
        />
      )}

      {/* Hero: greeting, how Lumi feels, and the one thing to do next */}
      <section className={`bg-gradient-to-br ${st.mood === "angry" ? "from-[#E5484D] via-[#FF6B35] to-[#EC4899]" : "from-[#FF6B35] via-[#FF8A4C] to-[#EC4899]"} rounded-3xl p-5 md:p-10 text-white mb-6 md:mb-8 relative overflow-hidden`}>
        <div className="absolute -right-1 top-1 md:right-4 md:top-3 pointer-events-none">
          <Lumi size={96} mood={st.mood}/>
        </div>
        <div className="relative">
          <p className="uppercase tracking-[0.2em] text-[11px] md:text-xs font-bold text-white/95 mb-2">
            <Sparkles className="w-3.5 h-3.5 inline -mt-0.5 mr-1"/>
            {greeting()}, {user?.name?.split(" ")[0] || "learner"}
          </p>
          <h1 className="font-[Outfit] font-black text-2xl md:text-5xl tracking-tight leading-tight max-w-[72%] md:max-w-2xl">
            {st.headline}
          </h1>
          <p className="text-white/95 text-sm mt-1.5 max-w-[62%] md:max-w-xl">{st.sub}</p>

          {hasNext ? (
            <button onClick={startNext} disabled={starting} data-testid="hero-continue"
              className="mt-4 w-full max-w-xl text-left rounded-2xl bg-white text-zinc-900 p-3.5 flex items-center gap-3 shadow-lg active:scale-[0.98] transition disabled:opacity-80">
              <span className="w-11 h-11 rounded-xl grid place-items-center text-white shrink-0" style={{ background: next.locked ? "#18181B" : (next.course.color || "#10B981") }}>
                {next.locked ? <Crown className="w-5 h-5" /> : <Play className="w-5 h-5" fill="currentColor" />}
              </span>
              <span className="flex-1 min-w-0">
                <span className="block text-[11px] font-bold tracking-widest uppercase text-zinc-600 truncate" data-testid="hero-continue-label">
                  {next.locked ? "Next lesson · Pro" : next.done === 0 ? "Start" : "Continue"} · {next.course.name}
                </span>
                <span className="block font-[Outfit] font-extrabold text-[16px] leading-tight line-clamp-2" data-testid="hero-continue-title">{next.concept.title}</span>
                <span className="mt-1.5 block h-1.5 rounded-full bg-zinc-100 overflow-hidden">
                  <span className="block h-full rounded-full" style={{ width: `${Math.round((next.done / Math.max(1, next.total)) * 100)}%`, background: next.course.color || "#10B981" }} />
                </span>
              </span>
              <ArrowRight className="w-5 h-5 text-zinc-500 shrink-0" />
            </button>
          ) : (
            <Link to="/courses" data-testid="hero-browse" className="mt-4 inline-flex items-center gap-2 rounded-2xl bg-white text-zinc-900 font-[Outfit] font-extrabold px-4 py-3 shadow-lg">
              Browse courses <ArrowRight className="w-4 h-4" />
            </Link>
          )}
          <p className="text-[12px] text-white/95 mt-3 font-semibold">Level {stats?.level || 1} · {xpToNext} XP to the next level</p>
        </div>
      </section>

      <TodayStrip />
      <TrialCard />
      <ProFeatures />
      <StreakWeek />

      {/* Daily goal */}
      <section className="bg-white border border-zinc-200 rounded-3xl p-4 mb-6" data-testid="daily-goal">
        <div className="flex items-center justify-between mb-2.5">
          <div>
            <p className="uppercase tracking-[0.18em] text-[10.5px] font-bold text-zinc-600">Daily goal</p>
            <h3 className="font-[Outfit] font-black text-xl tracking-tight">Earn {dailyGoal} XP today</h3>
            <button onClick={() => setShowGoal(true)} data-testid="change-goal" className="text-xs font-bold text-[#FF6B35] mt-0.5">{goalMinutes} min a day · Change</button>
          </div>
          <Target className="w-6 h-6 text-[#FF6B35]"/>
        </div>
        <div className="h-3 rounded-full bg-zinc-100 overflow-hidden">
          <div className="h-full bg-gradient-to-r from-[#FF6B35] to-[#EC4899] transition-all duration-700" style={{ width: `${dailyPct}%` }} data-testid="daily-progress-bar"/>
        </div>
        <p className="text-sm text-zinc-600 mt-2">{Math.min(todayXp, dailyGoal)} / {dailyGoal} XP today</p>
      </section>

      <DailyQuests />

      {/* Courses */}
      <section>
        <div className="flex items-end justify-between mb-4">
          <h2 className="font-[Outfit] font-black text-2xl tracking-tight">Your courses</h2>
          <Link to="/courses" data-testid="link-all-courses" className="text-sm font-semibold text-[#FF6B35] hover:underline">
            All {courses.length || ""} courses →
          </Link>
        </div>

        {courses.filter((c) => isEnrolled(c.id)).length > 0 ? (
          <div className="space-y-4">
            {courses.filter((c) => isEnrolled(c.id)).map((c) => (
              <Link key={c.id} to={`/learn/${c.id}`} data-testid={`btn-continue-${c.slug}`}
                className="flex items-center gap-4 rounded-3xl p-5 text-white relative overflow-hidden transition-all active:scale-[0.98] shadow-lg"
                style={{ background: `linear-gradient(135deg, ${c.color}ee, ${c.color}99)` }}>
                <div className="absolute inset-0 opacity-10"
                  style={{ backgroundImage: "radial-gradient(circle, white 1px, transparent 1px)", backgroundSize: "20px 20px" }} />
                <div className="relative w-14 h-14 rounded-2xl bg-white/20 grid place-items-center shrink-0">
                  <svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="white" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                    <path d={ICONS_SVG[c.icon] || ICONS_SVG.Shield}/>
                  </svg>
                </div>
                <div className="relative flex-1 min-w-0">
                  <p className="text-[10px] uppercase tracking-[0.25em] font-bold text-white/85">{c.certification}</p>
                  <p className="font-[Outfit] font-black text-xl tracking-tight leading-tight">{c.name}</p>
                  <p className="text-sm text-white/90 mt-0.5 truncate">{courseSubtitle(c)}</p>
                </div>
                <ArrowRight className="relative w-5 h-5 text-white shrink-0"/>
              </Link>
            ))}
          </div>
        ) : (
          <div className="space-y-3">
            {courses.slice(0, 1).map((c) => (
              <div key={c.id} className="rounded-3xl border-2 p-5 flex items-center gap-4 transition-all"
                style={{ borderColor: `${c.color}40`, background: `${c.color}08` }}>
                <div className="w-14 h-14 rounded-2xl grid place-items-center shrink-0 text-white"
                  style={{ background: `linear-gradient(135deg, ${c.color}, ${c.color}bb)` }}>
                  <svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="white" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                    <path d={ICONS_SVG[c.icon] || ICONS_SVG.Shield}/>
                  </svg>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-[Outfit] font-black text-xl tracking-tight">{c.name}</p>
                  <p className="text-sm text-zinc-600">{courseSubtitle(c)}</p>
                </div>
                <button onClick={() => enroll(c.id)} disabled={!!busy[c.id]}
                  data-testid={`btn-enroll-${c.slug}`}
                  className="px-4 py-2.5 rounded-xl text-sm font-bold transition active:scale-95 disabled:opacity-60 shrink-0"
                  style={{ background: `${c.color}20`, color: c.color }}>
                  {busy[c.id] ? "…" : "Begin"}
                </button>
              </div>
            ))}
          </div>
        )}
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
