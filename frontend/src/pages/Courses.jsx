import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "@/lib/api";
import { Lock, ArrowRight, Check, Star, ChevronDown, ChevronUp } from "lucide-react";
import { trackCourseEnrolled } from "@/lib/firebase";
import Lumi from "@/components/Lumi";

const ICONS_SVG = {
  Shield: "M12 2l8 4v6c0 5-3.5 9-8 10-4.5-1-8-5-8-10V6l8-4z",
  TrendingUp: "M3 17l6-6 4 4 8-8M21 7h-5M21 7v5",
  Briefcase: "M3 7h18v13H3zM8 7V5a2 2 0 012-2h4a2 2 0 012 2v2",
};

const COMING_SOON = [
  { name: "CFA Level 1", title: "Chartered Financial Analyst", color: "#2563EB", icon: "TrendingUp" },
  { name: "FRM Part 1", title: "Financial Risk Manager", color: "#7C3AED", icon: "Shield" },
  { name: "PMP", title: "Project Management Professional", color: "#059669", icon: "Briefcase" },
];

export default function Courses() {
  const nav = useNavigate();
  const [courses, setCourses] = useState([]);
  const [enrolled, setEnrolled] = useState([]);
  const [busy, setBusy] = useState({});

  useEffect(() => {
    (async () => {
      const [c, e] = await Promise.all([api.get("/courses"), api.get("/enrollments/me")]);
      setCourses(c.data);
      setEnrolled(e.data);
    })();
  }, []);

  const enroll = async (id) => {
    setBusy((b) => ({ ...b, [id]: true }));
    await api.post("/enrollments", { course_id: id });
    const course = courses.find((c) => c.id === id);
    trackCourseEnrolled({ courseId: id, courseName: course?.name || "" });
    const e = await api.get("/enrollments/me");
    setEnrolled(e.data);
    setBusy((b) => ({ ...b, [id]: false }));
    nav(`/learn/${id}`);
  };

  const isEnrolled = (id) => enrolled.some((x) => x.id === id);

  const allNodes = [
    ...courses.map((c) => ({ ...c, status: isEnrolled(c.id) ? "active" : "available" })),
    ...COMING_SOON.map((c) => ({ ...c, id: c.name, status: "locked" })),
  ];

  return (
    <div className="pb-28">
      <div className="mb-8">
        <p className="uppercase tracking-[0.25em] text-xs font-bold text-zinc-400">Learning Path</p>
        <h1 className="font-[Outfit] font-black text-3xl tracking-tighter">Your Journey</h1>
        <p className="text-zinc-500 text-sm mt-1">Complete certifications one concept at a time. More courses unlock as you progress.</p>
      </div>

      {/* Winding path */}
      <div className="relative px-2">
        {/* Vertical spine */}
        <div className="absolute left-1/2 top-0 bottom-0 w-0.5 border-l-2 border-dashed border-zinc-200 -translate-x-1/2 z-0" />

        <div className="flex flex-col gap-0">
          {allNodes.map((node, idx) => (
            <CourseNode
              key={node.id}
              node={node}
              idx={idx}
              isEnrolled={isEnrolled(node.id)}
              busy={!!busy[node.id]}
              onEnroll={() => enroll(node.id)}
              onContinue={() => nav(`/learn/${node.id}`)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

function CourseNode({ node, idx, isEnrolled, busy, onEnroll, onContinue }) {
  const [expanded, setExpanded] = useState(isEnrolled);
  const side = idx % 2 === 0 ? "left" : "right";
  const isLocked = node.status === "locked";
  const isActive = node.status === "active";

  const nodeStyle = isLocked
    ? { background: "#E4E4E7", boxShadow: "0 6px 20px -8px rgba(0,0,0,0.15)" }
    : isActive
    ? { background: `linear-gradient(135deg, ${node.color}, ${node.color}bb)`, boxShadow: `0 16px 32px -12px ${node.color}60` }
    : { background: `linear-gradient(135deg, ${node.color}90, ${node.color}60)`, boxShadow: `0 10px 24px -10px ${node.color}50` };

  return (
    <div className={`relative z-10 flex items-start my-5 ${side === "right" ? "flex-row-reverse" : "flex-row"}`}>
      {/* Course node bubble */}
      <button
        disabled={isLocked}
        onClick={() => !isLocked && setExpanded((x) => !x)}
        className={`relative w-20 h-20 rounded-[24px] grid place-items-center shrink-0 transition-all duration-300
          ${!isLocked ? "hover:scale-105 hover:-translate-y-1 active:scale-95" : "cursor-not-allowed"}`}
        style={nodeStyle}
      >
        {isLocked ? (
          <Lock className="w-7 h-7 text-zinc-400" />
        ) : (
          <svg viewBox="0 0 24 24" width="28" height="28" fill="none"
            stroke={isActive ? "white" : "white"} strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
            <path d={ICONS_SVG[node.icon] || ICONS_SVG.Shield} />
          </svg>
        )}

        {isActive && (
          <span className="absolute -top-2 -right-2 w-5 h-5 bg-[#FBBF24] rounded-full grid place-items-center">
            <Star className="w-3 h-3 text-zinc-900" fill="currentColor" />
          </span>
        )}

        {/* FINN mascot for available (not yet enrolled) */}
        {node.status === "available" && (
          <div className="absolute -bottom-3 left-1/2 -translate-x-1/2">
            <Lumi size={28} mood="happy" />
          </div>
        )}
      </button>

      {/* Connector to spine */}
      <div className={`h-0.5 mt-10 flex-none w-10 ${isLocked ? "bg-zinc-200" : isActive ? "bg-white/40" : ""}`}
        style={{ background: isLocked ? "#E4E4E7" : node.color + "80" }} />

      {/* Info card */}
      <div className={`flex-1 ${side === "right" ? "pr-2 text-right" : "pl-2"}`}>
        <button
          disabled={isLocked}
          onClick={() => !isLocked && setExpanded((x) => !x)}
          className="w-full text-left"
        >
          <p className="text-[10px] uppercase tracking-[0.25em] font-bold text-zinc-400">{node.certification || "Coming Soon"}</p>
          <p className="font-[Outfit] font-black text-[17px] tracking-tight text-zinc-900 leading-tight">{node.name}</p>
          <p className="text-xs text-zinc-500 mt-0.5 line-clamp-1">{node.title}</p>
          {isLocked && <p className="text-[10px] text-zinc-400 mt-1 font-semibold">🔒 Coming soon</p>}
          {isActive && <p className="text-[10px] text-[#10B981] mt-1 font-bold">IN PROGRESS →</p>}
          {node.status === "available" && <p className="text-[10px] text-zinc-500 mt-1 font-semibold">Tap to start</p>}
        </button>

        {/* Expanded action card */}
        {!isLocked && expanded && (
          <div className={`mt-3 rounded-2xl border-2 p-4 ${side === "right" ? "text-left" : ""}`}
            style={{ borderColor: node.color + "30", background: node.color + "08" }}>
            <p className="text-sm text-zinc-600 line-clamp-3 mb-3">{node.description}</p>
            {isEnrolled ? (
              <button onClick={onContinue}
                className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-white text-sm font-bold transition active:scale-95"
                style={{ background: node.color }}>
                Continue Learning <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button onClick={onEnroll} disabled={busy}
                className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold transition active:scale-95 disabled:opacity-60"
                style={{ background: node.color + "20", color: node.color }}>
                {busy ? "Starting…" : "Start Course"} <ArrowRight className="w-4 h-4" />
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
