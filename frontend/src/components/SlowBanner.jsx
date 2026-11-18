import React, { useEffect, useState } from "react";
import Lumi from "@/components/Lumi";
import { useTranslation } from "react-i18next";

// Shown when a request takes more than a few seconds (the free server may be waking up).
export default function SlowBanner() {
  const { t } = useTranslation();
  const [slow, setSlow] = useState(false);

  useEffect(() => {
    const on = (e) => setSlow(!!e.detail);
    window.addEventListener("fl:slow", on);
    return () => window.removeEventListener("fl:slow", on);
  }, []);

  if (!slow) return null;
  return (
    <div role="status" aria-live="polite" data-testid="slow-banner"
      className="fixed top-3 inset-x-3 z-50 mx-auto max-w-md flex items-center gap-3 rounded-2xl bg-white border border-zinc-200 shadow-lg px-4 py-3 font-[Manrope]">
      <Lumi size={36} mood="nervous" className="lumi-float" />
      <div>
        <p className="font-[Outfit] font-bold text-sm">{t("slowBanner.waking_things_up")}</p>
        <p className="text-xs text-zinc-500">{t("slowBanner.this_can_take_up_to_a")}</p>
      </div>
    </div>
  );
}
