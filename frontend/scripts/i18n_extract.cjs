/* Moves visible English text in every .jsx file under src into translation keys.
 *   node scripts/i18n_extract.cjs            (rewrites files, writes src/i18n/locales/en.json, scripts/i18n_manual.txt)
 * Only changes: whole-text JSX children, text attributes (placeholder/title/aria-label/alt), and plain string
 * literals shown in JSX ({cond ? "A" : "B"}). Text mixed with {values} is listed for hand conversion, never touched. */
const fs = require("fs");
const path = require("path");
const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;

const SRC = path.join(__dirname, "..", "src");
const SKIP_DIRS = [path.join(SRC, "components", "ui")];
const SKIP_FILES = new Set(["LanguagePicker.jsx", "Admin.jsx"]);
const ATTRS = new Set(["placeholder", "title", "aria-label", "alt"]);
const manual = [];
const stats = { files: 0, converted: 0 };

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (!SKIP_DIRS.includes(p)) walk(p, out);
    } else if (e.name.endsWith(".jsx") && !SKIP_FILES.has(e.name)) out.push(p);
  }
  return out;
}

const letters = (s) => (s.match(/[A-Za-zÀ-ɏ]/g) || []).length;
const looksHuman = (s) => {
  const t = s.trim();
  if (letters(t) < 2) return false;
  if (/^[a-z0-9_\-:/.#%]+$/.test(t)) return false; // class names, ids, paths
  if (/^(https?:|\/|#|data:)/.test(t)) return false;
  if (/^[a-z]+(-[a-z0-9]+)+$/.test(t)) return false;
  return true;
};
const slug = (s) =>
  s.toLowerCase().replace(/[^a-z0-9]+/g, " ").trim().split(/\s+/).slice(0, 6).join("_").slice(0, 40) || "text";

const bundle = {};
function keyFor(ns, text) {
  bundle[ns] = bundle[ns] || {};
  const base = slug(text);
  let k = base, i = 2;
  while (bundle[ns][k] !== undefined && bundle[ns][k] !== text) k = `${base}_${i++}`;
  bundle[ns][k] = text;
  return `${ns}.${k}`;
}

function componentOf(p) {
  for (let q = p; q; q = q.parentPath) {
    if (q.isFunctionDeclaration() && q.node.id && /^[A-Z]/.test(q.node.id.name)) return q;
    if ((q.isArrowFunctionExpression() || q.isFunctionExpression()) && q.parentPath.isVariableDeclarator()) {
      const id = q.parentPath.node.id;
      if (id.type === "Identifier" && /^[A-Z]/.test(id.name)) return q;
    }
    if (q.isCallExpression() && q.node.callee && /^(memo|forwardRef)$/.test(q.node.callee.name || "")) continue;
  }
  return null;
}

function processFile(file) {
  const src = fs.readFileSync(file, "utf8");
  const clash = /\b(const|let|var)\s+t\b|[(,]\s*t\s*[,)=]|\bt\s*=>|\{\s*t\s*[,}]/.test(src.replace(/useTranslation\(\)/g, "")) && !/const \{ t \} = useTranslation/.test(src);
  const FN = clash || /const \{ t: tx \} = useTranslation/.test(src) ? "tx" : "t";
  let ast;
  try {
    ast = parser.parse(src, { sourceType: "module", plugins: ["jsx"] });
  } catch (e) {
    manual.push(`${path.relative(SRC, file)}: could not parse (${e.message})`);
    return;
  }
  const ns = path.basename(file, ".jsx").replace(/[^A-Za-z0-9]/g, "").replace(/^./, (c) => c.toLowerCase());
  const rel = path.relative(SRC, file);
  const edits = [];
  const comps = new Map(); // component node -> insert position
  let hasHook = /useTranslation/.test(src);

  const need = (p, node) => {
    const c = componentOf(p);
    if (!c) {
      manual.push(`${rel}:${node.loc.start.line}: outside a component -> "${(node.value || "").toString().trim().slice(0, 60)}"`);
      return false;
    }
    const body = c.node.body;
    if (body.type !== "BlockStatement") {
      manual.push(`${rel}:${node.loc.start.line}: arrow component without a body block`);
      return false;
    }
    if (!comps.has(c.node)) {
      const text = src.slice(body.start, body.end);
      comps.set(c.node, { pos: body.start + 1, already: /useTranslation\(\)/.test(text) });
    }
    return true;
  };
  const tcall = (text) => `${FN}(${JSON.stringify(keyFor(ns, text))})`;

  traverse(ast, {
    JSXElement(p) {
      const kids = p.node.children;
      const real = kids.filter((k) => !(k.type === "JSXText" && !k.value.trim()));
      const texts = real.filter((k) => k.type === "JSXText");
      if (!texts.length) return;
      if (real.length === 1) {
        const k = real[0];
        const text = k.value.replace(/\s+/g, " ").trim();
        if (!looksHuman(text)) return;
        if (!need(p, k)) return;
        edits.push({ start: k.start, end: k.end, text: `{${tcall(text)}}` });
      } else if (real.every((k) => k.type === "JSXText" || k.type === "JSXElement" || k.type === "JSXSelfClosingElement") && texts.filter((k) => looksHuman(k.value)).length === 1) {
        // icon + label: only elements around one piece of text, so the sentence is whole
        const k = texts.find((x) => looksHuman(x.value));
        const text = k.value.replace(/\s+/g, " ").trim();
        if (!need(p, k)) return;
        // JSX drops whitespace that touches a line break, and keeps a plain space on the same line
        const lead = /^[^\S\n]+/.test(k.value) ? " " : "";
        const trail = /[^\S\n]+$/.test(k.value) ? " " : "";
        edits.push({ start: k.start, end: k.end, text: `${lead}{${tcall(text)}}${trail}` });
      } else if (
        real.every((k) => k.type === "JSXText" || (k.type === "JSXExpressionContainer" && k.expression.type !== "JSXEmptyExpression" && !/^JSX/.test(k.expression.type) && !/^(Conditional|Logical|Arrow|Function)/.test(k.expression.type))) &&
        letters(texts.map((k) => k.value).join(" ")) >= 3
      ) {
        // a sentence with values in it -> one template with {{placeholders}}, so other languages can reorder it
        if (!need(p, real[0])) return;
        const used = new Set();
        const vals = [];
        let tpl = "";
        real.forEach((k, i) => {
          if (k.type === "JSXText") { tpl += k.value.replace(/\s+/g, " "); return; }
          const ex = k.expression;
          let name = ex.type === "Identifier" ? ex.name : ex.type === "MemberExpression" && !ex.computed && ex.property.type === "Identifier" ? ex.property.name : `v${i}`;
          let n = name, c = 2;
          while (used.has(n)) n = `${name}${c++}`;
          used.add(n);
          const code = src.slice(ex.start, ex.end);
          vals.push(n === code ? n : `${n}: ${code}`);
          tpl += `{{${n}}}`;
        });
        tpl = tpl.replace(/\s+/g, " ").trim();
        const first = real[0], last = real[real.length - 1];
        edits.push({ start: first.start, end: last.end, text: `{${FN}(${JSON.stringify(keyFor(ns, tpl))}, { ${vals.join(", ")} })}` });
      } else if (texts.some((k) => looksHuman(k.value))) {
        manual.push(`${rel}:${p.node.loc.start.line}: text mixed with values -> "${texts.map((k) => k.value.trim()).filter(Boolean).join(" | ").slice(0, 80)}"`);
      }
    },
    JSXAttribute(p) {
      const v = p.node.value;
      if (!v || v.type !== "StringLiteral" || !ATTRS.has(p.node.name.name)) return;
      if (!looksHuman(v.value) || !need(p, v)) return;
      edits.push({ start: v.start, end: v.end, text: `{${tcall(v.value)}}` });
    },
    StringLiteral(p) {
      const parent = p.parent;
      let ok = false;
      if (parent.type === "JSXExpressionContainer" && p.parentPath.parent.type === "JSXElement") ok = true;
      if (parent.type === "ConditionalExpression" && (parent.consequent === p.node || parent.alternate === p.node)) {
        let up = p.parentPath;
        while (up && up.node.type === "ConditionalExpression") up = up.parentPath;
        if (up && up.node.type === "JSXExpressionContainer" && up.parentPath.parent.type === "JSXElement") ok = true;
      }
      if (parent.type === "LogicalExpression" && parent.right === p.node && p.parentPath.parent.type === "JSXExpressionContainer" && p.parentPath.parentPath.parent.type === "JSXElement") ok = true;
      if (!ok || !/\s|^[A-Z]/.test(p.node.value) || !looksHuman(p.node.value)) return;
      if (!need(p, p.node)) return;
      edits.push({ start: p.node.start, end: p.node.end, text: tcall(p.node.value) });
    },
  });

  if (!edits.length) return;
  for (const [, c] of comps) {
    if (!c.already) edits.push({ start: c.pos, end: c.pos, text: FN === "t" ? "\n  const { t } = useTranslation();" : "\n  const { t: tx } = useTranslation();" });
  }
  if (!hasHook) {
    const imps = ast.program.body.filter((n) => n.type === "ImportDeclaration");
    const last = imps[imps.length - 1];
    const at = last ? last.end : 0;
    edits.push({ start: at, end: at, text: `${last ? "\n" : ""}import { useTranslation } from "react-i18next";${last ? "" : "\n"}` });
  }
  edits.sort((a, b) => b.start - a.start || b.end - a.end);
  let out = src;
  for (const e of edits) out = out.slice(0, e.start) + e.text + out.slice(e.end);
  fs.writeFileSync(file, out);
  stats.files++;
  stats.converted += edits.filter((e) => /t[x]?\(/.test(e.text)).length;
}

for (const f of walk(SRC)) processFile(f);

const enPath = path.join(SRC, "i18n", "locales", "en.json");
const en = JSON.parse(fs.readFileSync(enPath, "utf8"));
for (const [ns, obj] of Object.entries(bundle)) en[ns] = { ...(en[ns] || {}), ...obj };
fs.writeFileSync(enPath, JSON.stringify(en, null, 2) + "\n");
fs.writeFileSync(path.join(__dirname, "i18n_manual.txt"), manual.join("\n") + "\n");
console.log(`files changed: ${stats.files}, strings moved: ${stats.converted}, left for hand conversion: ${manual.length}`);
