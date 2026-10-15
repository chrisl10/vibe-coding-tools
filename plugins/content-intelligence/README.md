# Content Intelligence

Two research and drafting skills for finding a current topic worth covering. [Repo Radar](skills/repo-radar-stinger/SKILL.md) covers GitHub repositories; [Viral News](skills/viral-news-stinger/SKILL.md) covers news. Each verifies one candidate and may return no post when the evidence does not clear its gate.

Both are direct-use standalone skills, explicitly marked in frontmatter. They do not claim companion Drones and do not need one to run in the current assistant or an approved Routine.

These skills need a shared topic ledger and Exa or Firecrawl MCP access. For voice-matched drafts they also use your own separate voice skill (optional; without one they write in a neutral voice and say so). Installing this pack alone does not supply those dependencies or authorize unattended publication.

## Configure your preferences

Each skill reads one user-editable file at the start of every run, so the skills stay self-contained:

- [repo-radar-stinger preferences](skills/repo-radar-stinger/references/editorial-preferences.md)
- [viral-news-stinger preferences](skills/viral-news-stinger/references/editorial-preferences.md)

Edit these before your first run (keep the two files consistent if you want both skills to behave alike):

1. **Voice skill.** Replace `none` with the name of your own voice skill, for example `<name>-voice-skill`. When set and installed, the skill loads it before drafting and its rules win. When left at `none`, drafts are written in a neutral, clear voice and labeled as such; no persona is invented.
2. **Beats and audience.** The shipped beats are examples. Replace them with the subjects and audience you actually cover.
3. **Editorial policy (optional).** The default is politically neutral: no partisan advocacy, claims fact-checked, contested issues presented fairly. Add topics to avoid or emphasize if you have a policy. Preferences steer which candidates are picked; they never relax the fact-check and vetting gates.

The `voice-skill` metadata value in each `SKILL.md` is a placeholder; the preferences file is the setting the skills actually read.

First-party instructions are licensed under [AGPL-3.0-or-later](LICENSE.md). The source tree retains research captures for provenance; built plugins ship the distillations, not those raw captures. See [third-party notices](THIRD-PARTY-NOTICES.md).

<!-- wasp-pack-guide:start -->
## Choose a capability

This pack contains 2 skills, 0 agents and 1 source command. The table explains each source skill; open its linked instructions for exact inputs, outputs and limits.

| Skill | What it does and when to use it |
| --- | --- |
| [repo-radar-stinger](skills/repo-radar-stinger/SKILL.md) | Scan GitHub for repos trending in the last 24 hours (vibe coding, AI coding, AI memory, vulnerabilities) via Exa/Firecrawl MCP, vet ONE, and output post options in the user's voice with receipts. |
| [viral-news-stinger](skills/viral-news-stinger/SKILL.md) | Mine the last 24 hours of trending news via Exa/Firecrawl MCP, fact-check ONE topic, and output viral-ready post options in the user's voice with receipts. Use for scheduled news-post Routine runs. |

## Start one task

Required packs: `wasp-nest-core`

Install the selected pack and its prerequisites through the marketplace. For the version 3 layout, purge the previous installation first. Select the skill shown by your client, or paste this request with real paths and scope:

After adding the Wasp Nest marketplace, Claude Code uses these installation instructions:

```text
/plugin install wasp-nest-core@wasp-nest
/plugin install content-intelligence@wasp-nest
```

Other clients use their plugin selection UI or discovered skill selector. Installing a package and invoking a task are separate steps.

```text
Use repo-radar-stinger to investigate one current repository candidate. Verify the evidence and return a draft or explain why no candidate qualifies.
```

Expected result: A checked topic and draft options, or no post when the evidence fails. Exa/Firecrawl, the voice skill and shared ledger are separate prerequisites.



Claude Code plugin command names:

| Command | What it does |
| --- | --- |
| `/content-intelligence:research-content-opportunity` ([procedure](commands/research-content-opportunity.md)) | Vet one fresh content opportunity with receipts, source times, duplicate checks, and honest no-post exits. |

## Agent responsibilities

This pack declares no paired agents; its standalone skills run in the current assistant.

Codex can use the named skill or its generated `source-command-<name>` wrapper where a source command exists. Home installations may expose flat commands. Use the actual selector offered by the host. A pack with no paired agents runs its standalone skills directly; a skill name does not prove that a native agent was launched.

## Prerequisites and boundaries

No extra workflow-specific pack prerequisite is declared. Tool and account requirements remain in each skill.

Core supplies shared routing and review methods. Native Codex role registration requires the explicit installed-plugin registry and trusted Core hook; a marketplace selection alone is not proof of registration. Read the linked skill before work. Missing source, browser, connector, renderer or account access is a reported gap. Installation does not authorize sending, publishing, paid work or live settings changes.
<!-- wasp-pack-guide:end -->
