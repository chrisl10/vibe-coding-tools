# Verify the artifacts and hand off

Check source preservation when organization changed, required PRD sections and lifecycle placement, every real local Markdown destination, exact CTR metadata/revision pins, schema field coverage, source hashes, dependency graph/capacity and exclusive ownership. Run the installed core contract validator for target contract/PRD changes. Read its result: a structurally valid Draft set still blocks accepted implementation readiness.

For a structured wave plan, run `scripts/validate_handoff.py` against the JSON handoff. It checks syntax, graph, revisions, capacity and leases. It does not inspect an actual source commit, qualify a harness, confirm human approval, execute SQL or test provider behavior. A valid preparation plan may contain Draft contracts and blocked future waves. Do not change status to Accepted merely to make a checker green.

If preparation changed tracked development/baseline material, run Security first, resolve Medium or higher findings and have them re-evaluated, then run Quality against the same candidate. Relevant Quality repairs return through affected Security checks. The coordinator performs repository-health review last, with the user's CI preference and unavailable remote data stated. Produce reports in the target Library's appropriate report folders. Reviews check the actual artifacts, not just a worker's claimed success.

Describe what exists now, what was only specified, what is unqualified, and the exact remaining owner decisions. Include a coordinator starter and bounded worker template. Keep provider setup, paid smoke, deployment and implementation actions behind their applicable authorization. Actual runtime claims require the runtime result; application estimates remain estimates until measured.

Before any authorized commit, recheck changed path scope, reviewed content identity and ownership. Stage only task-owned files. An approval to commit another repo does not authorize committing this one. Do not push, publish or install the plugin just because the pack built successfully.

Deliver Status, Delivered, Verified, Not done, Questions for the controlling user, and Out of scope, noticed only. Link saved artifacts and report exact failures with secrets removed. Stop after the preparation handoff unless the user explicitly extends scope.

Grounding: source workflow (source archive, summarized in the distillation); installed Security/Quality/repository-health methods govern their detailed evidence formats.
