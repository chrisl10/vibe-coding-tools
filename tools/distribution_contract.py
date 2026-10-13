"""Canonical v3 census shared by source and standalone public validators.

This module deliberately has no private build or source-checkout imports.
"""

EXPECTED_PLUGINS = frozenset({
    "wasp-nest-core", "website-audit-tools", "code-audit-tools", "documentation-tools",
    "web-development-tools", "backend-and-desktop-tools", "data-and-ai-tools",
    "platform-and-release-tools", "growth-and-customer-tools", "business-and-product-tools",
    "media-and-creative-tools", "browser-and-app-testing-tools", "highlevel",
    "littlebird-toolkit", "content-intelligence", "app-primer-zero",
    "developer-learning-tools", "software-economics-tools", "infrastructure-decision-tools",
    "repository-modernization-tools", "product-studio",
})
CANONICAL_TOTALS = {"skill": 223, "agent": 184, "command": 77}
CORE_TOTALS = {"skill": 18, "agent": 14, "command": 9}
IMMUTABLE_CORE = {"get-started-stinger", "library-stinger", "knowledge-stinger",
                  "quality-stinger", "security-stinger", "github-repo-health-stinger"}
