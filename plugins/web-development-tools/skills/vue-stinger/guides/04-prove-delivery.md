# Prove delivery
1. Read existing scripts and installed dependencies. Run only approved existing checks against owned changes. Never install a compiler, component test tool or browser to manufacture proof.
2. Check pure decoders and form constraints with meaningful valid/invalid/boundary fixtures. SFC compiler/type checker evidence is separate from Node TypeScript stripping or syntax acceptance.
3. With the real Vue toolchain, exercise rendered props/events, keyboard submit, labels, disabled duplicate submits, empty/loading/error/retry, parameter changes, stale request and unmount cleanup. Test behavior rather than private state.
4. With the existing browser harness, exercise direct route refresh, not-found handling, real backend boundaries and the entire authorized flow. Record exact commands, version, changed artifact hashes and outcomes; mocks cannot prove provider/auth deployment behavior.
5. Return [delivery evidence](../references/templates/delivery-evidence.md). Use PASS, FAIL or NOT_RUN. If Vue runtime/compiler/vue-tsc is unavailable, mark those checks NOT_RUN and report what blocks acceptance. Follow ordered Security then Quality then orchestrator Health before any separately authorized commit/push.

Grounding: testing, watchers, accessibility, history.

The [component spec](../references/templates/RecordForm.spec.ts) follows Vue Test Utils forms. Its runtime is NOT_RUN in this forge.
