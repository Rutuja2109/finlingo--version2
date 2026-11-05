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
- [ ] Daily quests
- [ ] Calculators: SIP, EMI, emergency fund
- [ ] First-time setup + placement quiz
- [ ] Practice portfolio (virtual Rs 1,00,000) + replay the crash
- [ ] Interactive sliders in lessons
- [ ] Friend challenges, weekly leagues
- [ ] Daily 60-second finance explainer
- [ ] Hindi + other languages
- [ ] Badges and certificates
- [ ] Ask Lumi tutor (guardrails)

### Content
- [x] Investment Analysis (exam-style), chapter 1: Quantitative Methods (4 concepts, math verified). Committed locally, not pushed.
- [x] Naming decision: neutral title (no "CFA" in the name) with a "not affiliated with CFA Institute" notice
- [ ] More Investment Analysis topics (Economics, Financial Statement Analysis, Corporate Issuers, Equity, Fixed Income, Derivatives, Alternatives, Portfolio Management, Ethics)
- [ ] More chapters per track
- [ ] Sources on lessons (after your accuracy review)

## Known risks
- Google sign-in uses an external service (auth.emergentagent.com). Test it, it may not work outside the original platform.
- data/loma.pdf (a copyrighted book) is in the public repo.
