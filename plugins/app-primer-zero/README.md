# App Primer Zero

Prepare a repository before the build starts: organize its private Library, establish current state, draft contracts and a complete schema baseline, qualify reuse candidates, and hand off a dependency-ordered wave plan.

This optional plugin runs directly in the current assistant. It uses the Wasp Nest core methods for repository setup, Knowledge, Library and shared contracts; it does not duplicate their specialist roles or add a new Drone. Its skill explicitly declares the standalone tier supported by this source repository.

## Invoke it

Install `wasp-nest-core` and `app-primer-zero` through the Wasp Nest marketplace, or select this pack with the source installer. Core is a required dependency. Review the installer's documented prerequisites before running it.

From the Wasp Nest source root:

```bash
./install.sh --packs app-primer-zero
```

This is an installation instruction for the user, not an action the skill runs automatically.

- Claude/Cursor plugin: use the discovered `app-primer-zero-stinger` skill, or the plugin command `app-primer-zero:app-primer-zero` where the harness exposes it.
- Codex: select `app-primer-zero:app-primer-zero-stinger`, or its generated command-as-skill wrapper when shown by the client. Use the exact installed selector.
- ZCode home installation: invoke the discovered `app-primer-zero-stinger`, command or generated command-as-skill wrapper. Selected home distributions include this pack's command and generated command-as-skill wrapper. Use the selector actually exposed by your installed client; native slash-command behavior depends on that client.
- Cowork: upload the built plugin and use the discovered skill/command. An accessible repository or supplied source archive is required; local shell and native subagents are capability-dependent.

Starter request:

```text
Run app-primer-zero for this repository. Inventory what exists, organize the
private Library within my authorized scope, draft the contracts/seams/schema
foundation, identify reusable committed modules, and produce a wave-plan
handoff. Keep approval and implementation status explicit. My harness/model
and maximum parallel slots are [supplied values]. CI preference is [supplied
preference]. Carry forward my existing decisions; ask only unresolved ones.
```

## What it delivers

The target repository receives current-state evidence under private knowledge; a foundation PRD with platform, data, contracts, reuse and verification sections; Draft shared CTRs or exact Accepted revision pins; a full source-field/schema ledger; a decision register; and a wave handoff with exclusive ownership and observable exits. No provider, model, framework, database or feature count is imposed. Document the actual repository's data/schema needs; a repository without a datastore does not need an invented database.

The fictional [Beacon Research example](skills/app-primer-zero-stinger/examples/beacon-research/README.md) demonstrates those handoffs without another customer's code, names, credentials or product rules. Its model/slot and schema values are teaching fixtures, not an accepted production design or throughput benchmark.

Read [the workflow map](skills/app-primer-zero-stinger/README.md), [runtime dependencies](skills/app-primer-zero-stinger/references/core-dependencies.md), and [source/build/install threading](skills/app-primer-zero-stinger/references/threading.md). All runtime guides, templates, examples and scripts live beneath the skill, so selected home/plugin installations retain them. The canonical plugin catalog assigns components and prerequisites; generated manifests and inventories follow that ownership map.

## Check the resources

```bash
python3 skills/app-primer-zero-stinger/scripts/validate_handoff.py skills/app-primer-zero-stinger/templates/wave-plan.example.json
python3 skills/app-primer-zero-stinger/scripts/test_validate_handoff.py
```

Run those from this pack directory, or resolve absolute paths from the installed skill. The validator reads a JSON planning artifact only. Its example returns PASS with expected fictional/unverified-capacity warnings. It cannot verify approval, installed harness capacity, source commit existence or a running app.

The helper keeps one logical integrator and counts actually overlapping work. In parallel mode, the coordinator consumes one slot and active reviewers count only when scheduled. A positive reviewer ceiling permits Security and Quality to reuse one slot in order. Explicit `serial-preparation` mode supports a one-slot preparation run and refuses implementation readiness. The [capacity contract](skills/app-primer-zero-stinger/references/capacity-and-review.md) defines the fields and limits. The helper supports at most 64 waves and 4,096 compatible concurrency sets, with disjoint canonical path prefixes rather than wildcard/exclusion leases.

First-party material is [AGPL-3.0-or-later](LICENSE.md). [Research notices](THIRD-PARTY-NOTICES.md) identify external primary sources. Source retains short attributed research notes; distribution retains the distillation and operational resources. This pack contains no hook, MCP server, account configuration or automatic implementation launcher.

<!-- wasp-pack-guide:start -->
## Choose a capability

This pack contains 1 skill, 0 agents and 1 source command. The table explains each source skill; open its linked instructions for exact inputs, outputs and limits.

| Skill | What it does and when to use it |
| --- | --- |
| [app-primer-zero-stinger](skills/app-primer-zero-stinger/SKILL.md) | Prepare an app's private Library, current state, contracts, complete schema baseline and bounded wave handoff before implementation. Use for app-primer-zero or foundation preparation. |

## Start one task

Required packs: `wasp-nest-core`

Install the selected pack and its prerequisites through the marketplace. For the version 3 layout, purge the previous installation first. Select the skill shown by your client, or paste this request with real paths and scope:

After adding the Wasp Nest marketplace, Claude Code uses these installation instructions:

```text
/plugin install wasp-nest-core@wasp-nest
/plugin install app-primer-zero@wasp-nest
```

Other clients use their plugin selection UI or discovered skill selector. Installing a package and invoking a task are separate steps.

```text
Run app-primer-zero for [repository]. Record current state, organize its Library, draft contracts and schema coverage, then deliver a bounded wave handoff. Use only the supplied stack and capacity decisions.
```

Expected result: Current-state knowledge, Draft contracts or accepted revision pins, a foundation PRD, schema/reuse ledgers and a reviewed handoff. It stops before implementation unless that work is separately authorized.



Claude Code plugin command names:

| Command | What it does |
| --- | --- |
| `/app-primer-zero:app-primer-zero` ([procedure](commands/app-primer-zero.md)) | Prepare an app's Library, contracts, schema and bounded wave-plan handoff before implementation. |

## Agent responsibilities

This pack declares no paired agents; its standalone skills run in the current assistant.

Codex can use the named skill or its generated `source-command-<name>` wrapper where a source command exists. Home installations may expose flat commands. Use the actual selector offered by the host. A pack with no paired agents runs its standalone skills directly; a skill name does not prove that a native agent was launched.

## Prerequisites and boundaries

No extra workflow-specific pack prerequisite is declared. Tool and account requirements remain in each skill.

Core supplies shared routing and review methods. Native Codex role registration requires the explicit installed-plugin registry and trusted Core hook; a marketplace selection alone is not proof of registration. Read the linked skill before work. Missing source, browser, connector, renderer or account access is a reported gap. Installation does not authorize sending, publishing, paid work or live settings changes.
<!-- wasp-pack-guide:end -->
