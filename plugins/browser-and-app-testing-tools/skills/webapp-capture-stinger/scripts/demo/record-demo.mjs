import { redactCapture } from "../lib/redaction.mjs";
// Record a scripted product demo: one video per scene, 3x key screenshots,
// WebVTT captions timed to the recording, a narration script, and an ffmpeg
// assembly script. The demo plan is human-approved JSON (see demo-plan.example.json).
// Designed by Legion Code Inc.
// Usage: CAPTURE_CONFIG=... PLAN=demo-plan.json node demo/record-demo.mjs
import fs from "node:fs";
import path from "node:path";
import { gotoChecked, loadConfig, log, openApp, pad, settle, shotOptions, captureScreenshot, slugify, ensurePrivateOutputDir, writePrivateCapture } from "../lib/common.mjs";

import { assertSafeDemoTarget, demoDenyPattern } from "../lib/onboarding.mjs";
import { startMaskedVideo } from "../lib/video-privacy.mjs";
import { withApprovedRequests } from "../lib/browser-policy.mjs";

const cfg = loadConfig();
if (!process.env.PLAN) throw new Error("Set PLAN=/path/to/demo-plan.json (see demo/demo-plan.example.json)");
const plan = JSON.parse(fs.readFileSync(process.env.PLAN, "utf8"));
if (!Array.isArray(plan.scenes) || !plan.scenes.length) throw new Error("plan.scenes must be a non-empty array");
if (plan.approved !== true) throw new Error('plan.approved is not true. Show the plan to the user, and set "approved": true only after they approve it.');
const ACTIONS = new Set(["wait", "hover", "click", "type", "scroll"]);
for (const [i, sc] of plan.scenes.entries()) {
  if (!sc.route || !sc.route.startsWith("/")) throw new Error(`scene ${i + 1}: route must start with /`);
  for (const a of sc.actions || []) {
    if (!ACTIONS.has(a.type)) throw new Error(`scene ${i + 1}: unknown action type "${a.type}"`);
    if (["hover", "click", "type"].includes(a.type) && !a.selector) throw new Error(`scene ${i + 1}: ${a.type} needs a selector`);
  }
}
const OUT = path.join(cfg.output.demo, slugify(redactCapture(cfg, plan.title || "demo")));
const VIDEO = { width: plan.video?.width || 1920, height: plan.video?.height || 1080 };
const WPM = plan.narration?.wordsPerMinute || 140; // 130 to 150 wpm band (research: demo section)
ensurePrivateOutputDir(cfg.output.demo);
ensurePrivateOutputDir(OUT);
ensurePrivateOutputDir(path.join(OUT, "scenes"));
ensurePrivateOutputDir(path.join(OUT, "screenshots"));

// Guard rails: a demo plan may interact, but never with destructive-looking targets.
const DENY = demoDenyPattern(plan.safety?.denyPattern);

const words = (s) => (s || "").trim().split(/\s+/).filter(Boolean).length;
const narrationMs = (s) => Math.ceil((words(s) / WPM) * 60000);
const ts = (ms) => {
  const h = Math.floor(ms / 3600000), m = Math.floor(ms / 60000) % 60, s = Math.floor(ms / 1000) % 60, x = ms % 1000;
  return `${pad(h, 2)}:${pad(m, 2)}:${pad(s, 2)}.${pad(x, 3)}`;
};

const cues = [];
const scriptLines = [`# ${plan.title}`, "", plan.summary || "", "", `Estimated narration pace: ${WPM} words per minute.`, ""];
const concat = [];
let offset = 0;

for (const [i, scene] of plan.scenes.entries()) {
  const id = `${pad(i + 1, 2)}-${slugify(redactCapture(cfg, scene.id || scene.title))}`;
  const { browser, context, page } = await openApp(
    { ...cfg, browser: { ...cfg.browser, viewport: VIDEO, deviceScaleFactor: 1 } },
    {
      slowMo: plan.video?.slowMo ?? 250, // human-watchable pacing
      // showActions: Playwright outlines each interacted element, adds an action subtitle, and draws a cursor.

    },
  );
  const recorder = await startMaskedVideo(cfg, page, path.join(OUT, "scenes", id), { fps: plan.video?.fps || 5 });
  const t0 = Date.now();
  let recording;
  try {
    await gotoChecked(cfg, page, scene.route);
    const minHold = narrationMs(scene.narration);
    for (const a of scene.actions || []) {
      const target = a.selector ? page.locator(a.selector).first() : null;
      if (target) {
        await assertSafeDemoTarget(target, a, DENY);
        const box = await target.boundingBox();
        if (box) await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2, { steps: 25 });
      }
      const interact = async () => {
      if (a.type === "click") { await target.click(); await settle(page, 5000, 600); }
      else if (a.type === "hover") await page.waitForTimeout(a.ms || 800);
      else if (a.type === "type") {
        await assertSafeDemoTarget(target, a, DENY);
        await target.pressSequentially(a.text, { delay: a.delay || 60 });
      } else if (a.type === "scroll") await page.mouse.wheel(0, a.dy || 600);
      else if (a.type === "wait") await page.waitForTimeout(a.ms || 1000);
      };
      if (plan.safety?.requests?.length) await withApprovedRequests(cfg, page, { ...plan.safety, approved: plan.approved }, interact);
      else await interact();
      if (a.screenshot) {
        writePrivateCapture(path.join(OUT, "screenshots", `${id}-${slugify(redactCapture(cfg, a.screenshot))}.png`), await captureScreenshot(cfg, page));
      }
    }
    const elapsed = Date.now() - t0;
    if (elapsed < minHold) await page.waitForTimeout(minHold - elapsed);
  } finally {
    try { recording = await recorder.stop(path.join(OUT, "scenes", `${id}.webm`)); } finally { await context.close(); await browser.close(); }
  }
  const dur = recording.durationMs;
  concat.push(`file 'scenes/${id}.mp4'`);
  if (scene.narration) cues.push(`${cues.length + 1}\n${ts(offset + 300)} --> ${ts(offset + Math.max(dur - 300, 1000))}\n${scene.narration}\n`);
  scriptLines.push(`## Scene ${i + 1}: ${scene.title}`, "", `- Route: \`${scene.route}\``, `- Recorded length: ${(dur / 1000).toFixed(1)}s (narration needs about ${(narrationMs(scene.narration) / 1000).toFixed(1)}s)`, "", `> ${scene.narration || "(no narration)"}`, "");
  offset += dur;
  log(`scene ${id}: ${(dur / 1000).toFixed(1)}s`);
}

writePrivateCapture(path.join(OUT, "captions.vtt"), redactCapture(cfg, "WEBVTT\n\n" + cues.join("\n")));
writePrivateCapture(path.join(OUT, "script.md"), redactCapture(cfg, scriptLines.join("\n")));
writePrivateCapture(path.join(OUT, "concat.txt"), concat.join("\n") + "\n");
writePrivateCapture(path.join(OUT, "plan.json"), JSON.stringify(redactCapture(cfg, plan), null, 2));
writePrivateCapture(path.join(OUT, "make-video.sh"), `#!/usr/bin/env bash
# Assemble the demo. Requires ffmpeg. Run from this directory.
set -euo pipefail
umask 077
fail() { echo "ERROR: video assembly refused unsafe input or existing output; use a fresh private output directory" >&2; exit 1; }
[[ -d scenes && ! -L scenes ]] || fail
for input in concat.txt captions.vtt scenes/*.webm; do
  [[ -f "$input" && ! -L "$input" ]] || fail
  links=$(stat -c %h "$input" 2>/dev/null || stat -f %l "$input" 2>/dev/null) || fail
  [[ "$links" == 1 ]] || fail
done
# Preflight every derived output before creating the first one.
for input in scenes/*.webm; do
  output="\${input%.webm}.mp4"
  [[ ! -e "$output" && ! -L "$output" ]] || fail
done
for output in demo-silent.mp4 demo.mp4; do
  [[ ! -e "$output" && ! -L "$output" ]] || fail
done
# 1) Normalize every clip to identical H.264 1920x1080 streams (concat demuxer needs identical codec parameters).
for f in scenes/*.webm; do
  ffmpeg -n -i "$f" -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black" \\
    -c:v libx264 -pix_fmt yuv420p -crf 20 -preset slow -r 30 -an "\${f%.webm}.mp4"
done
# 2) Concatenate without re-encoding.
ffmpeg -n -f concat -safe 1 -i concat.txt -c copy demo-silent.mp4
# 3) Soft, toggleable captions; +faststart last so playback starts before the download finishes.
ffmpeg -n -i demo-silent.mp4 -i captions.vtt -map 0:v -map 1 -c:v copy -c:s mov_text -movflags +faststart demo.mp4
# Optional narration (video stream copied, audio encoded once):
#   ffmpeg -n -i demo.mp4 -i narration.wav -map 0:v -map 1:a -map 0:s? -c:v copy -c:s copy -c:a aac -shortest -movflags +faststart demo-narrated.mp4
# Optional burned-in captions for players without subtitle tracks:
#   ffmpeg -n -i demo-silent.mp4 -vf subtitles=captions.vtt -c:v libx264 -pix_fmt yuv420p -crf 20 demo-burned.mp4
# Optional GIF preview (two-pass palette):
#   ffmpeg -n -i demo-silent.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,palettegen" palette.png
#   ffmpeg -n -i demo-silent.mp4 -i palette.png -lavfi "fps=15,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse" demo.gif
`);
fs.chmodSync(path.join(OUT, "make-video.sh"), 0o700);
log(`demo written to ${OUT}`);
