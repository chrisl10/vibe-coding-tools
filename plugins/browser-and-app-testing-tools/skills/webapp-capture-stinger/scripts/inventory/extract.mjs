// Headless UI inventory extractor. Read-only: navigates same-origin routes and
// clicks only real tabs. Never clicks buttons, toggles, or external links.
// Writes one JSON per page state plus element crops under <inventory>/_raw.
// Designed by Legion Code Inc.
// Usage: CAPTURE_CONFIG=... [SHARD=0 SHARDS=6] [ROUTES=/a,/b] node inventory/extract.mjs
//        or: node parallel.mjs inventory/extract.mjs
import fs from "node:fs";
import { collect } from "./dom-collector.mjs";
import { redactCapture, redactText } from "../lib/redaction.mjs";
import path from "node:path";
import { assertTheme, discoverRoutes, gotoChecked, listTabs, loadConfig, log, openApp, routeSlug, settle, shard, shotOptions, captureScreenshot, slugify, tabName, withTimeout, ensurePrivateOutputDir, writePrivateCapture } from "../lib/common.mjs";
import { runOnboarding } from "../lib/onboarding.mjs";

const cfg = loadConfig();
const RAW = process.env.RAW || path.join(cfg.output.inventory, "_raw");
const CROPS = path.join(RAW, "crops");
const CROPS_PER_KEY = 2;
ensurePrivateOutputDir(cfg.output.inventory);
ensurePrivateOutputDir(CROPS);
const { browser, page } = await openApp(cfg);

// ---------------------------------------------------------------------------
// In-page collector. Returns candidates, style statistics, and CSS variables.
// ---------------------------------------------------------------------------
// ---------------------------------------------------------------------------

async function captureState(route, stateName, isFirst, scan = true) {
  const stateId = stateName;
  const scrollHeight = await page.evaluate(() => {
    let best = document.scrollingElement;
    for (const el of document.querySelectorAll("*")) {
      const oy = getComputedStyle(el).overflowY;
      if (["auto", "scroll"].includes(oy) && el.scrollHeight > el.clientHeight + 1 && el.clientWidth > innerWidth * 0.4) {
        if (el.scrollHeight > best.scrollHeight) best = el;
      }
    }
    return best.scrollHeight;
  });
  await page.mouse.move(-1, -1); // avoid incidental :hover states in crops and styles
  const data = await page.evaluate(collect, { stateId, withVars: isFirst, redactPatterns: cfg.redact.patterns, iconPattern: cfg.icons?.classPattern || "^$" });

  // Crops: first CROPS_PER_KEY instances of each rough signature in this state.
  const seen = new Map();
  let crops = 0;
  for (const c of data.candidates) {
    const key = [c.tag, c.role, c.shape, c.style.backgroundColor, c.style.borderRadius, c.style.fontSize, c.rect.w > 600 ? "wide" : "narrow"].join("|");
    const n = seen.get(key) || 0;
    seen.set(key, n + 1);
    c.sigKey = key;
    if (n >= CROPS_PER_KEY || c.rect.h > 2400) continue;
    const file = `${c.id}.png`;
    try {
      writePrivateCapture(path.join(CROPS, file), await captureScreenshot(cfg, page, { timeout: 4000 }, page.locator(`[data-ui-probe="${c.id}"]`)));
      c.crop = `crops/${file}`;
      crops++;
    } catch (error) { c.cropError = redactText(cfg, String(error.message).split("\n")[0]); }
  }
  const outFile = path.join(RAW, `${stateId}.json`);
  writePrivateCapture(outFile, JSON.stringify(redactCapture(cfg, { route, state: stateName, scrollHeight, capture: { deviceScaleFactor: cfg.browser.deviceScaleFactor || 1, screenshotScale: "device", viewport: cfg.browser.viewport, iconConfig: cfg.icons || null }, ...data }), null, 1));
  log(`  ${redactText(cfg, stateName)}: ${data.candidates.length} candidates, ${crops} crops`);
  if (scan) {
    const targets = await page.evaluate(() => {
      const found = [], visited = new Set();
      const walk = (root) => {
        for (const el of root.querySelectorAll("*")) {
          if (el.shadowRoot) walk(el.shadowRoot);
          if (visited.size >= 10000) return;
          if (visited.has(el)) continue; visited.add(el);
          if (el.scrollHeight > el.clientHeight + 1 && el.clientHeight > 80 && (el === document.scrollingElement || /auto|scroll/.test(getComputedStyle(el).overflowY))) {
            const id = `capture-scroll-${found.length}`; el.setAttribute("data-capture-scroll", id);
            found.push({ id, top: el.scrollTop, height: el.clientHeight, total: el.scrollHeight });
          }
        }
      }; walk(document); return found;
    });
    let samples = 0; const maxSamples = 12;
    try {
      for (const target of targets.slice(0, 8)) {
        for (let y = target.height; y < target.total && samples < maxSamples; y += target.height) {
          await page.evaluate(({ id, y }) => {
            const walk = (root) => { for (const el of root.querySelectorAll("*")) { if (el.getAttribute("data-capture-scroll") === id) { el.scrollTop = y; return true; } if (el.shadowRoot && walk(el.shadowRoot)) return true; } };
            walk(document);
          }, { id: target.id, y });
          await page.waitForTimeout(200);
          await captureState(route, `${stateName}__scroll-${++samples}`, false, false);
        }
      }
    } finally {
      await page.evaluate((targets) => {
        const walk = (root) => { for (const el of root.querySelectorAll("*")) { const t = targets.find((t) => t.id === el.getAttribute("data-capture-scroll")); if (t) { el.scrollTop = t.top; el.removeAttribute("data-capture-scroll"); } if (el.shadowRoot) walk(el.shadowRoot); } }; walk(document);
      }, targets);
    }
    data.coverage.scroll = { containers: targets.length, containerLimit: 8, samples, sampleLimit: maxSamples, truncated: targets.length > 8 || targets.reduce((n, t) => n + Math.max(0, Math.ceil(t.total / t.height) - 1), 0) > samples, limitation: "Bounded vertical samples can reveal virtualized items; infinite lists, horizontal virtualization and unseen rows remain unproven." };
    writePrivateCapture(outFile, JSON.stringify(redactCapture(cfg, { route, state: stateName, scrollHeight, capture: { deviceScaleFactor: cfg.browser.deviceScaleFactor || 1, screenshotScale: "device", viewport: cfg.browser.viewport, iconConfig: cfg.icons || null }, ...data }), null, 1));
  }
}

let failures = 0;
try {
  if (!process.env.SHARDS && !process.env.WEBAPP_CAPTURE_ONBOARDING_DONE) {
    await runOnboarding(cfg, page, cfg.output.screenshots || path.join(cfg.output.inventory, "screenshots"));
  }
  let routes = process.env.ROUTES ? process.env.ROUTES.split(",").filter(Boolean) : await discoverRoutes(cfg, page);
  const varsRoute = routes[0]; // CSS variables are captured once, by whichever shard owns the first route
  if (process.env.SHARDS) routes = shard(routes, Number(process.env.SHARDS))[Number(process.env.SHARD || 0)] || [];

  for (const route of routes) {
    try {
      await withTimeout((async () => {
        await gotoChecked(cfg, page, route);
        const base = routeSlug(route);
        log(redactText(cfg, route));
        await captureState(route, base, route === varsRoute);
        for (const t of (await listTabs(cfg, page, route)).filter((x) => !x.selected)) {
          await gotoChecked(cfg, page, route);
          const currentTabs = await listTabs(cfg, page, route);
          const current = currentTabs.find((candidate) => candidate.index === t.index && candidate.label === t.label && !candidate.selected)
            || currentTabs.find((candidate) => candidate.label === t.label && !candidate.selected);
          if (!current) {
            log(`  tab ${redactText(cfg, t.label)}: skipped because it is no longer available from the base route`);
            continue;
          }
          const before = page.url();
          await page.locator(`${cfg.tabs.selector}:visible`).nth(current.index).click({ timeout: 5000 });
          await settle(page);
          await assertTheme(cfg, page);
          await captureState(route, `${base}__${tabName(before, page.url(), t.label)}`, false);
        }
      })(), 15 * 60000, route);
    } catch (err) {
      failures++;
      log(redactText(cfg, `${route} ERROR ${err.message.split("\n")[0]}`));
      if (/session expired/.test(err.message)) break; // every later route would fail too
    }
  }
} finally {
  await browser.close();
}
log(failures ? `done with ${failures} route error(s)` : "done");
process.exit(failures ? 1 : 0);
