// Package a Claude Design handoff: component library, candidate tokens, audit findings,
// page screenshots, and filled CLAUDE-DESIGN-INSTRUCTIONS.md, zipped for upload.
// Images are converted to lossless WebP (pixel-identical, smaller) unless KEEP_PNG=1.
// Designed by Legion Code Inc.
// Usage: CAPTURE_CONFIG=... node inventory/design-handoff.mjs
//   env: OUT=<zip path>  SHOTS_PER_COMPONENT=4  KEEP_PNG=1  SCREENSHOTS=<dir of route screenshots>
import fs from "node:fs";
import { createHash } from "node:crypto";
import { noLinks, safeMember, portableMember } from "./validation.mjs";
import { redactCapture, redactText } from "../lib/redaction.mjs";
import os from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { capturePaths, log, slugify, ensurePrivateOutputDir, writePrivateCapture } from "../lib/common.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const P = capturePaths();
const cfg = P.cfg;
const INV = P.inventory;
const ledgerPath = path.join(INV, "ledger.json");
if (!fs.existsSync(ledgerPath)) throw new Error(`${ledgerPath} not found: build the component library first (inventory/build.mjs)`);
noLinks(ledgerPath);
const ledger = redactCapture(P.cfg, JSON.parse(fs.readFileSync(ledgerPath, "utf8")));
noLinks(P.tokensRaw);
const tokensRaw = fs.existsSync(P.tokensRaw) ? redactCapture(P.cfg, JSON.parse(fs.readFileSync(P.tokensRaw, "utf8"))) : null;
const appName = redactText(cfg, cfg?.app?.name || "App");
const stamp = P.today;
const OUT = path.resolve(process.env.OUT || path.join(INV, `${slugify(appName)}-claude-design-handoff-${stamp}.zip`));
const SHOTS = Number(process.env.SHOTS_PER_COMPONENT || 4);
if (!Number.isInteger(SHOTS) || SHOTS < 1 || SHOTS > 100) throw new Error("SHOTS_PER_COMPONENT must be between 1 and 100");
noLinks(OUT);
if (fs.existsSync(OUT)) throw new Error("handoff output exists; choose a new OUT path rather than overwriting it");
if (!Array.isArray(ledger.components) || !ledger.components.length || !Array.isArray(ledger.unassigned || []) || ledger.unassigned?.length) throw new Error("handoff requires a nonempty complete ledger with zero unassigned groups");
const names = new Set();
for (const c of ledger.components) {
  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(c.name || "") || names.has(c.name) || c.path !== `components/${c.name}/`) throw new Error("ledger component names/paths must be unique canonical components/name/ paths");
  names.add(c.name); const dir = safeMember(INV, c.path, true);
  for (const f of ["component.md", "styles.json", "assets.json", "code.html"]) safeMember(dir, f);
  const shots = safeMember(dir, "screenshots", true);
  if (!fs.readdirSync(shots).some((f) => /\.(png|webp)$/i.test(f))) throw new Error(`component ${c.name} has no screenshot; rerun extraction/build`);
}
const contextFiles = (process.env.HANDOFF_FILES || "").split(",").filter(Boolean).map((file) => path.resolve(file));
const contextPortableNames = new Set();
for (const file of contextFiles) {
  noLinks(file); const name = portableMember(path.basename(file)).normalize("NFC").toLowerCase();
  if (contextPortableNames.has(name)) throw new Error("handoff context filenames must be unique across portable extraction targets");
  contextPortableNames.add(name);
}
const inspectTree = (dir) => {
  noLinks(dir); if (!fs.existsSync(dir)) return;
  const names = new Set();
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    portableMember(entry.name);
    const folded = entry.name.normalize("NFC").toLowerCase();
    if (names.has(folded)) throw new Error("handoff source contains case-insensitive filename collisions");
    names.add(folded);
    const file = path.join(dir, entry.name); noLinks(file);
    if (entry.isDirectory()) inspectTree(file);
    else if (!entry.isFile()) throw new Error("handoff input must contain only regular files/directories");
  }
};
for (const dir of [path.join(INV, "components"), path.join(INV, "assets"), path.join(INV, "shadcn"), P.audit, process.env.SCREENSHOTS || cfg?.output?.screenshots]) if (dir) inspectTree(dir);
for (const f of ["candidate.tokens.json", "tokens-raw.json"]) noLinks(path.join(INV, f));
const keepPng = process.env.KEEP_PNG === "1";

let sharp = null;
if (!keepPng) { try { sharp = (await import("sharp")).default; } catch { log("sharp not installed: images stay PNG"); } }

const stage = fs.mkdtempSync(path.join(os.tmpdir(), "claude-design-handoff-"));
const root = path.join(stage, `${slugify(appName)}-claude-design-handoff`);
portableMember(path.basename(root));
ensurePrivateOutputDir(root);
const copyText = (src, dst) => {
  portableMember(path.relative(root, dst).split(path.sep).join("/"));
  noLinks(src);
  const text = fs.readFileSync(src, "utf8");
  let safe;
  if (path.extname(src) === ".json") safe = JSON.stringify(redactCapture(cfg, JSON.parse(text)), null, 1);
  else safe = redactText(cfg, text);
  writePrivateCapture(dst, safe);
};
const copyImage = async (src, destNoExt) => {
  portableMember(path.relative(root, destNoExt).split(path.sep).join("/"));
  if (sharp) {
    const dest = `${destNoExt}.webp`;
    writePrivateCapture(dest, await sharp(src).webp({ lossless: true, effort: 4 }).toBuffer());
    return path.basename(dest);
  }
  const dest = `${destNoExt}${path.extname(src)}`;
  writePrivateCapture(dest, fs.readFileSync(src));
  return path.basename(dest);
};
const rewriteRefs = (text, renames) => renames.reduce((t, [a, b]) => t.split(a).join(b), text);

// 1) Components: markdown, styles, assets, markup, and a capped set of screenshots.
let imageCount = 0;
for (const c of ledger.components) {
  const src = path.join(INV, c.path);
  const dst = path.join(root, "components", c.name);
  safeMember(INV, c.path, true);
  ensurePrivateOutputDir(path.join(dst, "screenshots"));
  for (const f of ["styles.json", "assets.json", "code.html"]) {
    if (fs.existsSync(path.join(src, f))) copyText(path.join(src, f), path.join(dst, f));
  }
  const shotDir = path.join(src, "screenshots");
  const shots = fs.existsSync(shotDir) ? fs.readdirSync(shotDir).filter((f) => /\.(png|webp)$/i.test(f)).sort() : [];
  // Keep the first shot of each variant or part, then fill up to the cap.
  const firsts = shots.filter((f) => /-01\.(png|webp)$/i.test(f));
  const chosen = [...new Set([...firsts, ...shots])].slice(0, Math.max(SHOTS, firsts.length));
  const renames = [];
  for (const f of chosen) {
    const out = await copyImage(path.join(shotDir, f), path.join(dst, "screenshots", f.replace(/\.(png|webp)$/i, "")));
    if (out !== f) renames.push([`screenshots/${f}`, `screenshots/${out}`]);
    imageCount++;
  }
  const md = redactText(cfg, fs.readFileSync(path.join(src, "component.md"), "utf8"));
  writePrivateCapture(path.join(dst, "component.md"), rewriteRefs(md, renames));
}
writePrivateCapture(path.join(root, "ledger.json"), JSON.stringify(ledger, null, 1));

// 2) Tokens: candidate DTCG file plus a readable summary.
ensurePrivateOutputDir(path.join(root, "tokens"));
const candidate = path.join(INV, "candidate.tokens.json");
if (fs.existsSync(candidate)) copyText(candidate, path.join(root, "tokens", "candidate.tokens.json"));
const top = (key, n = 12) => (tokensRaw?.observed?.[key] || []).slice(0, n).map((e) => `| \`${e.value}\` | ${e.count} | ${e.routes} |`).join("\n");
if (tokensRaw) {
  const section = (title, key, n) => `## ${title}\n\n| Value | Uses | Routes |\n| --- | --- | --- |\n${top(key, n) || "| none observed | | |"}\n`;
  writePrivateCapture(path.join(root, "tokens", "tokens-summary.md"), [
    `# Observed token summary: ${appName}`, "",
    `${tokensRaw.generatedFrom.states} page states across ${tokensRaw.generatedFrom.routes} routes, ${tokensRaw.generatedFrom.theme} theme. Counts are text or box occurrences.`, "",
    section("Text colors", "color", 15), section("Background colors", "backgroundColor", 15), section("Border colors", "borderColor", 10),
    section("Font sizes", "fontSize", 15), section("Font weights", "fontWeight", 8), section("Line heights", "lineHeight", 10),
    section("Font families", "fontFamily", 5), section("Border radius", "borderRadius", 10), section("Spacing", "spacing", 20), section("Box shadows", "boxShadow", 8),
  ].join("\n"));
}

// 3) Audit reports (visual and code) from the configured audit folder, newest first.
ensurePrivateOutputDir(path.join(root, "audit"));
let hasCodeAudit = false;
let auditFiles = [];
if (fs.existsSync(P.audit)) {
  auditFiles = fs.readdirSync(P.audit).filter((f) => /(visual-audit|code-ui-audit|contrast-audit|ui-inconsistency-report)\.(md|json)$/.test(f)).sort().reverse();
  const latest = new Map();
  for (const f of auditFiles) {
    const kind = f.replace(/^\d{4}-\d{2}-\d{2}-/, "");
    if (!latest.has(kind)) latest.set(kind, f);
  }
  for (const f of latest.values()) {
    copyText(path.join(P.audit, f), path.join(root, "audit", f));
    if (f.includes("code-ui-audit")) hasCodeAudit = true;
  }
}
if (!fs.readdirSync(path.join(root, "audit")).length) {
  writePrivateCapture(path.join(root, "audit", "README.md"), "No audit reports were found when this package was built. Run the audit route to add them.\n");
}

// 4) Page screenshots: the first scroll shot of every route and tab state.
const shotsRoot = process.env.SCREENSHOTS || cfg?.output?.screenshots;
let pageCount = 0;
if (shotsRoot && fs.existsSync(shotsRoot)) {
  ensurePrivateOutputDir(path.join(root, "pages"));
  const walk = (dir) => fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? walk(path.join(dir, e.name)) : /-001\.png$/.test(e.name) ? [path.join(dir, e.name)] : []);
  for (const file of walk(shotsRoot).sort()) {
    await copyImage(file, path.join(root, "pages", `${path.basename(file).replace(/-001\.png$/, "")}-${createHash("sha256").update(path.relative(shotsRoot, file)).digest("hex").slice(0, 10)}`));
    pageCount++;
  }
  const onboarding = path.join(shotsRoot, "_onboarding");
  if (fs.existsSync(onboarding)) {
    for (const file of fs.readdirSync(onboarding).filter((name) => /\.png$/i.test(name)).sort()) {
      await copyImage(path.join(onboarding, file), path.join(root, "pages", `onboarding-${file.replace(/\.png$/i, "")}`));
      pageCount++;
    }
  }
}

// Optional project context files, supplied explicitly by the caller. These are
// copied as evidence only and never discovered from the source tree implicitly.
if (contextFiles.length) {
  ensurePrivateOutputDir(path.join(root, "context"));
  const contextNames = new Set();
  const sensitiveName = /(^|[._-])(env|auth|session|credential|secret|private[-_ ]?key)([._-]|$)|\.(pem|key|p12|pfx)$/i;
  const allowedExt = new Set([".md", ".txt", ".json"]);
  const redactPatterns = (cfg?.redact?.patterns || []).map((pattern) => new RegExp(pattern, "gi"));
  for (const file of contextFiles) {
    if (!fs.existsSync(file) || !fs.statSync(file).isFile()) throw new Error(`handoff context file not found: ${file}`);
    noLinks(file);
    if (fs.lstatSync(file).isSymbolicLink()) throw new Error(`handoff context file cannot be a symbolic link: ${file}`);
    const name = path.basename(file);
    if (contextNames.has(name.normalize("NFC").toLowerCase())) throw new Error(`handoff context filenames must be unique: ${name}`);
    if (sensitiveName.test(name)) throw new Error(`refusing sensitive-looking handoff context file: ${name}`);
    if (!allowedExt.has(path.extname(name).toLowerCase())) throw new Error(`handoff context file must be Markdown, plain text or JSON; convert unsupported formats before review: ${name}`);
    if (fs.statSync(file).size > 5 * 1024 * 1024) throw new Error(`handoff context file exceeds 5 MB: ${name}`);
    const content = fs.readFileSync(file, "utf8");
    for (const pattern of redactPatterns) {
      pattern.lastIndex = 0;
      if (pattern.test(content)) throw new Error(`handoff context file matches a configured redaction pattern: ${name}`);
    }
    copyText(file, path.join(root, "context", name));
    contextNames.add(name.normalize("NFC").toLowerCase());
  }
}

// 5) Assets, and the shadcn/ui map when one has been generated.
if (fs.existsSync(path.join(INV, "assets"))) {
  const copyAssets = (src, dst) => {
    ensurePrivateOutputDir(dst);
    for (const e of fs.readdirSync(src, { withFileTypes: true })) {
      const from = path.join(src, e.name), to = path.join(dst, e.name); noLinks(from);
      if (e.isDirectory()) copyAssets(from, to);
      else if (/\.(json|md|txt|html|css|svg)$/i.test(e.name)) copyText(from, to);
      else if (/\.(png|webp|jpg|jpeg|gif|avif|woff|woff2|ttf|otf)$/i.test(e.name)) writePrivateCapture(to, fs.readFileSync(from));
      else throw new Error("unsupported handoff asset type; convert text evidence to reviewed JSON or Markdown");
    }
  }; copyAssets(path.join(INV, "assets"), path.join(root, "assets"));
}
const hasShadcn = fs.existsSync(path.join(INV, "shadcn", "shadcn-map.json"));
if (hasShadcn) {
  ensurePrivateOutputDir(path.join(root, "shadcn"));
  for (const f of ["SHADCN-MAP.md", "shadcn-map.json", "globals.css", "theme.json"]) {
    if (fs.existsSync(path.join(INV, "shadcn", f))) copyText(path.join(INV, "shadcn", f), path.join(root, "shadcn", f));
  }
}

// 6) Instructions.
const byLayer = {};
for (const c of ledger.components) byLayer[c.layer] = (byLayer[c.layer] || 0) + 1;
const iconsFile = path.join(INV, "assets", "icons.json");
const icons = fs.existsSync(iconsFile) ? JSON.parse(fs.readFileSync(iconsFile, "utf8")) : null;
const keyNumbers = [
  `- ${ledger.components.length} components (${Object.entries(byLayer).map(([k, v]) => `${v} ${k}`).join(", ")}), ${(ledger.unassigned || []).length} unassigned groups`,
  tokensRaw ? `- ${tokensRaw.observed.color?.length || 0} text colors, ${tokensRaw.observed.backgroundColor?.length || 0} background colors, ${tokensRaw.observed.fontSize?.length || 0} font sizes, ${tokensRaw.observed.borderRadius?.length || 0} radii, ${tokensRaw.observed.boxShadow?.length || 0} shadows observed` : "",
  icons ? `- ${icons.glyphs.length} icon glyphs (${(icons.fonts || [icons.font].filter(Boolean)).join(", ") || "none observed"})` : "",
  `- ${pageCount} page screenshots, ${imageCount} component screenshots`,
].filter(Boolean).join("\n");
const topInconsistencies = (ledger.inconsistencies || []).slice(0, 15).map((x, i) => `${i + 1}. ${typeof x === "string" ? x : JSON.stringify(x)}`).join("\n") || "None recorded in the ledger; see `audit/`.";
const template = fs.readFileSync(path.join(here, "../../references/prompts/claude-design-handoff.md"), "utf8").replace(/^<!-- Template\..*?-->\s*/s, "");
const fill = {
  APP_NAME: appName,
  APP_CONTEXT: cfg?.app?.context || "a web application",
  DATE: stamp,
  ORIGIN: cfg?.app?.origin || "the captured origin",
  THEME: tokensRaw?.generatedFrom?.theme || cfg?.browser?.colorScheme || "default",
  ROUTES: String(tokensRaw?.generatedFrom?.routes ?? "?"),
  STATES: String(tokensRaw?.generatedFrom?.states ?? "?"),
  COMPONENTS: String(ledger.components.length),
  ICON_FONT: (icons?.fonts || [icons?.font].filter(Boolean)).join(", ") || cfg?.icons?.fontName || "none observed",
  SHADCN_ROW: hasShadcn ? "| `shadcn/` | A component-by-component map onto shadcn/ui (`shadcn-map.json`, `SHADCN-MAP.md`) and a draft `globals.css` theme | Use it so the system you design can be implemented directly with shadcn/ui |\n" : "",
  CODE_AUDIT_NOTE: hasCodeAudit ? ", plus code-level findings (hardcoded colors, one-off values, repeated class lists)" : "",
  KEY_NUMBERS: keyNumbers,
  TOP_INCONSISTENCIES: topInconsistencies,
};
writePrivateCapture(path.join(root, "CLAUDE-DESIGN-INSTRUCTIONS.md"), redactText(cfg, template.replace(/\{\{(\w+)\}\}/g, (m, k) => (k in fill ? fill[k] : m))));

// 7) Bind the exact packaged payload to a coverage and hash manifest.
const files = [];
const manifestWalk = (dir) => {
  fs.chmodSync(dir, 0o700);
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const file = path.join(dir, e.name); noLinks(file);
    portableMember(path.relative(root, file).split(path.sep).join("/"));
    if (e.isDirectory()) manifestWalk(file);
    else {
      const rel = path.relative(root, file).split(path.sep).join("/");
      if (redactText(cfg, rel) !== rel) throw new Error("handoff filename matches a redaction rule; rebuild with safe names");
      fs.chmodSync(file, 0o600);
      files.push({ path: rel, bytes: fs.statSync(file).size, sha256: createHash("sha256").update(fs.readFileSync(file)).digest("hex") });
    }
  }
};
manifestWalk(root);
writePrivateCapture(path.join(root, "handoff-manifest.json"), JSON.stringify({ version: 1, components: ledger.components.map((c) => ({ name: c.name, path: c.path })), componentCount: names.size, componentScreenshots: imageCount, pageScreenshots: pageCount, files: files.sort((a, b) => a.path.localeCompare(b.path)) }, null, 2));
const temporaryZip = path.join(stage, "handoff.zip");
try { execFileSync("zip", ["-qr", temporaryZip, path.basename(root)], { cwd: stage, stdio: "pipe" }); }
catch { execFileSync("tar", ["-a", "-cf", temporaryZip, path.basename(root)], { cwd: stage, stdio: "pipe" }); }
fs.chmodSync(temporaryZip, 0o600);
ensurePrivateOutputDir(path.dirname(OUT));
noLinks(OUT);
try { fs.linkSync(temporaryZip, OUT); }
catch (error) {
  if (error.code !== "EXDEV") throw error;
  const fd = fs.openSync(OUT, "wx", 0o600);
  try { fs.writeFileSync(fd, fs.readFileSync(temporaryZip)); }
  finally { fs.closeSync(fd); }
}
const bytes = fs.statSync(OUT).size;
fs.rmSync(stage, { recursive: true, force: true });
log(`Claude Design handoff: ${OUT}`);
log(`${ledger.components.length} components, ${imageCount} component screenshots, ${pageCount} page screenshots, ${(bytes / 1048576).toFixed(1)} MB`);
if (bytes > 200 * 1048576) log("WARNING: over 200 MB. Rerun with SHOTS_PER_COMPONENT=2 to shrink it.");
console.log(JSON.stringify({ zip: OUT, megabytes: +(bytes / 1048576).toFixed(1), components: ledger.components.length, componentScreenshots: imageCount, pageScreenshots: pageCount }));
