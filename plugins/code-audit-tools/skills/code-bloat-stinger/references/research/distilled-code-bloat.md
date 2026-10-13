# Distilled research: code bloat audits

Research window 2026-03-30 to 2026-09-30, fetched 2026-09-30. Older material is marked. Every claim ends with its raw file. Local verification runs are labeled as such inside the raw files; they settle conflicts between docs and real behavior.

## 1. Tool versions at fetch time

| Tool | Version | Published | How to run without a global install | Source |
| --- | --- | --- | --- | --- |
| jscpd (5.x, Rust) | 5.4.0 | 2026-09-30 | `npx jscpd@5.4.0` (native binary via npm optional deps) | [raw/jscpd--npm-release-timeline.md] [raw/jscpd--v5-readme-and-cli-help.md] |
| jscpd (4.x, JS) | 4.3.0 | 2026-08-13 | `npx jscpd@4.3.0` | [raw/jscpd--npm-release-timeline.md] |
| knip | 6.39.0 | 2026-09-30 | `npx knip@6.39.0`, needs Node 20.19+ | [raw/knip--cli-help-and-fixture-test.md] [raw/knip--v6-release-breaking-changes.md] |
| cloc | 2.10 upstream; npm wrapper 2.6.0-cloc | 2026-07-04 | release script needs Perl; `npx cloc` runs the older wrapper | [raw/cloc--readme-and-cli-help.md] |
| scc | 4.1.0 | 2026-09-07 | download release tarball into the scratch folder; or Docker | [raw/scc--readme-and-cli-help.md] |
| lizard | 1.24.0 | 2026-08-19 | `python3 -m venv` in scratch, `pip install lizard==1.24.0` | [raw/lizard--readme-and-csv-test.md] |
| vulture | 2.16 | 2026-03-25 | venv in scratch, `pip install vulture==2.16` | [raw/vulture--readme.md] |
| Go deadcode | x/tools v0.50.0 resolved | blog 2023-12-12 (older, official) | `go run golang.org/x/tools/cmd/deadcode@latest .` | [raw/go--deadcode-blog-and-test.md] |
| staticcheck | 2026.2.1 | 2026-08-21 | `go run honnef.co/go/tools/cmd/staticcheck@2026.2.1 -checks U1000 ./...` | [raw/go--staticcheck-u1000-test.md] |
| cargo-machete | 0.9.2 | 2026-04-15 | `cargo install cargo-machete` into a scratch `CARGO_HOME`, or Docker | [raw/rust--cargo-machete-readme.md] |
| cargo-udeps | 0.1.61 | 2026-04-29 | needs nightly: `cargo +nightly udeps` | [raw/rust--cargo-udeps-readme.md] |

The WHIPT reference run used jscpd 4.3.0 and knip 5.88.1 [raw/gold--whipt-bloat-audit-method.md]. Both have newer majors with different behavior (sections 2 and 4).

## 2. jscpd: silent caps and what the numbers mean

| Fact | 4.x | 5.x | Source |
| --- | --- | --- | --- |
| Default min tokens / min lines | 50 / 5 | 50 / 5 | [raw/jscpd--v4-readme-options.md] [raw/jscpd--v5-readme-and-cli-help.md] |
| Per-file line cap | `--max-lines` default 1000, file skipped silently | none (`--max-lines` is per block in 5.x) | [raw/jscpd--v4-large-file-skip-experiment.md] |
| Per-file size cap | `--max-size` default 100kb, skipped silently | `--max-size` default 1mb (help text; README shows none), skipped silently | [raw/jscpd--v4-large-file-skip-experiment.md] [raw/jscpd--v5-readme-and-cli-help.md] |
| How to lift | `--max-lines 1000000 --max-size 100mb` | `--max-size 100mb` | [raw/jscpd--v4-large-file-skip-experiment.md] |
| Detection of the skip | `statistics.total.sources` lower than the file count you expected | same, but only in a coverage run at `--min-tokens 1`, because small files are not counted at 50 | [raw/jscpd--v4-large-file-skip-experiment.md] [raw/jscpd--asymmetric-clones-and-small-files-experiment.md] |
| gitignore | respected by default since 4.2.x | respected by default | [raw/jscpd--v4-readme-options.md] [raw/jscpd--v5-readme-and-cli-help.md] |
| `percentage` | duplicatedLines / lines, one copy per clone | same | [raw/jscpd--json-report-shape.md] |
| Clone range bugs | 4.2.x fixed "entire-file duplicates silently dropped" | no invalid ranges seen; but `lines` describes the first copy only, and the second copy can span fewer or more lines | [raw/jscpd--v4-readme-options.md] [raw/jscpd--asymmetric-clones-and-small-files-experiment.md] |
| Files below `--min-tokens` | not tested | left out of `sources` and `lines` (103 files at 5 tokens, 100 at 50, 97 at 100) | [raw/jscpd--asymmetric-clones-and-small-files-experiment.md] |

Conflict: the jscpd 5.x README shows no default for `--max-size` while `--help` says `Default: 1mb`. The local test sided with the help text: a 1.5 MB file was skipped with defaults and included with `--max-size 100mb` [raw/jscpd--v4-large-file-skip-experiment.md].

The brief's instruction "jscpd skips files over 1,000 lines by default" is true for 4.x only. For 5.x the same class of bug is a 1 MB size cap. The guide lifts both regardless of version and verifies with the sources count.

"Both copies counted" is not in the report. It is the union of covered lines per file over both sides of every clone, divided by total scanned lines [raw/jscpd--json-report-shape.md]. In WHIPT it was about twice the standard figure (7.32% vs 3.58%) [raw/gold--whipt-bloat-audit-method.md].

File names in the JSON are relative to jscpd's working directory in 4.x and to the scanned path in 5.x [raw/jscpd--json-report-shape.md].

5.x extras worth knowing: `--summary`, `--skip-local`, `--cross-formats js-ts`, `--ignore-identifiers` (Type-2), `--similarity` (Type-3, JS/TS), `--semantic` (Type-4, experimental, 548 MB model download), `--dead-code` (JS, TS, Python) [raw/jscpd--v5-readme-and-cli-help.md]. jscpd covers 224 languages, so the duplication step works on non-JS repos [raw/jscpd--homepage.md].

## 3. Reading the duplication figures

| Pattern | Reading | Source |
| --- | --- | --- |
| Figure drops a lot from 50 to 100 tokens | many short repeated snippets (handler preambles, envelopes), not large pasted blocks | [raw/gold--whipt-bloat-audit-method.md] |
| Big files duplicate no more than small files | files are big, not pasted | [raw/gold--whipt-bloat-audit-method.md] |
| One area at 20 to 48% both copies while the repo is under 5% | a family of copied modules (WHIPT: local adapters), the clearest consolidation win | [raw/gold--whipt-bloat-audit-method.md] |
| Clone pairs between a package and a forked folder | forks of a package's own source; import instead | [raw/gold--whipt-bloat-audit-method.md] |
| Low jscpd figure | does not rule out reinvented helpers: agent redundancy is often Type-4 (same logic, different text), which token detectors miss | [raw/research--msr-2026-more-code-less-reuse.md] |

## 4. knip: workspaces, plugin failures, false positives

| Fact | Source |
| --- | --- |
| Workspaces are read from `package.json#workspaces`, `pnpm-workspace.yaml`, legacy `workspaces.packages`, and knip config; root is `"."` | [raw/knip--monorepos-and-workspaces.md] |
| knip needs a `package.json` where it runs; a repo without a root one fails with exit 2, so run once per package root | [raw/knip--cli-help-and-fixture-test.md] |
| A plugin config that throws makes knip exit 2, and `--no-exit-code` does not suppress it; the partial JSON printed is incomplete | [raw/knip--known-issues.md] [raw/knip--cli-help-and-fixture-test.md] |
| Fix without touching the repo: pass `-c <outside>/knip.json` with `{"workspaces":{".":{"playwright":false}}}` and `-D <copy>` | [raw/knip--configuration-reference.md] [raw/knip--cli-help-and-fixture-test.md] |
| Disabling a plugin turns its config file into an "unused file" and its package into an "unused devDependency": artifacts, classify as false alarms | [raw/knip--cli-help-and-fixture-test.md] |
| Unused exports of entry files are not reported by default | [raw/knip--handling-issues.md] |
| `dist/` export targets map to source only through tsconfig `outDir`, or a built `dist`, or a source condition | [raw/knip--source-mapping.md] |
| Entries knip does find: `main`, `bin`, `exports`, plugin entries, dynamic imports, `new URL(...)`, `new Worker(...)`, `child_process` with `path.join(__dirname, ...)`, package scripts, CI `run` commands | [raw/knip--entry-files.md] |
| Default mode includes tests, which keep test-only production code alive; `--production` focuses on shipped code and only `dependencies` | [raw/knip--production-mode.md] |
| `ignoreExportsUsedInFile` exists because many "unused exports" are used inside their own file | [raw/knip--configuration-reference.md] |
| knip 6 JSON: `{"issues":[{file, <type>: [{name,line,col,pos}]}]}`; 5.x also had a root `files` array | [raw/knip--json-reporter.md] [raw/knip--v6-release-breaking-changes.md] |
| `--fix` and `--allow-remove-files` modify the repo; never in an audit | [raw/knip--cli-help-and-fixture-test.md] |

False-positive classes (WHIPT spot-check plus docs):

| Class | Why knip misses it | Source |
| --- | --- | --- |
| Package `exports` pointing at `dist/` without tsconfig `outDir` | no source mapping | [raw/knip--source-mapping.md] [raw/gold--whipt-bloat-audit-method.md] |
| Service worker registered by string (`register('/sw.js')`) | not a module import | [raw/knip--entry-files.md] [raw/gold--whipt-bloat-audit-method.md] |
| Entry of a separate build (second Vite config, preview build) | no plugin reads that build input | [raw/knip--handling-issues.md] [raw/gold--whipt-bloat-audit-method.md] |
| `bin` entry or build input not declared where knip looks | entry not discovered | [raw/knip--entry-files.md] [raw/gold--whipt-bloat-audit-method.md] |
| Script run from `package.json` with unsupported arguments | script parser cannot see it | [raw/knip--handling-issues.md] |
| CLI spawned by name (agent CLIs) | listed dependency looks unused | [raw/gold--whipt-bloat-audit-method.md] |
| Dependency used only by tests, or belonging to another workspace | "Partial": misplaced, not dead | [raw/gold--whipt-bloat-audit-method.md] |
| Template-string dynamic imports, unrecognized aliases | unresolved imports | [raw/knip--handling-issues.md] |
| Standalone CLI scripts run by hand from documentation | no package script or import reaches them (18 of 19 CLIs in one real scripts folder) | [raw/knip--cli-help-and-fixture-test.md] |

## 5. Line counting

| Fact | Source |
| --- | --- |
| jscpd counts raw lines including comments and blanks; cloc counts code only; they compare only roughly (WHIPT 1.08M vs 977K core) | [raw/gold--whipt-bloat-audit-method.md] |
| cloc dedups identical files by default; `--skip-uniqueness` counts every copy | [raw/cloc--readme-and-cli-help.md] |
| cloc skips files over 100 MB by default (`--max-file-size`) | [raw/cloc--readme-and-cli-help.md] |
| cloc `--vcs=git` takes the file list from git | [raw/cloc--readme-and-cli-help.md] |
| scc large-file caps (1,000,000 bytes, 40,000 lines) apply only with `--no-large`; defaults counted 1.5 MB and 45,000-line files | [raw/scc--readme-and-cli-help.md] |
| scc does not drop duplicate files unless `-d` | [raw/scc--readme-and-cli-help.md] |

## 6. Function size and closures

| Fact | Source |
| --- | --- |
| lizard covers about 27 languages including TypeScript, TSX, Go, Rust, Python, Java, Kotlin, Swift, PHP, Ruby | [raw/lizard--readme-and-csv-test.md] |
| `lizard --csv` has no header; 11 columns ending `start, end`; nested and arrow functions are separate rows; outer span includes inner rows | [raw/lizard--readme-and-csv-test.md] |
| lizard measures how complex code "looks", not how complex it "is" | [raw/lizard--readme-and-csv-test.md] |
| On real JavaScript, lizard overstated 4 of the 5 largest function spans (233 lines reported for a 16-line function near regex literals); the skill's heuristic matched the real spans; `-t 4` hung on macOS | [raw/lizard--readme-and-csv-test.md] |
| WHIPT shape: four services were single factory closures of 5K to 19K lines with up to 179 inner functions; splitting needs a context-object step first | [raw/gold--whipt-bloat-audit-method.md] |

## 7. Non-JS dead code

| Ecosystem | Tool | Finds | Limits | Source |
| --- | --- | --- | --- | --- |
| Python | vulture 2.16 | unused imports, functions, classes, variables, unreachable code with confidence 60 to 100% | dynamic code: misses some, flags implicit calls; use `--min-confidence`, whitelists | [raw/vulture--readme.md] |
| Python, JS, TS | jscpd 5 `--dead-code` | unused files, exports, symbols, imports | new feature; accuracy not verified here | [raw/jscpd--v5-readme-and-cli-help.md] |
| Go programs | deadcode | unreachable functions program-wide, including exported | needs a `main`; libraries have no roots | [raw/go--deadcode-blog-and-test.md] |
| Go any | staticcheck U1000 | unused unexported identifiers | does not report exported identifiers (local test) | [raw/go--staticcheck-u1000-test.md] |
| Rust deps | cargo-machete | unused dependencies, fast, imprecise | build.rs and renamed crates; `--with-metadata` may change Cargo.lock | [raw/rust--cargo-machete-readme.md] |
| Rust deps | cargo-udeps | unused dependencies via a build | nightly only; misses some | [raw/rust--cargo-udeps-readme.md] |
| Rust code | compiler `dead_code` lint via `cargo check --message-format=json` (jscpd 5 reads it with `--rust-diagnostics`) | unused items | needs a working build | [raw/rust--cargo-udeps-readme.md] [raw/jscpd--v5-readme-and-cli-help.md] |
| Java, Kotlin, C#, Ruby, PHP, Swift | not researched in this window | | thin spot: report "no verified dead-code tool used" and rely on jscpd and size | none |

## 8. Bands

| Measure | Healthy | Bloated | Owner | Source |
| --- | --- | --- | --- | --- |
| Duplication (both jscpd figures) | under 5% | over 10% | Mario | [raw/gold--whipt-bloat-audit-method.md] |
| Truly dead code (after spot-check) | under 3% | over 8% | heuristic | [raw/gold--whipt-bloat-audit-method.md] |
| Code in files over 1,000 lines | under 15% | over 30% | heuristic | [raw/gold--whipt-bloat-audit-method.md] |

Contract mapping (healthy, moderate, at-risk, critical) is a design decision of this skill, documented in `references/bands.md`.

## 9. Is vibe-coded code more bloated? What the evidence says

| Finding | Source |
| --- | --- |
| Across 623M changes, duplicated blocks per million changed lines up 81% (2023 to 2026), refactoring moves down to 3.8% of changed lines; the report itself says the headline is not "AI writes bad code" | [raw/research--gitclear-2026-maintainability-gap.md] |
| In real repos, AI code had lower duplicated-line ratios than human code (18.69% vs 25.89%) but more fragmented clones and more verbose, deeper-nested code | [raw/research--arxiv-2603-27130-ai-vs-human-duplication.md] |
| Agent PRs carry about 1.87x the semantic (Type-4) redundancy of human PRs; reviewers do not notice | [raw/research--msr-2026-more-code-less-reuse.md] |
| In human and agent projects, humans introduced 86% of clone lineages | [raw/research--msr-2026-clone-genealogies.md] |
| 22.7% of AI-introduced issues survive at HEAD; code smells dominate | [raw/research--arxiv-2603-28592-ai-technical-debt.md] |

Reading: the evidence conflicts on duplication percentage and agrees on shape (verbosity, fragmentation, less reuse, less consolidation). That is what WHIPT found: low paste, heavy shape. The verdict must describe the repository's own numbers and must not claim a cause the numbers cannot show.

## Thin spots and open conflicts

- jscpd 5.x `--max-size` default: README and help disagree; the guide trusts the local test and lifts it anyway.
- jscpd "broken clone ranges" from the WHIPT run on 4.3.0: no reversed or out-of-file range was reproduced. What was reproduced on a real tree is asymmetric clones: `lines` matches the first copy only, the second copy's range is correct but shorter or longer [raw/jscpd--asymmetric-clones-and-small-files-experiment.md]. This is the most likely cause of the per-area miscounts WHIPT saw; recounting from each side's own range fixes it. The recount script also repairs truly invalid ranges and reports both counts.
- staticcheck U1000 doc text was not captured; behavior is from a local run.
- No verified dead-code tool for Java, Kotlin, C#, Ruby, PHP, Swift in this sweep.
- knip with dependencies not installed still produced correct results on the fixture, but plugin config loading may need installs on real repos [raw/knip--known-issues.md].
