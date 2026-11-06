// What Lumi feels about the learner's streak right now (drives the dashboard mascot and message).
export function streakState(stats, goalMinutes, now = new Date()) {
  const streak = stats?.streak_days || 0;
  const practiced = (stats?.xp_today || 0) > 0;
  let hour = now.getHours();
  try {
    // Testing aid: localStorage.fl_debug_hour = "22" previews Lumi's evening moods at any time of day.
    const dbg = localStorage.getItem("fl_debug_hour");
    if (dbg !== null && dbg !== "") hour = Number(dbg);
  } catch { /* storage unavailable */ }
  const mins = goalMinutes || 5;

  if (stats?.streak_broken) {
    return { mood: "sad", atRisk: false, headline: "Lumi missed you.", sub: "Start a new streak today. It only takes a few minutes." };
  }
  if (streak > 0 && practiced) {
    return { mood: "cheer", atRisk: false, headline: `${streak}-day streak. Done for today!`, sub: "Come back tomorrow to keep it going." };
  }
  if (streak > 0 && hour >= 21) {
    return { mood: "angry", atRisk: true, headline: `Lumi is NOT happy. Your ${streak}-day streak ends tonight!`, sub: `Just ${mins} minutes saves it.` };
  }
  if (streak > 0 && hour >= 18) {
    return { mood: "nervous", atRisk: true, headline: `Your ${streak}-day streak is at risk.`, sub: `${mins} minutes is all it takes.` };
  }
  if (streak > 0) {
    return { mood: "happy", atRisk: false, headline: `${streak}-day streak. Keep it alive today.`, sub: `Do ${mins} minutes before tonight.` };
  }
  return { mood: "happy", atRisk: false, headline: "Let's start your streak today.", sub: `${mins} minutes is enough.` };
}

export const GOAL_CHOICES = [
  { minutes: 5, xp: 20, label: "Casual", note: "About one lesson a day. Best for building the habit." },
  { minutes: 10, xp: 40, label: "Regular", note: "Two lessons a day." },
  { minutes: 15, xp: 60, label: "Serious", note: "Three lessons a day." },
];
