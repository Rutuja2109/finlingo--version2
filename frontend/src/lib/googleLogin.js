import { SocialLogin } from "@capgo/capacitor-social-login";

// Google sign-in for the web and the Android app. Returns the signed ID token that our server verifies.
// The server decides whether Google sign-in is available (GET /auth/config), so no client id is baked into the app.
let initializedFor = null;

export async function googleIdToken(webClientId) {
  if (initializedFor !== webClientId) {
    await SocialLogin.initialize({ google: { webClientId } });
    initializedFor = webClientId;
  }
  const res = await SocialLogin.login({ provider: "google", options: { scopes: ["email", "profile"] } });
  const token = res?.result?.idToken;
  if (!token) throw new Error("Google did not return a sign-in token");
  return token;
}

// The person closing the Google window is not an error worth showing.
export function wasCancelled(err) {
  const m = String(err?.message || err || "").toLowerCase();
  return m.includes("cancel") || m.includes("closed") || m.includes("dismiss") || m.includes("user_cancel") || m.includes("12501");
}
