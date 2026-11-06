// Builds design/demo-practice-trading.html from the template, embedding the real Lumi mascot art.
import { readFileSync, writeFileSync } from "node:fs";
import { lumiMarkup } from "../frontend/src/lib/lumiSvg.js";

const lumi = {};
for (const m of ["happy", "cheer", "nervous", "angry"]) lumi[m] = lumiMarkup(m);
const tpl = readFileSync(new URL("./demo-practice-trading.template.html", import.meta.url), "utf8");
writeFileSync(new URL("./demo-practice-trading.html", import.meta.url), tpl.replace("/*LUMI_JSON*/{}", JSON.stringify(lumi)));
console.log("written design/demo-practice-trading.html");
