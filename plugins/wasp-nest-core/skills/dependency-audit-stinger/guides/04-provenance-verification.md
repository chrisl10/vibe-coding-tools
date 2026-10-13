# Provenance Verification + Publish-Time Guards

> Preserved Hivemind npm case. Read [target repository audit](05-target-repository-audit.md) first; use the package-specific paths, guards and commands below only when the inspected target has them. Recheck vendor/version claims against current primary documentation before recommending or changing tools.

> **Research source:** `research/external/04-npm-provenance-sigstore-2026.md` (HIGH)

Two things protect the integrity of what `@deeplake/hivemind` ships: npm provenance (proof of where the package was built) and the repo's own publish-time guards (proof that nothing unexpected got into the tarball). This guide covers both.

---

## npm provenance (Sigstore-backed)

Provenance is cryptographic proof of where a package was built and from what source. It answers: "was this tarball actually built from the claimed repo, or tampered with post-build?"

### Publishing with provenance

```bash
# From GitHub Actions (OIDC-enabled runner)
npm publish --provenance --access public
```

Requirements:
- Must run from GitHub Actions (or another Sigstore-supported CI) with `id-token: write` permission
- Generates a Sigstore attestation automatically - no signing keys to manage
- The attestation is stored in the npm registry and visible at `npmjs.com/package/@deeplake/hivemind/v/<version>`

Treat those paths as retained case facts. Verify actual runner/provider, repository metadata, package visibility, publish method and authorization. Current npm trusted publishing can generate provenance automatically without the flag; see the [fresh release digest](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/src/skills/dependency-audit-stinger/references/research/release-evidence/digest.md). Do not change release configuration or publish from this guide alone.

### Verifying provenance as a consumer

```bash
# Basic verification of the resolved tree
npm audit signatures

# Full Sigstore bundle output (March 2026 addition) - for CI integration
npm audit signatures --json --include-attestations
```

The current npm audit manual documents signature checks and include-attestations output. Verify the installed CLI supports those flags and preserve actual output; the [fresh audit capture](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/src/skills/dependency-audit-stinger/references/research/release-evidence/raw/npm-audit.txt) is documentation, not an executed consumer verification.

### What provenance does and does not tell you

- **Does:** the source repo URL + commit SHA the tarball was built from, the workflow run that produced it, that it was not modified after CI.
- **Does NOT:** vouch that the source code itself is trustworthy. Provenance is a transport guarantee, not a content guarantee - a compromised repo produces valid provenance.

---

## The publish-time guards (this repo's own controls)

Provenance proves the build pipeline; these guards inspect bounded aspects of the tarball contents. They are already wired into `package.json` and must not be weakened.

### Guard 1: the `files` allowlist

`package.json` `files` is an allowlist, not a denylist. The retained case lists: `bundle`, the harness bundles (`codex`, `cursor`, `hermes`, `pi`, `openclaw`), `mcp/bundle`, `.claude-plugin`, `scripts`, `README.md`, `LICENSE`. Inspect the actual tarball to establish inclusion; npm also has automatically included files and packing rules. A files list alone cannot prove that secrets or unexpected content are absent. Adding a broad entry (or a `.npmignore` that fights the allowlist) is a supply-chain regression: review any change here.

### Guard 2: `pack-check.mjs`

`npm run pack:check` runs `scripts/pack-check.mjs`, which inspects what `npm pack` would publish and blocks the release if secrets or unexpected files slipped past the allowlist. Run it before any manual publish and keep it in the release pipeline.

### Guard 3: `audit:openclaw`

`npm run audit:openclaw` runs `scripts/audit-openclaw-bundle.mjs`, which replicates the static scan that ClawHub performs on the OpenClaw bundle. Run it before publishing the OpenClaw harness so a rejection surfaces locally, not after publish.

### Guard 4: CodeQL

`.github/workflows/codeql.yaml` scans `javascript-typescript`. It is application-code SAST, not dependency scanning - but it is part of the pre-release defense, so confirm it is green before a release tag.

---

## Pre-publish checklist for a release

| Step | Command / check |
|---|---|
| Reproducible install | `npm ci` (not `npm install`) |
| CVE baseline | `npm audit --audit-level=high` clean or triaged (see `guides/01`) |
| Tarball contents safe | `npm run pack:check` passes |
| OpenClaw bundle safe | `npm run audit:openclaw` passes |
| SAST green | CodeQL workflow passing |
| Provenance | publish with `npm publish --provenance --access public` from CI |
| Consumer verification | `npm audit signatures` after publish |

---

*Previous: `guides/03-lockfile-discipline.md`. Return to `SKILL.md` for the full guide map.*
