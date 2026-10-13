# 03. README authoring

How to fill `templates/README.md` so an AI or a human can complete it cleanly, and why the section order is fixed.

## Why this order

The canonical order is decreasing urgency: name and one-liner, badges, what it is, why it exists, quick start, install, usage, configuration, architecture, documentation, development, testing, deployment, contributing, license. Readers scan top to bottom and bail once they lose the thread, so the answers a first-time visitor needs to decide "is this worth my next five minutes" sit at the top, and reference material a returning user needs sits lower [raw/get-started--readme--how-to-write-a-github-readme-repoclip.md]. Do not reorder sections even if a later one feels more important to you: reordering forces every reader to hunt for the answer they came for.

## Filling it out

- **One-liner**: lead with the verb. "Converts CSV files to Markdown tables," not "This is a CSV project." State what it does and for whom.
- **Badges**: Up to 5, each carrying real information (CI status, version, license, coverage). Use only applicable badges. The template ships CI/license/release badges wired to `{org}`/`{repo}`/`{default_branch}` placeholders: fill those from the actual git remote, don't invent an org name. Drop any badge that would always read the same value; a badge that never changes conveys nothing.
- **Quick start vs Install vs Usage**: these are three different jobs, not one. Quick start is the smallest possible "install, run one command, see output": seconds, not a tour. Install is the full prerequisite list plus the exact copy-paste command, stated in that order (prerequisites first, so the reader isn't three lines into a failing command before learning they needed Node 20). Usage is where real value gets demonstrated: lead with the most common case, add one or two advanced examples after, keep each self-contained enough to copy and run without extra context [raw/get-started--readme--how-to-write-a-github-readme-repoclip.md].
- **Configuration**: a table, not prose. Every environment variable this project reads belongs here, cross-referenced with `.env.example` (guide `04`) so the two files never drift out of sync: the table's `{ENV_VAR_NAME}` rows should match `.env.example`'s keys exactly.
- **Architecture**: optional for a single-purpose utility, expected for anything with more than one moving part. GitHub renders ` ```mermaid ` fenced code blocks natively, so prefer a Mermaid diagram over an external image file that will go stale.
- **Contributing / License**: keep these short in the README itself and link out to `CONTRIBUTING.md` and the `LICENSE` file rather than duplicating their full content. A missing or ambiguous license legally defaults to "all rights reserved," which blocks corporate adoption even for genuinely open code: never leave the License section unfilled.

## Placeholder discipline

Every `{placeholder}` in the template exists so an AI filling this out has an explicit slot rather than a blank canvas to improvise on. Resolve as many as possible from observable repo state (package.json, git remote, LICENSE file, lockfile) before asking the user anything. For anything you can't observe (why the project exists, what the architecture diagram should show), leave the placeholder in place and flag it in the verification report rather than inventing plausible-sounding filler: a README that states something false is worse than one with a visible gap.

## Failure modes to avoid when filling this in

Named directly in the research: burying the value proposition under a table of contents or badge wall; a wall of text with no visual; an install command that only works because of local state on the machine that wrote it (test on a clean checkout mentally, or actually); describing a feature instead of showing a runnable example of it; and a README that references a version or API two releases old [raw/get-started--readme--how-to-write-a-github-readme-repoclip.md].

## Documentation and generated packets

Fill the Documentation section from the repository's actual files. Give each main reader a clear starting point. Label public and internal material, and keep internal links out of a public README. Remove empty rows or sections rather than implying that missing guides exist. A README is an entry point; do not duplicate the full library inside it.

Check the whole template family when the documentation layout changes: the project README, library root, public/private knowledge, requirements lifecycle, issues lifecycle, contracts, and routine reports. Library and Get Started copies of the same folder README must describe the same schema. For v2, feature plans live in `requirements/{backlog,in-work,completed}/prd-*/`, issue plans in `issues/{backlog,in-work,completed}/ird-*/`, and per-plan QA travels in `qa/`. Routine reports live in `requirements/reports/`. Do not seed the retired `knowledge-base/`, `requirements/features/`, or `library/qa/` layout.

When the team uses App Primer Zero, explain that it prepares current-state knowledge, Draft contracts, the foundation plan, and a bounded handoff before implementation. When it uses Library Packets, explain that it turns supported library sources into audience documents in Markdown, Word, PDF, and citations. Include their actual installed invocation only when the repository uses them. These workflows serve different tasks; neither makes unsupported facts true or authorizes publication. Do not add marketplace installation pitches to the target project's README.

Keep curated Markdown in its approved source domain. Store brand assets and generated binaries outside `library/` at the agreed output location. Keep a packet's full source map, private quotes, hashes, gaps, and review records in `_internal`, separate from public reader files and safe citations. Help guides, business briefs, and product explanations have different readers; use the appropriate starting point for each.

Before delivering the filled README, verify every link and named command against the receiving repository. Describe observed behavior as current, planned behavior as planned, and missing evidence as a gap. General explanations target grade 8; technical reference keeps needed precision. Use no em dashes and remove claims, badges, prerequisites, and feature-count targets that the source cannot support.
