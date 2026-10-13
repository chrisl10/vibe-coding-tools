# File safety negative decisions

All cases are CONSTRUCTED_DECISION, NOT_RUN. These are expected decisions for a future authorized consumer test, not executed assertions or native acceptance.

| Case | Required decision / preserved asset | Required future proof |
|---|---|---|
| Picker cancelled or token expired/reused | no read/write; invalidate operation | command test and real picker |
| Different window/origin uses selection token | deny | native IPC capability denial |
| Selected directory implies recursive import | deny without explicit recursive contract | dialog/plugin exact-version behavior |
| Traversal, encoded separator, prefix sibling, alternate stream/device path | reject under target-native parser | each supported OS |
| Symlink/reparse ancestor swaps after check; hardlink aliases owned file | qualified handle operation or fail closed | hostile-race/native identity tests |
| FIFO/device/directory pretending to be JSON | reject before read can block | target type and handle tests |
| Input grows after initial size check | stop at bytes-read cap; no state commit | bounded streaming test |
| Malformed JSON, unknown schema, executable instructions, archive bomb/link member | reject or inert validated data; preserve source | parser/expansion tests |
| Missing parent or new leaf cannot canonicalize | validate retained existing parent; do not guess | native creation test |
| Existing export target without overwrite approval | preserve target; deny | atomic no-replace test |
| Destination changes after overwrite preview | deny unless exact commit precondition enforced | target concurrency test |
| Disk full, ACL denial, lock, write/sync failure | preserve prior target; bounded redacted error | authorized native failure test |
| Cross-volume rename | explicit error; no hidden copy-delete | real separate-filesystem test |
| Crash after rename, power loss, network mount | durability OPEN until target proof | real recovery, storage evidence |
| Cleanup name/mtime matches but provenance unknown | retain | trusted manifest test |
| Imported/tampered ownership manifest | reject; no deletion | provenance validation test |
| App-private dir contains unowned file or external link | no blanket recursive delete | target cleanup test |
| Export originally created by app in Documents | retain as user-owned | packaged uninstall sentinel |
| Partial uninstall or another app process still writing | quiesce or retain; exact per-item ledger | authorized installer/concurrency test |
| Installer wildcard, subscription, provider/cloud backup | no assumed data ownership or external action | owner-specific contract and approval |
