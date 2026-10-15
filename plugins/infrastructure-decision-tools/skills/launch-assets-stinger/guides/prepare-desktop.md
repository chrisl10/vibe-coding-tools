# Prepare desktop distribution

1. Confirm target OS, packaging technology and release route. A local prototype, internal installer, direct download and store release have different milestones. Use selected Tauri/Electron/Rust/Go owners for implementation decisions.
2. For macOS direct distribution, record Developer Program owner, Developer ID signing custodian and notarization preparation. For a store route, hand off current store requirements to App Store Submission. Do not collect private signing material.
3. For Windows, record the selected executable signing route and identity-validation owner. Keep HTTPS download hosting separate. Explain that signed artifacts can still face SmartScreen reputation checks and that EV no longer guarantees immediate reputation. Do not promise a fixed reputation-building duration.
4. Record installer icon/metadata, update endpoint and recovery responsibility, support, privacy and signed-artifact/device test evidence requests. Linux assets depend on the accepted package/update route; leave its exact distribution requirements to the selected owner when not researched.
5. Keep an offline app's cloud database deferred unless sync/licensing/account features justify it. Prepare ledger blockers and handoffs, not certificates, purchases, installers or releases.

Grounding: Apple Developer ID, Windows signing, SmartScreen, TLS. Per-product inclusion is the approved topic contract.
