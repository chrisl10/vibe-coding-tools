# Security Report: Vibe Coding Tools migration

## Executive summary

**Verdict: PASS for the working tree, release archives, and outgoing Git history.**

Scope note: the selected Security Stinger is tuned for a TypeScript and Deep Lake application, while this repository distributes Markdown instructions, hook scripts, generators, and plugin archives. I used its universal checks for credentials, packaged secrets, hidden instructions, command execution, path handling, and supply-chain boundaries. Application-specific SQL, authentication, and runtime dependency checks do not apply because this repository has no application source, package manifest, or production dependency tree.

The original Doppler examples were synthetic, but they had the exact shape of provider credentials. They and every mirrored provider-shaped example have been replaced with obvious placeholders. No Critical, High, or Medium vulnerability remains in the working tree or extracted release packages.

The local starting commit that introduced the examples was not pushed. The feature branch was rebuilt as one clean commit from `origin/main`, the local `main` reference was restored to `origin/main`, and no branch or tag contains the discarded commit. The outgoing range contains only the clean replacement commit.

## Scope and evidence

| Area | Result | Evidence |
|---|---|---|
| Working-tree secret scan | PASS | `gitleaks dir . --redact --verbose --no-banner`, 42.19 MB scanned, no leaks |
| Exact provider patterns | PASS | Doppler personal, Doppler service, Stripe secret, and AWS access-key regex scans returned no matches |
| Extracted package scan | PASS | Three archives extracted, 41.21 MB scanned by Gitleaks, no leaks |
| Archive path safety | PASS | 10,663 entries checked; no absolute path, parent traversal, or Git metadata |
| Environment files | PASS | No tracked secret `.env` file; the intentional `.env.example` documentation template contains placeholders |
| Hidden instruction characters | PASS | No zero-width, bidi, or byte-order-mark character in active project instructions |
| Hook input and output | PASS | Claude allow/deny, Codex patch deny, Cursor deny, and raw-research exemption fixtures passed |
| Manifest and metadata parsing | PASS | JSON and TOML parse checks passed; strict Claude and Codex plugin validation passed |

## Remediations completed

### SEC-01: Provider-shaped Doppler documentation examples

- **Original severity:** Critical release blocker because push protection evaluates structure, not author intent.
- **Location:** `.claude/skills/doppler-stinger/references/research/raw/doppler--tokens--service-tokens-and-token-formats.md:54` and `:55`.
- **Fix:** Replaced both random-looking token bodies with `<DOPPLER_PERSONAL_TOKEN>` and `<DOPPLER_SERVICE_TOKEN>`.
- **Propagation:** Regenerated Claude, Codex, and Cursor package content and rebuilt all three archives.
- **Verification:** Exact Doppler detector-shaped scans and Gitleaks returned no match.

### SEC-02: Other realistic credential examples

- **Original severity:** High release risk because several documentation samples matched common provider detectors.
- **Locations:** Doppler Stripe examples, GoHighLevel OAuth and bearer examples, WorkOS invitation and API-key examples, and the Git history-cleanup AWS example.
- **Fix:** Replaced each value with an unmistakable provider-named placeholder such as `<STRIPE_TEST_KEY>`, `<GHL_ACCESS_TOKEN>`, `<WORKOS_API_KEY>`, or `<LEAKED_AWS_SECRET>`.
- **Verification:** Gitleaks on the working tree and extracted packages returned no findings.

### SEC-03: Cross-harness hook parsing

- **Original severity:** Medium correctness and policy risk. A copied Claude hook would not inspect Codex `apply_patch` input or return Cursor response fields.
- **Location:** `.claude/hooks/dash-guard.mjs:39` and `.claude/hooks/component-validate.mjs:48`.
- **Fix:** Added explicit patch extraction, per-harness output detection, fixed-argument `execFileSync`, and target allowlisting for `.claude` and `.cursor` components.
- **Verification:** All five hook fixtures passed. Command execution uses a fixed interpreter and validator argument array rather than a shell-built command.

## Completed history gate

### SEC-GATE-01: Remove the unpushed secret-shaped commit from the outgoing range

The prior local commit was removed rather than hidden by a later cleanup commit. The completed evidence is:

1. The feature branch contains one clean replacement commit based on `origin/main`.
2. Local `main` points to `origin/main`.
3. Branch and tag containment checks for discarded commit `da8f8d3` return no references.
4. Gitleaks on `origin/main..HEAD` reports no leaks.
5. Exact Doppler, Stripe, and AWS provider-pattern checks return no matches in the outgoing tree.

This gate is complete. Only the clean replacement commit is eligible for push.

## Findings

- Critical: None remaining in the working tree or packages.
- High: None remaining.
- Medium: None remaining.
- Low: None detected.

## Security conclusion

The distribution content is clean, the discarded credential-shaped commit is unreachable from branches and tags, and the harness adapters preserve the intended policy without introducing shell interpolation or package traversal. The release is approved for push.

## Post-quality security rerun

Quality inventory found one generated Python bytecode file. It was deleted and narrow Python cache ignores were added. A strict outgoing diff check then found whitespace inherited from imported research documents, followed by literal conflict sentinels in a Git teaching example. Exactly the reported text files and generated mirrors were normalized, the teaching markers were indented without changing their meaning, all three archives were rebuilt, and Security reran after each package change. Gitleaks found no leak in the tree, archives, or outgoing history; core links remained clean; and `git diff --check origin/main..HEAD` passed. The corrections did not add a new executable or dependency surface.
