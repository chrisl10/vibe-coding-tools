#!/usr/bin/env python3
"""Foundation audit scanner: deterministic, read-only checks for repository health.

Emits one JSON document shaped for the Audit My Code contract 1.0 (findings,
measures, coverage) plus a per-check ledger and a facts block the Drone uses to
decide which judgment checks to run.

Safety rules (enforced in code):
  * Never writes inside the audited repository (--out inside --repo is refused).
  * Reads the repo with plain file reads and read-only git commands only.
  * With --gh, calls only `gh api --method GET` on an allowlist of paths.
  * Never prints a secret value. Env file values are never emitted; pattern hits
    are redacted to the first 4 characters plus ****.

Python 3.11+, standard library only. Sources for each check: see
references/foundation-checklist.md and references/research/distilled-foundation.md.
"""

from __future__ import annotations

import argparse
import json
import os
import stat
import re
import subprocess
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

SOURCE = "code-foundation-wasp-drone"
GUIDE = "code-foundation-stinger/guides/"
# Hardened git invocation (audit L4): the audited repository's .git/config is untrusted.
GIT = ["git", "-c", "core.fsmonitor=false", "-c", "core.hooksPath=/dev/null", "-c", "diff.external=",
       "-c", "core.pager=cat"]


def git_env() -> dict:
    return {**os.environ, "GIT_OPTIONAL_LOCKS": "0", "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0"}

MAX_READ = 1_000_000
SKIP_DIRS = {"node_modules", "vendor", "dist", "build", ".next", ".svelte-kit", "target",
             "third_party", ".venv", "venv", "__pycache__", ".git", "coverage", ".turbo"}
SOURCE_EXT = {".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".py", ".go", ".rs", ".rb", ".java",
              ".kt", ".php", ".cs", ".swift", ".c", ".cc", ".cpp", ".h", ".hpp", ".svelte", ".vue",
              ".sh", ".scala", ".ex", ".exs"}
LOCKFILES = {"package-lock.json": "npm", "npm-shrinkwrap.json": "npm", "pnpm-lock.yaml": "pnpm",
             "yarn.lock": "yarn", "bun.lock": "bun", "bun.lockb": "bun"}
SEV_ORDER = ["info", "low", "medium", "high", "critical"]

# Wasp Nest heuristics, not sourced rules. Tuned in references/measures-and-bands.md.
OVERSIZED_LINES = 1000
AGENT_FILE_LINE_TARGET = 200  # Claude Code docs: target under 200 lines

NODE_EOL_MAX_MAJOR = 20       # raw/nodejs--release-status.md: v20 and older are EOL
PY_EOL_MAX_MINOR = 9          # raw/python--version-status.md: 3.9 and older are EOL
PY_SOON_EOL_MINOR = 10        # 3.10 reaches EOL in October 2026

SECRET_PATTERNS = [
    ("aws-access-key-id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("github-fine-grained-token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{50,}\b")),
    ("stripe-live-key", re.compile(r"\b[sr]k_live_[A-Za-z0-9]{16,}\b")),
    ("slack-token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("private-key-block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY(?: BLOCK)?-----")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("anthropic-api-key", re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}\b")),
    ("openai-project-key", re.compile(r"\bsk-proj-[A-Za-z0-9_\-]{20,}\b")),
]
NPMRC_TOKEN = re.compile(r"_authToken\s*=\s*(?!\$\{)(\S+)")
PLACEHOLDER = re.compile(r"(?i)^(|replace[-_ ]?me|change[-_ ]?me|your[-_ ].*|example.*|x{3,}|<.*>|\$\{.*\}|todo|placeholder|dummy|test|localhost.*|true|false|\d+)$")
SENSITIVE_FILENAMES = re.compile(r"(?i)(^|/)(id_rsa|id_ed25519|\.netrc|\.htpasswd)$|\.(pem|p12|pfx|jks|keystore|tfstate)$")
BINARY_EXT = {".exe", ".dll", ".so", ".dylib", ".jar", ".class", ".o", ".a", ".bin", ".pyc", ".whl", ".msi"}
EXAMPLE_SUFFIX = (".example", ".sample", ".template", ".dist", ".defaults", ".tpl")


def redact(value: str) -> str:
    return value[:4] + "****" if value else "****"


class Ctx:
    def __init__(self, repo: Path):
        self.repo = repo
        self.findings: list[dict] = []
        self.checks: list[dict] = []
        self.caps: list[str] = []
        self.facts: dict = {}
        self.files: list[str] = []
        self.fileset: set[str] = set()
        self.lower: dict[str, str] = {}
        self.is_git = False
        self.lines_scanned = 0
        self.files_scanned = 0
        self.skipped: list[str] = []
        self.measures: list[dict] = []

    # ---- file helpers -------------------------------------------------
    def read(self, rel: str, limit: int = MAX_READ) -> str | None:
        p = self.repo / rel
        try:
            if p.is_symlink() or not p.is_file():
                return None
            data = p.read_bytes()[:limit]
        except OSError:
            return None
        if b"\x00" in data[:4096]:
            return None
        return data.decode("utf-8", errors="replace")

    def has(self, rel: str) -> bool:
        return rel in self.fileset

    def has_ci(self, rel: str) -> str | None:
        return self.lower.get(rel.lower())

    def find_root(self, names) -> str | None:
        for n in names:
            hit = self.lower.get(n.lower())
            if hit and "/" not in hit:
                return hit
        return None

    def ignored(self, probe: str) -> bool | None:
        if not self.is_git:
            return None
        try:
            r = subprocess.run([*GIT, "-c", "core.excludesFile=/dev/null", "check-ignore", "-q", "--no-index", probe],
                               cwd=self.repo, capture_output=True, timeout=15, env=git_env())
        except (OSError, subprocess.SubprocessError):
            return None
        if r.returncode == 0:
            return True
        if r.returncode == 1:
            return False
        return None

    # ---- ledger -------------------------------------------------------
    def check(self, cid: str, area: str, title: str, status: str, finding_id: str | None = None):
        # status: pass | fail | na | judgment
        self.checks.append({"id": cid, "area": area, "title": title, "status": status, "finding_id": finding_id})

    def finding(self, area: str, num: int, title: str, severity: str, confidence: str, locations: list[dict],
                evidence: str, why: str, remediation: str, effort: str, refs: list[str], verified_by: str,
                tags: list[str] | None = None) -> str:
        if confidence == "possible" and SEV_ORDER.index(severity) > SEV_ORDER.index("medium"):
            severity = "medium"
        fid = f"FND-{area}-{num:03d}"
        self.findings.append({
            "id": fid, "dimension": "foundation", "source": SOURCE, "title": title, "severity": severity,
            "confidence": confidence, "locations": locations, "evidence": evidence.strip()[:2500],
            "why_it_matters": why, "remediation": remediation, "effort": effort, "refs": refs,
            "verified_by": verified_by, "tags": tags or [],
        })
        return fid

    def cap(self, text: str):
        if text not in self.caps:
            self.caps.append(text)


def loc(path: str, a: int | None = None, b: int | None = None) -> dict:
    d = {"path": path}
    if a:
        d["line_start"] = a
        d["line_end"] = b or a
    return d


def strip_jsonc(text: str) -> str:
    out, i, n, in_str, esc = [], 0, len(text), False, False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True
            out.append(c)
        elif c == "/" and i + 1 < n and text[i + 1] == "/":
            while i < n and text[i] != "\n":
                i += 1
            continue
        elif c == "/" and i + 1 < n and text[i + 1] == "*":
            i += 2
            while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                i += 1
            i += 2
            continue
        else:
            out.append(c)
        i += 1
    return re.sub(r",(\s*[}\]])", r"\1", "".join(out))


def load_json(ctx: Ctx, rel: str, jsonc: bool = False):
    text = ctx.read(rel)
    if text is None:
        return None
    try:
        return json.loads(strip_jsonc(text) if jsonc else text)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
def list_files(ctx: Ctx):
    try:
        r = subprocess.run([*GIT, "ls-files", "-z"], cwd=ctx.repo, capture_output=True, timeout=60,
                           env=git_env())
        if r.returncode == 0:
            ctx.is_git = True
            ctx.files = [f for f in r.stdout.decode("utf-8", "replace").split("\0") if f]
    except (OSError, subprocess.SubprocessError):
        pass
    if not ctx.is_git:
        ctx.cap("Not a git repository (or git unavailable): file list came from a directory walk, so tracked-versus-ignored checks were skipped.")
        for root, dirs, names in os.walk(ctx.repo):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for n in names:
                ctx.files.append(os.path.relpath(os.path.join(root, n), ctx.repo).replace(os.sep, "/"))
    ctx.files = [f for f in ctx.files if (ctx.repo / f).exists()]  # drop tracked-but-deleted
    ctx.fileset = set(ctx.files)
    ctx.lower = {f.lower(): f for f in ctx.files}


def is_vendor(path: str) -> bool:
    return any(part in SKIP_DIRS for part in path.split("/")[:-1])


TEST_PATH = re.compile(r"(^|/)(tests?|__tests__|specs?|e2e|testing)(/|$)")
TEST_NAME = re.compile(r"(\.(test|spec)\.[a-z]+$)|(_test\.(go|py|rb|rs)$)|(^|/)test_[^/]*\.py$|(Tests?\.(java|kt|cs)$)|(_spec\.rb$)")


def is_test(path: str) -> bool:
    return bool(TEST_PATH.search(path) or TEST_NAME.search(path))


def analyze_sources(ctx: Ctx):
    src, tests, big = [], [], []
    for f in ctx.files:
        ext = os.path.splitext(f)[1].lower()
        if ext not in SOURCE_EXT or is_vendor(f) or f.endswith(".d.ts") or ".min." in f:
            continue
        if is_test(f):
            tests.append(f)
        else:
            src.append(f)
        try:
            st = os.lstat(ctx.repo / f)
            if not stat.S_ISREG(st.st_mode):  # symlinks, devices, fifos: never read (a link to /dev/zero never returns)
                ctx.skipped.append(f + " (symlink or not a regular file)")
                continue
            if st.st_size > 5_000_000:
                ctx.skipped.append(f + " (over 5 MB)")
                continue
            with open(ctx.repo / f, "rb") as fh:
                n = fh.read(5_000_001).count(b"\n") + 1
        except OSError:
            continue
        ctx.files_scanned += 1
        ctx.lines_scanned += n
        if n > OVERSIZED_LINES and not is_test(f):
            big.append((f, n))
    ctx.facts["source_files"] = len(src)
    ctx.facts["test_files"] = len(tests)
    ctx.facts["test_file_samples"] = tests[:5]
    ctx.facts["oversized_files"] = sorted(big, key=lambda x: -x[1])[:25]
    ctx.facts["oversized_count"] = len(big)


def detect_ecosystems(ctx: Ctx):
    eco = set()
    names = {os.path.basename(f) for f in ctx.files if not is_vendor(f)}
    if "package.json" in names:
        eco.add("node")
    if any(f.endswith((".ts", ".tsx")) and not f.endswith(".d.ts") and not is_vendor(f) for f in ctx.files):
        eco.add("typescript")
    if names & {"pyproject.toml", "setup.py", "Pipfile", "setup.cfg"} or any(re.match(r"requirements.*\.txt$", n) for n in names):
        eco.add("python")
    if "go.mod" in names:
        eco.add("go")
    if "Cargo.toml" in names:
        eco.add("rust")
    if "Gemfile" in names:
        eco.add("ruby")
    if names & {"pom.xml", "build.gradle", "build.gradle.kts"}:
        eco.add("java")
    if "composer.json" in names:
        eco.add("php")
    if any(f.endswith((".csproj", ".sln")) for f in ctx.files):
        eco.add("dotnet")
    ctx.facts["ecosystems"] = sorted(eco)
    return eco


def has_existing_code(ctx: Ctx) -> bool:
    # Mirrors scripts/mark-repo-started.py in get-started-stinger.
    ignored = {".git", ".next", ".svelte-kit", ".venv", "build", "coverage", "dist", "docs", "library",
               "node_modules", "target", "vendor", "venv"}
    manifests = {"Cargo.toml", "Gemfile", "go.mod", "mix.exs", "package.json", "pyproject.toml", "pom.xml"}
    suffixes = {".c", ".cpp", ".cs", ".go", ".html", ".java", ".js", ".jsx", ".kt", ".php", ".py", ".rb", ".rs",
                ".sh", ".svelte", ".swift", ".ts", ".tsx", ".vue"}
    for f in ctx.files:
        parts = f.split("/")
        if len(parts) == 1 and parts[0] in manifests:
            return True
        if any(p in ignored for p in parts[:-1]):
            continue
        if os.path.splitext(f)[1] in suffixes:
            return True
    return False


# ---------------------------------------------------------------------------
# LIB
def check_library(ctx: Ctx):
    ex = has_existing_code(ctx)
    ctx.facts["existing_code"] = ex
    guide = GUIDE + "01-wasp-nest-readiness.md"
    fix_lock = "Wasp Nest get-started-stinger step 7 (guides/08-first-session-onboarding.md): after the baseline and knowledge pass, run scripts/mark-repo-started.py."
    lock = ctx.read("wasp-nest.lock") if ctx.has("wasp-nest.lock") else None
    lock_state = "missing"
    lock_data = None
    if lock is None:
        fid = ctx.finding("LIB", 1, "This repository has not been set up for The Wasp Nest (no wasp-nest.lock)", "medium", "confirmed",
                          [], "wasp-nest.lock is not tracked at the repository root.",
                          "Without the setup lock, agents and teammates cannot tell whether the docs library and baseline files were put in place.",
                          fix_lock + " Run Get Started first (guides/01-initialization-workflow.md), then the lock script.", "M",
                          [guide, "get-started-stinger/guides/08-first-session-onboarding.md"],
                          "Checked the tracked file list for wasp-nest.lock at the repo root.", ["get-started:step-7"])
        ctx.check("LIB-001", "LIB", "wasp-nest.lock present", "fail", fid)
    else:
        try:
            lock_data = json.loads(lock)
            ok = isinstance(lock_data, dict) and lock_data.get("schema") == 1 and lock_data.get("playbook") == "get-started-stinger"
        except ValueError:
            ok = False
        if not ok:
            lock_state = "invalid"
            fid = ctx.finding("LIB", 7, "wasp-nest.lock exists but is not a valid Get Started record", "low", "confirmed",
                              [loc("wasp-nest.lock")], "Expected JSON with schema 1 and playbook get-started-stinger; the file did not parse or did not match.",
                              "A broken lock file hides the real setup state from agents.",
                              "Re-run the get-started verification and recreate the lock with scripts/mark-repo-started.py (it refuses to overwrite, so move the bad file aside in a fix branch first).", "S",
                              [guide], "Parsed wasp-nest.lock as JSON and compared schema and playbook fields.", ["get-started:step-7"])
            ctx.check("LIB-001", "LIB", "wasp-nest.lock present", "fail", fid)
        else:
            lock_state = "valid"
            ctx.check("LIB-001", "LIB", "wasp-nest.lock present", "pass")
            if lock_data.get("existing_code") and lock_data.get("knowledge_status") != "completed":
                fid = ctx.finding("LIB", 8, "Lock says the knowledge pass is not complete for an existing codebase", "medium", "confirmed",
                                  [loc("wasp-nest.lock")], f"knowledge_status={lock_data.get('knowledge_status')!r} with existing_code=true",
                                  "Agents will not find written explanations of how the existing code works.",
                                  "Run the knowledge-stinger playbook over the code, then record completion.", "L", [guide],
                                  "Read the lock record.", ["get-started:step-6"])
                ctx.check("LIB-008", "LIB", "Lock records a completed knowledge pass", "fail", fid)
            else:
                ctx.check("LIB-008", "LIB", "Lock records a completed knowledge pass", "pass")
    ctx.facts["lock_state"] = lock_state

    required = ["library/knowledge", "library/requirements/backlog", "library/requirements/in-work", "library/requirements/completed",
                "library/requirements/reports", "library/issues/backlog", "library/issues/in-work", "library/issues/completed", "library/notes"]
    dirs = {os.path.dirname(f) for f in ctx.files if f.startswith("library/")}
    all_dirs = set()
    for d in dirs:
        while d:
            all_dirs.add(d)
            d = os.path.dirname(d)
    has_library = any(f.startswith("library/") for f in ctx.files)
    if not has_library:
        fid = ctx.finding("LIB", 2, "There is no library/ folder for plans and knowledge docs", "medium", "confirmed", [],
                          "No tracked file lives under library/.",
                          "The Library is where requirements, issues and written knowledge live. Without it agents have nowhere authoritative to read or write.",
                          "Run get-started-stinger stage 5 (copy library/ templates, guides/01-initialization-workflow.md).", "M",
                          [guide, "get-started-stinger/guides/01-initialization-workflow.md"], "Listed tracked files under library/.", ["get-started:step-3.5"])
        ctx.check("LIB-002", "LIB", "library/ exists", "fail", fid)
        for cid, t in (("LIB-003", "Library tree complete"), ("LIB-004", "library/README.md declares schema v2"),
                       ("LIB-005", "knowledge/private has architecture, standards, contracts"),
                       ("LIB-006", "Knowledge docs exist for existing code")):
            ctx.check(cid, "LIB", t, "fail" if cid == "LIB-006" and ex else "na", fid if cid == "LIB-006" and ex else None)
        ctx.facts["library_state"] = "none"
        return
    ctx.check("LIB-002", "LIB", "library/ exists", "pass")
    missing = [d for d in required if d not in all_dirs]
    if missing:
        fid = ctx.finding("LIB", 3, "The library/ folder is missing some required sub-folders", "low", "confirmed",
                          [loc("library")], "Missing: " + ", ".join(missing),
                          "Tools that file PRDs, issue docs and notes by folder will fail or create the wrong layout.",
                          "Run get-started-stinger stage 5 to add only the missing folders (it never overwrites existing files).", "S",
                          [guide], "Compared tracked directories to the Library Schema v2 list.", ["get-started:step-3.5"])
        ctx.check("LIB-003", "LIB", "Library tree complete", "fail", fid)
    else:
        ctx.check("LIB-003", "LIB", "Library tree complete", "pass")
    readme = ctx.read("library/README.md")
    if readme is None or not re.search(r"(?i)schema version|ai_description", readme):
        fid = ctx.finding("LIB", 4, "library/README.md is missing or does not state the schema version", "low", "confirmed",
                          [loc("library/README.md")], "library/README.md absent" if readme is None else "No 'Schema version' or ai_description front matter found.",
                          "Agents use this file to learn the folder rules.", "Copy get-started-stinger/templates/library/README.md.", "S", [guide],
                          "Read the file.", ["get-started:step-3.5"])
        ctx.check("LIB-004", "LIB", "library/README.md declares schema v2", "fail", fid)
    else:
        ctx.check("LIB-004", "LIB", "library/README.md declares schema v2", "pass")
    sub = [s for s in ("architecture", "standards", "contracts") if f"library/knowledge/private/{s}" not in all_dirs]
    if sub or not ctx.has("library/knowledge/private/standards/documentation-framework.md"):
        miss = sub + ([] if ctx.has("library/knowledge/private/standards/documentation-framework.md") else ["standards/documentation-framework.md"])
        fid = ctx.finding("LIB", 5, "library/knowledge/private is missing required parts", "low", "confirmed",
                          [loc("library/knowledge/private")], "Missing: " + ", ".join(miss),
                          "The schema reference and decision-record folders are what agents consult first.",
                          "Run get-started-stinger stage 5.", "S", [guide], "Compared tracked paths to the template.", ["get-started:step-3.5"])
        ctx.check("LIB-005", "LIB", "knowledge/private has architecture, standards, contracts", "fail", fid)
    else:
        ctx.check("LIB-005", "LIB", "knowledge/private has architecture, standards, contracts", "pass")
    kdocs = [f for f in ctx.files if f.startswith("library/knowledge/") and f.endswith(".md")
             and os.path.basename(f) != "README.md" and not f.endswith("standards/documentation-framework.md")]
    ctx.facts["knowledge_doc_count"] = len(kdocs)
    if ex:
        if not kdocs:
            fid = ctx.finding("LIB", 6, "The code has no written knowledge docs yet", "medium", "confirmed",
                              [loc("library/knowledge")], "Zero Markdown files under library/knowledge/ other than README.md and the schema file.",
                              "Without docs that explain the existing code, every new agent session has to rediscover how it works.",
                              "Run the knowledge-stinger code-grounded documentation pass (get-started-stinger step 6).", "L",
                              [guide, "knowledge-stinger/SKILL.md"], "Counted knowledge docs outside README.md and the schema file.", ["get-started:step-6"])
            ctx.check("LIB-006", "LIB", "Knowledge docs exist for existing code", "fail", fid)
        else:
            ctx.check("LIB-006", "LIB", "Knowledge docs exist for existing code", "pass")
    else:
        ctx.check("LIB-006", "LIB", "Knowledge docs exist for existing code", "na")
    ok_ids = {c["id"]: c["status"] for c in ctx.checks}
    complete = lock_state == "valid" and all(ok_ids.get(i) == "pass" for i in ("LIB-003", "LIB-004", "LIB-005", "LIB-008"))
    ctx.facts["library_state"] = "complete" if complete and (not ex or kdocs) else "partial"


PLACEHOLDER_NAMES = ("default_branch|repo_url|project_name|install_command|test_command|lint_command|typecheck_command|actions_checkout_sha|"
                     "actions_setup_node_sha|codeql_action_sha|codeql_languages|codeql_schedule_cron|package_manager|package_ecosystem|node_version|"
                     "repo_admin_owner|default_owner|docs_owner|frontend_owner|backend_owner|security_email|branch_prefix|runtime_and_version|"
                     "quick_start_command|usage_example|dev_setup_commands|license_name|previous_major|latest_major|oldest_supported_major")
PLACEHOLDER_RX = re.compile(r"(?<![$\{])\{(" + PLACEHOLDER_NAMES + r")\}(?!\})")
PLACEHOLDER_RX_ROOT = re.compile(r"(?<![$\{])\{(" + PLACEHOLDER_NAMES + r"|org|repo)\}(?!\})")


def check_placeholders(ctx: Ctx):
    """LIB-009: get-started template tokens left unfilled in copied baseline files."""
    guide = GUIDE + "01-wasp-nest-readiness.md"
    root_docs = ("README.md", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md")
    cand = [f for f in ctx.files if (f in root_docs or f in (".nvmrc", ".env.example", ".editorconfig", ".gitignore")
                                      or (f.startswith(".github/") and not f.startswith(".github/scripts/"))
                                      or (f.startswith("library/") and os.path.basename(f) == "README.md"))
            and "templates/" not in f]
    hits, sev = [], "low"
    for f in cand:
        t = ctx.read(f, 300_000)
        if not t:
            continue
        rx = PLACEHOLDER_RX_ROOT if f in root_docs else PLACEHOLDER_RX
        for m in rx.finditer(t):
            hits.append((f, t.count("\n", 0, m.start()) + 1, m.group(0)))
            if f.startswith(".github/workflows/"):
                sev = "medium"
    if hits:
        fid = ctx.finding("LIB", 9, "Setup template placeholders were left unfilled", sev, "confirmed", [loc(f, ln) for f, ln, _ in hits[:10]],
                          "; ".join(f"{f}:{ln} {tok}" for f, ln, tok in hits[:12]) + (f" (and {len(hits) - 12} more)" if len(hits) > 12 else ""),
                          "Get Started promises never to leave a literal placeholder in a file it calls done. A placeholder in a workflow breaks the build; in a README it tells readers nothing.",
                          "Fill each token from the repository's real values, or remove the file. Re-run the get-started verification (guides/07-verification-checklist.md).", "S",
                          [guide, "wasp-nest--get-started-assess-map"], "Regex for the exact token names the get-started templates use, in baseline files outside templates/ folders.", ["get-started:guide-01-rule-4"])
        ctx.check("LIB-009", "LIB", "No unfilled template placeholders", "fail", fid)
    else:
        ctx.check("LIB-009", "LIB", "No unfilled template placeholders", "pass")


# ---------------------------------------------------------------------------
# AGENT
def check_agent(ctx: Ctx):
    guide = GUIDE + "01-wasp-nest-readiness.md"
    agents = "AGENTS.md" if ctx.has("AGENTS.md") else None
    claude = "CLAUDE.md" if ctx.has("CLAUDE.md") else (".claude/CLAUDE.md" if ctx.has(".claude/CLAUDE.md") else None)
    other = [f for f in ctx.files if f in (".cursorrules", ".github/copilot-instructions.md", "GEMINI.md") or f.startswith(".cursor/rules/")]
    ctx.facts["agent_files"] = [x for x in (agents, claude) if x] + other
    note = "Not created by get-started-stinger (guide 08 only installs home-level instructions). Ask the harness to draft one (Claude Code: /init) or write AGENTS.md by hand."
    if not agents and not claude:
        sev = "medium" if not other else "low"
        fid = ctx.finding("AGENT", 1, "No instructions file tells AI agents how to work in this repository", sev, "confirmed", [],
                          "No AGENTS.md, CLAUDE.md or .claude/CLAUDE.md is tracked." + (f" Other tool files present: {', '.join(other[:5])}." if other else ""),
                          "Agents start every session blind. They guess the test command and the conventions, which costs time and produces wrong edits.",
                          "Add a short AGENTS.md with build, test and lint commands, code style, and boundaries. " + note, "S",
                          [GUIDE + "01-wasp-nest-readiness.md", "agents--agents-md-spec", "claude-code--memory-claude-md"],
                          "Listed tracked files for the known instruction file names.", ["agent-readiness"])
        ctx.check("AGENT-001", "AGENT", "Agent instructions file present", "fail", fid)
        for cid, t in (("AGENT-002", "AGENTS.md and CLAUDE.md agree"), ("AGENT-003", "Instructions file is short enough"),
                       ("AGENT-004", "Instructions name build or test commands"), ("AGENT-005", "Instructions reference real paths")):
            ctx.check(cid, "AGENT", t, "na")
    else:
        ctx.check("AGENT-001", "AGENT", "Agent instructions file present", "pass")
        if agents and claude:
            ctext = ctx.read(claude) or ""
            is_link = (ctx.repo / claude).is_symlink()
            if "@AGENTS.md" not in ctext and not is_link:
                fid = ctx.finding("AGENT", 2, "AGENTS.md and CLAUDE.md both exist and are not linked", "low", "confirmed",
                                  [loc(claude), loc(agents)], "CLAUDE.md does not contain an @AGENTS.md import and is not a symlink.",
                                  "Claude Code reads only CLAUDE.md when both exist, so other agents and Claude can get different rules that drift apart.",
                                  "Put '@AGENTS.md' on the first line of CLAUDE.md and keep Claude-only notes below it.", "S",
                                  [GUIDE + "01-wasp-nest-readiness.md", "claude-code--memory-claude-md"], "Read CLAUDE.md for an import line.", ["agent-readiness"])
                ctx.check("AGENT-002", "AGENT", "AGENTS.md and CLAUDE.md agree", "fail", fid)
            else:
                ctx.check("AGENT-002", "AGENT", "AGENTS.md and CLAUDE.md agree", "pass")
        else:
            ctx.check("AGENT-002", "AGENT", "AGENTS.md and CLAUDE.md agree", "na")
        long_files, no_cmd, dead = [], [], []
        cmd_re = re.compile(r"`[^`\n]*\b(npm|pnpm|yarn|bun|npx|pytest|python3?|uv|pip|poetry|go|cargo|make|just|mvn|gradle|dotnet|bundle|rake|composer|deno)\b[^`\n]*`")
        for f in [x for x in (agents, claude) if x]:
            t = ctx.read(f) or ""
            n = t.count("\n") + 1
            if n > AGENT_FILE_LINE_TARGET:
                long_files.append((f, n))
            if not cmd_re.search(t):
                no_cmd.append(f)
            for m in re.finditer(r"`([^`\s]+)`", t):
                tok = m.group(1).rstrip(".,:;")
                if not re.fullmatch(r"[\w@.\-]+(/[\w@.\-]+)+/?|[\w\-]+\.(?:md|json|ts|tsx|js|mjs|py|yml|yaml|toml|sh)", tok):
                    continue
                if tok.startswith(("http", "~", "/", "..", "./.")) or any(c in tok for c in "*<>{}$"):
                    continue
                if re.fullmatch(r"\d+(\.\d+){3}(/\d+)?", tok):
                    continue  # IP address or CIDR block
                t2 = tok[2:] if tok.startswith("./") else tok
                t2 = t2.rstrip("/")
                if "." in os.path.basename(t2) and not os.path.splitext(t2)[1]:
                    continue
                if t2 in ctx.fileset or any(x.startswith(t2 + "/") for x in ctx.files) or (ctx.repo / t2).exists():
                    continue  # exists on disk (possibly untracked or ignored): not stale
                if re.fullmatch(r"[\w\-]+/[\w\-]+", t2) and not os.path.splitext(t2)[1]:
                    continue  # "owner/repo" or "a/b" without extension: too ambiguous
                dead.append((f, t.count("\n", 0, m.start()) + 1, t2))
        if long_files:
            fid = ctx.finding("AGENT", 3, "The agent instructions file is longer than the recommended size", "low", "confirmed",
                              [loc(f) for f, _ in long_files], "; ".join(f"{f}: {n} lines (target under {AGENT_FILE_LINE_TARGET})" for f, n in long_files),
                              "Claude Code docs say longer files cost context and reduce how well instructions are followed.",
                              "Move topic-specific rules into .claude/rules/ files with paths front matter, or into skills; keep the shared file to facts needed every session.", "S",
                              [GUIDE + "01-wasp-nest-readiness.md", "claude-code--memory-claude-md"], "Counted lines.", ["agent-readiness"])
            ctx.check("AGENT-003", "AGENT", "Instructions file is short enough", "fail", fid)
        else:
            ctx.check("AGENT-003", "AGENT", "Instructions file is short enough", "pass")
        if len(no_cmd) == len([x for x in (agents, claude) if x]):
            fid = ctx.finding("AGENT", 4, "The agent instructions never name a build, test or lint command", "low", "possible",
                              [loc(f) for f in no_cmd], "No inline code span containing a common runner (npm, pnpm, pytest, go, cargo, make and similar) was found.",
                              "Without the exact test command an agent cannot check its own work.", "Add the exact commands for install, test, lint and typecheck.", "S",
                              [GUIDE + "01-wasp-nest-readiness.md", "agents--agents-md-spec"], "Pattern match only; the Drone must read the file before relying on this.", ["agent-readiness", "needs-drone-read"])
            ctx.check("AGENT-004", "AGENT", "Instructions name build or test commands", "fail", fid)
        else:
            ctx.check("AGENT-004", "AGENT", "Instructions name build or test commands", "pass")
        if dead:
            fid = ctx.finding("AGENT", 5, "The agent instructions point at files or folders that do not exist", "low", "likely",
                              [loc(f, ln) for f, ln, _ in dead[:10]], "; ".join(f"{f}:{ln} -> {p}" for f, ln, p in dead[:10]),
                              "An instruction that points at a missing path sends the agent to the wrong place, or teaches it to ignore the file.",
                              "Update or remove each stale reference.", "S", [GUIDE + "01-wasp-nest-readiness.md", "claude-code--memory-claude-md"],
                              "Checked each backticked path against the tracked file list.", ["agent-readiness"])
            ctx.check("AGENT-005", "AGENT", "Instructions reference real paths", "fail", fid)
        else:
            ctx.check("AGENT-005", "AGENT", "Instructions reference real paths", "pass")
    big = ctx.facts.get("oversized_files", [])
    if ctx.facts.get("source_files", 0) < 3:
        ctx.check("AGENT-006", "AGENT", "Source files small enough for agents to edit", "na")
    elif big:
        fid = ctx.finding("AGENT", 6, f"{ctx.facts['oversized_count']} source file(s) are over {OVERSIZED_LINES} lines", "low", "confirmed",
                          [loc(f) for f, _ in big[:10]], "; ".join(f"{f}: {n} lines" for f, n in big[:10]),
                          "Very long files are slow and error-prone for agents and humans to edit; edits often miss context outside the window.",
                          "Split the largest files along natural seams (the bloat audit ranks them by impact).", "L",
                          [GUIDE + "01-wasp-nest-readiness.md"], "Counted newline characters in each tracked source file. The threshold is a Wasp Nest heuristic, not a published standard.", ["agent-readiness", "wasp-heuristic"])
        ctx.check("AGENT-006", "AGENT", "Source files small enough for agents to edit", "fail", fid)
    else:
        ctx.check("AGENT-006", "AGENT", "Source files small enough for agents to edit", "pass")


# ---------------------------------------------------------------------------
# CI
CI_FILES = [".gitlab-ci.yml", ".circleci/config.yml", "azure-pipelines.yml", "Jenkinsfile", "bitbucket-pipelines.yml", ".travis.yml", ".drone.yml"]
TEST_CMD = re.compile(r"\b(npm (run )?test|pnpm (run )?test|pnpm test|yarn test|bun test|vitest|jest|pytest|go test|cargo test|mvn[^\n]*\btest|gradle[^\n]*\btest|dotnet test|rspec|rake test|make test|phpunit|deno test|ctest|tox|nox)\b")
LINT_CMD = re.compile(r"\b(eslint|biome|oxlint|ruff|flake8|pylint|golangci-lint|clippy|rubocop|npm run lint|pnpm (run )?lint|yarn lint|tsc|typecheck|mypy|pyright|svelte-check)\b")
INJECT = re.compile(r"\$\{\{\s*(github\.event\.(issue\.(title|body)|pull_request\.(title|body|head\.ref|head\.label)|comment\.body|review\.body|review_comment\.body|head_commit\.message|pages\.[^}]*page_name)|github\.head_ref)\s*\}\}")
USES = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)")


def parse_workflow(text: str):
    lines = text.splitlines()
    top_perm = None
    jobs_i = None
    for i, l in enumerate(lines):
        if re.match(r"^permissions\s*:", l):
            top_perm = (i + 1, l.strip())
        if re.match(r"^jobs\s*:", l):
            jobs_i = i
    job_names, job_perm = [], 0
    if jobs_i is not None:
        for l in lines[jobs_i + 1:]:
            if re.match(r"^\S", l) and not l.startswith("#"):
                break
            if re.match(r"^  [\w\-]+\s*:\s*(#.*)?$", l):
                job_names.append(l.strip().rstrip(":"))
            if re.match(r"^    permissions\s*:", l):
                job_perm += 1
    return lines, top_perm, job_names, job_perm


def check_ci(ctx: Ctx):
    guide = GUIDE + "02-ci-tests-lint-typecheck.md"
    wfs = [f for f in ctx.files if re.match(r"\.github/workflows/[^/]+\.ya?ml$", f)]
    other_ci = [f for f in ctx.files if f in CI_FILES]
    ctx.facts["workflows"] = wfs
    ctx.facts["other_ci"] = other_ci
    if not wfs and not other_ci:
        fid = ctx.finding("CI", 1, "No automated checks run when code changes (no CI configuration found)", "medium", "confirmed", [],
                          "No .github/workflows/*.yml and none of: " + ", ".join(CI_FILES),
                          "Nothing stops a broken change from reaching the main branch unnoticed.",
                          "Add a workflow that runs install, lint, typecheck and test. Wasp Nest get-started-stinger step 3.2 ships templates/.github/workflows/ci.yml (guides/02-github-ci-setup.md).", "M",
                          [guide, "wasp-nest--get-started-assess-map"], "Listed tracked files for known CI configuration paths.", ["get-started:step-3.2"])
        ctx.check("CI-001", "CI", "CI configuration present", "fail", fid)
        for cid, t in (("CI-002", "Workflow token permissions set"), ("CI-003", "Actions pinned to commit SHAs"), ("CI-004", "No dangerous workflow patterns"),
                       ("CI-005", "CI runs the tests"), ("CI-009", "CI runs lint or typecheck"), ("CI-010", "Static analysis in CI")):
            ctx.check(cid, "CI", t, "na")
        return
    ctx.check("CI-001", "CI", "CI configuration present", "pass")
    if not wfs:
        for cid, t in (("CI-002", "Workflow token permissions set"), ("CI-003", "Actions pinned to commit SHAs"), ("CI-004", "No dangerous workflow patterns")):
            ctx.check(cid, "CI", t, "na")
        ctx.cap("CI is not GitHub Actions (" + ", ".join(other_ci) + "); workflow-file checks for token permissions, pinning and dangerous patterns were not run.")
    texts = {f: (ctx.read(f) or "") for f in wfs}
    all_ci_text = "\n".join(texts.values()) + "\n".join((ctx.read(f) or "") for f in other_ci)
    no_perm, write_all, unpinned_third, unpinned_first, danger, inject = [], [], [], [], [], []
    for f, t in texts.items():
        lines, top, jobs, jperm = parse_workflow(t)
        if top is None and not (jobs and jperm == len(jobs)):
            no_perm.append(f)
        if top and re.search(r"write-all", top[1]):
            write_all.append((f, top[0]))
        for i, l in enumerate(lines):
            m = USES.match(l)
            if m:
                ref = m.group(1)
                if ref.startswith("./") or ref.startswith("docker://") and "@sha256:" in ref:
                    continue
                if "@" not in ref:
                    continue
                name, _, sha = ref.partition("@")
                if re.fullmatch(r"[0-9a-f]{40}", sha):
                    continue
                owner = name.split("/")[0].lower()
                (unpinned_first if owner in ("actions", "github") else unpinned_third).append((f, i + 1, ref))
        if re.search(r"^\s*(pull_request_target|workflow_run)\b|\bon:\s*\[?[^\n]*(pull_request_target|workflow_run)", t, re.M):
            if re.search(r"ref:\s*[\"']?\$\{\{\s*github\.(event\.pull_request\.head|head_ref|event\.workflow_run\.head)", t):
                ln = next((i + 1 for i, l in enumerate(lines) if re.search(r"ref:\s*[\"']?\$\{\{\s*github\.(event\.pull_request\.head|head_ref|event\.workflow_run\.head)", l)), 1)
                danger.append((f, ln))
        in_run, run_indent = False, 0
        for i, l in enumerate(lines):
            rm = re.match(r"^(\s*)(?:-\s*)?run:\s*(.*)$", l)
            if rm:
                rest = rm.group(2)
                if rest.startswith(("|", ">")) or rest == "":
                    in_run, run_indent = True, len(rm.group(1))
                else:
                    in_run = False
                    if INJECT.search(rest):
                        inject.append((f, i + 1, INJECT.search(rest).group(0)))
                continue
            if in_run:
                if l.strip() and (len(l) - len(l.lstrip())) <= run_indent:
                    in_run = False
                elif INJECT.search(l):
                    inject.append((f, i + 1, INJECT.search(l).group(0)))
    if wfs:
        if no_perm or write_all:
            ev = []
            if no_perm:
                ev.append("No top-level permissions block (and not set on every job): " + ", ".join(no_perm))
            ev += [f"{f}:{ln} permissions: write-all" for f, ln in write_all]
            fid = ctx.finding("CI", 2, "Workflow tokens can write to the repository by default", "medium", "likely",
                              [loc(f) for f in no_perm] + [loc(f, ln) for f, ln in write_all], "; ".join(ev),
                              "A leaked or hijacked workflow step could change code, releases or settings. Read-only by default limits the damage.",
                              "Add 'permissions: contents: read' at the top of each workflow and grant extra scopes per job only where a step needs them.", "S",
                              [guide, "actions--secure-use", "scorecard--checks-reference"], "Parsed each workflow for a column-zero permissions key and per-job permissions.", ["get-started:step-3.2", "scorecard:Token-Permissions"])
            ctx.check("CI-002", "CI", "Workflow token permissions set", "fail", fid)
        else:
            ctx.check("CI-002", "CI", "Workflow token permissions set", "pass")
        if unpinned_third or unpinned_first:
            sev = "medium" if unpinned_third else "low"
            sample = (unpinned_third + unpinned_first)[:12]
            fid = ctx.finding("CI", 3, "Workflow actions are referenced by movable tags, not fixed commits", sev, "confirmed",
                              [loc(f, ln) for f, ln, _ in sample], f"{len(unpinned_third)} third-party and {len(unpinned_first)} GitHub-owned references not pinned to a 40-character SHA. " + "; ".join(f"{f}:{ln} {r}" for f, ln, r in sample),
                              "A moved or hijacked tag runs new code inside your pipeline with your secrets.",
                              "Pin each uses: to a full commit SHA with a version comment, and let Dependabot's github-actions ecosystem keep the pins fresh.", "S",
                              [guide, "actions--secure-use", "scorecard--checks-reference"], "Matched uses: lines and tested the ref for a 40-hex SHA.", ["get-started:step-3.2", "scorecard:Pinned-Dependencies"])
            ctx.check("CI-003", "CI", "Actions pinned to commit SHAs", "fail", fid)
        else:
            ctx.check("CI-003", "CI", "Actions pinned to commit SHAs", "pass")
        if danger or inject:
            ev = [f"{f}:{ln} privileged trigger checks out pull request head" for f, ln in danger] + [f"{f}:{ln} untrusted value inside run script: {m}" for f, ln, m in inject]
            fid = ctx.finding("CI", 4, "A workflow may run untrusted pull request input with elevated access", "high", "likely",
                              [loc(f, ln) for f, ln in danger] + [loc(f, ln) for f, ln, _ in inject], "; ".join(ev[:8]),
                              "Anyone who can open a pull request or issue could run commands in your pipeline and reach secrets.",
                              "Do not check out pull request head code under pull_request_target or workflow_run. Pass untrusted values through env: variables, never directly into run: text.", "M",
                              [guide, "actions--secure-use", "scorecard--checks-reference"],
                              "Pattern match for the privileged trigger plus head checkout, or an untrusted expression inside a run block. The Drone must read the workflow and confirm before keeping severity high.", ["scorecard:Dangerous-Workflow", "needs-drone-read"])
            ctx.check("CI-004", "CI", "No dangerous workflow patterns", "fail", fid)
        else:
            ctx.check("CI-004", "CI", "No dangerous workflow patterns", "pass")
    tf = ctx.facts.get("test_files", 0)
    if tf == 0:
        ctx.check("CI-005", "CI", "CI runs the tests", "na")
    elif not TEST_CMD.search(all_ci_text):
        fid = ctx.finding("CI", 5, "The repository has tests but CI never runs them", "medium", "likely",
                          [loc(f) for f in wfs[:5] + other_ci[:2]], f"{tf} test files tracked; no known test command found in {len(wfs) + len(other_ci)} CI file(s).",
                          "Tests that nobody runs automatically stop passing without anyone noticing.", "Add a test job (get-started-stinger ci.yml has one) that runs the repository's test command.", "S",
                          [guide, "openssf--best-practices-criteria"], "Searched all CI files for common test commands.", ["scorecard:CI-Tests", "get-started:step-3.2"])
        ctx.check("CI-005", "CI", "CI runs the tests", "fail", fid)
    else:
        ctx.check("CI-005", "CI", "CI runs the tests", "pass")
    lint_exists = ctx.facts.get("linter_config") or ctx.facts.get("tsconfig")
    if not lint_exists:
        ctx.check("CI-009", "CI", "CI runs lint or typecheck", "na")
    elif not LINT_CMD.search(all_ci_text):
        fid = ctx.finding("CI", 9, "Lint or typecheck is set up but CI does not run it", "low", "possible",
                          [loc(f) for f in wfs[:5]], "Linter or tsconfig present; no lint or typecheck command found in CI files.",
                          "Style and type errors will only be caught on someone's laptop.", "Add lint and typecheck jobs.", "S", [guide],
                          "Pattern match only; the Drone must read the CI files (a wrapper script may run them).", ["needs-drone-read"])
        ctx.check("CI-009", "CI", "CI runs lint or typecheck", "fail", fid)
    else:
        ctx.check("CI-009", "CI", "CI runs lint or typecheck", "pass")
    if re.search(r"github/codeql-action|semgrep|sonar|snyk|trivy", all_ci_text, re.I):
        ctx.check("CI-010", "CI", "Static analysis in CI", "pass")
    else:
        fid = ctx.finding("CI", 10, "No static analysis scan is configured in a workflow", "low", "possible", [],
                          "No codeql-action, semgrep, sonar, snyk or trivy reference in CI files. GitHub's native CodeQL default setup is a Settings toggle and leaves no file, so it may still be on.",
                          "Automated scanning catches common bug classes before review.", "Enable CodeQL default setup (Settings) or add get-started-stinger's codeql.yml.", "S",
                          [guide, "scorecard--checks-reference"], "Searched CI files only. Settings were not checked.", ["scorecard:SAST", "get-started:step-3.2", "needs-drone-read"])
        ctx.check("CI-010", "CI", "Static analysis in CI", "fail", fid)


# ---------------------------------------------------------------------------
# TEST, LINT
def pm_for(ctx: Ctx, pkg: dict | None) -> str:
    if pkg and isinstance(pkg.get("packageManager"), str):
        return pkg["packageManager"].split("@")[0]
    for lf, pm in LOCKFILES.items():
        if ctx.has(lf):
            return pm
    return "npm"


def check_test_lint(ctx: Ctx, eco: set[str]):
    guide = GUIDE + "02-ci-tests-lint-typecheck.md"
    pkg = load_json(ctx, "package.json") if ctx.has("package.json") else None
    scripts = pkg.get("scripts", {}) if isinstance(pkg, dict) and isinstance(pkg.get("scripts"), dict) else {}
    pm = pm_for(ctx, pkg)
    ctx.facts["package_manager"] = pm if pkg else None
    run = (lambda s: f"{pm} test" if s == "test" and pm in ("npm", "yarn", "pnpm", "bun") else f"{pm} run {s}")
    cands = {"test": [], "lint": [], "typecheck": []}
    if "test" in scripts and "no test specified" not in str(scripts["test"]):
        cands["test"].append(run("test"))
    for k, v in scripts.items():
        if re.search(r"lint|biome|eslint", k + " " + str(v), re.I) and k != "test":
            cands["lint"].append(run(k))
            break
    for k, v in scripts.items():
        if re.search(r"typecheck|type-check|check-types|tsc|svelte-check", k + " " + str(v), re.I):
            cands["typecheck"].append(run(k))
            break
    if "python" in eco:
        if any(ctx.has(x) for x in ("pytest.ini", "tox.ini", "conftest.py")) or "[tool.pytest" in (ctx.read("pyproject.toml") or "") or any(f.startswith("tests/") for f in ctx.files):
            cands["test"].append("pytest")
    if "go" in eco:
        cands["test"].append("go test ./...")
        cands["lint"].append("go vet ./...")
    if "rust" in eco:
        cands["test"].append("cargo test")
        cands["lint"].append("cargo clippy")
    mk = ctx.read("Makefile") or ""
    for tgt in ("test", "lint", "typecheck"):
        if re.search(rf"^{tgt}\s*:", mk, re.M):
            cands[tgt].append(f"make {tgt}")
    ctx.facts["commands"] = cands

    src, tf = ctx.facts.get("source_files", 0), ctx.facts.get("test_files", 0)
    if src < 3:
        for cid, t in (("TEST-001", "Tests present"), ("TEST-002", "A test command exists"), ("TEST-004", "Test to source ratio")):
            ctx.check(cid, "TEST", t, "na")
    else:
        if tf == 0:
            fid = ctx.finding("TEST", 1, "The repository has code but no tests", "medium", "confirmed", [],
                              f"{src} source files, 0 test files (looked for tests/, __tests__/, spec/, *.test.*, *.spec.*, *_test.go, test_*.py and similar).",
                              "Without tests, nobody (human or AI) can tell whether a change broke something.",
                              "Add a test runner and start with tests around the most important behavior.", "L",
                              [guide, "openssf--best-practices-criteria"], "Counted tracked files matching common test naming patterns.", ["openssf:test"])
            ctx.check("TEST-001", "TEST", "Tests present", "fail", fid)
        else:
            ctx.check("TEST-001", "TEST", "Tests present", "pass")
        if pkg is not None and "node" in eco and ctx.has("package.json"):
            t = scripts.get("test")
            if t is None or "no test specified" in str(t):
                fid = ctx.finding("TEST", 2, "npm test does not run any tests", "medium", "confirmed", [loc("package.json")],
                                  "scripts.test is " + ("missing" if t is None else repr(str(t)[:80])) + (f"; {tf} test files exist" if tf else ""),
                                  "A fresh clone has no standard way to run the tests, so CI and agents cannot verify changes.",
                                  "Add a test script that runs the project's runner (vitest, jest, node --test or similar).", "S",
                                  [guide, "npm--package-json-fields", "openssf--best-practices-criteria"], "Read package.json scripts. The placeholder-text check is a Wasp Nest heuristic.", ["openssf:test_invocation", "wasp-heuristic"])
                ctx.check("TEST-002", "TEST", "A test command exists", "fail", fid)
            else:
                ctx.check("TEST-002", "TEST", "A test command exists", "pass")
        elif cands["test"]:
            ctx.check("TEST-002", "TEST", "A test command exists", "pass")
        else:
            ctx.check("TEST-002", "TEST", "A test command exists", "judgment")
        if src >= 100 and tf / max(src, 1) < 0.03 and tf > 0:
            fid = ctx.finding("TEST", 4, "Very few test files compared with the amount of code", "low", "possible", [],
                              f"{tf} test files for {src} source files ({tf / src:.1%}).", "Large untested areas make changes risky.",
                              "Add tests around the busiest and most critical modules first.", "L", [guide], "File count ratio only; file counts say nothing about coverage depth. Wasp Nest heuristic.", ["wasp-heuristic", "needs-drone-read"])
            ctx.check("TEST-004", "TEST", "Test to source ratio", "fail", fid)
        else:
            ctx.check("TEST-004", "TEST", "Test to source ratio", "pass" if tf else "na")

    # LINT
    cfg_names = ["eslint.config.js", "eslint.config.mjs", "eslint.config.cjs", "eslint.config.ts", "biome.json", "biome.jsonc",
                 ".oxlintrc.json", ".flake8", "ruff.toml", ".ruff.toml", ".pylintrc", ".rubocop.yml", ".golangci.yml", ".golangci.yaml", "phpcs.xml", "phpstan.neon"]
    base = {os.path.basename(f): f for f in ctx.files if not is_vendor(f)}
    lint_cfg = [base[n] for n in cfg_names if n in base]
    lint_cfg += [f for f in ctx.files if re.match(r"(^|.*/)\.eslintrc(\..+)?$", f) and not is_vendor(f)]
    pyproj = ctx.read("pyproject.toml") or ""
    if re.search(r"\[tool\.(ruff|pylint|flake8)", pyproj):
        lint_cfg.append("pyproject.toml")
    if isinstance(pkg, dict) and ("eslintConfig" in pkg):
        lint_cfg.append("package.json")
    ctx.facts["linter_config"] = lint_cfg
    needs_lint = bool(eco & {"node", "python", "ruby", "php"}) and ctx.facts.get("source_files", 0) >= 3
    if not needs_lint:
        ctx.check("LINT-001", "LINT", "Linter configured", "na")
    elif not lint_cfg:
        fid = ctx.finding("LINT", 1, "No linter is configured", "low", "confirmed", [],
                          "None of: eslint config, biome, oxlint, ruff, flake8, pylint, rubocop, phpcs, phpstan found (ecosystems: " + ", ".join(sorted(eco)) + ").",
                          "A linter catches whole classes of mistakes before review and gives agents a fast self-check.",
                          "Add the ecosystem's standard linter (ESLint or Biome for JS/TS, Ruff for Python) with a lint script.", "S",
                          [guide, "openssf--best-practices-criteria"], "Looked for known config file names and pyproject tool sections.", ["openssf:warnings", "get-started:guide-05"])
        ctx.check("LINT-001", "LINT", "Linter configured", "fail", fid)
    else:
        ctx.check("LINT-001", "LINT", "Linter configured", "pass")
    tsconfigs = [f for f in ctx.files if re.match(r"(^|.*/)tsconfig(\.[\w\-]+)?\.json$", f) and not is_vendor(f)]
    ctx.facts["tsconfig"] = tsconfigs[:5]
    ts_files = [f for f in ctx.files if f.endswith((".ts", ".tsx")) and not f.endswith(".d.ts") and not is_vendor(f)]
    if not ts_files:
        for cid, t in (("LINT-002", "tsconfig present for TypeScript"), ("LINT-003", "TypeScript strict mode on")):
            ctx.check(cid, "LINT", t, "na")
    else:
        if not tsconfigs:
            fid = ctx.finding("LINT", 2, "TypeScript files exist but there is no tsconfig.json", "medium", "confirmed", [],
                              f"{len(ts_files)} .ts/.tsx files, no tsconfig*.json tracked.", "Without a tsconfig the type checker cannot run the way the editor and CI expect.",
                              "Add a tsconfig.json and a typecheck script (tsc --noEmit).", "S", [guide], "Listed tracked tsconfig files.", [])
            ctx.check("LINT-002", "LINT", "tsconfig present for TypeScript", "fail", fid)
            ctx.check("LINT-003", "LINT", "TypeScript strict mode on", "na")
        else:
            ctx.check("LINT-002", "LINT", "tsconfig present for TypeScript", "pass")
            root = "tsconfig.json" if "tsconfig.json" in tsconfigs else tsconfigs[0]
            data = load_json(ctx, root, jsonc=True)
            if not isinstance(data, dict):
                ctx.check("LINT-003", "LINT", "TypeScript strict mode on", "judgment")
                ctx.cap(f"{root} could not be parsed as JSON with comments; strict mode not evaluated.")
            elif "extends" in data and "strict" not in (data.get("compilerOptions") or {}):
                ctx.check("LINT-003", "LINT", "TypeScript strict mode on", "judgment")
            elif (data.get("compilerOptions") or {}).get("strict") is not True:
                fid = ctx.finding("LINT", 3, "TypeScript strict mode is not turned on", "low", "confirmed", [loc(root)],
                                  f"compilerOptions.strict = {(data.get('compilerOptions') or {}).get('strict')!r} in {root}",
                                  "Without strict mode the type checker lets through null mistakes and implicit any, which is where most type bugs hide.",
                                  "Set compilerOptions.strict to true and fix errors in steps (or enable per-flag).", "M", [guide],
                                  "Parsed tsconfig as JSON with comments removed. Extended configs were not followed.", [])
                ctx.check("LINT-003", "LINT", "TypeScript strict mode on", "fail", fid)
            else:
                ctx.check("LINT-003", "LINT", "TypeScript strict mode on", "pass")
    if isinstance(pkg, dict) and (lint_cfg or tsconfigs):
        miss = []
        if lint_cfg and not cands["lint"]:
            miss.append("lint")
        if tsconfigs and not cands["typecheck"]:
            miss.append("typecheck")
        if miss:
            fid = ctx.finding("LINT", 4, "package.json has no script to run " + " and ".join(miss), "low", "confirmed", [loc("package.json")],
                              "scripts: " + ", ".join(sorted(scripts)) if scripts else "package.json has no scripts.",
                              "Without a named script, contributors, CI and agents each invent their own command.", "Add 'lint' and 'typecheck' scripts.", "S",
                              [guide], "Read package.json scripts.", ["get-started:step-3.2"])
            ctx.check("LINT-004", "LINT", "Lint and typecheck scripts exist", "fail", fid)
        else:
            ctx.check("LINT-004", "LINT", "Lint and typecheck scripts exist", "pass")
    else:
        ctx.check("LINT-004", "LINT", "Lint and typecheck scripts exist", "na")
    hooks = any(ctx.has(x) or any(f.startswith(x) for f in ctx.files) for x in (".husky/", ".pre-commit-config.yaml", "lefthook.yml", ".githooks/")) or (
        isinstance(pkg, dict) and any(k in pkg for k in ("husky", "lint-staged", "simple-git-hooks")))
    if not (eco & {"node", "python"}):
        ctx.check("LINT-005", "LINT", "Pre-commit hooks configured", "na")
    elif not hooks:
        fid = ctx.finding("LINT", 5, "No pre-commit hook runs lint before each commit", "info", "confirmed", [],
                          "No .husky, lefthook.yml, .pre-commit-config.yaml, .githooks or package.json hook config.", "Hooks catch problems before they reach CI. They are optional; CI is the real gate.",
                          "Optional: add husky with lint-staged, or lefthook (get-started-stinger guide 05).", "S", [guide, "wasp-nest--get-started-assess-map"], "Listed tracked files.", ["get-started:guide-05"])
        ctx.check("LINT-005", "LINT", "Pre-commit hooks configured", "fail", fid)
    else:
        ctx.check("LINT-005", "LINT", "Pre-commit hooks configured", "pass")
    if ctx.has(".editorconfig"):
        ctx.check("LINT-007", "LINT", ".editorconfig present", "pass")
    else:
        fid = ctx.finding("LINT", 7, "No .editorconfig keeps editor settings consistent", "info", "confirmed", [], ".editorconfig is not tracked.",
                          "Mixed indentation and line endings create noisy diffs.", "Copy get-started-stinger templates/.editorconfig.", "S", [guide], "Checked tracked files.", ["get-started:step-3.1"])
        ctx.check("LINT-007", "LINT", ".editorconfig present", "fail", fid)


# ---------------------------------------------------------------------------
# DEPS
def check_deps(ctx: Ctx, eco: set[str]):
    guide = GUIDE + "03-dependencies-lockfiles-secrets.md"
    manifests = [f for f in ctx.files if os.path.basename(f) == "package.json" and not is_vendor(f) and "/fixtures/" not in f and "/examples/" not in f]
    lock_dirs = {os.path.dirname(f): os.path.basename(f) for f in ctx.files if os.path.basename(f) in LOCKFILES and not is_vendor(f)}

    def has_lock_for(d: str) -> bool:
        while True:
            if any(os.path.dirname(f) == d and os.path.basename(f) in LOCKFILES for f in ctx.files):
                return True
            if not d:
                return False
            d = os.path.dirname(d)
    missing_lock = []
    for m in manifests:
        d = os.path.dirname(m)
        pj = load_json(ctx, m) or {}
        if not (pj.get("dependencies") or pj.get("devDependencies") or pj.get("peerDependencies") or pj.get("optionalDependencies")):
            continue
        if not has_lock_for(d):
            missing_lock.append(m)
    other_missing = []
    if "go" in eco and ctx.has("go.mod") and not ctx.has("go.sum") and "require" in (ctx.read("go.mod") or ""):
        other_missing.append("go.mod (no go.sum)")
    if "ruby" in eco and ctx.has("Gemfile") and not ctx.has("Gemfile.lock"):
        other_missing.append("Gemfile (no Gemfile.lock)")
    if "php" in eco and ctx.has("composer.json") and not ctx.has("composer.lock"):
        other_missing.append("composer.json (no composer.lock)")
    py_locks = ("uv.lock", "poetry.lock", "pdm.lock", "Pipfile.lock")
    if "python" in eco and ctx.has("pyproject.toml") and not any(ctx.has(x) for x in py_locks) and not any(re.match(r"requirements.*\.txt$", os.path.basename(f)) for f in ctx.files):
        other_missing.append("pyproject.toml (no uv.lock, poetry.lock, pdm.lock or requirements file)")
    if "rust" in eco and ctx.has("Cargo.toml") and not ctx.has("Cargo.lock"):
        other_missing.append("Cargo.toml (no Cargo.lock)")
    if not manifests and not other_missing and not (eco & {"go", "ruby", "php", "python", "rust"}):
        ctx.check("DEPS-001", "DEPS", "Lockfile committed", "na")
    elif missing_lock or other_missing:
        items = missing_lock + other_missing
        fid = ctx.finding("DEPS", 1, "Dependencies are not locked to exact versions", "medium", "confirmed", [loc(x.split(" ")[0]) for x in items[:10]],
                          "Manifests without a committed lockfile: " + "; ".join(items[:10]),
                          "Each install can pull different versions, so a build that worked yesterday can break today, and a hijacked release can slip in unreviewed.",
                          "Run the package manager's install once and commit the lockfile (npm install, pnpm install, uv lock, cargo generate-lockfile). Libraries published to npm may keep the lock out of the package but should still commit it.", "S",
                          [guide, "npm--ci", "pnpm--frozen-lockfile", "uv--project-layout-lockfile"], "Checked each manifest directory and its ancestors for a lockfile.", ["scorecard:Pinned-Dependencies"])
        ctx.check("DEPS-001", "DEPS", "Lockfile committed", "fail", fid)
    else:
        ctx.check("DEPS-001", "DEPS", "Lockfile committed", "pass")
    root_locks = [f for f in ctx.files if "/" not in f and os.path.basename(f) in LOCKFILES]
    kinds = {LOCKFILES[f] for f in root_locks}
    if len(kinds) > 1:
        fid = ctx.finding("DEPS", 2, "Two package managers have each written a lockfile", "medium", "confirmed", [loc(f) for f in root_locks],
                          "Root lockfiles: " + ", ".join(root_locks), "Contributors and CI may install different versions depending on which tool they use.",
                          "Pick one package manager, delete the other lockfile, and set packageManager in package.json.", "S", [guide], "Listed root lockfiles.", [])
        ctx.check("DEPS-002", "DEPS", "One package manager", "fail", fid)
    else:
        ctx.check("DEPS-002", "DEPS", "One package manager", "pass" if root_locks else "na")
    ignored_locks = []
    if ctx.is_git:
        for lf in ("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "uv.lock", "Cargo.lock", "Gemfile.lock", "poetry.lock", "composer.lock", "go.sum"):
            if not ctx.has(lf) and ctx.ignored(lf):
                ignored_locks.append(lf)
    if ignored_locks:
        fid = ctx.finding("DEPS", 3, "A lockfile is listed in .gitignore", "medium", "confirmed", [loc(".gitignore")],
                          "git check-ignore reports these paths as ignored: " + ", ".join(ignored_locks), "Ignored lockfiles never reach the repository, so installs are unpinned.",
                          "Remove the ignore rule and commit the lockfile.", "S", [guide, "git--gitignore"], "Ran git check-ignore on each lockfile name.", [])
        ctx.check("DEPS-003", "DEPS", "Lockfile not ignored", "fail", fid)
    else:
        ctx.check("DEPS-003", "DEPS", "Lockfile not ignored", "pass" if ctx.is_git else "na")

    # DEPS-004 packageManager mismatch, DEPS-005 manifest/lock names
    pkg = load_json(ctx, "package.json") if ctx.has("package.json") else None
    mism = []
    if isinstance(pkg, dict) and isinstance(pkg.get("packageManager"), str) and root_locks:
        declared = pkg["packageManager"].split("@")[0]
        if declared not in kinds:
            mism.append(f"packageManager={pkg['packageManager']} but root lockfile is for {', '.join(sorted(kinds))}")
    if mism:
        fid = ctx.finding("DEPS", 4, "The declared package manager does not match the lockfile", "medium", "confirmed", [loc("package.json")],
                          "; ".join(mism), "Tooling such as corepack will use one tool while the lockfile belongs to another.", "Align packageManager with the lockfile, or regenerate the lock.", "S", [guide], "Compared packageManager to root lockfile names.", [])
        ctx.check("DEPS-004", "DEPS", "packageManager matches lockfile", "fail", fid)
    else:
        ctx.check("DEPS-004", "DEPS", "packageManager matches lockfile", "pass" if isinstance(pkg, dict) and root_locks else "na")
    out_of_sync = []
    if isinstance(pkg, dict) and root_locks:
        declared = set()
        for k in ("dependencies", "devDependencies", "optionalDependencies"):
            if isinstance(pkg.get(k), dict):
                declared |= set(pkg[k])
        lf = root_locks[0]
        if lf in ("package-lock.json", "npm-shrinkwrap.json"):
            lj = load_json(ctx, lf)
            if isinstance(lj, dict) and isinstance(lj.get("packages"), dict):
                root = lj["packages"].get("", {})
                locked = set((root.get("dependencies") or {})) | set((root.get("devDependencies") or {})) | set((root.get("optionalDependencies") or {}))
                out_of_sync = sorted(declared - locked)[:15]
                ctx.facts["lock_check"] = "package-lock.json root dependency names compared"
        elif lf in ("pnpm-lock.yaml", "yarn.lock", "bun.lock"):
            text = ctx.read(lf, 5_000_000) or ""
            out_of_sync = sorted(n for n in declared if n not in text)[:15]
            ctx.facts["lock_check"] = f"{lf}: declared names searched as text"
    if out_of_sync:
        fid = ctx.finding("DEPS", 5, "package.json lists dependencies that the lockfile does not contain", "medium",
                          "confirmed" if root_locks and root_locks[0].startswith("package-lock") else "likely", [loc("package.json"), loc(root_locks[0])],
                          "Declared but missing from lockfile: " + ", ".join(out_of_sync), "A clean install with npm ci or pnpm --frozen-lockfile will fail, or CI will install something different from what was reviewed.",
                          "Re-run the install to refresh the lockfile and commit it. Confirm with 'npm ci' or 'pnpm install --frozen-lockfile' in the scratch copy.", "S",
                          [guide, "npm--ci", "pnpm--frozen-lockfile"], "Compared dependency names in package.json to the lockfile. Version ranges were not compared; the scratch-copy install is the full test.", [])
        ctx.check("DEPS-005", "DEPS", "Lockfile matches manifest", "fail", fid)
    else:
        ctx.check("DEPS-005", "DEPS", "Lockfile matches manifest", "pass" if root_locks and isinstance(pkg, dict) else "na")

    # DEPS-006 automation
    renovate = [f for f in ctx.files if f in ("renovate.json", "renovate.jsonc", "renovate.json5", ".github/renovate.json", ".github/renovate.jsonc", ".github/renovate.json5",
                                             ".gitlab/renovate.json", ".gitlab/renovate.jsonc", ".gitlab/renovate.json5", ".renovaterc", ".renovaterc.json", ".renovaterc.jsonc", ".renovaterc.json5")]
    if isinstance(pkg, dict) and "renovate" in pkg:
        renovate.append("package.json")
    dep = [f for f in ctx.files if f in (".github/dependabot.yml", ".github/dependabot.yaml")]
    ctx.facts["dependency_automation"] = {"dependabot": dep, "renovate": renovate}
    has_manifest = bool(manifests or eco & {"python", "go", "rust", "ruby", "php", "java", "dotnet"} or ctx.facts.get("workflows"))
    if not has_manifest:
        ctx.check("DEPS-006", "DEPS", "Dependency update automation configured", "na")
    elif not dep and not renovate:
        fid = ctx.finding("DEPS", 6, "Nothing proposes dependency updates automatically", "medium", "confirmed", [],
                          "No .github/dependabot.yml(.yaml) and no Renovate config in any of its 14 recognized locations. (Dependabot security alerts are a separate repository setting and may still be on.)",
                          "Dependencies go stale, and known fixes arrive only when someone remembers to look.",
                          "Add .github/dependabot.yml (Wasp Nest get-started-stinger step 3.2 template: package ecosystem plus github-actions).", "S",
                          [guide, "dependabot--options-reference", "dependabot--features-overview", "renovate--config-file-locations", "scorecard--checks-reference"],
                          "Listed tracked files. Whether the Renovate app is installed cannot be seen from files.", ["scorecard:Dependency-Update-Tool", "get-started:step-3.2"])
        ctx.check("DEPS-006", "DEPS", "Dependency update automation configured", "fail", fid)
    else:
        gaps = []
        if dep:
            text = "\n".join(ctx.read(f) or "" for f in dep)
            ecos = set(re.findall(r"package-ecosystem:\s*[\"']?([\w\-]+)", text))
            want = set()
            if manifests:
                want.add("npm")
            if "python" in eco:
                want.add("pip")
            if "go" in eco:
                want.add("gomod")
            if "rust" in eco:
                want.add("cargo")
            if "ruby" in eco:
                want.add("bundler")
            if ctx.facts.get("workflows"):
                want.add("github-actions")
            if ecos:
                gaps = sorted(want - ecos - ({"pip"} if "uv" in ecos else set()))
            if not re.search(r"^version:\s*2", text, re.M):
                gaps.append("version: 2 missing")
        if gaps:
            fid = ctx.finding("DEPS", 6, "Dependabot is configured but skips part of the repository", "low", "likely", [loc(dep[0])],
                              "Ecosystems present but not configured: " + ", ".join(gaps), "Skipped ecosystems never receive update PRs.", "Add an updates entry for each missing ecosystem.", "S",
                              [guide, "dependabot--options-reference"], "Compared package-ecosystem entries to detected manifests.", ["scorecard:Dependency-Update-Tool"])
            ctx.check("DEPS-006", "DEPS", "Dependency update automation configured", "fail", fid)
        else:
            ctx.check("DEPS-006", "DEPS", "Dependency update automation configured", "pass")

    # DEPS-007 runtime pin and 008 EOL
    node_pin = [f for f in (".nvmrc", ".node-version") if ctx.has(f)]
    ts = ctx.read(".tool-versions") or ""
    mise = (ctx.read("mise.toml") or "") + (ctx.read(".mise.toml") or "")
    engines = isinstance(pkg, dict) and isinstance(pkg.get("engines"), dict) and "node" in pkg["engines"]
    volta = isinstance(pkg, dict) and "volta" in pkg
    node_pinned = bool(node_pin or re.search(r"(?m)^nodejs\s", ts) or "node" in mise or engines or volta)
    py_pinned = ctx.has(".python-version") or re.search(r"(?m)^python\s", ts) or "requires-python" in (ctx.read("pyproject.toml") or "") or ctx.has("runtime.txt") or "python_requires" in (ctx.read("setup.py") or "") or "python_version" in (ctx.read("Pipfile") or "")
    unpinned = []
    if isinstance(pkg, dict) and not node_pinned:
        unpinned.append("Node (no .nvmrc, .node-version, engines.node, .tool-versions, mise or volta)")
    if "python" in eco and not py_pinned:
        unpinned.append("Python (no .python-version, requires-python, runtime.txt or .tool-versions)")
    if not (isinstance(pkg, dict) or "python" in eco):
        ctx.check("DEPS-007", "DEPS", "Runtime version pinned", "na")
    elif unpinned:
        fid = ctx.finding("DEPS", 7, "The language runtime version is not pinned", "low", "confirmed", [],
                          "Unpinned: " + "; ".join(unpinned), "Contributors and CI can run different runtime versions, which causes 'works on my machine' failures.",
                          "Add .nvmrc (Node) or .python-version / requires-python (Python). Wasp Nest get-started-stinger step 3.1 ships .nvmrc.", "S",
                          [guide, "nvm--nvmrc", "python-packaging--pyproject-toml"], "Checked the common version-pin files.", ["get-started:step-3.1"])
        ctx.check("DEPS-007", "DEPS", "Runtime version pinned", "fail", fid)
    else:
        ctx.check("DEPS-007", "DEPS", "Runtime version pinned", "pass")
    eol = []
    for f in node_pin:
        m = re.search(r"\d+", (ctx.read(f) or "").splitlines()[0] if (ctx.read(f) or "").strip() else "")
        if m and int(m.group(0)) <= NODE_EOL_MAX_MAJOR and not (ctx.read(f) or "").strip().startswith("lts/"):
            eol.append((f, f"Node {m.group(0)}"))
    for f in [x for x in ctx.files if os.path.basename(x).lower().startswith("dockerfile") or x.lower().endswith(".dockerfile")]:
        for m in re.finditer(r"(?im)^\s*FROM\s+(?:--platform=\S+\s+)?node:(\d+)", ctx.read(f) or ""):
            if int(m.group(1)) <= NODE_EOL_MAX_MAJOR:
                eol.append((f, f"Node {m.group(1)} base image"))
    if ctx.has(".python-version"):
        m = re.match(r"\s*3\.(\d+)", ctx.read(".python-version") or "")
        if m and int(m.group(1)) <= PY_EOL_MAX_MINOR:
            eol.append((".python-version", f"Python 3.{m.group(1)}"))
    if eol:
        fid = ctx.finding("DEPS", 8, "The pinned runtime version no longer gets security fixes", "medium", "confirmed", [loc(f) for f, _ in eol],
                          "; ".join(f"{f}: {v}" for f, v in eol) + " (support status as of 2026-09-30; see references/runtime-eol-table.md)",
                          "An unsupported runtime receives no security patches.", "Move to an Active or Maintenance LTS Node line, or a supported Python version.", "M",
                          [guide, "nodejs--release-status", "python--version-status"], "Parsed the pin and compared it to the support table. Re-read the source pages before reporting if this run is later than 2026-09-30.", [])
        ctx.check("DEPS-008", "DEPS", "Runtime version still supported", "fail", fid)
    else:
        ctx.check("DEPS-008", "DEPS", "Runtime version still supported", "pass" if (node_pin or ctx.has(".python-version")) else "na")


# ---------------------------------------------------------------------------
# ENV
def check_env(ctx: Ctx, eco: set[str]):
    guide = GUIDE + "03-dependencies-lockfiles-secrets.md"
    # ENV-001 tracked env files
    tracked_env = [f for f in ctx.files if re.match(r"^(\.env(\..+)?|.*\.env)$", os.path.basename(f)) and not os.path.basename(f).lower().endswith(EXAMPLE_SUFFIX)]
    if tracked_env:
        details, populated_total = [], 0
        for f in tracked_env[:10]:
            keys = []
            for l in (ctx.read(f) or "").splitlines():
                m = re.match(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", l)
                if m:
                    v = m.group(2).strip().strip("'\"")
                    if not PLACEHOLDER.match(v):
                        keys.append(m.group(1))
            populated_total += len(keys)
            details.append(f"{f}: {len(keys)} populated key(s)" + (f" ({', '.join(keys[:8])}; values not shown)" if keys else ""))
        sev = "high" if populated_total else "low"
        fid = ctx.finding("ENV", 1, "Environment files are committed to the repository", sev, "confirmed", [loc(f) for f in tracked_env[:10]],
                          "; ".join(details), "Anything in a committed .env file is readable by everyone with repository access and stays in git history after deletion.",
                          "Remove from tracking with 'git rm --cached', add the pattern to .gitignore, rotate every real value listed, and keep a .env.example with fake values. History cleanup is handled by git-wasp-drone; secret impact is security-wasp-drone's call.", "M",
                          [guide, "git--gitignore"], "Matched tracked file names, then listed key names whose values are not placeholders. Values were not read into this report.", ["get-started:guide-04", "handoff:security-wasp-drone"])
        ctx.check("ENV-001", "ENV", "No env files committed", "fail", fid)
    else:
        ctx.check("ENV-001", "ENV", "No env files committed", "pass")
    # ignore coverage
    if not ctx.has(".gitignore") and not ctx.is_git:
        ctx.check("ENV-002", "ENV", ".gitignore present", "na")
    elif not ctx.has(".gitignore"):
        fid = ctx.finding("ENV", 2, "The repository has no .gitignore", "medium", "confirmed", [], ".gitignore is not tracked at the root.",
                          "Dependencies, build output and secret files are easy to commit by accident.", "Copy get-started-stinger templates/.gitignore (step 3.1) and extend its project-specific section.", "S",
                          [guide, "wasp-nest--get-started-assess-map"], "Checked tracked files.", ["get-started:step-3.1"])
        ctx.check("ENV-002", "ENV", ".gitignore present", "fail", fid)
    else:
        ctx.check("ENV-002", "ENV", ".gitignore present", "pass")
    probes = [(".env", "ENV-003", "secrets"), (".env.local", "ENV-003", "secrets")]
    if ctx.is_git and ctx.has(".gitignore"):
        leaks = [p for p, _, _ in probes if ctx.ignored(p) is False]
        if leaks:
            fid = ctx.finding("ENV", 3, ".gitignore does not stop .env files from being committed", "medium", "confirmed", [loc(".gitignore")],
                              "git check-ignore says these are NOT ignored: " + ", ".join(leaks), "The next 'git add .' will commit real secrets.",
                              "Add '.env', '.env.*' and '!.env.example' (in that order) to .gitignore.", "S", [guide, "git--gitignore"], "Ran git check-ignore --no-index with global excludes disabled.", ["get-started:guide-04"])
            ctx.check("ENV-003", "ENV", ".gitignore ignores .env files", "fail", fid)
        else:
            ctx.check("ENV-003", "ENV", ".gitignore ignores .env files", "pass")
        want = []
        if isinstance(load_json(ctx, "package.json") if ctx.has("package.json") else None, dict) or "node" in eco:
            want += ["node_modules/x", "dist/x", "coverage/x"]
        if "python" in eco:
            want += [".venv/x", "__pycache__/x"]
        if "rust" in eco:
            want += ["target/x"]
        gaps = [p for p in want if ctx.ignored(p) is False]
        if gaps:
            fid = ctx.finding("ENV", 4, ".gitignore misses common generated folders", "low", "confirmed", [loc(".gitignore")],
                              "Not ignored: " + ", ".join(gaps), "Generated folders add noise and sometimes leak machine-specific or secret data into commits.",
                              "Extend .gitignore (template: get-started-stinger templates/.gitignore).", "S", [guide], "Ran git check-ignore on probe paths.", ["get-started:guide-04"])
            ctx.check("ENV-004", "ENV", ".gitignore covers generated folders", "fail", fid)
        else:
            ctx.check("ENV-004", "ENV", ".gitignore covers generated folders", "pass" if want else "na")
    else:
        ctx.check("ENV-003", "ENV", ".gitignore ignores .env files", "na")
        ctx.check("ENV-004", "ENV", ".gitignore covers generated folders", "na")
    tracked_gen = [f for f in ctx.files if re.match(r"(^|.*/)(node_modules|\.venv|venv|__pycache__|\.next|dist|build)/", f)]
    if tracked_gen:
        top = sorted({re.match(r"(^|.*?/)?(node_modules|\.venv|venv|__pycache__|\.next|dist|build)/", f).group(2) for f in tracked_gen})
        sev = "medium" if any(t in ("node_modules", ".venv", "venv") for t in top) else "low"
        fid = ctx.finding("ENV", 5, "Generated or installed folders are committed", sev, "confirmed", [loc(tracked_gen[0])],
                          f"{len(tracked_gen)} tracked files under: {', '.join(top)}. First: {tracked_gen[0]}", "These folders bloat the repository and hide the real diff. Some hold compiled output that cannot be reviewed.",
                          "git rm -r --cached each folder and add it to .gitignore. (A 'build' or 'dist' folder may be intentional for some projects; check before removing.)", "S", [guide, "git--gitignore"], "Listed tracked paths.", ["scorecard:Binary-Artifacts"])
        ctx.check("ENV-005", "ENV", "No generated folders committed", "fail", fid)
    else:
        ctx.check("ENV-005", "ENV", "No generated folders committed", "pass")
    # env example
    used = {}
    for f in ctx.files:
        if os.path.splitext(f)[1].lower() not in (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".py", ".svelte", ".vue", ".go", ".rb") or is_vendor(f) or is_test(f):
            continue
        t = ctx.read(f, 300_000)
        if not t:
            continue
        for m in re.finditer(r"process\.env\.([A-Z][A-Z0-9_]+)|process\.env\[['\"]([A-Z][A-Z0-9_]+)['\"]\]|os\.environ(?:\.get)?\(?\[?['\"]([A-Z][A-Z0-9_]+)['\"]|os\.getenv\(['\"]([A-Z][A-Z0-9_]+)['\"]|import\.meta\.env\.([A-Z][A-Z0-9_]+)|os\.Getenv\(\"([A-Z][A-Z0-9_]+)\"\)", t):
            name = next(g for g in m.groups() if g)
            used.setdefault(name, f)
    for k in ("NODE_ENV", "PATH", "HOME", "CI", "PORT", "DEV", "PROD", "MODE", "SSR", "BASE_URL"):
        used.pop(k, None)
    ex_file = next((f for f in ctx.files if "/" not in f and os.path.basename(f).lower() in (".env.example", ".env.sample", ".env.template", ".env.dist")), None)
    ctx.facts["env_vars_used"] = len(used)
    if not used:
        ctx.check("ENV-007", "ENV", ".env.example documents variables", "na")
        ctx.check("ENV-008", "ENV", ".env.example matches code", "na")
    elif not ex_file:
        fid = ctx.finding("ENV", 7, "The code reads environment variables but nothing documents them", "low", "likely", [],
                          f"{len(used)} variable names read in code, e.g. {', '.join(list(used)[:8])}; no .env.example, .env.sample or .env.template.",
                          "A new contributor or agent cannot tell which settings are needed to run the app.", "Add .env.example with fake placeholder values (get-started-stinger step 3.1).", "S",
                          [guide, "wasp-nest--get-started-assess-map"], "Searched source files for env reads and listed root example files.", ["get-started:step-3.1"])
        ctx.check("ENV-007", "ENV", ".env.example documents variables", "fail", fid)
        ctx.check("ENV-008", "ENV", ".env.example matches code", "na")
    else:
        ctx.check("ENV-007", "ENV", ".env.example documents variables", "pass")
        documented = set(re.findall(r"(?m)^\s*(?:export\s+)?([A-Z][A-Z0-9_]+)\s*=", ctx.read(ex_file) or ""))
        undoc = sorted(set(used) - documented)
        if len(undoc) >= 3:
            fid = ctx.finding("ENV", 8, ".env.example is missing variables the code reads", "low", "possible", [loc(ex_file)],
                              f"{len(undoc)} read in code but not in {ex_file}: " + ", ".join(undoc[:12]), "Missing entries leave setup incomplete.", "Add the missing names with fake values.", "S", [guide],
                              "Regex over source for env reads; some names may be set by the platform. The Drone must read before keeping this.", ["needs-drone-read"])
            ctx.check("ENV-008", "ENV", ".env.example matches code", "fail", fid)
        else:
            ctx.check("ENV-008", "ENV", ".env.example matches code", "pass")
    # secret patterns
    hits, files_read = [], 0
    for f in ctx.files:
        if is_vendor(f) or os.path.basename(f) in LOCKFILES or f.endswith((".lock", ".min.js", ".map", ".svg", ".png", ".jpg", ".pdf")):
            continue
        t = ctx.read(f)
        if t is None:
            continue
        files_read += 1
        for name, rx in SECRET_PATTERNS:
            for m in rx.finditer(t):
                hits.append((f, t.count("\n", 0, m.start()) + 1, name, redact(m.group(0))))
                if len(hits) > 200:
                    break
        if os.path.basename(f) == ".npmrc":
            for m in NPMRC_TOKEN.finditer(t):
                hits.append((f, t.count("\n", 0, m.start()) + 1, "npm-auth-token", redact(m.group(1))))
    sens_files = [f for f in ctx.files if SENSITIVE_FILENAMES.search(f) and not is_vendor(f)]
    if hits:
        def sample(f):
            fl = f.lower()
            return is_test(f) or fl.endswith((".md", ".mdx", ".txt", ".rst")) or any(x in fl for x in ("/fixture", "/research/", "/references/", "/examples/", "/docs/", "example"))
        primary = [h for h in hits if not sample(h[0])]
        shown = (primary or hits)
        sev = "high" if primary else "low"
        fid = ctx.finding("ENV", 9, "Text that looks like a real secret is committed" if primary else "Documentation or test files contain secret-shaped text",
                          sev, "possible", [loc(f, ln) for f, ln, *_ in shown[:10]],
                          "; ".join(f"{f}:{ln} {n} {r}" for f, ln, n, r in shown[:10]) + (f" (and {len(hits) - 10} more in {len(set(h[0] for h in hits))} files)" if len(hits) > 10 else "")
                          + ("" if primary else " All hits are in documentation, test or example files."),
                          "A live key in git can be used by anyone who can read the repository, and stays in history after deletion.",
                          "Read each hit. If real: revoke and rotate first, then remove from the code and history. If a documentation or test sample, move to a clearly fake value.", "M",
                          [guide, "github-api--secret-scanning-overview"], "Regex pattern match only (public key formats). Values are redacted to 4 characters. The Drone must read each hit and then set confidence and severity; hand real secrets to security-wasp-drone.",
                          ["handoff:security-wasp-drone", "needs-drone-read"] + ([] if primary else ["likely-sample"]))
        ctx.check("ENV-009", "ENV", "No secret-shaped strings committed", "fail", fid)
    else:
        ctx.check("ENV-009", "ENV", "No secret-shaped strings committed", "pass")
    if sens_files:
        fid = ctx.finding("ENV", 10, "Key or credential files are committed", "high", "possible", [loc(f) for f in sens_files[:10]],
                          "Tracked file names: " + ", ".join(sens_files[:10]), "Private keys, keystores and state files often hold live credentials.",
                          "Read each file's role. Remove real keys from the repository and rotate them.", "M", [guide], "File-name match only; contents were not read.", ["handoff:security-wasp-drone", "needs-drone-read"])
        ctx.check("ENV-010", "ENV", "No key or credential files committed", "fail", fid)
    else:
        ctx.check("ENV-010", "ENV", "No key or credential files committed", "pass")
    ctx.facts["tracked_secret_files"] = len(tracked_env) + len(sens_files)


# ---------------------------------------------------------------------------
# DOCS, REPO (file-based)
def check_docs_repo(ctx: Ctx):
    guide = GUIDE + "04-repository-governance.md"
    readme = ctx.find_root(["README.md", "README", "README.rst", "README.txt", "readme.md", "README.markdown"])
    ctx.facts["readme"] = readme
    if not readme:
        fid = ctx.finding("DOCS", 1, "There is no README", "medium", "confirmed", [], "No README file at the repository root.",
                          "A README is the front door. Without it nobody knows what the project is or how to run it.",
                          "Write a README with what it is, install, run and test steps (get-started-stinger step 3.3, guides/03-readme-authoring.md).", "S",
                          [guide, "wasp-nest--get-started-assess-map"], "Looked for README variants at the root.", ["get-started:step-3.3"])
        ctx.check("DOCS-001", "DOCS", "README present", "fail", fid)
        ctx.check("DOCS-002", "DOCS", "README has install and run steps", "na")
    else:
        ctx.check("DOCS-001", "DOCS", "README present", "pass")
        t = ctx.read(readme) or ""
        nonempty = [l for l in t.splitlines() if l.strip()]
        has_head = re.search(r"(?im)^#{1,4}\s*(install|installation|getting started|quick ?start|usage|setup|set up|running|run|development|build|contributing)", t)
        has_cmd = re.search(r"(?m)^\s*(\$ )?(npm|pnpm|yarn|bun|pip3?|uv|poetry|cargo|go |make|docker|python3?|node|bundle|composer|dotnet|mvn|gradle|git clone)\b", t)
        if len(nonempty) < 8 or not (has_head or has_cmd):
            fid = ctx.finding("DOCS", 2, "The README does not explain how to install or run the project", "low", "possible", [loc(readme)],
                              f"{len(nonempty)} non-empty lines; install/usage heading found: {bool(has_head)}; shell command line found: {bool(has_cmd)}.",
                              "People and agents cannot start the project without guessing.", "Add install, run and test steps with copy-paste commands and the Node/Python version needed.", "S",
                              [guide, "wasp-nest--get-started-assess-map", "openssf--best-practices-criteria"], "Heading and command pattern match. The Drone must read the README before keeping this.", ["get-started:step-3.3", "needs-drone-read"])
            ctx.check("DOCS-002", "DOCS", "README has install and run steps", "fail", fid)
        else:
            ctx.check("DOCS-002", "DOCS", "README has install and run steps", "judgment")
    lic = [f for f in ctx.files if re.match(r"(?i)^(licen[cs]e|copying|copyright|unlicense)(\.[a-z]+)?$", f) or f.startswith("LICENSES/")]
    pj = load_json(ctx, "package.json") if ctx.has("package.json") else None
    private = isinstance(pj, dict) and (pj.get("private") is True or pj.get("license") == "UNLICENSED")
    ctx.facts["license_files"] = lic[:3]
    if lic:
        ctx.check("DOCS-004", "DOCS", "LICENSE present", "pass")
    else:
        fid = ctx.finding("DOCS", 4, "The repository has no license file", "low" if private else "medium", "confirmed", [], "No LICENSE, LICENCE, COPYING or LICENSES/ at the root." + (" package.json marks the project private or UNLICENSED." if private else ""),
                          "Without a license, others have no legal right to use or contribute to the code (default is all rights reserved)." if not private else "Private project: low impact, but a statement of ownership still helps.",
                          "Choose a license (a business decision this audit does not make) and add the file. Get-started-stinger names this as a human decision.", "S",
                          [guide, "scorecard--checks-reference"], "Looked for license file names at the root.", ["scorecard:License", "get-started:human-decision"])
        ctx.check("DOCS-004", "DOCS", "LICENSE present", "fail", fid)
    for num, name, tag, why, sev in ((5, "CONTRIBUTING.md", "step-3.4", "New contributors and agents need the branch, commit and test rules.", "low"),
                                     (6, "SECURITY.md", "step-3.4", "Without it, people who find a vulnerability do not know how to report it privately.", "low"),
                                     (7, "CHANGELOG.md", "step-3.4", "Users cannot see what changed between versions.", "info")):
        hit = ctx.find_root([name]) or ctx.has_ci(".github/" + name) or ctx.has_ci("docs/" + name)
        if hit:
            ctx.check(f"DOCS-00{num}", "DOCS", f"{name} present", "pass")
        else:
            fid = ctx.finding("DOCS", num, f"There is no {name}", sev, "confirmed", [], f"{name} not found at the root, in .github/ or in docs/.", why,
                              f"Copy and fill get-started-stinger templates/{name} ({tag}).", "S", [guide, "wasp-nest--get-started-assess-map"], "Checked tracked paths.", [f"get-started:{tag}"] + (["scorecard:Security-Policy"] if name == "SECURITY.md" else []))
            ctx.check(f"DOCS-00{num}", "DOCS", f"{name} present", "fail", fid)
    tmpl = ctx.has_ci(".github/pull_request_template.md") or any(f.lower().startswith(".github/issue_template/") for f in ctx.files) or ctx.has_ci("pull_request_template.md")
    if tmpl:
        ctx.check("DOCS-008", "DOCS", "Issue or PR templates present", "pass")
    else:
        fid = ctx.finding("DOCS", 8, "No pull request or issue templates", "info", "confirmed", [], "No .github/PULL_REQUEST_TEMPLATE.md or .github/ISSUE_TEMPLATE/ found.", "Templates make reports and reviews more consistent.",
                          "Copy get-started-stinger templates/.github/ISSUE_TEMPLATE and PULL_REQUEST_TEMPLATE.md (step 3.2).", "S", [guide], "Checked tracked paths.", ["get-started:step-3.2"])
        ctx.check("DOCS-008", "DOCS", "Issue or PR templates present", "fail", fid)

    # REPO: CODEOWNERS
    co = next((f for f in (".github/CODEOWNERS", "CODEOWNERS", "docs/CODEOWNERS") if ctx.has(f)), None)
    ctx.facts["codeowners"] = co
    if not co:
        fid = ctx.finding("REPO", 1, "No CODEOWNERS file names who reviews what", "low", "confirmed", [], "No CODEOWNERS in .github/, the root or docs/.",
                          "Review requests and ownership of risky paths are left to chance.", "Add .github/CODEOWNERS (get-started-stinger step 3.2) and turn on 'Require review from Code Owners' in a ruleset.", "S",
                          [guide, "github--codeowners"], "Checked the three supported locations.", ["get-started:step-3.2"])
        ctx.check("REPO-001", "REPO", "CODEOWNERS present", "fail", fid)
        ctx.check("REPO-002", "REPO", "CODEOWNERS valid", "na")
    else:
        ctx.check("REPO-001", "REPO", "CODEOWNERS present", "pass")
        t = ctx.read(co) or ""
        problems = []
        for i, l in enumerate(t.splitlines(), 1):
            s = l.strip()
            if not s or s.startswith("#"):
                continue
            pat = s.split()[0]
            if pat.startswith("!") or pat.startswith("\\#") or re.search(r"\[.*\]", pat):
                problems.append(f"line {i}: pattern '{pat}' uses syntax CODEOWNERS ignores (! negation, \\# escape or [ ] range)")
            if len(s.split()) < 2:
                problems.append(f"line {i}: pattern with no owner")
        if os.lstat(ctx.repo / co).st_size > 3 * 1024 * 1024:
            problems.append("file is over 3 MB and will not load")
        if not re.search(r"(?m)^/?\.github/?\S*\s+@", t):
            problems.append("does not assign an owner to .github/ (anyone could change the rules)")
        if problems:
            fid = ctx.finding("REPO", 2, "CODEOWNERS has lines that will not work", "low", "likely", [loc(co)], "; ".join(problems[:8]),
                              "Ignored lines silently remove review requirements.", "Fix each line; own /.github/ so the file cannot be quietly changed.", "S", [guide, "github--codeowners"], "Parsed each line.", ["get-started:step-3.2"])
            ctx.check("REPO-002", "REPO", "CODEOWNERS valid", "fail", fid)
        else:
            ctx.check("REPO-002", "REPO", "CODEOWNERS valid", "pass")
    # binary artifacts
    bins = [f for f in ctx.files if os.path.splitext(f)[1].lower() in BINARY_EXT and not is_vendor(f)]
    if bins:
        fid = ctx.finding("REPO", 20, "Compiled binaries are committed", "low", "possible", [loc(f) for f in bins[:10]], f"{len(bins)} tracked files with binary extensions: " + ", ".join(bins[:10]),
                          "Binaries cannot be reviewed and may be outdated or malicious.", "Build them in CI, or move to releases. If deliberate (test fixtures, vendored tools), note why in a README.", "M",
                          [guide, "scorecard--checks-reference"], "Extension match only.", ["scorecard:Binary-Artifacts", "needs-drone-read"])
        ctx.check("REPO-020", "REPO", "No committed binaries", "fail", fid)
    else:
        ctx.check("REPO-020", "REPO", "No committed binaries", "pass")
    # commit convention
    if ctx.is_git:
        try:
            r = subprocess.run([*GIT, "log", "-n", "50", "--no-merges", "--no-ext-diff", "--no-textconv", "--format=%s"], cwd=ctx.repo, capture_output=True, timeout=30, env=git_env())
            subs = [s for s in r.stdout.decode("utf-8", "replace").splitlines() if s.strip()] if r.returncode == 0 else []
        except (OSError, subprocess.SubprocessError):
            subs = []
        if len(subs) >= 10:
            rate = sum(1 for s in subs if re.match(r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([^)]+\))?!?: ", s)) / len(subs)
            ctx.facts["conventional_commit_rate"] = round(rate, 2)
            if rate < 0.5:
                fid = ctx.finding("REPO", 23, "Commit messages do not follow a recognizable convention", "info", "confirmed", [],
                                  f"{rate:.0%} of the last {len(subs)} non-merge commits match the Conventional Commits pattern.", "A consistent format makes history searchable and supports automated release notes.",
                                  "Adopt Conventional Commits (get-started-stinger guide 05) if release automation or readable history matters to the team.", "S", [guide, "wasp-nest--get-started-assess-map"], "Regex over the last 50 subjects.", ["get-started:guide-05"])
                ctx.check("REPO-023", "REPO", "Commit convention in use", "fail", fid)
            else:
                ctx.check("REPO-023", "REPO", "Commit convention in use", "pass")
        else:
            ctx.check("REPO-023", "REPO", "Commit convention in use", "na")


# ---------------------------------------------------------------------------
# GitHub (read-only)
_SEG = r"[A-Za-z0-9][\w.\-]*"  # owner or repo: never starts with a dot, so "." and ".." cannot match
GH_ALLOW = [re.compile(p) for p in (
    rf"^repos/{_SEG}/{_SEG}$",
    rf"^repos/{_SEG}/{_SEG}/branches/[^/]+/protection$",
    rf"^repos/{_SEG}/{_SEG}/rules/branches/[^/]+$",
    rf"^repos/{_SEG}/{_SEG}/rulesets$",
    rf"^repos/{_SEG}/{_SEG}/community/profile$",
    rf"^repos/{_SEG}/{_SEG}/actions/runs\?[\w=&.%\-]+$",
)]


def gh_get(path: str, timeout: int):
    if not any(rx.match(path) for rx in GH_ALLOW):
        raise ValueError("gh path not on the read-only allowlist: " + path)
    try:
        r = subprocess.run(["gh", "api", "--method", "GET", "-H", "Accept: application/vnd.github+json", path], capture_output=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError) as e:
        return None, 0, str(e)[:120]
    out = r.stdout.decode("utf-8", "replace")
    try:
        data = json.loads(out) if out.strip() else None
    except ValueError:
        data = None
    status = 200 if r.returncode == 0 else int(m.group(1)) if (m := re.search(r"HTTP (\d{3})", r.stderr.decode("utf-8", "replace") + out)) else 0
    if r.returncode != 0 and isinstance(data, dict) and str(data.get("status", "")).isdigit():
        status = int(data["status"])
    return data, status, (data.get("message") if isinstance(data, dict) else r.stderr.decode("utf-8", "replace")[:160])


def check_github(ctx: Ctx, timeout: int):
    guide = GUIDE + "04-repository-governance.md"
    gh = {"mode": "files-only"}
    ctx.facts["gh"] = gh
    remote = ""
    if ctx.is_git:
        r = subprocess.run([*GIT, "remote", "get-url", "origin"], cwd=ctx.repo, capture_output=True, timeout=10, env=git_env())
        remote = r.stdout.decode().strip() if r.returncode == 0 else ""
    m = re.search(r"github\.com[:/](" + _SEG + r")/(" + _SEG + r"?)(?:\.git)?$", remote)
    if m and (".." in m.group(1) or ".." in m.group(2) or m.group(1) in {".", ".."} or m.group(2) in {".", ".."}):
        m = None
    api_checks = ["REPO-003", "REPO-004", "REPO-005", "REPO-006", "REPO-007", "REPO-008", "REPO-009", "REPO-010", "CI-006", "CI-007"]

    def skip(reason: str):
        ctx.cap(reason)
        for c in api_checks:
            ctx.check(c, "CI" if c.startswith("CI") else "REPO", "GitHub API check", "na")
    if not m:
        return skip("No GitHub origin remote found: branch protection, community profile, repository settings and CI status checks were not run.")
    try:
        auth = subprocess.run(["gh", "auth", "status"], capture_output=True, timeout=15)
    except (OSError, subprocess.SubprocessError):
        return skip("gh CLI is not installed: branch protection, community profile, repository settings and CI status checks were not run.")
    if auth.returncode != 0:
        return skip("gh is not authenticated: branch protection, community profile, repository settings and CI status checks were not run.")
    owner, repo = m.group(1), m.group(2)
    gh.update({"mode": "gh-readonly", "owner": owner, "repo": repo})
    base = f"repos/{owner}/{repo}"
    info, st, msg = gh_get(base, timeout)
    if not isinstance(info, dict):
        return skip(f"GitHub repository call failed (HTTP {st}: {msg}); API checks skipped.")
    branch = info.get("default_branch", "main")
    gh["default_branch"] = branch
    gh["visibility"] = info.get("visibility")
    gh["permissions"] = info.get("permissions")
    q = urllib.parse.quote(branch, safe="")
    if info.get("archived"):
        fid = ctx.finding("REPO", 8, "The repository is archived", "info", "confirmed", [], "archived=true", "Archived repositories are read-only and receive no updates.", "Unarchive if work should continue.", "S", [guide], "GitHub API repo response.", [])
        ctx.check("REPO-008", "REPO", "Repository is active", "fail", fid)
    else:
        ctx.check("REPO-008", "REPO", "Repository is active", "pass")
    pushed = info.get("pushed_at")
    if pushed:
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(pushed.replace("Z", "+00:00"))).days
        gh["days_since_push"] = age
        if age > 365:
            fid = ctx.finding("REPO", 10, f"No pushes for {age} days", "info", "confirmed", [], f"pushed_at={pushed}", "A repository with no recent activity may be unmaintained (OpenSSF Maintained check looks at 90 days).",
                              "Confirm the project is intentionally dormant.", "S", [guide, "scorecard--checks-reference"], "GitHub API repo response.", ["scorecard:Maintained"])
            ctx.check("REPO-010", "REPO", "Recent activity", "fail", fid)
        else:
            ctx.check("REPO-010", "REPO", "Recent activity", "pass")
    sa = info.get("security_and_analysis")
    if isinstance(sa, dict):
        ss = (sa.get("secret_scanning") or {}).get("status")
        pp = (sa.get("secret_scanning_push_protection") or {}).get("status")
        gh["secret_scanning"], gh["push_protection"] = ss, pp
        if ss == "disabled" or pp == "disabled":
            sev = "medium" if ss == "disabled" else "low"
            fid = ctx.finding("REPO", 7, "GitHub secret scanning protection is turned off", sev, "confirmed", [], f"secret_scanning={ss}, secret_scanning_push_protection={pp}",
                              "Committed secrets will not be flagged, and pushes containing them will not be blocked.", "Enable under Settings, Advanced Security (admin action, performed by a human). See get-started-stinger guide 04.", "S",
                              [guide, "github-api--secret-scanning-overview", "wasp-nest--get-started-assess-map"], "Read security_and_analysis from the repository response.", ["get-started:guide-04"])
            ctx.check("REPO-007", "REPO", "Secret scanning enabled", "fail", fid)
        else:
            ctx.check("REPO-007", "REPO", "Secret scanning enabled", "pass")
    else:
        ctx.cap("security_and_analysis not visible to this token (needs admin); secret scanning and push protection status not assessed.")
        ctx.check("REPO-007", "REPO", "Secret scanning enabled", "na")

    prot, st1, m1 = gh_get(f"{base}/branches/{q}/protection", timeout)
    rules, st2, m2 = gh_get(f"{base}/rules/branches/{q}", timeout)
    rulesets, st3, _ = gh_get(f"{base}/rulesets", timeout)
    classic = isinstance(prot, dict) and st1 == 200
    types = {r.get("type") for r in rules} if isinstance(rules, list) else set()
    known_none = (st1 == 404 and "not protected" in str(m1).lower()) and isinstance(rules, list) and not rules
    gh["protection"] = {"classic_http": st1, "rules_http": st2, "rulesets_http": st3, "rule_types": sorted(t for t in types if t)}
    if st1 == 403 and not types:
        ctx.cap("Branch protection not readable (HTTP 403, token lacks admin); protection status not assessed.")
        for c in ("REPO-003", "REPO-004", "REPO-005", "REPO-006"):
            ctx.check(c, "REPO", "Branch protection", "na")
    elif known_none:
        fid = ctx.finding("REPO", 3, f"The default branch ({branch}) has no protection", "medium", "confirmed", [],
                          f"GET branches/{branch}/protection returned 404 'Branch not protected'; GET rules/branches/{branch} returned an empty list.",
                          "Anyone with write access can push straight to the main branch, skip review and force-push over history.",
                          "Create a ruleset on the default branch: require a pull request, require the CI checks, block force pushes, require Code Owner review (get-started-stinger guide 06; Settings action for a human).", "S",
                          [guide, "github-api--branch-protection", "github-api--rulesets-rules", "scorecard--checks-reference"], "Called the protection and rules endpoints (read-only GET).", ["scorecard:Branch-Protection", "get-started:guide-06"])
        ctx.check("REPO-003", "REPO", "Default branch protected", "fail", fid)
        for c in ("REPO-004", "REPO-005", "REPO-006"):
            ctx.check(c, "REPO", "Branch protection detail", "na")
    else:
        ctx.check("REPO-003", "REPO", "Default branch protected", "pass")
        pr = (classic and prot.get("required_pull_request_reviews") is not None) or "pull_request" in types
        checks = (classic and prot.get("required_status_checks") is not None) or "required_status_checks" in types
        force_blocked = (classic and (prot.get("allow_force_pushes") or {}).get("enabled") is False) or "non_fast_forward" in types
        co_review = bool(classic and (prot.get("required_pull_request_reviews") or {}).get("require_code_owner_reviews"))
        if isinstance(rules, list):
            for r in rules:
                if r.get("type") == "pull_request" and (r.get("parameters") or {}).get("require_code_owner_review"):
                    co_review = True
        gh["protection"].update({"requires_pr": bool(pr), "requires_checks": bool(checks), "blocks_force_push": bool(force_blocked), "requires_code_owner_review": co_review})
        for num, ok, title, sev, why, fix in (
                (4, force_blocked, "Force pushes are allowed on the default branch", "medium", "History can be rewritten, which can hide or destroy reviewed work.", "Enable 'Block force pushes' in the ruleset."),
                (5, pr, "Changes can be pushed to the default branch without a pull request", "low", "Changes skip review.", "Require a pull request before merging."),
                (6, checks, "CI checks are not required before merging", "low", "A failing build can still be merged.", "Require the CI jobs as status checks.")):
            if ok:
                ctx.check(f"REPO-00{num}", "REPO", title, "pass")
            else:
                fid = ctx.finding("REPO", num, title, sev, "confirmed", [], f"Protection is present but requires_pr={bool(pr)}, requires_checks={bool(checks)}, blocks_force_push={bool(force_blocked)}.", why, fix, "S",
                                  [guide, "github-api--branch-protection", "github-api--rulesets-rules"], "Combined classic protection and rules endpoint output.", ["get-started:guide-06", "scorecard:Branch-Protection"])
                ctx.check(f"REPO-00{num}", "REPO", title, "fail", fid)
        if ctx.facts.get("codeowners") and not co_review:
            fid = ctx.finding("REPO", 11, "CODEOWNERS exists but Code Owner review is not required", "low", "confirmed", [loc(ctx.facts["codeowners"])], "No require_code_owner_reviews / require_code_owner_review found in protection or rules.",
                              "The CODEOWNERS file has no effect on merges until review by owners is required.", "Turn on 'Require review from Code Owners' in the ruleset.", "S", [guide, "github--codeowners"], "Read protection and rules output.", ["get-started:guide-06"])
            ctx.check("REPO-011", "REPO", "Code Owner review required", "fail", fid)
        elif ctx.facts.get("codeowners"):
            ctx.check("REPO-011", "REPO", "Code Owner review required", "pass")
    cp, st4, _ = gh_get(f"{base}/community/profile", timeout)
    if isinstance(cp, dict) and "health_percentage" in cp:
        gh["health_percentage"] = cp["health_percentage"]
        missing = [k for k, v in (cp.get("files") or {}).items() if v is None]
        if cp["health_percentage"] < 100:
            fid = ctx.finding("REPO", 9, f"GitHub community profile is {cp['health_percentage']} percent complete", "info", "confirmed", [], "Missing per GitHub: " + ", ".join(missing),
                              "GitHub's own checklist for a healthy public repository is incomplete.", "Add the missing files (code of conduct is not in the Wasp Nest template set).", "S", [guide, "github-api--community-profile"], "GitHub community profile API.", ["get-started:verification"])
            ctx.check("REPO-009", "REPO", "Community profile complete", "fail", fid)
        else:
            ctx.check("REPO-009", "REPO", "Community profile complete", "pass")
    else:
        ctx.check("REPO-009", "REPO", "Community profile complete", "na")
    runs, st5, m5 = gh_get(f"{base}/actions/runs?branch={q}&status=completed&exclude_pull_requests=true&per_page=10", timeout)
    if isinstance(runs, dict) and isinstance(runs.get("workflow_runs"), list):
        wr = runs["workflow_runs"]
        gh["recent_runs"] = [{"conclusion": r.get("conclusion"), "name": r.get("name"), "created_at": r.get("created_at"), "url": r.get("html_url")} for r in wr[:10]]
        if not wr:
            if ctx.facts.get("workflows"):
                fid = ctx.finding("CI", 7, "Workflows exist but none has completed on the default branch", "low", "possible", [], f"No completed runs for branch {branch} (exclude pull requests).",
                                  "CI may never have run, or workflows may only trigger on pull requests.", "Check triggers; run once on the default branch.", "S", [guide, "github-api--workflow-runs"], "Actions runs API.", ["needs-drone-read"])
                ctx.check("CI-007", "CI", "CI has run on the default branch", "fail", fid)
            else:
                ctx.check("CI-007", "CI", "CI has run on the default branch", "na")
            ctx.check("CI-006", "CI", "CI green on default branch", "na")
        else:
            ctx.check("CI-007", "CI", "CI has run on the default branch", "pass")
            concl = [r.get("conclusion") for r in wr]
            gh["latest_conclusion"] = concl[0]
            if concl[0] in ("failure", "timed_out", "startup_failure"):
                streak = next((i for i, c in enumerate(concl) if c not in ("failure", "timed_out", "startup_failure")), len(concl))
                sev = "high" if streak >= 5 else "medium"
                fid = ctx.finding("CI", 6, "The latest automated build on the default branch is failing", sev, "confirmed", [], f"Latest completed runs on {branch}: " + ", ".join(str(c) for c in concl[:10]) + f" (failing streak {streak}). Newest: {wr[0].get('html_url')}",
                                  "A red main branch means every new change starts from a broken base, and failures hide new ones.", "Open the failing run, fix or revert the cause, and keep main green.", "M",
                                  [guide, "github-api--workflow-runs", "openssf--best-practices-criteria"], "Actions runs API, completed runs on the default branch, pull request runs excluded.", ["openssf:test_continuous_integration"])
                ctx.check("CI-006", "CI", "CI green on default branch", "fail", fid)
            else:
                ctx.check("CI-006", "CI", "CI green on default branch", "pass")
    else:
        ctx.cap(f"Actions runs not readable (HTTP {st5}: {m5}); CI status on the default branch not assessed.")
        ctx.check("CI-006", "CI", "CI green on default branch", "na")
        ctx.check("CI-007", "CI", "CI has run on the default branch", "na")


# ---------------------------------------------------------------------------
def build_measures(ctx: Ctx):
    cs = ctx.checks
    passed = sum(1 for c in cs if c["status"] == "pass")
    failed = sum(1 for c in cs if c["status"] == "fail")
    rate = round(100 * passed / (passed + failed), 1) if passed + failed else None

    def band_rate(v):
        return "not-run" if v is None else "healthy" if v >= 85 else "moderate" if v >= 70 else "at-risk" if v >= 50 else "critical"
    M = ctx.measures
    M.append({"key": "checklist_pass_rate", "label": "Foundation checklist pass rate", "value": rate, "unit": "%", "band": band_rate(rate),
              "threshold": ">=85% healthy, 70-84.9 moderate, 50-69.9 at-risk, <50 critical", "source": f"foundation_scan.py ({passed} passed, {failed} failed, judgment and n/a checks excluded)"})
    agent = [c for c in cs if c["area"] == "AGENT" and c["status"] in ("pass", "fail")]
    ar = round(100 * sum(1 for c in agent if c["status"] == "pass") / len(agent), 1) if agent else None
    M.append({"key": "agent_readiness", "label": "AI agent readiness (agent file, size, commands, paths, file sizes)", "value": ar, "unit": "%", "band": band_rate(ar),
              "threshold": "same bands as checklist pass rate", "source": "foundation_scan.py AGENT checks"})
    tf = ctx.facts.get("test_files", 0)
    src = ctx.facts.get("source_files", 0)
    M.append({"key": "tests_present", "label": "Tests present", "value": "yes" if tf else ("no" if src >= 3 else "n/a"), "unit": "yes/no",
              "band": "healthy" if tf else ("at-risk" if src >= 3 else "not-run"), "threshold": "any test file = healthy; none with 3+ source files = at-risk",
              "source": f"foundation_scan.py ({tf} test files, {src} source files)"})
    M.append({"key": "tests_passing", "label": "Tests passing (run in the scratch copy)", "value": "not-run", "unit": "%", "band": "not-run",
              "threshold": "100% healthy, 95-99.9 moderate, 80-94.9 at-risk, <80 critical, did not run = not-run with a cap", "source": "Drone fills this from run_in_copy.py output"})
    has_ci = any(c["id"] == "CI-001" and c["status"] == "pass" for c in cs)
    M.append({"key": "ci_present", "label": "CI configuration present", "value": "yes" if has_ci else "no", "unit": "yes/no", "band": "healthy" if has_ci else "at-risk",
              "threshold": "present = healthy, absent = at-risk", "source": "foundation_scan.py"})
    gh = ctx.facts.get("gh", {})
    lc = gh.get("latest_conclusion")
    recent = [r["conclusion"] for r in gh.get("recent_runs", [])]
    if gh.get("mode") != "gh-readonly" or not recent:
        ci_val, ci_band = "unknown", "not-run"
    elif lc == "success" and all(c == "success" for c in recent[:5]):
        ci_val, ci_band = "green", "healthy"
    elif lc == "success":
        ci_val, ci_band = "green, recent failures", "moderate"
    else:
        streak = next((i for i, c in enumerate(recent) if c not in ("failure", "timed_out", "startup_failure")), len(recent))
        ci_val, ci_band = f"red ({streak} failing)", "critical" if streak >= 5 else "at-risk"
    M.append({"key": "ci_green_default_branch", "label": "CI result on the default branch", "value": ci_val, "unit": "status", "band": ci_band,
              "threshold": "latest and last 5 succeed = healthy; latest ok but earlier failures = moderate; latest fails = at-risk; 5 straight failures = critical",
              "source": "gh api actions/runs (read-only)" if ci_band != "not-run" else "not available (see caps)"})
    ls = ctx.facts.get("library_state", "none")
    M.append({"key": "library_initialized", "label": "Wasp Nest Library initialized", "value": {"complete": "yes", "partial": "partial", "none": "no"}[ls], "unit": "yes/partial/no",
              "band": {"complete": "healthy", "partial": "moderate", "none": "at-risk"}[ls], "threshold": "valid lock plus full library tree plus knowledge docs when code exists = yes; some = partial; none = no", "source": "foundation_scan.py LIB checks"})
    lk = [c for c in cs if c["id"] in ("DEPS-001", "DEPS-005", "DEPS-003") and c["status"] in ("pass", "fail")]
    M.append({"key": "lockfile_consistent", "label": "Lockfile committed and consistent", "value": ("yes" if lk and all(c["status"] == "pass" for c in lk) else "no") if lk else "n/a", "unit": "yes/no",
              "band": ("healthy" if lk and all(c["status"] == "pass" for c in lk) else "at-risk") if lk else "not-run", "threshold": "committed, not ignored, names match manifest = healthy", "source": "foundation_scan.py DEPS-001/003/005"})
    da = ctx.facts.get("dependency_automation", {})
    has_auto = bool(da.get("dependabot") or da.get("renovate"))
    M.append({"key": "dependency_automation", "label": "Dependency update automation configured", "value": "yes" if has_auto else "no", "unit": "yes/no", "band": "healthy" if has_auto else "moderate",
              "threshold": "Dependabot or Renovate config present = healthy", "source": "foundation_scan.py DEPS-006"})
    n = ctx.facts.get("tracked_secret_files", 0)
    M.append({"key": "committed_secret_files", "label": "Committed env or credential files", "value": n, "unit": "files", "band": "healthy" if n == 0 else "at-risk",
              "threshold": "0 healthy, 1 or more at-risk; the Drone sets critical only after confirming a live secret", "source": "foundation_scan.py ENV-001/010"})
    pr = gh.get("protection")
    if gh.get("mode") != "gh-readonly" or pr is None:
        bp_val, bp_band = "unknown", "not-run"
    elif any(c["id"] == "REPO-003" and c["status"] == "fail" for c in cs):
        bp_val, bp_band = "none", "at-risk"
    elif any(c["id"] in ("REPO-004", "REPO-005", "REPO-006") and c["status"] == "fail" for c in cs):
        bp_val, bp_band = "partial", "moderate"
    elif any(c["id"] == "REPO-003" and c["status"] == "pass" for c in cs):
        bp_val, bp_band = "protected", "healthy"
    else:
        bp_val, bp_band = "unknown", "not-run"
    M.append({"key": "branch_protection", "label": "Default branch protection", "value": bp_val, "unit": "status", "band": bp_band,
              "threshold": "PR + checks + no force push = healthy; some = moderate; none = at-risk; unreadable = not-run", "source": "gh api branches and rules (read-only)" if bp_band != "not-run" else "not available (see caps)"})
    big = ctx.facts.get("oversized_count", 0)
    M.append({"key": "oversized_source_files", "label": f"Source files over {OVERSIZED_LINES} lines", "value": big, "unit": "files",
              "band": "healthy" if big <= 2 else "moderate" if big <= 10 else "at-risk", "threshold": "<=2 healthy, 3-10 moderate, >10 at-risk (Wasp Nest heuristic)", "source": "foundation_scan.py AGENT-006"})
    loc_sc = [c for c in cs if c["id"] in ("CI-002", "CI-003", "CI-004", "DEPS-006", "DOCS-004", "DOCS-006", "REPO-020", "REPO-003") and c["status"] in ("pass", "fail")]
    sr = round(100 * sum(1 for c in loc_sc if c["status"] == "pass") / len(loc_sc), 1) if loc_sc else None
    M.append({"key": "scorecard_aligned_pass_rate", "label": "OpenSSF Scorecard aligned checks passed (Token-Permissions, Pinned-Dependencies, Dangerous-Workflow, Dependency-Update-Tool, License, Security-Policy, Binary-Artifacts, Branch-Protection)",
              "value": sr, "unit": "%", "band": band_rate(sr), "threshold": "same bands as checklist pass rate; this is an approximation, not an official Scorecard score", "source": "foundation_scan.py"})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True, type=Path, help="audited repository root (read only)")
    ap.add_argument("--out", type=Path, help="write JSON here (must be outside the repo); default is stdout")
    ap.add_argument("--gh", action="store_true", help="also run read-only GitHub API checks through the gh CLI")
    ap.add_argument("--gh-timeout", type=int, default=25)
    a = ap.parse_args()
    repo = a.repo.resolve()
    if not repo.is_dir():
        print(f"not a directory: {repo}", file=sys.stderr)
        return 2
    if a.out:
        out = a.out.resolve()
        if out == repo or repo in out.parents:
            print("refusing to write inside the audited repository", file=sys.stderr)
            return 2
    ctx = Ctx(repo)
    list_files(ctx)
    analyze_sources(ctx)
    eco = detect_ecosystems(ctx)
    check_library(ctx)
    check_placeholders(ctx)
    check_agent(ctx)
    check_test_lint(ctx, eco)
    check_ci(ctx)
    check_deps(ctx, eco)
    check_env(ctx, eco)
    check_docs_repo(ctx)
    if a.gh:
        check_github(ctx, a.gh_timeout)
    else:
        ctx.cap("GitHub API checks were not requested (--gh not passed): branch protection, repository settings, community profile and CI status on the default branch were not assessed.")
        for c in ("REPO-003", "CI-006"):
            ctx.check(c, "REPO", "GitHub API check", "na")
    if not any(f.startswith(".github/workflows/") for f in ctx.files):
        pass
    build_measures(ctx)
    doc = {
        "contract": "1.0", "dimension": "foundation", "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "repo": {"path": str(repo), "is_git": ctx.is_git}, "findings": ctx.findings, "checks": ctx.checks, "measures": ctx.measures, "facts": ctx.facts,
        "coverage": {"files_scanned": ctx.files_scanned, "lines_scanned": ctx.lines_scanned, "tracked_files": len(ctx.files),
                     "skipped": sorted(set(SKIP_DIRS)) + ctx.skipped[:20], "caps": ctx.caps},
    }
    text = json.dumps(doc, indent=2, default=str)
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {a.out}: {len(ctx.findings)} findings, {len(ctx.checks)} checks", file=sys.stderr)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
