# Getting Started

## What you are setting up

Vibe Coding Tools has two jobs:

1. Give your AI assistant specialist agents and playbooks.
2. Help your project store durable knowledge and requirements in a predictable `library/`.

The safest setup is additive. It inspects the target repository, preserves existing work, and creates only missing files.

## Step 1: choose a harness

- **Claude Code:** Run `claude --plugin-dir <path-to-checkout>/.claude`, or install that plugin directory using your normal Claude Code plugin workflow.
- **Codex:** Add `<path-to-checkout>/.codex/marketplace.json` as a local marketplace, install `vibe-coding-tools`, and start a new session. A direct checkout also provides native `.codex/agents` and hooks.
- **Cursor:** Open the checkout or copy/install the `.cursor` package into the target repository.

## Step 2: initialize the target repository

Open the repository you want to improve and ask:

```text
Use get-started-stinger to initialize Library Schema v2 here. Inspect existing documentation and harness files first. Preserve existing content, create only missing pieces, and produce a setup report with created, unchanged, assumed, and human-decision sections.
```

The skill should create a live structure like:

```text
library/
  knowledge/
    public/
    private/
  requirements/
    backlog/
    in-work/
    completed/
    reports/
  issues/
    backlog/
    in-work/
    completed/
  notes/
```

## Step 3: review before committing

Check the setup report and `git diff`. Confirm:

- No existing document was silently overwritten.
- Product facts were not invented.
- Live files are under the target repository's `library/`, not this repository's example folder.
- Harness instructions point to paths that exist.
- Secret examples use obvious placeholders.
- Security ran before quality for a release-sized change.

## Step 4: try one real task

Good first tasks include:

```text
Use the-beekeeper to route a README rewrite. Explain the chosen Bee and Stinger.
```

```text
Use product requirements guidance to draft a backlog PRD for passwordless sign-in. Make every acceptance criterion observable.
```

```text
Use git-stinger to explain how to recover an accidentally deleted local branch. Show the recovery path before any destructive command.
```

## Step 5: keep the mirrors current

When contributing to Vibe Coding Tools, edit `.claude` as the source and run:

```powershell
python learn/scripts/generate-harnesses.py
```

Review the `.cursor` and `.codex` output. Generated does not mean automatically correct; validation still matters.
