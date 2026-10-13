# Contributing to Website Audit Tools

Website Audit Tools is an optional plugin in the Wasp Nest source repository. Work from the repository root so validation can resolve Core and the other selected plugins.

## Source and ownership

```bash
git clone https://github.com/legioncodeinc/the-wasp-nest-source.git
cd the-wasp-nest-source
```

The [plugin catalog](../../plugin-catalog.json) owns package membership. Website audit procedures live in this pack's `skills/` and `agents/`; shared Core gates live under `src/`. Browser automation and Lighthouse belong to `browser-and-app-testing-tools`. The [layout guide](../../docs/PLUGIN-LAYOUT.md) explains those boundaries and the installed registry.

Read the relevant Stinger before changing its procedure. Preserve raw research captures and dated evidence. Update the paired Drone and active links when a procedure changes, and coordinate shared build, install or catalog edits with their current owner.

## Validation

From the repository root, run:

```bash
python3 scripts/validate.py
python3 scripts/check_markdown_links.py packs/website-audit-tools/README.md
python3 scripts/build.py --out /tmp/wasp-website-review --packs website-audit-tools
```

Choose a fresh output directory for a review build. The builder selects Core and Browser and App Testing automatically. These commands validate source, README links and packaging; they do not prove that a native host has installed or run the plugin. Check the other active Markdown files you changed with the link checker as well.

## Reviews and release

Keep each change focused and explain the concrete behavior and evidence in its review. Run Security, then Quality, then repository health before an authorized commit or push. Commits, pushes and publication remain explicit owner actions.

The [release process](../../docs/RELEASE-PROCESS.md) covers repository releases. Report security issues through the [security policy](SECURITY.md), without putting sensitive details into public issues.
