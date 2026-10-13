# Acceptance cases: map-highlevel

## Invocation

Request: A supplied HighLevel export contains workflow graph and step fields.

Expected: Create traceable per-workflow outputs, preserve branches/asset joins, lint, render when tooling permits, and report source freshness plus unresolved jumps.

## Boundary case

The export lacks `_workflowSteps`. Stop extraction and name the missing field; do not invent account structure or a live workflow-read API.

## Evidence rule

Retain source dates and revision identity. Queued jobs, proposed actions, draft artifacts and unavailable tools never become claimed completed results.
