import React from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { Flame, Zap, Coins, LogOut, Trophy, Home, BookOpen, Award, Repeat, Sparkles } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import Lumi from "@/components/Lumi";

export default function AppShell({ children }) {
  const { user, stats, logout } = useAuth();
  const nav = useNavigate();
  const loc = useLocation();

  const linkCls = (path) =>
    `flex items-center gap-2 px-3 py-2 rounded-xl text-sm font-semibold transition-all duration-200 ${
      loc.pathname.startsWith(path)
        ? "bg-[#FF6B35]/10 text-[#FF6B35]"
        : "text-zinc-500 hover:text-zinc-900 dark:hover:text-white"
    }`;

  return (
    <div className="min-h-screen bg-[#FAFAFA] text-zinc-900 font-[Manrope]">
      {/* Top bar */}
      <header
        data-testid="app-header"
        className="sticky top-0 z-40 backdrop-blur-xl bg-white/70 border-b border-zinc-200"
      >
        <div className="max-w-6xl mx-auto px-5 h-16 flex items-center justify-between">
          <Link to="/dashboard" className="flex items-center gap-2.5" data-testid="brand-logo">
            <Lumi size={36} />
            <span className="font-[Outfit] font-black text-xl tracking-tight">FinLingo</span>
          </Link>

          <nav className="hidden md:flex items-center gap-1">
            <Link to="/dashboard" className={linkCls("/dashboard")} data-testid="nav-dashboard">
              <Home className="w-4 h-4" /> Home
            </Link>
            <Link to="/courses" className={linkCls("/courses")} data-testid="nav-courses">
              <BookOpen className="w-4 h-4" /> Courses
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
            {user?.role === "admin" && (
              <Link to="/admin" className={linkCls("/admin")} data-testid="nav-admin">
                <Sparkles className="w-4 h-4" /> AI Lab
              </Link>
            )}
          </nav>

          <div className="flex items-center gap-3">
            <Stat icon={Flame} value={stats?.streak_days || 0} color="#FF5C00" testid="stat-streak" />
            <Stat icon={Zap} value={stats?.total_xp || 0} color="#FBBF24" testid="stat-xp" />
            <Stat icon={Coins} value={stats?.coins || 0} color="#F59E0B" testid="stat-coins" />
            <button
              onClick={async () => { await logout(); window.location.href = "/"; }}
              data-testid="btn-logout"
              className="ml-2 w-9 h-9 grid place-items-center rounded-full bg-zinc-100 hover:bg-zinc-200 transition"
              title={user?.name}
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-5 py-8">{children}</main>

      {/* Mobile nav */}
      <nav className="md:hidden fixed bottom-0 inset-x-0 z-40 bg-white/90 backdrop-blur-xl border-t border-zinc-200">
        <div className="max-w-md mx-auto grid grid-cols-4">
          {[
            { to: "/dashboard", Icon: Home, label: "Home", t: "mnav-dashboard" },
            { to: "/courses", Icon: BookOpen, label: "Courses", t: "mnav-courses" },
            { to: "/leaderboard", Icon: Trophy, label: "Rank", t: "mnav-leaderboard" },
            { to: "/achievements", Icon: Award, label: "Awards", t: "mnav-achievements" },
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
    </div>
  );
}

function Stat({ icon: Icon, value, color, testid }) {
  return (
    <div
      data-testid={testid}
      className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-full bg-zinc-100"
    >
      <Icon className="w-4 h-4" style={{ color }} />
      <span className="font-[Outfit] font-bold text-sm tabular-nums">{value}</span>
    </div>
  );
}
