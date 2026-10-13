# Practice output interpretation

Illustrative output shape, not a fabricated transcript:

```json
{
  "scope": "synthetic disposable repository only",
  "git_version": "actual observed version",
  "checks": {
    "untracked_status": true,
    "staged_addition": true,
    "clean_commit": true,
    "unstage_preserves_working_bytes": true,
    "restore_preserves_backup": true,
    "branch_keeps_baseline": true,
    "reflog_contains_detached_commit": true,
    "recovered_branch_has_expected_bytes": true
  },
  "passed": true
}
```

Dirty-tree case: a user's real project contains another worker's changes. The exercise uses a different task-created temporary repository; it neither stages nor restores that real file.

Recovery case: a learner made a synthetic detached commit and returned to `practice`. The reflog identifies its full SHA, and `git branch recovered <sha>` preserves it without resetting the baseline branch.

Missing-tool case: no existing Git or no `switch`/`restore` support. Stop practice and mark it unexecuted. Do not install tools or silently replace the named teaching method.

Backup limit case: the learner has an ignored local config in a real project. A bundle alone does not preserve its bytes; no history mutation proceeds until explicitly authorized byte coverage and ownership are established.
