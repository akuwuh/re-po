"""Input parsing helpers for the languages feature."""

from __future__ import annotations

from typing import List, Optional


def parse_float(value: Optional[object]) -> Optional[float]:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).strip())
    except (ValueError, AttributeError):
        print(f"Warning: Invalid float '{value}', ignoring.")
        return None


def parse_int(value: Optional[object]) -> Optional[int]:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    try:
        return int(str(value).strip())
    except (ValueError, AttributeError):
        print(f"Warning: Invalid integer '{value}', ignoring.")
        return None


def parse_list(value: Optional[object]) -> List[str]:
    if value in (None, ""):
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value).split(",") if item.strip()]
