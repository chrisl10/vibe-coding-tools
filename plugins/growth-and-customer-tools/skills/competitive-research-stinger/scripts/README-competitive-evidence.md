# Competitive evidence checker

Python 3.9+, standard library only. Resolve this script against the loaded selected skill root.

```bash
python3 -B scripts/competitive_evidence.py references/templates/competitive-evidence.json
python3 -B scripts/test_competitive_evidence.py -v
```

The template is a hypothetical fixture with assumed numbers; it is not a completed market study. Copy it into an authorized run directory and replace values/provenance. No installation, network, credentials, shell expansion, subprocess research or output-file writes occur in the checker. Its test suite invokes local CLI processes only to prove result/error behavior.

`--verify-archives` verifies referenced regular local capture files and hashes. Relative capture paths resolve from the input file directory; traversal and symlink escapes are rejected. The example contains an illustrative hash for the bytes `fixture`, and no vendor.txt file is shipped, so do not add that flag to the example unless you create an explicitly hypothetical capture. Real runs must preserve actual evidence.

Exit 0 means mechanical consistency, not current-source truth, observed execution, buyer validation, legal compliance or a defensible moat. Stale sources produce warnings under the supplied policy; source age does not prove dataset recency. Unknown market inputs return an incomplete scenario without numbers. Exit 2 reports malformed input to stderr with empty stdout; source contents are not executed. No source text, rate, PII or secret is requested by this helper. Human review must preserve the account/role-only scope and examine evidence quality.

Use the existing ICP ledger helper for its JSONL schema; this checker does not replace its merge/score/grading. Use selected unit-economics-stinger's existing calculator separately when profitability is requested; this checker only computes reached/served accounts and a supplied annual-price scenario.
