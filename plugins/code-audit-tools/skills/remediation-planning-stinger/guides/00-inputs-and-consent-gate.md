# 00 Inputs and the consent gate

Goal: confirm what you have to plan from, then split the work into the part you may always do (workspace files) and the part that needs approval (files inside the audited repository's `library/`).

## Steps

1. Read `intake.json` from the workspace root. Note `tier` (this Drone runs only for `mario`), `repo.path`, `stacks`, and `workspace`. If `tier` is not `mario`, stop and tell the orchestrator.
2. List the findings files: `00-foundation/`, `01-bloat/`, `02-security/`, `03-quality/`, each with `findings.jsonl`, `metrics.json`, `notes.md`. A missing dimension is acceptable only if the tier skipped it. If a dimension that should exist has no `findings.jsonl`, stop and report which Drone has not finished. Do not plan from partial input without saying so at the top of the roadmap.
3. Validate every line of every `findings.jsonl` is JSON with the fields of `audit-contract.md` section 5. Report malformed lines to the orchestrator; do not repair another Drone's output.
4. Read each `notes.md` "Not confirmed" section. Those items are not findings and never become work packages, but mention the count in the roadmap's last section.
5. Run the first cut: `python3 scripts/build_plan.py <workspace> --repo <repo.path> --roadmap-draft <workspace>/04-remediation/roadmap.draft.md`. It reads the repository only to number PRDs and detect existing knowledge docs. It writes only inside `04-remediation/`.
6. Check the Library: does `<repo.path>/library/` exist, with `requirements/`, `issues/`, and `knowledge/private/`? Record the answer in `plan.json` under `library.present`.
7. Always write the two workspace outputs after refining (guides 01 and 02): `04-remediation/roadmap.md` and `04-remediation/plan.json`.

## The consent gate

Writing into `library/` changes the audited repository. It happens only when all of these are true:

1. `library/` already exists. If it does not, stop and tell the orchestrator: "No Library found. Offer the get-started-stinger playbook first." Never create `library/`, its folders, or its README files yourself.
2. You showed the user the exact list of files you would create, one path per line, with one line each on what it is and which findings it covers (use `templates/consent-request.md`).
3. The user approved that list. When you run in write mode, the approved list in your arming line is the user's answer: the orchestrator asked, and you do not ask again. When you run standalone, ask in chat and wait for a yes. An approval of "the plan" is not an approval of files. A partial yes (some files) means only those files.
4. Nothing on the list already exists. If a path exists, do not overwrite: propose a different number, or skip, and say so.

If the user declines or does not answer, finish with the workspace outputs only and set `library.consent_state` to `declined` or `not-asked`. That is a complete, successful run.

Before writing the first file, set `library.consent_state` to `approved` and record the approved list in `plan.json` under `library.approved_files` (the brief reports library writes only from those two fields). Write only those files.

## Boundaries

- Never touch `library/notes/` (human only).
- Never modify source code, configs, CI, or tests in the audited repository.
- Never run git commands that change state in the audited repository.
- Never invent a GitHub issue number. IRDs need real numbers (guide 03).

## Sources

- [research/distilled-remediation-planning.md](../references/research/distilled-remediation-planning.md)
- Library rules: `library-stinger/guides/00-initialize.md`, `02-issue.md`, `03-feature-prd.md`
