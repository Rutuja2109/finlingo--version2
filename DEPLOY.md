# FinLearn deployment and Play Store guide

## 1. Database (MongoDB Atlas)
1. Create a free cluster at mongodb.com/atlas, then a database user.
2. Network Access: allow `0.0.0.0/0`.
3. Copy the connection string (`mongodb+srv://...`) for `MONGO_URL`.

## 2. Backend (Railway or Render)
Deploy this GitHub repo with root directory `backend`.
Start command (already in `Procfile` / `railway.json`):
`uvicorn server:app --host 0.0.0.0 --port $PORT`

Environment variables (full list and where to get each value: `docs/LAUNCH_CHECKLIST.md`):
| Name | Value |
|---|---|
| MONGO_URL | Atlas connection string |
| DB_NAME | finlingo |
| JWT_SECRET | long random string (new, not the local one) |
| ADMIN_EMAIL / ADMIN_PASSWORD | your admin login, strong password |
| PRIVACY_OPERATOR / PRIVACY_EMAIL | your name or business name, and the support email (shown on the public pages) |
| PUBLIC_BASE_URL | the server's public address, for links in emails |
| GOOGLE_CLIENT_IDS | the Web OAuth client ID (Google sign-in) |
| GOOGLE_PLAY_SERVICE_ACCOUNT_JSON | whole JSON key (checks purchases with Google Play) |
| PLAY_RTDN_SECRET | random string; used in the Play notification URL |
| SMTP_HOST / SMTP_PORT / SMTP_USER / SMTP_PASSWORD / MAIL_FROM | outgoing email for password reset |
| SENTRY_DSN | optional, error alerts |
| TRIAL_DAYS | optional, free Pro trial length (default 7) |

Never set in production: `SEED_DEMO`, `DEV_RESET_LINKS`, `DISABLE_RATE_LIMIT` (they exist only for local testing).

Check: `https://<your-url>/api/health` returns OK, `/api/health/deep` returns OK (database reachable), and `/privacy`, `/terms` and `/delete-account` open in a browser.
Note: uploaded PDFs are stored on the container disk and are lost on redeploy.

## 3. Point the app at the backend
In `frontend/.env`: `REACT_APP_BACKEND_URL=https://<your-url>`
(also update `DEFAULT_BACKEND_URL` in `frontend/src/lib/api.js`).

```
cd frontend
yarn build
npx cap sync android
```

## 4. Build the release bundle
1. Open `frontend/android` in Android Studio.
2. Check `applicationId` (`com.finlearnindia.app`), `versionCode` and `versionName` in `app/build.gradle`.
3. Build > Generate Signed Bundle > Android App Bundle. Create a keystore and back it up; losing it means you can never update the app.
4. `allowMixedContent` in `capacitor.config.json` can be set to false once the backend is https.

## 5. Play Console
- Developer account ($25 one-time, identity verification).
- Privacy policy URL (required: accounts, analytics, notifications).
- Data safety form, content rating, store listing, 512x512 icon, feature graphic, screenshots.
- Account deletion: the app has a delete button in the header; also provide a web page or email for deletion requests.
- New personal accounts: closed test with 12 testers for 14 days before production.
