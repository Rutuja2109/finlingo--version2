// Run: node src/lib/growth.check.mjs
import { sipFuture, inflate, doublingYears, inr } from "./growth.js";

let bad = 0;
const ok = (name, cond) => { console.log((cond ? "OK  " : "BAD ") + name); if (!cond) bad++; };
const near = (a, b, tol = 1) => Math.abs(a - b) <= tol;

// Independent month-by-month simulation (no closed formula) to cross-check the formula.
function sim(monthly, lump, years, ratePct) {
  let bal = lump; const i = ratePct / 100 / 12;
  for (let m = 0; m < years * 12; m++) { bal += monthly; bal *= 1 + i; }
  return bal;
}
const sip = sipFuture({ monthly: 5000, years: 10, ratePct: 12 });
ok("SIP 5000/month, 10 years, 12%: matches a month-by-month simulation", near(sip.value, sim(5000, 0, 10, 12), 1));
ok("SIP invested amount is 6 lakh", sip.invested === 600000);
ok("SIP value is about 11.6 lakh", near(sip.value, 1161695, 5));
ok("SIP gain = value - invested", near(sip.gain, sip.value - 600000, 0.01));
ok("zero rate SIP = just the deposits", sipFuture({ monthly: 1000, years: 2, ratePct: 0 }).value === 24000);

const lump = sipFuture({ lump: 10000, years: 10, ratePct: 8 });
ok("10,000 at 8% for 10 years = 21,589", Math.round(lump.value) === 21589);
ok("10,000 at 8% for 20 years = 46,610", Math.round(sipFuture({ lump: 10000, years: 20, ratePct: 8 }).value) === 46610);
ok("10,000 at 8% for 30 years = 1,00,627", Math.round(sipFuture({ lump: 10000, years: 30, ratePct: 8 }).value) === 100627);

const inf = inflate({ price: 100, years: 10, ratePct: 6 });
ok("something costing 100 costs 179 after 10 years at 6%", Math.round(inf.future) === 179);
ok("1,00,000 keeps only about 55,839 of buying power after 10 years at 6%", Math.round(inflate({ price: 100000, years: 10, ratePct: 6 }).worth) === 55839);

ok("rule of 72: 8% doubles in 9 years", doublingYears(8) === 9);
ok("rule of 72: 12% doubles in 6 years", doublingYears(12) === 6);
ok("rule of 72: 6% doubles in 12 years", doublingYears(6) === 12);

ok("inr small", inr(5400) === "₹5,400");
ok("inr lakh", inr(1161695) === "₹11.62 lakh");
ok("inr crore", inr(25000000) === "₹2.5 crore");
ok("inr rounds", inr(99999.6) === "₹1 lakh");

console.log(bad ? `\nFAILED: ${bad}` : "\nALL OK");
process.exit(bad ? 1 : 0);
