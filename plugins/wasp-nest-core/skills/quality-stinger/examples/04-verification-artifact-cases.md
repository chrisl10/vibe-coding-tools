# Verification artifact cases

All ten cases are constructed teaching scenarios. None is an observed application test or release approval. Expected conclusions follow [the evidence procedure](../guides/08-verification-artifacts.md).

| Scenario | Expected reviewer conclusion |
|---|---|
| Same Git HEAD, edited untracked handler | Old HEAD-only result cannot pin the new handler; candidate is incomplete or STALE. |
| One file changed after Security, before QA | Halt dependent verdict; reconcile scope and run Security on the new candidate before QA. |
| CI wrapper exited 0, one required shard still queued | INCOMPLETE; submitted work is not completed evidence. |
| Suite exit 0 with 12 passes and 4 skips | Preserve counts; the four skipped requirements remain unproven unless other evidence covers them. |
| xfail case unexpectedly passes under non-strict policy | Preserve XPASS and policy; green suite is not proof of intended failure behavior. |
| Expected malformed-input refusal prints ERROR, fixture assertion passes | Negative assertion can PASS within its scope; quote expected and actual outcomes. |
| Tutorial contains a working-looking SQL example never executed | NOT_RUN for SQL behavior; documentation may pass structural review only. |
| Candidate pin matches, ZIP includes an older transformed file | Build alone cannot close packaging claim; distribution check FAIL. |
| Imported signed provenance verifies against a different ZIP digest | Does not authenticate the intended artifact; keep mismatch as failed verification. |
| Local author hashes a report and names it an attestation | Integrity record only; signature NOT_PRESENT and authorship self-authored. |
