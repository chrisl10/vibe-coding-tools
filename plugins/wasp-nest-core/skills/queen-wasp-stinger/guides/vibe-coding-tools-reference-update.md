# Vibe Coding Tools reference update

Vibe Coding Tools is the repository that carries The Wasp Nest. Every forge, registration, or removal changes what the repository claims about itself, and stale references rot faster than code. This guide is the sweep you run after any component change.

## The reference surfaces

| Surface | What lives there | Update when |
|---|---|---|
| `src/skills/`, `packs/<plugin-id>/skills/` | Canonical Stingers in their declared owner | Any skill forged, updated, replaced, or removed |
| `src/agents/`, `packs/<plugin-id>/agents/` | Canonical Drones in the same owner as their Stinger | Any Drone forged, updated, replaced, or removed |
| `src/skills/pest-controller-suit/` | Roster, guides, sequences | Any pair registered or deregistered |
| `plugin-catalog.json` | Single component ownership, source roots, prerequisites and profiles | Every approved ownership or capability change |
| Generated home/plugin trees | Host projections, owner-specific command adapters and manifests | Rebuild after canonical changes; never hand-edit these as source |
| `AGENTS.md` | Cross-harness rules baseline (Codex native, Cursor native, Claude Code via import bridge) | Rule changes that should reach more than one harness |
| `CLAUDE.md` | Claude Code project guidance, mirrors `.cursor/rules/` per repo convention | Rule changes; keep the mirror statement true |
| `RULES.md` | Human explanation of each always-on rule | Any rule added or changed |
| `README.md` | Repo landing page, Wasp Nest overview | Structural changes: new component types, replaced systems |
| `library/` | Planning docs, knowledge docs, ADRs, PRDs, IRDs (Library Schema v2), Ship Gate reports | Every development cycle; reports land here |

## The post-change sweep

Run top to bottom after forging, updating, or removing any component:

1. **Component files themselves.** New or changed files in the right canonical location, folder name matches frontmatter name, Wasp Nest convention blocks present and verbatim.
2. **Pest Controller roster.** Row added, changed, or removed; guide file matches; registered count accurate; multi-Drone sequences still name real Drones.
3. **Cross-links.** Every related-skills list that should mention the component does, and none point at removed paths. Search the active authored files under `src/`, `packs/`, `docs/`, `learn/`, `publishing/`, and root docs for the old name. Preserve raw captures and historical records. Also inspect actual installed paths when that installation is in the authorized scope before declaring a removal complete.
4. **Rules bridges.** Rule changes need their own explicit scope. Update only the authorized canonical rule/templates and matching explanations; do not silently change src/AGENTS.md or user/global instructions during a documentation or component sweep.
5. **Library docs.** Decision-grade changes get an ADR. Feature work traces to its PRD or IRD. Ship Gate reports for the change sit in the relevant `library/` directory.
6. **Plugin builds.** If the component ships to Codex or Cowork via the plugin layer, rebuild and revalidate the plugin (`per-type-validation.py --type plugin`, then the Cowork packager if applicable). A source change is not a live deployment. Validate the generated owner plugin and dependency closure; install, registry writes, publication and pushes remain separately authorized effects.
7. **Repo hygiene conventions.** No em dashes in any prose written for the repo (chat, docs, commits, PR descriptions, comments). PRs checked for merge conflicts before being called shippable. Other agents' active work left untouched.

## Replacement records

When a system component is replaced wholesale (skill-creator and stinger-forge into queen-wasp-stinger being the founding example), record it where the next contributor will look:

- A short note in the successor's README naming what it replaced and why.
- The pest-controller deregistration steps from [pest-controller-registration.md](pest-controller-registration.md).
- An ADR in `library/` if the replacement changed how the system works, not just which file does the work.

## Drift audits

Once a quarter, or after any burst of parallel agent work, run a drift audit: validate every skill and agent under its catalog source_root with `per-type-validation.py --harness all`, grep the roster against the filesystem in both directions (registered but missing, present but unregistered), and spot-check that harness claims in the guides still match the research corpus. Harnesses ship fast; when the guides and the world disagree, re-run the research pipeline and update `references/research/` rather than hand-patching claims.
