import React from "react";

// Lumi — FinLearn's bunny mascot.
// Duolingo-style: big round head, huge expressive eyes, long ears, bold outlines.
// Moods: happy | cheer | sad | nervous | celebrate
export default function Lumi({ size = 96, mood = "happy", className = "", style = {} }) {
  const isCheer     = mood === "cheer";
  const isCelebrate = mood === "celebrate";
  const isSad       = mood === "sad";
  const isNervous   = mood === "nervous";

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      className={className}
      style={style}
      aria-hidden
    >
      {/* ── Left ear (behind head) ── */}
      <ellipse
        cx="32" cy="21" rx="11" ry="25"
        fill="#FFFBF5" stroke="#1C1C2E" strokeWidth="3"
        transform="rotate(-8 32 21)"
      />
      <ellipse
        cx="32" cy="23" rx="6" ry="17"
        fill="#FDA4AF"
        transform="rotate(-8 32 23)"
      />

      {/* ── Right ear (behind head) ── */}
      <ellipse
        cx="68" cy="21" rx="11" ry="25"
        fill="#FFFBF5" stroke="#1C1C2E" strokeWidth="3"
        transform="rotate(8 68 21)"
      />
      <ellipse
        cx="68" cy="23" rx="6" ry="17"
        fill="#FDA4AF"
        transform="rotate(8 68 23)"
      />

      {/* ── Body ── */}
      <ellipse cx="50" cy="90" rx="22" ry="14"
        fill="#FFFBF5" stroke="#1C1C2E" strokeWidth="3"/>

      {/* ── Arms / paws ── */}
      {isCelebrate ? (
        <>
          <ellipse cx="20" cy="64" rx="10" ry="7"
            fill="#FFFBF5" stroke="#1C1C2E" strokeWidth="2.5"
            transform="rotate(-45 20 64)"/>
          <ellipse cx="80" cy="64" rx="10" ry="7"
            fill="#FFFBF5" stroke="#1C1C2E" strokeWidth="2.5"
            transform="rotate(45 80 64)"/>
        </>
      ) : (
        <>
          <ellipse cx="28" cy="86" rx="10" ry="7"
            fill="#FFFBF5" stroke="#1C1C2E" strokeWidth="2.5"/>
          <ellipse cx="72" cy="86" rx="10" ry="7"
            fill="#FFFBF5" stroke="#1C1C2E" strokeWidth="2.5"/>
        </>
      )}

      {/* ── Head ── */}
      <circle cx="50" cy="57" r="32"
        fill="#FFFBF5" stroke="#1C1C2E" strokeWidth="3"/>

      {/* ── Eyes ── */}
      {isCheer || isCelebrate ? (
        /* ^_^ squint */
        <>
          <path d="M 27 53 Q 37 44 47 53"
            stroke="#1C1C2E" strokeWidth="4.5" fill="none" strokeLinecap="round"/>
          <path d="M 53 53 Q 63 44 73 53"
            stroke="#1C1C2E" strokeWidth="4.5" fill="none" strokeLinecap="round"/>
          {/* Blush */}
          <ellipse cx="28" cy="62" rx="9" ry="5.5" fill="#FB7185" opacity="0.32"/>
          <ellipse cx="72" cy="62" rx="9" ry="5.5" fill="#FB7185" opacity="0.32"/>
        </>
      ) : isSad ? (
        <>
          {/* Sad brows */}
          <path d="M 28 44 L 44 49" stroke="#1C1C2E" strokeWidth="3.5" strokeLinecap="round"/>
          <path d="M 56 49 L 72 44" stroke="#1C1C2E" strokeWidth="3.5" strokeLinecap="round"/>
          {/* Eyes — pupils drift down */}
          <circle cx="37" cy="55" r="10" fill="white" stroke="#1C1C2E" strokeWidth="2"/>
          <circle cx="63" cy="55" r="10" fill="white" stroke="#1C1C2E" strokeWidth="2"/>
          <circle cx="37" cy="55" r="7" fill="#06B6D4"/>
          <circle cx="63" cy="55" r="7" fill="#06B6D4"/>
          <circle cx="36" cy="57" r="4.5" fill="#1C1C2E"/>
          <circle cx="62" cy="57" r="4.5" fill="#1C1C2E"/>
          <circle cx="39" cy="52" r="2" fill="white"/>
          <circle cx="65" cy="52" r="2" fill="white"/>
        </>
      ) : (
        /* Happy / nervous */
        <>
          <circle cx="37" cy="54" r="10" fill="white" stroke="#1C1C2E" strokeWidth="2"/>
          <circle cx="63" cy="54" r="10" fill="white" stroke="#1C1C2E" strokeWidth="2"/>
          <circle cx="37" cy="54" r="7" fill="#06B6D4"/>
          <circle cx="63" cy="54" r="7" fill="#06B6D4"/>
          <circle cx="37" cy="54" r="4.5" fill="#1C1C2E"/>
          <circle cx="63" cy="54" r="4.5" fill="#1C1C2E"/>
          {/* Shine dots */}
          <circle cx="40" cy="51" r="2.2" fill="white"/>
          <circle cx="66" cy="51" r="2.2" fill="white"/>
          <circle cx="35" cy="55.5" r="1.1" fill="white"/>
          <circle cx="61" cy="55.5" r="1.1" fill="white"/>
          {isNervous && (
            /* Sweat drop */
            <ellipse cx="78" cy="38" rx="3.5" ry="5" fill="#93C5FD" opacity="0.9"/>
          )}
        </>
      )}

      {/* ── Nose ── */}
      <ellipse cx="50" cy="67" rx="4.5" ry="3.5" fill="#F472B6"/>

      {/* ── Mouth ── */}
      {isSad ? (
        <path d="M 42 75 Q 50 70 58 75"
          stroke="#1C1C2E" strokeWidth="2.8" fill="none" strokeLinecap="round"/>
      ) : (isCheer || isCelebrate) ? (
        <path d="M 39 72 Q 50 82 61 72"
          stroke="#1C1C2E" strokeWidth="2.8" fill="none" strokeLinecap="round"/>
      ) : (
        <path d="M 43 72 Q 50 79 57 72"
          stroke="#1C1C2E" strokeWidth="2.8" fill="none" strokeLinecap="round"/>
      )}

      {/* ── Celebrate sparkles ── */}
      {isCelebrate && (
        <>
          <text x="2"  y="30" fontSize="13">⭐</text>
          <text x="75" y="22" fontSize="11">✨</text>
          <text x="5"  y="72" fontSize="9"  opacity="0.8">✨</text>
        </>
      )}
    </svg>
  );
}
