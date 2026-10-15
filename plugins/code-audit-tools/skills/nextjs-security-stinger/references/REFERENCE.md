# nextjs-security-stinger reference index

| File | What it holds | Load when |
| --- | --- | --- |
| [advisory-table.md](advisory-table.md) | Human table of 61 Next.js advisories (2024 to 2026-09-30) with affected and first patched versions and preconditions | Guide 01, or any time a version question comes up |
| [next-advisories.json](next-advisories.json) | Same data, normalized for the scan script (`introduced` inclusive, `fixed` exclusive, `fix_status`) | Run by `scripts/next_audit_scan.py`; edit only when refreshing research |
| [checks-proxy-and-auth-boundaries.md](checks-proxy-and-auth-boundaries.md) | NX-PRX-01 to 05, NX-AUTH-01 to 04 | Guide 02 |
| [checks-server-actions-and-route-handlers.md](checks-server-actions-and-route-handlers.md) | NX-SA-01 to 09, NX-RH-01 to 05 | Guide 03 |
| [checks-data-exposure-and-caching.md](checks-data-exposure-and-caching.md) | NX-DATA-01 to 05, NX-CACHE-01 to 04 | Guide 04 |
| [checks-config-and-headers.md](checks-config-and-headers.md) | NX-CFG-01 to 08 | Guide 05 |
| [ai-failure-patterns.md](ai-failure-patterns.md) | AI-01 to AI-20 sweep, each pointing at its owning check | End of guides 02 to 05 |
| [finding-templates.md](finding-templates.md) | Severity mapping, example `findings-nextjs-security-wasp-drone.jsonl` lines, `metrics-nextjs-security-wasp-drone.json` and `notes-nextjs-security-wasp-drone.md` shapes | Guide 06 |
| [research/distilled-nextjs-security.md](research/distilled-nextjs-security.md) | Cited distillation of the research archive | Verifying a claim or settling a dispute |
| research/raw/ | 31 archived sources (advisories, official docs, auth library docs, standards, AI-code studies) | Tracing a claim to its source |

## Script

`../scripts/next_audit_scan.py` (Python 3.9 or newer, standard library only, read-only on the audited repo; pnpm workspaces are resolved per importer, npm workspaces per `<dir>/node_modules/next` then the root entry, yarn and bun list every `next` version found):

```bash
python3 <skill>/scripts/next_audit_scan.py --repo <repo> --out <workspace>/02-security/raw [--paths apps/web] [--id-start 1]
```

Outputs:
- `next-version-findings.jsonl`: contract-shaped findings (`SEC-NEXT-NNN`) for version and advisory matches: one per matched critical advisory, one roll-up for matched high advisories, one roll-up for medium and low, one for an unsupported major line, or one `info` line when nothing matches. Advisories with an unmet precondition are dropped (listed under `advisories_not_applicable`); unknown preconditions give `confidence: possible`, capped at medium.
- `next-inventory.json`: apps (declared and resolved versions, lockfile, router type, next.config security keys, middleware or proxy files with matchers, auth libraries, deployment hints, advisory matches with precondition status), `use_server_files` with exported actions and hint flags, `inline_use_server`, `route_handlers`, `pages_api_routes`, `use_client_files`, `use_cache`, `unstable_cache`, `next_public_vars`, `suspicious_next_public_names`, `hardcoded_secret_candidates` (redacted), and other hint lists.
- stdout: a JSON summary including `next_id` (the next free NNN for manual findings).

Refusals: exits 2 if `--out` is inside the audited repo.

Known limits (state them in `metrics-nextjs-security-wasp-drone.json.coverage.caps`): files over 2 MB skipped; `next.config` parsed by regex; `bun.lockb` (binary) not read, falls back to package.json range with `confidence: possible`; canary-only advisory lines are not modeled (see notes in the JSON).
