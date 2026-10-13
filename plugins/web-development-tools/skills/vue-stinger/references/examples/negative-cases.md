# Negative cases
| Trigger | Required rejection or repair | Proof needed |
|---|---|---|
| React hook copied into Vue SFC | Use Vue Composition API, preserve chosen stack | Real SFC compile/typecheck |
| watch(props.id, ...) snapshot | Watch getter; version-aware destructure boundary | Change prop and observe rerun |
| Fetch in computed getter | Move effect into watched source with cleanup | No duplicate side effects |
| Async watcher creation | Create synchronously or explicitly stop | Unmount cancellation |
| Slow old response after navigation | Abort and suppress stale results | Controlled overlapping real component requests |
| Prop mutation from child | Emit typed intent | Parent state updated through contract |
| Arbitrary v-html or user template | Render escaped text; approved sanitation owner for required rich HTML | Security review and render test |
| Placeholder-only label or clickable div | Native controls, explicit label and keyboard | Browser keyboard/focus check |
| Router guard treated as tenant auth | Retain server authorization | Backend isolation evidence |
| SPA history refresh 404 | Pending host fallback proof; no unapproved settings edits | Real direct navigation |
| SSR/Nuxt requested | Route to selected SSR owner; explicit missing owner if unavailable | SSR-specific qualification |
| Missing compiler or component runner | NOT_RUN, no install or stub | Authorized toolchain availability |
| Store added to isolated draft | Keep state local | Independent two-instance behavior |
| Mock/parser success called application delivery | Reject qualification claim | Actual compiler/component/browser output |
| Another worker owns required file | Stop dependent edit and hand off | Scoped ownership resolution |
