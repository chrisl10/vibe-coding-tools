# 01. Wave dispatch

Load this guide after intake. It defines which Drones run in which wave for each tier, and how to arm them.

References: [tier-matrix.md](../references/tier-matrix.md) for the wave table; [arming-lines.md](../references/arming-lines.md) for the exact dispatch text per Drone; [audit-contract.md](../references/audit-contract.md) section 2 for ownership.

## Waves

| Wave | Runs in tiers | Drones | Mode |
| --- | --- | --- | --- |
| W1 | all | `code-foundation-wasp-drone` | parallel with the rest of W1 |
| W1 | vibe, basic, full, mario | `code-bloat-wasp-drone` | parallel |
| W1 | basic, full, mario | `security-wasp-drone` (generic pass) plus framework Drones per [02-security-routing.md](02-security-routing.md) | parallel |
| W2 | full, mario | `quality-wasp-drone` | after W1, because it reads the security results (the Ship Gate order: security, then quality) |
| W3 | mario | `knowledge-wasp-drone`, then `remediation-planning-wasp-drone` | see [04-mario-tier.md](04-mario-tier.md) |
| W4 | all | `code-audit-brief-wasp-drone` | last, after verification |

## Steps

1. Build the W1 dispatch list for the tier. Look up each Drone's arming line in [arming-lines.md](../references/arming-lines.md) and fill in the workspace path, repo path, copy path, scope, and stack paths.
2. **Claude Code:** issue every W1 dispatch in a single turn so they run at the same time. Drones cannot spawn Drones, so you, the orchestrator, dispatch every one of them, including each framework security Drone.
   **Cursor and Codex:** dispatch the same Drones one after another if concurrent subagents are not available; the output is the same.
   **Cowork:** use the `commands/audit-my-code.md` path; plugin agents are dispatchable there.
3. While W1 runs, do nothing that changes the workspace. When each Drone returns, check its folder per [05-verify-and-deliver.md](05-verify-and-deliver.md). A failed check gets one re-dispatch with the specific gap named. A second failure becomes a cap in the brief, not a silent pass.
4. After each wave, run `scripts/build_evidence_index.py <workspace>` so the index stays current. Run W2 (and W3 for `mario`) the same way, then W4.
5. Keep a one-line progress note to the user at each wave boundary: which Drones finished, what each found at a glance (verdict word and finding count), what runs next.

## Watchdog

Review each running Drone's real output (files written in its workspace folder) about every ten minutes. A Drone with no new files for twenty minutes is stalled: stop it, and re-dispatch its remaining scope split across two Drones of the same type (for example by path prefix), recording the split in `evidence-index.md`.
