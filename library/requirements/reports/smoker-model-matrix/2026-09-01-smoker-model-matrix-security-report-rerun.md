# Security audit rerun - 2026-09-01 - Smoker packaged model matrix

## Executive summary

- Scope: the exact amended working-tree candidate on `codex/smoker-self-contained-matrix` against `fork/main`, including the rebuilt Codex plugin and project ZIP archives, updated checksum manifest, archive-aware regression test, canonical command, generator, generated trees, and bundled matrices.
- Coverage: REDUCED COVERAGE. This is a Markdown, Python, and release-archive distribution change rather than the SvelteKit application stack researched by `security-stinger`. All applicable archive traversal, archive integrity, secrets, prompt safety, path handling, generated-artifact consistency, and supply-chain controls were checked.
- Findings: 0 Critical, 0 High, 0 Medium, 1 Low.
- Ship Gate status: cleared to proceed to a fresh `quality-stinger` rerun. The earlier Quality report describes the pre-rebuild candidate and is now stale by design.

## Surface coverage checklist

### SvelteKit attack surface

None detected. The amended candidate adds no SvelteKit route, form action, environment import, HTML rendering, cookie handling, or CSP configuration.

### Authorization and tenancy (Drizzle / Neon)

None detected. The amended candidate adds no database access, SQL construction, authorization decision, tenant data, or persistence surface.

### Secrets and environment

None detected.

- High-confidence credential and private-key patterns produced no hits in either safely extracted archive tree.
- Neither archive contains a real `.env`, Git directory, private SSH key, credentials file, Terraform state, or macOS metadata.
- The only environment-template entries are the expected `get-started-stinger/templates/.env.example` copies. Their values are documented placeholders and the copies are byte-identical.
- GitHub secret scanning and push protection remain enabled for `chrisl10/vibe-coding-tools`, with zero open secret-scanning alerts at audit time.

### Webhooks and third-party intake

None detected. The candidate adds no HTTP intake, signature verification, callback, outbound fetch, or externally supplied URL handling.

### Dependencies and supply chain

One Low release-hygiene finding is documented below. No exploitable archive defect was detected.

- `learn/packages/vibe-coding-tools-codex-1.0.0.zip` has 3,651 entries, 3,030 regular files, 13,297,075 uncompressed bytes, and no absolute, parent-traversal, backslash, duplicate, symlink, or Git/macOS metadata entry.
- `learn/packages/vibe-coding-tools-codex-project-1.0.0.zip` has 7,461 entries, 6,214 regular files, 28,297,124 uncompressed bytes, and no absolute, parent-traversal, backslash, duplicate, symlink, or Git/macOS metadata entry.
- `unzip -t` passed for both rebuilt archives.
- Both archives were extracted only after the traversal precheck into fresh temporary directories. Recursive comparisons found no missing, altered, or unexpected files relative to `.codex/plugins/vibe-coding-tools`, `.agents`, and `.codex` respectively.
- `shasum -a 256 -c learn/packages/SHA256SUMS` passed for all four release archives. The rebuilt Codex hashes are `e61708fb32f0fb5dd96eb959effc5ab1ecc1052b5e9878103dfd207ec493efb9` and `7704bfab0c764e433d8ba0f317a9636884139dd311ce0816037f8a1403fcdac7`.
- The largest regular archived file is 176,355 bytes and aggregate compression is ordinary, with no zip-bomb indicator detected.

### Headers and transport

None detected. The candidate does not change a deployed HTTP service, hosting configuration, security header, TLS setting, WAF rule, or rate limit.

### AI-generated code patterns

None detected.

- The packaged plugin Smoker, packaged project `.agents` Smoker, and packaged project plugin Smoker all have SHA-256 `fddf0987b08aa15bb07376831f1d721dc1f543fb50dc944b2b3010a5b3c589eb`, identical to their source-tree counterparts.
- Every packaged Smoker resolves `references/model-comparison-matrix.md`, rejects the obsolete root-relative path, stops before dispatch if the matrix is unavailable, forbids ledger reuse and a silent high-cost fallback, and keeps model and reasoning settings separate.
- Every packaged matrix has SHA-256 `48743442d7a082db1eb421b807e3a88747080a517c55592b51176ad12e4ec7db`, identical to `.claude/model-comparison-matrix.md`.
- `learn/scripts/test-smoker-model-matrix.py:16-54` now checks both checked-out Codex surfaces and both declared installable package surfaces.

### PII and logging hygiene

None detected. The candidate does not collect, render, transmit, or log user data, telemetry, credentials, payment data, or other PII.

## Findings detail

### [LOW] Rebuilt release artifacts retain the existing 1.0.0 filenames

- **Location:** `learn/packages/SHA256SUMS:2-3`
- **Surface:** Dependencies and supply chain
- **Description:** The two rebuilt archives intentionally replace the prior bytes and checksums while retaining filenames ending in `1.0.0`. The current repository state is internally consistent and no tampering was found, but the same version label can identify different bytes across commits if the older archives were already distributed. This is release-provenance hygiene, not an exploitable archive flaw in this candidate.
- **Evidence:** `vibe-coding-tools-codex-1.0.0.zip` now maps to `e61708fb...`, and `vibe-coding-tools-codex-project-1.0.0.zip` now maps to `7704bfab...`, while the version component remains `1.0.0`.
- **Remediation:** If either prior archive was externally published, issue the corrected artifacts as a new package version and retain the historical `1.0.0` artifact identity. If these tracked ZIPs have not been published, document that fact in the PR and the current rebuild is acceptable.
- **Status:** NEEDS HUMAN REVIEW. Documented only because external publication history is not established by the working tree.

## Remediation summary

| Severity | Count | Fixed this session | Documented only |
|---|---:|---:|---:|
| Critical | 0 | 0 | 0 |
| High | 0 | 0 | 0 |
| Medium | 0 | 0 | 0 |
| Low | 1 | 0 | 1 |

## Verification evidence

- Archive entry traversal, absolute-path, backslash-path, duplicate-entry, symlink, special-metadata, and Git-metadata checks: passed.
- `unzip -t` for both rebuilt Codex archives: passed.
- Fresh-directory extraction followed by recursive source-tree comparison: passed with no difference.
- High-confidence archive-tree secret scan: no confirmed findings.
- `shasum -a 256 -c learn/packages/SHA256SUMS`: all four archives passed.
- `python3 learn/scripts/test-smoker-model-matrix.py`: passed with `Smoker model matrix packaging: PASS`.
- Direct Smoker instruction and matrix digest comparisons across source and packaged copies: passed.
- `git diff --check`: passed.

## Re-evaluation

This report is the required full Security re-evaluation after Quality caused a material package rebuild. No Medium-or-above security finding required another remediation cycle.

## Next step

The exact amended candidate is cleared to proceed to a fresh `quality-stinger` rerun. Before commit or push, the orchestrating agent must then load and run the orchestrator-level `github-repo-health-stinger`, per the repository Ship Gate.
