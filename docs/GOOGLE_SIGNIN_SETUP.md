# Turn on "Continue with Google"

The code is built and tested. The button stays hidden until you create the Google credentials below and give the
server the client ID. Nothing here costs money. Allow about 20 minutes.

## 1. Create the project and consent screen
1. Open https://console.cloud.google.com and create a project called **FinLearn** (or pick an existing one).
2. Go to **APIs & Services → OAuth consent screen** (Google may call this "Google Auth platform").
3. User type: **External**. App name: **FinLearn**. Support email: your email.
4. App domain: privacy policy link = `https://finlingo-api.onrender.com/privacy` (set `PRIVACY_OPERATOR` and `PRIVACY_EMAIL` on Render first so the page is complete).
5. Scopes: only the three defaults (**openid, email, profile**). These need no Google review.
6. **Publish the app** (set status to "In production"). If you leave it in "Testing", only people you list as test users can sign in.

## 2. Create two OAuth client IDs (Credentials → Create credentials → OAuth client ID)

**A. Web application** (this is the one the server and the app use as the "web client ID")
- Name: `FinLearn web`
- Authorised JavaScript origins: `https://localhost` and `http://localhost:3000`
  (`https://localhost` is how the Android app identifies itself; the second one is for testing in a browser.)
- Copy the **Client ID** (ends in `.apps.googleusercontent.com`). This is the value you need below.

**B. Android** (one for each key your app is signed with)
- Package name: `com.finlearnindia.app`
- SHA-1 for your **release** key (the one in `finlearn-keys`): `84:A6:1C:5B:C8:B7:7E:CA:65:E9:A8:61:71:90:FB:7D:38:82:7B:F8`
- Create a second Android client with the SHA-1 of the **debug/test build** if you want Google sign-in to work in test builds: `B1:38:52:21:FC:42:3E:41:8F:31:A3:EF:6D:DD:E7:2A:0C:B3:80:3C`
- **If you use Play App Signing** (the default for new Play apps): after you upload your first release, Play Console → *Test and release → Setup → App signing* shows an **App signing key certificate SHA-1**. Create a third Android client with that SHA-1, otherwise Google sign-in will fail for people who install from the Play Store.

You do not need to paste the Android client IDs anywhere. Google matches them by package name and SHA-1.

## 3. Give the server the web client ID
In Render, open your service → **Environment**, add:

| Key | Value |
| --- | --- |
| `GOOGLE_CLIENT_IDS` | the Web client ID from step 2A |

Save. Render redeploys. To allow more than one client ID, separate them with commas.

You can check it worked by opening `https://finlingo-api.onrender.com/api/auth/config`. It should show your client ID instead of `null`. When it does, the **Continue with Google** button appears on the login and sign-up pages.

## 4. Test
1. Build and install the app on a phone that has a Google account added (Settings → Accounts).
2. Tap **Continue with Google**, choose the account. You land on the dashboard.
3. Sign in again with the same account: you get the same learner, not a new one.

## How accounts are handled
- A new Google user gets a new learner with 50 starting coins, no password.
- If someone **already registered with that email and a password**, signing in with Google gives them that same account and **removes the old password** (the email on a password account was never verified, so this stops anyone who signed up with another person's email first). They can sign in with Google from then on.
- The admin account keeps its password.
- Account deletion works for Google users without asking for a password.

## If it does not work
| Symptom | Likely cause |
| --- | --- |
| No Google button | `GOOGLE_CLIENT_IDS` not set, or the service has not redeployed yet |
| "Google sign-in did not work" on the phone | Android client missing, wrong package name, or wrong SHA-1 (check release vs debug vs Play signing) |
| Error 400 / "app not verified" screen | The consent screen is still in Testing, or a sensitive scope was added |
| "Google sign-in could not be verified" | The client ID on Render is not the Web client ID the app used |
