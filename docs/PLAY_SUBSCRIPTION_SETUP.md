# FinLearn Pro: Play Console setup

The code is ready. Nothing can be bought until these steps are done. Prices: ₹49/month, ₹399/year (one subscription, two base plans).

## What is free and what is Pro
- Free: first 2 lessons of every course, daily quests, idea of the day, revision.
- Pro: all other lessons, boss battles, practice trading, My money, missions, calculators.
- Change the free amount in `backend/pro.py` (`FREE_CONCEPTS`).

## Steps (you)
1. **Play Console account** ($25 one time) and a **payments profile** (merchant account, needs bank details and PAN).
2. **Upload the app** (`finlearn-release.aab`) to an Internal testing track. Subscriptions can only be created after an app with the billing permission has been uploaded.
3. **Monetize > Products > Subscriptions > Create subscription**
   - Product ID: `finlearn_pro` (exactly)
   - Add base plan `monthly`: auto-renewing, billing period 1 month, price ₹49.
   - Add base plan `yearly`: auto-renewing, billing period 1 year, price ₹399.
   - Activate both base plans.
4. **Service account for the server** (so the server can ask Google whether a purchase is real):
   - Google Cloud (same project) > IAM > Service accounts > Create. No roles needed. Create a JSON key and keep the file private.
   - Play Console > Users and permissions > Invite new users > the service account email > permissions: "View financial data" and "Manage orders and subscriptions". (It can take up to a day to start working.)
   - Enable the **Google Play Android Developer API** in the Cloud project.
   - On Render, add env var `GOOGLE_PLAY_SERVICE_ACCOUNT_JSON` = the whole JSON file contents. Optional: `PLAY_PACKAGE_NAME` (default `com.finlearn.app`).
5. **License testers**: Play Console > Settings > License testing: add your Gmail. Test purchases are free and renew every few minutes.
6. Install from the testing track and buy on the phone. Check Account shows "FinLearn Pro".

## How it works
- The app opens Google's purchase sheet. After paying, it sends the purchase token to `/api/subscription/verify`.
- The server asks Google (Play Developer API). Only an active subscription for `finlearn_pro` unlocks Pro. A token can belong to one account only.
- Renewals and cancellations: when a stored period is about to end, the server asks Google again on the next app open. A lapsed plan turns Pro off.
- On a new phone or after reinstall the app finds the purchase and restores it automatically (also a "Restore my purchase" button).
- Admin can give Pro for N days: `POST /api/admin/pro/grant {"email": "...", "days": 30}` (use days 0 to remove). Handy for reviewers and friends.

## Rules to keep
- The paywall shows price, renewal and how to cancel (it does). Keep that text.
- Deleting an account does not cancel the subscription; the Account screen says so.
- Refunds are handled in Play Console. Not yet automatic: instant revoke on refund (needs Pub/Sub notifications; later).
