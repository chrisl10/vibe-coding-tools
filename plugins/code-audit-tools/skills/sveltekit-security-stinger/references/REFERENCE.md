# Reference index

| File | What it holds | Load when |
| --- | --- | --- |
| [check-catalog.md](check-catalog.md) | Every check (SVK-V, B, E, H, X, C, A): detection, confirm vs false positive, severity, vulnerable and fixed code, refs | Running any guide from 01 to 05 |
| [detection-patterns.md](detection-patterns.md) | Ripgrep commands per check, tested for parse errors | Before the manual read in each guide |
| [advisory-table.md](advisory-table.md) | Every published advisory for svelte, @sveltejs/kit, devalue and adapters, with ranges and preconditions | Guide 00, and when a version finding needs explaining |
| [severity-guide.md](severity-guide.md) | Confidence rules, severity anchors, adjusters, verdict | Guide 06, and any time a severity is in doubt |
| [research/distilled-sveltekit-security.md](research/distilled-sveltekit-security.md) | Cited summary of all research, with conflicts and thin spots | Verifying a claim before it goes into a finding |
| research/raw/ | One file per primary source | Tracing a claim to its source |
| [../scripts/sveltekit_audit_scan.py](../scripts/sveltekit_audit_scan.py) | Deterministic version match and surface inventory | Guide 00, once per run |
| [../scripts/advisories.json](../scripts/advisories.json) | The advisory data the scanner reads | Refreshing advisories |

## Scanner interface

```bash
python3 <skill>/scripts/sveltekit_audit_scan.py \
  --repo <audited repo> \
  --paths <stack path> [<stack path> ...] \
  --out-dir <workspace>/02-security/raw \
  --id-start 1
```

- Python 3.11 or newer, standard library only. Read only: it refuses an `--out-dir` inside `--repo`.
- Lockfiles read: `package-lock.json`, `npm-shrinkwrap.json`, `pnpm-lock.yaml`, `yarn.lock` (v1 and Berry), `bun.lock` (text). `bun.lockb` is listed but not parsed. Then `node_modules/<pkg>/package.json` if present. `package.json` ranges are recorded as `declared_ranges` only.
- Files skipped: `node_modules`, `.svelte-kit`, `.git`, `build`, `dist`, `.vercel`, `.netlify`, `.output`, `.wrangler`, `coverage`, `.turbo`, `.next`, `vendor`, and any file over 1.5 MB (listed in `skipped_large_files`). Report these in `coverage.caps`.

Outputs:

| File | Contents |
| --- | --- |
| `sveltekit-version-findings.jsonl` | Contract-shaped findings, ids `SEC-SVELTE-NNN` from `--id-start`. One finding per advisory whose precondition was found in source (`likely`), plus one roll-up per package version for the rest (`possible`, capped `medium`). |
| `sveltekit-inventory.json` | `lockfiles`, `versions`, `declared_ranges`, `versions_unresolved`, `clean_core_versions`, `advisory_matches`, `next_finding_id`, and `inventory`: `routes`, `hooks`, `remote_functions`, `html_sinks`, `dom_sinks`, `markdown_libraries`, `svelte_config`, `env_public_names`, `env_private_imports_in_client`, `cookie_options_weakened`, `redirects_dynamic`, `module_level_state`, `service_workers`, `error_with_dynamic_message`, `signals`, `cross_checks`, `files_scanned`, `skipped_large_files`. |

The scanner never decides that code is vulnerable. `routes[].needs_manual_authz_review`, `cross_checks`, and `signals` are a reading list for guides 01 to 05.

## Finding shape (contract section 5)

```json
{"id": "SEC-SVELTE-012", "dimension": "security", "source": "sveltekit-security-wasp-drone",
 "title": "Anyone can delete user accounts through the admin page's deleteUser form action",
 "severity": "high", "confidence": "confirmed",
 "locations": [{"path": "src/routes/admin/+page.server.ts", "line_start": 4, "line_end": 9}],
 "evidence": "export const actions = {\n  deleteUser: async ({ request }) => {\n    const id = (await request.formData()).get('id');\n    await db.delete(users).where(eq(users.id, String(id)));\n  }\n};",
 "why_it_matters": "The admin layout redirects non-admins when the page loads, but the action runs before any load (loads run after the action completes), so any signed-in user who posts to /admin?/deleteUser can delete any account.",
 "remediation": "In src/routes/admin/+page.server.ts, start deleteUser with `if (!locals.user?.isAdmin) error(403)`; better, enforce admin access for the /admin route group in src/hooks.server.ts as well.",
 "effort": "S", "refs": ["CWE-862", "OWASP A01:2025", "skills/sveltekit-security-stinger/guides/02-actions-endpoints-remote-functions.md"],
 "verified_by": "Read the action body and src/hooks.server.ts: handle sets locals.user but checks no route; the only guard is in +layout.server.ts, which runs only after the action has completed.",
 "tags": ["sveltekit", "form-action", "authz"]}
```
