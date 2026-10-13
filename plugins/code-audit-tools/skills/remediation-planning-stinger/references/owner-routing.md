# Owner Drone routing

Route through `pest-controller-suit` (read its roster before naming a Drone). The table is a starting point; build_plan.py guesses from file extensions and the Drone confirms against the roster and the finding text. Name only Drones that exist in the roster.

| Work package is mostly | Owner Drone |
| --- | --- |
| `.svelte` and SvelteKit routes | `svelte-wasp-drone` (security aspects: `sveltekit-security-wasp-drone` for the re-audit) |
| `.tsx`, React components | `react-wasp-drone` |
| Next.js Server Actions, route handlers | `react-wasp-drone` for structure; re-audit with `nextjs-security-wasp-drone` |
| `.ts`, `.js` server and library code | `typescript-node-wasp-drone` |
| `.py` | `python-wasp-drone` |
| `.rs`, Cargo | `rust-wasp-drone` |
| `.go` | `go-wasp-drone` |
| Dockerfile, workflows, CI | `devops-wasp-drone` or `ci-release-wasp-drone` |
| Lockfiles, advisories | `dependency-audit-wasp-drone` |
| SQL, migrations, ORM schema | `db-wasp-drone` (Neon and Drizzle: `neon-drizzle-wasp-drone`) |
| Auth design flaws | `auth-wasp-drone`, then re-audit with `security-wasp-drone` |
| Repo hygiene (branch rules, templates) | `github-repo-health-wasp-drone` |
| Docs and knowledge gaps | `knowledge-wasp-drone`, `library-wasp-drone` |
| Shared boundary between two packages | `contract-writing-wasp-drone` |

Verification is always a re-run of the audit dimension's Drone (`code-foundation-wasp-drone`, `code-bloat-wasp-drone`, `security-wasp-drone` plus the framework Drone, `quality-wasp-drone`), done by someone other than the implementer.
