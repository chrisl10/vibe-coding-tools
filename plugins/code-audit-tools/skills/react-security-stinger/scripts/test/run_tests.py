#!/usr/bin/env python3
"""Fixture tests for react_version_check.py and sink_scan.py. Run: python3 run_tests.py"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent
FIX = HERE / "fixtures"
REQUIRED = {"id", "dimension", "source", "title", "severity", "confidence", "locations", "evidence",
            "why_it_matters", "remediation", "effort", "refs", "verified_by"}
SEV = ["info", "low", "medium", "high", "critical"]


def materialize(name):
    """Copy a fixture to a temp dir, restoring real file names. Manifests and lockfiles are stored
    with a .fixture suffix so repository dependency scanners do not alert on deliberately old versions."""
    import shutil
    import tempfile
    dst = Path(tempfile.mkdtemp()) / name
    shutil.copytree(FIX / name, dst)
    for f in list(dst.rglob("*.fixture")):
        f.rename(f.with_suffix(""))
    return dst


def run_version(name):
    repo = materialize(name)
    out = subprocess.run([sys.executable, str(SCRIPTS / "react_version_check.py"), "--repo", str(repo)],
                         capture_output=True, text=True, check=True).stdout
    import shutil
    shutil.rmtree(repo.parent, ignore_errors=True)
    return [json.loads(l) for l in out.splitlines() if l.strip()]


def check_contract(findings):
    for f in findings:
        missing = REQUIRED - f.keys()
        assert not missing, f"{f['id']} missing {missing}"
        assert f["id"].startswith("SEC-REACT-")
        assert f["dimension"] == "security" and f["source"] == "react-security-wasp-drone"
        assert f["severity"] in SEV and f["confidence"] in {"confirmed", "likely", "possible"}
        assert f["effort"] in {"S", "M", "L"}
        if f["confidence"] == "possible":
            assert SEV.index(f["severity"]) <= SEV.index("medium"), f"{f['id']} possible above medium"
        assert chr(0x2014) not in json.dumps(f, ensure_ascii=False) and chr(0x2013) not in json.dumps(f, ensure_ascii=False)


def by_pkg(findings):
    return {f["title"].split(" ")[0]: f for f in findings}


cases = {
    "npm-vite-rsc": {"react-server-dom-webpack": ("critical", "likely", "19.2.8"), "@vitejs/plugin-rsc": ("critical", "likely", "0.5.29")},
    "pnpm-router": {"dompurify": ("medium", "likely", "3.4.7"), "react-router": ("high", "likely", "7.18.0")},
    "yarn-classic-cra": {"marked": ("medium", "possible", "18.0.2")},
    "yarn-berry-waku": {"react-server-dom-webpack": ("high", "likely", "19.1.9"), "waku": ("medium", "likely", "1.0.0-beta.1")},
    "clean-rsc": {},
}
fails = 0
for name, expect in cases.items():
    fs = run_version(name)
    try:
        check_contract(fs)
        got = by_pkg(fs)
        for pkg, (sev, conf, fixed) in expect.items():
            assert pkg in got, f"{name}: no finding for {pkg}"
            f = got[pkg]
            assert f["severity"] == sev, f"{name}/{pkg}: severity {f['severity']} != {sev}"
            assert f["confidence"] == conf, f"{name}/{pkg}: confidence {f['confidence']} != {conf}"
            assert f" to {fixed} or later" in f["remediation"], f"{name}/{pkg}: fix {fixed} not in remediation"
        if name == "clean-rsc":
            assert not fs, f"clean fixture produced {len(fs)} findings"
        if name == "yarn-classic-cra":
            assert any("react-scripts" in f["title"] and f["severity"] == "low" for f in fs)
            assert any(f["severity"] == "info" and "React 18.2.0" in f["title"] for f in fs)
        print(f"PASS version {name} ({len(fs)} findings)")
    except AssertionError as e:
        fails += 1
        print(f"FAIL version {name}: {e}")

scan = SCRIPTS / "sink_scan.py"
if scan.exists():
    import shutil
    import tempfile
    tmp = materialize("sinks")
    fake = "sk_" + "live_" + "51" + "FAKEFAKEFAKEFAKEFAKEFAKE"  # assembled at runtime, never a real key
    (tmp / "src" / "keys.js").write_text(f'export const STRIPE = "{fake}";\n', encoding="utf-8")
    out = subprocess.run([sys.executable, str(scan), "--repo", str(tmp)], capture_output=True, text=True, check=True).stdout
    shutil.rmtree(tmp.parent, ignore_errors=True)
    data = json.loads(out)
    hit_ids = {c["check"] for c in data["candidates"]}
    want = {"RX-01", "RX-02", "RX-03", "RX-05", "RS-01", "RC-02", "SD-02", "SD-04", "AR-03", "AR-04"}
    missing = want - hit_ids
    if missing:
        fails += 1
        print(f"FAIL sink_scan: missing {sorted(missing)}; got {sorted(hit_ids)}")
    else:
        print(f"PASS sink_scan ({len(data['candidates'])} candidates)")
    if "sk_live_51FAKE" in out or "sk_l****" not in out:
        fails += 1
        print("FAIL sink_scan: secret not redacted")
# Symlink regression (audit M3): symlinked files and dirs must never be read; fixtures built at run time.
def symlink_case():
    import os
    import shutil
    import tempfile
    base = Path(tempfile.mkdtemp())
    try:
        outside = base / "outside"
        outside.mkdir()
        (outside / "private.tsx").write_text("dangerouslySetInnerHTML={{__html: OUTSIDE_PRIVATE_CONTENT}}\n", encoding="utf-8")
        (outside / "pkgdir").mkdir()
        (outside / "pkgdir" / "leak.tsx").write_text("el.innerHTML = OUTSIDE_DIR_CONTENT;\n", encoding="utf-8")
        repo = base / "repo"
        (repo / "src").mkdir(parents=True)
        (repo / "src" / "ok.tsx").write_text("const a = 1;\n", encoding="utf-8")
        os.symlink(outside / "private.tsx", repo / "src" / "link.tsx")
        os.symlink(outside / "pkgdir", repo / "src" / "linkdir")
        os.symlink("/dev/zero", repo / "src" / "zero.tsx")
        res = subprocess.run([sys.executable, str(SCRIPTS / "sink_scan.py"), "--repo", str(repo)],
                             capture_output=True, text=True, timeout=60, check=True).stdout
        assert "OUTSIDE_PRIVATE_CONTENT" not in res and "OUTSIDE_DIR_CONTENT" not in res, "symlink target was read"
        data = json.loads(res)
        assert data["counts"] == {}, data["counts"]
        assert any("symlink" in c for c in data["caps"]), data["caps"]
        # output inside the repo is refused (audit L3)
        bad = subprocess.run([sys.executable, str(SCRIPTS / "sink_scan.py"), "--repo", str(repo), "--out", str(repo / "o.json")],
                             capture_output=True, text=True)
        assert bad.returncode == 2 and not (repo / "o.json").exists()
        (repo / "package.json").write_text("{}", encoding="utf-8")
        os.symlink(outside / "private.tsx", repo / "package-lock.json")
        vr = subprocess.run([sys.executable, str(SCRIPTS / "react_version_check.py"), "--repo", str(repo)],
                            capture_output=True, text=True, timeout=60)
        assert vr.returncode == 0 and "OUTSIDE_PRIVATE_CONTENT" not in vr.stdout + vr.stderr
        assert "symlink" in vr.stderr, vr.stderr
        print("PASS symlink regression (sink_scan, react_version_check)")
    except AssertionError as e:
        global fails
        fails += 1
        print(f"FAIL symlink regression: {e}")
    finally:
        shutil.rmtree(base, ignore_errors=True)


symlink_case()
sys.exit(1 if fails else 0)
