# Security and Secrets

## A fake secret can still cause a real problem

Secret scanners look for shapes, prefixes, lengths, and character patterns. They cannot read the author's mind. A made-up token that looks exactly like a provider token can block a push, trigger an alert, or train someone to paste unsafe examples.

Use unmistakable placeholders:

```text
<DOPPLER_SERVICE_TOKEN>
<STRIPE_TEST_KEY>
<GHL_ACCESS_TOKEN>
<WORKOS_API_KEY>
```

Avoid a real provider prefix followed by a realistic random body.

## If a scanner finds something

1. Stop copying the value into more files or mirrors.
2. Identify every occurrence and every reachable commit.
3. Decide whether the value is definitely synthetic.
4. If provenance is uncertain, treat it as real and revoke or rotate it first.
5. Replace the source example with an invalid placeholder.
6. Regenerate mirrors and packages.
7. Scan the working tree, commit range, and extracted package.
8. If the flagged commit was never pushed, rebuild the unpushed history so the bad shape is not sent to the remote.
9. Record evidence without recording the secret.

Deleting a secret in a later commit does not remove it from earlier commits. GitHub push protection can inspect the whole range being pushed.

## Repository rules

- Never commit `.env` files or credentials.
- Never print credential values into logs or reports.
- Use test accounts and least-privilege tokens for provider validation.
- Keep security review before independent quality review.
- If quality changes code, rerun both gates.
- Distinguish local proof from external provider proof.

## Package audit

Before release, confirm the archive contains no `.git`, `.env`, absolute paths, parent traversal, or credential-shaped examples. Scan the extracted archive, not only the source directory.
