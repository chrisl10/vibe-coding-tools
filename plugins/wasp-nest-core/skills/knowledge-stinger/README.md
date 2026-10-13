# knowledge-stinger

Companion skill to `library-stinger` for authoring **narrative knowledge documentation** - the technically deep, human-readable domain docs under `library/knowledge/private/<domain>/`.

## Purpose

`library-stinger` + `library-wasp-drone` own PRDs, IRDs, and the documentation lifecycle.  
`knowledge-stinger` + `knowledge-wasp-drone` own the knowledge/ domain - everything from system overviews to SQL schema references to coding standards.

## Directory map

```
knowledge-stinger/
  SKILL.md                          ← skill entry point (read this first)
  README.md                         ← this file
  guides/
    01-domain-taxonomy.md           <- how to choose domains for the repository being documented
    02-document-format.md           <- exact document format spec with annotated examples
    03-analysis-workflow.md         <- step-by-step workflow for building a full knowledge base
  templates/
    knowledge-doc-template.md       ← blank template (copy this to start a new doc)
  examples/
    example-system-overview.md      ← target quality example (architecture domain)
    example-auth-architecture.md    ← target quality example (auth domain with sequence diagram)
```

## Quick reference

| I want to... | Read this |
|---|---|
| Understand what goes in each domain folder | `guides/01-domain-taxonomy.md` |
| See the exact format every doc must follow | `guides/02-document-format.md` |
| Build a full knowledge base from scratch | `guides/03-analysis-workflow.md` |
| Turn supplied local meeting notes into decision and action drafts | [Guide 05](guides/05-turn-meeting-sources-into-decision-drafts.md), [worksheet](references/templates/meeting-decision-action-drafts.md), [synthetic receipts](references/examples/meeting-decisions/worked-drafts.md) |
| Start a new doc | Copy `templates/knowledge-doc-template.md` |
| See a target quality example | `examples/example-system-overview.md` |

## Relationship to library-stinger

| Artifact type | Skill | Agent |
|---|---|---|
| PRDs | `library-stinger` | `library-wasp-drone` |
| IRDs | `library-stinger` | `library-wasp-drone` |
| Knowledge docs | `knowledge-stinger` | `knowledge-wasp-drone` |
| QA reports | `quality-stinger` | `quality-wasp-drone` |
| ADRs | `adr-writing-stinger` | `adr-writing-wasp-drone` |

## Source and current plugin owner

Knowledge and Library stay in required Core. Source authoring uses src/skills and src/agents; installed Core contains the generated plugin/home carriers. The root plugin-catalog.json maps optional specialists and their prerequisites.

The six-host Deep Lake material in the guides/examples is a worked reference case, not a claim that The Wasp Nest packaging repository implements those tables, authentication flows or memory services. Read the target repository's decisions, requirements and actual code before applying the method.

Use optional Documentation Tools for KB Refresh or audience packets. Full KB Refresh additionally needs Code Audit; plain knowledge authorship remains in Core.


## Source-preserving novice explanation

Read guide 04 for a compact source-linked beginner tour; its template and actual-build/missing-implementation examples preserve actor, status and runtime evidence limits.

## Diagrams that preserve source behavior

Use [guide 06](guides/06-preserve-behavior-in-diagrams.md), the [edge worksheet](references/templates/source-grounded-diagram.md) and [three completed teaching journeys](references/examples/diagram-authority/worked-cases.md). Record caller, authorization, returns, queue acceptance versus completion, actual transaction/external boundaries and unknowns. Diagram syntax does not establish runtime, authority or deployment.
