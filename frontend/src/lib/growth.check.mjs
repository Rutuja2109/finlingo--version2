// Run: node src/lib/growth.check.mjs
import { sipFuture, inflate, doublingYears, inr, recoveryNeeded, costDrag } from "./growth.js";

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

ok("a 50% fall needs a 100% gain", Math.round(recoveryNeeded(50)) === 100);
ok("a 30% fall needs about 42.9%", near(recoveryNeeded(30), 42.857, 0.01));
ok("a 20% fall needs 25%", Math.round(recoveryNeeded(20)) === 25);
ok("a 10% fall needs about 11.1%", near(recoveryNeeded(10), 11.111, 0.01));
ok("recovery really restores the money: 100 -> 70 -> back to 100", near(70 * (1 + recoveryNeeded(30) / 100), 100, 1e-9));
const cd = costDrag({ monthly: 5000, years: 20, ratePct: 12, lowCostPct: 0.2, highCostPct: 1.5 });
ok("cost drag low plan matches simulation at 11.8%", near(cd.low, sim(5000, 0, 20, 11.8), 1));
ok("cost drag high plan matches simulation at 10.5%", near(cd.high, sim(5000, 0, 20, 10.5), 1));
ok("the costly plan ends lower", cd.high < cd.low && cd.lost > 0);
ok("same amount invested in both", cd.invested === 1200000);
// Rupee-cost averaging example used in the Stock Market lessons.
const navs = [50, 40, 25, 40, 50];
const units = navs.reduce((a, n) => a + 5000 / n, 0);
ok("SIP over NAVs 50,40,25,40,50 buys 650 units", Math.round(units) === 650);
ok("average cost is about 38.46", near(25000 / units, 38.46, 0.01));
ok("worth 32,500 when NAV is back to 50", Math.round(units * 50) === 32500);

console.log(bad ? `\nFAILED: ${bad}` : "\nALL OK");
process.exit(bad ? 1 : 0);
