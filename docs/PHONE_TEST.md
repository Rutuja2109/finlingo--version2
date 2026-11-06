# FinLearn phone test checklist

Test the release APK (`finlearn-release.apk`) on a real Android phone. Tick each item; note anything odd.

## Before you start
- [ ] **Warm up the server.** Open https://finlingo-api.onrender.com/api/health in your phone's browser. It should show `{"status":"ok"}`. The first time after a pause it can take up to a minute.
- [ ] **Remove any older FinLearn app** first (long-press the icon, Uninstall). The release APK uses a different signing key and will not install over an older debug version.
- [ ] Allow installing from the app you open the APK with (Files, Drive or WhatsApp) when Android asks.
- [ ] Use a **new test account** for the full test. Do not delete the shared demo account (`demo@finlingo.com`).

## 1. Install and first open
- [ ] App installs and the FinLearn icon (orange, bunny) appears
- [ ] App opens to the landing page, text is readable, nothing cut off
- [ ] "Privacy policy" link at the bottom opens a page in the browser

## 2. Sign up and login
- [ ] Sign up with a new email and a password (6+ characters)
- [ ] You land on the dashboard with your name in the greeting
- [ ] Log out (arrow icon), then log back in
- [ ] A wrong password shows a clear error
- [ ] Try "Forgot password"
- [ ] Try "Try the demo" from the landing page (it fills the demo login)
- [ ] If there is a Google sign-in button, try it and note whether it works

## 3. Dashboard
- [ ] Streak, XP and coins chips at the top fit on the screen
- [ ] The orange banner and three stat cards look right
- [ ] Daily goal shows "0 / 30 XP today" for a new account
- [ ] Bottom tabs (Home, Courses, Rank, Awards) all fit and open their pages

## 4. Courses
- [ ] Courses page shows five courses: Money Basics, Stock Market, Bitcoin and Crypto, Institutional Investing, Investment Analysis
- [ ] Each has the right icon (wallet, chart, Bitcoin, shield, calculator)
- [ ] Start Money Basics, open the course path

## 5. A full lesson (do this one slowly)
- [ ] Open "Where does your money go?"
- [ ] The intro is short, then separate cards for "In plain English", the example and key takeaways
- [ ] Tap the flashcard to flip it
- [ ] In a real-life situation, choose a **wrong** answer: red verdict, explanation, and the wallet bars
- [ ] Choose the **right** answer on the next one: green verdict
- [ ] The wrong question comes back later in the lesson
- [ ] The "Continue" button is reachable without awkward scrolling
- [ ] Finish the lesson: result screen with XP and coins
- [ ] Back on the dashboard, daily goal and XP have moved
- [ ] The next concept unlocked on the course path

## 6. Coins and streak freeze
- [ ] On the dashboard, the streak card shows "Streak freezes: 0/2"
- [ ] If you have 30+ coins, buy one: coins go down by 30 and freezes show 1/2
- [ ] With under 30 coins the button is disabled

## 7. Other pages
- [ ] Revise page opens (if concepts are due)
- [ ] Rank page shows the leaderboard
- [ ] Awards page shows achievements
- [ ] Boss battle is locked until concepts are done

## 8. Reminders (notifications)
- [ ] After login Android asks to allow notifications. Allow it.
- [ ] Notifications are scheduled (you may not see one until 8 am or 8 pm, and it may be a few minutes late)

## 9. Account
- [ ] Gear icon opens Account with your name and email
- [ ] "Privacy policy" link works
- [ ] Log out works
- [ ] **On your new test account only:** "Delete my account" asks for your password, then returns you to the login page. Logging in again with that account fails.

## 10. Real-world behaviour
- [ ] Rotate the phone, nothing breaks
- [ ] Turn on airplane mode and open the app: it shows an error but does not crash
- [ ] Turn off the internet during a lesson, then back on, and continue
- [ ] Phone's dark mode: text is still readable
- [ ] Switch away and back to the app: you are still logged in

## 11. New features (added after the first phone test)
Bottom tabs are now Home, Courses, Practice, Money, Rank. Awards moved to Account.
- [ ] **Practice:** Lumi's tour starts on first open. Tap through it (NIFTY, 5MIN, Buy, Confirm, Sell). Finish for +15 XP.
- [ ] Practice: chart readable, buy and sell sheets fit above the keyboard-free area, Portfolio and History tabs work
- [ ] Practice: "Replay a market crash" runs about 30 seconds, then shows the before and after message
- [ ] **My money:** add income and a few expenses (the amount field opens the number keyboard and is not hidden by it)
- [ ] My money: the 50/30/20 split and Lumi's comment update, entries can be deleted, month arrows work
- [ ] My money: create a goal ("New phone", 50000, 6 months) and see "Save ₹8,333 a month"
- [ ] **Calculators** (link at the top of My money): SIP, Loan EMI and Emergency fund tabs, sliders are easy to use with a thumb
- [ ] **Dashboard:** idea of the day card, daily quests card (three quests, Claim buttons, chest), missions card
- [ ] Explainer: read it, answer the quick check, see +XP
- [ ] **Missions:** open one, tick "I did it" with a note; try the "Log 5 spends" one before and after logging
- [ ] **New courses:** Taxes Made Simple, Insurance Basics, पैसों की बात (Hindi text shows correctly, not boxes)
- [ ] Investment Analysis now has four chapters

## What to send me
For any problem, tell me: which screen, what you tapped, what you expected, and what happened. A screenshot helps a lot.
