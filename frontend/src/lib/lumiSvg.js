// Lumi the bunny: SVG markup for each mood (viewBox 0 0 100 100).
// Cute proportions: wide round head, low-set dark sparkly eyes, blush cheeks, tiny nose and mouth.
// Scholar look: round glasses and a graduation cap with a gold tassel, drawn last so they sit on top of every mood.
const OUT = "#5A3E3E";
const FUR = "#FFF8F2";
const EAR = "#FFC2CF";
const BLUSH = "#FF9EB5";
const NOSE = "#F27C95";
const EYE = "#2B2230";
const SW = 2.2;

const ears = `
  <ellipse cx="31" cy="22" rx="9.5" ry="19" transform="rotate(-9 31 22)" fill="${FUR}" stroke="${OUT}" stroke-width="${SW}"/>
  <ellipse cx="31" cy="24" rx="4.8" ry="12.5" transform="rotate(-9 31 24)" fill="${EAR}"/>
  <ellipse cx="69" cy="22" rx="9.5" ry="19" transform="rotate(9 69 22)" fill="${FUR}" stroke="${OUT}" stroke-width="${SW}"/>
  <ellipse cx="69" cy="24" rx="4.8" ry="12.5" transform="rotate(9 69 24)" fill="${EAR}"/>`;

const body = `<ellipse cx="50" cy="91" rx="21" ry="12" fill="${FUR}" stroke="${OUT}" stroke-width="${SW}"/>`;
const head = `<ellipse cx="50" cy="58" rx="35" ry="30" fill="${FUR}" stroke="${OUT}" stroke-width="${SW}"/>`;
const nose = `<ellipse cx="50" cy="63.5" rx="3" ry="2.2" fill="${NOSE}"/>`;

const paws = (up) => up
  ? `<ellipse cx="15" cy="60" rx="6" ry="9.5" transform="rotate(-28 15 60)" fill="${FUR}" stroke="${OUT}" stroke-width="${SW}"/>
     <ellipse cx="85" cy="60" rx="6" ry="9.5" transform="rotate(28 85 60)" fill="${FUR}" stroke="${OUT}" stroke-width="${SW}"/>`
  : `<ellipse cx="32" cy="90" rx="7" ry="5" fill="${FUR}" stroke="${OUT}" stroke-width="${SW}"/>
     <ellipse cx="68" cy="90" rx="7" ry="5" fill="${FUR}" stroke="${OUT}" stroke-width="${SW}"/>`;

const cheeks = (o = 0.55, rx = 7.5, color = BLUSH) => `
  <ellipse cx="24" cy="66" rx="${rx}" ry="4.8" fill="${color}" opacity="${o}"/>
  <ellipse cx="76" cy="66" rx="${rx}" ry="4.8" fill="${color}" opacity="${o}"/>`;

const eyes = (r = 1) => `
  <ellipse cx="35" cy="55" rx="${4.6 * r}" ry="${5.8 * r}" fill="${EYE}"/>
  <circle cx="36.8" cy="52.8" r="1.9" fill="#fff"/><circle cx="33.6" cy="57.4" r="1" fill="#fff"/>
  <ellipse cx="65" cy="55" rx="${4.6 * r}" ry="${5.8 * r}" fill="${EYE}"/>
  <circle cx="66.8" cy="52.8" r="1.9" fill="#fff"/><circle cx="63.6" cy="57.4" r="1" fill="#fff"/>`;

const happyEyes = `
  <path d="M30 57 Q35 49.5 40 57" stroke="${EYE}" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M60 57 Q65 49.5 70 57" stroke="${EYE}" stroke-width="3" fill="none" stroke-linecap="round"/>`;

const smile = `<path d="M50 65.5 Q47.5 70.5 44 68 M50 65.5 Q52.5 70.5 56 68" stroke="${OUT}" stroke-width="1.9" fill="none" stroke-linecap="round"/>`;
const bigSmile = `<path d="M44 66.5 Q50 77 56 66.5 Z" fill="#E8667F" stroke="${OUT}" stroke-width="1.6" stroke-linejoin="round"/>
  <ellipse cx="50" cy="71.5" rx="3" ry="1.8" fill="#FF9EB5"/>`;
const frown = `<path d="M44 70 Q50 64.8 56 70" stroke="${OUT}" stroke-width="1.9" fill="none" stroke-linecap="round"/>`;
const wavy = `<path d="M44 68.5 q3 -3 6 0 t6 0" stroke="${OUT}" stroke-width="1.9" fill="none" stroke-linecap="round"/>`;

// Round glasses over the eyes (a thin dark frame with a faint lens tint so the eyes stay readable).
const GLASS = "#3B2F4A";
const glasses = `
  <circle cx="35" cy="56" r="9.6" fill="#BFE3FF" fill-opacity="0.18" stroke="${GLASS}" stroke-width="2.1"/>
  <circle cx="65" cy="56" r="9.6" fill="#BFE3FF" fill-opacity="0.18" stroke="${GLASS}" stroke-width="2.1"/>
  <path d="M44.4 54.5 Q50 51.5 55.6 54.5" stroke="${GLASS}" stroke-width="2" fill="none" stroke-linecap="round"/>
  <path d="M25.6 54 L21.5 52.5 M74.4 54 L78.5 52.5" stroke="${GLASS}" stroke-width="1.8" fill="none" stroke-linecap="round"/>
  <path d="M29.5 51 Q32 49.2 35 49.4" stroke="#fff" stroke-width="1.3" fill="none" stroke-linecap="round" opacity="0.8"/>
  <path d="M59.5 51 Q62 49.2 65 49.4" stroke="#fff" stroke-width="1.3" fill="none" stroke-linecap="round" opacity="0.8"/>`;

// Graduation cap: a rounded base on the forehead, a flat board on top, and a gold tassel hanging from the right.
const CAP = "#2F3B66", CAP_TOP = "#42528A", CAP_EDGE = "#222B4D", GOLD = "#FFC93C";
const cap = `
  <path d="M35 30 L35 38.5 Q50 46 65 38.5 L65 30 Z" fill="${CAP}" stroke="${OUT}" stroke-width="${SW}" stroke-linejoin="round"/>
  <path d="M23 25.5 L50 36.5 L77 25.5 L77 29.5 L50 40.5 L23 29.5 Z" fill="${CAP_EDGE}" stroke="${OUT}" stroke-width="${SW}" stroke-linejoin="round"/>
  <path d="M23 25.5 L50 14.5 L77 25.5 L50 36.5 Z" fill="${CAP_TOP}" stroke="${OUT}" stroke-width="${SW}" stroke-linejoin="round"/>
  <path d="M50 25.5 L72.5 27" stroke="${GOLD}" stroke-width="1.6" fill="none" stroke-linecap="round"/>
  <path d="M72.5 27 L72.5 41" stroke="${GOLD}" stroke-width="1.6" fill="none" stroke-linecap="round"/>
  <path d="M69.6 40.5 L75.4 40.5 L76.4 49.5 L68.6 49.5 Z" fill="${GOLD}" stroke="${OUT}" stroke-width="1.4" stroke-linejoin="round"/>
  <circle cx="50" cy="25.5" r="2.3" fill="${GOLD}" stroke="${OUT}" stroke-width="1.3"/>`;

const dress = glasses + cap;

const star = (x, y, s = 1) =>
  `<path transform="translate(${x} ${y}) scale(${s})" d="M0 -5 L1.4 -1.4 L5 0 L1.4 1.4 L0 5 L-1.4 1.4 L-5 0 L-1.4 -1.4Z" fill="#FFC93C"/>`;

const MOODS = {
  happy: () => ears + body + paws(false) + head + cheeks() + eyes() + nose + smile + dress,
  cheer: () => ears + body + paws(false) + head + cheeks(0.8) + happyEyes + nose + bigSmile + dress,
  celebrate: () => ears + body + paws(true) + head + cheeks(0.85) + happyEyes + nose + bigSmile + dress
    + star(10, 20, 1.3) + star(90, 18, 1.1) + star(8, 46, 0.8) + star(93, 44, 0.9),
  sad: () => ears + body + paws(false) + head + cheeks(0.4) + eyes(1.08)
    + `<path d="M29 48.5 L41 44.5 M59 44.5 L71 48.5" stroke="${OUT}" stroke-width="2" fill="none" stroke-linecap="round"/>`
    + `<path d="M30 62 q-3 5 0 7 q3 -2 0 -7z" fill="#8EC9FF"/>` + nose + frown + dress,
  nervous: () => ears + body + paws(false) + head + cheeks(0.45) + eyes(0.95)
    + `<path d="M29 48.5 L41 45.5 M59 45.5 L71 48.5" stroke="${OUT}" stroke-width="1.8" fill="none" stroke-linecap="round"/>`
    + `<path d="M85 40 q-4.5 6.5 0 9 q4.5 -2.5 0 -9z" fill="#9FD3FF"/>` + nose + wavy + dress,
  angry: () => ears + body + paws(false) + head
    + `<ellipse cx="50" cy="58" rx="35" ry="30" fill="#FF6B6B" opacity="0.16"/>`
    + cheeks(0.75, 8.5, "#FF6B6B") + eyes(0.82)
    + `<path d="M26 46 L42 52 M74 46 L58 52" stroke="${OUT}" stroke-width="3.2" fill="none" stroke-linecap="round"/>`
    + nose + `<path d="M44 70.5 Q50 65 56 70.5" stroke="${OUT}" stroke-width="2.2" fill="none" stroke-linecap="round"/>`
    + dress
    + `<g transform="translate(11 6)" stroke="#E5484D" stroke-width="2" fill="none" stroke-linecap="round"><path d="M77 30 q4 .5 5.5 4.5 M84 27.5 q-1 4.5 -5 5.5 M77.5 38 q4.5 -1 5.5 -5 M71 30 q.5 4.5 5.5 5.5"/></g>`,
};
MOODS.worried = MOODS.nervous;

export function lumiMarkup(mood = "happy") {
  return (MOODS[mood] || MOODS.happy)();
}

export const LUMI_MOODS = ["happy", "cheer", "celebrate", "sad", "nervous", "angry"];
