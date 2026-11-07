import React, { useEffect, useRef, useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { Flame, Zap, Coins, Settings, Trophy, Home, BookOpen, Award, Repeat, Sparkles, LineChart, Wallet, Flag } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import Logo from "@/components/Logo";
import ProStrip from "@/components/ProStrip";

export default function AppShell({ children }) {
  const { user, stats } = useAuth();
  const nav = useNavigate();
  const loc = useLocation();
  // Lessons and boss battles are full screen: no top bar or tab bar, so the question and the Continue button have room.
  const immersive = loc.pathname.startsWith("/concept") || loc.pathname.startsWith("/boss");

  const linkCls = (path) =>
    `flex items-center gap-1.5 px-2 xl:px-3 py-2 rounded-xl text-[13px] xl:text-sm font-semibold whitespace-nowrap transition-all duration-200 ${
      loc.pathname.startsWith(path)
        ? "bg-[#FF6B35]/10 text-[#FF6B35]"
        : "text-zinc-500 hover:text-zinc-900 dark:hover:text-white"
    }`;

  return (
    <div className="min-h-screen bg-[#FAFAFA] text-zinc-900 font-[Manrope]">
      {/* Top bar */}
      {!immersive && (
      <header
        data-testid="app-header"
        className="sticky top-0 z-40 backdrop-blur-xl bg-white/70 border-b border-zinc-200"
      >
        <div className="max-w-6xl mx-auto px-3 sm:px-5 h-16 flex items-center justify-between gap-2">
          <Link to="/dashboard" className="flex items-center gap-2.5" data-testid="brand-logo">
            <Logo size={36} />
            <span className="hidden sm:inline font-[Outfit] font-black text-xl tracking-tight">FinLearn</span>
          </Link>

          <nav className="hidden lg:flex items-center gap-0.5 xl:gap-1">
            <Link to="/dashboard" className={linkCls("/dashboard")} data-testid="nav-dashboard">
              <Home className="w-4 h-4" /> Home
            </Link>
            <Link to="/courses" className={linkCls("/courses")} data-testid="nav-courses">
              <BookOpen className="w-4 h-4" /> Courses
            </Link>
            <Link to="/practice" className={linkCls("/practice")} data-testid="nav-practice">
              <LineChart className="w-4 h-4" /> Practice
            </Link>
            <Link to="/money" className={linkCls("/money")} data-testid="nav-money">
              <Wallet className="w-4 h-4" /> My money
            </Link>
            <Link to="/missions" className={linkCls("/missions")} data-testid="nav-missions">
              <Flag className="w-4 h-4" /> Missions
            </Link>
            <Link to="/revise" className={linkCls("/revise")} data-testid="nav-revise">
              <Repeat className="w-4 h-4" /> Revise
            </Link>
            <Link to="/leaderboard" className={linkCls("/leaderboard")} data-testid="nav-leaderboard">
              <Trophy className="w-4 h-4" /> Leaderboard
            </Link>
            <Link to="/achievements" className={linkCls("/achievements")} data-testid="nav-achievements">
              <Award className="w-4 h-4" /> Achievements
            </Link>
            {/* nav-admin: render placeholder until user hydrates to avoid flash */}
            {user && user.role === "admin" ? (
              <>
                <Link to="/admin/explainers" className={linkCls("/admin/explainers")} data-testid="nav-admin-explainers">
                  <Flag className="w-4 h-4" /> Explainers
                </Link>
                <Link to="/admin" className={linkCls("/admin")} data-testid="nav-admin">
                  <Sparkles className="w-4 h-4" /> AI Lab
                </Link>
              </>
            ) : null}
          </nav>

          <div className="flex items-center gap-1.5 sm:gap-3">
            <Stat icon={Flame} value={stats?.streak_days || 0} color="#FF5C00" testid="stat-streak" />
            <Stat icon={Zap} value={stats?.total_xp || 0} color="#FBBF24" testid="stat-xp" />
            <Stat icon={Coins} value={stats?.coins || 0} color="#F59E0B" testid="stat-coins" />
            <Link
              to="/account"
              data-testid="btn-account"
              aria-label="Account and settings"
              className="w-9 h-9 grid place-items-center rounded-full bg-zinc-100 hover:bg-zinc-200 transition"
              title="Account"
            >
              <Settings className="w-4 h-4" />
            </Link>
          </div>
        </div>
        <ProStrip />
      </header>
      )}

      <main className={`max-w-6xl mx-auto px-5 ${immersive ? "py-3" : "py-8"}`}>{children}</main>

      {/* Mobile nav */}
      {!immersive && (
      <nav className="lg:hidden fixed bottom-0 inset-x-0 z-40 bg-white/90 backdrop-blur-xl border-t border-zinc-200">
        <div className="max-w-md mx-auto grid grid-cols-5">
          {[
            { to: "/dashboard", Icon: Home, label: "Home", t: "mnav-dashboard" },
            { to: "/courses", Icon: BookOpen, label: "Courses", t: "mnav-courses" },
            { to: "/practice", Icon: LineChart, label: "Practice", t: "mnav-practice" },
            { to: "/money", Icon: Wallet, label: "Money", t: "mnav-money" },
            { to: "/leaderboard", Icon: Trophy, label: "Rank", t: "mnav-leaderboard" },
          ].map(({ to, Icon, label, t }) => (
            <Link key={to} to={to} data-testid={t}
              className={`flex flex-col items-center gap-1 py-2.5 text-xs font-semibold ${
                loc.pathname.startsWith(to) ? "text-[#FF6B35]" : "text-zinc-500"
              }`}>
              <Icon className="w-5 h-5" />
              {label}
            </Link>
          ))}
        </div>
      </nav>
      )}
    </div>
  );
}

function Stat({ icon: Icon, value, color, testid }) {
  const prevRef = useRef(value);
  const [delta, setDelta] = useState(null);
  const [pulse, setPulse] = useState(false);

  useEffect(() => {
    const prev = prevRef.current;
    if (value > prev) {
      const diff = value - prev;
      setDelta(`+${diff}`);
      setPulse(true);
      const t1 = setTimeout(() => setDelta(null), 1800);
      const t2 = setTimeout(() => setPulse(false), 600);
      prevRef.current = value;
      return () => { clearTimeout(t1); clearTimeout(t2); };
    }
    prevRef.current = value;
  }, [value]);

  return (
    <div className="relative">
      <div
        data-testid={testid}
        className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-full transition-all duration-300 ${
          pulse ? "bg-zinc-200 scale-110" : "bg-zinc-100"
        }`}
      >
        <Icon className="w-4 h-4" style={{ color }} />
        <span className="font-[Outfit] font-bold text-sm tabular-nums">{value}</span>
      </div>
      {delta && (
        <span
          className="absolute -top-5 left-1/2 -translate-x-1/2 text-xs font-black tabular-nums animate-bounce-up pointer-events-none whitespace-nowrap"
          style={{ color }}
        >
          {delta}
        </span>
      )}
    </div>
  );
}
