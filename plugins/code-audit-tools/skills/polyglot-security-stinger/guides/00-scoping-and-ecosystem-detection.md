# 00 Scoping and ecosystem detection

Run this guide first, every time. It fixes what this Drone audits, what it leaves to other Drones, and where its output goes.

Loads: [../references/cross-cutting/tool-commands.md](../references/cross-cutting/tool-commands.md), [../references/cross-cutting/manifest-to-stack.md](../references/cross-cutting/manifest-to-stack.md), `scripts/detect_ecosystems.py`.

## Steps

1. **Read the contract and the arming line.** Read `audit-my-code-stinger/references/audit-contract.md` (sections 3 to 8). From the arming line take: workspace, audited repo path, throwaway copy path, include and exclude scope, the stacks JSON, and the audit paths for this Drone.
2. **Never write to the audited repository.** All reads of the repo are read-only; all tool runs happen in `<workspace>/.scratch/repo-copy/` (a `git archive` copy). History scans use a separate bare clone in `<workspace>/.scratch/history.git` (see tool-commands.md section 2).
3. **Set up** the variables and the `rgs` helper from tool-commands.md section 2. Create `02-security/raw/polyglot/`.
4. **Confirm the stacks.** Run the detector on the copy and save it:
   `python3 "$SKILL_DIR/scripts/detect_ecosystems.py" "$COPY" > "$RAW/detect.json"`
   Compare its `stacks` with `intake.json.stacks`. If they differ (for example the orchestrator missed a Go service in `tools/`), audit what the arming line assigned, and list the extra stacks in notes under "Scope differences" so the orchestrator can dispatch them. Do not silently expand scope into paths another Drone owns.
5. **Build the scope table** in `notes-polyglot-security-wasp-drone.md`:

   | Stack id | Paths | Version | Frameworks (from `details`) | Guide |
   | --- | --- | --- | --- | --- |
   | node-server | services/api | 22 | express 5.1.0 | 01 |

   Map each id to its guide: node-server 01, python 02, go 03, rust 04, ruby 05, php 06, java-kotlin 07, dotnet 08, other: cross-cutting guides only (09 to 13) plus a manual read for the obvious injection classes in [../references/cross-cutting/ai-failure-patterns.md](../references/cross-cutting/ai-failure-patterns.md).
6. **Mark what is not yours.** Paths under `nextjs`, `react`, `svelte`, or `sveltekit` ids belong to their framework Drones; skip them except where a `node-server` path overlaps (for example a custom Express server inside a Next.js app). The generic `security-wasp-drone` also scans secrets and dependencies repo-wide; you still run them for your paths, and the renderer merges duplicates.
7. **Repository-wide surfaces.** CI workflows, Dockerfiles, compose files, and Terraform listed in `detect.json.infra` are in scope for guide 12 when they build or deploy any of your stacks. If the orchestrator dispatched several polyglot instances, the one whose arming line includes `.` or the infra paths owns guide 12; otherwise note it as a scope difference.
8. **Plan the run.** For each stack: ecosystem guide, then the cross-cutting guides in order 09 (secrets), 10 (dependencies), 11 (static analysis), 12 (CI and infra), 13 (AI patterns), and finish with 14 (writing findings). Budget time so every stack gets at least its checklist pass; record any stack you could not finish as a cap.
9. **Record the tools available** (`command -v rg go python3 pipx uvx npm cargo bundle composer dotnet docker trivy`) and network reachability (`curl -sI https://proxy.golang.org` with a short timeout) in notes. This decides which ladder rung each later guide starts at.

## Done when

- `raw/polyglot/detect.json` exists, the scope table is in notes, every assigned path maps to a guide, and paths you will not audit are listed with the owner.

## Sources

[raw/deps--osv-scanner-supported-lockfiles.md], [raw/tools--version-pins-2026-09-30.md], [raw/ci--trivy-teampcp-compromise-2026.md]
