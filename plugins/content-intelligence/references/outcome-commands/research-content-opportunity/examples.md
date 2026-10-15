# Acceptance cases: research-content-opportunity

## Invocation

Request: Find a repository topic for today using a supplied duplicate ledger.

Expected: Verify a current spike, choose and vet one candidate, preserve exact receipts, and load the user's configured voice skill (from the preferences file) before voice-specific drafts; with none configured, label drafts as neutral voice.

## Boundary case

The chosen candidate fails its single-topic vetting gate. Produce no-post; do not deep-vet another candidate or write persistent memory without authorization.

## Evidence rule

Retain source dates and revision identity. Queued jobs, proposed actions, draft artifacts and unavailable tools never become claimed completed results.
