// Money maths used by the interactive lessons (sliders). Pure functions, checked in growth.check.mjs.
// All figures are illustrations with an assumed rate, never a promise of returns.

// Future value of a monthly SIP (instalment at the start of each month) plus an optional lump sum.
export function sipFuture({ monthly = 0, lump = 0, years, ratePct }) {
  const n = Math.round(years * 12);
  const i = ratePct / 100 / 12;
  const sip = i === 0 ? monthly * n : monthly * ((Math.pow(1 + i, n) - 1) / i) * (1 + i);
  const lumpFv = lump * Math.pow(1 + ratePct / 100, years);
  const invested = monthly * n + lump;
  const value = sip + lumpFv;
  return { invested, value, gain: value - invested };
}

// What something costing `price` today will cost after `years` of inflation, and what today's money will still buy.
export function inflate({ price, years, ratePct }) {
  const f = Math.pow(1 + ratePct / 100, years);
  return { future: price * f, worth: price / f };
}

// Years for money to double at a yearly rate (rule of 72, rounded to one decimal).
export const doublingYears = (ratePct) => Math.round((72 / ratePct) * 10) / 10;

// Rupees in Indian style: 12,34,567 / lakh / crore.
export function inr(n) {
  const v = Math.round(n);
  if (v >= 1e7) return `₹${(v / 1e7).toFixed(2).replace(/\.?0+$/, "")} crore`;
  if (v >= 1e5) return `₹${(v / 1e5).toFixed(2).replace(/\.?0+$/, "")} lakh`;
  return `₹${v.toLocaleString("en-IN")}`;
}
