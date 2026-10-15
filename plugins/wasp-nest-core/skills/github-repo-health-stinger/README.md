# github-repo-health-stinger

Repository hygiene auditor for GitHub repositories. Encodes the 2026 authoritative checklist across eight dimensions: branch protection rulesets, commit quality (Conventional Commits), CODEOWNERS, CI workflow density, docs presence, .gitignore, issue/PR templates, and repo settings.

Paired with: `github-repo-health-wasp-drone` (the Drone that wields this Stinger).

**Start here:** `SKILL.md` - the routing table, hard rules, and scoring weights.


**Research summary:** `research/research-summary.md` - 12 primary sources synthesized, normal depth tier, May 2026 window.

## Current plugin owner

This capability stays in required Wasp Nest Core. Its canonical source is src/skills, with canonical ownership recorded in the root [plugin catalog](../../plugin-catalog.json). Its SKILL.md metadata declares any standalone/orchestrator exception; specialist agents keep their actual paired Stinger. Host home/plugin files are generated carriers. Use [the layout and selection guide](../../learn/reference/PLUGIN-LAYOUT.md) when a workflow calls an optional specialist; source references alone do not enable an installed plugin.


## Automation permission review

[Guide 10](guides/10-review-automation-permissions.md) traces events, executable inputs, authority and candidate proof. Use the [worksheet](templates/automation-permission-review.md), [synthetic cases](examples/automation-permission-cases.md) and 2026-10-07 primary digest. This source enhancement does not repair a live repository.
