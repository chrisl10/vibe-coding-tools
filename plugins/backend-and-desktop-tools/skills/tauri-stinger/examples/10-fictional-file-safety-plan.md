# Fictional local file safety plan

CONSTRUCTED_DECISION, NOT_RUN. Product Paper Lantern, desktop Tauri candidate only. Paths are imaginary references. No files were imported, exported or deleted; no application or installer was launched.

Fictional owner approval A1 permits a single read of selected input S1, JSON schema 1, maximum 1 MiB and 1,000 records, with no upload. Rust issues token T1 bound to main window and verified source identity; parser creates a draft. Commit approval A2 permits only the previewed app records. These numbers are example product policy, not supported universal limits.

Fictional approval A3 permits export E1 to a selected new leaf with no overwrite. The Rust owner must qualify handle-relative ancestor checks and atomic no-replace publication on each actual target. Existing destination means deny and reselect; generic exists-then-rename is rejected. For a later overwrite request, A4 must bind the existing revision and verified backup B1; no real approval A4 exists in this example.

Fictional cleanup preview U1 contains app-private cache C1 with trusted creation provenance and excludes source S1, export E1, user document D1 and legacy unknown L1. An approved dry-run preview is not authority to execute deletion. Actual cleanup needs a separate explicit approval, target-native identity-safe removal and tested recovery; until then U1 is plan-only. Package installer ownership remains OPEN.

| Acceptance | Expected decision | Observation |
|---|---|---|
| S1 allowed regular bounded JSON | draft then exact commit approval | NOT_RUN |
| Renderer passes D1 instead of T1 | reject | NOT_RUN |
| E1 becomes symlink before publication | reject or safe qualified native operation | NOT_RUN |
| Destination already exists without A4 | preserve destination | NOT_RUN |
| Sync fails after draft write | preserve old destination, report failure | NOT_RUN |
| Crash after publication before parent-directory persistence | published durability-unconfirmed, reconcile | NOT_RUN |
| U1 encounters L1 or a link to D1 | retain and report | NOT_RUN |

Recovery: discard only identity-verified operation-owned draft before publication; reconcile publication after ambiguous outcome; retain prior backup until exact restore is authorized. No silent provider retry. Runtime/provider selection, Windows/macOS/Linux primitives and installer cleanup need their implementation owners. Use [the worksheet](../templates/file-safety-evidence.md) and [negative cases](11-file-safety-negative-cases.md).
