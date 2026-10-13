# Learn Git with a disposable practice repository

Grounding: [fresh command distillation](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/src/skills/git-stinger/references/research/beginner-practice/distillation.md).

## Before practice

Resolve the actual selected `git-stinger` through Core and load the paired Git Drone. Confirm this is teaching in a newly created disposable repository, not recovery or changes to the user's real project. Use `git --version`; this exercise requires Git with `switch` and `restore` (the existing matrix states 2.23 or newer), and the supplied runner checks installed support. Do not install Git, configure credentials, or edit global settings as part of the lesson. For real incidents use the matching recovery guide and explicit action authorization.

The automated exercise is `python <checked-skill-root>/scripts/practice-git.py --run`. It accepts no repository path, creates its own temporary repository, commits only synthetic task-created files, isolates inherited Git routing/configuration and hooks, uses fixture identity through per-command flags, reports actual checks, then removes only that created temporary directory. It does not authorize commits to a user repository. If Python/Git are missing, deliver instructions labeled UNEXECUTED.

## The bounded analogy

Think of the working tree as your desk, the index as a tray holding the exact pages for the next saved snapshot, and commits as saved snapshots. A branch is a named pointer to a commit; it is not another physical folder or a backup. Editing the desk after putting a page in the tray does not automatically replace the staged page. Reflog is a local movement log, not an unlimited backup and not a record of every unsaved keystroke.

## Exact practice sequence

All steps below run only inside the fresh runner-created exercise. Do not paste them into an existing repository. The runner applies fixture identity and disabled-hook settings per Git command; it never writes global identity.

1. Create the isolated practice repository and set its unborn HEAD to `practice`. Add synthetic `note.txt` containing `first draft` using Python file I/O. Run `git status --porcelain`; expect `?? note.txt`.
2. Run `git add -- note.txt`, then `git diff --cached --no-ext-diff --no-textconv -- note.txt`. Explain that the staged addition will form the first snapshot. Commit with per-command identity: `git -c user.name=Practice -c user.email=practice@example.invalid -c commit.gpgSign=false commit -m "practice: first snapshot"`. The runner additionally supplies an empty hooks path and isolated configuration. Expect a clean status.
3. Change the same synthetic file to `second draft`. Run `git diff --no-ext-diff --no-textconv -- note.txt`, then `git add -- note.txt` and `git diff --cached --no-ext-diff --no-textconv -- note.txt`. Explain unstaged versus staged comparison. Run `git restore --staged -- note.txt` to remove the change from the tray while preserving the edited file; inspect status and bytes.
4. Before deliberately discarding the task-created edit, save a byte-for-byte copy outside the practice repository in the task's temporary directory. Run `git restore --worktree -- note.txt`. Verify the file matches the committed first draft and the saved copy still contains second draft. This restore is destructive to that edit; it is permitted only for the synthetic exercise file with its known backup.
5. Verify clean status, run `git switch -c lesson`, make/stage a synthetic lesson edit, then commit using the same fixture flags. Run `git switch practice`. Verify the practice file still contains first draft and `git branch --list` shows both pointers. A real dirty tree or collaborator-owned file requires stopping and inspecting, not forcing a switch.
6. In this clean disposable repository only, run `git switch --detach lesson`, make and commit a synthetic `detached draft`, capture the full commit SHA, and run `git switch practice`. Run `git reflog --format=%H` and verify the captured SHA is present. Inspect it with `git show <captured-full-sha>:note.txt`, then create `git branch recovered <captured-full-sha>`. No history rewrite or deletion is required.
7. Run `git switch recovered`, verify the detached draft's bytes, confirm a clean status, and record the final checks. The runner removes only its own temporary directory after evidence is captured. It leaves the user's repository untouched.

## Failure and collaboration safeguards

- Dirty real tree, wrong cwd, unowned file, shared branch, or unclear task authority: stop the dependent mutation and inspect ownership. Never default to hard reset, force switch, stash deletion, branch deletion, or force-push.
- Missing identity in a real project: explain the owner decision. Do not change user/global configuration or enter credentials. The fixture identity exists only for synthetic commits.
- Before any history-changing operation in a real project, obtain exact action/path/ref authorization and preserve needed source bytes, untracked files, ignored files, and repository history in approved backup locations. A Git bundle covers referenced history, not all dirty or ignored bytes. Reflog alone is insufficient backup.
- New branch recovery preserves the found commit without replacing the user's current branch. Reflog recovery cannot promise unsaved-file recovery or expired/collected objects.
- No remotes, clone, fetch, pull, push, PR, account, credential, or installation stage belongs to this exercise. Explain collaboration separately using the actual team's accepted policy.

Use [worksheet](../templates/beginner-git-worksheet.md), [worked output](../examples/beginner-git-practice.md), and the runner's observed report. A successful synthetic exercise demonstrates these state transitions on the recorded Git version, not understanding or safety of a real recovery operation.
