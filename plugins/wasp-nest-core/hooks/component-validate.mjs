#!/usr/bin/env node
/** Bounded post-edit validation advisory for source components. */

import { execFileSync } from "node:child_process";
import { existsSync, readFileSync, readSync } from "node:fs";
import { relative, resolve, sep } from "node:path";
import { performance } from "node:perf_hooks";

const MAX_INPUT_BYTES = 262144;
const MAX_TARGETS = 20;
const BUDGET_MS = 4000;
const started = performance.now();

function payload() {
  try {
    const buffer = Buffer.alloc(MAX_INPUT_BYTES + 1);
    let size = 0;
    while (size < buffer.length) {
      const count = readSync(0, buffer, size, buffer.length - size, null);
      if (!count) break;
      size += count;
    }
    if (size > MAX_INPUT_BYTES) return { validation_input_limit: true };
    const data = JSON.parse(buffer.subarray(0, size).toString("utf8"));
    return data && typeof data === "object" && !Array.isArray(data) ? data : {};
  } catch { return {}; }
}

function isCursor(data) {
  const event = data.hook_event_name || data.hookEventName;
  return Boolean(data.cursor_version || data.cursorVersion) ||
    (typeof event === "string" && event.startsWith("post"));
}

function emit(data, message = "") {
  if (!message) process.stdout.write("{}");
  else if (isCursor(data)) process.stdout.write(JSON.stringify({ additional_context: message }));
  else process.stdout.write(JSON.stringify({ systemMessage: message }));
  process.exit(0);
}

function patchPaths(command) {
  return (typeof command === "string" ? command : "").split(/\r?\n/)
    .map((line) => line.match(/^\*\*\* (?:Add|Update) File: (.+)$/)?.[1]?.trim())
    .filter(Boolean);
}

const data = payload();
if (data.validation_input_limit) emit(data, "Wasp Nest validation unavailable: edit payload exceeds the bounded input size. The edit remains unverified.");
const input = data.tool_input || data.toolInput || {};
const paths = (input.command ? patchPaths(input.command) :
  [input.file_path, input.filePath, input.path])
  .filter((value) => typeof value === "string" && value);
if (!paths.length) emit(data);

const pluginRoot = process.env.PLUGIN_ROOT || process.env.CLAUDE_PLUGIN_ROOT || process.cwd();
const candidates = [
  resolve(pluginRoot, "skills/queen-wasp-stinger/references/scripts/per-type-validation.py"),
  resolve(pluginRoot, "src/skills/queen-wasp-stinger/references/scripts/per-type-validation.py"),
  resolve(process.cwd(), "src/skills/queen-wasp-stinger/references/scripts/per-type-validation.py"),
  resolve(pluginRoot, ".claude/skills/queen-wasp-stinger/references/scripts/per-type-validation.py"),
  resolve(pluginRoot, ".agents/skills/queen-wasp-stinger/references/scripts/per-type-validation.py"),
  resolve(pluginRoot, ".zcode/skills/queen-wasp-stinger/references/scripts/per-type-validation.py"),
  resolve(process.cwd(), ".claude/skills/queen-wasp-stinger/references/scripts/per-type-validation.py"),
  resolve(process.cwd(), ".agents/skills/queen-wasp-stinger/references/scripts/per-type-validation.py"),
  resolve(process.cwd(), ".zcode/skills/queen-wasp-stinger/references/scripts/per-type-validation.py"),
];
const validator = candidates.find(existsSync);

// Fail-open: this runs on every edit, so an unexpected payload shape must produce an
// empty result rather than an uncaught throw. `target` is rebuilt from the regex match
// (never from the raw path) and passed to execFileSync as an argv element, so it can
// carry neither a shell metacharacter nor a traversal into the validator invocation.
const failures = [];
try {
  const targets = new Map();
  for (const path of paths) {
    const rel = relative(process.cwd(), path).split(sep).join("/");
    const match = rel.match(/^(src|\.(?:claude|cursor|agents|codex|zcode)|packs\/[a-z0-9]+(?:-[a-z0-9]+)*)\/(skills\/[a-z0-9]+(?:-[a-z0-9]+)*|agents\/[a-z0-9]+(?:-[a-z0-9]+)*\.md|commands\/[a-z0-9]+(?:-[a-z0-9]+)*\.md|rules\/[a-z0-9]+(?:-[a-z0-9]+)*\.(?:md|mdc))(?:\/|$)/);
    const manifest = rel.match(/^(src|packs\/[a-z0-9]+(?:-[a-z0-9]+)*)\/(?:plugin\.json|\.(?:claude|cursor)-plugin\/plugin\.json)$/);
    if (!match && !manifest) continue;
    const ownerRoot = match ? match[1] : manifest[1];
    const target = match ? `${ownerRoot}/${match[2]}` : ownerRoot;
    const type = manifest ? "plugin" : match[2].startsWith("skills/") ? "skill" :
      match[2].startsWith("agents/") ? "agent" : match[2].startsWith("commands/") ? "command" : "rule";
    targets.set(`${type}:${target}`, { target, type, ownerRoot });
    if (targets.size > MAX_TARGETS) break;
  }
  if (targets.size > MAX_TARGETS) failures.push("Validation target limit reached; remaining components are unverified.");
  for (const { target, type, ownerRoot } of [...targets.values()].slice(0, MAX_TARGETS)) {
    const catalog = resolve(process.cwd(), "plugin-catalog.json");
    if (ownerRoot.startsWith("packs/") && existsSync(catalog)) {
      const owners = JSON.parse(readFileSync(catalog, "utf8")).plugins || [];
      if (!owners.some((owner) => owner.source_root === ownerRoot)) {
        failures.push(`ERROR ${target}: optional plugin owner is absent from the catalog`);
        continue;
      }
    }
    if (!validator) {
      failures.push(`Validation unavailable for ${target}: Queen validator is absent; component is unverified.`);
      continue;
    }
    const remaining = Math.floor(BUDGET_MS - (performance.now() - started));
    if (remaining <= 0) {
      failures.push("Validation time budget exhausted; remaining components are unverified.");
      break;
    }
    try {
      execFileSync(process.platform === "win32" ? "python" : "python3", [
        validator, target, "--type", type, "--harness", "all",
      ], { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"], timeout: remaining, maxBuffer: 65536 });
    } catch (error) {
      const output = `${error.stdout || ""}${error.stderr || ""}`;
      const count = output.split("\n").filter((line) => line.startsWith("ERROR")).length;
      if (count) failures.push(`ERROR ${target}: validator reported ${count} error(s); component is unverified. Error text is not forwarded here. To read it, run: ${process.platform === "win32" ? (/^[A-Za-z0-9 _.:\\\/-]+$/.test(validator) ? `python "${validator}"` : "python <Core>\\skills\\queen-wasp-stinger\\references\\scripts\\per-type-validation.py") : `python3 '${validator.replace(/'/g, "'\\''")}'`} ${target} --type ${type} --harness all`);
      else failures.push(`Validation unavailable for ${target}: validator failed, timed out or exceeded its output bound; component is unverified.`);
    }
  }
} catch {
  emit(data, "Wasp Nest validation unavailable: component metadata could not be inspected. The edit remains unverified.");
}

emit(data, failures.length
  ? `Wasp Nest component validation advisory:\n${failures.slice(0, 24).join("\n")}\nResolve failures or unavailable checks before registration.`
  : "");
