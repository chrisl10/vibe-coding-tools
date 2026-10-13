# Intake script

Ask these in one message, with defaults already filled in. The user can answer "defaults" to accept everything.

> I'm ready to run the **{tier label}** on **{repo name}** (`{branch}` at `{sha}`).
>
> 1. **Who is the brief for?** Default: {git user.name}.
> 2. **Scope.** Default: all tracked files, excluding {default excludes}. Any paths to add or leave out?
> 3. **Where should output go?** Default: `{parent}/{repo}-code-audit/{date}-{tier}/`, next to the repo. Nothing is written inside the repo{mario clause}.
> 4. **Run the repository's own code?** Some checks run this repository's test, lint, and typecheck commands, and the unused-code tool loads its config files. That executes code from the repository on this machine. Default: **no**. Choose **container** (recommended when Docker or Podman is available: only a copy is mounted, dependencies install with scripts off, and tests run with no network), **host** (only for code you trust: credentials are stripped from the environment, but it is not a sandbox), or **no** (those checks are reported as not run).
> {5. **Uncommitted changes.** Your working tree has uncommitted changes. Audit HEAD (default) or the working tree as it is now?}

Record answer 4 as `intake.json.execution` (contract section 4). Detect a container runtime first (`docker info` or `podman info`, read-only) so the question only offers `container` when one works.

`{mario clause}` for the Mario tier: ", except the `library/` documents you approve at the end".

## Default excludes

`node_modules/`, `vendor/`, `dist/`, `build/`, `out/`, `.next/`, `.svelte-kit/`, `coverage/`, `target/`, `**/*.min.js`, `**/*.d.ts`, `**/__generated__/**`, `**/generated/**`, lockfiles (for the bloat dimension only; security still reads them), test fixtures and snapshots (bloat only).

Excluding tests from bloat measurement matches how the reference WHIPT audit scoped duplication; security and quality still read tests.
