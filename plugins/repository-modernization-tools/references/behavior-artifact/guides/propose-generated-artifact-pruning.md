# Prepare an exact generated artifact removal proposal

Read the digest and [the worksheet](../references/behavior-artifact-worksheet.md). This procedure proposes candidates. It neither deletes files nor creates a cleanup engine.

1. Enumerate exact relative candidate paths, bytes and hashes under the assigned repository root. Reject symlinks that escape it and ambiguous path resolution. Directory names, extensions, age, mtime and a generated-file banner alone are insufficient ownership proof.
2. For each file, identify the producer command/version, source commit, configuration, lockfile and generated output manifest. Confirm who owns it and whether it contains handwritten edits, vendored code, licenses, notices, private evidence or irreplaceable inputs. Preserve these when any evidence is missing.
3. Identify every known consumer: build/deploy scripts, release packages, documentation, fixtures, runtime dynamic loads and external users. Text search provides candidates, not proof of no use. Mark unknown consumers explicitly.
4. Separate dependency caches, build outputs, release artifacts and investigation evidence. GitHub's cache/artifact distinction concerns different uses, not a blanket local deletion rule. A generated artifact with no reproducible producer remains PRESERVE_UNKNOWN.
5. Demonstrate regeneration in an authorized isolated location with pinned inputs and existing tools. Record bytes or justified semantic comparisons, commands, costs and unavailable external resources. No network, dependency installation, paid regeneration or private/provider access follows implicitly from the proposal.
6. Record applicable retention authority, legal/evidence holds when actually known, backup location/hash and an observed restore exercise. Do not assert backup success because a path exists. Unknown retention or untested recovery is a reason to preserve. Never upload private evidence to obtain a backup.
7. Produce the exact reviewable file list and one decision per row: PRESERVE, PRESERVE_UNKNOWN or PROPOSE_REMOVAL. State expected space reclaimed without double counting shared bytes. Send the proposal to the existing refactor-safely command/the owner. Obtain the owner's explicit approval naming this task and exact list before deletion; any byte/path/consumer change invalidates that proposal and approval scope.
8. Before approved execution, the implementation owner rechecks hashes and ownership and follows the existing Security, Quality and parent Repository Health process. Remote workflow runs are a separate action: deleting a run removes its artifacts and requires separate exact authorization.

Grounding: GitHub artifacts, retention and digest validation. Permission controls derive from the owner's active operating rules, not inferred vendor approval.
