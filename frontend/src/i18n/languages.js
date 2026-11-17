// The 13 launch languages. `rtl` flips the whole layout. `native` is what the picker shows.
export const LANGUAGES = [
  { code: "en", native: "English", rtl: false },
  { code: "hi", native: "हिन्दी", rtl: false },
  { code: "es", native: "Español", rtl: false },
  { code: "fr", native: "Français", rtl: false },
  { code: "ar", native: "العربية", rtl: true },
  { code: "bn", native: "বাংলা", rtl: false },
  { code: "pt", native: "Português", rtl: false },
  { code: "ru", native: "Русский", rtl: false },
  { code: "ur", native: "اردو", rtl: true },
  { code: "id", native: "Bahasa Indonesia", rtl: false },
  { code: "de", native: "Deutsch", rtl: false },
  { code: "ja", native: "日本語", rtl: false },
  { code: "zh", native: "中文", rtl: false },
];

export const SUPPORTED = LANGUAGES.map((l) => l.code);
export const isRtl = (code) => !!LANGUAGES.find((l) => l.code === code)?.rtl;

// Map a browser locale like "pt-BR" or "zh-Hans-CN" to one of ours, else English.
export function pickSupported(locale) {
  const base = String(locale || "").toLowerCase().split(/[-_]/)[0];
  return SUPPORTED.includes(base) ? base : "en";
}
