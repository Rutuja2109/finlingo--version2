# FinLingo — Product Requirements Doc

## Mission
AI-powered mastery learning platform for professional certifications (LOMA, CFA, FRM, PMP, AWS, etc.). Turn long boring books into interactive bite-sized journeys.

## Architecture
- **Frontend**: React 19 + Tailwind + lucide-react. Pages: Landing, Auth, ForgotPassword, ResetPassword, AuthCallback, Dashboard, Courses, CoursePath, LessonPlayer (with retry), Leaderboard, Achievements, Admin (AI Lab), Revision, BossBattle.
- **Backend**: FastAPI + Motor (async Mongo). Routes under `/api`. JWT auth with httpOnly cookies + Bearer fallback.
- **DB**: MongoDB collections — users, user_stats, user_progress, user_enrollments, courses, chapters, modules, concepts, lessons, pdf_uploads, generation_jobs, boss_battles, password_resets.
- **PDF Ingestion**: `pdftotext` (poppler-utils) — ~13s for 302-page PDF.
- **LLM**: GPT-5.2 (primary) + Claude Sonnet 4.5 (fallback) via Emergent Universal Key. Hard 180s per-call timeout.
- **Auth providers**: JWT email/password + Emergent-managed Google OAuth + Forgot password (dev-mode token).
- **Mascot**: Lumi — pure-SVG crystalline orb with 4 moods.

## Live Courses (real, AI-generated where noted)
1. **LOMA 357 — Institutional Investing** · AI-generated from full LOMA PDF · **10 chapters · 89 concepts · 356 lessons** · real-world examples, exam-style MCQs, common-mistake traps
2. CFA L1 — Quantitative Methods (seed)
3. PMP — Project Management Foundations (seed)

## Learning Model (generic, supports any cert)
Course → Chapter → Module → Concept → Lesson (intro / mcq / flashcard / scenario) → Boss Battle (chapter capstone)

## Gamification (REAL)
- XP per concept (perfect-score bonus, idempotent)
- Levels (every 100 XP), coins, daily streak
- Spaced repetition (SM-2 lite) with 4-button grading
- 7 achievements + boss_slayer
- Real-time leaderboard
- Boss Battle (dark-mode, server-side scoring)
- **Quiz retry** — wrong answers show feedback + "Try again →"; correct answer required to advance

## Lesson Player Features
- 5 interaction types: intro (with key takeaways + real-world example panels), MCQ (with retry), flashcard, match-pairs, scenario (with retry)
- Confetti burst on mastery
- Shake animation on wrong answer
- Real-world example callouts on intro screens
- Inline takeaway checklists

## Phase History
- **Phase 1** ✓ — Auth, Dashboard, Course path, Lesson player, XP/coins/streak, Leaderboard, Achievements, Lumi mascot.
- **Phase 2** ✓ — PDF ingestion (poppler) + AI lesson generation + Admin AI Lab + Background jobs + Spaced repetition + Boss Battle (server-graded).
- **Phase 2.5** ✓ — Google OAuth (Emergent-managed) + Forgot/Reset password flow.
- **Phase 3** ✓ — Comprehensive LOMA 357 (10 chapters, 89 concepts) + quiz retry + real-world example panels + confetti/shake animations + course dedupe.

## Personas
- Cert candidate · Continuing professional · Content admin · B2B compliance teams.

## Backlog (P1/P2)
- P1: Replace dev-mode reset with Resend/SendGrid.
- P1: Drag-drop, timeline, branching-story lesson types.
- P1: Background job: retry failed chapters automatically with smaller prompt.
- P2: Dark mode toggle (user pref).
- P2: OCR fallback for image-scanned PDFs.
- P2: Cohort/team mode for B2B.
- P2: Server-side router refactor (server.py >1100 lines).
- P2: Rate limiting on auth endpoints.

## Decisions
- LOMA 357 is the canonical AI-generated course (replaces old LOMA 280/281).
- Quiz retry pattern: wrong answer doesn't penalize — learner must reach correct answer to progress.
- Boss Battle scoring is server-side (cheat-proof).
- pdftotext `-raw` for 2-up scanned PDFs.
- GPT-5.2 primary (Claude has per-call budget limits on the Universal Key).

## Next Phase Recommendation
**Phase 4**: B2B cohort mode + Stripe enterprise billing + admin content editor for fine-tuning AI-generated lessons.
