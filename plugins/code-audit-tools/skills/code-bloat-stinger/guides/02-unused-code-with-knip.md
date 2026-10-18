# 02. Unused code with knip (and the non-JS equivalents)

Goal: flagged counts per category and per workspace, from a run that covered the whole workspace, ready for the spot-check in guide 05.

Loads: [../references/tool-commands.md](../references/tool-commands.md) (Unused code), [../references/false-positive-classes.md](../references/false-positive-classes.md), [../references/non-js-dead-code.md](../references/non-js-dead-code.md), `../scripts/knip_summarize.py`.

## 1. Run knip workspace-aware, from outside the repo

knip executes the project's own config files to discover plugins (`vitest.config.ts`, `playwright.config.ts`, `next.config.js`, `eslint.config.js`, and others). That is repository code running, so it needs `intake.json.execution.allowed`. When the user declined, do not run knip: band `dead_truly_pct` as `not-run`, record the cap "unused-code analysis not run: knip executes the project's config files and the user declined code execution", and say in the verdict paragraph that dead code was not measured. When allowed, use the consented mode (container command in [../references/tool-commands.md](../references/tool-commands.md), or host with `SAFE_ENV`).


1. knip handles workspaces by itself. It reads `package.json#workspaces`, `pnpm-workspace.yaml`, and knip config [../references/research/raw/knip--monorepos-and-workspaces.md (source-repository research, not shipped)]. Do not pass `--workspace` for the main run; you want every workspace at once.
2. knip needs a `package.json` at the directory it runs in; without one it stops with `ERROR: Unable to find package.json` and exit code 2 (seen on a repository that is a collection of packages). If the root has none, find the package roots (`rg --files -g 'package.json' -g '!**/node_modules/**' <copy>`) and run knip once per package root with `-D <copy>/<package>`, saving `raw/knip-<package>.json`. Summarize each and add the counts. If there is no `package.json` anywhere, the JS dead-code step did not run: band `dead_truly_pct` as `not-run` and say why.
3. Run from `.scratch/tools/` with `-D <copy>` and `--reporter json --no-progress --no-exit-code`. Save stdout to `raw/knip.json`, stderr and the exit code to `raw/knip.stderr`.
4. Run `--debug` once into `raw/knip-debug.txt`. It shows the workspaces found, the enabled plugins, and source mapping. Check every workspace you expect is listed.
5. Never pass `--fix`, `--fix-type`, `--allow-remove-files`, or `--format`. They modify files [../references/research/raw/knip--cli-help-and-fixture-test.md (source-repository research, not shipped)].
6. If the repo already has a knip config, knip uses it. Read it: an `ignore` list there hides issues, so note it in `notes.md` as a limit on what was counted [../references/research/raw/knip--configuration-reference.md (source-repository research, not shipped)].

## 2. If a plugin config throws

Symptom: `ERROR: Error loading <tool>.config.ts` on stderr and exit code 2. `--no-exit-code` does not suppress it, and the JSON printed is incomplete [../references/research/raw/knip--known-issues.md] [../references/research/raw/knip--cli-help-and-fixture-test.md (source-repository research, not shipped)].

Work through these in order, all without touching the repo:

1. Read the error. Missing module: install the copy's dependencies with `--ignore-scripts` (guide 00) and rerun.
2. Missing environment variables or secrets (for example a Playwright config that throws when a URL or token is unset): never create or fetch real secrets. Disable that plugin instead.
3. Write an external config at `.scratch/knip/knip.json` and pass it with `-c`: `{"workspaces": {".": {"playwright": false}}}` to turn the Playwright plugin off for the root workspace, or key it by the one workspace that fails. Declared workspaces are still analyzed [../references/research/raw/knip--configuration-reference.md] [../references/research/raw/knip--cli-help-and-fixture-test.md (source-repository research, not shipped)].
4. Copy that config to `raw/knip-config.json` and record in `coverage.caps`: which plugin, which workspace, and why (for example "tests/canary-onboarding/playwright.config.ts throws on load; runner-e2e config needs eight env vars including secrets").
5. Say what the workaround costs: entry points that plugin would have added are no longer known. With Playwright that is e2e specs, which are out of scope anyway. The plugin's own config file and package now show as unused: classify them as false alarms (class 9).

If a repo has its own knip config with the failing plugin, copy that config into `.scratch/knip/`, change only the plugin entry, and pass it with `-c`.

## 3. Run production mode as a second view

Run once more with `--production` into `raw/knip-production.json`. Default mode counts test usage as usage; production mode shows code only tests keep alive [../references/research/raw/knip--production-mode.md (source-repository research, not shipped)]. Use it in the spot-check to spot "used only by tests" (class 7). Report default-mode counts as the headline.

## 4. Summarize

Run `scripts/knip_summarize.py --report raw/knip.json --root <copy>` with `--exclude` globs for non-core paths (vendor, tests, fixtures, examples, devtools), `--sample 16`, `--json-out raw/knip-summary.json`, `--sample-out raw/spot-check.md`. It accepts knip 6 and knip 5 JSON (5.x had a root `files` list [../references/research/raw/knip--v6-release-breaking-changes.md [source-repository research, not shipped]]).

It gives, for core code only:

| Category | Note to carry into the report |
| --- | --- |
| Unused files | count and non-blank line total |
| Unused exports | how many are used inside their own file (drop `export`, keep code) |
| Unused types | same |
| Duplicate exports | count |
| Unused dependencies, devDependencies, optional peers | names per workspace |
| Unlisted dependencies | where they are; inside vendor folders they are noise |
| Unresolved imports | names; native addons and generated files are expected |

Plus a per-workspace table (files, exports, types, deps, dev deps) and the flagged dependency names.

## 5. Dependencies need a manual read

Before you list a dependency as unused, search for it as a binary and as a string: `rg -n "<name>" <copy> --glob '!**/node_modules/**'`. Spawned CLIs, packages only tests use, and packages that belong to another workspace are the usual false or partial results (classes 6, 7, 8).

## 6. Non-JS repositories

Run the tool for each ecosystem in scope ([../references/non-js-dead-code.md](../references/non-js-dead-code.md)): vulture for Python, deadcode plus staticcheck U1000 for Go, cargo-machete plus `cargo check` dead_code warnings for Rust. Save output in `raw/`. Where no verified tool exists, set `dead_truly_pct` to band `not-run`, add the language to `coverage.skipped`, and say so in the verdict. Never estimate a dead-code percentage without a tool and a spot-check.

## Done when

- `raw/knip.json` comes from a run that exited 0 (or exit 1 with issues, never 2).
- `raw/knip-summary.json` and `raw/spot-check.md` exist.
- Every disabled plugin and installed dependency set is in `coverage.caps`.

## Sources

The notes listed below are source-repository research, not shipped.

- ../references/research/raw/knip--monorepos-and-workspaces.md (source-repository research, not shipped)
- ../references/research/raw/knip--configuration-reference.md (source-repository research, not shipped)
- ../references/research/raw/knip--known-issues.md (source-repository research, not shipped)
- ../references/research/raw/knip--production-mode.md (source-repository research, not shipped)
- ../references/research/raw/knip--cli-help-and-fixture-test.md (source-repository research, not shipped)
- ../references/research/raw/knip--v6-release-breaking-changes.md (source-repository research, not shipped)
- ../references/research/raw/knip--json-reporter.md (source-repository research, not shipped)
- ../references/research/raw/gold--whipt-bloat-audit-method.md (source-repository research, not shipped)
