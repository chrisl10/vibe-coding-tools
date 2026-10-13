# Tauri Stinger

`tauri-stinger` is the Tauri 2 engineering knowledge package for `tauri-wasp-drone`. It covers desktop and mobile project structure, dependency alignment, Tauri 1 migration, typed IPC, capabilities, sidecars, AI runtime designs, persistence, native verification, signing, updater integration, and distribution.

The root `SKILL.md` is intentionally lean. Detailed work lives here:

- `guides/` contains one procedure per major engineering verb.
- `references/` contains the dated version snapshot, IPC and security model, derived AI architecture choices, and release checklist.
- `references/research/raw/` archives one primary-source note per official or upstream source.
- `references/research/distilled-tauri-2.md` ties every factual claim to that archive.
- `examples/` contains six practical AI-oriented and migration/update examples.
- `templates/` contains inspection, architecture, capability, upgrade, and release-evidence artifacts.
- `scripts/inspect-tauri-project.py` performs a deterministic, read-only first pass over a target project and emits JSON.

## Research posture

The primary release and advisory sweep covers 2026-03-03 through 2026-09-03. Mutable official documentation fetched at the cutoff supplies supplemental baseline behavior and is not presented as an in-window release.

The generated Tauri release website lagged several official package-specific GitHub releases dated 2026-08-31. The dated snapshot therefore records both the discrepancy and the package-specific tags used to resolve it. Runtime users must refresh current versions before changing a consumer project.

No first-party Tauri AI reference application was found in the official source sweep. Every hosted-provider, local-sidecar, native-runtime, stream-protocol, and AI persistence pattern is labeled as a derived application design.

## Inspector

Run from the Stinger directory:

```text
python scripts/inspect-tauri-project.py <project-root> --pretty
```

Run its deterministic in-memory check:

```text
python scripts/inspect-tauri-project.py --self-test --pretty
```

The inspector performs no network requests, project commands, or file writes. It parses strict JSON, `package.json`, and common one-line Cargo dependency forms. It reports JSON5, TOML, lockfiles, and complex glob overlap as manual-review limitations.

## Validation

From the repository root:

```text
python3 src/skills/queen-wasp-stinger/references/scripts/per-type-validation.py packs/backend-and-desktop-tools/skills/tauri-stinger --type skill --harness all
```

The required bar is zero validation errors, no non-portable frontmatter, no dynamic shell injection, no broken internal links, no unmarked mutable version defaults, and no em dash or en dash characters in authored prose.

## Scope boundary

This Stinger owns Tauri-specific integration. General Rust belongs to `rust-stinger`; frontend framework details belong to the relevant framework Stinger; formal security audit belongs to `security-stinger`; CI topology and release automation belong to `ci-release-stinger` or `devops-stinger`; dependency vulnerability triage belongs to `dependency-audit-stinger`.

## Desktop capability qualification update

For sidecar credentials use [guide 13](guides/13-qualify-sidecars-and-credential-brokers.md); for local schema upgrades and recoverable data use [guide 14](guides/14-qualify-local-data-migrations.md); for updater key/version/data transitions use [guide 15](guides/15-qualify-updater-trust-and-recovery.md); for tray, shortcuts and notifications use [guide 16](guides/16-qualify-tray-shortcuts-and-notifications.md); for real app acceptance beyond browser tests use [guide 17](guides/17-qualify-native-tests-beyond-the-browser.md). Read the [2026-10-07 evidence digest](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/backend-and-desktop-tools/skills/tauri-stinger/references/research/desktop-capabilities-20261007/distilled-desktop-capabilities.md), complete [the record](templates/desktop-capability-evidence.md), and distinguish [synthetic decisions](examples/08-desktop-capability-decisions.md) and the [temporary SQLite exercise](examples/09-sqlite-recovery-exercise.py) from native app proof.

## Native release qualification update

The [2026-10-07 digest](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/backend-and-desktop-tools/skills/tauri-stinger/references/research/native-release-20261007/distilled-native-release.md) grounds [macOS](guides/10-qualify-macos-release.md), [Windows](guides/11-qualify-windows-release.md), and [Linux](guides/12-qualify-linux-distribution.md) qualification. Use the [record](templates/native-release-qualification.md) and [eight synthetic candidate exercises](examples/07-native-release-candidate-decisions.md). This refresh covers release behavior, not a current Tauri package-version graph or native app proof.

## Local file safety update

For O105 use [bounded import](guides/18-qualify-local-import.md), [safe export](guides/19-qualify-safe-export.md) and [app-data uninstall](guides/20-qualify-app-data-uninstall.md). Read the [2026-10-08 digest](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/backend-and-desktop-tools/skills/tauri-stinger/references/research/file-safety-20261008/digest.md), fill the [evidence worksheet](templates/file-safety-evidence.md), and review the [fictional plan](examples/10-fictional-file-safety-plan.md) and [negative decisions](examples/11-file-safety-negative-cases.md). File selection is not arbitrary file authority. Require operation-specific approval, native identity/race review, bounded parsing, qualified publication and app-owned cleanup provenance. User documents/exports remain retained. Constructed cases are NOT_RUN; current runtime/plugin/OS support and native durability/uninstall proof remain consumer obligations.

