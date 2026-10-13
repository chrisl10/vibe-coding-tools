# Fictional fit exercise, not a customer estimate

A fictional owner supplies a stateless AMD64 Node HTTP image, PostgreSQL data, no uploads/native syscalls, a continuous queue consumer, European users, 20 requests/sec peak estimate, unknown RAM and a two-hour/week operations budget without Linux coverage. Planned new account creation: 20 October 2026. RPO one hour and RTO four hours are desired, unproven. Region preference FRA is supplied; DB co-location and exact extension eligibility are unverified.

Recommendation: PROVISIONAL App Platform service plus separately sized worker and managed PostgreSQL, because server management exceeds supplied operator coverage. Droplets lose on that responsibility constraint, not on an invented price comparison. Do not select the $5 fixed service simply from request count or assume request scaling applies to the worker. App RAM and DB extension/region/connection evidence remain missing.

Date-sensitive DB constraint: this fictional new account has never created a PostgreSQL or MySQL cluster. Standard standby eligibility is restricted for its planned create date under archived policy. If business availability needs a standby, investigate current Advanced eligibility/rates instead of recommending a historic $30 primary+$30 standby topology. No actual resources or account were inspected.

Cost handoff: give Operating Cost component quantities, dated plan rows after sizing, DB edition/nodes/storage, transfer routes/pools, queue/object costs if needed, support/domain and operator hours. Total UNPRICED until those inputs exist. Desired recovery targets require a separately authorized restore/cutover rehearsal. Public seven-day PITR capability does not prove achieved one-hour RPO/four-hour RTO.

Review trigger supplied for this exercise: revisit after the owner measures peak memory, DB connections and queue lag at the intended load. Those measurements were not run. No purchase, login, deployment or native host dispatch occurred.
