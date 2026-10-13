# Native release qualification record

Derived evidence template. Complete under the consumer repository's report location; never store secret values. UNKNOWN/OPEN is preferable to an invented pass.

- Observation date and official source refresh:
- Owner, authorized effects and report location:
- Source revision / resolved Tauri graph / toolchain / runner:
- OS version / architecture / package route / download route / target policy:
- App and nested code paths, package paths and final SHA-256:

| Independent evidence | State (OPEN/PASS/FAIL/N/A with reason) | Exact check, target, artifact hash and sanitized output path |
|---|---|---|
| App/nested code identity and integrity | OPEN | |
| Installer/container signature where applicable | OPEN | |
| Notarization accepted status and reviewed log (macOS) | OPEN | |
| Stapled ticket and offline discovery (macOS) | OPEN | |
| SmartScreen/Smart App Control/policy observation (Windows) | OPEN | |
| Package metadata/dependencies/trust (Linux) | OPEN | |
| Actual downloaded install and first launch | OPEN | |
| Updater artifact signature and metadata binding | OPEN | |
| Invalid signature denied / interrupted download / failed install | OPEN | |
| Data-compatible recovery / reinstall / uninstall | OPEN | |

## Secrets and approvals

List protected secret NAME references and identity owner only. List separate approval/evidence for signing, service submission, credentials, installation, uploading, publication and live rollout. A completed record never grants those approvals.

## Recovery contract

Installed version -> candidate; schema version before/after; forward/backward compatibility; backup owner and restore test; permitted reinstall/downgrade path; partial download/install recovery; failed-update launch policy; revoked or lost signing/updater key response; user notification owner. Do not silently retry paid work or mutate user data. If older code cannot read migrated state, stop and design compatible recovery with DB/Rust peers rather than calling it rollback.

## Qualification

Source guidance / synthetic bookkeeping / native artifact check / packaged installation / external service acceptance are separate evidence levels. List unsupported rows and unresolved peer handoffs. Security, Quality and repository-health reports in required order; Mario's publication decision separately.
