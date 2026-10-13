# Analysis Workflow - From Zero to Full Knowledge Base

Build a knowledge base from the target repository's real decisions, requirements and implementation. Read relevant ADRs/PRDs when they exist, map actual domains, and author in dependency order. The six-host Deep Lake material below is a worked example, not a required stack, table count or folder layout for every repository.

---

## Step 1: Survey the source material

### Read the target repository's decisions

List the actual ADRs and note their domains. If formal ADRs are absent, cite owner-confirmed decisions or code evidence and state the decision gap; do not fabricate records. For the preserved memory-system example, a mapping could be:

```
system-overview            -> architecture/, integrations/
session-lifecycle          -> architecture/, ai/
desktop-harness-overview   -> integrations/, architecture/
```

As new ADRs land (e.g. a storage-substrate decision -> data/, a device-flow decision -> auth/, an MCP-server decision -> plugins/), add a row. This mapping tells you which domain folders to create and what ADRs each doc should reference.

### Read relevant requirements and implementation detail

For each real PRD or IRD, extract the applicable facts below and compare them with source code. An intended feature is not evidence of deployed behavior; when requirements are absent, document what the code proves and disclose the missing specification.
- **SQL DDL / column lists:** Every table or `ColumnDef` block -> contributes to `data/deeplake-tables-schema.md`
- **API specs:** Tool / command signatures -> contribute to `standards/api-design-conventions.md` and domain docs
- **Technical Considerations sections:** Implementation details -> contribute to the relevant domain docs
- **Files Touched sections:** Real file paths -> used to cite source code in knowledge docs
- **Architecture notes:** System-level observations -> contribute to `architecture/` docs

**Do NOT copy PRD content verbatim.** PRDs are specs ("what to build"). Knowledge docs are explanations ("how it works and why"). Transform spec language into narrative explanations.

---

## Step 2: Plan the domain structure

Create a planning table before writing any docs:

```
Domain           | Docs to create                          | Source material
-----------------|-----------------------------------------|----------------
architecture/    | system-overview, request-lifecycle,      | system-overview ADR,
                 | desktop-harness-overview                 | session-lifecycle ADR
ai/              | session-capture, hybrid-recall-pipeline, | session-lifecycle ADR + recall PRDs
                 | embeddings-daemon, skillify-pipeline     |
data/            | deeplake-tables-schema, schema-healing,  | src/deeplake-schema.ts + storage PRDs
                 | vfs-path-conventions                     |
integrations/    | six-harness-overview, adding-a-harness   | harness ADRs + per-harness PRDs
...
```

Confirm the domain list matches the ADRs and PRDs in this repo. Skip domains that aren't applicable (e.g., `frontend/` only if the repo ships the dashboard / graph-visualizer surfaces).

---

## Step 3: Author in dependency order

### Batch A first (sets the stage)

For a full knowledge-base build, write these docs first. A targeted diagram uses guide 06 and its source ledger without inventing a full Batch A:

1. `library/knowledge/private/overview.md` - the entry point doc
2. `library/knowledge/private/architecture/system-overview.md` - master diagram
3. `library/knowledge/private/architecture/request-lifecycle.md` - the target system's main end-to-end flow; use session-lifecycle.md only when sessions are the actual domain

These three docs force you to understand the system well enough to write everything else.

### Batches B-E can parallelize

After Batch A, the remaining domains are largely independent:

```
Batch B: ai/ + auth/ + data/
Batch C: integrations/ + plugins/
Batch D: frontend/ + collaboration/
Batch E: infrastructure/ + multi-tenant/ + security/ + standards/ + operations/
```

---

## Step 4: Writing each doc

### For narrative docs (architecture, AI, auth, security)

1. Open the relevant ADR(s). Understand the DECISION section.
2. Open the relevant PRD(s). Read the Technical Considerations section.
3. Write the doc opening with WHY (pulled from ADR's Context section), then WHAT (the component's role), then HOW (pulled from PRD's Technical Considerations).
4. Add a Mermaid diagram if the doc benefits from a visual.
5. Fill in the Related section.

### For schema documentation

1. Locate the actual schema declarations, migrations or authoritative contracts. Record the storage technology and the source paths you read.
2. Document every in-scope table, collection or key family completely. Use real columns/types/constraints and indexes; do not force a seven-table count or invent a Deep Lake schema file.
3. Explain actual writers, readers, tenancy and migration/version behavior above the schema reference. State any uncertainty that the inspected source cannot resolve.
4. For the preserved Deep Lake example only, data/deeplake-tables-schema.md collects the seven *_COLUMNS definitions from its real src/deeplake-schema.ts and explains SELECT-first additive healing.


### For pipeline documentation

1. Trace the target pipeline's actual entry points, dependencies, state changes and outputs. Cite the functions and paths that prove each step.
2. Explain why the pipeline exists and how its stages fit together; name the actual mechanism rather than importing another product's flow.
3. Add a diagram and one source-backed example when they clarify the mechanism.
4. In the preserved hybrid-recall example, src/shell/grep-core.ts contains searchDeeplakeTables, normalizeSessionContent and refineGrepMatches. Use those names only when the target repository actually contains that implementation.


### For standards docs

1. Read the target repository's actual language, formatter, package and build configuration. For a TypeScript project, inspect tsconfig.json, lint/format config and package.json; use its real package manager rather than inheriting the example's npm choice.
2. Look at any existing convention notes in the codebase.
3. Make explicit what was implicit - the conventions developers follow by habit.
4. Add examples from the actual codebase (cite file paths).

---

## Step 5: Cross-link verification

After all docs are written, verify cross-links:

1. Every doc's Related section: do all linked files exist?
2. Every ADR reference: does the cited ADR exist at the expected path?
3. `overview.md` reading guide: do all paths it mentions exist?
4. No doc is an island - every doc should link to at least 2 others.

Quick check command:
```bash
# List all docs in the knowledge base
find library/knowledge/private -name "*.md" | grep -v "ADR-" | sort

# Check for broken relative links (manual inspection of Related sections)
grep -r "\]\(\.\./" library/knowledge/private/ | grep -v "ADR-"
```

---

## Step 6: Quality check checklist

Before declaring the knowledge base complete:

- [ ] Every domain folder has at least one doc (no empty folders)
- [ ] `overview.md` exists at the top level and has a reading guide
- [ ] `architecture/system-overview.md` has a Mermaid architecture diagram
- [ ] The schema reference covers all actual in-scope data objects and cites their real definitions; the seven-table Deep Lake checklist applies only to that worked example
- [ ] Every doc has the standard header (Category, Version, Date, Status)
- [ ] Every doc has a Related section with at least 2 links
- [ ] No doc exceeds 500 lines without a good reason
- [ ] All Mermaid diagrams use standard formatting (no explicit colors, no click events)
- [ ] Security doc `trust-boundaries.md` has a trust boundary diagram
- [ ] Standards docs have concrete code examples (not just prose rules)

---

## Common Pitfalls

### Pitfall: Copying PRD content verbatim
PRDs are specs. Knowledge docs are explanations. Do not automatically rewrite "The system MUST do X" as "The system does X". Check the implementation first; keep intended requirements, inspected behavior and observed runtime separate. Explain verified implementation details in narrative prose and preserve missing or contradictory evidence. For diagrams use [guide 06](06-preserve-behavior-in-diagrams.md).

### Pitfall: Making one giant doc per domain
Split by coherent topic. `data/` should have separate files for the table schema, schema healing, and the VFS path conventions - not one 2000-line file.

### Pitfall: Skipping the overview.md
The overview is the map. Without it, someone arriving at the knowledge base cold doesn't know where to start. Write it after Batch A so you have a clear picture of the whole system.

### Pitfall: Diagrams with spaces in node IDs
`A[My Component]` is fine. `My Component --> Another Component` will break. Always use camelCase or underscores in Mermaid node IDs.

### Pitfall: Writing bullet soup instead of prose
If a section is 12 nested bullets with no connective tissue, rewrite as prose. Bullets are for true lists (tables, catalogs, checklists). For explanations, use paragraphs.

### Pitfall: Forgetting to update cross-references
When you add a new doc, add it to the Related section of its most related sibling. Knowledge bases rot when docs become islands.
