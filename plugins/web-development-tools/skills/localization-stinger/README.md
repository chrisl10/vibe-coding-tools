# Localization Stinger
Specialist implementation owner for O073, paired only with localization-wasp-drone. Start after the framework and supported locale/content decisions are approved. It implements route/resource wiring, message and Intl formatting, and RTL behavior within existing target conventions.

| Work | Read |
|---|---|
| Locale precedence, paths, resources and privacy | [Locale guide](guides/01-locales-and-resources.md) |
| ICU/plurals, money and timezone contracts | [Formatting guide](guides/02-messages-and-formatting.md) |
| RTL, bidi, accessibility and translation review | [RTL guide](guides/03-rtl-and-translation-review.md) |
| Claim grounding | [Distillation](references/research/distillation.md) |
| Synthetic bounded assumptions | [Contract](references/contract.md) |
| Plain Node demonstration | [Mechanics](examples/mechanics.mjs), [independent proof](examples/contract-proof.mjs) |
| ICU/HTML/CSS integration shape | [Constructed examples](examples/icu-and-rtl.md) |
| Target closeout | [Evidence template](templates/evidence-report.md) |

Run node examples/contract-proof.mjs only for the bounded synthetic contract. It is not a replacement for actual application, browser or translation review. Resource injection/security belongs to Core security. UI direction and actual design implementation follow Impeccable and the selected framework owner. Typography owns language glyph/loading evidence; do not assume a Latin-only subset supports RTL scripts.
