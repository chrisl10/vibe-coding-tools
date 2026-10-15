# 02. Security routing

Load this guide for `basic`, `full`, and `mario`. It turns `intake.json.stacks` into the list of security Drones for W1.

References: [audit-contract.md](../references/audit-contract.md) section 2; [arming-lines.md](../references/arming-lines.md).

## Rules

1. **Always** dispatch `security-wasp-drone` for the generic pass: secrets, dependency advisories, OWASP Top 10 classes, and anything stack-agnostic. Its Stinger, `security-stinger`, is written for one specific stack, so the arming line tells it to apply only the parts that match this repository. `security-stinger` has no built-in report-only mode, so the arming line states the constraint as a direct instruction: report findings only, remediate nothing, skip its Ship Gate and commit steps, and write nothing outside `02-security/` (not the repository, not `library/`).
2. For each entry in `stacks`:

   | Stack id | Dispatch | Scope |
   | --- | --- | --- |
   | `nextjs` | `nextjs-security-wasp-drone` and `react-security-wasp-drone` | the stack's `paths`; the React Drone skips Next.js server surfaces |
   | `react` (no `nextjs` on the same paths) | `react-security-wasp-drone` | the stack's `paths` |
   | `svelte`, `sveltekit` | `sveltekit-security-wasp-drone` | the stack's `paths` |
   | any other id | `polyglot-security-wasp-drone`, once, with every other stack listed | those stacks' `paths` |

3. Dispatch one Drone per type, not per path: a monorepo with two Next.js apps gets one `nextjs-security-wasp-drone` with both paths.
4. Each Drone writes its own findings file to avoid write collisions: `02-security/findings-<source>.jsonl`, `02-security/metrics-<source>.json`, and `02-security/notes-<source>.md`. After W1, you (the orchestrator) merge them into `02-security/findings.jsonl` and one `02-security/metrics.json` with `python3 <this-skill>/scripts/merge_security.py <workspace>`, which sets the merged verdict with contract section 8. Keep the per-source files; the evidence index lists them.
5. If no framework Drone applies and `polyglot-security-wasp-drone` finds nothing it covers, the generic pass stands alone. Say so in `02-security/notes.md`.

## Why both Next.js and React Drones

Next.js apps are React apps. The Next.js Drone owns server boundaries (proxy and middleware, Server Actions, route handlers, caching, config). The React Drone owns client patterns (XSS sinks, client trust, bundle secrets). Running both on the same paths, with the overlap rule above, covers both halves without double counting; the brief's merge rule removes any duplicate that slips through.
