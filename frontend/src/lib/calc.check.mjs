// Run: node frontend/src/lib/calc.check.mjs
import { sip, sipNeeded, emi, monthsToPayOff, loanBalances, emergency, inrShort } from "./calc.js";

let bad = 0;
const ok = (name, cond) => { console.log((cond ? "OK  " : "BAD ") + name); if (!cond) bad++; };
const near = (a, b, tol = 1) => Math.abs(a - b) <= tol;

const s = sip(5000, 12, 10);
ok("SIP 5,000/month, 12%, 10 years = about 11,61,695 (start-of-month)", near(s.total, 1161695, 5));
ok("SIP invested is 6,00,000", s.invested === 600000 && near(s.gain, s.total - 600000, 0.001));
ok("SIP rows: 10 years, last equals total", s.rows.length === 10 && near(s.rows[9].value, s.total, 0.001));
ok("SIP 0% return = money put in", sip(1000, 0, 5).total === 60000);
ok("sipNeeded is the inverse of sip", near(sip(sipNeeded(1000000, 12, 5), 12, 5).total, 1000000, 0.5));

const e = emi(1000000, 10, 60);
ok("EMI 10 lakh, 10%, 5 years = about 21,247", near(e.emi, 21247, 1));
ok("EMI interest = total - principal", near(e.interest, e.total - 1000000, 0.001) && near(e.interest, 274819, 30));
ok("EMI 0% is principal / months", emi(120000, 0, 12).emi === 10000);
const extra = monthsToPayOff(1000000, 10, e.emi * 1.1);
ok("paying 10% more finishes earlier (about 6 months sooner)", extra < 60 && extra >= 50);
ok("paying exactly the EMI takes 60 months", monthsToPayOff(1000000, 10, e.emi + 0.01) === 60);
ok("paying less than the interest never ends", monthsToPayOff(1000000, 10, 5000) === Infinity);
const lb = loanBalances(1000000, 10, 60);
ok("loan balance reaches zero at the end", lb.length === 5 && near(lb[4].balance, 0, 1));

const f = emergency(20000, 6, 30000, 9);
ok("emergency: 6 x 20,000 = 1,20,000, gap 90,000, 10,000 a month", f.target === 120000 && f.gap === 90000 && f.monthly === 10000 && f.pct === 25);
ok("emergency: already covered", emergency(10000, 3, 50000, 6).gap === 0);

ok("inrShort formats lakhs and crores", inrShort(1161695) === "₹11.62 L" && inrShort(12345678) === "₹1.23 Cr" && inrShort(8500) === "₹8,500");
console.log(bad ? `\nFAILED: ${bad}` : "\nALL PASSED");
process.exit(bad ? 1 : 0);
