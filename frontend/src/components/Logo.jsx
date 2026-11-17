import React from "react";
import logo from "@/assets/logo.png";
import { useTranslation } from "react-i18next";

// FinLearn mark (rising bars and arrow).
export default function Logo({ size = 36, className = "" }) {
  const { t } = useTranslation();
  return <img src={logo} width={size} height={size} alt={t("logo.finlearn")} className={className} style={{ width: size, height: size }} />;
}
