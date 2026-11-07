/**
 * Duolingo-style daily reminder notifications using Capacitor Local Notifications.
 * Only active on native (Android/iOS). On web, silently no-ops.
 */

// The plugin is returned inside a plain object: resolving a Capacitor plugin proxy
// directly from an async function makes JS call `.then` on it, which Capacitor 5+ rejects.
let _holder = null;

async function getPlugin() {
  if (_holder) return _holder;
  try {
    const { LocalNotifications } = await import("@capacitor/local-notifications");
    _holder = { LN: LocalNotifications };
    return _holder;
  } catch {
    return null;
  }
}

export async function requestNotificationPermission() {
  const plugin = await getPlugin();
  if (!plugin) return false;
  const LN = plugin.LN;
  try {
    const { display } = await LN.requestPermissions();
    return display === "granted";
  } catch {
    return false;
  }
}

const REMINDER_IDS = [1001, 1002, 1003];
const TRIAL_IDS = [2001, 2002];

const sameDay = (a, b) => a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();

// Decides what to schedule. Plain function so it can be tested without a phone.
// Once today's practice is done, today's reminders are pointless (and the "streak at risk" ones are wrong), so every
// reminder starts tomorrow instead. They repeat daily from there until the app is opened and practised again.
export function planReminders(now, streakDays = 0, practicedToday = false, reminderHour = 8) {
  const messages = getMessages(streakDays);
  const next = (h, m) => {
    const d = new Date(now);
    d.setHours(h, m, 0, 0);
    if (d <= now) d.setDate(d.getDate() + 1);
    if (practicedToday && sameDay(d, now)) d.setDate(d.getDate() + 1);
    return d;
  };
  return [
    { id: 1001, at: next(reminderHour, 0), color: "#FF6B35", ...messages.morning },
    { id: 1002, at: next(20, 0), color: "#FF6B35", ...messages.evening },
    { id: 1003, at: next(21, 30), color: "#E5484D", ...messages.late },
  ];
}

export async function scheduleReminders(streakDays = 0, reminderHour = 8, practicedToday = false) {
  const plugin = await getPlugin();
  if (!plugin) return;
  const LN = plugin.LN;

  try {
    // Cancel only the daily reminders (the trial reminders have their own ids and must survive)
    const pending = await LN.getPending();
    const mine = pending.notifications.filter((n) => REMINDER_IDS.includes(n.id));
    if (mine.length > 0) {
      await LN.cancel({ notifications: mine.map((n) => ({ id: n.id })) });
    }
    const plan = planReminders(new Date(), streakDays, practicedToday, reminderHour);
    await LN.schedule({
      notifications: plan.map((n) => ({
        id: n.id, title: n.title, body: n.body,
        schedule: { at: n.at, repeats: true, every: "day" },
        sound: null, smallIcon: "ic_launcher_foreground", iconColor: n.color,
      })),
    });
  } catch (e) {
    console.warn("Notification scheduling failed:", e);
  }
}

export async function cancelReminders() {
  const plugin = await getPlugin();
  if (!plugin) return;
  const LN = plugin.LN;
  try {
    const pending = await LN.getPending();
    if (pending.notifications.length > 0) {
      await LN.cancel({ notifications: pending.notifications.map((n) => ({ id: n.id })) });
    }
  } catch {}
}

// Two honest heads-ups before a free Pro trial ends (2 days and 1 day before, at 6 pm). Plain function, tested without a phone.
export function planTrialReminders(endsAtISO, now = new Date()) {
  const ends = new Date(endsAtISO);
  if (isNaN(ends)) return [];
  const at = (daysBefore) => { const d = new Date(ends); d.setDate(d.getDate() - daysBefore); d.setHours(18, 0, 0, 0); return d; };
  return [
    { id: 2001, at: at(2), title: "Your Pro trial ends in 2 days", body: "Your trades, spends and missions stay saved. One plan keeps every Pro feature for ₹49 a month." },
    { id: 2002, at: at(1), title: "Your Pro trial ends tomorrow", body: "Keep practice trading, My money, missions and every lesson. Cancel any time." },
  ].filter((n) => n.at > now && n.at < ends);
}

export async function scheduleTrialReminders(endsAtISO) {
  const plugin = await getPlugin();
  if (!plugin) return;
  const LN = plugin.LN;
  try {
    await LN.cancel({ notifications: TRIAL_IDS.map((id) => ({ id })) });
    const plan = planTrialReminders(endsAtISO);
    if (plan.length === 0) return;
    await LN.schedule({
      notifications: plan.map((n) => ({ id: n.id, title: n.title, body: n.body, schedule: { at: n.at }, sound: null, smallIcon: "ic_launcher_foreground", iconColor: "#8B5CF6" })),
    });
  } catch (e) {
    console.warn("Trial reminder scheduling failed:", e);
  }
}

export async function cancelTrialReminders() {
  const plugin = await getPlugin();
  if (!plugin) return;
  try { await plugin.LN.cancel({ notifications: TRIAL_IDS.map((id) => ({ id })) }); } catch { /* nothing scheduled */ }
}

// Lumi's reminders get more worried, then angry, as the day goes on and a streak is on the line.
function getMessages(streakDays) {
  if (streakDays === 0) {
    return {
      morning: { title: "Start your streak today!", body: "Five minutes of FinLearn counts. Lumi is cheering for you." },
      evening: { title: "Lumi is waiting for you", body: "One quick lesson before bed? It only takes a few minutes." },
      late: { title: "Last call for today", body: "A 5-minute lesson still counts today. Lumi believes in you." },
    };
  }
  const n = streakDays;
  return {
    morning: {
      title: n < 7 ? `Day ${n + 1}. Keep it going!` : `${n} days strong!`,
      body: "One lesson today keeps your streak alive.",
    },
    evening: {
      title: `Your ${n}-day streak is at risk`,
      body: "Lumi is getting worried. Just 5 minutes saves it.",
    },
    late: {
      title: "Lumi is NOT happy",
      body: `Your ${n}-day streak is about to break. Don't make Lumi angry. 5 minutes is all it takes!`,
    },
  };
}