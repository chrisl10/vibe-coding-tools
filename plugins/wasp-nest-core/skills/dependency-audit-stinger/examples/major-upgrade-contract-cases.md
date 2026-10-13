# Rendered major-upgrade contract cases

Cases are review exercises, not actual dependency upgrades.

## Type-compatible change to defaults

Synthetic client v1 retries zero times; v2 retries three times while keeping request(url) callable. The lock resolves and compilation passes. Existing payment request consumer assumes one attempt. Decision: needs migration work; characterize retry/idempotency behavior with Payments/Security owners before canary. Passing install does not establish equivalence.

## Svelte migration with unexamined consumers

The [official migration snapshot](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/src/skills/dependency-audit-stinger/references/research/release-evidence/raw/svelte-migration.txt) documents Svelte 5 changes and compatibility paths. A candidate updates one component but leaves an internal consumer unexamined. Decision: needs migration work until the actual consumed APIs, events and behavior have baseline/candidate evidence. This is a source-review case; no Svelte application was compiled here.

## Rollback blocked by persistent format

Synthetic v2 writes a new on-device state shape that v1 cannot read. Reinstalling the old executable restores bytes but not data compatibility. Decision: stop release preparation at the unresolved migration/restore contract; obtain an authorized rehearsal. Do not call artifact rollback safe solely because an old binary exists.

## Unknown native target

A Linux build passes while an optional ARM native module has no candidate build/runtime evidence. Decision: ready only for the tested, explicitly scoped Linux test environment; ARM release remains pending. No forced peer/native override is accepted as proof.
