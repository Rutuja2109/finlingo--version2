import { SocialLogin } from "@capgo/capacitor-social-login";

// Google sign-in for the web and the Android app. Returns the signed ID token that our server verifies.
// The server decides whether Google sign-in is available (GET /auth/config), so no client id is baked into the app.
let initializedFor = null;

export async function googleIdToken(webClientId) {
  if (initializedFor !== webClientId) {
    await SocialLogin.initialize({ google: { webClientId } });
    initializedFor = webClientId;
  }
  // filterByAuthorizedAccounts:false shows every Google account on the phone. The default (true) only offers accounts
  // that already used this app, so a first-time sign-in finds nothing and fails.
  const res = await SocialLogin.login({
    provider: "google",
    options: { scopes: ["email", "profile"], filterByAuthorizedAccounts: false, autoSelectEnabled: false },
  });
  const token = res?.result?.idToken;
  if (!token) throw new Error("Google did not return a sign-in token");
  return token;
}

// The person closing the Google window is not an error worth showing.
// A short, safe hint about what went wrong (no tokens), shown in small print so problems can be reported precisely.
export function failureHint(err) {
  const m = String(err?.message || err || "").replace(/\s+/g, " ").trim();
  return m.slice(0, 90);
}

export function wasCancelled(err) {
  const m = String(err?.message || err || "").toLowerCase();
  return m.includes("cancel") || m.includes("closed") || m.includes("dismiss") || m.includes("user_cancel") || m.includes("12501");
}
