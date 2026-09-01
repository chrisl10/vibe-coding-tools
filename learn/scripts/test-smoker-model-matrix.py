#!/usr/bin/env python3
"""Verify that every generated Codex Smoker can resolve its model matrix."""

from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[2]
CANONICAL_MATRIX = ROOT / ".claude" / "model-comparison-matrix.md"
SMOKER_SKILLS = (
    ROOT / ".agents" / "skills" / "the-smoker",
    ROOT / ".codex" / "plugins" / "vibe-coding-tools" / "skills" / "the-smoker",
)
SMOKER_ARCHIVES = (
    (
        ROOT / "learn" / "packages" / "vibe-coding-tools-codex-1.0.1.zip",
        "skills/the-smoker",
    ),
    (
        ROOT / "learn" / "packages" / "vibe-coding-tools-codex-project-1.0.1.zip",
        ".agents/skills/the-smoker",
    ),
)


def assert_smoker_contract(skill_text: str, source: object) -> None:
    assert "references/model-comparison-matrix.md" in skill_text, source
    assert "../../model-comparison-matrix.md" not in skill_text, source
    assert "Do not dispatch any Bee" in skill_text, source
    assert "Do not reuse a ledger selection" in skill_text, source
    assert "silently default to a high-cost model" in skill_text, source
    assert "model identifier and reasoning effort as separate" in skill_text, source


def main() -> None:
    expected_matrix = CANONICAL_MATRIX.read_bytes()

    for skill_dir in SMOKER_SKILLS:
        skill_file = skill_dir / "SKILL.md"
        bundled_matrix = skill_dir / "references" / "model-comparison-matrix.md"
        skill_text = skill_file.read_text(encoding="utf-8")

        assert_smoker_contract(skill_text, skill_file)
        assert bundled_matrix.read_bytes() == expected_matrix, bundled_matrix

    for archive, skill_root in SMOKER_ARCHIVES:
        with ZipFile(archive) as package:
            skill_path = f"{skill_root}/SKILL.md"
            matrix_path = f"{skill_root}/references/model-comparison-matrix.md"
            skill_text = package.read(skill_path).decode("utf-8")
            assert_smoker_contract(skill_text, f"{archive}:{skill_path}")
            assert package.read(matrix_path) == expected_matrix, f"{archive}:{matrix_path}"

    print("Smoker model matrix packaging: PASS")


if __name__ == "__main__":
    main()
