# Worked native release candidate exercises

These are synthetic DERIVED review decisions, not native artifacts or provider results. No app was signed, installed, notarized or published.

| Candidate supplied record | Decision | Missing evidence / owning action |
|---|---|---|
| macOS arm64 app has ad-hoc signature; updater signature present; public Developer ID distribution requested | HOLD | Developer ID route qualification, native code/nested identity, accepted notarization, ticket and downloaded first-launch proof. Updater PASS cannot close them. |
| macOS app accepted by notarization service; final ZIP repacked afterward, old delivery hash retained | HOLD | Verify stapled app, bind final archive bytes/hash and repeat affected package checks; accepted service status alone does not bind transformed bytes. ZIP cannot be stapled. |
| Windows EXE/installer signatures valid; new EV-signed file shows SmartScreen warning | Signature PASS; reputation observation WARN; release acceptance OPEN | Record policy and communicate accurate expectations. Do not buy another EV certificate or claim a bypass. The release owner decides release against declared acceptance criteria. |
| Windows installer signed; bundled helper and DLL identity absent | HOLD | Inspect required payload signatures, actual installed paths and native launch. |
| AppImage built on a newer distribution; minimum target cannot satisfy required libc symbol | FAIL supported target | Rebuild on qualified oldest supported baseline, rebind hashes and test target. A successful container build cannot close desktop proof. |
| DEB control metadata correct on x86_64; arm64 build omitted; Linux support claimed generally | Narrow proof to named x86_64 row; arm64 OPEN | Native architecture-specific package/runtime tests remain required. |
| RPM package signature checked; self-updater enabled without package-manager ownership decision | HOLD | Decide update owner and data-compatible recovery before live rollout. Package trust does not replace updater signature trust. |
| Update signature valid; database migrated to schema unreadable by old release | Recovery OPEN | DB/Rust owner designs and tests compatible restore/reinstall. Do not promise automatic rollback. |

Basis: dated digest. Use [the record](../templates/native-release-qualification.md) for real artifacts, preserving each target row independently.
