# Detection patterns and code pairs

Patterns for the checks the Drone does by hand (the script already applies the first set). Use ripgrep with `--no-config` against the repo, or Grep. Sources: [research/raw/actions--secure-use.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-foundation-stinger/references/research/raw/actions--secure-use.md), [research/raw/scorecard--checks-reference.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-foundation-stinger/references/research/raw/scorecard--checks-reference.md), [research/raw/git--gitignore.md](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/packs/code-audit-tools/skills/code-foundation-stinger/references/research/raw/git--gitignore.md).

## Workflow files (`.github/workflows/*.yml`)

| Concern | Pattern (ERE) | Read for |
| --- | --- | --- |
| Unpinned action | `uses:\s*[^\s#]+@(?![0-9a-f]{40}\b)` (PCRE) | any non-local ref that is not a 40-hex SHA |
| Token default | `^permissions:` at column 0 | absent at top and absent on a job |
| Write-all | `permissions:\s*write-all` | always a finding |
| Privileged trigger | `pull_request_target\|workflow_run` | then look for a checkout of the pull request head |
| Head checkout | `ref:\s*\$\{\{\s*github\.(event\.pull_request\.head\|head_ref\|event\.workflow_run\.head)` | with the trigger above this is the "pwn request" shape |
| Script injection | `\$\{\{\s*github\.(event\.(issue\|pull_request\|comment\|review)\.[a-z_.]*(title\|body\|ref\|label)\|head_ref)` inside a `run:` block | not when it sits under `env:` |
| Swallowed failures | `continue-on-error:\s*true` and `\|\|\s*true` on a test or lint line | FND-CI-050 |
| Test gated off | `if:\s*false` or `if: github.event_name == 'push'` on the only test job | FND-CI-050 |

Vulnerable versus fixed:

```yaml
# vulnerable: untrusted title is pasted into the shell script
- run: echo "${{ github.event.pull_request.title }}"

# fixed: the value travels through an environment variable
- env:
    TITLE: ${{ github.event.pull_request.title }}
  run: echo "$TITLE"
```

```yaml
# vulnerable: tag can be moved
- uses: some-org/some-action@v1
# fixed: full SHA with a readable comment
- uses: some-org/some-action@0123456789abcdef0123456789abcdef01234567 # v1.2.3
```

(The SHA above is a placeholder shape, not a real commit.)

```yaml
# vulnerable: every job gets the repository default token scopes
name: CI
on: [push]
jobs: { ... }
# fixed
name: CI
on: [push]
permissions:
  contents: read
jobs: { ... }
```

## Secrets and env hygiene

| Concern | Command | Notes |
| --- | --- | --- |
| Tracked env files | `git ls-files -- '.env' '.env.*' '*.env'` | exclude names ending `.example`, `.sample`, `.template`, `.dist` |
| Ignore rule works | `git -c core.excludesFile=/dev/null check-ignore -v --no-index .env` | exit 0 = ignored; global excludes disabled so a personal ignore does not hide the gap |
| Stop tracking (remediation text only) | `git rm --cached <file>` then ignore it | the audit never runs it |
| Secret shapes | see `SECRET_PATTERNS` in `scripts/foundation_scan.py` | Wasp Nest heuristic, not archived from a primary page; read every hit; redact to 4 characters plus `****` |
| Negation trap | `!.env.example` must come after `.env.*`; an excluded parent directory cannot be re-included | git--gitignore |

## Lockfile consistency

| Package manager | Evidence in the scratch copy (via `run_in_copy.py`) |
| --- | --- |
| npm | `npm ci --ignore-scripts` exits non-zero with a lock-versus-manifest message |
| pnpm | `pnpm install --frozen-lockfile --ignore-scripts` fails when the lockfile is out of date |
| yarn | `yarn install --immutable --mode=skip-build` (Yarn 2 and later; not covered by a fetched source, label as heuristic if used) |
| uv | `uv sync --locked` (the fetched uv page does not document this flag; use only if `uv --help` in the copy shows it) |

If installation needs the network and the sandbox has none, record a cap and fall back to the script's name-presence check.

## Agent instruction health

| Concern | Check |
| --- | --- |
| Contradicts repo | instruction names a package manager, test runner or directory the repo does not use (compare to lockfile, devDependencies, tree) |
| Stale paths | the script's AGENT-005 list; open the file to confirm the path is really gone (a rename is the usual cause) |
| Too long | over 200 lines; propose moving topic rules to `.claude/rules/` with `paths:` front matter |
| Two files | AGENTS.md and CLAUDE.md both present; CLAUDE.md should import `@AGENTS.md` |
