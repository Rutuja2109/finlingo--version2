import React, { useEffect, useState, useRef } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { Upload, FileText, Sparkles, CheckCircle2, Loader2, AlertCircle, BookOpen, ShieldAlert } from "lucide-react";

export default function Admin() {
  const { user } = useAuth();
  const [pdfs, setPdfs] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [form, setForm] = useState({
    name: "LOMA 281", title: "Institutional Investing", certification: "LOMA",
    description: "AI-generated from official LOMA study material.",
    color: "#FF6B35", icon: "BookOpen", max_chapters: 2,
  });
  const [selectedPdf, setSelectedPdf] = useState(null);
  const fileRef = useRef(null);

  const load = async () => {
    try {
      const [p, j] = await Promise.all([api.get("/admin/pdf/list"), api.get("/admin/jobs")]);
      setPdfs(p.data); setJobs(j.data);
    } catch {}
  };

  useEffect(() => { load(); const t = setInterval(load, 3500); return () => clearInterval(t); }, []);

  if (user && user.role !== "admin") {
    return (
      <div className="bg-white border border-zinc-200 rounded-3xl p-10 text-center">
        <ShieldAlert className="w-10 h-10 mx-auto text-[#EF4444] mb-2"/>
        <h2 className="font-[Outfit] font-black text-2xl">Admins only</h2>
        <p className="text-zinc-500">Sign in as <code>admin@finlingo.com</code> to access the AI lab.</p>
      </div>
    );
  }

  const upload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    const fd = new FormData();
    fd.append("file", file);
    try {
      const { data } = await api.post("/admin/pdf/upload", fd, { headers: { "Content-Type": "multipart/form-data" } });
      await load();
      setSelectedPdf(data.pdf_id);
    } catch (e) { alert("Upload failed"); }
    finally { setUploading(false); if (fileRef.current) fileRef.current.value = ""; }
  };

  const generate = async () => {
    if (!selectedPdf) { alert("Select a PDF first"); return; }
    setGenerating(true);
    try {
      await api.post(`/admin/pdf/${selectedPdf}/generate`, form);
      await load();
    } catch (e) { alert("Generation failed to start"); }
    finally { setGenerating(false); }
  };

  return (
    <div className="pb-24 max-w-5xl">
      <div className="mb-7">
        <p className="uppercase tracking-[0.25em] text-xs font-bold text-zinc-400">Admin · AI Lab</p>
        <h1 className="font-[Outfit] font-black text-3xl md:text-4xl tracking-tighter">Generate a course from a PDF</h1>
        <p className="text-zinc-500 mt-1">Upload a textbook → we'll extract chapters and generate interactive lessons using Claude Sonnet 4.5 + GPT-5.2.</p>
      </div>

      {/* Upload */}
      <section className="bg-white border border-zinc-200 rounded-3xl p-6 mb-6">
        <h2 className="font-[Outfit] font-bold text-xl mb-3">1. Upload PDF</h2>
        <label data-testid="pdf-uploader"
          className="flex items-center justify-center gap-3 p-6 border-2 border-dashed border-zinc-300 rounded-2xl cursor-pointer hover:border-[#FF6B35] hover:bg-[#FF6B35]/5 transition">
          <Upload className="w-5 h-5 text-zinc-500"/>
          <span className="font-semibold text-zinc-700">{uploading ? "Uploading…" : "Click to choose a PDF (max ~80MB)"}</span>
          <input ref={fileRef} type="file" accept="application/pdf" className="hidden" onChange={upload} disabled={uploading}/>
        </label>

        {pdfs.length > 0 && (
          <div className="mt-5">
            <p className="text-xs uppercase tracking-[0.2em] font-bold text-zinc-500 mb-2">Available PDFs</p>
            <div className="space-y-2">
              {pdfs.map((p) => (
                <label key={p.id} data-testid={`pdf-${p.id}`}
                  className={`flex items-center gap-3 p-3 rounded-xl border-2 cursor-pointer transition ${selectedPdf === p.id ? "border-[#FF6B35] bg-[#FF6B35]/5" : "border-zinc-200 hover:border-zinc-400"}`}>
                  <input type="radio" name="pdf" checked={selectedPdf === p.id} onChange={() => setSelectedPdf(p.id)} className="accent-[#FF6B35]"/>
                  <FileText className="w-4 h-4 text-zinc-500"/>
                  <span className="font-semibold flex-1 truncate">{p.original_name}</span>
                  <span className="text-xs text-zinc-400">{Math.round(p.size_bytes/1024/1024)} MB</span>
                </label>
              ))}
            </div>
          </div>
        )}
      </section>

      {/* Course meta */}
      <section className="bg-white border border-zinc-200 rounded-3xl p-6 mb-6">
        <h2 className="font-[Outfit] font-bold text-xl mb-4">2. Course details</h2>
        <div className="grid sm:grid-cols-2 gap-4">
          <Input label="Course name" testid="course-name" value={form.name} onChange={(v) => setForm({...form, name: v})}/>
          <Input label="Title" testid="course-title" value={form.title} onChange={(v) => setForm({...form, title: v})}/>
          <Input label="Certification" testid="course-cert" value={form.certification} onChange={(v) => setForm({...form, certification: v})}/>
          <Input label="Color" testid="course-color" value={form.color} onChange={(v) => setForm({...form, color: v})}/>
          <Input label="Description" testid="course-desc" value={form.description} onChange={(v) => setForm({...form, description: v})}/>
          <div>
            <label className="text-xs uppercase tracking-[0.2em] font-semibold text-zinc-500 mb-1.5 block">Chapters to generate (cost cap)</label>
            <input type="number" min="1" max="12" data-testid="course-maxch" value={form.max_chapters}
              onChange={(e) => setForm({...form, max_chapters: parseInt(e.target.value) || 1})}
              className="w-full px-4 py-3 rounded-xl border border-zinc-200 outline-none focus:border-[#FF6B35]"/>
          </div>
        </div>
      </section>

      {/* Generate */}
      <section className="mb-6">
        <button onClick={generate} disabled={!selectedPdf || generating} data-testid="btn-generate"
          className="px-7 py-4 rounded-2xl bg-[#FF6B35] hover:bg-[#FF5618] text-white font-[Outfit] font-bold tracking-tight inline-flex items-center gap-2 disabled:opacity-50 transition active:scale-[0.98]">
          <Sparkles className="w-5 h-5"/> {generating ? "Starting…" : "Generate course with AI"}
        </button>
        <p className="text-xs text-zinc-500 mt-2">Runs in background. Track progress below.</p>
      </section>

      {/* Jobs */}
      <section className="bg-white border border-zinc-200 rounded-3xl p-6">
        <h2 className="font-[Outfit] font-bold text-xl mb-4">3. Generation jobs</h2>
        {jobs.length === 0 && <p className="text-zinc-500">No jobs yet.</p>}
        <div className="space-y-3">
          {jobs.map((j) => (
            <div key={j.id} data-testid={`job-${j.id}`} className="border border-zinc-200 rounded-2xl p-4">
              <div className="flex items-center justify-between mb-2">
                <div>
                  <p className="font-[Outfit] font-bold">{j.course_meta?.name} · {j.course_meta?.certification}</p>
                  <p className="text-xs text-zinc-500">{j.created_at?.slice(0,19).replace("T"," ")}</p>
                </div>
                <StatusPill status={j.status}/>
              </div>
              <div className="h-2 rounded-full bg-zinc-100 overflow-hidden">
                <div className="h-full bg-gradient-to-r from-[#FF6B35] to-[#EC4899] transition-all duration-700"
                  style={{ width: `${j.progress || 0}%` }}/>
              </div>
              <p className="text-xs text-zinc-500 mt-2">
                {j.status === "completed" && <>Done — chapters: {j.chapters_detected}. <a className="text-[#FF6B35] font-bold" href={`/learn/${j.course_id}`}>Open course →</a></>}
                {j.status === "generating" && <>Generating: {j.current_chapter}…</>}
                {j.status === "extracting" && "Extracting chapters from PDF…"}
                {j.status === "failed" && <span className="text-red-600">Error: {j.error}</span>}
                {j.status === "queued" && "Queued — starting shortly."}
              </p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

function Input({ label, value, onChange, testid }) {
  return (
    <label className="block">
      <span className="text-xs uppercase tracking-[0.2em] font-semibold text-zinc-500 mb-1.5 block">{label}</span>
      <input value={value} onChange={(e) => onChange(e.target.value)} data-testid={testid}
        className="w-full px-4 py-3 rounded-xl border border-zinc-200 outline-none focus:border-[#FF6B35] focus:ring-2 focus:ring-[#FF6B35]/20"/>
    </label>
  );
}

function StatusPill({ status }) {
  const map = {
    queued:     { c: "#71717A", bg: "#F4F4F5", Ic: Loader2, t: "Queued" },
    extracting: { c: "#2563EB", bg: "#DBEAFE", Ic: Loader2, t: "Extracting" },
    generating: { c: "#FF6B35", bg: "#FFE5D6", Ic: Loader2, t: "Generating" },
    completed:  { c: "#10B981", bg: "#D1FAE5", Ic: CheckCircle2, t: "Done" },
    failed:     { c: "#EF4444", bg: "#FEE2E2", Ic: AlertCircle, t: "Failed" },
  };
  const s = map[status] || map.queued;
  return (
    <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider"
      style={{ color: s.c, background: s.bg }}>
      <s.Ic className={`w-3.5 h-3.5 ${status !== "completed" && status !== "failed" ? "animate-spin" : ""}`}/>
      {s.t}
    </span>
  );
}
