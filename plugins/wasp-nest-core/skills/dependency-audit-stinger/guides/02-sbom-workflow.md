# SBOM Workflow (Syft + CycloneDX + Sigstore) for the published package

> Preserved Hivemind npm case. Read [target repository audit](05-target-repository-audit.md) first; use the package-specific paths, guards and commands below only when the inspected target has them. Recheck vendor/version claims against current primary documentation before recommending or changing tools.

> **Research source:** `research/external/03-sbom-cyclonedx-spdx-2026.md` (CRITICAL)
> **Template:** `templates/github-actions-sbom-workflow.yml`

A Software Bill of Materials (SBOM) records identified components and their relationships within a stated scope. For the retained Hivemind case the release subject is the npm tarball. Coverage, schema conformance, legal requirements and procurement acceptance need separate evidence. Follow [artifact binding and coverage](07-bind-sbom-to-release-artifact.md) for current work.

---

## Format selection: CycloneDX 1.6 JSON

The retained case uses CycloneDX JSON. Select the exact format/version the consumer accepts and record the generator's actual emitted version; this example does not establish a universal preference over SPDX.

---

## Generator: Syft

| Artifact | Generator |
|---|---|
| The published npm tarball / built `bundle/` | `anchore/syft` (`anchore/sbom-action`) - native CycloneDX output, widest support |
| Single npm package (alternative) | `@cyclonedx/cyclonedx-npm` |

**Key rule:** generate from the **packed tarball or built bundle**, not the raw source tree. The `files` allowlist (`bundle`, `harnesses/*/bundle`, `mcp/bundle`, `scripts`, etc.) decides what actually ships - a source-tree SBOM would list devDependencies and unbundled source that never reach consumers, overstating the surface. Run `npm pack` (or build the bundle) first, then point Syft at the result. Source: `research/external/03-sbom-cyclonedx-spdx-2026.md`.

---

## The 5-step production workflow

1. **Build / pack the artifact** - `npm ci && npm run build`, then `npm pack` to produce the tarball that matches the `files` allowlist
2. **Generate the SBOM** from the packed tarball / `bundle/` using Syft (CycloneDX 1.6 JSON)
3. **Qualify the SBOM** - record parse/schema checks and reconcile artifact coverage with manifest/lock/build evidence. Component count alone cannot establish completeness.
4. **Attest with Sigstore** using `actions/attest-sbom@v2` (GitHub OIDC-backed, no long-lived keys)
5. **Store** - keep the SBOM as a release asset; extend GitHub artifact retention if a compliance horizon requires it

See `templates/github-actions-sbom-workflow.yml` for the ready-to-use implementation.

---

## Attestation: why and how

An unattested SBOM is a document; an attested SBOM is a signed claim. Sigstore attestation gives:

- A signed association between a named artifact digest and an SBOM predicate; it does not prove generation accuracy or coverage
- An immutable audit trail tied to the GitHub Actions OIDC token (no signing keys to manage)
- Consumer verification via `gh attestation verify`

```bash
# Illustrative consumer check: substitute actual artifact, identity and predicate
gh attestation verify ./deeplake-hivemind-<version>.tgz --repo <expected-owner>/<expected-repo> --predicate-type <actual-sbom-predicate-type>
```

---

## When to trigger SBOM generation

- **Trigger on tag push** (`on: push: tags: ['v*']`) or `release: published` - one SBOM per release, matching the npm version published.
- PR inventories can support dependency review, but they do not substitute for the final release-artifact binding.
- This pairs naturally with the existing release flow that also runs `npm publish`.

---

*Previous: `guides/01-vulnerability-triage.md`. Next: `guides/03-lockfile-discipline.md`.*
