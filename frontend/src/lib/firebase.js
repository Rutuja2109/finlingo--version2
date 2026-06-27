import { initializeApp } from "firebase/app";
import { getAnalytics, logEvent, setUserId, setUserProperties } from "firebase/analytics";

// ─────────────────────────────────────────────────────────────────────────────
// PASTE YOUR FIREBASE CONFIG HERE
// Steps:
//   1. Go to console.firebase.google.com
//   2. Create project "FinLingo" → click Analytics → enable Google Analytics
//   3. Click "Add app" → choose Web (</>)  → register app name "FinLingo Web"
//   4. Copy the firebaseConfig object below and replace this placeholder
// ─────────────────────────────────────────────────────────────────────────────
const firebaseConfig = {
  apiKey: "AIzaSyCyBc_FWa1MuutXWLdQK587tbpEnbz106g",
  authDomain: "finlingo-9a7ee.firebaseapp.com",
  projectId: "finlingo-9a7ee",
  storageBucket: "finlingo-9a7ee.firebasestorage.app",
  messagingSenderId: "981811440836",
  appId: "1:981811440836:web:ceca2af046919519606d91",
  measurementId: "G-86L2WCKQ8K",
};

let analytics = null;

function getAnalyticsInstance() {
  if (analytics) return analytics;
  try {
    // Only init if config is filled in
    if (firebaseConfig.apiKey === "PASTE_YOUR_API_KEY") return null;
    const app = initializeApp(firebaseConfig);
    analytics = getAnalytics(app);
    return analytics;
  } catch {
    return null;
  }
}

// ─── Core tracker (safe no-op if Firebase not configured) ────────────────────
function track(eventName, params = {}) {
  try {
    const a = getAnalyticsInstance();
    if (!a) return;
    logEvent(a, eventName, { ...params, app: "finlingo", timestamp: Date.now() });
  } catch {}
}

// ─── Identity ─────────────────────────────────────────────────────────────────
export function identifyUser(userId, name, email) {
  try {
    const a = getAnalyticsInstance();
    if (!a) return;
    setUserId(a, userId);
    setUserProperties(a, { name, email_domain: email?.split("@")[1] || "unknown" });
  } catch {}
}

// ─── Auth events ──────────────────────────────────────────────────────────────
export function trackLogin(method = "email") {
  track("login", { method });
}

export function trackSignUp(method = "email") {
  track("sign_up", { method });
}

// ─── Screen views ─────────────────────────────────────────────────────────────
export function trackScreen(screenName) {
  track("screen_view", { firebase_screen: screenName, firebase_screen_class: screenName });
}

// ─── Learning events ──────────────────────────────────────────────────────────
export function trackLessonCompleted({ conceptId, lessonType, correct, xpEarned }) {
  track("lesson_completed", { concept_id: conceptId, lesson_type: lessonType, correct, xp_earned: xpEarned });
}

export function trackConceptCompleted({ conceptId, conceptTitle, chapterId, score, xpEarned }) {
  track("concept_completed", {
    concept_id: conceptId, concept_title: conceptTitle,
    chapter_id: chapterId, score, xp_earned: xpEarned,
  });
}

export function trackChapterStarted({ chapterId, chapterTitle, chapterOrder }) {
  track("chapter_started", { chapter_id: chapterId, chapter_title: chapterTitle, chapter_order: chapterOrder });
}

export function trackCaseStudyViewed({ title, conceptId }) {
  track("case_study_viewed", { title, concept_id: conceptId });
}

// ─── Boss Battle ──────────────────────────────────────────────────────────────
export function trackBossBattleStarted({ chapterId }) {
  track("boss_battle_started", { chapter_id: chapterId });
}

export function trackBossBattleCompleted({ chapterId, score, passed, xpEarned }) {
  track("boss_battle_completed", {
    chapter_id: chapterId, score, passed, xp_earned: xpEarned,
  });
}

// ─── Streak & engagement ──────────────────────────────────────────────────────
export function trackStreakUpdated({ streakDays, isNewRecord }) {
  track("streak_updated", { streak_days: streakDays, is_new_record: isNewRecord });
}

export function trackDailyGoalHit({ xpEarned }) {
  track("daily_goal_completed", { xp_earned: xpEarned });
}

// ─── Course events ────────────────────────────────────────────────────────────
export function trackCourseEnrolled({ courseId, courseName }) {
  track("course_enrolled", { course_id: courseId, course_name: courseName });
}

export function trackRevisionStarted({ dueCount }) {
  track("revision_started", { due_count: dueCount });
}
