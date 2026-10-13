# Worked CI efficiency source cases

These are hypothetical review fixtures, not workflow runs. Case records: [JSON](ci-efficiency-cases.json). Apply [guide 17](../guides/17-reduce-ci-work-with-proof.md); replace fixture labels with actual full candidate identities and measurements in a target review.

## Duplicate build with a different environment

A Vercel Git integration builds preview candidate A. Actions also builds A and has a deployment step that rebuilds it remotely. Recommend one deployment producer, subject to owner approval of any deployment/settings change. First map each build's env/toolchain/consumer obligation: a production-shaped smoke build has a distinct contract and cannot be removed because preview succeeded. A confirmed equivalent build can be reused; fewer named jobs alone proves nothing. Baseline/proposed runtime, billed units and savings stay Unknown. Expected review: redundant producer identified; distinct smoke obligation retained; platform execution pending.

## Docs path hides a generated API contract

A workflow ignores `docs/**`, but a generator consumes `docs/api-spec.md` to build the client contract. A docs-only PR changes that file. Required workflow may never report; a shortcut treating all Markdown as irrelevant loses generator/consumer coverage. Recommend an always-admitted reporter with conservative obligation selection through the existing dependency graph. Run contract generation and consumer checks for this path; missing graph evidence runs the obligation. Expected review: shortcut rejected, candidate remains unproven until required results exist.

## Cancellation and the wrong preview

Candidate A begins tests at a moving preview URL. Candidate B arrives; concurrency cancels A and the URL now serves B. No A completion or deployment/candidate match exists. Expected review: cancellation is unproven; B's ready deployment cannot retroactively validate A. Require immutable preview identity, approved protected access, relevant successful tests and resource reconciliation. The last finished shard or an uploaded partial report cannot substitute for the missing obligations.

## Partial rerun versus combined candidate

Candidate A has accepted lint, build and shard 1 results; shard 2 fails. A rerun of shard 2 uses unchanged A, same toolchain/config, shard set and isolated baseline: its accepted result may complete the evidence union if every other obligation is retained. If base movement produces combined candidate C, A plus its rerun does not prove C. Rerunning A stays on its original event SHA/ref. Expected review: accept equivalent A union only; reject C claim and request the target's combined-candidate proof.

## Cache restores slower than installation

No timings are supplied. A proposed pnpm/browser cache adds restore/save steps and trust scope. Expected review: savings Unknown, preserve cache security and OS dependency installation. Official Playwright guidance supports fresh browser install as default; pnpm says caching is optional. Do not invent a monthly saving or assume a warm-cache speedup.
