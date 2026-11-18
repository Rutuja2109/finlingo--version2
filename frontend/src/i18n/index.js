import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import { isRtl, pickSupported } from "@/i18n/languages";
import en from "@/i18n/locales/en.json";

const KEY = "fl_lang";

function stored() {
  try {
    return localStorage.getItem(KEY);
  } catch {
    return null;
  }
}

function applyDirection(code) {
  const html = document.documentElement;
  html.lang = code;
  html.dir = isRtl(code) ? "rtl" : "ltr";
}

// Other languages load on demand, so English users never download them.
async function loadLanguage(code) {
  if (code === "en" || i18n.hasResourceBundle(code, "translation")) return;
  try {
    const mod = await import(`@/i18n/locales/${code}.json`);
    i18n.addResourceBundle(code, "translation", mod.default || mod, true, true);
  } catch {
    /* a missing file just falls back to English */
  }
}

// English unless the learner chose another language in Account. Translations are switched on by choice only, until native speakers have checked them.
const initial = pickSupported(stored() || "en");

i18n.use(initReactI18next).init({
  resources: { en: { translation: en } },
  lng: "en",
  fallbackLng: "en",
  interpolation: { escapeValue: false },
  returnNull: false,
});

export async function setLanguage(code) {
  const lang = pickSupported(code);
  await loadLanguage(lang);
  await i18n.changeLanguage(lang);
  applyDirection(lang);
  try {
    localStorage.setItem(KEY, lang);
  } catch {
    /* private mode: the choice just will not stick */
  }
}

setLanguage(initial);

export default i18n;
