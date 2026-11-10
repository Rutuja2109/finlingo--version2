# FinLearn launch checklist

Status key: DONE = built and tested here. YOU = needs your account or decision. Last updated 9 Nov 2026.

## 1. Already built and tested (no action)
- Subscriptions: ₹49/month or ₹399/year, 7-day free trial, server-side purchase check, refund/cancel notifications (RTDN), Pro perks.
- Sign-in: email and Google (code done; see 2.3). Password reset by email (see 2.4).
- Abuse protection: rate limits on login, sign-up, reset and Google sign-in; security headers; 8-character passwords.
- Public pages served by the backend: `/privacy`, `/terms`, `/delete-account`, `/reset-password`.
- In-app account deletion; data deletion page (needed by Google Play).
- Automated checks: backend suites for subscriptions, security, email reset, Google sign-in, practice, money, quests, missions, explainers, next-lesson; lesson maths and structure checks.

## 2. Set up once (YOU, in this order)

### 2.1 Render: environment variables (Dashboard > your service > Environment)
| Name | Value | Needed for |
|---|---|---|
| `PRIVACY_OPERATOR` | your name or business name | privacy and terms pages (already set) |
| `PRIVACY_EMAIL` | support email (already set) | support contact, shown in app and pages |
| `PUBLIC_BASE_URL` | `https://finlingo-api.onrender.com` (or your own domain later) | links in emails |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `MAIL_FROM` | see 2.4 | password-reset email |
| `GOOGLE_PLAY_SERVICE_ACCOUNT_JSON` | the whole JSON key file | checking purchases with Google |
| `PLAY_RTDN_SECRET` | a long random string you make up | refund and cancel notifications |
| `SENTRY_DSN` | from sentry.io (optional) | error alerts |
| `GOOGLE_CLIENT_IDS`, `JWT_SECRET`, `ADMIN_*`, `MONGO_URL`, `DB_NAME` | already set | |

### 2.2 Hosting (the biggest speed win)
1. Render: upgrade the service to a paid plan so it never sleeps (the free plan sleeps after 15 minutes and the first open then takes 30 to 60 seconds).
2. A region near India is better (Singapore). A region cannot be changed on an existing Render service: create a new service in Singapore from the same repo, copy the environment variables, test it, then change the app's server address and release an update.
3. MongoDB Atlas: check the free M0 limits (512 MB, connection cap). Turn on backups (paid) or schedule your own export before real users arrive.
4. Free uptime alerts: UptimeRobot, monitor `https://<your server>/api/health/deep` every 5 minutes. Add your email for alerts.

### 2.3 Google sign-in for everyone (not just test users)
1. Google Cloud > your project > OAuth consent screen: add the app name, support email, privacy policy link `https://<server>/privacy` and terms link `https://<server>/terms`.
2. Domain: Google wants authorized domains you own. Use a cheap domain or a Firebase Hosting page (`finlingo-9a7ee.web.app`) that links to the privacy and terms pages. `onrender.com` cannot be authorised.
3. Click **Publish app** (move out of Testing). With only basic scopes (email, profile) no long review should be needed.
4. After your first upload to Play, copy the **App signing key SHA-1** (Play Console > Setup > App signing) and add a third Android OAuth client with it (package `com.finlearnindia.app`). Without it Google sign-in fails for people who install from Play.
5. In Google Cloud > APIs & Services > Credentials, open the Firebase browser API key and restrict it to the Android app (package and SHA-1).

### 2.4 Password-reset email
Pick one:
- **Free Render plan (SMTP ports are blocked there): Google Apps Script relay.** Sign in to the Gmail account, open script.google.com > New project, paste `docs/gmail_relay.gs`, replace the SECRET text with your own long random text. Deploy > New deployment > Web app > Execute as: Me, Who has access: Anyone > Deploy, and allow the permissions. Copy the Web app URL. In Render set `MAIL_RELAY_URL=<that URL>` and `MAIL_RELAY_SECRET=<the same secret>`. About 100 emails a day.
- **Gmail (easiest, free, about 500 emails a day):** turn on 2-step verification for the Gmail account, create an App password (Google Account > Security > App passwords), then set `SMTP_HOST=smtp.gmail.com`, `SMTP_PORT=587`, `SMTP_USER=<the gmail address>`, `SMTP_PASSWORD=<the 16-character app password>`, `MAIL_FROM=FinLearn <the gmail address>`.
- **Brevo (free, 300 a day, nicer sender):** make an account, create an SMTP key, set the same variables from Brevo's SMTP settings.
After saving, open the app > Log in > Forgot password. The page becomes a real form. Test with your own address.

### 2.5 Play Console (long pole; start first)
1. Create the developer account ($25), complete identity verification, and set up the payments profile (bank account, PAN).
2. Create the app: name FinLearn (check the name is free on Play), default language English (India), App, Free. Category Education (or Finance). Add support email.
3. Production needs a closed test first for new personal accounts (Google has required about 12 testers for 14 days; check the current rule on the Play Console dashboard). Upload `finlearn-release.aab` to a Closed testing track, add testers by email, and ask them to install.
4. Turn on **Play App Signing** when prompted (recommended), then do 2.3 step 4.
5. Monetize > Subscriptions > Create: Product ID `finlearn_pro` exactly. Add base plan `monthly` (1 month, ₹49) and `yearly` (1 year, ₹399), activate both.
6. Service account for the server: Google Cloud > IAM > Service accounts > create (no roles), make a JSON key. In Play Console > Users and permissions invite that service account email with "View financial data" and "Manage orders and subscriptions". Enable the Google Play Android Developer API in Cloud. Put the whole JSON in Render as `GOOGLE_PLAY_SERVICE_ACCOUNT_JSON`.
7. Refund and cancel notifications: Play Console > Monetize > Monetization setup > Real-time developer notifications. Create a Pub/Sub topic (Google gives the steps), then a **Push** subscription to `https://<server>/api/subscription/rtdn?token=<PLAY_RTDN_SECRET>`. Press "Send test notification" (it should show success).
8. Settings > License testing: add your Gmail. Install from the closed test and buy; test purchases renew every few minutes. Check Account shows FinLearn Pro, then cancel and watch it end.

### 2.6 Store listing and policy forms (Play Console)
- Listing text: see `docs/STORE_LISTING.md`. Icon, feature graphic and 2 to 8 phone screenshots. The icon and feature graphic are in `design/brand` and `design/store/out`. **New screenshots are still needed** (the old ones show the old logo and layout).
- Privacy policy URL: `https://<server>/privacy`. Account deletion URL (Data safety): `https://<server>/delete-account`.
- **Data safety form** (what to answer):
  - Collected: name, email address, user IDs, app interactions, purchase history (subscription status), crash/diagnostic logs only if you turn Sentry on.
  - Purpose: app functionality, account management, analytics. Not for advertising. Not sold.
  - Shared with third parties: no (service providers only: hosting, database, Firebase, Google Play).
  - Encrypted in transit: yes. Users can request deletion: yes (in app and on the web page).
- **Content rating** (IARC questionnaire): an educational app with no violence, no user-generated content, no gambling. Answer the finance-related questions honestly: practice trading is simulated with virtual money.
- **Target audience:** 18 and older. Do not select children.
- **Financial features declaration:** declare that the app provides financial education and simulated trading, and does not offer loans, real trading, or investment advice. Keep the in-app wording "education, not advice".
- **Ads:** none. **Data deletion**: provide the URL above.

## 3. Content review (YOU or a professional)
Have someone qualified read the tax, insurance, crypto-rule and Hindi lessons. Rules change every Budget. Plan a yearly update each February.

## 4. Before pressing "Publish"
- Install from the closed test on at least 3 phones (one older and slow) and run the checklist in `docs/PHONE_TEST.md`.
- Buy and cancel once with a license tester; confirm refund notification (cancel and refund in Play Console, then check Pro ends).
- Open each public page on your phone: `/privacy`, `/terms`, `/delete-account`.
- Make the GitHub repository private (an old copyrighted book is still in its history).
- Back up the release keystore and its passwords somewhere safe (two places).

## 5. After launch
- Watch Sentry and UptimeRobot alerts; reply to support email within a day.
- Friend referral, leagues, more chapters, Hindi button labels everywhere.
