# FinLearn task tracker

Legend: [x] done, [~] in progress, [ ] to do, (you) = needs you

## Decisions made
- [x] Currency: rupees (India)
- [x] App name: FinLearn
- [x] LOMA: one course only ("Institutional Investing", the rebranded one); stale "LOMA 357" copy hidden

## Go live
- [x] Backend on Render + MongoDB Atlas, login works
- [x] Old public admin account removed
- [x] New version deployed (finance tracks, Account page, daily XP fix) and verified
- [ ] (you) Change ADMIN_PASSWORD in Render
- [ ] Deploy the LOMA tidy-up (committed, not pushed)
- [ ] Rebuild APK against live server, test on phone (you)

## Before Play Store
- [ ] (you) Decide on LOMA book rights: loma.pdf is in the public repo
- [ ] Remove loma.pdf from the repo, or make the repo private
- [ ] Verify package id com.finlearn.app is free (shown when creating the app in Play Console)
- [ ] Privacy policy: fill name + support email, host it, link in app
- [ ] Always-on Render plan (you)
- [ ] Signed release bundle (AAB) + keystore backup (you)
- [ ] Turn off cleartext traffic / mixed content
- [ ] Review SCHEDULE_EXACT_ALARM permission
- [ ] Store listing: icon, feature graphic, screenshots, description
- [ ] Data safety form, content rating, reviewer test login
- [ ] (you) Play Console account ($25), 12 testers for 14 days if required

## Fix and clean
- [ ] Garbled characters in LOMA lessons
- [ ] Give coins a purpose or remove them
- [ ] Split long lesson intros into short cards
- [ ] Accessibility pass
- [ ] Friendly "waking up" message while server starts

## Features
- [ ] Daily quests + streak freeze
- [ ] Calculators: SIP, EMI, emergency fund
- [ ] First-time setup + placement quiz
- [ ] Practice portfolio (virtual Rs 1,00,000) + replay the crash
- [ ] Interactive sliders in lessons
- [ ] Friend challenges, weekly leagues
- [ ] Daily 60-second finance explainer
- [ ] Hindi + other languages
- [ ] Badges and certificates
- [ ] Ask Lumi tutor (guardrails)

## Content
- [x] Money Basics, Stock Market, Bitcoin and Crypto (1 chapter each)
- [ ] (you) Review all lessons for accuracy
- [ ] More chapters per track
- [ ] "Last reviewed" dates and sources on lessons
