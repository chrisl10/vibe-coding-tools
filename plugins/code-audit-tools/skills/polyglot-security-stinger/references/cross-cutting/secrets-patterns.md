# Secrets: patterns, history search, and triage

Loaded by [guides/09-secrets-scanning.md](../../guides/09-secrets-scanning.md).

## 1. Manual ripgrep sweep (last rung of the ladder)

Shapes come from gitleaks default rules [raw/secrets--gitleaks-default-rules.md]. Python-compatible forms are in `scripts/secrets_fallback.py`.

```bash
# Provider token shapes
$RG -e '\b(AKIA|ASIA|ABIA|ACCA)[A-Z2-7]{16}\b' \
    -e '\bgh[pousr]_[0-9a-zA-Z]{36}\b' -e 'github_pat_\w{82}' -e 'glpat-[\w-]{20}' \
    -e '\b(sk|rk)_(live|prod|test)_[a-zA-Z0-9]{10,99}' -e '\bAIza[\w-]{35}' \
    -e 'sk-(proj|svcacct|admin)-[A-Za-z0-9_-]{20,}' -e 'sk-ant-(api03|admin01)-[A-Za-z0-9_-]{20,}' \
    -e '\bnpm_[A-Za-z0-9]{36}' -e '\bSG\.[A-Za-z0-9_.=-]{66}' -e 'xox[bpe]-[0-9]{10,13}-' \
    -e 'hooks\.slack\.com/(services|workflows|triggers)/' -e 'shpat_[a-fA-F0-9]{32}' \
    -e 'doo_v1_[a-f0-9]{64}' -e 'dp\.pt\.[A-Za-z0-9]{43}' -e 'pypi-AgEIcHlwaS5vcmc'
# Private keys and credentialed URLs
$RG -e '-----BEGIN[ A-Z0-9_-]{0,100}PRIVATE KEY' \
    -e '(postgres(ql)?|mysql|mongodb(\+srv)?|redis|rediss|amqps?)://[^\s:/@]+:[^\s@]{3,}@'
# Assignments with secret-looking names (noisy: read every hit)
$RG -e '(?i)(api[_-]?key|secret|token|passw(or)?d|client[_-]?secret|private[_-]?key)\w*\s*[:=]\s*["\x27][^"\x27\s]{12,}["\x27]'
# Committed env and key files
$RG --files -g '.env' -g '.env.*' -g '!.env.example' -g '!.env.sample' -g '*.pem' -g '*.p12' -g '*.pfx' -g '*.key' -g 'id_rsa*' -g 'credentials.json' -g 'service-account*.json' -g 'config/master.key' -g '*.tfstate' -g '*.tfvars'
```

## 2. History search without a scanner

Run against the bare clone (`$HIST`), never the audited repository's `.git`.

```bash
# Files that once existed and look sensitive
git -C "$HIST" log --all --diff-filter=A --name-only --format= | sort -u | rg -i '(\.env$|\.env\.|\.pem$|\.key$|id_rsa|credentials|secret|\.tfstate|\.tfvars|master\.key)'
# Commits that added a given token shape (pickaxe with regex)
git -C "$HIST" log --all -G 'AKIA[A-Z2-7]{16}' --format='%h %ad %an %s' --date=short
# Show the added line, redact before writing evidence
git -C "$HIST" log --all -p -G 'sk_live_' --format='COMMIT %h' | rg '^\+.*sk_live_'
# Was the secret removed later? (still in history means still leaked)
git -C "$HIST" log --all --format='%h %ad' --date=short -- path/to/file
```

## 3. Triage rules

| Situation | Severity | Confidence |
| --- | --- | --- |
| Live-format provider key (`sk_live_`, `AKIA`, `ghp_`, private key block) in the working tree of a deployed service | `critical` | `likely` (shape plus manual read); `confirmed` only with consented verification |
| Same, only in git history (removed from HEAD) | `high`: anyone with clone access still has it; rotation is the fix | `likely` |
| Test-mode key (`sk_test_`, sandbox) | `low` | `likely` |
| Placeholder (`xxxx`, `changeme`, `your-key-here`, `<...>`, `${VAR}`) | not a finding; note in `notes` | |
| Generic assignment hit with no provider shape | `medium` at most until read; drop if it is a variable name, a hash of a public value, or a test fixture | `possible` |
| Committed `.env` with real-looking values | `high` | `likely` |
| Committed `.env` with only placeholders | `low` (hygiene: add to `.gitignore`) | `confirmed` |
| `*.tfstate` committed | `high` when the file holds credentials; read it, since state can record resource attributes such as generated passwords | `likely` after reading |

Redaction: evidence keeps the first 4 characters then `****` (contract rule 2). Never put a full secret in any output file, including `raw/`: pass `--redact` to gitleaks, and the fallback script redacts by design [raw/secrets--gitleaks.md].

Verification: trufflehog verification calls the provider with the secret [raw/secrets--trufflehog.md]. Do not verify unless the user explicitly consented in the run; a verified result may raise confidence to `confirmed`.

The remediation for any real leaked secret is always, in order: rotate or revoke the credential at the provider, remove it from the code and load it from the environment or a secret manager, and then decide with the owner whether to rewrite history (rotation is what actually closes the hole).

Sources: [raw/secrets--gitleaks.md], [raw/secrets--gitleaks-default-rules.md], [raw/secrets--trufflehog.md], [raw/infra--docker-compose-secrets.md]
