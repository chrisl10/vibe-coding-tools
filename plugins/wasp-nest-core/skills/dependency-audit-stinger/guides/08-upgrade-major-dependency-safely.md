# Upgrade a major dependency with explicit contracts

Use this guide for O111. Start with [target audit](05-target-repository-audit.md), release digest and the [upgrade worksheet](../templates/major-upgrade-evidence.md). This procedure prepares or executes only the scope the owner authorized.

## Capture the baseline before changing dependencies

Record ecosystem, package manager/version, runtime/compiler, manifest/lock/vendor hashes, installed resolution, build flags, target platforms and last passing source/artifact checks. Inventory direct and transitive exposure, peers, overrides, optional native modules, install scripts and internal consumers. Name exact old and proposed new versions. Archive the vendor's official release notes and migration guide for those versions. A semantic major is a signal to investigate, not a complete inventory of breaking changes; pre-1.0 projects and unusual version policies require their actual contracts.

## Translate migration notes into affected contracts

Map each consumed API to its before/after signature, behavior, default, error and serialization format. Include exports/module format, auth/session behavior, HTTP/event contracts, DB migrations, persistent on-device formats, generated SDKs, native ABI, license notices and vendor patches. Explicitly record unaffected or unexamined surfaces, with basis. Route application/security, language, database or UI work to the selected specialists. Keep scope narrow; a forced resolution or peer override does not repair an incompatible consumer.

## Choose the actual ecosystem's verification

| Ecosystem | Capture and controlled verification | Caution |
|---|---|---|
| npm | package.json, lock, installed graph; authorized clean npm ci with original resolution flags | Removes node_modules and can execute scripts. Passing install does not prove API behavior. |
| pnpm | workspace/package manifests, pnpm-lock.yaml, peer settings; frozen-lockfile under authorized install | Check actual workspace filters and pnpm version. |
| uv/Python | pyproject, uv.lock, interpreter/platform extras; freshness check with locked, then authorized sync | frozen skips freshness checking; import success does not prove compatibility. |
| Cargo | Cargo.toml/lock, features, rust-version/target; locked checks or frozen with available cache | frozen also forbids network; native linking/runtime still needs proof. |
| Go | go.mod/sum, replace directives, module graph, vendor state/build target | Checksums are not an npm-style full install lock; review actual selection and binary build. |

Consult the archived official manuals for exact flags. Preserve manifest, resolved graph and install evidence independently. Do not install missing tooling or rewrite dependencies during a read-only audit.

## Execute one bounded candidate when authorized

Use an isolated owner-approved checkout. Change the identified dependency family and required migration edits only. Inspect manifest/lock differences for unexpected packages, registry/source changes, weakened integrity, peers and scripts. Run focused contract tests, consumers, types, build, native targets and baseline security checks. Capture new artifact hashes and compare expected exports/assets/size/licensing. A green lock or compiler is insufficient when runtime contracts changed. Revert or stop on unexpected scope.

## Canary, rollback and acceptance

Define the canary population/environment, measurable error/latency/resource/behavior thresholds, observation duration, evidence owner and stop condition before a live rollout. Do not deploy as part of preparation. Preserve the exact old source/lock/config and artifact, compatibility with persistent data, and a demonstrated restore procedure in an authorized test environment. If the new version writes irreversible data, artifact rollback alone is unsafe; require migration/restore design from the database owner before release.

The recommendation is one of ready for approved canary, needs migration work, or stop, with evidence. Equivalence is bounded to tested contracts and platforms. Unknown consumers and unavailable native tests remain pending. No claim of safe upgrade comes from a worksheet, synthetic case or version bump. See [upgrade cases](../examples/major-upgrade-contract-cases.md).
