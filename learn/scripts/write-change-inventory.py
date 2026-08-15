#!/usr/bin/env python3
"""Write the exact origin/main to working-tree file inventory for QA."""

from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "learn" / "reports" / "2026-08-14-change-inventory.txt"


def git(*args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, capture_output=True
    )
    return [line for line in result.stdout.splitlines() if line]


def main() -> None:
    tracked = git("diff", "--name-status", "origin/main")
    untracked = [f"A\t{path}" for path in git("ls-files", "--others", "--exclude-standard")]
    entries = sorted(set(tracked + untracked), key=lambda line: line.split("\t")[-1])
    counts: dict[str, int] = {}
    for line in entries:
        status = line.split("\t", 1)[0]
        counts[status] = counts.get(status, 0) + 1
    header = [
        "Vibe Coding Tools change inventory",
        "Base: origin/main",
        f"Entries: {len(entries)}",
        "Status counts: " + ", ".join(f"{key}={value}" for key, value in sorted(counts.items())),
        "",
    ]
    OUTPUT.write_text("\n".join(header + entries) + "\n", encoding="utf-8")
    print(f"Wrote {len(entries)} entries to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
