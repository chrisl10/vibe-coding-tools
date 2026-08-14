# Library Structure

The `library/` is a project memory system. It keeps stable facts, planned changes, reactive fixes, reports, and temporary notes from becoming one confusing pile.

## The four rooms

Imagine a school with four rooms:

| Folder | Room analogy | What belongs there |
|---|---|---|
| `knowledge/` | Library | Durable facts, guides, standards, ADRs, architecture |
| `requirements/` | Planning room | PRDs for intentional product work |
| `issues/` | Repair room | IRDs for bugs, incidents, and reactive corrections |
| `notes/` | Personal notebook | Temporary human scratch notes |

### Knowledge

`knowledge/public/` is safe for customers or the public. `knowledge/private/` contains internal engineering, operations, security, and business material. Private does not mean secrets belong in Git. Credentials still belong in a secret manager.

### Requirements

Each PRD moves through `backlog`, `in-work`, and `completed`. The folder moves; it is not copied. Reports that span several requirements belong in `requirements/reports/`.

### Issues

IRDs describe reactive work. They use the same lifecycle so a defect has a visible state and evidence.

### Notes

Notes are human-owned scratch space. Agents may read them when authorized but should not treat an unverified note as durable truth.

## Why lifecycle folders matter

The folder answers a simple question without opening the document: are we considering this, doing it, or finished? Completion still requires evidence inside the document.

## Example versus live library

[`learn/examples/library/`](../examples/library/) teaches the shape. It is not the active planning system for Vibe Coding Tools and should not receive new project knowledge. Run `get-started-stinger` in a consumer repository to create that repository's live `library/`.

The full standard is in the example at [`documentation-framework.md`](../examples/library/knowledge/private/standards/documentation-framework.md).
