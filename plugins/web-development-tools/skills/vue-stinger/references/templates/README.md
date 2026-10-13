# Bounded adaptation templates
Original examples, not an installed application. Resolve imports and define actual endpoints/views before use. Existing compiler/version/contracts remain authoritative.

- [Architecture record](architecture-record.md) and [state map](state-ownership.md).
- [Pure model](model.ts): runtime decoding and validation limits.
- [Composable](useRecord.ts): watcher cleanup, abort and stale suppression.
- [SFC form](RecordForm.vue): typed props/events, computed errors and labeled native controls.
- [Resource view](RecordView.vue) and [not-found view](NotFoundView.vue) demonstrate loading/error/empty/text states.
- [Component spec](RecordForm.spec.ts) exercises labels, validation, pending events and escaped server text in the existing toolchain; NOT_RUN here.
- [Routes](routes.ts): real views and independently proven host fallback required.
- [Test contract](component-test-contract.md) and [delivery evidence](delivery-evidence.md).

Vue compilation, SFC transform, vue-tsc and component/browser runtime are NOT_RUN here. No mocks or Node parser output substitute for them.
