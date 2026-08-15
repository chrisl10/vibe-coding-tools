# Vibe Coding Tools

**Give your AI coding assistant a senior team, a repeatable playbook, and safety rails in one repository.**

## Why use it?

Most coding assistants start every task like a smart new hire on day one. They can write code, but they do not automatically know your preferred workflow, which specialist should handle a job, where project knowledge belongs, or what must be checked before shipping.

Vibe Coding Tools fixes that. It gives you:

- 75 focused specialist agents for Git, security, testing, databases, product work, documentation, and more.
- 78 reusable skills with detailed procedures, examples, templates, and research.
- A setup skill that creates a clean documentation library in another repository.
- Delivery commands that route work and run planning, implementation, security, and quality in order.
- Rules and hooks that turn important standards into automatic checks.
- Native packages and project adapters for Claude Code, Codex, and Cursor.

The payoff is simple: less time explaining the same process, fewer missed steps, and work that is easier to review.

## Use it in a repository

The quickest first win is to create a documentation library for the project you are working on.

1. Clone Vibe Coding Tools or add its package for your AI tool.
2. Open the target repository with Claude Code, Codex, or Cursor.
3. Ask your assistant:

   ```text
   Use get-started-stinger to set up this repository with the Library Schema v2 structure. Inspect what already exists, preserve it, create only what is missing, and give me the final setup report.
   ```

4. Review the report. It separates files created, files left unchanged, assumptions, and decisions that still need a human.
5. Put durable project facts in `library/knowledge/`, planned work in `library/requirements/`, reactive work in `library/issues/`, and temporary human notes in `library/notes/`.

The folder at [`learn/examples/library/`](learn/examples/library/) is only a teaching example. The setup skill creates the live `library/` inside your target repository.

Read [Getting Started](learn/guides/GETTING-STARTED.md) for a slower walkthrough.

## Pick your tool

### Claude Code

The [`.claude/`](.claude/) directory is both a project configuration and a Claude Code plugin. It contains 75 agents, 78 skills, two commands, four Claude rules, and two hooks.

Test it directly from this checkout:

```powershell
claude --plugin-dir .claude
```

The plugin manifest is at [`.claude/.claude-plugin/plugin.json`](.claude/.claude-plugin/plugin.json).

### Codex

Codex uses two layers because its plugin and project-agent formats solve different jobs:

- The installable plugin at [`.codex/plugins/vibe-coding-tools/`](.codex/plugins/vibe-coding-tools/) provides 80 skills and the safety hooks.
- The project adapter at [`.codex/`](.codex/) provides 75 native TOML agents, project hooks, and configuration. This layer also works in the Codex IDE extension.

Add [`.codex/marketplace.json`](.codex/marketplace.json) as a local marketplace source, install `vibe-coding-tools`, and start a new Codex session. When working directly in this checkout, Codex also discovers the project adapter automatically after you trust the repository and review its hooks with `/hooks`.

### Cursor

Open this repository in Cursor. The [`.cursor/`](.cursor/) directory contains the native agents, skills, commands, rules, model matrix, and Cursor hook manifest. It also includes a package manifest at [`.cursor/.cursor-plugin/plugin.json`](.cursor/.cursor-plugin/plugin.json).

## How the pieces fit

| Piece | Plain-language job | In this project |
|---|---|---|
| Bee | A specialist teammate with one clear area of ownership | 75 agents |
| Stinger | The specialist's playbook, examples, and tools | 78 core skills |
| Command | A named workflow that coordinates several steps | 2 commands |
| Rule | Guidance that should stay active during work | 4 policies |
| Hook | A script that runs automatically around tool actions | 2 checks |

Every domain Bee has one matching Stinger. Three extra skills run the overall system: `beekeeper-suit`, `get-started-stinger`, and `queen-bee-stinger`.

The full generated inventory and compatibility ledger are in [Asset Catalog](learn/ASSET-CATALOG.md) and [Harness Compatibility](learn/guides/HARNESS-COMPATIBILITY.md).

Ready-to-share archives and SHA-256 checksums are in [`learn/packages/`](learn/packages/).

## Learn without the jargon

- [Agents](learn/guides/AGENTS.md)
- [Skills](learn/guides/SKILLS.md)
- [Commands](learn/guides/COMMANDS.md)
- [Hooks](learn/guides/HOOKS.md)
- [Rules](learn/guides/RULES.md)
- [Product Requirements Documents](learn/guides/PRODUCT-REQUIREMENTS-DOCUMENT.md)
- [PRD Execution Prompt](learn/guides/PRD-EXECUTION-PROMPT.md)
- [Library Structure](learn/guides/LIBRARY-STRUCTURE.md)
- [Model Selection](learn/guides/MODEL-SELECTION.md)
- [Security and Secrets](learn/guides/SECURITY-AND-SECRETS.md)
- [Troubleshooting](learn/guides/TROUBLESHOOTING.md)
- [Glossary](learn/guides/GLOSSARY.md)

## Source of truth

The `.claude/` tree is the editable source. Run the generator after changing agents, skills, commands, or hooks:

The root keeps only three human-facing Markdown documents: `README.md`, `CLAUDE.md`, and `LICENSE.md`. The `.gitignore`, hidden harness directories, and `learn/` remain at root because Git and the three AI tools discover them there. Human guides and the example library live under `learn/`.

```powershell
python learn/scripts/generate-harnesses.py
```

It normalizes Claude agent metadata, refreshes the Cursor mirror, generates Codex TOML agents, and updates the Codex plugin skills. Review the generated diff and run the validation gates before committing.

## License

[MIT](LICENSE.md). Built by [Legion Code Inc.](https://www.legioncodeinc.com).
