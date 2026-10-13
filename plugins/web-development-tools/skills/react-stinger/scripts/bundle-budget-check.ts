/**
 * Measure an explicit Vite static-JavaScript entry graph.
 * Usage: BUILD_DIR MANIFEST ENTRY [BUDGET_KIB].
 * Use a Node runtime qualified for this TypeScript helper (see guide 23).
 * Example: node bundle-budget-check.ts dist dist/.vite/manifest.json src/main.tsx 90
 * The optional positive budget is in gzip KiB, not a route or load-time guarantee.
 * Without a budget the result is MEASURED_NO_BUDGET, not a budget pass.
 * Static imports are deduplicated; dynamic entries are listed separately.
 * Filename-only usage exits 2 UNVERIFIED. Next.js output is unsupported.
 * Historical heuristic functions below are unreachable in the supported CLI mode;
 * their route budgets and waivers are not a supported configuration contract.
 */

import { readFile, readdir, stat, realpath } from 'node:fs/promises';
import { join, relative, resolve, isAbsolute } from 'node:path';
import { gzipSync } from 'node:zlib';
import process from 'node:process';

type Budgets = {
  defaults: { firstLoadJs: number };
  routes: Record<string, { firstLoadJs: number }>;
  waivers?: { route: string; until: string; reason: string }[];
};

async function readBudgets(): Promise<Budgets> {
  try {
    return JSON.parse(await readFile('react-stinger.budgets.json', 'utf8'));
  } catch {
    return { defaults: { firstLoadJs: 300 }, routes: {} };
  }
}

async function walk(dir: string): Promise<string[]> {
  const out: string[] = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const full = join(dir, entry.name);
    if (entry.isDirectory()) out.push(...(await walk(full)));
    else if (entry.name.endsWith('.js')) out.push(full);
  }
  return out;
}

async function gzSize(path: string): Promise<number> {
  const buf = await readFile(path);
  return gzipSync(buf).length;
}

async function main() {
  const buildDir = process.argv[2] ?? 'dist';
  if (process.argv[3]) {
    await measureManifest(buildDir, process.argv[3], process.argv[4], process.argv[5]);
    return;
  }
  console.error('UNVERIFIED: filename heuristics cannot establish route bundle weight. Supply MANIFEST ENTRY [BUDGET_KIB].');
  process.exitCode = 2;
  return;
  // Historical heuristic retained for reference, unreachable in verified mode.
  const budgets = await readBudgets();

  const files = await walk(buildDir);
  const byRoute = new Map<string, number>();

  for (const f of files) {
    const rel = relative(buildDir, f);
    // Heuristic: map chunk file to route. Real impls parse the build manifest
    // (Vite's stats.json, Next's .next/build-manifest.json).
    const route = chunkToRoute(rel);
    const size = await gzSize(f);
    byRoute.set(route, (byRoute.get(route) ?? 0) + size);
  }

  const violations: { route: string; actual: number; budget: number }[] = [];

  for (const [route, size] of byRoute) {
    const kb = size / 1024;
    const budget = budgets.routes[route]?.firstLoadJs ?? budgets.defaults.firstLoadJs;
    if (kb > budget) {
      const waived = budgets.waivers?.some((w) => w.route === route && new Date(w.until) > new Date());
      if (!waived) violations.push({ route, actual: kb, budget });
    }
  }

  console.log('# Bundle budget report');
  console.log('');
  for (const [route, size] of [...byRoute].sort()) {
    const kb = (size / 1024).toFixed(1);
    const budget = budgets.routes[route]?.firstLoadJs ?? budgets.defaults.firstLoadJs;
    const mark = Number(kb) > budget ? 'OVER' : 'ok';
    console.log(`- ${route.padEnd(30)} ${kb.padStart(8)} KB gz  (budget ${budget})  ${mark}`);
  }
  console.log('');

  if (violations.length > 0) {
    console.error(`FAIL — ${violations.length} route(s) over budget.`);
    process.exit(1);
  }
  console.log('PASS');
}

function chunkToRoute(chunk: string): string {
  // Very naive mapping for the stub; real impl reads the framework's manifest.
  // Example: 'assets/app-login-a1b2c3.js' -> '/app/login'
  const base = chunk.replace(/\.[a-f0-9]{6,}\.js$/, '').replace(/^assets\//, '').replace(/-/g, '/');
  return '/' + base.replace(/\/index$/, '');
}

async function measureManifest(dir: string, manifestPath: string, entry: string, budgetText?: string) {
  const budget = budgetText === undefined ? undefined : Number(budgetText);
  if (!entry || process.argv.length > 6 || (budget !== undefined && (!Number.isFinite(budget) || budget <= 0))) throw new Error('Invalid arguments');
  const root = await realpath(dir);
  const manifest = JSON.parse(await readFile(manifestPath, 'utf8'));
  if (!manifest || typeof manifest !== 'object' || Array.isArray(manifest) || !Object.hasOwn(manifest, entry) || manifest[entry]?.isEntry !== true) throw new Error('Invalid manifest entry');
  const visited = new Set<string>(), assets = new Set<string>(), dynamic = new Set<string>();
  async function visit(key: string) {
    if (visited.has(key)) return;
    if (!Object.hasOwn(manifest, key)) throw new Error('Missing import');
    const chunk = manifest[key];
    if (!chunk || typeof chunk !== 'object' || Array.isArray(chunk) || typeof chunk.file !== 'string') throw new Error('Invalid chunk');
    for (const field of ['imports', 'dynamicImports']) {
      if (chunk[field] !== undefined && (!Array.isArray(chunk[field]) || !chunk[field].every((x: unknown) => typeof x === 'string'))) throw new Error('Invalid imports');
    }
    if (!/\.m?js$/.test(chunk.file)) throw new Error('Unsupported non-JS chunk');
    const candidate = resolve(root, chunk.file), rel = relative(root, candidate);
    if (isAbsolute(chunk.file) || rel.startsWith('..') || isAbsolute(rel)) throw new Error('Escaping asset');
    const actual = await realpath(candidate), actualRel = relative(root, actual);
    if (actualRel.startsWith('..') || isAbsolute(actualRel) || !(await stat(actual)).isFile()) throw new Error('Unsafe asset');
    visited.add(key); assets.add(actual);
    for (const lazy of chunk.dynamicImports ?? []) dynamic.add(lazy);
    for (const dependency of chunk.imports ?? []) await visit(dependency);
  }
  await visit(entry);
  const measurements = [];
  for (const asset of [...assets].sort()) {
    const data = await readFile(asset);
    measurements.push({file:relative(root,asset), bytes:data.length, gzipBytes:gzipSync(data,{level:9}).length});
  }
  const gzipBytes = measurements.reduce((sum,a) => sum+a.gzipBytes,0);
  const verdict = budget === undefined ? 'MEASURED_NO_BUDGET' : gzipBytes/1024 > budget ? 'OVER_BUDGET' : 'WITHIN_BUDGET';
  console.log(JSON.stringify({entry,assets:measurements,staticAssetCount:assets.size,gzipBytes,gzipKiB:gzipBytes/1024,dynamicEntries:[...dynamic].filter(k=>!visited.has(k)).sort(),budgetKiB:budget??null,verdict,limits:'Static JS graph only; excludes CSS/media, runtime requests, CDN encoding, browser timing and dynamic totals.'},null,2));
  if (verdict === 'OVER_BUDGET') process.exitCode = 1;
}
main().catch(() => { console.error('UNVERIFIED: missing, malformed, unsupported or unsafe bundle measurement input.'); process.exitCode = 2; });
