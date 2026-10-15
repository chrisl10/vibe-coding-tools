# 00. Scoping and version check

Run this guide first, every time. It fixes what you audit, proves which framework versions are deployed, and produces the reading list for guides 01 to 05.

Loads: [../references/REFERENCE.md](../references/REFERENCE.md), [../references/advisory-table.md](../references/advisory-table.md), [../references/check-catalog.md](../references/check-catalog.md) (section V), [../references/severity-guide.md](../references/severity-guide.md).

## Steps

1. **Read the run inputs.** Open `<workspace>/intake.json`. Take the `svelte` or `sveltekit` entries in `stacks` and their `paths`; those are your scope. Note `scope.exclude`. If no Svelte stack is listed but you were dispatched anyway, scan the repository root and say so in notes.
2. **Never write in the audited repository.** All output goes to `<workspace>/02-security/`. Do not run `npm install`, `pnpm install`, builds, or dev servers in the repository. If a tool must write, use the throwaway copy the orchestrator names (`<workspace>/.scratch/repo-copy`).
3. **Classify each path.** For each stack path, read `package.json` and `svelte.config.*`:
   - SvelteKit app: `@sveltejs/kit` present and `src/routes/` exists. Run every guide.
   - Plain Svelte + Vite SPA: `svelte` without `@sveltejs/kit`. Skip guides 02, 03 and the adapter parts of 05; focus on 01 (client secrets via `VITE_`, hardcoded keys), 04 (XSS, storage), and the back end the SPA calls belongs to `polyglot-security-wasp-drone` or `security-wasp-drone`.
   - Svelte library or design system package: run 04 only.
   - Note the major versions: Svelte 3, 4 or 5; SvelteKit 1 or 2 (SvelteKit 3 is pre-release on 2026-09-30). Checks in this skill target Svelte 5 and SvelteKit 2; for Kit 1 apps also flag SVK-V1 for the two CSRF advisories fixed in 1.15.1 and 1.15.2.
4. **Check the advisory data is fresh.** `scripts/advisories.json` was generated on 2026-09-30. If today is more than 30 days later and network access is allowed, refresh it per the rules at the top of [advisory-table.md](../references/advisory-table.md) and record the refresh in notes. If you cannot refresh, add a coverage cap: "advisory data as of 2026-09-30".
5. **Run the scanner once per run:**

   ```bash
   python3 <skill>/scripts/sveltekit_audit_scan.py --repo <repo> --paths <stack paths> \
     --out-dir <workspace>/02-security/raw --id-start 1
   ```

   Keep its stdout summary for the notes. If it fails, fall back to the manual commands in the Versions section of [detection-patterns.md](../references/detection-patterns.md) and record the failure.
6. **Resolve versions from lockfiles only.** Read `sveltekit-inventory.json` `versions`. For anything in `versions_unresolved` (a `package.json` range with no lockfile entry), do not raise a version finding; write "version unresolved, lockfile missing" under Not confirmed and add a cap.
7. **Review each version finding** in `raw/sveltekit-version-findings.jsonl`:
   - For `likely` findings, open the source signal named in `evidence` and decide whether attacker input reaches the feature. Raise to `confirmed` only when traced; drop to the roll-up when the signal is a false positive (for example `{...props}` built only from constants).
   - For roll-ups (`possible`), keep them as they are. They tell the reader the version is behind and what upgrading clears.
   - Check SVK-V2 by hand: kit below 2.70.0 plus a deploy build with a non-production `NODE_ENV`.
   - Copy the reviewed findings into `02-security/findings-sveltekit-security-wasp-drone.jsonl`. Start your manual findings at `next_finding_id`.
8. **Record clean versions.** For each entry in `clean_core_versions`, write one `info` finding ("SvelteKit 2.70.3 has no published advisories as of 2026-09-30") or a single combined one. Contract section 7 lists this as the `info` example.
9. **Build the reading list.** From the inventory, list for guides 01 to 05: every `routes[]` entry with `needs_manual_authz_review`, every `hooks[]` file, every `remote_functions[]` entry, every `html_sinks[]` and `dom_sinks[]` entry, `svelte_config[]` flags, `env_public_names[]` with `looks_secret`, `cross_checks`, `signals`. Put the counts in `metrics-sveltekit-security-wasp-drone.json` measures (see guide 06).
10. **Set coverage.** `files_scanned` from the inventory; `skipped` lists excluded paths and `skipped_large_files`; `caps` lists every limit (advisory data date, unparsed `bun.lockb`, files over 1.5 MB, paths out of scope).

## Done when

The version findings are reviewed and copied, clean versions are recorded, the reading list exists, and coverage caps are written down.

## Sources

raw/advisory--github-advisory-db-svelte-ecosystem.md, raw/advisory--kit-repo-advisories.md, raw/advisory--svelte-repo-advisories.md, raw/advisory--devalue-repo-advisories.md, raw/kit-source--csrf-implementation-and-prs.md, raw/npm--current-versions-2026-09-30.md, raw/vite-docs--env-variables-prefix.md.
