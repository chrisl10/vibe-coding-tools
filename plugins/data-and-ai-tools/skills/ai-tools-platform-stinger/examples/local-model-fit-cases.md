# Local-model source cases

1. **Publisher card only:** Qwen3-0.6B card capture states 32768 context and Apache-2.0. No artifact was downloaded. Artifact hash, quantization, runtime, user hardware and performance are Unknown. Decision: conditional candidate; no fit or quality claim.
2. **Disk file fits, memory unknown:** A hypothetical owner supplies a 5 GiB artifact on a machine with 8 GiB physical RAM but no free-RAM, KV/context, backend-buffer or OS-load measurements. Disk capacity is not memory capacity. Decision: conditional, collect missing fields rather than declaring 8B runs comfortably.
3. **Concurrency changed:** A previously observed single-request setup moves to four requests at the same context. Ollama FAQ documents context-memory growth with parallel requests. The earlier run does not prove the new load fits; requalify peak memory, latency and quality.
4. **Supported GPU, wrong OS/backend:** Check the exact combination against hardware documentation and LM Studio requirements. A marketing GPU family alone does not qualify the installed driver/runtime. Unsupported combination fails eligibility; no silent installation or purchase.
5. **Local runtime with remote tool:** The model call may be local while search, embeddings, telemetry or fallback sends data elsewhere. Ollama FAQ distinguishes local and cloud features. Decision: privacy Unknown until the whole application's egress and retention are reviewed; no config changed.

No user hardware was inspected, no inference ran, and no latency, memory fit, savings or privacy outcome is claimed.
