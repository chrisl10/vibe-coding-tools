# Definition of Done template

> Copy to: `library/knowledge/private/standards/definition-of-done.md`
> Replace every `<placeholder>`. Delete these quote lines when done.
> Remove an item only with the owner's written reason in the revision history. Never remove the five core items.
> Guide: [../../guides/05-set-definition-of-done.md](../../guides/05-set-definition-of-done.md)

---

# Definition of Done: <product name>

> **Status:** Draft | Approved
> **Revision:** <n>
> **Approved by:** <owner name> on <YYYY-MM-DD> | Not yet approved

## What this is

This is the minimum every PRD in this project must meet before it counts as done. Every PRD inherits it. A PRD may add stricter checks in its own checklist, but it may never skip an item here. Work that misses any item is not done: it does not exit its wave and does not move to `completed/`.

Acceptance criteria and this list are different things. Acceptance criteria say what one PRD must do. This list says how well every PRD must be finished.

## Project Definition of Done

A PRD is **done** only when every box is true:

### 1. Acceptance criteria verified separately
- [ ] Every acceptance criterion in the PRD's ID table is marked VERIFIED.
- [ ] The VERIFIED mark came from a separate pass (a reviewer or Drone that did not build it), with evidence linked.

### 2. Tests
- [ ] New behavior has automated tests that would fail if the behavior broke.
- [ ] The full existing test suite passes.
- [ ] <project-specific: type check, lint, build commands that must pass>

### 3. Security, then quality
- [ ] A security review ran first, and no finding of medium severity or higher is open.
- [ ] A quality review against the PRD ran after the security fixes, and no finding of medium severity or higher is open.
- [ ] Every shared boundary the PRD uses passes its provider and consumer checks against the pinned CTR revision.

### 4. Docs and knowledge updated
- [ ] Library knowledge docs that describe the changed behavior are updated.
- [ ] The PRD folder is moved to the right lifecycle folder, with its `qa/` evidence inside.
- [ ] <project-specific: user docs, API docs, changelog>

### 5. Owner approval
- [ ] The owner reviewed the evidence and approved the PRD as done.

### Project-specific additions
- [ ] <for example: works on the smallest supported phone width>
- [ ] <for example: no new accessibility violations in the automated scan>

## PRD-level checklist

Copy this block into each PRD (Library places it). Fill the extra lines from that PRD's risks.

```markdown
## Definition of Done checklist

Inherits: [Project Definition of Done](<relative link>) revision <n>

- [ ] Project Definition of Done items 1 to 5 all true
- [ ] PRD-specific: <extra check from this PRD's risk>
- [ ] PRD-specific: <extra check>
```

## Revision history

| Revision | Date | Change and reason | Approved by |
|---|---|---|---|
| 1 | <YYYY-MM-DD> | First version | <owner> |
