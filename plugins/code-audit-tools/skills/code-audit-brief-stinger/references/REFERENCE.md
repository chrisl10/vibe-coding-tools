# Reference: render_brief.py

Script map, inputs, and output contract for the brief renderer. Derived from the run contract (`../../audit-my-code-stinger/references/audit-contract.md`) and the distillation (`research/distilled-brief-rendering.md`).

## Command line

| Command | Effect |
| --- | --- |
| `python3 scripts/render_brief.py <workspace>` | Writes `<workspace>/brief/brief.html`; theme follows the viewer's OS |
| `--theme light` or `--theme dark` | Pins `data-theme` on the root element |
| `--brand <path>` | Uses another `brand.json` (default `references/brand/brand.json`) |
| `--out <path>` | Writes somewhere else (used for previews; the contract path is the default) |
| `python3 scripts/test_render_brief.py` | Self-tests: rollup, escaping, merge, fixtures |

Exit codes: `0` written; `2` workspace missing. A missing or unreadable `intake.json`, or a tier outside the contract, stops the run with an error message. Everything else becomes a "Data checks" row in the brief instead of a crash.

## Files read (and only these)

| Path | Used for |
| --- | --- |
| `intake.json` | tier, repo name, branch, sha, requested_by, started_at, stacks, tools |
| `NN-*/metrics.json` | verdict, summary, measures, coverage (files, lines, skipped, caps) |
| `NN-*/findings.jsonl` | findings, one per line |
| `NN-*/notes.md` | "Not confirmed" box and collapsed Drone notes |
| `NN-*/raw/` | file list and sizes for the evidence index (contents are never read) |
| `04-remediation/plan.json`, `roadmap.md` | mario tier only |
| `evidence-index.md` | evidence index section |

Only folders for the tier's dimensions are read. A `metrics.json` outside the tier produces an "Outside tier" data check and is not shown.

## Functions worth knowing

| Function | Contract |
| --- | --- |
| `rollup_verdict(dimension_verdicts)` | Worst-of on healthy < moderate < at-risk < critical; `not-run` ignored. Pure, isolated, refined later |
| `esc(value)` | `html.escape(str(value), quote=True)`; the only way repo text reaches the page |
| `md_block(text)` | Escape-first Markdown subset: headings, lists, pipe tables, fences, inline code, bold; links become text plus the URL in plain text, never `href` |
| `merge_findings(run)` | Contract 5.4: same path, overlapping lines, shared CWE; keeps the higher severity, lists merged ids |
| `sort_key(f)` | severity, then confidence, then effort, then id |
| `mask_secrets(text)` | Masks anything still shaped like a live secret and records a data check |
| `css_string(text)` | Hex-escapes text for `@page` footer `content` strings |

## Output contract

One file, `brief/brief.html`, self-contained except the Google Fonts stylesheet (system fonts take over offline). Logos are inline SVG; the favicon is a `data:` URI. No script. Typical size 50 to 110 KB.

## Fixtures

| Fixture | Tier | Exercises |
| --- | --- | --- |
| `references/fixtures/sample-foundation/` | foundation | single dimension, empty caps list, repo-wide findings |
| `references/fixtures/sample-full/` | full | all four dimensions, caps callouts, percent chart, duplicate merge, an unparseable findings line, hostile strings in title, evidence, and notes |
| `references/fixtures/sample-mario/` | mario | everything in full, plus a dimension that did not run (quality) and the remediation timeline from `plan.json` and `roadmap.md` |

All fixture data is fictional ("acme-dashboard", "Jordan Example (fictional)", `example.invalid`).

`sample-full` and `sample-mario` deliberately violate contract 1.0 (an unparseable quality findings line, and a missing quality `metrics.json`) to exercise the renderer's data checks. They are not examples of valid workspaces, and `check_workspace.py` reports them as failed by design.

Sources: [research/raw/escape--python-html-escape.md], [research/raw/escape--owasp-xss-prevention.md], [research/raw/data--jsonlines-format.md], [research/raw/print--mdn-page-at-rule.md].
