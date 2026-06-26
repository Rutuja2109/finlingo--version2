import React from "react";

// Lumi — original FinLingo mascot.
// Crystalline orb with iridescent core + minimalist face.
export default function Lumi({ size = 96, mood = "happy", className = "" }) {
  const s = size;
  const moods = {
    happy: { mouth: "M 35 60 Q 50 72 65 60", eye: 4 },
    cheer: { mouth: "M 32 58 Q 50 78 68 58", eye: 5 },
    think: { mouth: "M 38 64 L 62 64", eye: 3 },
    sad:   { mouth: "M 35 68 Q 50 58 65 68", eye: 3 },
  };
  const m = moods[mood] || moods.happy;
  const gid = `lumi-grad-${size}-${mood}`;
  const cid = `lumi-core-${size}-${mood}`;

  return (
    <svg width={s} height={s} viewBox="0 0 100 100" className={className} aria-hidden>
      <defs>
        <radialGradient id={gid} cx="50%" cy="40%" r="55%">
          <stop offset="0%" stopColor="#FFE9D6" stopOpacity="0.95" />
          <stop offset="55%" stopColor="#FFB088" stopOpacity="0.55" />
          <stop offset="100%" stopColor="#FF6B35" stopOpacity="0.25" />
        </radialGradient>
        <radialGradient id={cid} cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#FFD4B8" />
          <stop offset="45%" stopColor="#FF8A4C" />
          <stop offset="100%" stopColor="#FF4D17" />
        </radialGradient>
      </defs>
      {/* outer crystalline shell */}
      <circle cx="50" cy="50" r="42" fill={`url(#${gid})`} stroke="#FF6B35" strokeOpacity="0.35" strokeWidth="1.2"/>
      {/* core */}
      <circle cx="50" cy="50" r="26" fill={`url(#${cid})`} />
      {/* highlight */}
      <ellipse cx="42" cy="40" rx="8" ry="5" fill="#FFFFFF" opacity="0.5" />
      {/* eyes */}
      <circle cx="42" cy="52" r={m.eye} fill="#1B1B1F" />
      <circle cx="58" cy="52" r={m.eye} fill="#1B1B1F" />
      {/* mouth */}
      <path d={m.mouth} stroke="#1B1B1F" strokeWidth="2.4" fill="none" strokeLinecap="round" />
      {/* facet lines */}
      <path d="M 50 8 L 50 92" stroke="#FFFFFF" strokeOpacity="0.18" strokeWidth="0.6" />
      <path d="M 8 50 L 92 50" stroke="#FFFFFF" strokeOpacity="0.18" strokeWidth="0.6" />
    </svg>
  );
}
