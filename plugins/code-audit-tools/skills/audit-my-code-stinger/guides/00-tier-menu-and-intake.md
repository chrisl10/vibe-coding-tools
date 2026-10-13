# 00. Tier menu and intake

Load this guide at the start of every `/audit-my-code` run. It ends when `intake.json` exists and the throwaway copy is ready.

References: [audit-contract.md](../references/audit-contract.md) sections 1, 3, 4; [tier-matrix.md](../references/tier-matrix.md); [intake-script.md](../references/intake-script.md).

## Steps

1. **Resolve the tier.** Match `$1` case-insensitively against the tier table in the contract. No match: show the menu from [tier-matrix.md](../references/tier-matrix.md), including the token weight and what each tier adds, and wait for a choice.
2. **Resolve the repository.** Default is the current working directory's git root (`git rev-parse --show-toplevel`). A path in `$2` overrides it. Record branch, HEAD sha (`git rev-parse --short=8 HEAD`), and the remote URL. If the working tree is dirty, say so: the audit runs against HEAD, and uncommitted changes are not audited unless the user asks to audit the working tree instead. Then build the copy in step 6 from the files git knows about, so ignored files (`.env`, keys, local credentials) never enter it:
   `git -C <repo> ls-files -z --cached --others --exclude-standard | rsync -a --from0 --files-from=- --include '.env.example' --exclude '.env' --exclude '.env.*' --exclude '*.pem' --exclude '*.key' --exclude '.npmrc' --exclude '*.tfstate*' <repo>/ <workspace>/.scratch/repo-copy/`
   Record the excluded patterns as a cap. A test that fails because a `.env` is missing is a cap, never a reason to copy one in.
3. **Ask the intake questions** in one message, with defaults filled in from what you found, per [intake-script.md](../references/intake-script.md): who the brief is for (default: the git user name), scope include and exclude paths (default: everything tracked, minus vendor, generated, build output, fixtures, and `*.d.ts`), the workspace path (default: `<parent-of-repo>/<repo-name>-code-audit/<YYYY-MM-DD>-<tier>/`), and whether the repository's own code may run (default: no; see the code execution consent table in contract section 4). For `mario`, also confirm `library-stinger` and `knowledge-stinger` are installed (see [04-mario-tier.md](04-mario-tier.md)); if they are not, offer to run `full` instead.
4. **Detect stacks.** Run the polyglot Stinger's detector against the repository root:
   `python3 <polyglot-security-stinger>/scripts/detect_ecosystems.py <repo>`
   Put its `stacks` array into `intake.json` unchanged. Add `languages` from `cloc` or the bloat Stinger's line counter if it has already run; otherwise leave it for the bloat Drone to fill.
5. **Create the workspace** with the folder layout from the contract, only the dimension folders the tier needs, plus `brief/`.
6. **Make the throwaway copy** for tiers that run tools (`vibe` and above):
   `git -C <repo> archive --format=tar HEAD | (mkdir -p <workspace>/.scratch/repo-copy && tar -x -C <workspace>/.scratch/repo-copy)`
   The copy has no `.git`, which is what the tools need. If a Drone needs history (secrets in history, churn), it reads the real repository's `.git` read-only with `git log` and `git show`, never with commands that write.
7. **Write `intake.json`** per contract section 4, then tell the user in two lines: what will run, where output goes, that the repository's files will not change, and whether its code will run (and how: container, host, or not at all).

## Why a sibling workspace

The audit must leave the repository exactly as it found it, so nothing is created inside it, not even an ignored folder. A sibling folder also keeps the brief next to the repo where the user will look for it, and it survives `git clean`.
