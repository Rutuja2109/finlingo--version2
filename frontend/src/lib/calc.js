// Money calculators. Plain functions so they can be checked without the UI.

// SIP: equal amount invested at the start of every month (how AMFI-style calculators work).
export function sip(monthly, annualPct, years) {
  const n = Math.round(years * 12), i = annualPct / 1200;
  const fv = (m) => (i === 0 ? monthly * m : monthly * ((Math.pow(1 + i, m) - 1) / i) * (1 + i));
  const rows = [];
  for (let y = 1; y <= years; y++) rows.push({ year: y, invested: monthly * 12 * y, value: fv(y * 12) });
  const total = fv(n), invested = monthly * n;
  return { total, invested, gain: total - invested, rows };
}

// Monthly SIP needed to reach `target` in `years` at `annualPct`.
export function sipNeeded(target, annualPct, years) {
  const unit = sip(1, annualPct, years).total;
  return unit > 0 ? target / unit : 0;
}

// EMI on a loan: P * r * (1+r)^n / ((1+r)^n - 1)
export function emi(principal, annualPct, months) {
  const r = annualPct / 1200;
  const e = r === 0 ? principal / months : (principal * r * Math.pow(1 + r, months)) / (Math.pow(1 + r, months) - 1);
  return { emi: e, total: e * months, interest: e * months - principal };
}

// Months needed to clear the loan if you pay `payment` a month instead.
export function monthsToPayOff(principal, annualPct, payment) {
  const r = annualPct / 1200;
  if (r === 0) return Math.ceil(principal / payment);
  if (payment <= principal * r) return Infinity;
  return Math.ceil(-Math.log(1 - (principal * r) / payment) / Math.log(1 + r));
}

// Loan balance after each year, for a small chart.
export function loanBalances(principal, annualPct, months) {
  const r = annualPct / 1200, e = emi(principal, annualPct, months).emi;
  let bal = principal;
  const out = [];
  for (let m = 1; m <= months; m++) {
    bal = bal * (1 + r) - e;
    if (m % 12 === 0 || m === months) out.push({ month: m, balance: Math.max(0, bal) });
  }
  return out;
}

// Emergency fund: months of essential expenses you want covered.
export function emergency(monthlyNeeds, monthsCover, saved, monthsToBuild) {
  const target = monthlyNeeds * monthsCover;
  const gap = Math.max(0, target - saved);
  return { target, gap, monthly: monthsToBuild > 0 ? gap / monthsToBuild : 0, pct: target ? Math.min(100, Math.round((saved / target) * 100)) : 0 };
}

// "₹11.6 L", "₹1.16 Cr", "₹8,500"
export function inrShort(n) {
  const a = Math.abs(n), s = n < 0 ? "−" : "";
  if (a >= 1e7) return `${s}₹${(a / 1e7).toFixed(2)} Cr`;
  if (a >= 1e5) return `${s}₹${(a / 1e5).toFixed(2)} L`;
  return `${s}₹${Math.round(a).toLocaleString("en-IN")}`;
}
