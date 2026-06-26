# FinLingo — Product Requirements Doc

## Mission
AI-powered mastery learning platform for professional certifications (LOMA, CFA, FRM, PMP, AWS, etc.). Turn long boring books into interactive bite-sized journeys. Improve pass rates, retention, and engagement.

## Architecture (Phase 1)
- **Frontend**: React 19 + Tailwind + Framer Motion + lucide-react. Pages: Landing, Auth, Dashboard, Courses, CoursePath, LessonPlayer, Leaderboard, Achievements.
- **Backend**: FastAPI + Motor (async Mongo). Routes under `/api`. JWT auth with httpOnly cookies + Bearer fallback.
- **DB**: MongoDB (users, user_stats, user_progress, user_enrollments, courses, chapters, modules, concepts, lessons).
- **Mascot**: Lumi — pure-SVG crystalline orb with 4 moods (happy, cheer, think, sad).

## Learning Model (generic, supports any cert)
Course → Chapter → Module → Concept → Lesson (intro / mcq / flashcard / match / scenario)

## Gamification (REAL — no fake data)
- XP per concept (with perfect-score bonus)
- Levels (every 100 XP)
- Coins (XP/5)
- Daily streak (auto-increments, resets if skipped)
- 6 achievements (first_step, streak_3, streak_7, level_5, master_5, perfect)
- Real-time leaderboard (top 50 users by total XP)

## Phase 1 — COMPLETED
- [x] JWT auth + admin/demo seeding
- [x] Landing page
- [x] Login / Signup
- [x] Dashboard with daily-goal, streak widget, course cards
- [x] Course catalog
- [x] Course progress path (concepts unlock sequentially)
- [x] Lesson player with 5 interaction types (intro, MCQ, flashcard, match, scenario)
- [x] Real-time XP/coin/level/streak/achievement updates
- [x] Leaderboard (real users)
- [x] Achievements page
- [x] Lumi mascot integrated across screens
- [x] Mobile-responsive nav

## Personas
- **Cert candidate** preparing for LOMA/CFA/PMP/etc.
- **Continuing professional** doing nightly micro-learning.
- **Admin** seeding/managing content.

## Backlog (P0/P1/P2)
- P0: PDF ingestion pipeline (LOMA PDF was uploaded)
- P0: AI lesson generation from extracted content
- P1: Spaced-repetition revision queue
- P1: Boss Battle UI (dark-mode high-stakes quiz)
- P1: Drag-drop interaction type
- P2: Dark mode toggle
- P2: Daily revision reminders
- P2: Multi-provider AI routing (Claude/GPT/Gemini)

## Decisions
- Used React + FastAPI + MongoDB (vs preferred Next.js + Postgres) for fastest iteration in env. Clean repository-style separation enables Postgres swap later.
- httpOnly cookies + Bearer fallback (works in iframe / cross-origin preview).
- Concepts unlock sequentially within a module (mastery-learning principle).
- Mastery = score ≥ 90; Completed = score ≥ 60.

## Next Phase Recommendation
**Phase 2**: PDF ingestion pipeline + AI lesson generation (use LOMA PDF as first content source). Multi-provider LLM via Emergent Universal Key.
