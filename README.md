# Vibe Coding Tools

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/legioncodeinc/brands/main/legion-code-inc/logos/legion-logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/legioncodeinc/brands/main/legion-code-inc/logos/legion-logo-light.svg">
  <img alt="Legion Code Inc." src="https://raw.githubusercontent.com/legioncodeinc/brands/main/legion-code-inc/logos/legion-logo-light.svg" width="280">
</picture>

### Get the Git life.

**AI coding agents, skills, commands, hooks, and rules for Codex, Claude Code, and Cursor.**

Give your coding assistant a whole Hive of specialists instead of one blank prompt.

</div>

<div align="center">

<a href="https://www.ospry.ai">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/legioncodeinc/brands/main/ospry/logos/png/core-assets/transparent/horizontal-white-1024.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/legioncodeinc/brands/main/ospry/logos/png/core-assets/transparent/horizontal-ink-1024.png">
    <img alt="OSPRY" src="https://raw.githubusercontent.com/legioncodeinc/brands/main/ospry/logos/png/core-assets/transparent/horizontal-ink-1024.png" width="260">
  </picture>
</a>

<sub>Want to know what will actually drive more revenue? <strong><a href="https://www.ospry.ai">OSPRY</a></strong> is the insight engine built for exactly that.</sub>

</div>

---

## Why bring the Hive into your repo?

Most AI coding assistants are brilliant new hires with no memory of how your team works. Every new task starts with the same tax: explain the architecture, repeat the standards, name the right tools, remind the agent to check security, and hope nothing important gets skipped.

Vibe Coding Tools stops that cycle.

- **75 Bees** give you focused specialists for Git, security, databases, testing, product work, documentation, design, and more.
- **78 Stingers** give those specialists repeatable playbooks, examples, templates, and research.
- **2 Hive commands** route work and drive PRDs to verified completion.
- **4 rules and 2 hooks** turn standards into active guardrails.
- **One Library system** gives humans and agents a durable place for requirements, decisions, issues, and knowledge.
- **Three native harnesses** let the same operating system work in Codex, Claude Code, and Cursor.

The win is not more AI output. The win is less guessing, less repeated prompting, fewer skipped checks, and work that can be reviewed against a written definition of done.

## Start here

The fastest first win is to give an existing repository a durable knowledge and requirements library.

1. Clone Vibe Coding Tools or install the package for your harness.
2. Open the repository you want to improve.
3. Give your assistant this request:

   ```text
   Use get-started-stinger to set up this repository with the Library Schema v2 structure. Inspect what already exists, preserve it, create only what is missing, and give me the final setup report.
   ```

4. Review the report before accepting human-decision items.
5. Put durable facts in `library/knowledge/`, planned work in `library/requirements/`, reactive work in `library/issues/`, and temporary notes in `library/notes/`.

The folder at [`learn/examples/library/`](learn/examples/library/) is a teaching example. `get-started-stinger` creates the live `library/` in your target repository.

[Read the full getting-started guide](learn/guides/GETTING-STARTED.md).

## Meet the Hive

This is not a loose pile of prompts. It is a chain of command built by [Legion Code Inc.](https://www.legioncodeinc.com).

| Hive piece | What it means | What it does |
|---|---|---|
| **Bee** | A specialist agent | Owns one domain and makes focused decisions |
| **Stinger** | The Bee's skill | Supplies the workflow, references, templates, and guardrails |
| **Beekeeper** | The router | Finds the right Bee and arms it with the matching Stinger |
| **Smoker** | The delivery orchestrator | Drives PRDs and every acceptance criterion through implementation, Security, Quality, and shipping |
| **Rule** | Always-on direction | Keeps every worker inside the same operating boundaries |
| **Hook** | Automatic enforcement | Checks important actions before or after tools run |

Every domain Bee has one paired Stinger. The generated [Asset Catalog](learn/ASSET-CATALOG.md) shows all 75 pairs and the three system-level skills that manage the Hive.

## Choose your harness

### Codex

A cloned repository works without installing the plugin:

- [`.agents/skills/`](.agents/skills/) contains all 80 repository-scoped skills: 78 Stingers plus the Beekeeper and Smoker workflows.
- [`.codex/agents/`](.codex/agents/) contains 75 native TOML agents.
- [`.codex/hooks.json`](.codex/hooks.json) and [`.codex/config.toml`](.codex/config.toml) provide project enforcement and routing.

Invoke the two command workflows as explicit Codex skills:

```text
$the-beekeeper route this task to the right specialists
$the-smoker execute these PRDs through verified completion
```

The installable plugin at [`.codex/plugins/vibe-coding-tools/`](.codex/plugins/vibe-coding-tools/) carries the same 80 skills and hooks for Codex CLI and the ChatGPT desktop app. The project adapter remains separate because plugin installation does not install repository agent TOMLs.

### Claude Code

The [`.claude/`](.claude/) tree contains 75 agents, 78 skills, 2 slash commands, 4 rules, 2 hooks, and the Claude Code plugin manifest.

```powershell
claude --plugin-dir .claude
```

Use `/the-beekeeper` to route work or `/the-smoker` to run the full delivery line.

### Cursor

The [`.cursor/`](.cursor/) tree contains 75 agents, 78 skills, 2 commands, 4 MDC rules, hooks, and a Cursor plugin manifest. Open the repository in Cursor and the project configuration is available in place.

## The Legion way

Code tells you what the machine does today. Documents tell you why it does it, what it should do next, and what must be true before you call the work finished.

That is why this system treats documentation as operational memory:

- Knowledge files preserve the domain truth that would otherwise disappear into a Slack thread or one person's head.
- ADRs preserve the reasoning behind expensive architecture decisions.
- PRDs turn ideas into goals, non-goals, user stories, and acceptance criteria an agent can actually execute.
- IRDs give bugs and incidents a traceable problem, cause, fix plan, and verification record.
- Security runs before independent Quality because a security fix can change what Quality needs to verify.

An agent with no context guesses. An agent armed with your project knowledge and a written definition of done can work like a teammate.

## Learn the system

- [Agents and Bees](learn/guides/AGENTS.md)
- [Skills and Stingers](learn/guides/SKILLS.md)
- [Commands](learn/guides/COMMANDS.md)
- [Product Requirements Documents](learn/guides/PRODUCT-REQUIREMENTS-DOCUMENT.md)
- [Library Structure](learn/guides/LIBRARY-STRUCTURE.md)
- [Hooks](learn/guides/HOOKS.md)
- [Rules](learn/guides/RULES.md)
- [Model Selection](learn/guides/MODEL-SELECTION.md)
- [Security and Secrets](learn/guides/SECURITY-AND-SECRETS.md)
- [Harness Compatibility](learn/guides/HARNESS-COMPATIBILITY.md)
- [Troubleshooting](learn/guides/TROUBLESHOOTING.md)

Ready-to-share archives and SHA-256 checksums live in [`learn/packages/`](learn/packages/).

## Build from the source of truth

The `.claude/` tree is the editable source. Regenerate the Cursor mirror, Codex agents, repository skills, plugin skills, and catalog after changing an agent, skill, command, or hook:

```powershell
python learn/scripts/generate-harnesses.py
```

Human guides and examples live under `learn/`. The hidden `.claude`, `.codex`, `.cursor`, and `.agents` directories stay at the repository root because the harnesses discover them there.

## License and attribution

Vibe Coding Tools is source-available software created by **Mario Aldayuz and [Legion Code Inc.](https://www.legioncodeinc.com)**.

You may use the Work personally, educationally, internally, commercially, and as a tool in paid services. You may not sell the Work itself, remove the attribution, or pass it off as your own. Read [LICENSE.md](LICENSE.md) for the complete terms.

---

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/legioncodeinc/brands/main/legion-code-inc/logos/legion-symbol-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/legioncodeinc/brands/main/legion-code-inc/logos/legion-symbol-light.svg">
  <img alt="Legion symbol" src="https://raw.githubusercontent.com/legioncodeinc/brands/main/legion-code-inc/logos/legion-symbol-light.svg" width="36">
</picture>

<sub><strong>We are Legion. Vibe with Legion.</strong></sub>

</div>
