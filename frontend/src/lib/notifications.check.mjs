// Run: node frontend/src/lib/notifications.check.mjs
import { planReminders } from "./notifications.js";

let bad = 0;
const ok = (name, cond) => { console.log((cond ? "OK  " : "BAD ") + name); if (!cond) bad++; };
const day = (d) => `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`;
const at = (y, m, d, h, mi = 0) => new Date(y, m - 1, d, h, mi, 0);
const byId = (plan, id) => plan.find((p) => p.id === id);

// 3 pm on 6 Nov, streak of 4, has NOT practised
let now = at(2026, 11, 6, 15);
let plan = planReminders(now, 4, false);
ok("three reminders with the usual ids", plan.map((p) => p.id).join() === "1001,1002,1003");
ok("not practised: morning is tomorrow 8:00, evening today 20:00, late today 21:30",
  day(byId(plan, 1001).at) === "2026-11-7" && byId(plan, 1001).at.getHours() === 8
  && day(byId(plan, 1002).at) === "2026-11-6" && byId(plan, 1002).at.getHours() === 20
  && day(byId(plan, 1003).at) === "2026-11-6" && byId(plan, 1003).at.getHours() === 21 && byId(plan, 1003).at.getMinutes() === 30);
ok("not practised: the evening one warns about the streak", /at risk/i.test(byId(plan, 1002).title) && /4-day/.test(byId(plan, 1002).title));
ok("not practised: the late one is the angry Lumi", /NOT happy/.test(byId(plan, 1003).title));

// same moment, but already practised today
plan = planReminders(now, 4, true);
ok("practised: every reminder starts tomorrow", plan.every((p) => day(p.at) === "2026-11-7"));
ok("practised: tomorrow's times are still 8:00, 20:00 and 21:30", [8, 20, 21].every((h, i) => plan[i].at.getHours() === h));
ok("practised: nothing is scheduled for today", plan.every((p) => p.at > now && day(p.at) !== day(now)));

// early morning (6 am) and practised: the 8 am nudge today is pointless too
now = at(2026, 11, 6, 6);
plan = planReminders(now, 4, true);
ok("practised at 6 am: even the 8 am reminder moves to tomorrow", day(byId(plan, 1001).at) === "2026-11-7");
plan = planReminders(now, 4, false);
ok("not practised at 6 am: the 8 am reminder is still today", day(byId(plan, 1001).at) === "2026-11-6");

// late night after the last reminder
now = at(2026, 11, 6, 23, 10);
plan = planReminders(now, 4, false);
ok("11 pm: everything is tomorrow, even without practising", plan.every((p) => day(p.at) === "2026-11-7"));

// month and year rollover
now = at(2026, 12, 31, 15);
plan = planReminders(now, 4, true);
ok("year end rolls over to 1 January", plan.every((p) => day(p.at) === "2027-1-1"));

// messages
plan = planReminders(at(2026, 11, 6, 9), 0, false);
ok("no streak: encourages starting one", /Start your streak/.test(byId(plan, 1001).title));
plan = planReminders(at(2026, 11, 6, 9), 9, false);
ok("long streak: the morning message cheers", /9 days strong/.test(byId(plan, 1001).title));
ok("every reminder has a title, a body and a colour", plan.every((p) => p.title && p.body && /^#/.test(p.color)));

console.log(bad ? `\nFAILED: ${bad}` : "\nALL PASSED");
process.exit(bad ? 1 : 0);
