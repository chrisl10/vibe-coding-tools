# Report spec

The final work-accomplished report: markdown canonical, PDF for humans. Both come from run artifacts, never memory.

## report.md structure

```markdown
# <Repo> documentation refresh: work report
> Run dates | pinned commit | owner | pipeline version

## What this was
Two or three sentences: what the run set out to do and the plan that was approved.

## The numbers
| Docs written | Docs updated | Docs kept | Units | Gate passes | Tokens | Working hours / wall clock |
Every number from run artifacts (unit map, gate summaries, ledger). Token counts summed from per-run totals.

## What changed
Per unit, one line: unit, docs touched, verdict.

## How it was verified
The gauntlet with real counts: write, adversarial rounds (N passed first round, N needed 2, N hit the cap), security gate (fixes, rechecks), quality gate (fixes, rechecks), repo validation result.

## What we found
Suspect summary (counts by severity and category, pointer to SUSPECTS.md) and drift summary (count, pointer to the drift report).

## Handoff
The batched PR list, merge order notes, the merge brief location, who merges.

## Limitations
Unverified claim count, anything skipped and why, caps hit and logged.
```

Tone rules: the owner's plain register, no em dashes or en dashes, every number traceable to a file in the run workspace.

## report.html and the PDF

`LEGION_BRAND_KIT_ROOT` means the user-supplied, authorized local root of the Legion Code Inc. brand kit. Resolve and verify that directory in the current environment; the placeholder does not assert a bundled kit or any author-specific home path.

1. Build a single print-styled HTML sheet (one page for the summary version; the full report may run longer). House style, from the Legion Code Inc. brand kit at `${LEGION_BRAND_KIT_ROOT}/source/claude-design/logos/LCI _Logos/`:
   - Paper `#F4F4F3`, near-black ink `#0A0B0D`, one accent rule color per section (blue `#2563EB`, rust `#C2571F`, green `#16A34A`).
   - Mono uppercase letter-spaced section labels with numeric prefixes (`01 SCOPE`).
   - Stat boxes with thin borders; huge tight headlines.
   - Legion symbol, verified paths from the brand kit: light background `<path d="M12 8 L24 8 L24 44 L48 44 L48 56 L12 56 Z" fill="#0A0B0D"/><rect x="12" y="8" width="12" height="8" fill="#18A968"/>`; dark background `fill="#F5F6F7"` with cap `fill="#3DDC97"`. Wordmark: `LEGION`, Inter 700, letter-spacing about -1.2px. Never hand-draw the mark; inline these paths.
   - Print CSS: `@page { size: letter; margin: 0 }`, `print-color-adjust: exact`, footer band as a black strip with the co-brand and a single mono line.
2. Render: `scripts/md-to-pdf.sh report.html report.pdf` (headless Chrome, `--no-pdf-header-footer`). Verify the PDF exists and is non-trivial in size; a zero-byte PDF means Chrome failed and the markdown stands alone. Say so in the closing report.

## Delivery set

`report.md`, `report.html`, `report.pdf`, `SUSPECTS.md`, the drift report, the merge brief. The closing report links all six with paths.
