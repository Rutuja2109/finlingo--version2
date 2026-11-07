import React from "react";
import logo from "@/assets/logo.png";

// FinLearn mark (rising bars and arrow).
export default function Logo({ size = 36, className = "" }) {
  return <img src={logo} width={size} height={size} alt="FinLearn" className={className} style={{ width: size, height: size }} />;
}
