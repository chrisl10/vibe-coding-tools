// Local synthetic pipeline qualification. No real login, provider or external model call.
import assert from "node:assert/strict";
import fs from "node:fs";
import http from "node:http";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { spawn, execFileSync } from "node:child_process";
import test from "node:test";
import { chromiumPath, saveSessionState, routeSlug, ensurePrivateOutputDir } from "../lib/common.mjs";

const scripts = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const catalog = JSON.parse(fs.readFileSync(path.join(scripts, "../references/shadcn-catalog.json"), "utf8"));

test("seeded local capture exports, audits, map, video and complete handoff", { timeout: 240000 }, async (t) => {
  let chromium;
  try { ({ chromium } = await import("playwright-core")); await import("sharp"); }
  catch { if (process.env.WEBAPP_CAPTURE_NATIVE_REQUIRED) throw new Error("native pipeline dependencies unavailable"); t.skip("install declared runtime dependencies before native pipeline qualification"); return; }
  const executable = chromiumPath({ browser: {} });
  if (!executable) { if (process.env.WEBAPP_CAPTURE_NATIVE_REQUIRED) throw new Error("existing Chromium unavailable"); t.skip("Chromium unavailable"); return; }
  const root = process.env.CAPTURE_TEST_ARTIFACT_DIR ? path.resolve(process.env.CAPTURE_TEST_ARTIFACT_DIR) : fs.mkdtempSync(path.join(os.tmpdir(), "capture-pipeline-"));
  ensurePrivateOutputDir(root);
  const tokenValues = Object.fromEntries(catalog.themeTokens.filter((x) => x !== "radius").map((x) => [x, /foreground/.test(x) ? "#111111" : /background|card|popover|muted/.test(x) ? "#ffffff" : "#335577"]));
  let writes = 0;
  const server = http.createServer((req, res) => {
    if (!["GET", "HEAD"].includes(req.method)) { writes++; res.end("mutation"); return; }
    res.setHeader("content-type", "text/html; charset=utf-8");
    res.end(`<!doctype html><html class="light"><head><title>CAPTURE_CANARY title</title><style>
      :root{${Object.entries(tokenValues).map(([k,v]) => `--${k}:${v}`).join(";")};--radius:8px}
      html,body{margin:0;background:#fff;color:#111;font:16px Arial}main{padding:16px}.card{background:#fff;border:1px solid #335577;border-radius:8px;padding:12px;margin:8px}
      .sensitive{background:#00ff00;width:90px;height:40px}.bad-contrast{color:#eee;background:#fff}.complex{background:linear-gradient(#fff,#ddd);color:#111}
      .fixture-icon{font-family:monospace;font-variation-settings:'wght' 500;font-size:20px}button{border:2px solid #335577;background:#fff;color:#111;border-radius:8px;padding:8px}
      #virtual{height:100px;overflow:auto;border:1px solid #335577}#track{height:600px;position:relative}#rows{position:absolute;top:0;left:0;width:100%}.row{height:30px}
    </style></head><body><main><h1>Capture fixture</h1><div class="sensitive">CAPTURE_CANARY</div>
    <div class="card" title="CAPTURE_CANARY" aria-label="CAPTURE_CANARY">Visible card <span class="fixture-icon">star</span></div>
    <button>Review</button><p class="bad-contrast">Low contrast fixture</p><p class="complex">Unknown paint fixture</p><div id="shadow-host"></div>
    <div id="virtual"><div id="track"><div id="rows"></div></div></div></main><script>
    document.querySelector('#shadow-host').attachShadow({mode:'open'}).innerHTML='<button style="background:white;color:#111;border:1px solid #335577">Shadow action</button>';
    const box=document.querySelector('#virtual'),rows=document.querySelector('#rows');function render(){const n=Math.floor(box.scrollTop/30);rows.style.top=(n*30)+'px';rows.innerHTML=Array.from({length:5},(_,i)=>'<div class="row">Virtual row '+(n+i)+'</div>').join('')}box.addEventListener('scroll',render);render();
    </script></body></html>`);
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const inventory = path.join(root, "inventory"), raw = path.join(inventory, "_raw"), audit = path.join(root, "audit");
  const cfg = { app: { name: "Synthetic capture", origin, context: "Local synthetic UI fixture only", loginPath: "/login" }, auth: { storageState: path.join(root, "auth.json") }, browser: { executablePath: executable, viewport: { width: 640, height: 500 }, deviceScaleFactor: 2, colorScheme: "light", reducedMotion: "reduce", shards: 1 }, theme: { verify: { htmlClassIncludes: "light" } }, routes: { discover: "list", startPath: "/fixture", list: ["/fixture", "/a/b", "/a-b", "/Team", "/team"], maxShots: 2 }, tabs: { selector: '[role="tab"]', noTabsOnRoutes: [], notATabLabel: "^$" }, icons: { classPattern: "fixture-icon", fontName: "monospace" }, redact: { patterns: ["CAPTURE_CANARY"], maskSelectors: [".sensitive"] }, output: { screenshots: path.join(root, "screenshots"), inventory, demo: path.join(root, "demo"), audit }, ai: { describeBatchSize: 10, maxConcurrentAgents: 1 } };
  const config = path.join(root, "capture.config.json"); fs.writeFileSync(config, JSON.stringify(cfg), { mode: 0o600 });
  saveSessionState(cfg, { cookies: [], origins: [] }, {});
  const steps = [];
  const run = (script, args = [], extra = {}) => new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [path.join(scripts, script), ...args], { cwd: scripts, env: { ...process.env, CAPTURE_CONFIG: config, ...extra }, stdio: ["ignore", "pipe", "pipe"] });
    let stdout = "", stderr = ""; child.stdout.on("data", x => stdout += x); child.stderr.on("data", x => stderr += x);
    child.once("error", reject); child.once("exit", code => { steps.push({ script, code }); code === 0 ? resolve(stdout) : reject(new Error(`${script} exited ${code}: ${stderr}\n${stdout}`)); });
  });
  try {
    assert.equal(new Set(cfg.routes.list.map(routeSlug)).size, cfg.routes.list.length);
    await run("screenshots.mjs");
    const shots = fs.readdirSync(cfg.output.screenshots).filter(x => fs.statSync(path.join(cfg.output.screenshots, x)).isDirectory()); assert.equal(shots.length, cfg.routes.list.length);
    await run("inventory/extract.mjs", [], { ROUTES: "/fixture" });
    const rawStates = fs.readdirSync(raw).filter(x => x.endsWith(".json"));
    assert.ok(rawStates.length > 1, "virtualized scroll states recorded");
    const stateText = rawStates.map(x => fs.readFileSync(path.join(raw, x), "utf8")).join("\n");
    assert.ok(stateText.includes("Shadow action")); assert.ok(stateText.includes("Virtual row")); assert.ok(stateText.includes("fontVariationSettings")); assert.ok(!stateText.includes("CAPTURE_CANARY"));
    await run("inventory/cluster.mjs"); await run("inventory/tokens.mjs"); await run("inventory/tokens-dtcg.mjs"); await run("inventory/sheets.mjs"); await run("inventory/prepare-describe.mjs");
    const groups = JSON.parse(fs.readFileSync(path.join(raw, "groups.json"), "utf8")); assert.ok(groups.length > 0);
    const ai = path.join(raw, "ai");
    for (const batch of fs.readdirSync(ai).filter(x => /^batch-\d+\.json$/.test(x))) {
      const entries = JSON.parse(fs.readFileSync(path.join(ai, batch), "utf8"));
      const descriptions = entries.map(g => ({ gid: g.gid, name: `fixture-${g.gid}`, kind: "other", purpose: "Measured synthetic fixture group", anatomy: "Observed DOM", variants: "observed", states: ["default"], visual: {}, tokens_observed: [], usage: "Fixture page", same_as: [], is_noise: false, confidence: "high" }));
      fs.writeFileSync(path.join(ai, batch.replace("batch-", "desc-")), JSON.stringify(descriptions), { mode: 0o600 });
    }
    await run("inventory/prepare-merge.mjs");
    const plan = { components: groups.map(g => ({ name: `fixture-${g.gid}`, kind: "other", layer: "primitive", purpose: "Measured synthetic fixture group", anatomy: "Observed DOM", gids: [g.gid], parts: [], variants: [{ name: "default", gids: [g.gid], description: "Measured default state", visual: {} }], states: ["default"], tokens_observed: [], glyphs: [], related: [], confidence: "high" })), unassigned: [], inconsistencies: [] };
    fs.writeFileSync(path.join(ai, "components.json"), JSON.stringify(plan), { mode: 0o600 });
    await run("inventory/validate-merge.mjs"); await run("inventory/build.mjs");
    await run("audit/audit-visual.mjs"); await run("audit/audit-code.mjs", [], { SRC: path.join(scripts, "../guides") });
    await run("audit/audit-contrast.mjs", [], { ROUTES: "/fixture" });
    const contrastFile = fs.readdirSync(audit).find(x => x.endsWith("contrast-audit.json")); const contrast = JSON.parse(fs.readFileSync(path.join(audit, contrastFile), "utf8"));
    assert.ok(contrast.counts.fail > 0); assert.ok(contrast.counts.unmeasured > 0); assert.ok(contrast.counts.pass > 0);
    await run("inventory/shadcn-prepare.mjs");
    const shadcn = path.join(inventory, "shadcn");
    for (const batch of fs.readdirSync(path.join(shadcn, "batches")).filter(x => /^batch-\d+\.json$/.test(x))) {
      const entries = JSON.parse(fs.readFileSync(path.join(shadcn, "batches", batch), "utf8"));
      const maps = entries.map(x => ({ name: x.name, strategy: "custom", shadcn: [], install: [], newVariants: [], variantMap: [], customTokens: [], notes: "Synthetic fixture mapping, not an external agent result" }));
      fs.writeFileSync(path.join(shadcn, "batches", batch.replace("batch-", "map-")), JSON.stringify(maps), { mode: 0o600 });
    }
    const values = Object.fromEntries(Object.entries(tokenValues).map(([k,v]) => [k, { value: v, source: `Fixture root --${k} declaration`, reason: "Measured seeded fixture CSS variable" }]));
    fs.writeFileSync(path.join(shadcn, "theme.json"), JSON.stringify({ capturedTheme: "light", themes: { light: values, dark: null }, radius: { value: "8px", reason: "Fixture --radius" }, fonts: { sans: "Arial", mono: "monospace", icons: "monospace" }, customTokens: [], decisions: ["Synthetic fixture mappings are explicitly reviewed test data"], gaps: [] }), { mode: 0o600 });
    await run("inventory/shadcn-build.mjs");
    const demoPlan = path.join(root, "demo-plan.json");fs.writeFileSync(demoPlan, JSON.stringify({ title: "Fixture demo", approved: true, video: { width: 640, height: 500, fps: 5 }, narration: { wordsPerMinute: 140 }, scenes: [{ id: "overview", title: "Fixture overview", route: "/fixture", narration: "Local fixture overview.", actions: [{ type: "wait", ms: 500, screenshot: "overview" }] }] }), { mode: 0o600 });
    await run("demo/record-demo.mjs", [], { PLAN: demoPlan });
    const demoDir = path.join(cfg.output.demo, "fixture-demo");
    await new Promise((resolve,reject) => { const c=spawn("bash",["make-video.sh"],{cwd:demoDir,stdio:"ignore"});c.once("error",reject);c.once("exit",code=>code===0?resolve():reject(new Error("ffmpeg assembly failed"))); });
    assert.ok(fs.statSync(path.join(demoDir, "demo.mp4")).size > 0);
    await run("inventory/design-handoff.mjs", [], { OUT: path.join(root, "fixture-handoff.zip"), KEEP_PNG: "1" });
    const handoffZip = path.join(root, "fixture-handoff.zip");
    assert.ok(fs.statSync(handoffZip).size > 0);
    const handoffMembers = execFileSync("unzip", ["-Z1", handoffZip], { encoding: "utf8" }).trim().split("\n");
    const contrastJsonMember = handoffMembers.find(x => x.endsWith(`/audit/${contrastFile}`));
    const contrastMdMember = handoffMembers.find(x => x.endsWith(`/audit/${contrastFile.replace(/\.json$/, ".md")}`));
    assert.ok(contrastJsonMember && contrastMdMember, "handoff retains both contrast evidence formats");
    const handoffContrast = JSON.parse(execFileSync("unzip", ["-p", handoffZip, contrastJsonMember], { encoding: "utf8" }));
    assert.deepEqual(handoffContrast.counts, contrast.counts, "handoff retains failed and unmeasured contrast counts");
    assert.ok(execFileSync("unzip", ["-p", handoffZip, contrastMdMember], { encoding: "utf8" }).includes("Failed: 1. Unmeasured: 2."));
    assert.equal(writes, 0);
    const ledger = JSON.parse(fs.readFileSync(path.join(inventory, "ledger.json"), "utf8"));assert.equal(ledger.components.length, groups.length);
    fs.writeFileSync(path.join(root, "PIPELINE-PROOF.json"), JSON.stringify({ method: "native cached Chromium, installed ffmpeg, synthetic localhost data", steps, groups: groups.length, rawStates: rawStates.length, routes: cfg.routes.list.length, mutationRequests: writes, contrast: contrast.counts, handoffContrast: { json: contrastJsonMember, markdown: contrastMdMember, counts: handoffContrast.counts }, agentStages: "Reviewed deterministic fixture descriptions and maps, no external model run", outputs: [path.relative(root, path.join(demoDir, "demo.mp4")), "inventory/ledger.json", "fixture-handoff.zip"] }, null, 2), { mode: 0o600 });
    console.log(`Pipeline proof: ${root}`);
  } finally {
    await new Promise(resolve => server.close(resolve));
    if (!process.env.CAPTURE_TEST_ARTIFACT_DIR) fs.rmSync(root, { recursive: true, force: true });
  }
});
