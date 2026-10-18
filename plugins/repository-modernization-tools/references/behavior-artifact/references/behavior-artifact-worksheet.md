# Behavior and artifact evidence worksheet

Constructed template; no real application measurements.

## Characterization record

- Boundary/case, baseline commit and dirty hashes, candidate commit and dirty hashes:
- Runner/version, OS, lock hash, invocation, fixture hashes, environment names:
- Clock/randomness/IO substitutions and limits:
- OBSERVED_CURRENT outputs/errors/order/side effects, exit code and evidence hash:
- INTENDED_REQUIREMENT and approval/reference source:
- Normalization and reason; stable/unstable/unexecuted:
- Candidate difference and regression/authorized/unresolved classification:
- Consumer and provider versions; separate verification receipts:
- Coverage omitted, redaction controls, implementation owner:

## Artifact proposal row

| Exact path | Bytes/hash | Producer/source/lock/config | Consumer evidence/unknowns | Handwritten/vendor/notices/private evidence | Rebuild receipt | Retention authority | Backup and actual restore receipt | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Fill actual path | Actual values | Actual identities | Include dynamic/external use | Preserve if unresolved | Observed or NOT_RUN | Actual or UNKNOWN | Observed or NOT_RUN | PRESERVE / PRESERVE_UNKNOWN / PROPOSE_REMOVAL |

Approval: exact list digest, task, the owner's decision and scope. No deletion command is included. Recheck hashes before authorized execution.
