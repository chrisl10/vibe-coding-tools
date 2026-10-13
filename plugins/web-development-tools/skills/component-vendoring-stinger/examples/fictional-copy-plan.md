# Completed fictional copy plan, not executed

Product: Fictional Atlas internal web app. Existing stack: Svelte 5.40 / Tailwind 4, invented fixture inputs. Need: one consistent action button. Existing `AtlasAction` already satisfies semantics and tokens, so recommendation: reuse it. The inspected alternative is a shadcn-svelte button source-copy plan held for review; no copy is needed now. This demonstrates that O218 can end in reuse while O272 stays unexecuted.

| Field | Completed plan value |
|---|---|
| Alternative source | huntabyte/shadcn-svelte commit 493481fab94f68b8982949bc8a37eede786f2462 |
| Upstream file | docs/src/lib/registry/ui/button/button.svelte; actual hash in source-index entry shadcn-button-source |
| Proposed local path | src/lib/components/ui/action-button.svelte; DOES_NOT_EXIST |
| MIT evidence | archived exact root LICENSE; subset/file exceptions need reviewer confirmation |
| Source/dependency split | button wrapper could be copied; import closure and variant exports must be inventoried first; Bits UI is a separate normal dependency unless an approved plan says otherwise |
| Required notice destination | THIRD_PARTY_NOTICES/shadcn-svelte/LICENSE, proposed only; preserve complete upstream copyright and permission text |
| Modifications | planned token mapping to AtlasAction tokens; no content changes performed |
| Prerequisites | actual lockfile, source import closure, framework compatibility and asset list UNKNOWN |
| Rights review | Software Licensing/counsel pending; no distribution approval |
| Authorization | none to copy/install; approved activity only selection worksheet |
| Patch history | empty, no local fork |
| Update comparison | original pinned; candidate not selected; upstream/local diffs NOT_RUN |
| Maintainer | fictional Atlas UI maintainer; review after an accepted upstream/security/framework change |
| Acceptance proof | target build/browser/accessibility/license compatibility/native host NOT_RUN |

Synthetic [fixture manifest](fictional-provenance.json) exercises notice identity and hash drift without external code. It is independent of this actual-library research and cannot qualify an application.

A separate [filled synthetic lifecycle manifest](fictional-completed-manifest.json) provides a completed plan with exact fixture hashes, destinations, no dependencies, maintainer and comparison records. It grants no real copy authority and makes no MIT claim about its synthetic terms.
