from __future__ import annotations

import ast
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURES_ROOT = PROJECT_ROOT / "repo" / "features"
LEGACY_ROOTS = tuple(path for path in FEATURES_ROOT.rglob("legacy") if path.is_dir())


def _legacy_imports_in_file(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    violations: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name
                if name == "legacy" or name.startswith("legacy."):
                    violations.append(f"import {name}")
                if name.startswith("repo.features.") and ".legacy" in name:
                    violations.append(f"import {name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module == "legacy" or module.startswith("legacy."):
                violations.append(f"from {module} import ...")
            if module.startswith("repo.features.") and ".legacy" in module:
                violations.append(f"from {module} import ...")
            if node.level > 0 and module.startswith("legacy"):
                violations.append(f"from {'.' * node.level}{module} import ...")

    return violations


def test_no_legacy_imports_outside_legacy_folder() -> None:
    violations: list[str] = []

    for path in FEATURES_ROOT.rglob("*.py"):
        if any(
            _is_relative_to(path, legacy_root)
            for legacy_root in LEGACY_ROOTS
        ):
            continue
        found = _legacy_imports_in_file(path)
        for item in found:
            violations.append(f"{path.relative_to(PROJECT_ROOT)} -> {item}")

    assert not violations, "Non-legacy modules must not import legacy:\n" + "\n".join(violations)


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False
