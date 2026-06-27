/**
 * Duolingo-style daily reminder notifications using Capacitor Local Notifications.
 * Only active on native (Android/iOS). On web, silently no-ops.
 */

let _LocalNotifications = null;

async function getPlugin() {
  if (_LocalNotifications) return _LocalNotifications;
  try {
    const { LocalNotifications } = await import("@capacitor/local-notifications");
    _LocalNotifications = LocalNotifications;
    return _LocalNotifications;
  } catch {
    return null;
  }
}

export async function requestNotificationPermission() {
  const LN = await getPlugin();
  if (!LN) return false;
  try {
    const { display } = await LN.requestPermissions();
    return display === "granted";
  } catch {
    return false;
  }
}

export async function scheduleReminders(streakDays = 0, reminderHour = 8) {
  const LN = await getPlugin();
  if (!LN) return;

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

    await LN.schedule({
      notifications: [
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
  const LN = await getPlugin();
  if (!LN) return;
  try {
    const pending = await LN.getPending();
    if (pending.notifications.length > 0) {
      await LN.cancel({ notifications: pending.notifications.map((n) => ({ id: n.id })) });
    }
  } catch {}
}

function getMessages(streakDays) {
  if (streakDays === 0) {
    return {
      morning: { title: "Start your streak today! 🔥", body: "Even 5 minutes of FinLearn counts. Begin your first concept now." },
      evening: { title: "Still time to start! ⏰", body: "Open FinLearn and complete one concept before midnight." },
    };
  }
  if (streakDays < 3) {
    return {
      morning: { title: `Day ${streakDays + 1} — keep it going! 🔥`, body: "You're building a habit. Practice a concept to grow your streak." },
      evening: { title: "Don't lose your streak! ⚠️", body: `You're on a ${streakDays}-day streak. Complete today's lesson before midnight.` },
    };
  }
  if (streakDays < 7) {
    return {
      morning: { title: `${streakDays}-day streak! Keep it alive 🔥`, body: "Your consistency is paying off. One concept a day keeps the streak alive." },
      evening: { title: "Streak at risk! 😰", body: `Don't let your ${streakDays}-day streak die tonight. Jump in for 5 minutes.` },
    };
  }
  if (streakDays < 30) {
    return {
      morning: { title: `${streakDays} days strong 🏆`, body: "You're in the top learners this week. Keep the momentum going!" },
      evening: { title: `Protect your ${streakDays}-day streak! 🔥`, body: "You've worked hard for this. Don't let tonight break it." },
    };
  }
  return {
    morning: { title: `${streakDays}-day legend! 🌟`, body: "You're unstoppable. Keep mastering LOMA 357 one concept at a time." },
    evening: { title: `${streakDays} days — don't stop now! 🏆`, body: "Champions practice every day. A quick concept is all it takes." },
  };
}
