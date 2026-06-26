import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "@/lib/api";
import { ArrowRight } from "lucide-react";

const ICONS_SVG = {
  Shield: "M12 2l8 4v6c0 5-3.5 9-8 10-4.5-1-8-5-8-10V6l8-4z",
  TrendingUp: "M3 17l6-6 4 4 8-8M21 7h-5M21 7v5",
  Briefcase: "M3 7h18v13H3zM8 7V5a2 2 0 012-2h4a2 2 0 012 2v2",
};

export default function Courses() {
  const [courses, setCourses] = useState([]);
  const [enrolled, setEnrolled] = useState([]);

  useEffect(() => {
    (async () => {
      const [c, e] = await Promise.all([api.get("/courses"), api.get("/enrollments/me")]);
      setCourses(c.data); setEnrolled(e.data);
    })();
  }, []);

  const enroll = async (id) => {
    await api.post("/enrollments", { course_id: id });
    const e = await api.get("/enrollments/me");
    setEnrolled(e.data);
  };
  const isEnrolled = (id) => enrolled.some((x) => x.id === id);

  return (
    <div className="pb-24">
      <div className="mb-7">
        <p className="uppercase tracking-[0.25em] text-xs font-bold text-zinc-400">Catalog</p>
        <h1 className="font-[Outfit] font-black text-3xl md:text-4xl tracking-tighter">All Courses</h1>
        <p className="text-zinc-500 mt-1">More certifications coming soon. The platform is built to scale to any cert.</p>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {courses.map((c) => (
          <div key={c.id} data-testid={`catalog-card-${c.slug}`}
            className="bg-white border border-zinc-200 rounded-3xl p-6 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
            <div className="flex items-start justify-between mb-4">
              <div className="w-12 h-12 rounded-2xl grid place-items-center text-white" style={{ background: c.color }}>
                <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
                  <path d={ICONS_SVG[c.icon] || ICONS_SVG.Shield}/>
                </svg>
              </div>
              <span className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-400">{c.certification}</span>
            </div>
            <h3 className="font-[Outfit] font-black text-xl tracking-tight">{c.name}</h3>
            <p className="text-sm text-zinc-500 mt-1">{c.title}</p>
            <p className="text-sm text-zinc-600 mt-3 line-clamp-2">{c.description}</p>
            {isEnrolled(c.id) ? (
              <Link to={`/learn/${c.id}`} data-testid={`catalog-continue-${c.slug}`}
                className="mt-5 inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-zinc-900 text-white text-sm font-bold">
                Continue <ArrowRight className="w-4 h-4"/>
              </Link>
            ) : (
              <button onClick={() => enroll(c.id)} data-testid={`catalog-enroll-${c.slug}`}
                className="mt-5 inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold"
                style={{ background: `${c.color}1A`, color: c.color }}>
                Enroll <ArrowRight className="w-4 h-4"/>
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
