# Repository Modernization Tools

Compose repository baseline, safe refactoring and contributor onboarding through selected specialist owners.

Requires `wasp-nest-core`. This is a source candidate; no installation or native-host qualification is implied.

<!-- wasp-pack-guide:start -->
## Choose a capability

This pack contains 1 skill, 1 agent and 6 source commands. The table explains each source skill; open its linked instructions for exact inputs, outputs and limits.

| Skill | What it does and when to use it |
| --- | --- |
| [flaky-test-repair-stinger](skills/flaky-test-repair-stinger/SKILL.md) | Repair flaky tests from observed failures with bounded causal reproduction, narrow fixture fixes, preserved assertions and exact final-candidate evidence. |

## Start one task

Required packs: `wasp-nest-core`

Install the selected pack and its prerequisites through the marketplace. For the version 3 layout, purge the previous installation first. Select the skill shown by your client, or paste this request with real paths and scope:

After adding the Wasp Nest marketplace, Claude Code uses these installation instructions:

```text
/plugin install wasp-nest-core@wasp-nest
/plugin install repository-modernization-tools@wasp-nest
```

Other clients use their plugin selection UI or discovered skill selector. Installing a package and invoking a task are separate steps.

```text
Use improve-repository on [repository/ref] to establish a baseline, then refactor-safely for [authorized bounded change] and verify-refactor for exact before/after evidence.
```

Expected result: A current baseline and selected-owner repair/refactor/onboarding workflow with concrete evidence and unsupported surfaces reported; no implicit deletion, migration or release.



Claude Code plugin command names:

| Command | What it does |
| --- | --- |
| `/repository-modernization-tools:improve-repository` ([procedure](commands/improve-repository.md)) | Establish a repository baseline and prepare evidence-backed, owned repair batches. |
| `/repository-modernization-tools:onboard-contributor` ([procedure](commands/onboard-contributor.md)) | Prepare and exercise a contributor setup path, first contribution and complete contractor handoff packet when requested using actual repository evidence. |
| `/repository-modernization-tools:refactor-safely` ([procedure](commands/refactor-safely.md)) | Convert bloat evidence into bounded behavior-preserving repairs with baseline and rollback proof. |
| `/repository-modernization-tools:remove-unused-dependencies` ([procedure](commands/remove-unused-dependencies.md)) | Remove manually qualified unused dependencies within exact approved package and lockfile scope, with before/after import and build proof. |
| `/repository-modernization-tools:repair-flaky-tests` ([procedure](commands/repair-flaky-tests.md)) | Diagnose observed flaky failures and repair a bounded causal defect while preserving test assertions and evidence. |
| `/repository-modernization-tools:verify-refactor` ([procedure](commands/verify-refactor.md)) | Compare pinned refactor behavior, performance, and accepted interfaces with explicit evidence limits. |

## Agent responsibilities

| Agent | Responsibility | Paired skill |
| --- | --- | --- |
| [flaky-test-repair-wasp-drone](agents/flaky-test-repair-wasp-drone.md) | Observed-failure flaky-test triage and bounded test/fixture repair specialist. | [flaky-test-repair-stinger](skills/flaky-test-repair-stinger/SKILL.md) |

Codex can use the named skill or its generated `source-command-<name>` wrapper where a source command exists. Home installations may expose flat commands. Use the actual selector offered by the host. A pack with no paired agents runs its standalone skills directly; a skill name does not prove that a native agent was launched.

## Prerequisites and boundaries

- `improve-repository-audit` also needs `code-audit-tools`.
- `refactor-language` also needs `backend-and-desktop-tools`.
- `refactor-browser` also needs `browser-and-app-testing-tools`.
- `onboard-docs-site` also needs `documentation-tools`.
- `remove-dependencies-audit` also needs `code-audit-tools`.
- `remove-dependencies-backend` also needs `backend-and-desktop-tools`.
- `remove-dependencies-web` also needs `web-development-tools`.
- `repair-flaky-tests-browser` also needs `browser-and-app-testing-tools`.
- `repair-flaky-tests-web` also needs `web-development-tools`.
- `repair-flaky-tests-backend` also needs `backend-and-desktop-tools`.

Core supplies shared routing and review methods. Native Codex role registration requires the explicit installed-plugin registry and trusted Core hook; a marketplace selection alone is not proof of registration. Read the linked skill before work. Missing source, browser, connector, renderer or account access is a reported gap. Installation does not authorize sending, publishing, paid work or live settings changes.
<!-- wasp-pack-guide:end -->
