"""
Shared file-system utilities used across features.
"""

from __future__ import annotations

from pathlib import Path
from typing import Union


def ensure_directory(path: Union[str, Path]) -> Path:
    """Ensure the directory exists and return it as a Path."""
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj


def write_file(path: Union[str, Path], content: str, encoding: str = "utf-8") -> Path:
    """Write content to a file, creating parent folders if necessary."""
    destination = Path(path)
    ensure_directory(destination.parent)
    destination.write_text(content, encoding=encoding)
    return destination


def read_file(path: Union[str, Path], encoding: str = "utf-8") -> str:
    """Read file content."""
    return Path(path).read_text(encoding=encoding)


def get_project_root() -> Path:
    """Return the repository root."""
    return Path(__file__).resolve().parents[2]


