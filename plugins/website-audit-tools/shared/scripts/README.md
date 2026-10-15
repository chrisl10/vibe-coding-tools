Deterministic, harness-portable scripts shared across multiple Stingers, per the build plan's "shared where the use case is genuinely shared" instruction. No absolute paths. Each Stinger's `references/scripts/README.md` points here rather than duplicating a copy.

| Script | Used by |
|---|---|
| `fingerprint.py` | stack-fingerprint-stinger |
| `crawl-extract.py` | site-crawler-stinger |
| `vendor-census.py` | vendor-inventory-stinger |
| `seo-technical.py` | technical-seo-stinger |
| `aeo-technical.py` | aeo-audit-stinger |
| `a11y-scan.py` | accessibility-audit-stinger |
| `security-headers.py` | web-security-posture-stinger |
| `score-rollup.py` | audit-scoring-stinger (independent cross-check of the scorecard rollups; tested by `test_score_rollup.py`) |

Not implemented. These planned helpers exit with status 2 and a message naming what the Drone does instead. No guide or skill depends on them:

| Script | Owner | The Drone does instead |
|---|---|---|
| `cwv-collect.py` | performance-cwv-stinger | Collects field and lab Core Web Vitals itself (guide 01, step 3) |
| `visual-capture.py` | visual-funnel-stinger | Captures checkpoint screenshots with the harness browser tool (guide 03) |
| `xlsx-populate.py` | audit-scoring-stinger | Transcribes validated leaves into a copy of the scorecard template (SKILL.md steps 1 and 4) |
