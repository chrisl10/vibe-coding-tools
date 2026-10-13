# Distilled research: product design packages and the Claude Design round trip

Research window: 2026-04-12 to 2026-10-12. Fetched 2026-10-12. 24 raw sources in `raw/`, indexed with hashes in `source-ledger.json`. Every claim ends with its raw file. Foundational UX method sources older than the window are kept on purpose and labelled; no newer primary source replaced them in the sweep.

Repo-internal sources (not re-researched, cited by path): Impeccable context contract and detector gate (`packs/web-development-tools/skills/impeccable-stinger/guides/01-context-contract.md`, `06-detector-gate.md`), webapp-capture handoff template (`packs/browser-and-app-testing-tools/skills/webapp-capture-stinger/references/prompts/claude-design-handoff.md`, `guides/02-component-library-capture.md`), design-system bootstrap (`packs/web-development-tools/skills/design-system-stinger/SKILL.md`), and UX/UI enforcement (`packs/web-development-tools/skills/ux-ui-stinger/SKILL.md`).

## 1. Claude Design: what is confirmed, what is not

Read this section before writing any brief or import. Claude Design export details are thin. Anthropic documents the export menu, not the file contents.

### 1.1 Confirmed by official Anthropic sources

| Fact | Source |
|---|---|
| Launched 2026-04-17 as an Anthropic Labs research preview for designs, prototypes, slides and one-pagers | [raw/claude-design--anthropic-launch-announcement.md] |
| Now an artifact template usable in any chat, in Claude Code and from the Artifacts tab; standalone claude.ai/design closes 2026-12-14 | [raw/claude-design--support-get-started.md] |
| On by default for Free, Pro, Max, Team; Enterprise on by default from 2026-10-15 | [raw/claude-design--support-get-started.md] |
| Inputs: prompt, images, screenshots, wireframes, decks or documents (DOCX, PPTX, XLSX named at launch), a linked code repository, a web capture tool | [raw/claude-design--anthropic-launch-announcement.md], [raw/claude-design--support-get-started.md] |
| A strong prompt states goal, layout, content and audience | [raw/claude-design--support-get-started.md] |
| Projects inherit the organization design system; Claude checks output against it before showing it | [raw/claude-design--support-get-started.md] |
| Design systems import from a GitHub repo, design files, raw uploads, or a local codebase via `/design-sync` in Claude Code | [raw/claude-design--support-get-started.md] |
| Editing: chat, inline canvas comments, direct canvas editing; launch also named adjustment knobs and custom sliders | [raw/claude-design--support-get-started.md], [raw/claude-design--anthropic-launch-announcement.md] |
| Export menu: Download as .zip; PDF; PPTX; standalone HTML; Google Slides; send to a list of partner tools (Canva, Lovable, v0, Vercel, Netlify and others) | [raw/claude-design--support-get-started.md] |
| Handoff to Claude Code: "Send to local coding agent" or "Send to Claude Code Web"; Claude "packages everything into a handoff bundle" | [raw/claude-design--support-get-started.md], [raw/claude-design--anthropic-launch-announcement.md] |
| From Claude Code, `/design` can import a design into a codebase, export code as a live prototype, or build the whole thing | [raw/claude-design--support-get-started.md] |
| No version history yet; usage counts toward shared Claude limits; inline comments sometimes do not appear | [raw/claude-design--support-get-started.md] |

### 1.2 Reported by secondary or community sources only

| Claim | Source | Confidence |
|---|---|---|
| `/design-sync` targets React design systems; first sync can take hours on large repos; needs a claude.ai account and `/design-login` | [raw/claude-design--aicatchup-design-sync.md], [raw/claude-design--serverworks-design-sync-walkthrough.md] | medium (secondary cites Anthropic docs; practitioner reproduced it) |
| `/design` needs Claude Code v2.1.265 or later; artboards export as PNG or PDF | [raw/claude-design--aicatchup-design-sync.md] | medium |
| The Share menu yields a prompt pointing Claude Code at a `claude_design` MCP endpoint plus the project URL; first attempt may fail on MCP OAuth until `/mcp` completes | [raw/claude-design--serverworks-design-sync-walkthrough.md] | low to medium (one practitioner) |
| The handoff tells Claude Code to fetch the design and read a README; the zip is a fallback | [raw/claude-design--horadecodar-export.md] | low (one practitioner) |

### 1.3 Not documented anywhere in the sweep (treat as unknown)

- The file and folder layout of the .zip download. [raw/claude-design--support-get-started.md], [raw/claude-design--horadecodar-export.md]
- The contents of the Claude Code handoff bundle. [raw/claude-design--anthropic-launch-announcement.md], [raw/claude-design--aicatchup-design-sync.md]
- Whether exports carry design tokens in any machine format (DTCG JSON, CSS variables, DESIGN.md). No source says so.
- Whether standalone HTML keeps interactions when opened offline. [raw/claude-design--horadecodar-export.md]
- Direct PNG, JPEG or SVG export from the web canvas (not in the official export list). [raw/claude-design--support-get-started.md]

Consequence for this skill: the import procedure inventories whatever arrives and derives tokens from evidence (CSS custom properties, computed values, screenshots). It never assumes a file exists because a guide said so.

## 2. Journeys, flows and information architecture

| Artifact | Use when | Must contain | Source |
|---|---|---|---|
| Journey map | Goal spans channels or time; emotions matter | One actor; scenario and expectations; phases; actions, mindsets, an emotion line; opportunities with owner and metric | [raw/ux--nngroup-journey-mapping-101.md], [raw/ux--nngroup-journeys-vs-flows.md] |
| Task flow | Goal completes in minutes or hours inside one product | Key user steps and system responses; ideal path; no emotions | [raw/ux--nngroup-journeys-vs-flows.md] |
| IA and screen map | Before any wireframe or prototype | Content inventory, grouping, controlled vocabulary, tiered hierarchy; navigation chosen from the IA | [raw/ux--nngroup-ia-vs-navigation.md] |

Rules distilled:

- One actor per journey map; separate maps for separate user types. [raw/ux--nngroup-journey-mapping-101.md]
- A journey is not an interaction log; a flow is where steps and system responses go. [raw/ux--nngroup-journey-mapping-101.md], [raw/ux--nngroup-journeys-vs-flows.md]
- IA first, navigation second; do not pick navigation patterns "based on looks alone". A first-pass IA is enough to start wireframes. [raw/ux--nngroup-ia-vs-navigation.md]
- Decision points, error branches and entry points in flows are this skill's own convention (Mermaid decision shapes), not an NN/g requirement. [raw/ux--nngroup-journeys-vs-flows.md] says flows follow the typical or ideal path; adding the failure branches is how this skill feeds the screen-state specs.

## 3. States, content and errors

| State | Requirement | Source |
|---|---|---|
| Empty | Say whether loading, errored or truly empty; teach what the area is for; offer a direct pathway (Create, Learn more, demo data). Never show "no records" before data finishes loading | [raw/ux--nngroup-empty-states.md] |
| Loading | Visible system status with prompt feedback | [raw/ux--nngroup-ten-heuristics.md], [raw/ux--nngroup-empty-states.md] |
| Error | Message near its source; redundant cues beyond color; plain, precise, constructive, nonjudgmental; preserve input; suggest a fix; no humor | [raw/ux--nngroup-error-messages.md] |
| Success | Visible status and a clear next step (heuristic 1 and 3) | [raw/ux--nngroup-ten-heuristics.md] |

The ten heuristics give the content review checklist: status, real-world language, control and undo, consistency, error prevention, recognition over recall, efficiency, minimalism, error recovery, help. [raw/ux--nngroup-ten-heuristics.md]

## 4. Critique and visual quality

- A critique judges a design against agreed objectives and user needs. Without them feedback is subjective. [raw/ux--nngroup-design-critiques.md]
- Reframe directives into questions about the user's main task. [raw/ux--nngroup-design-critiques.md]
- Hierarchy tools: contrast in value and saturation, scale (no more than three sizes, at most two large elements), grouping by proximity and white space; containers sparingly. "If everything is contrasted, then nothing stands out." [raw/ux--nngroup-visual-hierarchy.md]
- Squint or blur test at roughly 5, 10 and 20 px reveals unintended dominance. [raw/ux--nngroup-visual-hierarchy.md]
- Impeccable's detector encodes anti-slop and quality rules (30 slop rules such as gradient text, hero eyebrow chip, cream palette, nested cards, em-dash overuse; 29 quality rules such as low contrast, line length, tight leading, tiny text). `npx impeccable detect <target>` exits 0 clean, 2 on findings, 1 on failure; it scans static HTML files. (repo: `impeccable-stinger/guides/06-detector-gate.md`)
- Impeccable requires bounded passes: one batched inspection, one fix batch, at most one confirmation, then hand to the user; never self-grade as final. (repo: `impeccable-stinger/SKILL.md`)

The seven rubric dimensions (hierarchy, spacing rhythm, typography, color and contrast, motion restraint, states completeness, anti-slop) were set by the locked topic. Their anchors are synthesized from the sources above; the 0 to 4 scale mirrors Impeccable's audit scale (repo: `impeccable-stinger/SKILL.md`, Phase 3). There is no external standard rubric with these exact dimensions; say so if asked.

## 5. Prototype fidelity

- Fidelity has three independent dimensions: interactivity, visuals, content. [raw/ux--nngroup-prototype-fidelity.md]
- Low fidelity is cheap and signals unfinished work; high fidelity suits workflow and visual tests but invites attachment and premature launch decisions. [raw/ux--nngroup-prototype-fidelity.md]
- Therefore this skill locks direction (owner approval) before building high-fidelity prototypes, and labels every prototype "prototype, not production". [raw/ux--nngroup-prototype-fidelity.md]
- Pilot every prototype before showing it. [raw/ux--nngroup-prototype-fidelity.md]

## 6. Accessibility baseline (WCAG 2.2 AA)

| SC | Level | Design-time requirement | Source |
|---|---|---|---|
| 1.4.3 Contrast (Minimum) | AA | 4.5:1 body text, 3:1 large text | [raw/a11y--w3c-wcag22-recommendation.md] |
| 1.4.11 Non-text Contrast | AA | 3:1 for component boundaries, states, required graphics | [raw/a11y--w3c-wcag22-recommendation.md] |
| 1.4.10 Reflow | AA | Works at 320 CSS px wide without two-dimensional scroll | [raw/a11y--w3c-wcag22-recommendation.md] |
| 2.4.7 Focus Visible | AA | Visible keyboard focus | [raw/a11y--w3c-wcag22-recommendation.md] |
| 2.4.11 Focus Not Obscured (Minimum) | AA, new | Sticky headers and overlays never fully hide focus | [raw/a11y--w3c-wai-new-in-22.md] |
| 2.5.7 Dragging Movements | AA, new | Single-pointer alternative for every drag | [raw/a11y--w3c-wai-new-in-22.md] |
| 2.5.8 Target Size (Minimum) | AA, new | 24 by 24 CSS px targets or a listed exception | [raw/a11y--w3c-wai-new-in-22.md] |
| 3.2.6 Consistent Help | A, new | Help in the same relative order across screens | [raw/a11y--w3c-wai-new-in-22.md] |
| 3.3.7 Redundant Entry | A, new | Do not re-ask for data already entered in the flow | [raw/a11y--w3c-wai-new-in-22.md] |
| 3.3.8 Accessible Authentication (Minimum) | AA, new | No cognitive test at sign-in without an alternative (allow paste and password managers) | [raw/a11y--w3c-wai-new-in-22.md] |
| 1.3.1 Info and Relationships | A | Structure shown visually is also in markup or text | [raw/a11y--w3c-wcag22-quickref.md] |
| 1.4.1 Use of Color | A | Color is never the only signal | [raw/a11y--w3c-wcag22-quickref.md] |
| 2.4.6 Headings and Labels | AA | Headings and labels describe topic or purpose | [raw/a11y--w3c-wcag22-quickref.md] |
| 4.1.2 Name, Role, Value | A | Controls expose name, role, state to assistive technology | [raw/a11y--w3c-wcag22-quickref.md] |
| 4.1.3 Status Messages | AA | Status announced without moving focus (live regions) | [raw/a11y--w3c-wcag22-quickref.md] |
| 2.3.3 Animation from Interactions | AAA | Interaction motion can be turned off; this skill adopts it as a house rule via reduced motion | [raw/a11y--w3c-wcag22-quickref.md] |
| 4.1.1 Parsing | removed | Not part of 2.2 | [raw/a11y--w3c-wcag22-recommendation.md] |

Reduced motion: honor `prefers-reduced-motion: reduce` by removing or replacing scale and pan motion, for example with opacity. [raw/css--mdn-prefers-reduced-motion.md] A design-time baseline does not establish conformance; conformance needs testing of the built product (consistent with `impeccable-stinger` motion guidance, repo).

## 7. Tokens and DESIGN.md

| Format | Shape | Status | Source |
|---|---|---|---|
| DTCG Format Module 2025.10 | JSON, `.tokens.json`, `$value`, `$type`, groups, `{group.token}` aliases, composite types | Stable community group report, 2025-10-28 | [raw/tokens--dtcg-format-2025-10.md] |
| DESIGN.md (Google Labs) | YAML front matter tokens (colors, typography, rounded, spacing, components) plus ordered `##` prose sections | Draft, version alpha, Apache-2.0 | [raw/tokens--google-design-md-repo.md], [raw/tokens--google-stitch-design-md-blog.md] |

- DESIGN.md prose sections, when present, must follow: Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts. Duplicate headings reject the file. [raw/tokens--google-design-md-repo.md]
- `npx @google/design.md lint DESIGN.md` validates (exit 1 on errors; warns under 4.5:1 contrast); `export --format dtcg` or `css-tailwind` converts. [raw/tokens--google-design-md-repo.md]
- Impeccable's `DESIGN.md` uses this Stitch format and is written by `/impeccable document`, with `.impeccable/design.json` as a sidecar not to be hand-edited. (repo: `impeccable-stinger/guides/01-context-contract.md`) So this skill drafts DESIGN.md proposals and lets the Impeccable owner or the human owner promote them.
- webapp-capture already emits candidate tokens in DTCG 2025.10 shape for live apps. (repo: `webapp-capture-stinger/references/prompts/claude-design-handoff.md`)

## 8. Diagrams

- Mermaid flowcharts: `flowchart TD` or `LR`; decision nodes via `diam` shape or `{}`; `%%` comments on their own line; do not use lowercase `end` as a label. [raw/diagram--mermaid-flowchart.md]
- Every diagram gets `accTitle:` and `accDescr:` immediately after the declaration; they render as SVG title and desc with aria attributes. [raw/diagram--mermaid-accessibility.md]

## 9. Light and dark in single-file prototypes

- Set `color-scheme: light dark` on `:root`; then `light-dark(a, b)` resolves per scheme without media blocks. Baseline 2024. [raw/css--mdn-light-dark.md]
- `color-scheme` can be forced on a subtree, which is how a manual theme toggle overrides the OS preference. [raw/css--mdn-light-dark.md]

## 10. Known gaps and conflicts

- Claude Design export internals are undocumented (section 1.3). Conflict: launch article lists "a saved folder" and "internal URL" exports, the current help article lists .zip and partner destinations; prefer the current help article. [raw/claude-design--anthropic-launch-announcement.md], [raw/claude-design--support-get-started.md]
- `/design-sync` scope conflict: help article lists four import sources (repo, design files, raw uploads, local codebase); secondary coverage says the command itself targets React design systems. Read as: the four sources are Claude Design import paths, and `/design-sync` is the local-codebase path that works best for React. [raw/claude-design--support-get-started.md], [raw/claude-design--aicatchup-design-sync.md]
- Several UX method sources predate the window. They were kept because they remain the primary references and several were reviewed by their publisher inside the window (journey mapping 2026-07-15, journeys vs flows 2026-08-27).
- No primary source defines a numeric "good enough" threshold for a design critique. The pass bar in this skill is a stated house decision, not research.
