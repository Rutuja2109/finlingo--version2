# FinLingo — Product Requirements Doc

## Mission
AI-powered mastery learning platform for professional certifications (LOMA, CFA, FRM, PMP, AWS, etc.). Turn long boring books into interactive bite-sized journeys. Improve pass rates, retention, and engagement.

## Architecture
- **Frontend**: React 19 + Tailwind + Framer Motion + lucide-react. Pages: Landing, Auth, Dashboard, Courses, CoursePath, LessonPlayer, Leaderboard, Achievements, **Admin (AI Lab), Revision, BossBattle**.
- **Backend**: FastAPI + Motor (async Mongo). Routes under `/api`. JWT auth with httpOnly cookies + Bearer fallback.
- **DB**: MongoDB collections — users, user_stats, user_progress, user_enrollments, courses, chapters, modules, concepts, lessons, **pdf_uploads, generation_jobs, boss_battles**.
- **PDF Ingestion**: `pdftotext` (poppler-utils) — 15× faster than pdfplumber. 302-page PDF processed in ~13s.
- **LLM**: emergentintegrations LlmChat with Claude Sonnet 4.5 (primary) + GPT-5.2 (fallback). Strict JSON output, retry-on-parse-fail across providers.
- **Mascot**: Lumi — pure-SVG crystalline orb with 4 moods.

## Learning Model (generic, supports any cert)
Course → Chapter → Module → Concept → Lesson (intro / mcq / flashcard / match / scenario) → **Boss Battle** (chapter capstone)

## Gamification (REAL)
- XP per concept with perfect-score bonus · idempotent (re-completion = 0 XP)
- Levels (every 100 XP)
- Coins (XP/5)
- Daily streak (auto-tracked)
- **Spaced repetition (SM-2 lite)** — every mastered concept gets a `next_review_at`
- 7 achievements: first_step, streak_3, streak_7, level_5, master_5, perfect, **boss_slayer**
- Real-time leaderboard (no fake data)
- **Boss Battle** — dark-mode chapter capstone, server-side scoring (cheat-proof)

## Phase 1 — COMPLETED ✓
- JWT auth + admin/demo seeding
- Landing, Auth, Dashboard, Course catalog, Course path, Lesson player (5 types)
- Real XP/coin/level/streak/achievement, Leaderboard, Achievements, Lumi mascot

## Phase 2 — COMPLETED ✓
- [x] PDF ingestion pipeline (poppler-utils based; max-chapters early exit)
- [x] AI lesson generation — Claude Sonnet 4.5 primary, GPT-5.2 fallback
- [x] Admin AI Lab UI (upload PDF, configure course meta, kick off generation, watch live progress)
- [x] Background generation job runner with status tracking
- [x] LOMA 281 v2 generated end-to-end (13 concepts, 6 modules, 2 chapters) from the uploaded LOMA PDF
- [x] Spaced-repetition revision queue (SM-2 lite, 4-button grading)
- [x] Boss Battle dark-mode UI (full-page dark) with server-side scoring (cheat-proof) and boss_slayer achievement
- [x] Course path boss-CTA per chapter (locks until all chapter concepts complete)

## Personas
- **Cert candidate** preparing for LOMA/CFA/PMP/AWS/etc.
- **Continuing professional** doing nightly micro-learning + spaced revision.
- **Content admin** uploading new certification PDFs to auto-generate courses.

## Backlog (P1/P2)
- P1: Drag-drop interaction type · Timeline lesson · Branching story
- P1: Multi-provider AI A/B routing tuned by cost/quality
- P2: Dark-mode toggle (user pref, not just boss battle)
- P2: Daily reminder push notifications
- P2: Admin content editor (manual concept tweak post-generation)
- P2: OCR fallback for image-only scanned PDFs (current LOMA PDF body was image-based)
- P2: Cohort/team mode, instructor dashboard
- P2: Mobile native app (Expo/React Native)

## Decisions
- React + FastAPI + MongoDB stack (vs Next.js/Postgres) for fastest iteration.
- httpOnly cookies + Bearer fallback (works in iframe / cross-origin preview).
- Concepts unlock sequentially within module (mastery-learning).
- Mastery = score ≥ 90; Completed = ≥ 60.
- Boss Battle scoring is server-side (client sends `{question_id: chosen_index}` map, server grades) to prevent cheating.
- pdftotext `-raw` flag chosen for clean text on 2-up scanned PDFs.

## Next Phase Recommendation
**Phase 3**: Cohort/team mode with employer billing — high-CAC EdTech revenue lever for B2B sales to compliance teams (insurance, banks). Add admin seats, team leaderboards, certification expiry tracking.
