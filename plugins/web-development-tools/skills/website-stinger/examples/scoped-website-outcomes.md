# Constructed scope cases

These are completed decision examples, not executed app tests.

## Quick local brochure
Request: three public pages for a repair shop, supplied licensed images/copy, owner edits in Git, contact via supplied email link, no tracking. Decision: one SvelteKit app with static output and local assets. Select 1, 2, 3, 12 and applicable 11 content/CTA checks; skip 5, 6, 7, 4, 8, 9, 10 with no dependent runtime integrations. No database, account screen, upload admin or fake success form. Check accepted routes in generated output and mobile/keyboard locally; mark build/browser evidence pending until observed. A later real enquiry form reopens runtime/destination decision.

## CMS for an existing public site
Request: two approved editor roles managing articles for a separate SvelteKit consumer; no customer login. Contract: Payload/Next CMS owns articles, media and editor Users. Public API includes title/slug/excerpt/public image, `_status=published` access, depth 0 and page-bound navigation. Author email is excluded. User role fields require accepted admin policy on create and update. No SaaS subscriptions/leads/app_settings copied. Public page SSR freshness and authenticated no-store preview are separate checks. Anonymous direct draft ID request must deny even if the browser omitted its normal published query. Runtime requests/build/upload/cache checks remain pending.

## Required Vue public client
Website owner implements SvelteKit public sites. Prepare independent Payload contract and CMS work if authorized; use `vue-stinger` or `nuxt-stinger` for the public site and report them as a gap if they are not selected. Do not claim a Svelte template satisfies Vue.

## New CMS drafts with a published record
Existing published title A, editor saves draft title B. Anonymous requests must return only published version A; preview requires authenticated editor context. Unpublish must remove public access and cached A. Verify direct ID, REST list, relationship expansion and preview cache separately. A front-end status filter alone fails this case.

Filled artifacts: [brochure scope](quick-brochure-scope.md), [article CMS contract](payload-article-contract.md).
