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

export async function scheduleReminders(streakDays = 0, reminderHour = 8) {
  const plugin = await getPlugin();
  if (!plugin) return;
  const LN = plugin.LN;

  try {
    // Cancel existing reminders first
    const pending = await LN.getPending();
    if (pending.notifications.length > 0) {
      await LN.cancel({ notifications: pending.notifications.map((n) => ({ id: n.id })) });
    }

    const now = new Date();
    const messages = getMessages(streakDays);

    // Daily morning reminder (8 AM by default)
    const morningTime = new Date(now);
    morningTime.setHours(reminderHour, 0, 0, 0);
    if (morningTime <= now) morningTime.setDate(morningTime.getDate() + 1);

    // Evening streak-risk reminder (8 PM) — fires only if user hasn't practiced
    const eveningTime = new Date(now);
    eveningTime.setHours(20, 0, 0, 0);
    if (eveningTime <= now) eveningTime.setDate(eveningTime.getDate() + 1);

    // Last call (9:30 PM): the angry one
    const lateTime = new Date(now);
    lateTime.setHours(21, 30, 0, 0);
    if (lateTime <= now) lateTime.setDate(lateTime.getDate() + 1);

    await LN.schedule({
      notifications: [
        {
          id: 1003,
          title: messages.late.title,
          body: messages.late.body,
          schedule: { at: lateTime, repeats: true, every: "day" },
          sound: null,
          smallIcon: "ic_launcher_foreground",
          iconColor: "#E5484D",
        },
        {
          id: 1001,
          title: messages.morning.title,
          body: messages.morning.body,
          schedule: { at: morningTime, repeats: true, every: "day" },
          sound: null,
          smallIcon: "ic_launcher_foreground",
          iconColor: "#FF6B35",
        },
        {
          id: 1002,
          title: messages.evening.title,
          body: messages.evening.body,
          schedule: { at: eveningTime, repeats: true, every: "day" },
          sound: null,
          smallIcon: "ic_launcher_foreground",
          iconColor: "#FF6B35",
        },
      ],
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