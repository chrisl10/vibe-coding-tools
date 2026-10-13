# Worked freshness receipts
All scenarios are synthetic teaching records created October 7, 2026. Revisions A, B and C are content-addressed fixture directories, not real Git commits or deployed products. Exact source quotes, line references and hashes live in [receipts.json](receipts.json).

| Row | What the source says | Review outcome |
|---|---|---|
| F1 | [A owner guard](fixtures/rev-a/route.py), lines 2-3 | keep after review even if page is old |
| F2 | [B definition](fixtures/rev-b/route.py), lines 2-3 admits editor | owner-only sentence contradicted |
| F3 | [C moved definition](fixtures/rev-c/access.py), lines 2-3 | locator changed, definition unchanged |
| F4 | A definition exists, no execution recorded | source presence does not prove production enforcement |
| F5 | [Proposal](fixtures/records/proposal.md), lines 3-4 remains Proposed | proposed cannot become shipped because date is recent |
| F6 | No execution receipt exists | missing proof and explicit `(unverified)` |
| F7 | [Native example](fixtures/records/native-format.md), lines 2-5 is dated fiction | no assertion about current hosts or installed apps |
| F8 | [Intended decision](fixtures/records/decision.md), lines 3-4 requires owner while B definition admits editor | unresolved contradiction, report both; decision remains read-only |
| F9 | [Consumer](fixtures/records/consumer.md), line 2 awaits review | incomplete budget coverage remains unchecked |

For F8 the definition alone does not establish end-to-end authorization; other callers could restrict access. The review reports the local definition conflict and missing wider context, without claiming an exploitable vulnerability. For F9 record the one remaining read in the resumed unit map. The preparation check only compares quotes/hashes/labels. It does not run fixture application code, certify claim truth or prove native compatibility.
