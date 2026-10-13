# 05: Merge the ledger and grade claims

## Commands

Resolve `scripts/icp_ledger.py` relative to this Stinger's `SKILL.md` and run it with your tools:

```text
python <skill>/scripts/icp_ledger.py validate <run-dir>/lane-*.jsonl
python <skill>/scripts/icp_ledger.py merge <run-dir>/lane-*.jsonl -o <run-dir>/ledger.jsonl
python <skill>/scripts/icp_ledger.py score <run-dir>/ledger.jsonl --company-domain <domain> --pretty -o <run-dir>/score.json
python <skill>/scripts/icp_ledger.py render <run-dir>/ledger.jsonl --company-domain <domain> -o <run-dir>/evidence.md
```

Exit code 1 means validation or privacy failure: fix the lane file (remove personal data, correct enums, shorten quotes) and rerun. Never bypass the privacy check. After changing the script, run `--self-test`.

## What the grades mean

| Grade | Rule | Use in the dossier |
|---|---|---|
| strong | 3+ independent domains, 2+ source types, 1+ revealed | Finding |
| moderate | 2+ independent domains | Finding, with its limits |
| weak | 1 domain | Hypothesis |
| contested | contradicting domains at least half of supporting | Present both sides |

These thresholds are **derived**: they operationalize the documented idea that realized-customer evidence outranks stated positioning (D2, C5). Also read `first_party_only` and `stated_only`: a claim supported only by the company's own marketing is never the primary ICP, whatever its count.

## Normalizing before scoring

Grading groups identical `(claim_type, value)` pairs after lowercasing, so inconsistent labels split the evidence. Before scoring, reconcile values across lanes to the conventions in [references/LEDGER-SCHEMA.md](../references/LEDGER-SCHEMA.md) (size bands, plain industry labels, role-prefixed personas). Keep a source's own wording in `note` when you normalize it.

## Second pass (Deep mode)

For weak claims that would change the ICP if confirmed, run one targeted query each and rescore. Stop when a second pass adds no new domain.
