# Semantic qualification scenarios

| Trigger | Required behavior |
|---|---|
| missing Code Audit owner | Stop foundation output and identify owner; continue independently available health view. |
| baseline-only request | Generate findings and proposed batches; no repair writes. |
| dirty file owned by another worker | Record exclusion and do not overwrite it. |
| remote settings inaccessible | Report unknown with exact unavailable check, not a configured state. |

These scenarios qualify procedure semantics only. They do not claim live harness execution or application behavior.
