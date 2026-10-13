# Bind the SBOM to the release artifact

Use this guide for O274. Start with [target audit](05-target-repository-audit.md) and the [release digest](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/src/skills/dependency-audit-stinger/references/research/release-evidence/digest.md). Produce the [release evidence worksheet](../templates/release-artifact-evidence.md).

## Identify what the consumer receives

Record exact source revision, workspace, toolchain and package-manager versions, target platform, build flags and distribution channel. Name the final tarball, wheel, executable, plugin ZIP or immutable image digest. A source checkout, lockfile or intermediate build directory is not the shipped subject. List each platform artifact separately. Hash exact final bytes and preserve the filename, algorithm, length and retrieval/build location. Repacking, signing or changing bytes requires a new digest and a new binding.

## Reconcile four inventories

| Evidence | Establishes | Does not establish |
|---|---|---|
| Manifest | Requested dependency declarations, peers, optional/dev scope | Exact resolution or packaged contents |
| Lockfile | Recorded resolved graph for its ecosystem | Actual install, inclusion in bundles or runtime loading |
| Installed tree/build graph | Observed build inputs at stated time/flags | All those inputs ship to users |
| Final artifact inventory | Observed files and recoverable package metadata in final bytes | Complete recognition of bundled/minified code, external runtime downloads or loaded modules |

For every direct/transitive component record identifier, version, scope, inclusion basis, evidence location and license/provenance status. Distinguish code embedded in a bundle from a runtime dependency declared for later installation. Record vendored code, native libraries, dynamically fetched models/plugins, optional platform packages and build-only tools. Unknown version/license/origin remains unknown. A scanner finding one package.json in a tarball cannot establish that it identified every bundled component. Reconcile source/lock/build information with artifact findings; preserve exclusions and unresolved coverage.

## Generate and inspect with existing tooling

Record generator/version, input path/digest, format/version, command, timestamp, stdout/stderr and exit status. Select CycloneDX or SPDX versions accepted by the receiving system, not a universal preferred version. npm sbom is project-graph evidence, including lock-only mode; labeling it as a packed-byte scan is incorrect. Reuse the target's installed tools. A missing generator or schema validator leaves that step pending, without installing one or downloading executable packages.

Validate against the exact selected format schema using an existing validator. Then inspect identity, dependency edges, hashes, missing/duplicate identifiers, license fields and coverage assumptions. JSON parsing proves parseability only. A nonzero component count is a weak sanity check and never a release acceptance rule by itself. Record schema validation separately from coverage review and vulnerability triage.

## Bind, sign and independently verify

The attestation subject is the final artifact's name/digest; its predicate is the SBOM. The SBOM itself also has a digest for evidence preservation. A signature verifies the signed claim under a selected identity/trust policy, not the truth or completeness of the inventory. The [retained template](../templates/github-actions-sbom-workflow.yml) now subjects the tarball; its version tags and scanner coverage need review before use. Current attest-sbom is deprecated in favor of actions/attest, as archived in the digest.

A consumer verifies the exact downloaded artifact, expected repository/workflow identity and intended predicate type. gh attestation verify defaults to build provenance, so an SBOM check must set the matching predicate type supported by the actual document. Read the predicate type from the produced statement and confirm it against the action and format version. Keep build provenance verification and SBOM verification results separate. Do not run signing, API persistence or publishing without authorization. Retain artifact, SBOM, attestation bundle, checksums and verifier output in the approved retention system; do not promise a legal retention period.

## Acceptance

Report each of: parsed, schema-valid, coverage-reviewed, subject-digest-matched, signature-valid, identity-policy-satisfied and release-upload-matched as proved, failed or pending with exact evidence. Release qualification requires the target's chosen coverage policy and independent Security/Quality gates. See the [rendered cases](../examples/release-artifact-evidence-cases.md).
