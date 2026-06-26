import React from "react";
import "@/App.css";
import "@/index.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "@/context/AuthContext";
import AppShell from "@/components/AppShell";
import Landing from "@/pages/Landing";
import AuthPage from "@/pages/AuthPage";
import Dashboard from "@/pages/Dashboard";
import Courses from "@/pages/Courses";
import CoursePath from "@/pages/CoursePath";
import LessonPlayer from "@/pages/LessonPlayer";
import Leaderboard from "@/pages/Leaderboard";
import Achievements from "@/pages/Achievements";

function Protected({ children }) {
  const { user } = useAuth();
  if (user === null) {
    return <div className="min-h-screen grid place-items-center text-zinc-500 font-[Manrope]">Loading…</div>;
  }
  if (!user) return <Navigate to="/login" replace />;
  return <AppShell>{children}</AppShell>;
}

function PublicOnly({ children }) {
  const { user } = useAuth();
  if (user) return <Navigate to="/dashboard" replace />;
  return children;
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<PublicOnly><Landing/></PublicOnly>}/>
          <Route path="/login" element={<PublicOnly><AuthPage mode="login"/></PublicOnly>}/>
          <Route path="/signup" element={<PublicOnly><AuthPage mode="signup"/></PublicOnly>}/>
          <Route path="/dashboard" element={<Protected><Dashboard/></Protected>}/>
          <Route path="/courses" element={<Protected><Courses/></Protected>}/>
          <Route path="/learn/:courseId" element={<Protected><CoursePath/></Protected>}/>
          <Route path="/concept/:conceptId" element={<Protected><LessonPlayer/></Protected>}/>
          <Route path="/leaderboard" element={<Protected><Leaderboard/></Protected>}/>
          <Route path="/achievements" element={<Protected><Achievements/></Protected>}/>
          <Route path="*" element={<Navigate to="/" replace/>}/>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
