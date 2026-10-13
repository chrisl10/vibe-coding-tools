# Worked security-design cases

All cases are synthetic design reviews, not runtime results or claims about a real repository. Facts derive from [the nine captured primary sources](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/src/skills/security-stinger/references/research/security-design/distillation.md). The judgments below are Wasp Nest derived policy. Expected outcomes are deliberately separate from actual results.

## O151: exported invoice threat model

Synthetic assets: tenant invoice amount and recipient; actors: A member, B member, export worker and privileged setup operator. Flow: browser request -> server membership -> invoice query -> durable export job -> object download. Boundary: browser-supplied organization ID and object key. Abuse: A guesses B's export key after a role revocation. Proposed control: authorized query plus actor-scoped export retrieval and membership recheck. Proposed evidence: own-tenant positive export, A-to-B denied download, revoked A denied existing link, independent check no foreign rows entered the export. Actual: NOT RUN; no endpoint, schema or exported file supplied. Source: OWASP threat/authorization captures.

## O154: correctly scoped query with leaking serializer

Synthetic query predicate selects tenant A; a joined profile serializer returns internal recovery metadata outside the permitted response schema. Review verdict: scoped SQL alone does not establish field confidentiality. Proposed control: explicit allowed fields per actor and nested relations, with error response and cache/search/export scope review. Expected: A receives only approved fields; B and anonymous receive no private fields; denied mutation has no effect. Actual: SOURCE REVIEW of this illustrative scenario only. For real RLS, owner/BYPASSRLS and policy snapshots must be tested by DB guide 12. Source: authorization and PostgreSQL captures.

## O156: valid signature followed by lost work

Synthetic route verifies raw bytes, inserts event ID, starts an in-memory callback, returns 200, then process terminates before projection. Authentication can pass while fulfillment is lost. Proposed invariant: success response means the verified event was durably accepted for recoverable processing or its authorized projection committed. Expected failure cases: durable insert unavailable -> no successful acceptance; two deliveries -> one business effect; crash after effect -> recovery does not repeat credit. Keep dedupe history; replay does not clear completed effects or bypass timestamp checks. Actual: NOT RUN; no SDK/database/runtime exists in this case. Source: Stripe contract; durable inbox/outbox policy derives from Payments owner.

## O157: production artifact and agent-context scope

Synthetic sentinel PRIVATE_SENTINEL_NOT_A_CREDENTIAL appears in a client-public environment assignment and a diagnostic exception context. Review scope: source assignment, actual production bundle, SSR output, source maps, log sink and sanitized agent context. Expected evidence records detector class/path/artifact digest only, not matched value. A clean source grep would leave published bundle/log scope unknown. Actual: SOURCE REVIEW of the text scenario; no build or sink checked. If a real credential were issued and exposed, owner-authorized revocation/rotation would be separate from source repair. Source: SvelteKit boundary plus OWASP logging/secrets captures.

## O164: unit green while tenant export is untested

Synthetic candidate unit tests validate string formatting, but the risk is B data in A's download and duplicate webhook credit. Proposed coverage maps each to actor-specific integration behavior and independent effects, pins final candidate hash and lists unavailable provider/database/build evidence. Expected table: formatting SYNTHETIC EXERCISE, tenant export NOT RUN, webhook duplicate NOT RUN. Aggregate verdict: those application controls remain unproven; no blanket green label. Actual: the expected table is a design artifact only. Source: OWASP threat/authorization and ASVS overview; no individual ASVS requirement number is asserted without its actual versioned text.
