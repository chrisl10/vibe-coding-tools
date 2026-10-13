# Grounding law

The owner's directive, applied to every agent in every kb-refresh run. Section 1 is the verbatim text to paste into every writer, verifier, fixer, and gate brief. Sections 2 and 3 are how the orchestrator enforces it.

## 1. Verbatim brief text (paste as-is)

```
GROUNDING RULES (binding, no exceptions):
1. Every behavioral claim you write must carry a citation of the form path:line pointing at the exact ref being documented.
2. Re-open the file and read the cited lines immediately before you write the citation. Never cite from memory, from a summary, from an earlier read, or from another agent's output.
3. If you cannot verify a claim by opening the source, mark it "(unverified)" inline. An unverified claim is acceptable; an uncited claim is not.
4. Sources are: source code on the pinned ref, git history, existing library docs, ADRs, PRDs, IRDs, runbooks, config files on the ref. Model memory is not a source.
5. Never write secret values, tokens, keys, passwords, private hostnames, or customer data into docs, gate reports, PR bodies, or your sus log. Environment variable NAMES are fine. If you would quote a value, quote the redacted shape instead.
6. No em dashes (U+2014) or en dashes (U+2013) in anything you write.
7. You are read-only against the codebase. If you notice a suspected bug, security hole, or functional problem: append it to your sus log with file:line and why, and move on. Never fix, refactor, revert, or work around it. Writing your assigned docs, your sus log, and your assigned reports is the only writing you do.
8. If a rule here blocks your task, stop and report. Do not reinterpret, relax, or work around it.
```

## 2. Enforcement by role

| Role | Grounding duty |
|---|---|
| Writer | Re-open before citing; `(unverified)` labels; sus log entries while reading |
| Adversarial verifier | Independently re-open every citation on the pinned commit; verdict per claim: pass, fail, unverifiable |
| Fixer | Applies only verifier-verified corrections; no self-authored improvements |
| Gate (security) | Secrets scan across docs, PR body, and quoted config |
| Gate (quality) | Citation sweep with sampled re-opens; dash sweep; completeness against the unit plan |

## 3. Judging a grounded line

A line is properly grounded when all three hold:

1. It has a `path:line` citation.
2. The citation resolves on the pinned commit (the file exists at that ref and the lines say what the claim says).
3. The claim does not overreach the lines it cites (a claim about behavior needs lines that exhibit the behavior, not lines that merely mention the topic).

Anything failing 2 or 3 is a verifier finding. Anything failing 1 with no `(unverified)` label is an automatic quality-gate failure for the unit.
