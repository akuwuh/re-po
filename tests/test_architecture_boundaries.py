from __future__ import annotations

import ast
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LANGUAGES_ROOT = PROJECT_ROOT / "repo" / "features" / "languages"
LEGACY_ROOT = LANGUAGES_ROOT / "legacy"


def _legacy_imports_in_file(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    violations: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name
                if name == "legacy" or name.startswith("legacy."):
                    violations.append(f"import {name}")
                if name.startswith("repo.features.languages.legacy"):
                    violations.append(f"import {name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module == "legacy" or module.startswith("legacy."):
                violations.append(f"from {module} import ...")
            if module.startswith("repo.features.languages.legacy"):
                violations.append(f"from {module} import ...")
            if node.level > 0 and module.startswith("legacy"):
                violations.append(f"from {'.' * node.level}{module} import ...")

    return violations


def test_no_legacy_imports_outside_legacy_folder() -> None:
    violations: list[str] = []

    for path in LANGUAGES_ROOT.rglob("*.py"):
        if path.is_relative_to(LEGACY_ROOT):
            continue
        found = _legacy_imports_in_file(path)
        for item in found:
            violations.append(f"{path.relative_to(PROJECT_ROOT)} -> {item}")

    assert not violations, "Non-legacy modules must not import legacy:\n" + "\n".join(violations)
