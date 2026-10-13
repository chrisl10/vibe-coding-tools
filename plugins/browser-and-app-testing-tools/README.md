# Browser and App Testing Tools

Automate browsers, capture live apps and measure Lighthouse/PageSpeed behavior.

Browser/CDP expertise and authenticated capture are reused by audit and engineering workflows without duplicating their implementations.

Requires `wasp-nest-core`.

<!-- wasp-pack-guide:start -->
## Choose a capability

This pack contains 4 skills, 4 agents and 1 source command. The table explains each source skill; open its linked instructions for exact inputs, outputs and limits.

| Skill | What it does and when to use it |
| --- | --- |
| [browser-automation-stinger](skills/browser-automation-stinger/SKILL.md) | Playwright and Puppeteer automation for deterministic browser tests, debugging, downloads, screenshots, and browser lifecycle control. Use for browser automation work. |
| [chrome-chromium-stinger](skills/chrome-chromium-stinger/SKILL.md) | Chrome DevTools Protocol and Chromium development for remote debugging, profiles, protocol inspection, source builds, and browser-engine diagnosis. Use for Chrome or Chromium engineering. |
| [lighthouse-pagespeed-stinger](skills/lighthouse-pagespeed-stinger/SKILL.md) | Runs Lighthouse and PageSpeed Insights for React/Next.js: CI setup (LHCI), audit categories, performance budgets, lab-vs-CrUX gap. Use when setting up or debugging Lighthouse CI. |
| [webapp-capture-stinger](skills/webapp-capture-stinger/SKILL.md) | Capture live web apps. Demo videos and scripts; component library with tokens, a Claude Design handoff zip, and a shadcn/ui map; visual and code audits. |

## Start one task

Required packs: `wasp-nest-core`

Install the selected pack and its prerequisites through the marketplace. For the version 3 layout, purge the previous installation first. Select the skill shown by your client, or paste this request with real paths and scope:

After adding the Wasp Nest marketplace, Claude Code uses these installation instructions:

```text
/plugin install wasp-nest-core@wasp-nest
/plugin install browser-and-app-testing-tools@wasp-nest
```

Other clients use their plugin selection UI or discovered skill selector. Installing a package and invoking a task are separate steps.

```text
Use webapp-capture-stinger to capture [accessible app] within [page scope]. Report missing login or capture tools and avoid submitting forms.
```

Expected result: The scoped screenshots, walkthrough or browser review. Actual browser access and the requested capture tools must be available.



Claude Code plugin command names:

| Command | What it does |
| --- | --- |
| `/browser-and-app-testing-tools:webapp-capture` ([procedure](commands/webapp-capture.md)) | Capture a live web app. Demo video and script; component library with design tokens, a Claude Design handoff zip, and a shadcn/ui map; UI inconsistency audit. |

## Agent responsibilities

| Agent | Responsibility | Paired skill |
| --- | --- | --- |
| [browser-automation-wasp-drone](agents/browser-automation-wasp-drone.md) | Playwright and Puppeteer automation specialist for browser tests, scripts, traces, screenshots, browser installs, and CI reliability. | [browser-automation-stinger](skills/browser-automation-stinger/SKILL.md) |
| [chrome-chromium-wasp-drone](agents/chrome-chromium-wasp-drone.md) | Chrome DevTools Protocol and Chromium specialist for remote debugging, developer profiles, protocol inspection, source builds, and browser-engine diagnosis. | [chrome-chromium-stinger](skills/chrome-chromium-stinger/SKILL.md) |
| [lighthouse-pagespeed-wasp-drone](agents/lighthouse-pagespeed-wasp-drone.md) | Lighthouse + PageSpeed Insights specialist: running audits locally vs in CI (LHCI 0.15.x / GitHub Actions), interpreting all four audit categories (Performance, Accessibility, Best Practices, SEO; PWA removed in LH12), setting score budgets and performance budgets, authoring custom Lighthouse plugins, and navigating the lab-vs-CrUX field-data gap (including the TBT/INP limitation). | [lighthouse-pagespeed-stinger](skills/lighthouse-pagespeed-stinger/SKILL.md) |
| [webapp-capture-wasp-drone](agents/webapp-capture-wasp-drone.md) | Headless capture of live, authenticated web apps. | [webapp-capture-stinger](skills/webapp-capture-stinger/SKILL.md) |

Codex can use the named skill or its generated `source-command-<name>` wrapper where a source command exists. Home installations may expose flat commands. Use the actual selector offered by the host. A pack with no paired agents runs its standalone skills directly; a skill name does not prove that a native agent was launched.

## Prerequisites and boundaries

No extra workflow-specific pack prerequisite is declared. Tool and account requirements remain in each skill.

Core supplies shared routing and review methods. Native Codex role registration requires the explicit installed-plugin registry and trusted Core hook; a marketplace selection alone is not proof of registration. Read the linked skill before work. Missing source, browser, connector, renderer or account access is a reported gap. Installation does not authorize sending, publishing, paid work or live settings changes.
<!-- wasp-pack-guide:end -->
