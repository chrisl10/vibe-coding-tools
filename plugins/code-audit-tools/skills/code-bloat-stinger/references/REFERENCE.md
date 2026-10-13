# Code Bloat Stinger: reference index

## Files in this skill

| Path | What it holds |
| --- | --- |
| `references/tool-commands.md` | Copy-ready commands for every step, with pinned versions |
| `references/bands.md` | Healthy and bloated lines, the mapping onto the contract scale, severity rubric, verdict rule |
| `references/false-positive-classes.md` | The 16 knip false-positive classes and the search that tests each one |
| `references/non-js-dead-code.md` | Dead-code tools for Python, Go, Rust, and the honest gap for other languages |
| `references/output-templates.md` | `metrics.json` keys and example, `findings.jsonl` examples per kind, `notes.md` outline |
| `references/research/distilled-code-bloat.md` | The cited distillation of this skill's research |
| `references/research/raw/` | 31 archived sources, including local verification runs |

## Scripts (Python 3.9+, standard library only)

| Script | Input | Output | Guide |
| --- | --- | --- | --- |
| `scripts/jscpd_recount.py` | `jscpd-report.json`, the scanned tree, optional coverage report | standard metric, both-copies figure, per area, per file, big vs small, top pairs, asymmetric and repaired range counts, coverage warnings | 01 |
| `scripts/knip_summarize.py` | knip JSON (5.x or 6.x), the tree | category counts, per workspace, dependency names, unused-file line totals, used-in-own-file counts, a seeded spot-check worksheet | 02, 05 |
| `scripts/size_profile.py` | cloc or scc by-file JSON, or a folder | share of code in files over N lines, largest files, per area | 03 |
| `scripts/function_profile.py` | `lizard --csv`, or a folder (JS/TS heuristic) | largest functions, closure factories with inner-function counts | 04 |
| `scripts/validate_outputs.py` | the `01-bloat/` folder | contract errors and warnings; exit 1 on error | 06 |

Every script prints Markdown tables to stdout and writes full JSON with `--json-out`. Run any of them with `--help`.

## Raw folder layout (`01-bloat/raw/`)

| File | Made by |
| --- | --- |
| `sha.txt`, `versions.txt` | guide 00 |
| `file-list.txt`, `scope.md` | guide 00 |
| `jscpd-50/jscpd-report.json`, `jscpd-50/recount.json`, `jscpd-100/...`, `jscpd-coverage/jscpd-report.json` | guide 01 |
| `knip.json`, `knip.stderr`, `knip-production.json`, `knip-debug.txt`, `knip-config.json` (copy of the external config), `knip-summary.json`, `spot-check.md` | guide 02, 05 |
| `vulture.txt`, `deadcode.txt`, `staticcheck-u1000.txt`, `cargo-machete.txt`, `cargo-check.json` | guide 02 (non-JS) |
| `cloc-by-file.json` or `scc-by-file.json`, `size-profile.json` | guide 03 |
| `lizard.csv`, `functions.json` | guide 04 |

List each file under `## Evidence` in `01-bloat/notes.md` with a one-line description; the orchestrator builds `evidence-index.md` (contract section 9).
