# Track freshness and missing proof

Use a claim receipt to decide what needs refresh. Start inside the owner's named file set and pinned revision. Use the existing inventory, unit map, grounding law and adversarial verification chain; this guide adds evidence fields, not a second pipeline. [Research digest](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/documentation-tools/skills/kb-refresh-stinger/references/research/documentation-freshness/distilled.md).

## Read the receipt before the date

A document modified yesterday can still describe a proposal as shipped. An older page can accurately describe unchanged behavior. File age, commits since review and a changed hash are triage signals. They do not by themselves prove semantic drift. Mark a page keep only after its relevant claims were re-opened and supported, update when a specific claim or citation needs correction, and write when the needed document is absent from the fenced inventory.

## Fill one row per material claim

Use the [receipt worksheet](../references/templates/documentation-freshness-receipts.md). Record document path and claim, claim type, exact source revision, path and lines, digest of the observed bytes, UTC observation date, verifier and support assessment. For dirty source use a content-addressed snapshot and record that it is not a committed revision. Never invent a commit SHA for a fixture.

A source claim says what the pinned code defines. A runtime claim needs an actual execution receipt matching code version, environment, host version and result. A proposal claim needs its proposal/status record and says what is intended. A successful check on another revision or host is historical evidence. A hash proves byte identity, not truth. Record branch movement separately and keep the original pin.

## Decide what changed

| Evidence condition | Receipt status | Documentation action |
|---|---|---|
| Re-opened source still supports claim | supported | keep, record review date |
| Source behavior changed and contradicts sentence | contradicted | update the sentence and re-verify |
| Same behavior at a different locator | moved | update locator after checking context and incoming consumers |
| Cited file or execution receipt unavailable | missing | label claim `(unverified)`, record exact gap |
| Runtime claim cites only code | wrong-proof-type | narrow to source claim or retain runtime `(unverified)` |
| Proposal text presented as shipped | wrong-status | restore proposed status and required proof |
| Two relevant authoritative records disagree | unresolved-contradiction | show both revisions and readings, request scoped resolution |
| Old native-format example used as current instructions | historical-only | date it; qualify current host separately before instructions change |
| Budget ended before checking claim | unchecked | retain unresolved row and explicit resume action |

Moved does not mean removed. Search only the authorized source set for the symbol or replacement path, reopen the candidate and check surrounding dependencies before relinking. A link that resolves can point to the wrong implementation. Retain conflicting evidence rather than choosing whichever source has the newest date. PRDs, ADRs, contracts and code changes outside the write fence stay read-only; report drift and suspects through the existing protocol.

## Bound verification and consumer review

Record the time allowance, claim count, reviewed count, unchecked count, actual command results and output paths. Within an approved sampling budget, select security-sensitive and public behavior claims first, then changed dependencies and incoming links. Call the result sampled, never fully verified. The standard full-refresh verifier still requires every citation; a budget stop leaves that unit incomplete. Do not infer checks from an agent's completion message.

Check named incoming consumers and indexes for moved links within scope. If another unit owns a consumer, send its owner a finding rather than editing it. For named consumers outside scope, record unreviewed consumers and the exact resume read. Do not silently broaden the crawl. If the entire document is inaccessible, record its inventory row as unread and request access; do not fabricate claim totals.

## Close with actual proof

Use existing structural validators and contracts where applicable, then the owner's security and quality gates. Separate structural PASS, reviewed claims, fixture exercises and actual native/runtime execution in the receipt. No structural validator certifies semantic accuracy. Keep SUSPECTS.md even when empty. A bounded freshness pass does not launch a fleet, publish, change installed availability or activate hooks.

See [worked receipts](../references/examples/documentation-freshness/worked-receipts.md) for changed, moved, missing, historical and contradictory cases.
