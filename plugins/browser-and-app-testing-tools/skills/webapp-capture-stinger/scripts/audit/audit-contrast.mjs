// Read-only computed-paint contrast heuristic. Does not certify WCAG conformance.
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { loadConfig, openApp, gotoChecked, discoverRoutes, routeSlug, ensurePrivateOutputDir, writePrivateCapture } from "../lib/common.mjs";
import { assessContrast } from "../lib/contrast.mjs";
import { redactCapture } from "../lib/redaction.mjs";

export async function collectContrast(page, cfg) {
  return page.evaluate(({ maxElements, maskSelectors, iconPattern }) => {
    const cfgIconPattern = iconPattern ? new RegExp(iconPattern) : null;
    const canvas = document.createElement("canvas"); canvas.width = canvas.height = 1;
    const paint = canvas.getContext("2d", { willReadFrequently: true });
    const rgba = (color) => {
      if (!CSS.supports("color", color)) return null;
      paint.clearRect(0, 0, 1, 1); paint.fillStyle = color; paint.fillRect(0, 0, 1, 1);
      const x = paint.getImageData(0, 0, 1, 1).data;
      return [x[0], x[1], x[2], x[3] / 255];
    };
    const over = (a, b) => {
      const opacity = a[3] + b[3] * (1 - a[3]);
      return opacity ? [...a.slice(0, 3).map((x, i) => (x * a[3] + b[i] * b[3] * (1 - a[3])) / opacity), opacity] : [0, 0, 0, 0];
    };
    const parent = (el) => el.parentElement || el.getRootNode()?.host || null;
    const backdrop = (el, includeSelf) => {
      let current = includeSelf ? el : parent(el), color = [0, 0, 0, 0];
      const unknown = [];
      while (current) {
        const style = getComputedStyle(current);
        if (color[3] < 0.999 && style.backgroundImage !== "none") unknown.push("background image or gradient");
        if (Number(style.opacity) !== 1) unknown.push("ancestor/group opacity");
        if (style.mixBlendMode !== "normal" || style.filter !== "none" || style.backdropFilter !== "none") unknown.push("filter or blend paint");
        const bg = rgba(style.backgroundColor);
        if (!bg) unknown.push("unsupported background color");
        else if (color[3] < 0.999) color = over(color, bg);
        current = parent(current);
      }
      if (color[3] < 0.999) unknown.push("transparent page canvas");
      return { color, unknown };
    };
    const elements = [], roots = [document], visited = new Set();
    while (roots.length && elements.length < maxElements) {
      const root = roots.shift();
      for (const el of root.querySelectorAll("*")) {
        if (visited.has(el)) continue;
        visited.add(el); elements.push(el);
        if (el.shadowRoot) roots.push(el.shadowRoot);
        if (elements.length >= maxElements) break;
      }
    }
    const items = [];
    for (const [index, el] of elements.entries()) {
      const rect = el.getBoundingClientRect(), style = getComputedStyle(el);
      if (!rect.width || !rect.height || style.visibility !== "visible" || style.display === "none") continue;
      if (el.matches(":disabled") || el.getAttribute("aria-disabled") === "true") continue;
      let masked = false;
      for (let current = el; current; current = parent(current)) {
        if (maskSelectors.some((s) => { try { return current.matches(s); } catch { return false; } })) { masked = true; break; }
      }
      if (masked) continue;
      const text = [...el.childNodes].filter((n) => n.nodeType === Node.TEXT_NODE).map((n) => n.textContent.trim()).filter(Boolean).join(" ");
      if (text) {
        const bg = backdrop(el, true), unknown = [...bg.unknown];
        if (Number(style.opacity) !== 1) unknown.push("text/group opacity");
        if (style.textShadow !== "none") unknown.push("text shadow");
        if (el.closest("svg,canvas")) unknown.push("graphic text paint");
        if (cfgIconPattern && cfgIconPattern.test(typeof el.className === "string" ? el.className : "")) unknown.push("icon-font glyph requires non-text classification");
        items.push({ id: `text-${index}`, kind: "text", tag: el.tagName.toLowerCase(), text: text.slice(0, 160), foreground: rgba(style.color), background: bg.color, fontSize: parseFloat(style.fontSize), fontWeight: parseFloat(style.fontWeight), unknown });
      }
      if (el.matches('button,input,select,textarea,[role="button"],[role="checkbox"],[role="switch"]')) {
        const bg = backdrop(el, false), own = rgba(style.backgroundColor);
        const border = parseFloat(style.borderTopWidth) > 0 ? rgba(style.borderTopColor) : null;
        const foreground = border?.[3] ? border : own;
        const unknown = [...bg.unknown];
        if (Number(style.opacity) !== 1 || style.filter !== "none" || style.mixBlendMode !== "normal") unknown.push("control opacity or complex paint");
        if (style.backgroundImage !== "none") unknown.push("control background image or gradient");
        if (border && border[3] < 1 && own?.[3]) unknown.push("translucent border over control fill");
        if (!foreground || foreground[3] === 0) unknown.push("no measurable painted boundary");
        if (style.appearance !== "none" && el.matches("input,select")) unknown.push("native control paint");
        items.push({ id: `ui-${index}`, kind: "ui", tag: el.tagName.toLowerCase(), foreground, background: bg.color, unknown });
      }
    }
    return { items, coverage: { inspectedElements: elements.length, limit: maxElements, truncated: elements.length >= maxElements, openShadowTraversal: true, limits: ["closed shadow roots", "opaque frames", "virtualized or unvisited states", "overlap and complex paint require manual review"] } };
  }, { maxElements: cfg.contrast?.maxElements || 6000, maskSelectors: cfg.redact?.maskSelectors || [], iconPattern: cfg.icons?.classPattern });
}

export async function runContrast(cfg, out) {
  const app = await openApp(cfg), states = [], items = [];
  try {
    const routes = process.env.ROUTES ? process.env.ROUTES.split(",").filter(Boolean) : await discoverRoutes(cfg, app.page);
    for (const route of routes) {
      await gotoChecked(cfg, app.page, route);
      const collected = await collectContrast(app.page, cfg);
      const id = routeSlug(route);
      states.push({ route, id, ...collected.coverage });
      items.push(...collected.items.map((x) => assessContrast({ ...x, route, state: id })));
    }
  } finally { await app.context.close(); await app.browser.close(); }
  const report = redactCapture(cfg, { schemaVersion: 1, method: "automated-plus-heuristic computed-paint contrast", scope: "Read-only visible DOM states, not a WCAG conformance determination", states, items, counts: { pass: items.filter((x) => x.status === "pass").length, fail: items.filter((x) => x.status === "fail").length, unmeasured: items.filter((x) => x.status === "unmeasured").length } });
  ensurePrivateOutputDir(path.dirname(out));
  writePrivateCapture(out + ".json", JSON.stringify(report, null, 2));
  const cell = (x) => String(x ?? "").replace(/\|/g, "\\|").replace(/\n/g, " ");
  const rows = report.items.filter((x) => x.status !== "pass").map((x) => `| ${cell(x.state)} | ${cell(x.id)} | ${cell(x.kind)} | ${cell(x.status)} | ${x.ratio?.toFixed(3) || "unknown"} | ${x.threshold} | ${cell(x.reasons?.join("; ") || x.criterion)} |`);
  writePrivateCapture(out + ".md", ["# Contrast review", "", report.scope, "", `Passed: ${report.counts.pass}. Failed: ${report.counts.fail}. Unmeasured: ${report.counts.unmeasured}.`, "", "| State | Element | Kind | Result | Ratio | Required | Evidence |", "| --- | --- | --- | --- | ---: | ---: | --- |", ...rows, "", "Review complex paint, overlap, missing states and unmeasured entries before any accessibility conclusion.", ""].join("\n"));
  return report;
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  const cfg = loadConfig(), out = process.env.OUT || path.join(cfg.output.audit, `${new Date().toISOString().slice(0, 10)}-contrast-audit`);
  const report = await runContrast(cfg, out);
  console.log(JSON.stringify({ output: out, counts: report.counts, states: report.states.length }));
}
