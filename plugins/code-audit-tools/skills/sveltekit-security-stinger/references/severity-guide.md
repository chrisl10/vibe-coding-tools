# Severity and confidence guide (contract 1.0, sections 5 and 7)

The contract's scale is fixed: `critical`, `high`, `medium`, `low`, `info`. This page says how SvelteKit findings land on it. Per-check guidance lives in [check-catalog.md](check-catalog.md); when the two disagree, the stricter one wins.

## Confidence first

| Confidence | When to use it for SvelteKit findings |
| --- | --- |
| `confirmed` | The path is traced end to end: for example the action is reachable with a POST to `?/name`, nothing in `handle` stops it, and the body writes without a check. Or a version advisory whose precondition you read in code and whose input is attacker-reachable. |
| `likely` | Pattern match plus a manual read of the file and its callers, with one unverifiable link (for example the data is "probably" user-controlled because it comes from a CMS you cannot see). Version findings where the scanner found the precondition signal. |
| `possible` | Pattern match only. Severity must be `medium` or lower (contract rule 5.3). Version roll-ups from the scanner land here. |

If you cannot show evidence, it is not a finding: write it under "Not confirmed" in the notes file (rule 5.1).

## Severity anchors

| Severity | SvelteKit examples |
| --- | --- |
| `critical` | Anonymous visitor reads or changes other users' data through an endpoint, action, or remote function (SVK-E1 to E3, E5); a live secret key in the client bundle via `PUBLIC_` or `VITE_` (SVK-B3); identity taken from an unverified token so anyone can become anyone (SVK-H3); stored XSS that any visitor can plant and admins view (SVK-X1). |
| `high` | Signed-in user reaches another user's data or admin actions (missing per-action check, IDOR, path guard that remote functions bypass); SSRF from a server fetch (SVK-H4); server load returning password hashes or tokens (SVK-B1); shared module state leaking between users (SVK-B5); `trustedOrigins: ['*']` with cookie-authenticated actions (SVK-E7); a version advisory with its precondition present and rated high. |
| `medium` | A weakness that needs a second condition: GET with side effects behind `SameSite=Lax` cookies; open redirect (SVK-H7); unvalidated remote arguments with no proven sink (SVK-E4); layout-only authorization with every child currently checked (structural, SVK-H1); service worker caching authenticated responses (SVK-C5); session cookie readable by script (SVK-X6); version roll-ups. |
| `low` | Defense in depth: missing or weak CSP alone (SVK-X5); error messages that reveal internals but no secrets (SVK-H6); missing `secure` behind HTTPS-only hosting. |
| `info` | Context: current framework versions, `dangerZone` dead config in v2, `paths.relative` notes, the list of trusted origins, the remote-function inventory. |

## Adjusters

- Raise one level when the same app also has a confirmed XSS (cookie and storage findings become easier to exploit) or when the affected data is regulated (health, payment, government ids).
- Lower one level when a platform control you have read in the repository mitigates it (for example a documented WAF rule or a proxy that strips forwarded headers), and say so in `verified_by`.
- Never raise above the advisory's reviewed severity for a version-only finding.
- Never set `confirmed` on a version finding unless you traced attacker input to the vulnerable feature.

## Verdict for this Drone's metrics file

Use contract section 8 unchanged: `critical` if any critical at `confirmed` or `likely`; `at-risk` if any high; `moderate` if any medium; otherwise `healthy`. The orchestrator's `merge_security.py` recomputes the merged verdict from all security Drones.

Sources: raw/owasp--top10-2025-categories-and-cwes.md, raw/advisory--github-advisory-db-svelte-ecosystem.md, raw/kit-docs--form-actions-and-routing.md, raw/kit-source--csrf-implementation-and-prs.md.
