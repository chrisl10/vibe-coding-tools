#!/usr/bin/env python3
"""Render the Audit My Code brief: one self-contained HTML file per run.

Usage:
    python3 render_brief.py <workspace>
    python3 render_brief.py <workspace> --theme dark      # pin a theme (default: follow the viewer's OS)
    python3 render_brief.py <workspace> --brand path/to/brand.json
    python3 render_brief.py <workspace> --out path/to/brief.html

Reads exactly what contract 1.0 describes (intake.json, NN-*/metrics.json, findings.jsonl,
notes.md, evidence-index.md, 04-remediation/roadmap.md and plan.json) and writes
<workspace>/brief/brief.html. The renderer never invents or edits a finding. Every string that
came from the audited repository or a Drone is untrusted and passes through esc() before it
reaches the page. The page carries no script.

Standard library only (Python 3.11).
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import html
import json
import math
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------------------------
# Overall verdict. Kept small and isolated on purpose: the rule will be refined later.
# --------------------------------------------------------------------------------------------

VERDICT_SCALE = ("healthy", "moderate", "at-risk", "critical")


def rollup_verdict(dimension_verdicts: dict[str, str]) -> str:
    """Return the overall run verdict from each dimension's metrics.json verdict.

    Rule (version 1, worst-of): the overall verdict is the worst verdict among the dimensions
    that ran, on the scale healthy < moderate < at-risk < critical. Dimensions whose verdict is
    "not-run" (or any value outside the scale) are ignored. If no dimension has a verdict on
    the scale, the result is "not-run".

    >>> rollup_verdict({"foundation": "healthy", "bloat": "moderate", "security": "not-run"})
    'moderate'
    >>> rollup_verdict({"foundation": "not-run"})
    'not-run'
    """
    ranked = [VERDICT_SCALE.index(v) for v in dimension_verdicts.values() if v in VERDICT_SCALE]
    return VERDICT_SCALE[max(ranked)] if ranked else "not-run"


# --------------------------------------------------------------------------------------------
# Contract constants (audit-contract.md sections 1, 2, 5, 6, 7)
# --------------------------------------------------------------------------------------------

CONTRACT = "1.0"
TIERS = {
    "foundation": ("Foundation audit", ["foundation"]),
    "vibe": ("Vibe (Lite) code audit", ["foundation", "bloat"]),
    "basic": ("Basic code audit", ["foundation", "bloat", "security"]),
    "full": ("Full code audit", ["foundation", "bloat", "security", "quality"]),
    "mario": ("Mario Audit", ["foundation", "bloat", "security", "quality", "remediation"]),
}
FOLDERS = {
    "foundation": "00-foundation",
    "bloat": "01-bloat",
    "security": "02-security",
    "quality": "03-quality",
    "remediation": "04-remediation",
}
DIM_TITLES = {
    "foundation": "Foundation",
    "bloat": "Bloat",
    "security": "Security",
    "quality": "Quality",
    "remediation": "Remediation roadmap",
}
DIM_QUESTIONS = {
    "foundation": "Is the repository set up so people and agents can work in it safely?",
    "bloat": "How much of the code is copied, unused, or packed into oversized files?",
    "security": "What could an attacker or a careless change do to this app today?",
    "quality": "Does the code do what it claims, and is it tested and maintainable?",
    "remediation": "What to fix, in what order, and how we will know it is fixed.",
}
SEVERITIES = ("critical", "high", "medium", "low", "info")
SEV_RANK = {s: i for i, s in enumerate(SEVERITIES)}
CONF_RANK = {"confirmed": 0, "likely": 1, "possible": 2}
EFFORT_RANK = {"S": 0, "M": 1, "L": 2}
# S/M/L is the contract enum for findings. XS and XL appear only on remediation work packages
# (plan-schema.md), which sum several findings; they are listed here so the badge tooltip is never empty.
EFFORT_WORDS = {"XS": "under 1 hour", "S": "1 to 3 hours", "M": "3 to 8 hours", "L": "1 to 3 days", "XL": "more than 3 days"}
BANDS = ("healthy", "moderate", "at-risk", "critical", "not-run")
BAND_WORDS = {"healthy": "Healthy", "moderate": "Moderate", "at-risk": "At risk",
              "critical": "Critical", "not-run": "Not run"}
CWE_RE = re.compile(r"\bCWE-(\d+)\b", re.I)
ADVISORY_RE = re.compile(r"\b(CVE-\d{4}-\d{4,}|GHSA(?:-[0-9a-z]{4}){3})\b", re.I)
# Generic "vulnerable or outdated component" CWEs that every version advisory carries; never a merge key.
NON_KEY_CWES = {"CWE-1395", "CWE-1104"}
_SECRET_PARTS = (
    # original prefixes
    r"(?<![A-Za-z0-9])(?:sk-ant-|sk_live_|rk_live_|ghp_|github_pat_|xox[abpsr]-|AKIA|ASIA)[A-Za-z0-9_-]{12,}",
    # widened (audit L6), ported from polyglot-security-stinger/scripts/secrets_fallback.py; jwt left out (false positives)
    r"\b(?:A3T[A-Z0-9]|AKIA|ASIA|ABIA|ACCA)[A-Z2-7]{16}\b",
    r"\bgh[opsu]_[0-9a-zA-Z]{36}\b",
    r"\bgithub_pat_\w{82}",
    r"\bglpat-[\w-]{20}",
    r"\bxox[abpsr]-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*",
    r"(?:https?://)?hooks\.slack\.com/(?:services|workflows|triggers)/[A-Za-z0-9+/]{20,}",
    r"\b(?:sk|rk)_(?:test|live|prod)_[a-zA-Z0-9]{10,99}",
    r"\bAIza[\w-]{35}",
    r"\bsk-(?:proj|svcacct|admin)-[A-Za-z0-9_-]{20,}",
    r"\bsk-[a-zA-Z0-9]{20}T3BlbkFJ[a-zA-Z0-9]{20}",
    r"\bsk-ant-(?:api03|admin01)-[a-zA-Z0-9_-]{20,}",
    r"\bnpm_[A-Za-z0-9]{36}",
    r"\bSG\.[A-Za-z0-9=_.-]{66}",
    r"\bshpat_[a-fA-F0-9]{32}",
    r"\bdoo_v1_[a-f0-9]{64}",
    r"\bdp\.pt\.[A-Za-z0-9]{43}",
    r"\bhf_[A-Za-z]{34}",
    r"pypi-AgEIcHlwaS5vcmc[\w-]{50,1000}",
    r"\bdapi[a-f0-9]{32}(?:-\d)?",
    r"-----BEGIN[ A-Z0-9_-]{0,100}PRIVATE KEY(?: BLOCK)?-----",
    # credentialed database and queue URLs
    r"\b(?:postgres(?:ql)?|mysql|mariadb|mongodb(?:\+srv)?|redis|rediss|amqps?)://[^\s:/@'\"]+:[^\s@'\"]{3,}@[^\s'\"]+",
)
SECRET_RE = re.compile("|".join(_SECRET_PARTS))
_SINK: list = []   # the active Run's issue list; set by Run.__init__ so md_inline/md_block/esc can report masking
SAFE_CSS_VALUE = re.compile(r"^[#A-Za-z0-9 ,.'\"()%+/:=@?&_-]*$")

HERE = Path(__file__).resolve().parent
DEFAULT_BRAND = HERE.parent / "references" / "brand" / "brand.json"


# --------------------------------------------------------------------------------------------
# Escaping and small helpers
# --------------------------------------------------------------------------------------------

def esc(value) -> str:
    """Escape any value for HTML body text or a double-quoted attribute. Secret-looking values are masked first."""
    if value is None:
        return ""
    return html.escape(mask_secrets(str(value)), quote=True)


def mask_secrets(text: str, issues: list | None = None) -> str:
    """Belt and braces for contract rule 5.2: mask anything that still looks like a live secret."""
    sink = _SINK if issues is None else issues

    def repl(m):
        note = ("Evidence masked", "A value that looks like an unredacted secret was masked "
                "in the brief. Fix the source finding so it keeps only the first 4 characters.")
        if note not in sink:
            sink.append(note)
        return m.group(0)[:4] + "****"
    return SECRET_RE.sub(repl, text)


def mask_deep(value, issues: list):
    """Mask every string inside a finding (any nesting). Keys starting with an underscore are skipped."""
    if isinstance(value, str):
        return mask_secrets(value, issues)
    if isinstance(value, list):
        return [mask_deep(v, issues) for v in value]
    if isinstance(value, dict):
        return {k: (v if isinstance(k, str) and k.startswith("_") else mask_deep(v, issues)) for k, v in value.items()}
    return value


def fmt_num(v) -> str:
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, int):
        return f"{v:,}"
    if isinstance(v, float):
        if math.isfinite(v) and v == int(v) and abs(v) >= 1000:
            return f"{int(v):,}"
        return f"{v:,.2f}".rstrip("0").rstrip(".")
    return str(v)


def fmt_value(v, unit) -> str:
    unit = "" if unit in (None, "") else str(unit)
    text = fmt_num(v)
    if not unit:
        return text
    return text + unit if unit in ("%", "x") else f"{text} {unit}"


def to_float(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)) and math.isfinite(v):
        return float(v)
    return None


def pretty_date(iso: str | None) -> str:
    if not iso:
        return "date not recorded"
    try:
        d = dt.datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
        return f"{d:%B} {d.day}, {d.year}"
    except ValueError:
        return str(iso)


def pretty_time(iso: str | None) -> str:
    if not iso:
        return "not recorded"
    try:
        d = dt.datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
        return d.strftime("%Y-%m-%d %H:%M %z").strip()
    except ValueError:
        return str(iso)


def pill(kind: str, value: str, words: dict | None = None) -> str:
    """kind is 'sev' or 'band'. Unknown values get a neutral pill, still labeled in text."""
    known = SEVERITIES if kind == "sev" else BANDS
    word = (words or {}).get(value, value)
    cls = f"{kind}-{value}" if value in known else "unknown"
    return f'<span class="pill {cls}">{esc(word)}</span>'


def frame(table_html: str, label: str) -> str:
    return (f'<div class="frame" role="region" tabindex="0" aria-label="{esc(label)}">'
            f"{table_html}</div>")


def table(caption: str, heads: list[tuple[str, str]], rows: list[list[str]], cls: str = "",
          caption_visible: bool = False) -> str:
    """heads: (label, css class). rows: already-escaped cell HTML."""
    cap_cls = "" if caption_visible else ' class="sr-only"'
    th = "".join(f'<th scope="col" class="{c}">{esc(h)}</th>' for h, c in heads)
    body = []
    for r in rows:
        tds = "".join(f'<td class="{heads[i][1]}">{cell}</td>' for i, cell in enumerate(r))
        body.append(f"<tr>{tds}</tr>")
    return (f'<table class="{cls}"><caption{cap_cls}>{esc(caption)}</caption>'
            f"<thead><tr>{th}</tr></thead><tbody>{''.join(body)}</tbody></table>")


def remember(text: str) -> str:
    return ('<aside class="remember"><span class="remember-label">Remember</span>'
            f'<p>{esc(text)}</p></aside>')


# --------------------------------------------------------------------------------------------
# Tiny, safe Markdown subset for notes.md, roadmap.md, evidence-index.md
# Everything is escaped first; links render as text plus the URL in plain text, never href.
# --------------------------------------------------------------------------------------------

def md_inline(text: str) -> str:
    out = esc(mask_secrets(text))
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'\1 <span class="url">(\2)</span>', out)
    return out


def md_block(text: str, heading_base: int = 4) -> str:
    text = mask_secrets(text)
    lines = text.replace("\r\n", "\n").split("\n")
    out, para, i = [], [], 0

    def flush():
        if para:
            out.append(f"<p>{md_inline(' '.join(para))}</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if s.startswith("```"):
            flush()
            j = i + 1
            code = []
            while j < len(lines) and not lines[j].strip().startswith("```"):
                code.append(lines[j])
                j += 1
            out.append(f'<pre class="code">{esc(chr(10).join(code))}</pre>')
            i = j + 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            flush()
            level = min(6, heading_base + len(m.group(1)) - 1)
            out.append(f'<h{level} class="md-h">{md_inline(m.group(2))}</h{level}>')
            i += 1
            continue
        if s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*:?-{3,}", lines[i + 1].strip()):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], [r for r in rows[2:]]
            th = "".join(f'<th scope="col">{md_inline(c)}</th>' for c in head)
            trs = "".join("<tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in r) + "</tr>" for r in body)
            out.append(frame(f"<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>",
                             "Table from a workspace note"))
            continue
        if re.match(r"^([-*]|\d+[.)])\s+", s):
            flush()
            ordered = bool(re.match(r"^\d", s))
            items = []
            while i < len(lines) and re.match(r"^([-*]|\d+[.)])\s+", lines[i].strip()):
                items.append(re.sub(r"^([-*]|\d+[.)])\s+", "", lines[i].strip()))
                i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{md_inline(x)}</li>" for x in items) + f"</{tag}>")
            continue
        if not s:
            flush()
        else:
            para.append(s)
        i += 1
    flush()
    return "\n".join(out)


def md_sections(text: str) -> dict[str, str]:
    """Split markdown into {heading lowercased: body} at level-2 headings."""
    parts, current, buf = {}, "", []
    for line in text.replace("\r\n", "\n").split("\n"):
        m = re.match(r"^##\s+(.*)$", line.strip())
        if m:
            parts[current] = "\n".join(buf).strip()
            current, buf = m.group(1).strip().lower(), []
        else:
            buf.append(line)
    parts[current] = "\n".join(buf).strip()
    return parts


# --------------------------------------------------------------------------------------------
# Loading the workspace
# --------------------------------------------------------------------------------------------

class Run:
    def __init__(self, ws: Path):
        global _SINK
        self.ws = ws
        self.issues: list[tuple[str, str]] = []   # (kind, message) shown in "Data checks"
        _SINK = self.issues
        self.intake: dict = {}
        self.tier = ""
        self.tier_label = ""
        self.dims: list[str] = []
        self.metrics: dict[str, dict | None] = {}
        self.not_run_reason: dict[str, str] = {}
        self.notes: dict[str, str] = {}
        self.findings: list[dict] = []
        self.merges: list[tuple[str, list[str]]] = []
        self.roadmap_md: str | None = None
        self.plan: dict | None = None
        self.evidence_md: str | None = None
        self.raw_files: dict[str, list[tuple[str, int]]] = {}

    def issue(self, kind: str, msg: str):
        self.issues.append((kind, msg))


def read_json(path: Path, run: Run) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        return None
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        run.issue("Unreadable file", f"{path.relative_to(run.ws)}: {exc}")
        return None
    if not isinstance(data, dict):
        run.issue("Unreadable file", f"{path.relative_to(run.ws)}: top level is not an object")
        return None
    return data


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8-sig")
    except (FileNotFoundError, UnicodeDecodeError):
        return None


def first_sentence(md: str | None) -> str:
    if not md:
        return ""
    for line in md.split("\n"):
        s = line.strip()
        if s and not s.startswith(("#", "|", "```", "-", "*")):
            return s[:400]
    return ""


def load(ws: Path) -> Run:
    run = Run(ws)
    intake = read_json(ws / "intake.json", run)
    if intake is None:
        raise SystemExit(f"error: {ws / 'intake.json'} is missing or unreadable; nothing to render")
    run.intake = intake
    if str(intake.get("contract")) != CONTRACT:
        run.issue("Contract version", f"intake.json says contract {intake.get('contract')!r}; "
                  f"this renderer reads contract {CONTRACT}")
    tier = str(intake.get("tier", "")).strip().lower()
    if tier not in TIERS:
        raise SystemExit(f"error: intake.json tier {intake.get('tier')!r} is not one of {sorted(TIERS)}")
    run.tier = tier
    run.tier_label, run.dims = TIERS[tier]

    for dim in run.dims:
        folder = ws / FOLDERS[dim]
        notes = read_text(folder / "notes.md")
        if notes is not None:
            run.notes[dim] = notes
        raw = folder / "raw"
        if raw.is_dir():
            run.raw_files[dim] = sorted(
                (str(p.relative_to(ws)), p.stat().st_size) for p in raw.rglob("*") if p.is_file())
        if dim == "remediation":
            run.roadmap_md = read_text(folder / "roadmap.md")
            run.plan = read_json(folder / "plan.json", run)
            if run.roadmap_md is None and run.plan is None:
                run.not_run_reason[dim] = (f"{FOLDERS[dim]}/ has no roadmap.md or plan.json, so the "
                                           "remediation step did not finish.")
            continue
        metrics = read_json(folder / "metrics.json", run)
        run.metrics[dim] = metrics
        if metrics is None:
            if not folder.is_dir():
                reason = f"The folder {FOLDERS[dim]}/ does not exist in the workspace."
            else:
                reason = f"{FOLDERS[dim]}/metrics.json was not written."
            note = first_sentence(notes)
            run.not_run_reason[dim] = reason + (f" notes.md says: {note}" if note else "")
        else:
            if metrics.get("verdict") == "not-run":
                run.not_run_reason[dim] = str(metrics.get("summary") or "The Drone marked it not run.")
            if metrics.get("verdict") not in BANDS:
                run.issue("Unknown verdict", f"{FOLDERS[dim]}/metrics.json verdict "
                          f"{metrics.get('verdict')!r} is not on the shared scale")
            if metrics.get("dimension") not in (None, dim):
                run.issue("Dimension mismatch", f"{FOLDERS[dim]}/metrics.json says dimension "
                          f"{metrics.get('dimension')!r}")
            cov = metrics.get("coverage")
            if not isinstance(cov, dict) or "caps" not in cov:
                run.issue("Missing caps", f"{FOLDERS[dim]}/metrics.json has no coverage.caps, so the "
                          "brief cannot say whether any tool limit applied")
        load_findings(run, dim, folder / "findings.jsonl")

    for d, folder in FOLDERS.items():
        if d not in run.dims and (ws / folder / "metrics.json").exists():
            run.issue("Outside tier", f"{folder}/metrics.json exists but {d} is not part of the "
                      f"{tier} tier; it is not shown")
    run.evidence_md = read_text(ws / "evidence-index.md")
    if run.evidence_md is None:
        run.issue("Missing file", "evidence-index.md is missing (contract section 9)")
    merge_findings(run)
    return run


def load_findings(run: Run, dim: str, path: Path):
    text = read_text(path)
    if text is None:
        if (run.metrics.get(dim) or {}).get("verdict") not in (None, "not-run"):
            run.issue("Missing file", f"{path.relative_to(run.ws)} is missing")
        return
    for n, line in enumerate(text.split("\n"), start=1):
        if not line.strip():
            continue
        try:
            f = json.loads(line)
        except json.JSONDecodeError as exc:
            run.issue("Unparsed line", f"{path.relative_to(run.ws)} line {n}: {exc.msg}; the line is "
                      "not in the brief")
            continue
        if not isinstance(f, dict):
            run.issue("Unparsed line", f"{path.relative_to(run.ws)} line {n} is not an object")
            continue
        f = mask_deep(f, run.issues)
        fid = str(f.get("id", f"(no id, line {n})"))
        if f.get("severity") not in SEV_RANK:
            run.issue("Unknown severity", f"{fid}: {f.get('severity')!r}; sorted last")
        if f.get("confidence") not in CONF_RANK:
            run.issue("Unknown confidence", f"{fid}: {f.get('confidence')!r}")
        if f.get("confidence") == "possible" and SEV_RANK.get(f.get("severity"), 9) < SEV_RANK["medium"]:
            run.issue("Contract rule 5.3", f"{fid} is 'possible' but rated {f.get('severity')}; "
                      "shown as written, the Drone should lower it")
        if f.get("dimension") not in (None, dim):
            run.issue("Dimension mismatch", f"{fid} sits in {FOLDERS[dim]}/ but says "
                      f"dimension {f.get('dimension')!r}")
        missing = [k for k in ("title", "severity", "confidence", "evidence", "remediation", "effort")
                   if not f.get(k)]
        if missing:
            run.issue("Missing fields", f"{fid}: {', '.join(missing)}")
        f["_dim"] = dim
        f["_sources"] = [str(f.get("source", ""))]
        f["_ids"] = [fid]
        f["id"] = fid
        run.findings.append(f)


def _locs(f: dict) -> list[dict]:
    locs = f.get("locations")
    return [l for l in locs if isinstance(l, dict) and l.get("path")] if isinstance(locs, list) else []


def _cwes(f: dict) -> set[str]:
    refs = f.get("refs") if isinstance(f.get("refs"), list) else []
    cwes = {f"CWE-{m.group(1)}" for r in refs for m in CWE_RE.finditer(str(r))}
    return cwes - NON_KEY_CWES


def _advisories(f: dict) -> frozenset:
    refs = f.get("refs") if isinstance(f.get("refs"), list) else []
    return frozenset(m.group(1).upper() for r in refs for m in ADVISORY_RE.finditer(str(r)))


def _overlap(a: dict, b: dict) -> bool:
    if a.get("path") != b.get("path"):
        return False
    a1, a2 = a.get("line_start"), a.get("line_end", a.get("line_start"))
    b1, b2 = b.get("line_start"), b.get("line_end", b.get("line_start"))
    if not all(isinstance(x, int) for x in (a1, a2, b1, b2)):
        return True   # a location without lines covers the whole file
    return a1 <= b2 and b1 <= a2


def sort_key(f: dict):
    return (SEV_RANK.get(f.get("severity"), 9), CONF_RANK.get(f.get("confidence"), 9),
            EFFORT_RANK.get(f.get("effort"), 9), str(f.get("id")))


def merge_findings(run: Run):
    """Contract 5.4: merge findings sharing a path, an overlapping line range, and a CWE.
    The higher-severity finding is kept as written; the others are listed as merged into it."""
    fs = run.findings
    parent = list(range(len(fs)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    cw = [_cwes(f) for f in fs]
    adv = [_advisories(f) for f in fs]
    lc = [_locs(f) for f in fs]
    for i in range(len(fs)):
        for j in range(i + 1, len(fs)):
            if adv[i] != adv[j]:
                continue   # distinct CVE or GHSA ids are distinct findings, never merged
            if cw[i] & cw[j] and any(_overlap(a, b) for a in lc[i] for b in lc[j]):
                parent[find(i)] = find(j)
    groups: dict[int, list[dict]] = {}
    for i, f in enumerate(fs):
        groups.setdefault(find(i), []).append(f)
    merged = []
    for g in groups.values():
        g.sort(key=sort_key)
        keep = g[0]
        if len(g) > 1:
            others = g[1:]
            keep["_ids"] = [keep["id"]] + [o["id"] for o in others]
            keep["_sources"] = list(dict.fromkeys(keep["_sources"] + [o["_sources"][0] for o in others]))
            seen = {(l.get("path"), l.get("line_start"), l.get("line_end")) for l in _locs(keep)}
            extra = []
            for o in others:
                for l in _locs(o):
                    k = (l.get("path"), l.get("line_start"), l.get("line_end"))
                    if k not in seen:
                        seen.add(k)
                        extra.append(l)
            keep["_extra_locs"] = extra
            run.merges.append((keep["id"], [o["id"] for o in others]))
        merged.append(keep)
    merged.sort(key=sort_key)
    run.findings = merged


# --------------------------------------------------------------------------------------------
# Brand
# --------------------------------------------------------------------------------------------

def load_brand(path: Path) -> dict:
    brand = json.loads(path.read_text(encoding="utf-8"))

    def walk(obj, where):
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, f"{where}.{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, f"{where}[{i}]")
        elif isinstance(obj, str) and where.split(".")[1] in ("palette", "severity", "bands", "fonts"):
            if not SAFE_CSS_VALUE.match(obj):
                raise SystemExit(f"error: brand value {where} has characters not allowed in CSS: {obj!r}")
    walk(brand, "brand")
    brand["_dir"] = path.parent
    return brand


def svg_inline(brand: dict, key: str, cls: str) -> str:
    """Inline a brand SVG (trusted, shipped with the skill). Comments and the XML prolog are dropped."""
    raw = (brand["_dir"] / brand["logos"][key]).read_text(encoding="utf-8")
    raw = re.sub(r"<\?xml[^>]*\?>", "", raw)
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    raw = re.sub(r"\s*\n\s*", " ", raw).strip()
    return raw.replace("<svg ", f'<svg class="{cls}" ', 1)


def favicon_uri(brand: dict) -> str:
    data = (brand["_dir"] / brand["logos"]["favicon"]).read_bytes()
    return "data:image/svg+xml;base64," + base64.b64encode(data).decode("ascii")


def css_string(text: str) -> str:
    """Quote text for a CSS content value. Anything but letters, digits, and a few safe marks is
    hex-escaped (OWASP CSS context rule), so repo-derived text cannot end the string or the rule."""
    out = []
    for ch in str(text):
        if ch.isascii() and (ch.isalnum() or ch in " .,_@-"):
            out.append(ch)
        else:
            out.append(f"\\{ord(ch):06x} ")   # the trailing space ends the escape and is consumed
    return '"' + "".join(out) + '"'


def page_footer_css(brand: dict, left: str, right: str) -> str:
    """Running footer on every printed page via @page margin boxes (CSS Paged Media). Browsers
    that do not support margin boxes still get the footer once, at the end of the document."""
    color = brand["palette"]["light"]["faint"]
    font = brand["fonts"]["mono"]
    box = f"font-family: {font}; font-size: 7.5pt; color: {color}; vertical-align: top; padding-top: 4mm;"
    return (f"@page {{ @bottom-left {{ content: {css_string(left)}; {box} }} "
            f"@bottom-right {{ content: {css_string(right)}; {box} text-align: right; }} }}\n")


def token_css(brand: dict) -> str:
    def block(mode):
        lines = [f"--{k}: {v};" for k, v in brand["palette"][mode].items()]
        lines += [f"--sev-{k}: {v};" for k, v in brand["severity"][mode].items()]
        lines += [f"--band-{k}: {v};" for k, v in brand["bands"][mode].items()]
        return " ".join(lines)
    fonts = f"--font-sans: {brand['fonts']['sans']}; --font-mono: {brand['fonts']['mono']};"
    light, dark = block("light"), block("dark")
    return (f":root {{ {light} {fonts} color-scheme: light; }}\n"
            f"@media (prefers-color-scheme: dark) {{ :root:not([data-theme=\"light\"]) {{ {dark} "
            f"color-scheme: dark; }} }}\n"
            f":root[data-theme=\"dark\"] {{ {dark} color-scheme: dark; }}\n"
            f"@media print {{ :root, :root[data-theme=\"dark\"], :root:not([data-theme=\"light\"]) "
            f"{{ {light} color-scheme: light; }} }}\n")


# --------------------------------------------------------------------------------------------
# Static CSS (layout, components, print). Field Guide system; see guides/03-branding-system.md
# --------------------------------------------------------------------------------------------

BASE_CSS = r"""
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--paper); color: var(--ink); font: 400 16px/1.6 var(--font-sans);
  padding: 32px 16px 0; font-feature-settings: "cv11" 1; overflow-wrap: break-word; }
li, p, dd, td, .lbl { overflow-wrap: anywhere; }
main { max-width: 64rem; margin: 0 auto; display: grid; gap: 64px; }
h1, h2, h3, h4, h5, h6 { margin: 0; line-height: 1.15; text-wrap: balance; }
h2 { font-size: clamp(1.75rem, 4.2vw, 2.4rem); font-weight: 800; letter-spacing: -0.035em; }
h3 { font-size: 1.3rem; font-weight: 700; letter-spacing: -0.02em; margin-top: 8px; }
h4, h5, h6 { font-size: 1.05rem; font-weight: 700; letter-spacing: -0.01em; }
p { margin: 0; max-width: 72ch; }
code, .mono, pre { font-family: var(--font-mono); }
code { font-size: 0.86em; background: var(--box); border: 1px solid var(--rule); padding: 0.05em 0.35em;
  border-radius: 3px; overflow-wrap: anywhere; }
pre.code, pre.evidence { margin: 0; font-size: 0.8rem; line-height: 1.5; background: var(--box);
  border: 1px solid var(--rule); padding: 12px 14px; overflow-x: auto; white-space: pre; max-width: 100%; }
.url { font-family: var(--font-mono); font-size: 0.8em; color: var(--faint); overflow-wrap: anywhere; }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden;
  clip: rect(0 0 0 0); white-space: nowrap; border: 0; }
.eyebrow { font: 500 0.75rem/1.2 var(--font-mono); text-transform: uppercase; letter-spacing: 0.14em;
  color: var(--faint); }
.lead { color: var(--muted); font-size: 1.1rem; }
.muted { color: var(--muted); }
.stack { display: grid; gap: 14px; }
section { display: grid; gap: 22px; min-width: 0; }
main, section, .stack, .part-head, .cover, .verdict { grid-template-columns: minmax(0, 1fr); }
a { color: var(--ink); text-decoration-color: var(--rule-strong); text-underline-offset: 3px; }
a:hover { text-decoration-color: var(--ink); }
td.dim { min-width: 14rem; }
.cards { grid-template-columns: repeat(auto-fit, minmax(min(14rem, 100%), 1fr)); }

/* Cover */
.cover { background: var(--panel); border: 1px solid var(--rule); padding: clamp(24px, 6vw, 72px);
  display: grid; gap: 28px; min-width: 0; }
.cover-eyebrow { display: flex; align-items: center; gap: 14px; font: 500 0.8rem/1 var(--font-mono);
  text-transform: uppercase; letter-spacing: 0.16em; color: var(--faint); }
.cover-eyebrow .idx { color: var(--brand-green); }
.cover-eyebrow .line { flex: 1; height: 1px; background: var(--rule-strong); min-width: 24px; }
.cover-bar { width: 96px; height: 8px; background: var(--brand-amber); margin-top: clamp(24px, 8vw, 120px); }
.cover h1 { font-size: clamp(2.6rem, 10vw, 6.4rem); font-weight: 850; letter-spacing: -0.055em;
  line-height: 0.95; overflow-wrap: anywhere; }
.cover .subtitle { font-size: clamp(1.15rem, 2.6vw, 1.6rem); font-weight: 500; color: var(--muted);
  letter-spacing: -0.015em; line-height: 1.3; max-width: 40ch; }
.framing { color: var(--ink); font-size: 1.02rem; }
.meta { display: flex; flex-wrap: wrap; gap: 6px 22px; color: var(--muted); font-size: 0.88rem; }
.meta span { font-family: var(--font-mono); font-size: 0.82rem; color: var(--ink); overflow-wrap: anywhere; }
.strip { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); background: var(--surface);
  border: 1px solid var(--rule); margin-top: clamp(16px, 5vw, 64px); }
.strip > div { padding: 16px 20px; border-left: 1px solid var(--rule); min-width: 0; }
.strip > div:first-child { border-left: 0; }
.strip .eyebrow { display: block; margin-bottom: 6px; }
.strip strong { font-size: 1.05rem; overflow-wrap: anywhere; }
.cover-foot { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px; }
.cover-foot .mono { font-size: 0.82rem; color: var(--faint); overflow-wrap: anywhere; }
.logo { height: 34px; width: auto; display: block; }
.logo-dark { display: none; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .logo-light { display: none; }
  :root:not([data-theme="light"]) .logo-dark { display: block; } }
:root[data-theme="dark"] .logo-light { display: none; }
:root[data-theme="dark"] .logo-dark { display: block; }

/* Body pages */
.part { border-top: 6px solid var(--ink); padding-top: 18px; }
.part.fair { border-top-color: var(--faint); }
.part.end { border-top-color: var(--brand-green); }
.part-head { display: grid; gap: 12px; }
.contents { border-top: 1px solid var(--rule-strong); }
.contents a { display: grid; grid-template-columns: 7rem 1fr auto; gap: 16px; padding: 16px 0;
  border-bottom: 1px solid var(--rule); color: inherit; text-decoration: none; align-items: baseline; }
.contents a:hover strong { text-decoration: underline; }
.contents .mono { font-size: 0.85rem; color: var(--faint); }
.legend { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(13rem, 100%), 1fr)); border: 1px solid var(--rule); }
.legend div { padding: 14px 18px; border-left: 1px solid var(--rule); display: flex; gap: 12px; align-items: flex-start; font-size: 0.95rem; }
.legend div:first-child { border-left: 0; }
.sw { width: 14px; height: 14px; flex: none; margin-top: 5px; }

/* Verdict */
.verdict { display: grid; gap: 22px; }
.verdict-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px 22px; }
.verdict-word { font: 850 clamp(2.6rem, 9vw, 4.6rem)/0.95 var(--font-sans); letter-spacing: -0.05em; }
.verdict-word.v-healthy { color: var(--band-healthy-fg); }
.verdict-word.v-moderate { color: var(--band-moderate-fg); }
.verdict-word.v-at-risk { color: var(--band-at-risk-fg); }
.verdict-word.v-critical { color: var(--band-critical-fg); }
.verdict-word.v-not-run { color: var(--band-not-run-fg); }
.one-para p + p { margin-top: 14px; }
.sentences { list-style: none; padding: 0; margin: 0; border-top: 1px solid var(--rule-strong); }
.sentences li { display: grid; grid-template-columns: 3rem 1fr; padding: 16px 0; border-bottom: 1px solid var(--rule); }
.sentences .n { font-family: var(--font-mono); color: var(--faint); }

/* Pills */
.pill { display: inline-block; font: 600 0.7rem/1 var(--font-mono); text-transform: uppercase;
  letter-spacing: 0.08em; padding: 5px 8px; border-radius: 2px; white-space: nowrap;
  -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.pill.unknown { color: var(--ink); background: var(--box); border: 1px dashed var(--faint); }
.sev-critical { color: var(--sev-critical-fg); background: var(--sev-critical-bg); }
.sev-high { color: var(--sev-high-fg); background: var(--sev-high-bg); }
.sev-medium { color: var(--sev-medium-fg); background: var(--sev-medium-bg); }
.sev-low { color: var(--sev-low-fg); background: var(--sev-low-bg); }
.sev-info { color: var(--sev-info-fg); background: var(--sev-info-bg); }
.band-healthy { color: var(--band-healthy-fg); background: var(--band-healthy-bg); }
.band-moderate { color: var(--band-moderate-fg); background: var(--band-moderate-bg); }
.band-at-risk { color: var(--band-at-risk-fg); background: var(--band-at-risk-bg); }
.band-critical { color: var(--band-critical-fg); background: var(--band-critical-bg); }
.band-not-run { color: var(--band-not-run-fg); background: var(--band-not-run-bg); }
.effort { font: 600 0.8rem/1 var(--font-mono); }

/* Tables: Field Guide style, mono heads, hairline rows, scroll inside the frame */
.frame { overflow-x: auto; max-width: 100%; -webkit-overflow-scrolling: touch; }
.frame:focus-visible { outline: 2px solid var(--brand-blue); outline-offset: 2px; }
table { border-collapse: collapse; width: 100%; font-size: 0.92rem; }
caption { text-align: left; }
th, td { text-align: left; padding: 12px 14px 12px 0; border-bottom: 1px solid var(--rule); vertical-align: top; }
thead th { font: 500 0.7rem/1.3 var(--font-mono); text-transform: uppercase; letter-spacing: 0.12em;
  color: var(--faint); border-bottom: 1px solid var(--rule-strong); white-space: nowrap; }
td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
td.lead-col { font-weight: 700; overflow-wrap: normal; min-width: 8.5rem; }
td.dim { color: var(--muted); }
td.path, .path { font-family: var(--font-mono); font-size: 0.8rem; overflow-wrap: anywhere; }
td.path { min-width: 13rem; }
td.nowrap { white-space: nowrap; }
.findings td.title-col { min-width: 16rem; }
.findings td.fix-col { min-width: 16rem; color: var(--muted); }
.findings .conf { display: block; font: 500 0.7rem/1.4 var(--font-mono); color: var(--faint);
  text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px; }

/* Cards */
.cards { display: grid; gap: 0;
  border: 1px solid var(--rule); background: var(--surface); }
.card { padding: 18px 20px; border-left: 1px solid var(--rule); display: grid; gap: 8px; align-content: start; min-width: 0; }
.card:first-child { border-left: 0; }
.card .big { font: 800 1.9rem/1 var(--font-sans); letter-spacing: -0.03em; font-variant-numeric: tabular-nums; overflow-wrap: anywhere; }
.card p { font-size: 0.9rem; color: var(--muted); }

/* Callouts */
.remember { display: grid; grid-template-columns: 10rem 1fr; gap: 16px; align-items: center;
  border: 1px solid var(--brand-green); background: var(--brand-mint); padding: 20px 24px;
  -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.remember-label { font: 600 0.8rem/1 var(--font-mono); letter-spacing: 0.16em; text-transform: uppercase; color: var(--brand-green-ink); }
.remember p { font-weight: 700; font-size: 1.08rem; max-width: none; }
.gotcha { border: 2px solid var(--brand-amber); background: var(--brand-amber-soft); padding: 18px 22px;
  display: grid; gap: 6px; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.gotcha strong.h { font-size: 1.12rem; font-weight: 800; letter-spacing: -0.02em; }
.gotcha p { max-width: none; }
.notbox { background: var(--box); border: 1px solid var(--rule); padding: 18px 22px; display: grid; gap: 8px; }
.notrun { border: 1px dashed var(--faint); background: var(--box); padding: 18px 22px; display: grid; gap: 8px; }

/* To-scale bar chart */
.chart { background: var(--box); border: 1px solid var(--rule); padding: 20px 22px 14px; display: grid; gap: 10px;
  -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.chart-legend { display: flex; flex-wrap: wrap; gap: 4px 18px; font: 0.75rem/1.4 var(--font-mono); color: var(--faint); }
.chart-row, .chart-axis { display: grid; grid-template-columns: minmax(6.5rem, 14rem) minmax(0, 1fr) 5.5rem; gap: 12px; align-items: center; }
.chart-row .lbl { font-size: 0.85rem; overflow-wrap: anywhere; }
.chart-row .val { text-align: right; font: 0.8rem var(--font-mono); font-variant-numeric: tabular-nums; }
.track { position: relative; height: 14px; background: var(--surface); border: 1px solid var(--rule); }
.fill { position: absolute; top: 0; bottom: 0; left: 0; background: var(--bar); border-radius: 0 4px 4px 0; }
.fill.f-critical { background: var(--sev-critical-fg); } .fill.f-high { background: var(--sev-high-fg); }
.fill.f-medium { background: var(--sev-medium-fg); } .fill.f-low { background: var(--sev-low-fg); }
.fill.f-info { background: var(--sev-info-fg); }
.fill.b-healthy { background: var(--band-healthy-fg); } .fill.b-moderate { background: var(--band-moderate-fg); }
.fill.b-at-risk { background: var(--band-at-risk-fg); } .fill.b-critical { background: var(--band-critical-fg); }
.fill.b-not-run { background: var(--band-not-run-fg); }
.tick { position: absolute; top: -4px; bottom: -4px; width: 0; border-left: 1px dashed var(--ink); opacity: 0.55; }
.chart-axis .scale { position: relative; height: 1.3em; font: 0.7rem var(--font-mono); color: var(--faint); }
.chart-axis .scale span { position: absolute; transform: translateX(-50%); white-space: nowrap; }
.chart-axis .scale span:first-child { transform: none; }
.chart-axis .scale span:last-child { transform: translateX(-100%); }

/* Lease-style timeline (mario tier) */
.lease { background: var(--box); border: 1px solid var(--rule); padding: 22px; display: grid; gap: 16px;
  -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.lease-track { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); }
.lease-node { position: relative; padding-top: 34px; padding-right: 16px; min-width: 0; }
.lease-node::before { content: ""; position: absolute; top: 4px; left: 0; width: 18px; height: 18px;
  border: 4px solid var(--brand-green); background: var(--box); box-sizing: border-box; z-index: 1; }
.lease-node.filled::before { background: var(--brand-green); }
.lease-node::after { content: ""; position: absolute; top: 11px; left: 18px; right: 0; height: 4px; background: var(--brand-green); }
.lease-node:last-child::after { display: none; }
.lease-node.empty::before { border-color: var(--faint); border-style: dashed; }
.lease-node.empty::after { background: repeating-linear-gradient(90deg, var(--faint) 0 10px, transparent 10px 16px); }
.lease-node .n { font: 700 0.95rem/1.2 var(--font-mono); letter-spacing: 0.04em; text-transform: uppercase; }
.lease-node .cap { color: var(--muted); font-size: 0.9rem; margin: 6px 0 8px; }
.lease-node ul { list-style: none; padding: 0; margin: 0; display: grid; gap: 6px; }
.lease-node li { font: 0.8rem/1.4 var(--font-mono); color: var(--brand-amber-ink); overflow-wrap: anywhere; }

/* Lists */
ol.savings, ol.top { margin: 0; padding: 0; list-style: none; border-top: 1px solid var(--rule-strong); counter-reset: n; }
ol.savings > li, ol.top > li { counter-increment: n; display: grid; grid-template-columns: 3rem minmax(0, 1fr); gap: 4px 12px;
  padding: 16px 0; border-bottom: 1px solid var(--rule); }
ol.savings > li::before, ol.top > li::before { content: counter(n); font-family: var(--font-mono); color: var(--faint); }
ol.top .line1 { display: flex; flex-wrap: wrap; gap: 8px 12px; align-items: baseline; }
ol.top .fix { color: var(--muted); grid-column: 2; }
ul, ol { margin: 0; padding-left: 1.3rem; display: grid; gap: 6px; max-width: 76ch; }

/* Finding details */
.detail { border-top: 1px solid var(--rule); padding: 14px 0; }
.detail summary { cursor: pointer; display: flex; flex-wrap: wrap; gap: 8px 12px; align-items: baseline; list-style-position: outside; }
.detail summary .fid { font: 600 0.82rem var(--font-mono); }
.detail .body { display: grid; gap: 10px; margin-top: 12px; }
.detail dl { display: grid; grid-template-columns: 9rem minmax(0, 1fr); gap: 6px 16px; margin: 0; font-size: 0.92rem; }
.detail dt { font: 500 0.7rem/1.9 var(--font-mono); text-transform: uppercase; letter-spacing: 0.1em; color: var(--faint); }
.detail dd { margin: 0; min-width: 0; overflow-wrap: anywhere; }
.md-h { margin-top: 10px; }
.notes { display: grid; gap: 12px; }

/* Running footer */
.running { max-width: 64rem; margin: 72px auto 0; border-top: 1px solid var(--rule); padding: 18px 0 28px;
  display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px 24px;
  font: 0.78rem/1.5 var(--font-mono); color: var(--faint); }
.running span { overflow-wrap: anywhere; }

@media (max-width: 640px) {
  body { font-size: 15px; }
  .strip { grid-template-columns: 1fr; }
  .strip > div { border-left: 0; border-top: 1px solid var(--rule); }
  .strip > div:first-child { border-top: 0; }
  .remember { grid-template-columns: 1fr; gap: 8px; }
  .contents a { grid-template-columns: 4.5rem 1fr; }
  .contents a .pill { grid-column: 2; justify-self: start; }
  .chart-row, .chart-axis { grid-template-columns: 6rem minmax(0, 1fr) 4.2rem; gap: 8px; }
  .lease-track { grid-template-columns: 1fr; gap: 18px; }
  .lease-node::after { display: none; }
  .detail dl { grid-template-columns: 1fr; }
  .card { border-left: 0; border-top: 1px solid var(--rule); }
  .card:first-child { border-top: 0; }
  .sentences li, ol.savings > li, ol.top > li { grid-template-columns: 2rem minmax(0, 1fr); }
}

@page { size: letter; margin: 14mm 14mm 22mm; }
@media print {
  body { padding: 0; font-size: 10.5pt; background: #FFFFFF; }
  main { max-width: none; gap: 28px; }
  .cover { height: 236mm; break-after: page; align-content: space-between; }
  .part { break-before: page; }
  h2, h3, h4, .part-head { break-after: avoid; }
  .remember, .gotcha, .card, .chart, .lease, .notrun, .notbox, tr, .detail, .strip, .verdict-head { break-inside: avoid; }
  .frame { overflow: visible; }
  table { font-size: 8.5pt; }
  .findings td.title-col, .findings td.fix-col, td.path { min-width: 0; }
  td.num { white-space: normal; }
  th, td { padding: 6px 8px 6px 0; overflow-wrap: anywhere; }
  thead th, td.nowrap { white-space: nowrap; overflow-wrap: normal; }
  td.path, .path, pre.code, pre.evidence { font-size: 7.5pt; }
  td.dim { min-width: 0; }
  pre.code, pre.evidence { white-space: pre-wrap; overflow-wrap: anywhere; }
  details > summary { list-style: none; break-inside: avoid; break-after: avoid; }
  details > summary::-webkit-details-marker { display: none; }
  a { color: inherit; text-decoration: none; }
  .running { margin-top: 24px; }
}
"""


# --------------------------------------------------------------------------------------------
# Section builders
# --------------------------------------------------------------------------------------------

def location_text(f: dict) -> str:
    locs = _locs(f) + f.get("_extra_locs", [])
    if not locs:
        return '<span class="muted">repo-wide</span>'
    def one(l):
        p = str(l.get("path"))
        a, b = l.get("line_start"), l.get("line_end")
        if isinstance(a, int):
            p += f":{a}" + (f"-{b}" if isinstance(b, int) and b != a else "")
        return p
    text = esc(one(locs[0]))
    if len(locs) > 1:
        text += f' <span class="muted">+{len(locs) - 1} more</span>'
    return f'<span class="path">{text}</span>'


def effort_cell(e) -> str:
    word = EFFORT_WORDS.get(e)
    return f'<span class="effort" title="{esc(word or "")}">{esc(e)}</span>' if e else ""


def severity_counts(findings: list[dict]) -> dict[str, int]:
    c = {s: 0 for s in SEVERITIES}
    for f in findings:
        if f.get("severity") in c:
            c[f.get("severity")] += 1
    return c


def nice_max(v: float) -> float:
    if v <= 0:
        return 1.0
    mag = 10 ** math.floor(math.log10(v))
    for step in (1, 2, 2.5, 5, 10):
        if v <= step * mag:
            return step * mag
    return 10 * mag


def bar_chart(label: str, rows: list[tuple], scale_max: float, unit: str, legend: list[str]) -> str:
    """rows: (label, value, fill class, display value, ticks). Every bar is to scale on 0..scale_max;
    ticks are that row's own threshold values, drawn as dashed lines."""
    if not rows:
        return ""
    parts = [f'<figure class="chart" role="group" aria-label="{esc(label)}" style="margin:0">',
             '<div class="chart-legend">' + "".join(f"<span>{esc(x)}</span>" for x in legend) + "</div>"]
    for name, value, cls, shown, ticks in rows:
        w = max(0.0, min(value, scale_max)) / scale_max * 100
        tick_html = "".join(f'<span class="tick" style="left:{t / scale_max * 100:.2f}%"></span>'
                            for t in ticks if 0 < t < scale_max)
        parts.append(f'<div class="chart-row" title="{esc(name)}: {esc(shown)}"><span class="lbl">{esc(name)}</span>'
                     f'<div class="track"><div class="fill {cls}" style="width:{w:.2f}%"></div>{tick_html}</div>'
                     f'<span class="val">{esc(shown)}</span></div>')
    marks = [0, scale_max / 4, scale_max / 2, scale_max * 3 / 4, scale_max]
    scale = "".join(f'<span style="left:{m / scale_max * 100:.2f}%">{esc(fmt_num(round(m, 2)))}'
                    f'{esc(unit) if i == len(marks) - 1 else ""}</span>' for i, m in enumerate(marks))
    parts.append(f'<div class="chart-axis" aria-hidden="true"><span></span><div class="scale">{scale}</div><span></span></div>')
    parts.append("</figure>")
    return "".join(parts)


def severity_chart(findings: list[dict], label: str) -> str:
    c = severity_counts(findings)
    if not any(c.values()):
        return ""
    top = nice_max(max(c.values()))
    rows = [(s.capitalize(), float(n), f"f-{s}", fmt_num(n), []) for s, n in c.items()]
    return bar_chart(label, rows, top, "",
                     [f"Bar length to scale, 0 to {fmt_num(top)} findings", "Each bar is labeled with its count"])


def threshold_ticks(text: str) -> list[float]:
    return [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*%", str(text or ""))]


def measures_chart(measures: list[dict], dim: str) -> str:
    pct = [m for m in measures if str(m.get("unit")) == "%" and to_float(m.get("value")) is not None]
    if len(pct) < 2:
        return ""
    ticks = [t for m in pct for t in threshold_ticks(m.get("threshold"))]
    top = nice_max(max([to_float(m["value"]) for m in pct] + ticks) * 1.1)
    rows = [(str(m.get("label", m.get("key"))), to_float(m["value"]), f"b-{m.get('band')}",
             fmt_value(m.get("value"), "%"), threshold_ticks(m.get("threshold"))) for m in pct]
    legend = [f"Bar length to scale, 0 to {fmt_num(top)}%"]
    if ticks:
        legend.append("Dashed lines: that measure's own thresholds")
    legend.append("Bar color follows the band, which the table also names")
    return bar_chart(f"{DIM_TITLES[dim]} percentage measures, to scale", rows, top, "%", legend)


def measures_table(measures: list[dict], dim: str) -> str:
    rows = []
    for m in measures:
        result = fmt_value(m.get("value"), m.get("unit"))
        rows.append([esc(m.get("label", m.get("key", ""))), esc(result),
                     pill("band", str(m.get("band")), BAND_WORDS), esc(m.get("threshold", "")),
                     f'<span class="muted">{esc(m.get("source", ""))}</span>'])
    if not rows:
        return '<p class="muted">This dimension reported no measures.</p>'
    return frame(table(f"{DIM_TITLES[dim]} measures",
                       [("Measure", "lead-col"), ("Result", "num"), ("Band", "nowrap"), ("Threshold", "dim"),
                        ("Source", "")], rows), f"{DIM_TITLES[dim]} measures table")


def findings_table(findings: list[dict], dim: str, issues: list) -> str:
    if not findings:
        return '<p class="muted">No findings were recorded for this dimension.</p>'
    rows = []
    for f in findings:
        merged = ""
        if len(f["_ids"]) > 1:
            merged = f'<span class="conf">merged: {esc(", ".join(f["_ids"][1:]))}</span>'
        rows.append([f'<a class="path" href="#f-{esc(slug(f["id"]))}">{esc(f["id"])}</a>{merged}',
                     pill("sev", str(f.get("severity"))), location_text(f),
                     f'{esc(f.get("title", ""))}<span class="conf">{esc(f.get("confidence", ""))}</span>',
                     esc(mask_secrets(str(f.get("remediation", "")), issues)), effort_cell(f.get("effort"))])
    return frame(table(f"{DIM_TITLES[dim]} findings, most severe first",
                       [("ID", "nowrap"), ("Severity", "nowrap"), ("Location", "path"), ("Finding", "title-col"),
                        ("Fix", "fix-col"), ("Effort", "nowrap")], rows, cls="findings"),
                 f"{DIM_TITLES[dim]} findings table")


def slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "-", s).strip("-").lower() or "x"


def spot_check_table(findings: list[dict], dim: str) -> str:
    rows = [[esc(f["id"]), esc(f.get("confidence", "")), esc(f.get("verified_by", "")) or '<span class="muted">not stated</span>']
            for f in findings]
    if not rows:
        return ""
    return frame(table(f"How each {DIM_TITLES[dim].lower()} finding was checked",
                       [("Finding", "nowrap"), ("Confidence", "nowrap"), ("How false positives were ruled out", "dim")],
                       rows), f"{DIM_TITLES[dim]} spot-check table")


def savings_list(findings: list[dict]) -> str:
    acts = [f for f in findings if f.get("severity") in ("critical", "high", "medium", "low")][:5]
    if not acts:
        return ""
    lis = "".join(f'<li><div><strong>{esc(f.get("title", ""))}</strong> '
                  f'<span class="muted">{esc(f.get("remediation", ""))}</span></div></li>' for f in acts)
    return f'<h3>Where the real savings are</h3><ol class="savings">{lis}</ol>'


def detail_blocks(findings: list[dict], issues: list) -> str:
    out = []
    for f in findings:
        refs = f.get("refs") if isinstance(f.get("refs"), list) else []
        locs = _locs(f) + f.get("_extra_locs", [])
        loc_list = "<br>".join(
            esc(str(l.get("path")) + (f":{l.get('line_start')}" if isinstance(l.get("line_start"), int) else "")
                + (f"-{l.get('line_end')}" if isinstance(l.get("line_end"), int) and l.get("line_end") != l.get("line_start") else ""))
            for l in locs) or "repo-wide"
        open_attr = " open" if f.get("severity") in ("critical", "high", "medium") else ""
        evidence = mask_secrets(str(f.get("evidence", "")), issues)
        out.append(
            f'<details class="detail" id="f-{esc(slug(f["id"]))}"{open_attr}><summary>'
            f'<span class="fid">{esc(f["id"])}</span>{pill("sev", str(f.get("severity")))}'
            f'<span>{esc(f.get("title", ""))}</span></summary><div class="body"><dl>'
            f'<dt>Why it matters</dt><dd>{esc(f.get("why_it_matters", ""))}</dd>'
            f'<dt>Fix</dt><dd>{esc(mask_secrets(str(f.get("remediation", "")), issues))}</dd>'
            f'<dt>Effort</dt><dd>{esc(f.get("effort", ""))} {esc(EFFORT_WORDS.get(f.get("effort"), ""))}</dd>'
            f'<dt>Locations</dt><dd class="path">{loc_list}</dd>'
            f'<dt>Confidence</dt><dd>{esc(f.get("confidence", ""))}: {esc(f.get("verified_by", ""))}</dd>'
            f'<dt>Standards</dt><dd>{esc(", ".join(str(r) for r in refs)) or "none listed"}</dd>'
            f'<dt>Reported by</dt><dd>{esc(", ".join(s for s in f["_sources"] if s))}'
            + (f' (merged {esc(", ".join(f["_ids"][1:]))})' if len(f["_ids"]) > 1 else "")
            + f'</dd></dl><pre class="evidence">{esc(evidence)}</pre></div></details>')
    return "".join(out)


def gotchas(metrics: dict) -> str:
    caps = (metrics.get("coverage") or {}).get("caps") if isinstance(metrics.get("coverage"), dict) else None
    if not isinstance(caps, list) or not caps:
        return ""
    return "".join(f'<div class="gotcha"><strong class="h">Tool limit, handled.</strong><p>{esc(c)}</p></div>'
                   for c in caps)


def scope_paragraph(metrics: dict) -> str:
    cov = metrics.get("coverage") if isinstance(metrics.get("coverage"), dict) else {}
    bits = []
    if cov.get("files_scanned") is not None:
        bits.append(f"{fmt_num(cov['files_scanned'])} files")
    if cov.get("lines_scanned") is not None:
        bits.append(f"{fmt_num(cov['lines_scanned'])} lines")
    text = "Scope: " + (" and ".join(bits) if bits else "file and line counts not reported") + "."
    skipped = cov.get("skipped") if isinstance(cov.get("skipped"), list) else []
    if skipped:
        text += " Excluded: " + ", ".join(str(s) for s in skipped) + "."
    return f'<p class="muted">{esc(text)}</p>'


def dimension_cards(metrics: dict, findings: list[dict]) -> str:
    c = severity_counts(findings)
    cards = []
    for m in (metrics.get("measures") or [])[:2]:
        cards.append(f'<div class="card"><span class="eyebrow">{esc(m.get("label", m.get("key", "")))}</span>'
                     f'<span class="big">{esc(fmt_value(m.get("value"), m.get("unit")))}</span>'
                     f'<p>{pill("band", str(m.get("band")), BAND_WORDS)} {esc(m.get("threshold", ""))}</p></div>')
    urgent = c["critical"] + c["high"]
    cards.append(f'<div class="card"><span class="eyebrow">Findings</span><span class="big">{fmt_num(len(findings))}</span>'
                 f'<p>{fmt_num(urgent)} critical or high, {fmt_num(c["medium"])} medium, '
                 f'{fmt_num(c["low"] + c["info"])} low or info.</p></div>')
    return '<div class="cards">' + "".join(cards) + "</div>"


def sources_eyebrow(n: int, metrics: dict | None, dim: str) -> str:
    srcs = []
    for m in (metrics or {}).get("measures") or []:
        s = str(m.get("source", "")).split(" ")[0]
        if s and s not in srcs:
            srcs.append(s)
    label = " · ".join([str(n)] + (srcs[:3] if srcs else [DIM_TITLES[dim]]))
    return f'<span class="eyebrow">{esc(label)}</span>'


def notes_block(md: str | None) -> str:
    if not md or not md.strip():
        return ""
    secs = md_sections(md)
    out = []
    nc = next((v for k, v in secs.items() if k.startswith("not confirmed")), None)
    if nc:
        out.append(f'<div class="notbox"><span class="eyebrow">Not confirmed</span>{md_block(nc, 5)}</div>')
    rest = "\n\n".join((f"## {k}\n{v}" if k else v) for k, v in secs.items()
                       if v and not k.startswith("not confirmed"))
    if rest.strip():
        out.append(f'<details class="detail"><summary><span class="fid">Drone notes</span>'
                   f'<span class="muted">notes.md, rendered as written</span></summary>'
                   f'<div class="body notes">{md_block(rest, 4)}</div></details>')
    return "".join(out)


def dimension_section(run: Run, n: int, dim: str) -> str:
    metrics = run.metrics.get(dim)
    fs = [f for f in run.findings if f["_dim"] == dim]
    head = (f'<div class="part-head">{sources_eyebrow(n, metrics, dim)}'
            f'<h2 id="{dim}">{esc(DIM_TITLES[dim])}</h2><p class="lead">{esc(DIM_QUESTIONS[dim])}</p></div>')
    if metrics is None or metrics.get("verdict") == "not-run":
        reason = run.not_run_reason.get(dim, "No output was found for this dimension.")
        extra = ("<h3>Findings it did write</h3>" + findings_table(fs, dim, run.issues)) if fs else ""
        return (f'<section class="part" aria-labelledby="{dim}">{head}<div class="notrun">{pill("band", "not-run", BAND_WORDS)}'
                f'<p>{esc(reason)}</p></div>{extra}{notes_block(run.notes.get(dim))}</section>')
    verdict = str(metrics.get("verdict"))
    parts = [f'<section class="part" aria-labelledby="{dim}">', head,
             f'<div class="verdict-head"><span class="eyebrow">Dimension verdict</span>{pill("band", verdict, BAND_WORDS)}</div>',
             scope_paragraph(metrics)]
    if metrics.get("summary"):
        parts.append(remember(str(metrics.get("summary"))))
    parts.append(gotchas(metrics))
    parts.append(dimension_cards(metrics, fs))
    parts.append("<h3>Measures</h3>" + measures_table(metrics.get("measures") or [], dim))
    chart = measures_chart(metrics.get("measures") or [], dim)
    if chart:
        parts.append("<h3>Measures, to scale</h3>" + chart)
    sc = severity_chart(fs, f"{DIM_TITLES[dim]} findings by severity")
    if sc:
        parts.append("<h3>Findings by severity</h3>" + sc)
    parts.append("<h3>Findings</h3>" + findings_table(fs, dim, run.issues))
    st = spot_check_table(fs, dim)
    if st:
        parts.append("<h3>Spot checks</h3>" + st)
    parts.append(savings_list(fs))
    if fs:
        parts.append("<h3>Finding details</h3>" + detail_blocks(fs, run.issues))
    parts.append(notes_block(run.notes.get(dim)))
    parts.append("</section>")
    return "".join(p for p in parts if p)


def remediation_section(run: Run, n: int) -> str:
    dim = "remediation"
    head = (f'<div class="part-head"><span class="eyebrow">{n} · Roadmap</span>'
            f'<h2 id="{dim}">{esc(DIM_TITLES[dim])}</h2><p class="lead">{esc(DIM_QUESTIONS[dim])}</p></div>')
    if dim in run.not_run_reason:
        return (f'<section class="part" aria-labelledby="{dim}">{head}<div class="notrun">{pill("band", "not-run", BAND_WORDS)}'
                f'<p>{esc(run.not_run_reason[dim])}</p></div></section>')
    parts = [f'<section class="part" aria-labelledby="{dim}">', head]
    plan = run.plan or {}
    items = [i for i in plan.get("items", []) if isinstance(i, dict)] if isinstance(plan.get("items"), list) else []
    by_id = {str(i.get("id")): i for i in items}
    waves = plan.get("waves") if isinstance(plan.get("waves"), dict) else {}
    if items:
        caps = {"now": "start here", "next": "after Now lands", "later": "when there is room"}
        nodes = []
        for w in ("now", "next", "later"):
            ids = [str(x) for x in (waves.get(w) or [])] or [str(i.get("id")) for i in items if i.get("wave") == w]
            cls = "filled" if w == "later" and ids else ("empty" if not ids else "")
            lis = "".join(f'<li>{esc(i)} {esc((by_id.get(i) or {}).get("title", ""))}</li>' for i in ids) or "<li>nothing planned</li>"
            nodes.append(f'<div class="lease-node {cls}"><div class="n">{esc(w)}</div>'
                         f'<p class="cap">{esc(caps[w])}, {len(ids)} work package{"s" if len(ids) != 1 else ""}</p><ul>{lis}</ul></div>')
        parts.append('<figure class="lease" style="margin:0" aria-label="Remediation waves, Now then Next then Later">'
                     '<span class="eyebrow">The plan, start to finish</span>'
                     f'<div class="lease-track">{"".join(nodes)}</div></figure>')
        first = by_id.get(str((waves.get("now") or [None])[0])) if waves.get("now") else None
        if first:
            parts.append(remember(f"Do {first.get('id')} first: {first.get('title', '')}. {first.get('impact', '')}".strip()))
        rows = []
        for i in items:
            rows.append([esc(i.get("id", "")), esc(i.get("title", "")),
                         esc(", ".join(str(x) for x in i.get("finding_ids", []) or [])),
                         pill("sev", str(i.get("max_severity", ""))), effort_cell(i.get("effort")),
                         esc(i.get("risk", "")), esc(i.get("wave", "")), esc(i.get("owner_drone", "")),
                         esc(", ".join(str(x) for x in i.get("depends_on", []) or [])) or '<span class="muted">none</span>'])
        parts.append("<h3>Work packages</h3>" + frame(table(
            "Remediation work packages", [("Item", "nowrap"), ("Title", "title-col"), ("Findings", "path"),
                                          ("Max severity", "nowrap"), ("Effort", "nowrap"), ("Risk", "dim"),
                                          ("Wave", "nowrap"), ("Owner Drone", "path"), ("Depends on", "path")],
            rows, cls="findings"), "Remediation work packages table"))
        lib = plan.get("library") if isinstance(plan.get("library"), dict) else {}
        if lib:
            approved = lib.get("approved_files") or []
            parts.append(f'<div class="notbox"><span class="eyebrow">library/ consent</span><p>State: '
                         f'{esc(lib.get("consent_state", "not recorded"))}. Approved files: {fmt_num(len(approved))}.</p>'
                         + ("<ul>" + "".join(f'<li class="path">{esc(a)}</li>' for a in approved) + "</ul>" if approved else "")
                         + "</div>")
        unc = plan.get("uncovered_finding_ids") or []
        if unc:
            run.issue("Plan coverage", "plan.json leaves these findings uncovered: " + ", ".join(str(u) for u in unc))
    if run.roadmap_md:
        parts.append('<h3>Roadmap, as written</h3><div class="notes">' + md_block(run.roadmap_md, 4) + "</div>")
    parts.append("</section>")
    return "".join(parts)


# --------------------------------------------------------------------------------------------
# Page assembly
# --------------------------------------------------------------------------------------------

def repo_changes(run: Run) -> str:
    if run.tier != "mario":
        return "none"
    lib = (run.plan or {}).get("library") if isinstance((run.plan or {}).get("library"), dict) else {}
    if lib.get("consent_state") == "approved" and lib.get("approved_files"):
        return f"library/ only, {len(lib['approved_files'])} files the requester approved"
    return "none (library/ files wait for approval)"


def code_execution(run: Run) -> str:
    """Plain-language record of the user's consent to run the repository's own code (contract 4)."""
    ex = run.intake.get("execution") if isinstance(run.intake.get("execution"), dict) else {}
    mode = ex.get("mode")
    if mode == "container":
        return "the repository's own commands ran in a throwaway container with no network, with the requester's consent"
    if mode == "host":
        return "the repository's own commands ran on the auditor's machine with credentials stripped, with the requester's consent"
    if mode == "none":
        return "none; the requester declined, so checks that would run the repository's code are reported as not run"
    return "not recorded"


def build(run: Run, brand: dict, theme: str | None) -> str:
    it = run.intake
    repo = it.get("repo") if isinstance(it.get("repo"), dict) else {}
    repo_name = str(repo.get("name") or "repository")
    requested_by = str(it.get("requested_by") or "requester not recorded")
    date = pretty_date(it.get("started_at"))
    title = f"{repo_name} {brand.get('title_suffix', 'Code Audit')}"
    ctx = {"company": brand.get("company", ""), "requested_by": requested_by, "repo": repo_name,
           "date": date, "title": title}
    foot_left = brand["footer"]["left"].format(**ctx)
    foot_right = brand["footer"]["right"].format(**ctx)

    verdicts = {d: str((run.metrics.get(d) or {}).get("verdict") or "not-run") for d in run.dims if d != "remediation"}
    overall = rollup_verdict(verdicts)
    tools = it.get("tools") if isinstance(it.get("tools"), dict) else {}
    tools_text = " · ".join(f"{k} {v}" for k, v in tools.items()) or "not recorded"
    stacks = it.get("stacks") if isinstance(it.get("stacks"), list) else []
    stack_text = ", ".join(f"{s.get('id')} {s.get('version', '')}".strip() for s in stacks if isinstance(s, dict))
    dims_text = ", ".join(DIM_TITLES[d].split(" ")[0].lower() for d in run.dims)
    branch_sha = " ".join(x for x in (str(repo.get("branch") or ""), str(repo.get("sha") or "")[:12]) if x)

    sections = []
    n = 0
    for d in run.dims:
        n += 1
        sections.append(remediation_section(run, n) if d == "remediation" else dimension_section(run, n, d))

    # The whole audit in one paragraph: each dimension's own summary, in tier order.
    summaries = []
    for d in run.dims:
        if d == "remediation":
            continue
        m = run.metrics.get(d)
        s = (m or {}).get("summary") if m else None
        summaries.append((d, str(s) if s else f"Did not run. {run.not_run_reason.get(d, 'No output was found.')}"))
    one_para = " ".join(f"{DIM_TITLES[d]}: {s}" for d, s in summaries)

    # Scorecard
    score_rows = []
    for d in run.dims:
        if d == "remediation":
            st = "not-run" if d in run.not_run_reason else "healthy"
            score_rows.append([f'<a href="#{d}">{esc(DIM_TITLES[d])}</a>',
                               pill("band", "not-run", BAND_WORDS) if st == "not-run" else '<span class="muted">plan</span>',
                               "", "", "", "", esc(run.not_run_reason.get(d, "Waves, work packages, and library/ proposals."))])
            continue
        fs = [f for f in run.findings if f["_dim"] == d]
        c = severity_counts(fs)
        m = run.metrics.get(d) or {}
        score_rows.append([f'<a href="#{d}">{esc(DIM_TITLES[d])}</a>', pill("band", verdicts[d], BAND_WORDS),
                           fmt_num(c["critical"]), fmt_num(c["high"]), fmt_num(c["medium"]),
                           fmt_num(c["low"] + c["info"]),
                           esc(m.get("summary") or run.not_run_reason.get(d, ""))])
    scorecard = frame(table("Verdict by dimension", [("Dimension", "lead-col"), ("Verdict", "nowrap"),
                                                      ("Critical", "num"), ("High", "num"), ("Medium", "num"),
                                                      ("Low or info", "num"), ("Summary", "dim")], score_rows),
                      "Scorecard table")

    # Top 10
    top = [f for f in run.findings if f.get("severity") in ("critical", "high", "medium", "low")][:10]
    top_html = "".join(
        f'<li><div class="line1">{pill("sev", str(f.get("severity")))}<a class="path" href="#f-{esc(slug(f["id"]))}">{esc(f["id"])}</a>'
        f'<strong>{esc(f.get("title", ""))}</strong>{effort_cell(f.get("effort"))}</div>'
        f'<div class="fix">{esc(mask_secrets(str(f.get("remediation", "")), run.issues))} {location_text(f)}</div></li>'
        for f in top) or '<li><div>No actionable findings were recorded.</div></li>'

    # Coverage and caps
    cov_rows = []
    for d in run.dims:
        if d == "remediation":
            continue
        m = run.metrics.get(d)
        if m is None:
            cov_rows.append([esc(DIM_TITLES[d]), "", "", "", f'<span class="muted">{esc(run.not_run_reason.get(d, "not run"))}</span>'])
            continue
        cov = m.get("coverage") if isinstance(m.get("coverage"), dict) else {}
        caps = cov.get("caps")
        if isinstance(caps, list) and caps:
            cap_html = "<ul>" + "".join(f"<li>{esc(c)}</li>" for c in caps) + "</ul>"
        elif isinstance(caps, list):
            cap_html = '<span class="muted">No limit applied (an empty caps list is the Drone\'s claim)</span>'
        else:
            cap_html = '<strong>Not reported.</strong> The Drone did not say whether a tool limit applied.'
        sk = cov.get("skipped") if isinstance(cov.get("skipped"), list) else []
        cov_rows.append([esc(DIM_TITLES[d]), esc(fmt_num(cov.get("files_scanned", ""))), esc(fmt_num(cov.get("lines_scanned", ""))),
                         f'<span class="path">{esc(", ".join(str(s) for s in sk)) or "none"}</span>', cap_html])
    coverage = frame(table("Coverage and caps by dimension", [("Dimension", "lead-col"), ("Files", "num"), ("Lines", "num"),
                                                              ("Skipped", "path"), ("Limits and caps", "")], cov_rows),
                     "Coverage and caps table")

    # Evidence index
    ex_cfg = run.intake.get("execution") if isinstance(run.intake.get("execution"), dict) else {}
    throwaway_li = ('<li>Tools that install or write ran against a throwaway copy of the repository, '
                    'which was removed at the end of the run.</li>'
                    if "bloat" in run.dims or ex_cfg.get("allowed") is True else "")
    ev_parts = []
    if run.evidence_md:
        ev_parts.append('<div class="notes">' + md_block(run.evidence_md, 4) + "</div>")
    raw_rows = [[f'<span class="path">{esc(p)}</span>', esc(fmt_num(size))]
                for d in run.dims for p, size in run.raw_files.get(d, [])]
    if raw_rows:
        ev_parts.append("<h3>Raw artifacts in the workspace</h3>" + frame(
            table("Raw artifacts", [("Path", "path"), ("Bytes", "num")], raw_rows), "Raw artifacts table"))

    # Data checks (render after sections so masking issues are collected)
    merges = [[esc(k), esc(", ".join(v))] for k, v in run.merges]
    merge_html = (frame(table("Merged duplicate findings", [("Kept", "nowrap"), ("Merged into it", "path")], merges),
                      "Merged findings table") if merges else
                  '<p class="muted">No duplicate findings were merged.</p>')
    seen_issue = []
    for x in run.issues:
        if x not in seen_issue:
            seen_issue.append(x)
    issue_html = (frame(table("Data checks", [("Check", "nowrap"), ("Detail", "dim")],
                              [[esc(k), esc(v)] for k, v in seen_issue]), "Data checks table")
                  if seen_issue else '<p class="muted">Every workspace file the brief reads parsed cleanly against contract 1.0.</p>')

    contents_rows = ['<a href="#start"><span class="mono">Start</span><strong>The whole audit in one paragraph</strong></a>',
                     f'<a href="#verdict"><span class="mono">Verdict</span><strong>Scorecard across dimensions</strong>'
                     f'{pill("band", overall, BAND_WORDS)}</a>']
    for i, d in enumerate(run.dims, start=1):
        v = verdicts.get(d, "not-run" if d in run.not_run_reason else None)
        contents_rows.append(f'<a href="#{d}"><span class="mono">Part {i}</span><strong>{esc(DIM_TITLES[d])}</strong>'
                             + (pill("band", v, BAND_WORDS) if v else "") + "</a>")
    contents_rows += ['<a href="#first"><span class="mono">Fix</span><strong>Fix these first</strong></a>',
                      '<a href="#coverage"><span class="mono">Limits</span><strong>Coverage and caps</strong></a>',
                      '<a href="#method"><span class="mono">End</span><strong>Method and evidence index</strong></a>']

    word_source = one_para + " ".join(str(f.get("title", "")) + " " + str(f.get("remediation", "")) + " "
                                      + str(f.get("why_it_matters", "")) for f in run.findings)
    read_minutes = max(1, round(len(word_source.split()) / 230 + len(run.findings) * 0.15))

    kind = run.tier_label if run.tier == "mario" else "read-only " + run.tier_label[0].lower() + run.tier_label[1:]
    framing = (f"A {kind} of {repo_name}, covering {dims_text}. Prepared for {requested_by}. "
               "Every number and finding below comes from the run workspace; nothing was added by the renderer.")
    theme_attr = f' data-theme="{esc(theme)}"' if theme in ("light", "dark") else ""
    pre = "".join(f'<link rel="preconnect" href="{esc(u)}"{" crossorigin" if "gstatic" in u else ""}>'
                  for u in brand["fonts"].get("preconnect", []))
    body = f"""
<main>
<header class="cover" id="top">
  <div class="cover-eyebrow"><span class="idx">01</span><span>{esc(brand.get('eyebrow', ''))}</span><span class="line"></span></div>
  <div class="stack">
    <div class="cover-bar" aria-hidden="true"></div>
    <h1>{esc(repo_name)}<br>{esc(brand.get('title_suffix', 'Code Audit'))}</h1>
    <p class="subtitle">{esc(run.tier_label)}: {esc(dims_text)}</p>
    <p class="framing">{esc(framing)}</p>
    <div class="meta">
      <div>Run <span>{esc(pretty_time(it.get('started_at')))}</span></div>
      <div>Tools <span>{esc(tools_text)}</span></div>
      <div>Stack <span>{esc(stack_text or 'not recorded')}</span></div>
      <div>Repo changes <span>{esc(repo_changes(run))}</span></div>
    </div>
  </div>
  <div class="stack">
    <div class="strip">
      <div><span class="eyebrow">By</span><strong>{esc(brand.get('company', ''))} for {esc(requested_by)}</strong></div>
      <div><span class="eyebrow">Tier</span><strong>{esc(run.tier_label)}</strong></div>
      <div><span class="eyebrow">Repo</span><strong class="path">{esc(repo_name)}{(' @ ' + esc(branch_sha)) if branch_sha else ''}</strong></div>
    </div>
    <div class="cover-foot">{svg_inline(brand, 'light', 'logo logo-light')}{svg_inline(brand, 'dark', 'logo logo-dark')}
      <span class="mono">{esc(date)} · read time about {read_minutes} minutes</span></div>
  </div>
</header>

<section aria-labelledby="contents-h">
  <div class="cover-eyebrow"><span class="idx">00</span><span>Contents</span><span class="line"></span></div>
  <h2 id="contents-h">What is in here</h2>
  <p class="lead">Plain language throughout. Every finding says what is wrong, why it matters here, and the exact fix.</p>
  <nav class="contents" aria-label="Contents">{''.join(contents_rows)}</nav>
  <div class="legend" aria-label="Color key">
    <div><span class="sw" style="background:var(--band-critical-fg)"></span><span>Red and orange pills are critical or high: fix first. Every pill also says its word.</span></div>
    <div><span class="sw" style="background:var(--brand-green)"></span><span>Green boxes marked Remember hold the one thing to keep from a section.</span></div>
    <div><span class="sw" style="background:var(--brand-amber)"></span><span>Amber boxes are tool limits the run hit or lifted, so nothing is silently cut.</span></div>
  </div>
</section>

<section class="part" aria-labelledby="start">
  <div class="part-head"><span class="eyebrow">Start here</span><h2 id="start">The whole audit in one paragraph</h2></div>
  <div class="one-para"><p>{esc(one_para)}</p></div>
  <ol class="sentences">{''.join(f'<li><span class="n">{i}</span><span><strong>{esc(DIM_TITLES[d])}.</strong> {esc(s)}</span></li>' for i, (d, s) in enumerate(summaries, start=1))}</ol>
</section>

<section class="part verdict" aria-labelledby="verdict">
  <div class="verdict-head"><span class="eyebrow" id="verdict">Verdict</span>
    <span class="verdict-word v-{esc(overall)}">{esc(BAND_WORDS.get(overall, overall))}</span></div>
  <p><strong>The overall verdict is the worst dimension verdict.</strong> One dimension at risk makes the whole run at risk, because a single weak area is enough to hurt the app.</p>
  {scorecard}
  {severity_chart(run.findings, "All findings by severity")}
</section>

{''.join(sections)}

<section class="part" aria-labelledby="first">
  <div class="part-head"><span class="eyebrow">Next steps</span><h2 id="first">Fix these first</h2>
  <p class="lead">The ten most urgent findings across every dimension: most severe first, then the most certain, then the quickest.</p></div>
  <ol class="top">{top_html}</ol>
</section>

<section class="part fair" aria-labelledby="coverage">
  <div class="part-head"><span class="eyebrow">Limits, said out loud</span><h2 id="coverage">Coverage and caps</h2>
  <p class="lead">What each dimension scanned, what it skipped, and every tool limit it hit or lifted.</p></div>
  {coverage}
  <h3>Data checks</h3>
  {issue_html}
  <h3>Merged duplicates</h3>
  <p class="muted">Findings from different Drones that share a file, an overlapping line range, and a CWE are shown once; the higher severity is kept. Findings with different CVE or GHSA ids are never merged, and generic dependency CWEs do not count as shared.</p>
  {merge_html}
</section>

<section class="part end" aria-labelledby="method">
  <div class="part-head"><span class="eyebrow">The end</span><h2 id="method">Method and evidence index</h2></div>
  <ul>
    <li>Each dimension was run by its own Drone, which wrote findings, measures, and notes to the run workspace under contract {esc(CONTRACT)}.</li>
    {throwaway_li}
    <li>This brief was rendered from the workspace by code-audit-brief-wasp-drone. It sorts, merges duplicates, and formats; it never adds or edits a finding.</li>
    <li>Repo changes: {esc(repo_changes(run))}.</li>
    <li>Repository code run: {esc(code_execution(run))}.</li>
    <li>This page loads its typefaces from Google Fonts when opened, which shares the reader's IP address with Google; no audit content is sent, and system fonts are used offline.</li>
  </ul>
  {''.join(ev_parts) or '<p class="muted">No evidence index was written.</p>'}
</section>
</main>
<footer class="running"><span>{esc(foot_left)}</span><span>{esc(foot_right)}</span></footer>
"""
    head = f"""<!doctype html>
<html lang="en"{theme_attr}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="generator" content="code-audit-brief-stinger render_brief.py, contract {esc(CONTRACT)}">
<title>{esc(title)}</title>
<link rel="icon" href="{favicon_uri(brand)}">
{pre}
<link rel="stylesheet" href="{esc(brand['fonts']['stylesheet'])}">
<style>
{token_css(brand)}
{BASE_CSS}
{page_footer_css(brand, foot_left, foot_right)}
</style>
</head>
<body>"""
    return head + body + "</body>\n</html>\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Render the Audit My Code brief from a run workspace.")
    ap.add_argument("workspace", type=Path)
    ap.add_argument("--brand", type=Path, default=DEFAULT_BRAND)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--theme", choices=("auto", "light", "dark"), default="auto")
    args = ap.parse_args(argv)
    ws = args.workspace.resolve()
    if not ws.is_dir():
        print(f"error: workspace {ws} is not a directory", file=sys.stderr)
        return 2
    run = load(ws)
    brand = load_brand(args.brand)
    page = build(run, brand, None if args.theme == "auto" else args.theme)
    out = args.out or ws / "brief" / "brief.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out} ({len(page):,} bytes, {len(run.findings)} findings after merge, "
          f"{len(run.merges)} merges, {len(run.issues)} data checks, overall verdict {rollup_verdict({d: str((run.metrics.get(d) or {}).get('verdict') or 'not-run') for d in run.dims if d != 'remediation'})})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
