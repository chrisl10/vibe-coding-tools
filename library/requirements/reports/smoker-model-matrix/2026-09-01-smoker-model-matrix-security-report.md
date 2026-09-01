# Security audit - 2026-09-01 - Smoker self-contained model matrix

## Executive summary

- Scope: the complete uncommitted working-tree candidate on `codex/smoker-self-contained-matrix` against `fork/main`, covering the canonical Smoker command, generated Codex and Cursor artifacts, generator changes, bundled model-matrix copies, and the regression test.
- Coverage: REDUCED COVERAGE. This candidate is a Markdown and Python distribution change rather than the SvelteKit, Neon, WorkOS, Stripe, Vercel, Doppler, and GoHighLevel application stack researched by `security-stinger`. All applicable secrets, path handling, generated-artifact integrity, prompt safety, dependency, and supply-chain controls were checked.
- Findings: 0 Critical, 0 High, 0 Medium, 0 Low.
- Ship Gate status: cleared to proceed to `quality-stinger`.

## Surface coverage checklist

### SvelteKit attack surface

None detected. The candidate adds no SvelteKit source, route, form action, environment import, HTML rendering, cookie handling, or CSP configuration.

### Authorization and tenancy (Drizzle / Neon)

None detected. The candidate adds no database access, SQL construction, authorization decision, tenant data, or persistence surface.

### Secrets and environment

None detected.

- The changed files contain no public-prefixed credential names, hardcoded secret defaults, private keys, provider tokens, or credential-shaped additions.
- No tracked or historically-added non-example `.env` file was found by the prescribed history sweep.
- GitHub reports secret scanning and push protection enabled for `chrisl10/vibe-coding-tools`, with zero open secret-scanning alerts at audit time.
- The new copies are regular repository files, not symlinks, and all three model-matrix files have SHA-256 `48743442d7a082db1eb421b807e3a88747080a517c55592b51176ad12e4ec7db`.

### Webhooks and third-party intake

None detected. The candidate adds no HTTP intake, signature verification, callback, outbound fetch, or externally supplied URL handling.

### Dependencies and supply chain

None detected.

- No package manifest, lockfile, workflow, Dockerfile, or dependency version changes are present.
- `learn/scripts/generate-harnesses.py:22-23` fixes both source and destination names as repository-owned constants.
- `learn/scripts/generate-harnesses.py:69-72` copies only the canonical repository matrix to a constant skill-local path. No request, environment, network, command execution, dynamic import, or caller-controlled path enters this operation.
- Regeneration changed only the expected candidate files and remained idempotent at the working-tree level.

### Headers and transport

None detected. The candidate does not change a deployed HTTP service, hosting configuration, security header, TLS setting, WAF rule, or rate limit.

### AI-generated code patterns

None detected.

- `.claude/commands/the-smoker.md:16-18` requires the exact matrix path to be resolved and read before dispatch, fails closed when it is missing or unreadable, and forbids ledger reuse or a silent high-cost fallback.
- `.agents/skills/the-smoker/SKILL.md:17-19` and `.codex/plugins/vibe-coding-tools/skills/the-smoker/SKILL.md:17-19` preserve the same fail-closed rule in the two Codex distribution surfaces.
- The added text does not grant a Bee broader authority, accept untrusted instructions, invoke a shell, weaken the Security then Quality gate, or bypass user review.
- `learn/scripts/test-smoker-model-matrix.py:18-29` checks the exact bundled bytes, rejects the obsolete relative path, and verifies both fail-closed prohibitions in each Codex Smoker skill.

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

## Verification evidence

- `python3 learn/scripts/generate-harnesses.py`: passed.
- `python3 learn/scripts/test-smoker-model-matrix.py`: passed with `Smoker model matrix packaging: PASS`.
- Command validation for `.claude/commands/the-smoker.md` across all harnesses: 0 errors, 0 warnings, 0 informational findings.
- Skill validation for `.agents/skills/the-smoker` across all harnesses: 0 errors, 0 warnings, 0 informational findings.
- Canonical-to-bundled byte comparisons for both Codex distribution surfaces: passed.
- `git diff --check`: passed.
- Deterministic changed-file secret and unsafe-execution sweeps: no confirmed findings.

## Re-evaluation

N/A. No Medium-or-above findings required fixes.

## Next step

The exact candidate is cleared to proceed to `quality-stinger`. Before commit or push, the orchestrating agent must then load and run the orchestrator-level `github-repo-health-stinger`, per the repository Ship Gate.
