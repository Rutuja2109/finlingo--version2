// Money shown in the learner's own currency instead of always rupees.
// The country comes from the device region (e.g. "pt-BR" -> BR); the learner can override it later.
const COUNTRY_CURRENCY = {
  IN: "INR", US: "USD", GB: "GBP", CA: "CAD", AU: "AUD", NZ: "NZD", SG: "SGD", AE: "AED", SA: "SAR", EG: "EGP",
  PK: "PKR", BD: "BDT", ID: "IDR", JP: "JPY", CN: "CNY", RU: "RUB", BR: "BRL", PT: "EUR", ES: "EUR", FR: "EUR",
  DE: "EUR", IT: "EUR", NL: "EUR", MX: "MXN", AR: "ARS", CL: "CLP", CO: "COP", TR: "TRY", ZA: "ZAR", NG: "NGN", KE: "KES",
};

const KEY = "fl_country";

export function detectCountry() {
  try {
    const saved = localStorage.getItem(KEY);
    if (saved) return saved;
  } catch {
    /* ignore */
  }
  const loc = typeof navigator !== "undefined" ? navigator.language || "" : "";
  const m = loc.match(/[-_]([A-Za-z]{2})\b/);
  return (m ? m[1] : "IN").toUpperCase();
}

export function setCountry(code) {
  try {
    localStorage.setItem(KEY, String(code).toUpperCase());
  } catch {
    /* ignore */
  }
}

export const currencyFor = (country = detectCountry()) => COUNTRY_CURRENCY[country] || "USD";

// formatMoney(2500) -> "₹2,500" in India, "$2,500" in the US, "2.500 €" in Germany.
export function formatMoney(amount, { country, locale } = {}) {
  const loc = locale || (typeof navigator !== "undefined" ? navigator.language : "en");
  try {
    return new Intl.NumberFormat(loc, {
      style: "currency",
      currency: currencyFor(country),
      maximumFractionDigits: 0,
    }).format(amount);
  } catch {
    return `${currencyFor(country)} ${Math.round(amount)}`;
  }
}
