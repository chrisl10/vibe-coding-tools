// Build the component inventory deliverable from the merge plan.
// Usage: RAW=<dir with groups.json, crops/, ai/components.json, tokens-raw.json> DEST=<output dir> node build.mjs
import fs from "node:fs";
import { redactCapture, redactText } from "../lib/redaction.mjs";
import path from "node:path";
import { capturePaths, ensurePrivateOutputDir, writePrivateCapture } from "../lib/common.mjs";

const P = capturePaths();
const RAW = P.raw;
const DEST = path.resolve(process.env.DEST || P.inventory);

function noLinks(target) {
  let current = path.resolve(target);
  for (;;) {
    try {
      if (fs.lstatSync(current).isSymbolicLink()) {
        const systemAlias = process.platform === "darwin" && ["/tmp", "/var", "/etc"].includes(current);
        if (!systemAlias || fs.realpathSync(current) !== `/private${current}`) {
          throw new Error(`refusing linked inventory path: ${current}`);
        }
      }
    } catch (error) { if (error.code !== "ENOENT") throw error; }
    const parent = path.dirname(current);
    if (parent === current) break;
    current = parent;
  }
}

function contained(root, relative) {
  if (typeof relative !== "string" || !relative || relative.includes("\\") || relative.includes("\0") ||
      path.isAbsolute(relative) || path.win32.isAbsolute(relative) || relative.split("/").includes("..")) {
    throw new Error("inventory source path must be a relative contained path");
  }
  const target = path.resolve(root, relative);
  if (!target.startsWith(path.resolve(root) + path.sep)) throw new Error("inventory source escapes its root");
  noLinks(target);
  if (fs.existsSync(target) && !fs.statSync(target).isFile()) throw new Error("inventory source must be a regular file");
  return target;
}

const read = (p) => {
  noLinks(p);
  if (!fs.statSync(p).isFile()) throw new Error("inventory JSON input must be a regular file");
  return redactCapture(P.cfg, JSON.parse(fs.readFileSync(p, "utf8")));
};
noLinks(RAW);
noLinks(DEST);
const groupList = read(path.join(RAW, "groups.json"));
const plan = read(path.join(RAW, "ai", "components.json"));
const descriptions = read(path.join(RAW, "ai", "descriptions.json"));
if (!Array.isArray(groupList) || !Array.isArray(descriptions) || !Array.isArray(plan?.components)) {
  throw new Error("inventory inputs require groups[], descriptions[] and components[]");
}

function strings(value, label, optional = false) {
  if (optional && value === undefined) return;
  if (!Array.isArray(value) || value.some((item) => typeof item !== "string")) {
    throw new Error(`${label} must be an array of strings`);
  }
}
function object(value, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error(`${label} must be an object`);
}
const groupIds = new Set();
for (const g of groupList) {
  object(g, "group");
  if (typeof g.gid !== "string" || !g.gid || groupIds.has(g.gid)) throw new Error("group IDs must be unique strings");
  groupIds.add(g.gid);
  if (!Number.isFinite(g.instances) || g.instances < 0 || !Array.isArray(g.variants)) throw new Error("invalid group instances or variants");
  for (const key of ["routes", "regions"]) strings(g[key], `group ${key}`);
  for (const key of ["icons", "images"]) strings(g[key], `group ${key}`, true);
  for (const v of g.variants) {
    object(v, "group variant");
    strings(v.crops, "variant crops");
    for (const crop of v.crops) contained(RAW, crop);
    if (!Array.isArray(v.examples)) throw new Error("variant examples must be an array");
    for (const e of v.examples) {
      object(e, "variant example");
      object(e.style, "example style");
      object(e.rect, "example rect");
      if (!Number.isFinite(e.rect.w) || !Number.isFinite(e.rect.h) || typeof e.html !== "string") throw new Error("invalid example rect or HTML");
    }
  }
}
for (const d of descriptions) {
  object(d, "description");
  if (typeof d.gid !== "string") throw new Error("description gid must be a string");
}
const componentNames = new Set();
for (const c of plan.components) {
  object(c, "component");
  if (typeof c.name !== "string" || !/^[a-z0-9]+(-[a-z0-9]+)*$/.test(c.name) || componentNames.has(c.name)) {
    throw new Error("component names must be unique kebab-case names");
  }
  componentNames.add(c.name);
  for (const key of ["kind", "layer", "purpose", "confidence"]) {
    if (typeof c[key] !== "string") throw new Error(`component ${key} must be a string`);
  }
  strings(c.gids, "component gids");
  if (c.gids.some((gid) => !groupIds.has(gid))) throw new Error("component references an unknown group");
  for (const key of ["states", "tokens_observed", "glyphs", "related"]) strings(c[key], `component ${key}`, true);
  for (const key of ["variants", "parts"]) {
    if (c[key] !== undefined && !Array.isArray(c[key])) throw new Error(`component ${key} must be an array`);
    for (const b of c[key] || []) {
      object(b, "component variant/part");
      if (typeof b.name !== "string" || !b.name.trim()) throw new Error("variant/part name must be a string");
      strings(b.gids, "variant/part gids", true);
      if ((b.gids || []).some((gid) => !groupIds.has(gid))) throw new Error("variant/part references an unknown group");
      if (b.visual !== undefined && b.visual !== null) object(b.visual, "variant/part visual");
    }
  }
}
if (fs.existsSync(path.join(RAW, "tokens-raw.json"))) read(path.join(RAW, "tokens-raw.json"));
const groups = Object.fromEntries(groupList.map((g) => [g.gid, g]));
const descs = Object.fromEntries(descriptions.map((d) => [d.gid, d]));

const COMP = path.join(DEST, "components");
if (path.resolve(RAW) === DEST || path.resolve(RAW) === COMP || path.resolve(RAW).startsWith(COMP + path.sep)) {
  throw new Error("inventory output cleanup overlaps the raw input directory");
}
// Refuse unsafe output roots before any cleanup or output.
ensurePrivateOutputDir(DEST);
if (fs.existsSync(COMP)) ensurePrivateOutputDir(COMP);
if (fs.existsSync(path.join(DEST, "assets"))) ensurePrivateOutputDir(path.join(DEST, "assets"));
// Refuse every existing output link before cleaning or overwriting any output.
function checkOutputTree(target) {
  noLinks(target);
  if (!fs.existsSync(target)) return;
  if (fs.statSync(target).isDirectory()) {
    for (const name of fs.readdirSync(target)) checkOutputTree(path.join(target, name));
  }
}
checkOutputTree(COMP);
checkOutputTree(path.join(DEST, "assets"));
for (const name of ["ledger.json", "tokens-raw.json"]) noLinks(path.join(DEST, name));
fs.rmSync(COMP, { recursive: true, force: true });
ensurePrivateOutputDir(COMP);

const STYLE_KEYS = ["display", "color", "backgroundColor", "backgroundImage", "borderTopColor", "borderTopWidth", "borderTopStyle", "borderRadius", "boxShadow", "fontFamily", "fontSize", "fontWeight", "lineHeight", "letterSpacing", "textTransform", "paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "gap", "width", "height", "cursor", "opacity"];
const pick = (s) => Object.fromEntries(STYLE_KEYS.filter((k) => s?.[k] !== undefined).map((k) => [k, s[k]]));
const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "default";
const list = (a) => (a && a.length ? a.map((x) => `- ${x}`).join("\n") : "- none recorded");
const visualTable = (v) =>
  v && Object.keys(v).length
    ? "| Property | Value |\n| --- | --- |\n" + Object.entries(v).filter(([, x]) => x).map(([k, x]) => `| ${k} | ${String(x).replace(/\|/g, "\\|")} |`).join("\n")
    : "";

const h2 = (n) => Math.round(n).toString(16).padStart(2, "0");
const hexify = (v) =>
  String(v).replace(/rgba?\(\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\s*\)/g, (_, r, g, b, a) =>
    `#${h2(+r)}${h2(+g)}${h2(+b)}${a !== undefined && +a < 1 ? h2(+a * 255) : ""}`);
const cleanShadow = (v) => {
  if (!v || v === "none") return "none";
  const layers = hexify(v).split(/,(?![^(]*\))/).map((x) => x.trim()).filter((x) => !/^#[0-9a-f]{6}00\b/.test(x) && !/^#00000000/.test(x));
  return layers.length ? layers.join(", ") : "none";
};
const computedTable = (entry) => {
  const e = entry?.computed?.[0];
  if (!e) return "";
  const st = e.style;
  const border = parseFloat(st.borderTopWidth) > 0 && st.borderTopStyle !== "none" ? `${st.borderTopWidth} ${st.borderTopStyle} ${st.borderTopColor}` : "none";
  const rows = [
    ["background", st.backgroundImage && st.backgroundImage !== "none" ? `${st.backgroundColor}; image ${st.backgroundImage.slice(0, 120)}` : st.backgroundColor],
    ["text color", st.color], ["border", border], ["radius", st.borderRadius], ["shadow", st.boxShadow],
    ["font", `${st.fontSize}/${st.lineHeight} ${st.fontWeight} ${String(st.fontFamily).split(",")[0]}`],
    ["padding", `${st.paddingTop} ${st.paddingRight} ${st.paddingBottom} ${st.paddingLeft}`], ["gap", st.gap],
    ["size", `${e.rect.w} x ${e.rect.h} px`], ["page state", e.page],
  ];
  return "| Property | Value |\n| --- | --- |\n" + rows.map(([k, v]) => `| ${k} | ${(k === "shadow" ? cleanShadow(v) : hexify(v)).replace(/\|/g, "\\|")} |`).join("\n");
};

const ledger = [];
const iconGlyphs = new Map();
const images = new Map();

for (const c of plan.components) {
  const dir = path.join(COMP, c.name);
  const shots = path.join(dir, "screenshots");
  ensurePrivateOutputDir(shots);

  const allGids = [...new Set(c.gids)];
  const members = allGids.map((g) => groups[g]).filter(Boolean);
  const instances = members.reduce((n, g) => n + g.instances, 0);
  const routes = [...new Set(members.flatMap((g) => g.routes))].sort();
  const regions = [...new Set(members.flatMap((g) => g.regions))];

  const styles = {};
  const htmlBlocks = [];
  const shotList = [];
  const buckets = [
    ...(c.variants || []).map((v) => ({ kind: "variant", ...v })),
    ...(c.parts || []).map((p) => ({ kind: "part", ...p })),
  ];
  for (const b of buckets) {
    const key = `${b.kind === "part" ? "part-" : ""}${slug(b.name)}`;
    const bg = (b.gids || []).map((g) => groups[g]).filter(Boolean);
    const examples = bg.flatMap((g) => g.variants.flatMap((v) => v.examples.map((e) => ({ ...e, gid: g.gid }))));
    styles[key] = {
      description: b.description || "",
      gids: b.gids || [],
      visual: b.visual || null,
      computed: examples.slice(0, 3).map((e) => ({ gid: e.gid, page: e.state, rect: e.rect, style: pick(e.style), capture: e.capture || null })),
    };
    if (examples[0]) {
      htmlBlocks.push(`<!-- ${b.kind}: ${b.name} (gid ${examples[0].gid}, page state ${examples[0].state}) -->\n${examples[0].html}`);
    }
    let n = 0;
    for (const g of bg) {
      for (const v of g.variants) {
        for (const crop of v.crops) {
          if (n >= 3) break;
          const src = path.join(RAW, crop);
          if (!fs.existsSync(src)) continue;
          const file = `${key}-${String(++n).padStart(2, "0")}.png`;
          writePrivateCapture(path.join(shots, file), fs.readFileSync(src));
          shotList.push(`screenshots/${file}`);
        }
      }
    }
  }

  const glyphs = [...new Set([...(c.glyphs || []), ...members.flatMap((g) => g.icons || [])])].filter(Boolean);
  const imgs = [...new Set(members.flatMap((g) => g.images || []))].filter(Boolean);
  glyphs.forEach((gl) => iconGlyphs.set(gl, (iconGlyphs.get(gl) || new Set()).add(c.name)));
  imgs.forEach((src) => images.set(src, (images.get(src) || new Set()).add(c.name)));

  writePrivateCapture(path.join(dir, "code.html"), htmlBlocks.join("\n\n") + "\n");
  writePrivateCapture(path.join(dir, "styles.json"), JSON.stringify(styles, null, 1));
  const iconMetadata = [...new Map(members.flatMap((g) => g.iconMetadata || []).map((m) => [JSON.stringify(m), m])).values()];
  const captureMetadata = [...new Map(members.flatMap((g) => g.captureMetadata || []).map((m) => [JSON.stringify(m), m])).values()];
  writePrivateCapture(path.join(dir, "assets.json"), JSON.stringify({ iconFonts: [...new Set(iconMetadata.map((m) => m.fontFamily))], iconMetadata, glyphs, images: imgs, captureMetadata }, null, 1));

  const md = [
    `# ${c.name}`,
    "",
    `- **Kind:** ${c.kind}`,
    `- **Layer:** ${c.layer}`,
    `- **Instances observed:** ${instances} across ${routes.length} route(s)`,
    `- **Regions:** ${regions.join(", ")}`,
    `- **Confidence:** ${c.confidence}`,
    "",
    "## Purpose",
    "",
    c.purpose,
    "",
    "## Anatomy",
    "",
    c.anatomy,
    "",
    ...(c.parts?.length ? ["## Parts", "", ...c.parts.map((p) => `- **${p.name}:** ${p.description}`), ""] : []),
    "## Variants",
    "",
    ...(c.variants || []).flatMap((v) => [
      `### ${v.name}`, "", v.description, "",
      "Described:", "", visualTable(v.visual), "",
      ...(computedTable(styles[slug(v.name)]) ? ["Measured in the browser (first example):", "", computedTable(styles[slug(v.name)]), ""] : []),
    ]),
    "## States",
    "",
    list(c.states),
    "",
    "## Tokens observed",
    "",
    list(c.tokens_observed),
    "",
    "## Usage",
    "",
    c.usage,
    "",
    "Routes:",
    "",
    list(routes.map((r) => `\`${r}\``)),
    "",
    ...(glyphs.length ? ["## Icon glyphs", "", glyphs.map((g) => `\`${g}\``).join(", "), ""] : []),
    ...(c.related?.length ? ["## Related components", "", list(c.related.map((r) => `[${r}](../${r}/component.md)`)), ""] : []),
    ...(c.notes ? ["## Notes", "", c.notes, ""] : []),
    "## Files",
    "",
    "- `code.html`: representative markup for each variant and part (sensitive values redacted)",
    "- `styles.json`: computed styles per variant and part",
    "- `assets.json`: icon glyphs and images used",
    `- \`screenshots/\`: ${shotList.length} crops; actual scale and viewport recorded in assets.json`,
    "",
    "## Source groups",
    "",
    allGids.map((g) => `\`${g}\` (${descs[g]?.name || "?"})`).join(", "),
    "",
  ].join("\n");
  writePrivateCapture(path.join(dir, "component.md"), md);

  ledger.push({
    name: c.name, kind: c.kind, layer: c.layer, confidence: c.confidence,
    variants: (c.variants || []).map((v) => v.name), parts: (c.parts || []).map((p) => p.name),
    instances, routes, regions, related: c.related || [], sourceGroups: allGids,
    path: `components/${c.name}/`,
  });
}

ledger.sort((a, b) => a.layer.localeCompare(b.layer) || b.instances - a.instances);
writePrivateCapture(path.join(DEST, "ledger.json"), JSON.stringify({
  generated: new Date().toISOString().slice(0, 10),
  source: redactText(P.cfg, process.env.SOURCE || P.source),
  components: ledger,
  unassigned: plan.unassigned || [],
  inconsistencies: plan.inconsistencies || [],
}, null, 1));

ensurePrivateOutputDir(path.join(DEST, "assets"));
writePrivateCapture(path.join(DEST, "assets", "icons.json"), JSON.stringify({
  fonts: [...new Set(groupList.flatMap((g) => (g.iconMetadata || []).map((m) => m.fontFamily)))],
  metadata: groupList.flatMap((g) => g.iconMetadata || []),
  glyphs: [...iconGlyphs.entries()].map(([g, s]) => ({ glyph: g, usedBy: [...s] })).sort((a, b) => a.glyph.localeCompare(b.glyph)),
}, null, 1));
writePrivateCapture(path.join(DEST, "assets", "images.json"), JSON.stringify(
  [...images.entries()].map(([src, s]) => ({ src, usedBy: [...s] })), null, 1));
if (fs.existsSync(path.join(RAW, "tokens-raw.json"))) {
  writePrivateCapture(path.join(DEST, "tokens-raw.json"), JSON.stringify(read(path.join(RAW, "tokens-raw.json")), null, 1));
}
console.log(`built ${ledger.length} components, ${iconGlyphs.size} glyphs, ${images.size} images`);
