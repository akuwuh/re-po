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


def _cross_feature_imports_in_file(path: Path, owning_feature: str) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    violations: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name
                if not name.startswith("repo.features."):
                    continue
                parts = name.split(".")
                if len(parts) < 3:
                    continue
                target_feature = parts[2]
                if target_feature != owning_feature:
                    violations.append(f"import {name}")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if not module.startswith("repo.features."):
                continue
            parts = module.split(".")
            if len(parts) < 3:
                continue
            target_feature = parts[2]
            if target_feature != owning_feature:
                violations.append(f"from {module} import ...")

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


def test_no_cross_feature_imports() -> None:
    violations: list[str] = []

    for path in FEATURES_ROOT.rglob("*.py"):
        if any(_is_relative_to(path, legacy_root) for legacy_root in LEGACY_ROOTS):
            continue

        relative = path.relative_to(FEATURES_ROOT)
        if len(relative.parts) < 2:
            continue
        owning_feature = relative.parts[0]
        if owning_feature == "__pycache__":
            continue

        found = _cross_feature_imports_in_file(path, owning_feature)
        for item in found:
            violations.append(f"{path.relative_to(PROJECT_ROOT)} -> {item}")

    assert not violations, "Feature modules must not import other features:\n" + "\n".join(violations)


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False
