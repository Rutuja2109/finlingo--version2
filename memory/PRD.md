# FinLingo — Product Requirements Doc

## Mission
AI-powered mastery learning platform for professional certifications (LOMA, CFA, FRM, PMP, AWS, etc.). Turn long boring books into interactive bite-sized journeys.

## Architecture
- **Frontend**: React 19 + Tailwind + lucide-react. Pages: Landing, Auth, ForgotPassword, ResetPassword, AuthCallback, Dashboard, Courses, CoursePath, LessonPlayer, Leaderboard, Achievements, Admin (AI Lab), Revision, BossBattle.
- **Backend**: FastAPI + Motor (async Mongo). Routes under `/api`. JWT auth with httpOnly cookies + Bearer fallback.
- **DB**: MongoDB collections — users, user_stats, user_progress, user_enrollments, courses, chapters, modules, concepts, lessons, pdf_uploads, generation_jobs, boss_battles, password_resets.
- **PDF Ingestion**: `pdftotext` (poppler-utils) — ~13s for 302-page PDF.
- **LLM**: emergentintegrations LlmChat with Claude Sonnet 4.5 primary + GPT-5.2 fallback.
- **Auth providers**: JWT email/password + Emergent-managed Google OAuth (additive).
- **Mascot**: Lumi — pure-SVG crystalline orb with 4 moods.

## Learning Model (generic, supports any cert)
Course → Chapter → Module → Concept → Lesson (intro / mcq / flashcard / match / scenario) → Boss Battle (chapter capstone)

## Gamification (REAL)
- XP per concept (with perfect-score bonus, idempotent)
- Levels, coins, daily streak
- Spaced repetition (SM-2 lite)
- 7 achievements + boss_slayer
- Real-time leaderboard
- Boss Battle (dark-mode, server-side scoring)

## Phase 1 — COMPLETED ✓
JWT auth + Dashboard + Course catalog + Course path + Lesson player (5 types) + XP/coin/streak/level/achievement + Leaderboard + Lumi mascot.

## Phase 2 — COMPLETED ✓
PDF ingestion (poppler) + AI lesson generation (Claude + GPT) + Admin AI Lab + Background generation jobs + LOMA 281 v2 generated end-to-end + Spaced repetition + Boss Battle (server-graded, cheat-proof).

## Phase 2.5 — COMPLETED ✓
- [x] Google OAuth via Emergent (one-click "Continue with Google"). Auto-creates user or links to existing email.
- [x] Forgot password flow (dev-mode, no email service): /forgot-password → backend returns reset_token + path → frontend builds same-origin URL → /reset-password auto-logs-in.
- [x] AuthCallback page handles session_id hash synchronously before any Protected route renders.
- [x] AuthContext skips /auth/me when URL has session_id (race-free).

## Personas
- Cert candidate · Continuing professional · Content admin.

## Backlog (P1/P2)
- P1: Replace dev-mode reset with Resend/SendGrid emails when API key available.
- P1: Drag-drop, timeline, branching-story lesson types.
- P2: Dark mode toggle (user pref).
- P2: OCR fallback for image-scanned PDFs.
- P2: Cohort/team mode for B2B.
- P2: Server-side router refactor (server.py >1000 lines).
- P2: Rate limiting on /auth/google/session and /auth/forgot-password.

## Decisions
- Forgot password returns token+path (not full URL) → frontend assembles same-origin link → works across preview/prod without env-var fiddling.
- Google auth merges with existing users by email (no duplicate accounts).
- Boss Battle scoring is server-side (cheat-proof).
- pdftotext `-raw` for 2-up scanned PDFs.

## Next Phase Recommendation
**Phase 3**: B2B cohort mode + Stripe enterprise billing. One insurance carrier contract = 1000+ seats × $400/yr.
