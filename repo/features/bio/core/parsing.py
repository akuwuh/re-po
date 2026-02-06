"""
Input parsing helpers for the bio feature.
"""

from __future__ import annotations

import json
from typing import Iterable, Optional, Tuple

from .request import BioRow


def parse_rows_json(raw_rows: object) -> Tuple[BioRow, ...]:
    if raw_rows in (None, ""):
        raise ValueError("bio_rows is required and must be a JSON array")

    if isinstance(raw_rows, str):
        try:
            decoded = json.loads(raw_rows)
        except json.JSONDecodeError as exc:
            raise ValueError(f"bio_rows must be valid JSON: {exc.msg}") from exc
    else:
        decoded = raw_rows

    if not isinstance(decoded, list):
        raise ValueError("bio_rows must be a JSON array")
    if not decoded:
        raise ValueError("bio_rows must contain at least one row")

    rows = []
    for index, row_data in enumerate(decoded):
        if not isinstance(row_data, dict):
            raise ValueError(f"bio_rows[{index}] must be an object")

        if "label" not in row_data:
            raise ValueError(f"bio_rows[{index}] missing required field: label")
        if "value" not in row_data:
            raise ValueError(f"bio_rows[{index}] missing required field: value")

        rows.append(
            BioRow(
                label=row_data["label"],
                value=row_data["value"],
                align=row_data.get("align", "left"),
                pad=int(row_data.get("pad", 1)),
                prefix=row_data.get("prefix", "// "),
            )
        )

    return tuple(rows)


def parse_bool(value: Optional[object], default: bool = True) -> bool:
    if value in (None, ""):
        return default
    if isinstance(value, bool):
        return value

    normalized = str(value).strip().lower()
    if normalized in ("1", "true", "yes", "on"):
        return True
    if normalized in ("0", "false", "no", "off"):
        return False

    raise ValueError(f"Invalid boolean value: {value}")


def parse_str(value: Optional[object], default: str = "") -> str:
    if value in (None, ""):
        return default
    return str(value)
