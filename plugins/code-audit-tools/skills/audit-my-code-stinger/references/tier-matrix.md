# Tier matrix

The menu shown when `/audit-my-code` runs with no tier, and the source for every tier decision.

## Menu text

Show this to the user as is:

> **Which audit do you want?**
>
> 1. **Foundation** (`foundation`): Is this repo set up so people and AI agents can work in it safely? Library, agent instructions, CI, tests, lint, lockfiles, secrets hygiene, governance. Light.
> 2. **Vibe (Lite)** (`vibe`): Foundation, plus how much of the code is copy-paste, dead, or packed into giant files (jscpd, knip, cloc). Answers "is it bloated because it was vibe coded?" Light to medium.
> 3. **Basic** (`basic`): Vibe, plus a security audit: a generic pass and a framework-deep pass for React, Next.js, SvelteKit, or other stacks. Medium.
> 4. **Full** (`full`): Basic, plus a quality audit: does the code do what its plans and README say, and do its tests, lint, and typecheck pass? Heavy.
> 5. **Mario Audit** (`mario`): Full, plus remediation planning: a Now/Next/Later roadmap, knowledge docs, and PRDs and IRDs written into your `library/` after you approve the list. Requires the Wasp Nest core (`library-stinger`, `knowledge-stinger`). Very heavy.
>
> Every tier ends with a branded brief. Only the Mario Audit writes anything into your repository, and only after you approve the exact files. Checks that would run your repository's own code (tests, lint, typecheck, and the unused-code tool's config loading) ask first, and default to not running it.

## Dimensions by tier

The owner's tier definitions call the jscpd, knip, and cloc checks "new" (Lite is "health plus new, which is jscpd, knip, cloc"), so every tier from Vibe up includes the bloat dimension: Basic is health plus security plus new, and Full is health plus quality plus security plus new.


| Tier | foundation | bloat | security | quality | remediation | brief |
| --- | :---: | :---: | :---: | :---: | :---: | :---: |
| foundation | yes | | | | | yes |
| vibe | yes | yes | | | | yes |
| basic | yes | yes | yes | | | yes |
| full | yes | yes | yes | yes | | yes |
| mario | yes | yes | yes | yes | yes | yes |

## Brief sections by tier

| Section | foundation | vibe | basic | full | mario |
| --- | :---: | :---: | :---: | :---: | :---: |
| Cover, one-paragraph summary, verdict scorecard | yes | yes | yes | yes | yes |
| Foundation | yes | yes | yes | yes | yes |
| Duplication, unused code, size and structure | | yes | yes | yes | yes |
| Security (generic plus framework) | | | yes | yes | yes |
| Quality | | | | yes | yes |
| Remediation roadmap | | | | | yes |
| Fix these first, coverage and caps, method, evidence index | yes | yes | yes | yes | yes |
