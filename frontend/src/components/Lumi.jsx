import React from "react";
import { lumiMarkup } from "@/lib/lumiSvg";

// Lumi — FinLearn's bunny mascot.
// Moods: happy | cheer | celebrate | sad | nervous (worried) | angry
export default function Lumi({ size = 96, mood = "happy", className = "", style = {} }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      className={className}
      style={style}
      aria-hidden
      dangerouslySetInnerHTML={{ __html: lumiMarkup(mood) }}
    />
  );
}
