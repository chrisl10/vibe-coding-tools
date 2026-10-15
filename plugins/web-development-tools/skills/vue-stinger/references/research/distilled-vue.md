# Vue implementation digest
Retrieved 2026-10-08. The ledger pins URL, fetch date, body hash and exact archive hash. Live documentation has no stated publication date. These are current snapshots, not release-version certification. Templates below are original bounded examples; protocol decisions are project recommendations.

| Decision | Evidence and consequence |
|---|---|
| Reactive ownership | Ref state stays local by default. Destructuring primitive properties from a reactive object disconnects tracking. Return a plain object of refs from a composable so destructuring preserves refs. Reactivity, Composables. |
| Derived values | Computed getters perform pure derivation; no mutation, async request or DOM effect. Watchers own side effects. Computed, Watchers. |
| Cleanup | Watch callbacks receive onCleanup; register cancellation before awaiting. onWatcherCleanup requires Vue 3.5+ and synchronous registration. Synchronously created setup watchers stop on unmount, while asynchronously created ones require explicit stopping. Templates use callback cleanup and stale-result suppression. Watchers. |
| Typed boundaries | Props flow down, events request changes. Type-only defineProps/defineEmits support Composition API SFCs; type checking does not validate network JSON. Preserve props access through getters, including across composable boundaries; reactive destructure behavior depends on Vue 3.5. Props, Events, Types. |
| Shared state | Keep independent draft state per component; lift genuinely shared state and centralize mutations. Vue recommends Pinia for new larger shared-state applications. Existing state architecture wins; adding Pinia needs authorization. Do not share process-global request state under SSR. State. |
| Forms | v-model synchronizes JavaScript state with form controls. Native semantic labels and instructions remain necessary; placeholders are insufficient. Forms, Accessibility. |
| Client routing | A parameter change can reuse the component instance, so watch the specific parameter. History routes require host fallback for deep links and an application not-found route; configure nothing without approval. Router, History. |
| User data | Interpolation escapes text. Untrusted templates and unsanitized HTML are unsafe. URL sanitation belongs before storage at the backend; a client route guard is no authorization boundary. Templates render only text and construct same-origin URLs from encoded identifiers. Security. |
| Testing | Separate pure unit, rendered component and full browser tests. Vue recommends Vitest for Vite-based unit tests; select the existing toolchain and test observable behavior. Neither a parser test nor a static format check proves an SFC compiles or a user flow works. Testing. |

The original component spec uses awaited setValue/trigger and emitted-event assertions from the official Vue Test Utils form guide. A synthetic submit checks the component handler; it does not prove real browser keyboard/default submission behavior.

No compiler, Vue runtime, SFC transform or vue-tsc was available or installed for this staging run. Framework-dependent examples remain NOT_RUN. Browser accessibility, history fallback and real auth/backend behavior need separate application evidence.
