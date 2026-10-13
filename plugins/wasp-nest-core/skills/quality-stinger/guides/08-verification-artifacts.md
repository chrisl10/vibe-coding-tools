# Bind verification to the candidate actually reviewed

Use alongside inventory, traceability and report writing whenever a QA conclusion depends on executed checks, generated outputs or imported evidence. O293 extends the existing report; it grants no permission to run remote jobs or publish evidence. Start with the receiving plan and repository's existing tooling. [Research and limits](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/src/skills/quality-stinger/references/research/verification-artifacts/distillation.md).

## 1. Declare the claim and the scope

Write what this packet can establish: source guidance qualification, static analysis, local behavioral exercise, native app behavior, provider integration or manual observation. Map each required claim to plan items and actual evidence. A source guide's examples are not an app implementation. Mark hypothetical examples explicitly. Ask about ambiguous acceptance criteria before dependent work.

## 2. Pin the bytes and freeze the inputs

Record resolved full base/head IDs and worktree identity. Inventory committed, staged, unstaged and untracked files with existing repository tools. A three-dot diff alone does not capture dirty inputs; retain the existing inventory procedure. See [Git reference](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/src/skills/quality-stinger/references/research/verification-artifacts/raw/git-diff.html.txt).

Reuse an existing candidate manifest. If none exists, record a deterministic sorted inventory of reviewed relative paths and exact-byte hashes using already available tools. State scope exclusions, deleted-path representation, modes and symlink policy. Include relevant plan, configuration, fixtures and lockfiles; do not collect secrets or unrelated customer files. Hash the manifest bytes. Keep the manifest/report outside its own subject set to avoid circular hashes. Record external inputs that cannot be pinned as limitations. Do not call a scoped manifest a full-repository identity.

Stop edits to the reviewed scope while checking. Compare current inputs with the pin before and after the check. A changed candidate makes previous evidence STALE for changed claims; retain the old receipt. Reconcile coverage and rerun affected checks on the new pin. Unchanged results may be reused only with explicit scope and dependency reasoning. Never silently relabel an old result as current. Do not touch another active worker's files to obtain a freeze.

## 3. Capture actual check receipts

Fill [verification-artifacts.md](../templates/verification-artifacts.md) with the exact invocation, cwd, runner/tool versions, relevant nonsecret inputs, timestamps, exit/signal, observed outcome counts, and log/output hashes. Preserve permitted raw logs separately from summaries. Redact sensitive values before sharing and record the redaction boundary. A submitted job or wrapper exit is not proof that every required child check completed.

| Local result label | Required observation |
|---|---|
| PASS | Check executed, satisfied its stated assertions, and remained bound to its candidate. Required behavior outside its coverage remains unproven. |
| FAIL | Executed assertion or required check failed; cite actual failure and coordinates. |
| NOT_RUN | No execution evidence, including written examples, unavailable runner or permission-dependent operation. |
| SKIPPED | Runner explicitly skipped it; retain reason and affected requirement. |
| CANCELLED | Execution was cancelled; completed partial outputs do not prove remaining work. |
| INCOMPLETE | Missing terminal state, truncated required evidence or unaccounted child checks. |
| STALE | Recorded result applies to an older candidate or relevant changed input. |
| UNKNOWN | A required fact was not observed; do not manufacture timestamps, counts or exits. |

Keep runner labels such as xfail and xpass and their configured strictness. A green exit does not convert those cases into passed assertions. [pytest outcome semantics](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/src/skills/quality-stinger/references/research/verification-artifacts/raw/pytest-skips.html.txt). For a negative test, record the expected refusal/error and actual assertion result; an ERROR line may be the expected fixture output. Inspect the terminal test summary and required assertion rather than guessing from one log line.

## 4. Identify generated artifacts and their producer

Record source candidate, build command/version, inputs, invocation receipt and each output's actual digest. A successful build does not establish that the packaged output contains the reviewed bytes. Use existing distribution checks to compare expected contents, transformation rules and output identity. If a report imports external evidence, retain its subject, producer and verification basis; identify agent-authored summaries as summaries.

SLSA separates outputs, build inputs, builder and run metadata. Use that separation without claiming conformance to its format. [Build provenance](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/src/skills/quality-stinger/references/research/verification-artifacts/raw/slsa-build-provenance.html.txt). A local manifest has no signature or independent producer verification unless actually supplied. Hash equality is an integrity observation, not a trust, license or security verdict. Where signed provenance exists, record the verification result against the intended artifact and expected producer policy; absence stays NOT_PRESENT. [Attestation purpose](https://github.com/legioncodeinc/the-wasp-nest-source/blob/main/src/skills/quality-stinger/references/research/verification-artifacts/raw/github-attestations.html.txt).

## 5. Close only the supported claims

Security must precede Quality for the same candidate; unresolved findings or a stale Security snapshot halt the dependent QA verdict. Put candidate identity and receipts before the Summary using the existing report template's metadata area. Preserve its seven section order and five axes. Link logs and companion packet from traceability rows. Separate observed proof from reviewer interpretation and authorship. This packet does not make a source author an independent reviewer or grant merge/deploy approval. Record missing runtime, external provider and other-host proof explicitly.

See [constructed review cases](../examples/04-verification-artifact-cases.md). They are reasoning exercises with no app, provider, CI or signature execution claims.
