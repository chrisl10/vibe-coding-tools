# 08: Hand off to Claude Design (outbound)

Goal: give the owner one brief and a set of files that let Claude Design explore or refine the design without losing the decisions already made.

Grounding: [Claude Design help article](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-design-stinger/references/research/raw/claude-design--support-get-started.md), [launch announcement](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-design-stinger/references/research/raw/claude-design--anthropic-launch-announcement.md), [design-sync coverage](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/product-studio/skills/product-design-stinger/references/research/raw/claude-design--aicatchup-design-sync.md), webapp-capture handoff conventions (repo: `packs/browser-and-app-testing-tools/skills/webapp-capture-stinger/references/prompts/claude-design-handoff.md`, `guides/02-component-library-capture.md` stage 8). Distilled: [section 1](../references/research/distilled-product-design.md).

## What is confirmed about Claude Design (read before promising anything)

- It accepts prompts, images, screenshots, wireframes, documents and decks, and a linked code repository. A strong prompt states goal, layout, content and audience.
- A project inherits the organization design system. Design systems import from a GitHub repo, design files, raw uploads, or a local codebase through `/design-sync` in Claude Code (reported to work best for React design systems).
- Exports: .zip, PDF, PPTX, standalone HTML, Google Slides, partner destinations, and "Hand off to Claude Code".
- Not documented: what the .zip or the handoff bundle contains. Do not tell the owner it will return tokens or specs in any particular format.

## Choose the path

| Situation | Path |
|---|---|
| No app yet, package exists | Brief from this package only |
| An app already runs | First run webapp-capture-stinger's capture and handoff zip (its stage 8). Attach that zip AND this brief: the capture carries measured components and candidate DTCG tokens, this brief carries product intent, flows and states the capture cannot measure |
| The repo has a React design system and the owner uses Claude Code | Suggest the owner run `/design-sync` (after `/design-login`) so Claude Design uses the real components. This is the owner's action in their own account; do not run it for them |

## Procedure

1. Copy [claude-design-brief.md](../references/templates/claude-design-brief.md) to `design/claude-design/brief.md`. Fill it from the package: product, actor, screens in scope, approved direction, constraints.
2. List the attachments. Prefer the package files themselves over summaries; Claude Design reads documents.
3. Keep the prompt short and literal. It tells Claude Design to read every attachment, follow the specs' reading order and states, use the vocabulary, mark invented copy as a proposal, meet the accessibility floor, and list every deviation.
4. Ask for the return formats in priority order: standalone HTML, the .zip, screenshots or PDF of every artboard in both themes, any token text Claude Design shows.
5. Give the owner the brief path and the attachment list. The owner uploads and sends it; this skill never signs in to Claude Design or uses the owner's account.
6. Record in the README provenance index: brief version, date, attachments sent.

## When the owner hands off straight to Claude Code

"Hand off to Claude Code" ("Send to local coding agent" or "Send to Claude Code Web") makes Claude Code implement code. Practitioners report it may point Claude Code at a `claude_design` MCP endpoint and may need `/mcp` OAuth to complete. That path does not update this package. Afterwards, run guide 09 on whatever HTML or screenshots the owner keeps, so the specs stay the source of truth, and hand implementation review to `impeccable-stinger`.
