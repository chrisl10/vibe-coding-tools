# Native worker example: bounded integer transform

This is a teaching fixture for [guide 11](../guides/11-native-background-work.md). An owned dedicated Rust thread accepts synthetic integer jobs through a one-slot channel. `try_send` rejects saturation without losing the submitted value. Each job performs memory-only reader I/O and checked CPU accumulation with cooperative cancellation. There are no file paths, network, IPC, credentials, persistent data, timers or dependency acquisitions.

The owner closes admission and joins the thread. Terminal outcomes return through the join value, so shutdown does not wait for a full result queue. Accepted jobs are collected in the thread's result vector; this teaching API accepts at most two jobs over its lifetime, bounding that vector. Production jobs require a measured byte bound and an approved result delivery contract. A start-gate channel exists solely to make saturation/disconnect/cancellation tests deterministic; tests release or drop it before joining.

Compile using the already installed compiler in an owned temporary directory:

```sh
rustc --edition=2024 --test examples/native-background-worker.rs -D warnings -o /task-owned-temp/native-worker-tests
/task-owned-temp/native-worker-tests
rustfmt --edition 2024 --check examples/native-background-worker.rs
```

Resolve `examples/` relative to the loaded Stinger. The actual run is recorded in the parent run evidence. The same source is useful for readers without Cargo because it uses only `std`. It does not prove Tokio scheduling, Tauri permissions, real file I/O, power-loss safety, a hard shutdown deadline, throughput, mobile/background suspension, Windows or Linux behavior.

Read the tests by invariant: capacity returns the rejected job; failure does not become success; cancellation retains a terminal result; cancellation between compute chunks discards a partial result; thread panic becomes a typed shutdown error; closed admission rejects another request; all successful shutdown calls join their worker. Empty shutdown does not invent a completed job. Fixture arithmetic overflow and malformed memory-reader input produce typed errors without echoing payloads.
