import React from "react";
import { useTranslation } from "react-i18next";
import { Languages } from "lucide-react";
import { LANGUAGES } from "@/i18n/languages";
import { setLanguage } from "@/i18n";

export default function LanguagePicker() {
  const { t, i18n } = useTranslation();
  const current = (i18n.resolvedLanguage || i18n.language || "en").split("-")[0];
  return (
    <div className="rounded-3xl border bg-white p-5" data-testid="language-picker">
      <div className="flex items-center gap-2 font-display text-lg">
        <Languages className="h-5 w-5" /> {t("language.title")}
      </div>
      <p className="mt-1 text-sm text-slate-500">{t("language.hint")}</p>
      <div className="mt-3 flex flex-wrap gap-2">
        {LANGUAGES.map((l) => (
          <button
            key={l.code}
            type="button"
            onClick={async () => {
              if (current === l.code) return;
              await setLanguage(l.code);
              window.location.reload(); // lessons come from the server in the chosen language, so reload them
            }}
            data-testid={`lang-${l.code}`}
            className={`rounded-full border px-3 py-1.5 text-sm font-semibold ${
              current === l.code ? "border-orange-500 bg-orange-50 text-orange-600" : "border-slate-200 text-slate-700"
            }`}
          >
            {l.native}
          </button>
        ))}
      </div>
    </div>
  );
}
