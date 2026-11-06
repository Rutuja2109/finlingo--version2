# FinLearn task tracker

Legend: [x] done, [~] in progress, [ ] to do, (you) = needs you. Updated 2026-11-05.
All "built" items below were pushed and are live on the server as of commit 5a2c257 (verified).

## Decisions made
- [x] Currency: rupees (India)
- [x] App name: FinLearn (package com.finlearn.app: confirm it is free when you create the app in Play Console)
- [x] LOMA: one course only ("Institutional Investing", the rebranded one); stale "LOMA 357" copy hidden

## Live on the server
- [x] Backend on Render + MongoDB Atlas, login works
- [x] Old public admin account removed
- [x] Finance tracks, Account page, daily XP fix, choice lessons (deployed 2026-11-05)

## Built and live (server) or ready (files)
- [x] Hide duplicate LOMA 357 course
- [x] Garbled characters fixed in source and repaired in the database at startup
- [x] Android: https only, no mixed content, backups off, exact-alarm permission removed
- [x] Privacy policy served at /privacy and linked from landing, sign-up and Account
- [x] Lesson intro split into short cards
- [x] Accessibility: contrast, button labels, reduced motion
- [x] "Waking up" banner and 90 second request timeout
- [x] Streak freeze (30 coins, holds 2): coins now have a purpose
- [x] Release signing set up (key stored outside the repo)
- [x] Store listing text, data-safety and content-rating notes (docs/STORE_LISTING.md)
- [x] Store assets: icon, feature graphic, 7 screenshots (design/store/out)
- [x] Signed release bundle (AAB) and installable release APK built (finlearn-release.aab / .apk in repo root, git-ignored)
- [x] Verified live: single LOMA course, /privacy page, streak-freeze route, no garbled text in 64 concepts, old admin rejected

## Phone test (Samsung SM-S921E, Android 16, 2026-11-06)
- [x] Installed release build, signed, targets Android 15
- [x] Tested on device (local test server over USB): sign-up, login, dashboard, course path, a full lesson (wrong and right answers, repeat question, result), streak freeze purchase, Courses, Rank, Awards, Account, privacy link, delete account, deleted account rejected
- [x] Fixed from the phone test: status bar/gesture bar overlap, keyboard hiding forms, demo credentials prefilled on sign-up, Continue hidden below the fold, cramped headlines, repeated course titles, leaderboard layout and names, old trademark placeholders on Courses
- [ ] (you) Log in on the phone with the release build (live server) and re-check; not tested by me: Revise page, boss battle, notification delivery at 8 am / 8 pm, offline mode, rotation

## Duolingo-inspired round (2026-11-06, committed, not pushed)
- [x] Lumi redesigned (cuter) with new angry and worried moods (design/mascot-preview.html)
- [x] Daily goal: choose 5, 10 or 15 minutes a day (20 / 40 / 60 XP), asked once after sign-up, changeable from the dashboard
- [x] Streak-at-risk behaviour: worried Lumi from 6 pm, angry Lumi (red hero) from 9 pm, sad Lumi when a streak broke
- [x] Reminder notifications escalate: morning, 8 pm worried, 9:30 pm angry
- [x] Days now follow the learner's own timezone (streak and daily goal reset at local midnight)
- [x] Practice trading built into the app (new Practice tab): Rs 1,00,000 virtual money, 4 simulated assets, chart with 7 timeframes, buy/sell, portfolio, history, crash replay, Lumi's 15-step tour with +15 XP. Server tests: backend/tests/test_practice.py. Phone-tested on the Samsung (2026-11-06).
- [x] My money tab: manual expense tracker with 50/30/20 split and Lumi coaching, income and expense entries by month, savings-goal planner ("save Rs X a month"). No SMS or bank access. Tests: backend/tests/test_money.py. Phone-tested on the Samsung (2026-11-06).
- [x] Calculators (linked from My money): SIP (what you will get, and what to save for a target), loan EMI (with the pay-extra tip), emergency fund (can use your needs from My money). Maths checked in frontend/src/lib/calc.check.mjs. Phone-tested on the Samsung (2026-11-06).
- [x] The 'coming soon' courses are now real: Taxes Made Simple (4 concepts), Insurance Basics (4), and पैसों की बात, personal finance in Hindi (4). 108 lessons. Every number rechecked in backend/tests/check_life_math.py; shape checks in check_course_shape.py. Needs your accuracy review, and a Hindi reader's review.
- [ ] More Investment Analysis chapters
- [x] Daily quests on the dashboard: 3 a day from a pool (XP, lesson, perfect score, revise, practice trade, My money log), +5 coins each, daily chest +15 coins, week view. Tests: backend/tests/test_quests.py. Phone-tested on the Samsung (2026-11-06).
- [x] Real-life missions (18): UPI history, log spends, auto-transfer, emergency fund, two-step verification, spot a scam, check health cover, PAN-Aadhaar link and more. 5 check themselves from your data, the rest are honour system with an optional note. +20 to 30 XP each, once. Mission of the week on the Dashboard. Tests: backend/tests/test_missions.py. Phone-tested on the Samsung (2026-11-06).
- [x] Daily 60-second explainer: 14 built-in 'idea of the day' explainers explaining the idea behind common headlines (repo rate, inflation, Sensex, GDP, rupee, FD, IPO, credit score, gold, NAV, bear market, regulators, budget, lifestyle inflation), one-question check, +5 XP (+5 more if right), also a daily quest. Admin page (/admin/explainers) to publish a real-headline explainer with a source link, which replaces the built-in one for that date. Nothing about real news is shown unless a person publishes it. Tests: backend/tests/test_explainers.py.
- [ ] Friend streaks, weekly leagues

## You need to do (see the list in chat)
- [ ] (you) Change ADMIN_PASSWORD in Render
- [ ] (you) Set PRIVACY_OPERATOR and PRIVACY_EMAIL in Render, then check /privacy
- [ ] (you) Back up C:\Users\Admin\finlearn-keys (two places)
- [ ] (you) Decide on LOMA book rights: loma.pdf is in the public repo
- [ ] (you) Always-on Render plan
- [ ] (you) Google Play Console account ($25), then create the app, upload AAB, fill the forms
- [ ] (you) 12 testers for 14 days, if your account type requires it
- [ ] (you) Test the APK on your phone
- [ ] (you) Review all lessons for accuracy

## Still to build
### Features (each: demo, your approval, then build)
- [ ] Calculators: SIP, EMI, emergency fund
- [ ] First-time setup + placement quiz
- [ ] Interactive sliders in lessons
- [ ] Friend challenges, weekly leagues
- [x] Hindi course (first one). More languages later
- [ ] Badges and certificates
- [ ] Ask Lumi tutor (guardrails)

### Content
- [x] Investment Analysis (exam-style), chapter 1: Quantitative Methods (4 concepts, math verified). Live on the server (verified 2026-11-05, commit e44a477).
- [x] Naming decision: neutral title (no "CFA" in the name) with a "not affiliated with CFA Institute" notice
- [x] Investment Analysis chapters 2 to 4: Fixed Income (bond pricing, duration, credit risk), Equity Valuation (dividend discount model, multiples, ROE and growth), Portfolio Management (diversification, CAPM, allocation and rebalancing). 81 lessons, every figure rechecked in backend/tests/check_ia_math.py. Course version bumped to ia-2.
- [ ] Still to write for Investment Analysis: Economics, Financial Statement Analysis, Corporate Issuers, Derivatives, Alternatives, Ethics
- [ ] More chapters per track
- [ ] Sources on lessons (after your accuracy review)

## Known risks
- [x] Google sign-in rebuilt: the app gets a Google ID token (web and Android), our server verifies it against Google's keys and issues our own login. The old Emergent-hosted flow is removed. Needs your Google Cloud client ID: see docs/GOOGLE_SIGNIN_SETUP.md. Not tested with a real Google account.
- data/loma.pdf (a copyrighted book) is in the public repo.


