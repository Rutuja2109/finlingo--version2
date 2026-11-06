// Builds design/mascot-preview.html from the real mascot module, so the preview always matches the app.
import { writeFileSync } from "node:fs";
import { lumiMarkup, LUMI_MOODS } from "../frontend/src/lib/lumiSvg.js";

const labels = {
  happy: "Happy", cheer: "Cheering", celebrate: "Celebrating",
  sad: "Sad (missed you)", nervous: "Worried (streak at risk)", angry: "Angry (streak about to break)",
};
const cell = (m) => `<div class="c"><svg viewBox="0 0 100 100" width="150" height="150">${lumiMarkup(m)}</svg><p>${labels[m]}</p></div>`;
const small = (m, bg) => `<div class="s" style="background:${bg}"><svg viewBox="0 0 100 100" width="48" height="48">${lumiMarkup(m)}</svg></div>`;

const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lumi mascot preview</title>
<style>
body{margin:0;background:#FAFAFA;color:#18181b;font-family:system-ui,sans-serif;padding:24px 14px 50px}
h1{font-size:22px;margin:0 0 4px} .sub{color:#71717a;font-size:14px;margin:0 0 18px}
.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;max-width:640px}
.c{background:#fff;border:1px solid #e4e4e7;border-radius:20px;padding:14px;text-align:center}
.c p{margin:6px 0 0;font-size:13px;font-weight:600;color:#52525b}
.row{display:flex;gap:10px;margin-top:18px;flex-wrap:wrap}
.s{border-radius:16px;padding:8px;border:1px solid #e4e4e7}
.hero{margin-top:18px;max-width:640px;background:linear-gradient(135deg,#FF6B35,#FF8A4C,#EC4899);border-radius:24px;padding:18px;color:#fff;position:relative;overflow:hidden}
.hero h2{margin:0;font-size:20px;max-width:70%}.hero svg{position:absolute;right:6px;top:2px;opacity:.9}
</style></head><body>
<h1>Lumi, the scholar</h1><p class="sub">Now a scholar: round glasses and a graduation cap with a gold tassel. Same six moods the app uses.</p>
<div class="g">${LUMI_MOODS.map(cell).join("")}</div>
<div class="row">${small("happy", "#fff")}${small("happy", "#FF8A4C")}${small("cheer", "#10B981")}${small("angry", "#fff")}${small("sad", "#fff")}</div>
<div class="hero"><svg viewBox="0 0 100 100" width="110" height="110">${lumiMarkup("angry")}</svg><h2>Your 5-day streak ends tonight. Lumi is NOT happy.</h2></div>
</body></html>`;
writeFileSync(new URL("./mascot-preview.html", import.meta.url), html);
console.log("written design/mascot-preview.html");
