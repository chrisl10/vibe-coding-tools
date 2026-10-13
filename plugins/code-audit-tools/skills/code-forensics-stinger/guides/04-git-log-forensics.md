# Acquired Git history

Acquire only within the user's permission. Preserve the supplied repository, object/reference scope and acquisition hashes. A source ZIP without Git objects is not commit-history evidence. Do not hide the purpose of acquisition or request access under a false pretext.

Git author and committer identities and timestamps are supplied by creators. History can be incomplete or rewritten. Object hashes bind captured content; corroborate dates and work with independent records. See [Git commit information](https://git-scm.com/docs/git-commit#_commit_information).

The optional `scripts/parse_git_log.py` takes `--input FILE --out DIR` after a captured `git log --all --pretty=format:'%H|%ai|%an|%ae|%s' --shortstat`. It emits `commits.json` and `git_by_month.json`. Its hour estimate uses lines changed, category hints and a cap. This is an unvalidated heuristic, not measured hours, delivery value or proof of an overcharge.

Review unusual subjects, merge/import commits, generated code, squashed work and log format limits. Keep the complete hash in source references. Absence of commits cannot establish absence of support, meetings or other contracted work. Report missing history as a coverage gap.
