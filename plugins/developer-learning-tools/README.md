# Developer Learning Tools

Explain technical sources with source-grounded analogies and learner checks.

Requires `wasp-nest-core`. This is a source candidate; no installation or native-host qualification is implied.

<!-- wasp-pack-guide:start -->
## Choose a capability

This pack contains 4 skills, 4 agents and 5 source commands. The table explains each source skill; open its linked instructions for exact inputs, outputs and limits.

| Skill | What it does and when to use it |
| --- | --- |
| [builder-readiness-stinger](skills/builder-readiness-stinger/SKILL.md) | Help new coders prepare to build: clarify one goal, learning prerequisites, roles, expectations, unknowns and a first-slice proposal. |
| [project-learning-stinger](skills/project-learning-stinger/SKILL.md) | Teach web fundamentals through tiny projects, or prepare an exercise and criterion rubric from one supplied technical source revision. Use attempts, feedback and teach-back. |
| [technical-explainer-stinger](skills/technical-explainer-stinger/SKILL.md) | Explain technical sources, errors and generated code at grade 8 with bounded analogies, source claims, glossary and teach-back. |
| [testing-coach-stinger](skills/testing-coach-stinger/SKILL.md) | Teach contract-based testing through tiny exercises, failure interpretation and changed conditions. Use for learning assertions without copying implementation. |

## Start one task

Required packs: `wasp-nest-core`

Install the selected pack and its prerequisites through the marketplace. For the version 3 layout, purge the previous installation first. Select the skill shown by your client, or paste this request with real paths and scope:

After adding the Wasp Nest marketplace, Claude Code uses these installation instructions:

```text
/plugin install wasp-nest-core@wasp-nest
/plugin install developer-learning-tools@wasp-nest
```

Other clients use their plugin selection UI or discovered skill selector. Installing a package and invoking a task are separate steps.

```text
Use technical-explainer-stinger to explain [accessible technical source] at grade 8 with one bounded analogy, a glossary and source claims.
```

Expected result: A source-grounded explanation with a claim ledger, analogy limits and a teach-back question; reader comprehension remains separately observed.



Claude Code plugin command names:

| Command | What it does |
| --- | --- |
| `/developer-learning-tools:explain-this` ([procedure](commands/explain-this.md)) | Explain a technical source at grade 8 with a bounded analogy, glossary, evidence and teach-back. |
| `/developer-learning-tools:learn-through-project` ([procedure](commands/learn-through-project.md)) | Choose a beginner learning path and teach HTML, CSS and JavaScript through one bounded project with observed learning checks. |
| `/developer-learning-tools:practice-tests` ([procedure](commands/practice-tests.md)) | Teach independent tests from a stated contract with prediction, observed attempts, failure interpretation and changed-condition practice. |
| `/developer-learning-tools:prepare-learning-exercise` ([procedure](commands/prepare-learning-exercise.md)) | Prepare one source-linked technical exercise, teach-back and criterion-level evidence rubric without assuming mastery. |
| `/developer-learning-tools:prepare-to-build` ([procedure](commands/prepare-to-build.md)) | Help a new coder prepare one build goal with learning prerequisites, responsibilities, unknowns and a first-slice proposal. |

## Agent responsibilities

| Agent | Responsibility | Paired skill |
| --- | --- | --- |
| [builder-readiness-wasp-drone](agents/builder-readiness-wasp-drone.md) | Help a new coder prepare an app, site, desktop app, integration, plugin or tool: one scoped recommendation, prerequisites, roles, unknowns and first-slice proposal. | [builder-readiness-stinger](skills/builder-readiness-stinger/SKILL.md) |
| [project-learning-wasp-drone](agents/project-learning-wasp-drone.md) | Teach web fundamentals through small projects, or prepare an exercise and criterion rubric from one supplied technical source revision. | [project-learning-stinger](skills/project-learning-stinger/SKILL.md) |
| [technical-explainer-wasp-drone](agents/technical-explainer-wasp-drone.md) | Explain technical documents, posts, messages, errors or generated code at grade 8 with consistent analogies, glossary, source claims and teach-back. | [technical-explainer-stinger](skills/technical-explainer-stinger/SKILL.md) |
| [testing-coach-wasp-drone](agents/testing-coach-wasp-drone.md) | Teach independent contract-based assertions, test failure interpretation and changed-condition practice. | [testing-coach-stinger](skills/testing-coach-stinger/SKILL.md) |

Codex can use the named skill or its generated `source-command-<name>` wrapper where a source command exists. Home installations may expose flat commands. Use the actual selector offered by the host. A pack with no paired agents runs its standalone skills directly; a skill name does not prove that a native agent was launched.

## Prerequisites and boundaries

- `library-packets` also needs `documentation-tools`.

Core supplies shared routing and review methods. Native Codex role registration requires the explicit installed-plugin registry and trusted Core hook; a marketplace selection alone is not proof of registration. Read the linked skill before work. Missing source, browser, connector, renderer or account access is a reported gap. Installation does not authorize sending, publishing, paid work or live settings changes.
<!-- wasp-pack-guide:end -->
