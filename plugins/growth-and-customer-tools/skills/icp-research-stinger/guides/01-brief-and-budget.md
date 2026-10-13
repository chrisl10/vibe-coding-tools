# 01: Brief and budget

## Normalize the domain

1. Accept a URL, a bare domain, or a company name. With only a name, find the official site first and confirm it with the requester when more than one candidate exists.
2. Strip scheme, `www.`, paths, and query strings. Fetch the homepage once and record the final domain after redirects.
3. Note related domains in scope (a separate product site, regional sites) and domains out of scope (a parent company, an unrelated namesake).

## Fill the brief

Copy [templates/research-brief.md](../templates/research-brief.md) to the run directory (by default `library/research/icp/<domain>/<YYYY-MM-DD>/` in the consumer repository, or the path the requester names). Fill purpose, depth mode, budget, tools, and stop conditions.

## Choose depth and budget

Use [references/REFERENCE.md](../references/REFERENCE.md) section 1. Default to Standard. Estimate spend with [references/TOOLS.md](../references/TOOLS.md) before starting and write both the page budget and the money or credit cap into the brief.

Spending money on third-party APIs is an external effect. If the brief's cap exceeds what the requester already approved, or no cap was approved, ask before starting. Free tiers and keyless modes still carry rate limits.

## Plan the run directory

```text
<run-dir>/
  research-brief.md
  seed-brief.md
  lane-<name>.jsonl, lane-<name>-notes.md   (one pair per lane)
  ledger.jsonl                               (merged)
  score.json, evidence.md                    (scored and rendered)
  icp-dossier.md, icp.json                   (final)
```

Nothing in this directory may contain personal data (guide 00).
