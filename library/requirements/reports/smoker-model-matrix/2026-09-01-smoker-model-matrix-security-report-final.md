# Security audit final rerun - 2026-09-01 - Smoker 1.0.1 release candidate

## Executive summary

- Scope: the exact final working-tree candidate on `codex/smoker-self-contained-matrix` against `fork/main`, including all four 1.0.1 release archives, three plugin manifests, package documentation, checksum manifest, archive-aware regression test, canonical command, generator, generated trees, and bundled matrices.
- Coverage: REDUCED COVERAGE. This is a Markdown, Python, plugin-manifest, and release-archive distribution change rather than the SvelteKit application stack researched by `security-stinger`. All applicable archive traversal, integrity, secrets, prompt safety, path handling, version identity, generated-artifact consistency, and supply-chain controls were checked.
- Findings: 0 Critical, 0 High, 0 Medium, 0 Low.
- Ship Gate status: cleared to proceed to a fresh `quality-stinger` rerun. Both earlier Security reports and the earlier Quality report cover superseded candidates and remain historical evidence only.

## Surface coverage checklist

### SvelteKit attack surface

None detected. The final candidate adds no SvelteKit route, form action, environment import, HTML rendering, cookie handling, or CSP configuration.

### Authorization and tenancy (Drizzle / Neon)

None detected. The final candidate adds no database access, SQL construction, authorization decision, tenant data, or persistence surface.

### Secrets and environment

None detected.

- High-confidence credential and private-key patterns produced no hits in any of the four safely extracted archive trees.
- No archive contains a real `.env`, Git directory, private SSH key, credentials file, Terraform state, or macOS metadata.
- The expected `.env.example` template copies contain documented non-working placeholders and match their source trees exactly.
- GitHub secret scanning and push protection remain enabled for `chrisl10/vibe-coding-tools`, with zero open secret-scanning alerts at audit time.

### Webhooks and third-party intake

None detected. The candidate adds no HTTP intake, signature verification, callback, outbound fetch, or externally supplied URL handling.

### Dependencies and supply chain

None detected.

- `learn/packages/SHA256SUMS:1-4` names exactly the four archive files present in `learn/packages/`, and every SHA-256 verification passes.
- `learn/packages/README.md:4-10` names the same four 1.0.1 files, with no stale 1.0.0 package reference in any active release path.
- The prior tracked 1.0.0 archives are removed and replaced by four distinct 1.0.1 artifacts, resolving the superseded report's mutable-version finding.
- All four archives have no absolute, parent-traversal, backslash, duplicate, symlink, Git metadata, or macOS metadata entry.
- `unzip -t` passed on all four archives. Aggregate uncompressed sizes range from 13,297,069 to 28,297,118 bytes, and the largest regular file is 176,355 bytes, with no zip-bomb indicator detected.
- All four archives were extracted only after the traversal precheck into fresh temporary directories. Recursive comparisons found no missing, altered, or unexpected files relative to `.claude`, `.cursor`, `.codex/plugins/vibe-coding-tools`, `.agents`, and `.codex` as applicable.

### Headers and transport

None detected. The candidate does not change a deployed HTTP service, hosting configuration, security header, TLS setting, WAF rule, or rate limit.

### AI-generated code patterns

None detected.

- `.claude/.claude-plugin/plugin.json:3` and `.cursor/.cursor-plugin/plugin.json:4` declare `1.0.1`, matching their 1.0.1 archive names and packaged manifests.
- `.codex/plugins/vibe-coding-tools/.codex-plugin/plugin.json:3` declares `1.0.1+codex.20260901`. Both the Codex plugin archive and the Codex project archive contain this exact manifest value, whose base release matches their 1.0.1 filenames.
- Every packaged Codex Smoker resolves `references/model-comparison-matrix.md`, rejects the obsolete root-relative path, stops before dispatch if the matrix is unavailable, forbids ledger reuse and a silent high-cost fallback, and keeps model and reasoning settings separate.
- Every packaged Smoker instruction file is byte-identical to its source counterpart. Every packaged matrix is byte-identical to `.claude/model-comparison-matrix.md` with SHA-256 `48743442d7a082db1eb421b807e3a88747080a517c55592b51176ad12e4ec7db`.
- `learn/scripts/test-smoker-model-matrix.py:16-54` points only to the current 1.0.1 Codex archives and verifies both checked-out and installable Smoker surfaces.

### PII and logging hygiene

None detected. The candidate does not collect, render, transmit, or log user data, telemetry, credentials, payment data, or other PII.

## Findings detail

None detected.

## Remediation summary

| Severity | Count | Fixed this session | Documented only |
|---|---:|---:|---:|
| Critical | 0 | 0 | 0 |
| High | 0 | 0 | 0 |
| Medium | 0 | 0 | 0 |
| Low | 0 | 0 | 0 |

The Low release-version finding from the preceding Security rerun is resolved by the 1.0.1 archive and manifest update.

## Verification evidence

- Four-archive traversal, absolute-path, backslash-path, duplicate-entry, symlink, special-metadata, and Git-metadata checks: passed.
- `unzip -t` for all four 1.0.1 archives: passed.
- Fresh-directory extraction followed by recursive source-tree comparison for all four archives: passed with no difference.
- High-confidence archive-tree secret scan: no confirmed findings.
- `shasum -a 256 -c learn/packages/SHA256SUMS`: all four archives passed.
- Checksum-manifest, package-directory, and package-README filename sets: exactly equal.
- Source and packaged plugin version checks: Claude `1.0.1`, Cursor `1.0.1`, Codex `1.0.1+codex.20260901`.
- Active release-path stale-version scan: no `1.0.0` reference.
- `python3 learn/scripts/test-smoker-model-matrix.py`: passed with `Smoker model matrix packaging: PASS`.
- `git diff --check`: passed.

## Re-evaluation

This report is the required full Security re-evaluation after the final material release-version amendment. The prior Low finding is resolved, and no Medium-or-above finding requires another remediation cycle.

## Next step

The exact final candidate is cleared to proceed to a fresh `quality-stinger` rerun. Before commit or push, the orchestrating agent must then load and run the orchestrator-level `github-repo-health-stinger`, per the repository Ship Gate.

## Exact-candidate addendum

After this final pass, `learn/packages/README.md:19` was corrected from "Rebuild all three archives" to "Rebuild all four archives." This is a documentation-only release-checklist correction that matches the four already-audited 1.0.1 artifacts. It changes no archive, checksum, manifest, generator, test, hook, skill, or runtime instruction. `git diff --check` passed after the correction. The final Security verdict remains 0 Critical, 0 High, 0 Medium, 0 Low, cleared for the fresh Quality rerun.
