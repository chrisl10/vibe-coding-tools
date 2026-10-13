// Synthetic package-resolution exercise, not a generated SDK or package publisher.
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { execFileSync } from 'node:child_process';

const root = mkdtempSync(join(tmpdir(), 'wasp-sdk-exports-'));
try {
  const sdk = join(root, 'node_modules', 'synthetic-sdk');
  mkdirSync(sdk, { recursive: true });
  const manifest = { name: 'synthetic-sdk', version: '0.0.0', type: 'module' };
  writeFileSync(join(sdk, 'index.mjs'), 'export const client = "synthetic";\n');
  writeFileSync(join(sdk, 'models.mjs'), 'export const state = "draft";\n');
  writeFileSync(join(sdk, 'package.json'), JSON.stringify(manifest));
  const consumer = join(root, 'consumer.mjs');
  const run = source => {
    writeFileSync(consumer, source);
    // No inherited NODE_OPTIONS preload, custom resolver or NODE_PATH injection.
    const env = { ...process.env };
    delete env.NODE_OPTIONS;
    delete env.NODE_PATH;
    return execFileSync(process.execPath, [consumer], {
      cwd: root, env, encoding: 'utf8', timeout: 5000, maxBuffer: 8192,
    }).trim();
  };
  assert.equal(run('import {state} from "synthetic-sdk/models.mjs"; console.log(state);'), 'draft');
  manifest.exports = { '.': './index.mjs' };
  writeFileSync(join(sdk, 'package.json'), JSON.stringify(manifest));
  assert.equal(run('import {client} from "synthetic-sdk"; console.log(client);'), 'synthetic');
  assert.equal(run('try { await import("synthetic-sdk/models.mjs"); console.log("unexpected"); } catch (e) { console.log(e.code); }'), 'ERR_PACKAGE_PATH_NOT_EXPORTED');
  console.log(JSON.stringify({ runtime: process.version, passed: 3,
    evidence: 'Old deep import works; candidate root import works; candidate old deep import fails.',
    limits: 'Synthetic ESM package only; no generator, production server, CJS/browser consumer or publishing proof.' }));
} finally {
  // Only the temporary tree created by this exercise is removed.
  rmSync(root, { recursive: true, force: true });
}
