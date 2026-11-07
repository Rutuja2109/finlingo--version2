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

// After a fall of `lossPct`, the gain needed just to get back to where you started (a 50% fall needs a 100% gain).
export const recoveryNeeded = (lossPct) => (lossPct >= 100 ? Infinity : (1 / (1 - lossPct / 100) - 1) * 100);

// The same monthly investing in a cheap plan versus a costly one: costs come off the yearly return.
export function costDrag({ monthly, years, ratePct, lowCostPct, highCostPct }) {
  const low = sipFuture({ monthly, years, ratePct: ratePct - lowCostPct });
  const high = sipFuture({ monthly, years, ratePct: ratePct - highCostPct });
  return { low: low.value, high: high.value, lost: low.value - high.value, invested: low.invested };
}

// Years for money to double at a yearly rate (rule of 72, rounded to one decimal).
export const doublingYears = (ratePct) => Math.round((72 / ratePct) * 10) / 10;

// Rupees in Indian style: 12,34,567 / lakh / crore. `u` can rename the units (e.g. Hindi: { lakh: "लाख", crore: "करोड़" }).
export function inr(n, u = {}) {
  const lakh = u.lakh || "lakh";
  const crore = u.crore || "crore";
  const v = Math.round(n);
  if (v >= 1e7) return `₹${(v / 1e7).toFixed(2).replace(/\.?0+$/, "")} ${crore}`;
  if (v >= 1e5) return `₹${(v / 1e5).toFixed(2).replace(/\.?0+$/, "")} ${lakh}`;
  return `₹${v.toLocaleString("en-IN")}`;
}
