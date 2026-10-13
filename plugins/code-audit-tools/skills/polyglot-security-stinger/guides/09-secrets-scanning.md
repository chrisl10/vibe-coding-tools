# 09 Secrets scanning (working tree and git history)

Loads [../references/cross-cutting/secrets-patterns.md](../references/cross-cutting/secrets-patterns.md), [../references/cross-cutting/tool-commands.md](../references/cross-cutting/tool-commands.md), `scripts/secrets_fallback.py`.

The generic `security-wasp-drone` also scans secrets repo-wide. This guide still runs for this Drone's paths and the infra files it owns; the brief renderer merges duplicates.

## Steps

1. **Prepare the targets.** Working tree: `$COPY` (from `git archive`, so it has committed files only; uncommitted local files are out of reach, record that as a cap). History: a bare clone, `git clone --bare --no-local --quiet "<repo>" "$HIST"`. Cloning only reads the source repository. If cloning fails, record the cap "git history not scanned" and continue with the tree.
2. **Climb the ladder** in tool-commands.md section 3 (Secrets), stopping at the first rung that runs:
   1. gitleaks v8.30.1: `dir` mode on `$COPY` and `git` mode on `$HIST`, both with `--redact` and JSON reports [raw/secrets--gitleaks.md].
   2. trufflehog v3.97.9 with `--no-verification` [raw/secrets--trufflehog.md].
   3. `scripts/secrets_fallback.py` (tree, and `--history --no-tree` on `$HIST`) [raw/secrets--gitleaks-default-rules.md].
   4. the manual `rg` sweep plus the git pickaxe commands in secrets-patterns.md sections 1 and 2.
3. **Never verify a secret against its provider** unless the user consented in this run. Verification sends the secret to a third party [raw/secrets--trufflehog.md].
4. **Scope the hits.** Keep hits under this Drone's paths, root-level config, and the infra files from `detect.json.infra`. Drop hits inside other Drones' paths (note the count).
5. **Read every hit.** Open the file and line (tree) or the commit (history: `git -C "$HIST" show <commit> -- <path>`). Classify with the triage table in secrets-patterns.md section 3: live-format, test-mode, placeholder, or noise.
6. **Check for removal.** For tree hits, check whether the value is also in history (it almost always is). For history-only hits, confirm the file at HEAD no longer has it. Both are findings; the severity differs.
7. **Check committed sensitive files**: `.env`, keys, `*.tfstate`, `*.tfvars`, `config/master.key`, service-account JSON (the `--files` sweep and `detect.json.infra.env_files`).
8. **Check how secrets reach the app** for each stack: environment variables or a secret manager (good), compose `environment:` with literals or Dockerfile `ENV` (finding per guide 12) [raw/infra--docker-compose-secrets.md].
9. **Write findings.** One finding per distinct secret (not per occurrence); list every location. Evidence shows the redacted value (first 4 characters then `****`), the rule id, and the commit when from history. Remediation is always: rotate or revoke at the provider first, then move to environment or a secret manager, then decide on history rewriting with the owner.
10. **Record measures**: `secrets_live` (count of live-format secrets), `secrets_history_only`, `secret_files_committed`, each with the tool and version as `source`.

## Done when

The tree and history were scanned (or caps recorded), every hit was classified, nothing unredacted was written anywhere in the workspace, and the measures are in metrics.

## Sources

[raw/secrets--gitleaks.md], [raw/secrets--gitleaks-default-rules.md], [raw/secrets--trufflehog.md], [raw/infra--docker-compose-secrets.md]
