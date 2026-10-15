# 05. Spot-check and false-positive triage

Goal: turn knip's (or vulture's, or deadcode's) flagged counts into an honest "truly dead" estimate. A raw count is not dead code. knip itself says a surprising result is "a real finding or a configuration gap" [../references/research/raw/knip--handling-issues.md (source-repository research, not shipped)]; only reading decides which.

Loads: [../references/false-positive-classes.md](../references/false-positive-classes.md), `raw/spot-check.md` and `raw/knip-summary.json` from guide 02.

## 1. Sample

1. Use the worksheet `knip_summarize.py` wrote (`raw/spot-check.md`). It is a seeded, stratified sample across categories: files, dependencies, exports, devDependencies, types, unlisted, unresolved, duplicates.
2. Classify at least 12 items. Use 16 or more when one workspace dominates the flagged files, and 20 or more for Python.
3. Add by hand: the five largest unused files by line count, and every flagged item in the workspace with the most unused files. Large files and outlier workspaces move the estimate most, and an outlier workspace is often one false-positive class (WHIPT: one workspace's 59 flagged files were mostly a missed `exports` to `dist/` mapping) [../references/research/raw/gold--whipt-bloat-audit-method.md (source-repository research, not shipped)].

## 2. Classify each item

For each row, run the tests in [../references/false-positive-classes.md](../references/false-positive-classes.md), then write one verdict and one reason:

| Verdict | Meaning | Example reason (WHIPT style) |
| --- | --- | --- |
| Dead | nothing reaches it; safe to delete | "Barrel re-export with no importers (44 lines)"; "Left behind by the classic-view removal (204 lines)"; "Not routed; only named in codemod comments" |
| False alarm | live, the tool missed the entry | "Entry of a separate Vite preview build"; "Service worker registered by string"; "Reached through package exports to dist/; knip missed the mapping"; "A bin entry and build input"; "Run by a root package script" |
| Partial | live but misplaced, or only part is dead | "Only used by server tests" (devDependency); "Belongs to adapter-utils, not server"; "Used inside its own file: drop the export" |

Dead needs a whole-copy search for the name, including configs, HTML, scripts, CI workflows and docs, with every hit read. If you are not sure, it is Partial.

## 3. Estimate truly dead code

Group flagged items into buckets that behave alike, usually by workspace and category (for example "ui unused files", "root scripts and infra", "orphan exports").

For each bucket:

1. Flagged lines: non-blank lines of flagged files (`knip_summarize.py` totals them), plus for exports an upper bound from the export's span.
2. Dead ratio: from the spot-check rows in that bucket. With fewer than three rows in a bucket, read three more items from it before estimating.
3. Truly dead: flagged lines times the ratio, written as a range (for example "about 3K to 4K"). Ranges are honest; one precise number is not.
4. Note: why the ratio is what it is (for example "its scripts are false alarms", "mostly the export-mapping miss", "barrel re-exports inflate the upper bound").

Total the buckets and divide by core code lines from guide 03. That is `dead_truly_pct`. The WHIPT total was about 12K to 16K lines, about 1.5% of 977K core lines [../references/research/raw/gold--whipt-bloat-audit-method.md (source-repository research, not shipped)]. Report the midpoint as the measure value and the range in the label or `notes.md`.

## 4. Findings from the spot-check

- Confirmed dead files and exports become `BLOAT-DEAD-NNN` findings, `low` severity, `confirmed` confidence, grouped by cause (one finding for "pages left behind by a removal", not one per file).
- Partial items that matter (a production dependency only tests use, a dependency in the wrong workspace) become `BLOAT-DEAD-NNN` at `low`.
- False alarms are not findings. List them in `notes.md` so the next run can configure knip better.
- Unsampled flagged items are counts, not findings.

## 5. Record the worksheet

Copy the filled table into `notes.md` section 2 ("Spot-check of N findings"), and keep the filled `raw/spot-check.md`. Then the estimate table: bucket, flagged, truly dead, note, total, and the share of core lines.

## Sources

The notes listed below are source-repository research, not shipped.

- ../references/research/raw/gold--whipt-bloat-audit-method.md (source-repository research, not shipped)
- ../references/research/raw/knip--handling-issues.md (source-repository research, not shipped)
- ../references/research/raw/knip--entry-files.md (source-repository research, not shipped)
- ../references/research/raw/knip--source-mapping.md (source-repository research, not shipped)
- ../references/research/raw/vulture--readme.md (source-repository research, not shipped)
