# Security notes

## Not confirmed

- `apps/api/src/admin.ts` may expose an admin route without rate limiting; could not reproduce locally because the route needs a seeded admin.
- A [suspicious link](javascript:alert(1)) in docs was noted but not followed.

## Method

Ran **security-wasp-drone** for the generic pass, then the Next.js, React, and polyglot Drones on their paths.

| Drone | Paths | Findings |
| --- | --- | --- |
| nextjs-security-wasp-drone | apps/web | 3 |
| polyglot-security-wasp-drone | apps/api | 1 |
