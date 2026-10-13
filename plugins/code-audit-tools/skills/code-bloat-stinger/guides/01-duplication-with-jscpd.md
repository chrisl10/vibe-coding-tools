# 01. Duplication with jscpd

Goal: two honest duplication figures at two clone sizes, plus the breakdowns that say where the copying is and what kind it is.

Loads: [../references/tool-commands.md](../references/tool-commands.md) (Duplication), [../references/bands.md](../references/bands.md), `../scripts/jscpd_recount.py`.

## 1. Know the silent caps before you run

| jscpd line | Caps that skip whole files silently | Lift with |
| --- | --- | --- |
| 4.x (4.3.0) | `--max-lines` 1000 lines, `--max-size` 100kb | `--max-lines 1000000 --max-size 100mb` |
| 5.x (5.4.0) | `--max-size` 1mb (help text; the README shows no default) | `--max-size 100mb` |

Verified locally: 4.3.0 dropped two 1,630-line files with no warning; 5.4.0 dropped a 1.5 MB file with no warning [../references/research/raw/jscpd--v4-large-file-skip-experiment.md]. In 5.x, `--max-lines` means lines per clone block, not per file, so do not set it [../references/research/raw/jscpd--v5-readme-and-cli-help.md].

Always lift the caps, whatever version you run, and record each one in `coverage.caps` as "lifted".

## 2. Run at 50 and 100 tokens

1. From `.scratch/tools/`, run jscpd on the copy with the scope's format list and ignore list, `--min-tokens 50`, the caps lifted, `--reporters json`, `--output raw/jscpd-50`. Repeat with `--min-tokens 100` into `raw/jscpd-100`. 50 is the default; 100 is the stricter view [../references/research/raw/jscpd--v4-readme-options.md].
2. Keep the default mode (`mild`). Do not pass `--ignore-identifiers`, `--similarity` or `--semantic` for the headline figures; they change what counts as a clone. You may run `--ignore-identifiers` as an extra and report it separately.
3. jscpd respects `.gitignore` by default; that is correct for the copy.
4. Format names come from `npx jscpd --list` (for example `typescript`, `tsx`, `javascript`, `jsx`, `python`, `go`, `rust`).

## 3. Check the scan covered the scope

jscpd 5.x leaves files with fewer tokens than `--min-tokens` out of `sources` and `lines` (on a real tree: 103 files at 5 tokens, 100 at 50, 97 at 100) [../references/research/raw/jscpd--asymmetric-clones-and-small-files-experiment.md]. So the 50-token report's `sources` cannot prove coverage on its own.

1. Run one coverage pass: same formats, ignores and lifted caps, `--min-tokens 1`, output to `raw/jscpd-coverage`.
2. Its `statistics.total.sources` must equal the number of in-scope files of those formats in `raw/file-list.txt`. If it is lower, a cap still applied or the lists differ. Fix and rerun. Do not report figures from a short scan.
3. Pass it to the recount with `--coverage-report raw/jscpd-coverage/jscpd-report.json`. The script then warns only on a real coverage gap. Treat any warning as blocking until fixed or explained in `notes.md`.

## 4. Recount with the script

Run `scripts/jscpd_recount.py` on each report with `--root` the copy, the same extensions and excludes, your areas (`--area`, `--area-depth`), `--big-lines 1000`, and `--json-out raw/jscpd-50/recount.json` (and the 100 equivalent).

The script gives you:

| Output | Meaning |
| --- | --- |
| `jscpd_standard_pct` | jscpd's own metric: duplicated lines counted once per clone, over scanned lines [../references/research/raw/jscpd--json-report-shape.md] |
| `both_copies_pct` | the union of lines covered by any clone, both sides, over scanned lines. Usually close to twice the standard figure |
| `areas` | the both-copies figure per area, recounted from each clone's own range |
| `big_files` / `small_files` | duplication in files over 1,000 lines versus the rest |
| `largest_files` | duplication of the biggest files |
| `top_clone_pairs` | the largest pairs, with ranges |
| `asymmetric_clone_sides` | sides whose own range differs from the clone's `lines`; kept as is, because each side's range is its real length |
| `repaired_clone_sides` | sides with an invalid range (missing, reversed, past the end of the file), repaired from the clone's `lines` |

Why recount: the WHIPT run found jscpd emitting some broken clone ranges, so per-area figures were recounted from each clone's real length [../references/research/raw/gold--whipt-bloat-audit-method.md]. On a real tree the cause reproduced as asymmetry: a clone's `lines` describes the first copy only, and the second copy can be the same tokens on fewer, longer lines [../references/research/raw/jscpd--asymmetric-clones-and-small-files-experiment.md]. Per-file and per-area figures built from `lines` are therefore wrong; built from each side's own range they are right. Report both counts in `notes.md`. If repaired sides are more than a few percent, say the per-area figures are approximate.

The both-copies denominator is every in-scope file, including files too small to hold a clone, which jscpd leaves out of its own `lines`.

## 5. Read the numbers

Use these readings, in plain words, in `notes.md`:

- **50 versus 100 tokens.** A large drop (for example 20% to under 4% in one file) means many short repeated snippets such as handler preambles and response envelopes, not large pasted blocks. A small drop means real pasted blocks.
- **Big versus small files.** If big files duplicate about as much as small ones, they are big, not pasted. If big files duplicate much more, they grew by pasting.
- **By area.** One area far above the repo (for example 20 to 48% while the repo is under 5%) is a family of copied modules. Open the top pairs to confirm and name the family.
- **Top pairs.** Look for three recurring shapes: forks of a package's own source in another folder, type or schema copies of a shared package, and an index or barrel repeating another file.
- **Limit.** jscpd finds text and token clones. Agent-written redundancy is often the same logic written differently (Type-4), which it does not find [../references/research/raw/research--msr-2026-more-code-less-reuse.md]. Say this in the verdict when the figure is low.

## 6. Band and record

1. Band each of the four figures with [../references/bands.md](../references/bands.md): under 5% healthy, over 10% bloated (Mario's bands), mapped to the contract scale.
2. Write measures `dup_std_50`, `dup_both_50`, `dup_std_100`, `dup_both_100`, `dup_big_files`, `dup_small_files` ([../references/output-templates.md](../references/output-templates.md)).
3. `coverage.files_scanned` and `coverage.lines_scanned` come from the 50-token report's `sources` and `lines`.
4. Raise `BLOAT-DUP-NNN` findings only for things you opened and read: a copy family, a fork, type copies, a file whose short-snippet duplication a helper would absorb. Quote the recount numbers and the pair ranges in `evidence`.

## Sources

- [../references/research/raw/jscpd--v4-readme-options.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-bloat-stinger/references/research/raw/jscpd--v4-readme-options.md)
- [../references/research/raw/jscpd--v4-large-file-skip-experiment.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-bloat-stinger/references/research/raw/jscpd--v4-large-file-skip-experiment.md)
- [../references/research/raw/jscpd--v5-readme-and-cli-help.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-bloat-stinger/references/research/raw/jscpd--v5-readme-and-cli-help.md)
- [../references/research/raw/jscpd--json-report-shape.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-bloat-stinger/references/research/raw/jscpd--json-report-shape.md)
- [../references/research/raw/jscpd--asymmetric-clones-and-small-files-experiment.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-bloat-stinger/references/research/raw/jscpd--asymmetric-clones-and-small-files-experiment.md)
- [../references/research/raw/jscpd--npm-release-timeline.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-bloat-stinger/references/research/raw/jscpd--npm-release-timeline.md)
- [../references/research/raw/gold--whipt-bloat-audit-method.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-bloat-stinger/references/research/raw/gold--whipt-bloat-audit-method.md)
- [../references/research/raw/research--msr-2026-more-code-less-reuse.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-bloat-stinger/references/research/raw/research--msr-2026-more-code-less-reuse.md)
