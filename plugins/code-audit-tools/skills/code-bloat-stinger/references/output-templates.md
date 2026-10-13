# Output templates: metrics.json, findings.jsonl, notes.md

The contract (`audit-my-code-stinger/references/audit-contract.md`, sections 5 and 6) is the authority. These templates fill it for the bloat dimension. The example values are illustrative, shaped like the WHIPT audit [research/raw/gold--whipt-bloat-audit-method.md]; never copy the numbers.

## metrics.json

Measure keys. Use exactly these keys so the brief renderer and later runs line up. Add extra measures after them if useful.

| key | label | unit | band rule (references/bands.md) |
| --- | --- | --- | --- |
| `dup_std_50` | Duplication, jscpd standard metric, 50 tokens | % | duplication |
| `dup_both_50` | Duplication, both copies counted, 50 tokens | % | duplication |
| `dup_std_100` | Duplication, jscpd standard metric, 100 tokens | % | duplication |
| `dup_both_100` | Duplication, both copies counted, 100 tokens | % | duplication |
| `dup_big_files` | Duplication in files over 1,000 lines, both copies, 50 tokens | % | duplication |
| `dup_small_files` | Duplication in files up to 1,000 lines, both copies, 50 tokens | % | duplication |
| `dead_truly_pct` | Truly dead code (after spot-check), share of core code lines | % | dead code; `not-run` when no tool ran |
| `big_file_share` | Code in files over 1,000 lines | % | big-file share |
| `largest_function_lines` | Largest single function (name in label) | lines | largest function |

Every `band` uses the contract scale (`healthy`, `moderate`, `at-risk`, `critical`, `not-run`); there is no `n/a`. Pure counts (flagged files, core code lines, clone pairs) are not measures: put them in `notes.md` and `coverage`. The example below is abbreviated; a real run includes every key in the table, with band `not-run` for any step that did not run.

```json
{
  "dimension": "bloat",
  "verdict": "moderate",
  "summary": "Mostly no, it is not bloated because it was vibe coded: little is copy-pasted or dead, but nearly half the code sits in files over 1,000 lines and one function is 5,527 lines long.",
  "measures": [
    {"key": "dup_std_50", "label": "Duplication, jscpd standard metric, 50 tokens", "value": 3.58, "unit": "%", "band": "healthy", "threshold": "<5% healthy, >10% bloated (Mario's bands)", "source": "jscpd 5.4.0"},
    {"key": "dup_both_50", "label": "Duplication, both copies counted, 50 tokens", "value": 7.32, "unit": "%", "band": "moderate", "threshold": "<5% healthy, >10% bloated (Mario's bands)", "source": "jscpd 5.4.0 plus scripts/jscpd_recount.py"},
    {"key": "dead_truly_pct", "label": "Truly dead code, after a 12-item spot-check", "value": 1.5, "unit": "%", "band": "healthy", "threshold": "<3% healthy, >8% bloated (heuristic)", "source": "knip 6.39.0 plus manual spot-check"},
    {"key": "big_file_share", "label": "Code in files over 1,000 lines", "value": 45.7, "unit": "%", "band": "at-risk", "threshold": "<15% healthy, >30% bloated (heuristic)", "source": "cloc 2.10 plus scripts/size_profile.py"},
    {"key": "largest_function_lines", "label": "Largest single function (executeRun in server/src/services/heartbeat.ts)", "value": 5527, "unit": "lines", "band": "critical", "threshold": "<200 healthy, >1,000 bloated (heuristic; 1,000 is lizard's default length warning)", "source": "lizard 1.24.0"}
  ],
  "coverage": {
    "files_scanned": 3171,
    "lines_scanned": 1079239,
    "skipped": ["vendor/", "dist/", "**/*.d.ts", "tests and fixtures (excluded from duplication by design)"],
    "caps": [
      "jscpd 5.4.0 skips files over 1 MB by default (--max-size); rerun with --max-size 100mb; jscpd sources matched the file walk (3,171 of 3,171)",
      "jscpd 4.x would also skip files over 1,000 lines (--max-lines); not used",
      "cloc counts identical files once by default; run with --skip-uniqueness",
      "knip Playwright plugin disabled for the root workspace via an external config: tests/canary-onboarding/playwright.config.ts throws on load",
      "knip run without installing dependencies"
    ]
  }
}
```

`files_scanned` and `lines_scanned` are the duplication scope (jscpd raw lines). State the cloc code-line total in `notes.md` ("core code lines"), because jscpd counts raw lines including comments and blanks and cloc counts code only, so the two compare only roughly [research/raw/gold--whipt-bloat-audit-method.md].

## findings.jsonl

One line per finding. Ids: `BLOAT-DUP-NNN`, `BLOAT-DEAD-NNN`, `BLOAT-SIZE-NNN`, `BLOAT-STRUCT-NNN`, numbered from 001 per kind. Shown pretty-printed here; write each as one line.

```json
{"id": "BLOAT-DUP-001", "dimension": "bloat", "source": "code-bloat-wasp-drone",
 "title": "Six local adapter packages are near copies of each other",
 "severity": "medium", "confidence": "confirmed",
 "locations": [{"path": "packages/adapters/gemini-local/src/index.ts", "line_start": 1, "line_end": 410},
               {"path": "packages/adapters/kimi-local/src/index.ts", "line_start": 1, "line_end": 398}],
 "evidence": "jscpd 5.4.0 at 50 tokens, both copies counted: gemini-local 48.0%, kimi-local 45.2%, opencode-local 37.1%, cursor-local 36.8%, pi-local 34.6%, grok-local 20.6% (raw/jscpd-50/recount.json). Largest pair: packages/adapters/gemini-local/src/index.ts:12-187 and packages/adapters/kimi-local/src/index.ts:10-185 (176 lines).",
 "why_it_matters": "A fix or new feature in one adapter has to be repeated by hand in five others, and the copies already drift apart.",
 "remediation": "Extract the shared session, spawn, and output-parsing code into one base in packages/adapter-utils and make each adapter a thin configuration over it, starting with gemini-local and kimi-local.",
 "effort": "L", "refs": ["guides/01-duplication-with-jscpd.md"],
 "verified_by": "Opened both files of the three largest clone pairs and confirmed the blocks are the same logic with renamed identifiers, not generated code.",
 "tags": ["copy-family", "adapters"]}
{"id": "BLOAT-SIZE-001", "dimension": "bloat", "source": "code-bloat-wasp-drone",
 "title": "One function in the heartbeat service is 5,527 lines long",
 "severity": "medium", "confidence": "confirmed",
 "locations": [{"path": "server/src/services/heartbeat.ts", "line_start": 8412, "line_end": 13938}],
 "evidence": "lizard 1.24.0 CSV row: executeRun, start 8412, end 13938 (raw/lizard.csv). Second largest in the file: enqueueWakeup, 1,674 lines.",
 "why_it_matters": "Nobody can review or safely change a 5,500-line function, and every agent edit lands in the same place, which keeps it growing.",
 "remediation": "Split executeRun in server/src/services/heartbeat.ts into four to six phase functions (prepare, resolve workspace and session, invoke adapter, finalize, follow-ups) behind a context object, as in guide 04.",
 "effort": "L", "refs": ["guides/04-structure-and-split-planning.md"],
 "verified_by": "Read the function start and end lines in the copy; the span matches lizard and contains no nested module-level code."}
{"id": "BLOAT-DEAD-001", "dimension": "bloat", "source": "code-bloat-wasp-drone",
 "title": "Two old pages were left behind when the classic view was removed",
 "severity": "low", "confidence": "confirmed",
 "locations": [{"path": "ui/src/pages/MyIssues.tsx"}, {"path": "ui/src/pages/Org.tsx"}],
 "evidence": "knip 6.39.0 unused files: ui/src/pages/MyIssues.tsx, ui/src/pages/Org.tsx (raw/knip.json). rg -n 'MyIssues|pages/Org' in the copy returns only the files themselves.",
 "why_it_matters": "Dead pages confuse agents and people searching the code, and they keep importing components that would otherwise also be removable.",
 "remediation": "Delete ui/src/pages/MyIssues.tsx and ui/src/pages/Org.tsx (204 lines), then rerun knip to see what else becomes unused.",
 "effort": "S", "refs": ["guides/05-spot-check-and-false-positives.md"],
 "verified_by": "Spot-check row 4: searched the whole copy including routes, configs and HTML; no references; not a build entry."}
{"id": "BLOAT-STRUCT-001", "dimension": "bloat", "source": "code-bloat-wasp-drone",
 "title": "Four core services are each one giant function that holds all their code",
 "severity": "medium", "confidence": "confirmed",
 "locations": [{"path": "server/src/services/heartbeat.ts", "line_start": 8459, "line_end": 27141},
               {"path": "server/src/routes/issues.ts", "line_start": 2910, "line_end": 14864}],
 "evidence": "scripts/function_profile.py on lizard output: heartbeatService span 18,683 lines with 179 inner functions; issueRoutes span 11,954 lines; toolAccessService 12,227; issueService 5,020 (raw/functions.json).",
 "why_it_matters": "Every inner function shares captured state, so none of them can be moved, tested, or reviewed on its own until that state is made explicit.",
 "remediation": "For each service, first pass the captured state as an explicit context object, then move inner functions into modules by concern, following the split plan in notes.md.",
 "effort": "L", "refs": ["guides/04-structure-and-split-planning.md"],
 "verified_by": "Read the opening lines of each closure and confirmed the inner functions reference closure variables, not module imports."}
```

Rules from the contract that bite most often in this dimension: no finding without evidence (unsampled knip items stay as counts); paths are repo-relative, never `.scratch/repo-copy/...`; `possible` confidence stays at `medium` or below; evidence quotes the tool, it does not paraphrase it.

## notes.md

`notes.md` carries the narrative tables the brief can link to. Follow the WHIPT order [research/raw/gold--whipt-bloat-audit-method.md]:

```markdown
# Bloat audit: <repo> @ <branch> <short sha>

Run <start> to <end>. Tools: jscpd <v>, knip <v>, cloc <v> (or scc <v>), lizard <v>. Repo changes: none.

## Verdict
<one paragraph that answers the user's question in plain words; see guides/06>

| Measure | Result | Band | Threshold |
| --- | --- | --- | --- |
<one row per metrics.json measure>
Duplication bands are Mario's; the others are heuristics.

## 1. Duplication (jscpd)
Scope: <languages>, <folders>, <files> files and <raw lines> raw lines. Excluded: <list>.
Tool gotcha: <which cap applied, how it was lifted, sources count check>. <Repaired clone ranges: N>.
50 tokens: <std>% (<pairs> clone pairs), <both>% both copies. 100 tokens: <std>% / <both>%.
Big files vs small: <x>% vs <y>%. <reading>.
### By area (50 tokens, both copies)
<table: area, lines, dup @50, dup @100; mark areas over 10%>
### Largest files
<table: file, lines, dup @50, dup @100; reading of the 50 to 100 drop>
### Top clone pairs (50 tokens)
<table: lines, copy A, copy B>; named hotspots.

## 2. Unused code (knip, or the language tool)
Run: <workspace-aware or not>, <plugins disabled and why>, <production run or not>. Counts are core only.
<category table with notes> <per-workspace table> <flagged dependency names>
### Spot-check of <N> findings
<table: finding, verdict (Dead / False alarm / Partial), why>
### Estimate of truly dead code
<table: bucket, flagged lines, truly dead, note; total and % of core lines>

## 3. Structure
Share of code in files over 1,000 lines: <x>%. Largest files and functions. Closure factories.
### How the largest files could split
<table: file, lines, shape, modules, risk> then per-file module lists and the context-object note.

## 4. Next steps: where the real savings are
<ordered list, biggest win first>

## Not confirmed
<suspicions without evidence, or "none">

## Coverage and caps
<files and lines scanned, skipped paths, every cap lifted or hit, tools not run and why>

Footnote: jscpd counts raw lines including comments and blanks; cloc counts code only, so the two compare only roughly. Tools ran in a throwaway copy that was removed afterwards; no tests were run.
```
