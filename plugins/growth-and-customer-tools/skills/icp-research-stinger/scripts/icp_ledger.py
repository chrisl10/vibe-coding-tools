#!/usr/bin/env python3
"""Evidence ledger for ICP research: validate, merge, score, and render.

Each research lane writes JSON Lines, one evidence item per line. This script
uses only the Python standard library, makes no network calls, and writes only
the output file named with -o. Exit codes: 0 ok, 1 validation or privacy
failure, 2 usage error.

    python icp_ledger.py validate lane-*.jsonl
    python icp_ledger.py merge lane-*.jsonl -o ledger.jsonl
    python icp_ledger.py score ledger.jsonl --company-domain example.com --pretty
    python icp_ledger.py render ledger.jsonl --company-domain example.com -o evidence.md
    python icp_ledger.py --self-test
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple
from urllib.parse import urlsplit

SCHEMA_VERSION = 1
MAX_QUOTE = 400
MAX_VALUE = 200
MAX_NOTE = 1000
MAX_ITEMS = 20000
MAX_ERRORS = 1000
MAX_FILE_BYTES = 20 * 1024 * 1024

LANES = {"onsite", "customers", "market", "hiring", "voice", "news", "technographic"}
CLAIM_TYPES = {
    "industry", "employee_band", "revenue_band", "geography", "business_model",
    "company_stage", "segment", "use_case", "persona", "pain", "trigger",
    "disqualifier", "technographic", "pricing_tier", "competitor", "customer_example",
}
# Revealed signals show who actually buys; stated signals show who the company says it targets.
SIGNALS = {"stated", "revealed"}
SOURCE_TYPES = {
    "first_party", "customer_story", "customer_site", "review_site", "job_posting",
    "news", "funding_database", "directory", "partner_marketplace", "community", "other",
}
POLARITIES = {"supports", "contradicts"}
TOOLS = {"exa", "firecrawl", "websearch", "webfetch", "manual"}
REQUIRED = ("lane", "claim_type", "value", "signal", "polarity", "source_url",
            "source_type", "quote", "retrieved", "tool")
# Unknown fields are rejected so nothing (a name, a contact) rides through merge unscanned.
ALLOWED_KEYS = set(REQUIRED) | {"confidence", "note"}

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# Phone shapes, kept narrow so size bands (1001-5000), money (25 000 000), and years stay valid:
# North American 3-3-4 groups, international numbers that start with "+", and trunk-prefixed "0" numbers.
PHONE_RES = (
    re.compile(r"(?<![\d.])(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}(?![\d.])"),
    re.compile(r"(?<![\w+])\+\d{1,3}(?:[\s.-]?\(?\d{1,4}\)?){2,5}(?!\d)"),
    re.compile(r"(?<![\d.])0\d{2,4}[\s.-]\d{3,4}[\s.-]\d{3,4}(?![\d.])"),
)
# Personal profile URLs this script can recognize. It cannot recognize every person page or any name:
# the lane rules (record roles, never people) remain the primary control.
PROFILE_RE = re.compile(
    r"linkedin\.com/(?:in|pub)/|facebook\.com/profile\.php|"
    r"(?:facebook|instagram)\.com/(?!(?:company|business|pages|groups|events|p|reel|reels|explore|watch)(?![A-Za-z0-9.]))"
    r"[A-Za-z0-9.]+(?![A-Za-z0-9.])", re.IGNORECASE)
MULTI_PART_SUFFIXES = {"co.uk", "org.uk", "ac.uk", "gov.uk", "com.au", "net.au", "org.au", "co.nz",
                       "co.jp", "com.br", "com.mx", "co.in", "co.za", "com.sg", "com.hk", "com.cn"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def host_of(url: str) -> str:
    host = (urlsplit(url).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def registrable(host: str) -> str:
    """Approximate the registrable domain so jobs.x.com and blog.x.com count as one source."""
    host = host.lower().removeprefix("www.").strip(".")
    labels = host.split(".")
    if len(labels) >= 3 and ".".join(labels[-2:]) in MULTI_PART_SUFFIXES:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:]) if len(labels) >= 2 else host


def domain_of(url: str) -> str:
    return registrable(host_of(url))


def validate_item(item: Any, where: str) -> List[str]:
    errors: List[str] = []
    if not isinstance(item, dict):
        return [f"{where}: item is not an object"]
    for key in REQUIRED:
        if not isinstance(item.get(key), str) or not item[key].strip():
            errors.append(f"{where}: missing or empty '{key}'")
    unknown = sorted(set(item) - ALLOWED_KEYS)
    if unknown:
        errors.append(f"{where}: unknown fields {unknown}; only the ledger schema fields are allowed")
    if "note" in item and not isinstance(item["note"], str):
        errors.append(f"{where}: note must be a string")
    elif len(item.get("note", "")) > MAX_NOTE:
        errors.append(f"{where}: note longer than {MAX_NOTE} characters")
    if errors:
        return errors
    if len(item["value"]) > MAX_VALUE:
        # Also bounds the privacy regexes below, which are quadratic on very long input.
        return [f"{where}: value longer than {MAX_VALUE} characters; normalize it"]
    checks = (("lane", LANES), ("claim_type", CLAIM_TYPES), ("signal", SIGNALS),
              ("polarity", POLARITIES), ("source_type", SOURCE_TYPES), ("tool", TOOLS))
    for key, allowed in checks:
        if item[key] not in allowed:
            errors.append(f"{where}: {key} '{item[key]}' not in {sorted(allowed)}")
    try:
        url_ok = urlsplit(item["source_url"]).scheme in {"http", "https"} and bool(domain_of(item["source_url"]))
    except ValueError:  # e.g. "https://[bad" raises in urlsplit or .hostname
        url_ok = False
    if not url_ok:
        errors.append(f"{where}: source_url must be an absolute http(s) URL")
    if len(item["quote"]) > MAX_QUOTE:
        return errors + [f"{where}: quote longer than {MAX_QUOTE} characters; quote the minimum"]
    if len(item["source_url"]) > 2048:
        return errors + [f"{where}: source_url longer than 2048 characters"]
    if not DATE_RE.match(item["retrieved"]):
        errors.append(f"{where}: retrieved must be YYYY-MM-DD")
    else:
        try:
            date.fromisoformat(item["retrieved"])
        except ValueError:
            errors.append(f"{where}: retrieved '{item['retrieved']}' is not a real calendar date")
    conf = item.get("confidence")
    if conf is not None and (isinstance(conf, bool) or not isinstance(conf, (int, float)) or not 0 <= conf <= 1):
        errors.append(f"{where}: confidence must be a number from 0 to 1")
    # Privacy guard: the ICP is account- and role-level. Person-level data never enters the ledger.
    text = " ".join(str(item.get(k, "")) for k in ("value", "quote", "note"))
    if EMAIL_RE.search(text) or EMAIL_RE.search(item["source_url"]):
        errors.append(f"{where}: PRIVACY email address in evidence; record the role, not the person")
    if any(r.search(text) for r in PHONE_RES):
        errors.append(f"{where}: PRIVACY phone number in evidence")
    if PROFILE_RE.search(item["source_url"]) or PROFILE_RE.search(text):
        errors.append(f"{where}: PRIVACY personal profile URL; use company pages or job postings instead")
    return errors


def read_items(paths: Iterable[Path]) -> Tuple[List[Dict[str, Any]], List[str]]:
    items: List[Dict[str, Any]] = []
    errors: List[str] = []
    for path in paths:
        try:
            if not path.is_file():
                errors.append(f"{path}: not a regular file")
                continue
            if path.stat().st_size > MAX_FILE_BYTES:
                errors.append(f"{path}: larger than {MAX_FILE_BYTES} bytes")
                continue
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{path}: cannot read ({exc})")
            continue
        for number, line in enumerate(lines, 1):
            if len(errors) > MAX_ERRORS:
                errors.append(f"more than {MAX_ERRORS} errors; stopped reading")
                return items, errors
            if not line.strip():
                continue
            where = f"{path.name}:{number}"
            try:
                item = json.loads(line)
            except (json.JSONDecodeError, RecursionError) as exc:
                errors.append(f"{where}: invalid JSON ({getattr(exc, 'msg', 'too deeply nested')})")
                continue
            problems = validate_item(item, where)
            if problems:
                errors.extend(problems)
            else:
                items.append(item)
            if len(items) > MAX_ITEMS:
                errors.append(f"more than {MAX_ITEMS} items; split the run")
                return items, errors
    return items, errors


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def merge(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Drop duplicate evidence: same claim, same value, same page, same polarity."""
    seen: Dict[Tuple[str, str, str, str], Dict[str, Any]] = {}
    for item in items:
        key = (item["claim_type"], norm(item["value"]), item["source_url"].rstrip("/"), item["polarity"])
        if key not in seen or (item["signal"] == "revealed" and seen[key]["signal"] == "stated"):
            seen[key] = item
    return sorted(seen.values(), key=lambda i: (i["claim_type"], norm(i["value"]), i["source_url"]))


def grade(domains: int, source_types: int, revealed: int, contra_domains: int) -> str:
    if contra_domains and contra_domains * 2 >= domains:
        return "contested"
    if domains >= 3 and source_types >= 2 and revealed >= 1:
        return "strong"
    if domains >= 2:
        return "moderate"
    return "weak"


def own_hosts(company_domain: str) -> set:
    """Normalize --company-domain entries to bare hosts: accepts example.com, www.example.com, or a URL."""
    hosts = set()
    for entry in company_domain.split(","):
        entry = entry.strip()
        if not entry:
            continue
        host = host_of(entry if "://" in entry else "//" + entry)
        if host:
            hosts.add(host)
    return hosts


FIRST_PARTY_KEY = "(company's own domains)"


def score(items: List[Dict[str, Any]], company_domain: str = "") -> Dict[str, Any]:
    """company_domain may list several of the company's own domains, comma-separated."""
    # First-party detection uses the company's own hosts (and their subdomains), not registrable
    # domains, so a company on a shared platform (acme.webflow.io) does not claim every sibling site.
    own = own_hosts(company_domain)
    company_domain = ",".join(sorted(own))
    groups: Dict[Tuple[str, str], Dict[str, Any]] = defaultdict(lambda: {
        "value": "", "support_domains": set(), "contra_domains": set(), "source_types": set(),
        "lanes": set(), "stated": 0, "revealed": 0, "third_party": False, "urls": set(),
    })
    for item in items:
        group = groups[(item["claim_type"], norm(item["value"]))]
        group["value"] = group["value"] or item["value"].strip()
        host = host_of(item["source_url"])
        is_own_host = any(host == o or host.endswith("." + o) for o in own)
        # All of the company's own domains are one source, not several independent ones.
        dom = FIRST_PARTY_KEY if is_own_host else domain_of(item["source_url"])
        group["urls"].add(item["source_url"])
        if item["polarity"] == "contradicts":
            group["contra_domains"].add(dom)
            continue
        group["support_domains"].add(dom)
        group["source_types"].add(item["source_type"])
        group["lanes"].add(item["lane"])
        group[item["signal"]] += 1
        first_party = item["source_type"] == "first_party" or is_own_host
        if not first_party:
            group["third_party"] = True
    claims = []
    for (claim_type, _), g in groups.items():
        domains = len(g["support_domains"])
        claims.append({
            "claim_type": claim_type,
            "value": g["value"],
            "grade": grade(domains, len(g["source_types"]), g["revealed"], len(g["contra_domains"])),
            "independent_domains": domains,
            "contradicting_domains": len(g["contra_domains"]),
            "source_types": sorted(g["source_types"]),
            "lanes": sorted(g["lanes"]),
            "stated": g["stated"],
            "revealed": g["revealed"],
            "stated_only": g["revealed"] == 0,
            "first_party_only": not g["third_party"],
            "sources": len(g["urls"]),
        })
    order = {"strong": 0, "moderate": 1, "contested": 2, "weak": 3}
    claims.sort(key=lambda c: (c["claim_type"], order[c["grade"]], -c["independent_domains"], c["value"].lower()))
    lanes_seen = sorted({i["lane"] for i in items})
    return {
        "schema_version": SCHEMA_VERSION,
        "company_domain": company_domain,
        "items": len(items),
        "lanes_covered": lanes_seen,
        "lanes_missing": sorted(LANES - set(lanes_seen)),
        "claims": claims,
        "grades": {g: sum(1 for c in claims if c["grade"] == g) for g in order},
    }


def cell(text: str) -> str:
    return text.replace("|", "/").replace("\n", " ")


def render(items: List[Dict[str, Any]], scored: Dict[str, Any]) -> str:
    by_claim: Dict[Tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for item in items:
        by_claim[(item["claim_type"], norm(item["value"]))].append(item)
    out = ["# ICP evidence ledger", "",
           f"Company: {scored['company_domain'] or 'unspecified'}. Items: {scored['items']}. "
           f"Lanes covered: {', '.join(scored['lanes_covered']) or 'none'}. "
           f"Lanes missing: {', '.join(scored['lanes_missing']) or 'none'}.", "",
           "| Claim type | Value | Grade | Domains | Revealed | Stated | First-party only | Source types |",
           "|---|---|---|---|---|---|---|---|"]
    for c in scored["claims"]:
        out.append(f"| {c['claim_type']} | {cell(c['value'])} | {c['grade']} | {c['independent_domains']} | "
                   f"{c['revealed']} | {c['stated']} | {'yes' if c['first_party_only'] else 'no'} | "
                   f"{', '.join(c['source_types'])} |")
    out += ["", "## Sources by claim", ""]
    for c in scored["claims"]:
        out.append(f"### {c['claim_type']}: {cell(c['value'])} ({c['grade']})")
        for item in by_claim[(c["claim_type"], norm(c["value"]))]:
            out.append(f"- [{item['polarity']}, {item['signal']}, {item['source_type']}] "
                       f"{item['source_url']} (retrieved {item['retrieved']}, {item['tool']}): "
                       f"\"{cell(item['quote'])}\"")
        out.append("")
    return "\n".join(out)


def self_test() -> Dict[str, Any]:
    base = {"lane": "customers", "claim_type": "industry", "value": "Healthcare", "signal": "revealed",
            "polarity": "supports", "source_type": "customer_story", "quote": "Acme Health cut intake time",
            "retrieved": "2026-09-23", "tool": "exa"}
    items = [
        {**base, "source_url": "https://vendor.com/customers/acme-health"},
        {**base, "source_url": "https://www.g2.com/products/vendor/reviews", "source_type": "review_site", "lane": "voice"},
        {**base, "source_url": "https://news.example.com/a", "source_type": "news", "lane": "news", "signal": "stated"},
        {**base, "source_url": "https://vendor.com/customers/acme-health"},
        {**base, "claim_type": "employee_band", "value": "1001-5000", "signal": "stated", "lane": "onsite",
         "source_type": "first_party", "source_url": "https://vendor.com/enterprise"},
    ]
    checks: List[Tuple[str, bool]] = []
    merged = merge(items)
    checks.append(("merge dedupes identical evidence", len(merged) == 4))
    scored = score(merged, "www.vendor.com")
    health = next(c for c in scored["claims"] if c["value"] == "Healthcare")
    band = next(c for c in scored["claims"] if c["claim_type"] == "employee_band")
    checks.append(("three domains, two types, revealed grades strong", health["grade"] == "strong"))
    checks.append(("single first-party stated claim grades weak", band["grade"] == "weak" and band["first_party_only"]))
    contested = merged + [{**base, "polarity": "contradicts", "source_url": "https://x.com/1"},
                          {**base, "polarity": "contradicts", "source_url": "https://y.com/1"}]
    checks.append(("contradictions mark a claim contested",
                   next(c for c in score(contested)["claims"] if c["value"] == "Healthcare")["grade"] == "contested"))
    checks.append(("email rejected", any("PRIVACY" in e for e in validate_item(
        {**base, "source_url": "https://a.com", "quote": "contact jane@acme.com"}, "t"))))
    checks.append(("phone rejected", any("PRIVACY" in e for e in validate_item(
        {**base, "source_url": "https://a.com", "quote": "call +1 415 555 0133"}, "t"))))
    for label, quote in (("years and counts", "Since 2019, 1,200 hospitals and 350 clinics"),
                         ("size band", "1001-5000"), ("money", "ARR of 25 000 000"),
                         ("year run", "Series B 2024 2025 2026")):
        checks.append((f"{label} not mistaken for a phone", not validate_item(
            {**base, "source_url": "https://a.com", "value": quote, "quote": quote}, "t")))
    for label, quote in (("north american phone", "(415) 555-0133"), ("international phone", "+44 20 7946 0958")):
        checks.append((f"{label} rejected", any("PRIVACY" in e for e in validate_item(
            {**base, "source_url": "https://a.com", "quote": quote}, "t"))))
    subdomains = merged + [{**base, "source_url": "https://jobs.other.com/a"}, {**base, "source_url": "https://blog.other.com/b"}]
    shared = [{**base, "lane": "voice", "source_type": "review_site", "source_url": "https://reviews.webflow.io/acme"}]
    checks.append(("shared-platform sibling is not first-party",
                   not score(shared, "acme.webflow.io")["claims"][0]["first_party_only"]))
    two_sites = [{**base, "signal": "stated", "source_type": "first_party", "source_url": "https://vendor.com/"},
                 {**base, "signal": "stated", "source_type": "first_party", "source_url": "https://vendor.io/"},
                 {**base, "lane": "voice", "source_type": "review_site", "source_url": "https://reviews.example/v"}]
    own_two = score(two_sites, "https://www.vendor.com/, vendor.io")["claims"][0]
    checks.append(("company's own domains count as one source",
                   own_two["independent_domains"] == 2 and own_two["grade"] == "moderate"))
    checks.append(("subdomains of one site count once", next(
        c for c in score(subdomains)["claims"] if c["value"] == "Healthcare")["independent_domains"] == 4))
    checks.append(("profile URL rejected", any("PRIVACY" in e for e in validate_item(
        {**base, "source_url": "https://www.linkedin.com/in/jane"}, "t"))))
    for label, extra in (("facebook profile with query", {"source_url": "https://www.facebook.com/jane.doe?ref=x"}),
                         ("facebook profile.php", {"source_url": "https://facebook.com/profile.php?id=1"}),
                         ("instagram profile in a quote", {"source_url": "https://a.com", "quote": "see instagram.com/jane.doe now"}),
                         ("email in source_url", {"source_url": "https://a.com/?email=jane@acme.com"})):
        checks.append((f"{label} rejected", any("PRIVACY" in e for e in validate_item({**base, **extra}, "t"))))
    checks.append(("company social pages allowed", not validate_item(
        {**base, "source_url": "https://www.facebook.com/pages/acme", "quote": "linkedin.com/company/acme"}, "t")))
    checks.append(("unknown field rejected", bool(validate_item(
        {**base, "source_url": "https://a.com", "contact": "Jane Doe"}, "t"))))
    checks.append(("overlong value rejected", bool(validate_item(
        {**base, "source_url": "https://a.com", "value": "a" * (MAX_VALUE + 1)}, "t"))))
    checks.append(("bad enum rejected", bool(validate_item({**base, "source_url": "https://a.com", "lane": "vibes"}, "t"))))
    checks.append(("render has table row", "| industry | Healthcare | strong |" in render(merged, scored)))
    failed = [name for name, ok in checks if not ok]
    return {"schema_version": SCHEMA_VERSION, "status": "ok" if not failed else "error",
            "checks": len(checks), "failed": failed}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate, merge, score, and render ICP evidence ledgers.")
    parser.add_argument("--self-test", action="store_true", help="run deterministic in-memory checks")
    sub = parser.add_subparsers(dest="cmd")
    for name in ("validate", "merge", "score", "render"):
        p = sub.add_parser(name)
        p.add_argument("files", nargs="+", type=Path)
        p.add_argument("-o", "--out", type=Path)
        p.add_argument("--company-domain", default="", help="researched company's domain, for first-party detection")
        p.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        result = self_test()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["status"] == "ok" else 1
    if not args.cmd:
        parser.print_usage(sys.stderr)
        return 2
    items, errors = read_items(args.files)
    if errors:
        print(json.dumps({"status": "error", "error_count": len(errors), "errors": errors[:200]}, indent=2))
        return 1
    if args.cmd == "validate":
        print(json.dumps({"status": "ok", "items": len(items)}))
        return 0
    merged = merge(items)
    if args.cmd == "merge":
        if not args.out:
            print("merge requires -o", file=sys.stderr)
            return 2
        args.out.write_text("".join(json.dumps(i, sort_keys=True) + "\n" for i in merged), encoding="utf-8")
        print(json.dumps({"status": "ok", "items_in": len(items), "items_out": len(merged)}))
        return 0
    scored = score(merged, args.company_domain)
    text = json.dumps(scored, indent=2 if args.pretty else None, sort_keys=True) if args.cmd == "score" else render(merged, scored)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
