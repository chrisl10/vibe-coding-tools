# Simplify state without request races

Start with transitions and data ownership, not a store-library replacement. Grounding

1. List each field, owner, readers, writes, persistence and reset rule. Classify server cache, URL, form, transient UI and derived values. Preserve the existing appropriate library; a new library is not required to simplify state.
2. Derive values from current props/state during render when they are purely computed. Keep expensive optimization evidence separate from correctness. Do not mirror a filtered list into state through an Effect unless a separate lifecycle actually requires it.
3. Consolidate coupled transitions in a pure reducer when one event changes several fields. Preserve atomic transitions, optimistic rollback and request identity. Functional updates avoid stale snapshots for updates based on previous state. Do not merge unrelated lifetimes merely to shrink field count.
4. For Effect-based fetching, retain dependencies and cleanup. Ignore obsolete responses, and cancel transport where supported; abortion alone does not establish application ordering. Guard completion by active request identity or cleanup status. Cover A-start/B-start/B-finish/A-finish, unmount, rejection, refresh, double submission and tenant/user switch. Never retain previous-tenant results in a shared cache accidentally.
5. Compare event traces and derived views before/after using the installed test setup. The [synthetic reducer/request exercise](../examples/outcome-modernization.md#state-simplification) proves only the stated JavaScript transitions. Mounted Effects, Strict Mode cleanup, subscriptions and UI updates need native React tests. Preserve behavior first; fix preexisting races as a separately stated behavior change.

A user event belongs in its event handler; an Effect synchronizes an external system. Keep subscribed external stores and server caches under their existing owners. Do not remove an Effect simply because a scanner flagged it.
