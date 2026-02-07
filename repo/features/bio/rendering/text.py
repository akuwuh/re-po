"""
Text rendering for the bio card.
"""

from __future__ import annotations

from typing import List

from ..core.request import BioRequest, BioRow

LEFT_MARGIN = "  "
VERTICAL_GUIDE = "│  "


def _render_row(row: BioRow, *, is_last: bool, label_width: int, value_width: int) -> str:
    branch = "└─" if is_last else "├─"
    label_part = row.label.ljust(label_width)
    value_raw = f"{row.prefix}{row.value}"
    if row.align == "right":
        value_part = value_raw.rjust(value_width)
    else:
        value_part = value_raw.ljust(value_width)
    spacing = " " * row.pad
    # Match the reference layout: rows are indented and show a vertical guide.
    return f"{LEFT_MARGIN}{VERTICAL_GUIDE}{branch} {label_part}{spacing}{value_part}"


def render_text_lines(request: BioRequest) -> List[str]:
    label_width = max(len(row.label) for row in request.rows)
    value_width = max(len(f"{row.prefix}{row.value}") for row in request.rows)

    lines = [f"{LEFT_MARGIN}{VERTICAL_GUIDE}{request.title}"]
    for index, row in enumerate(request.rows):
        lines.append(
            _render_row(
                row,
                is_last=index == len(request.rows) - 1,
                label_width=label_width,
                value_width=value_width,
            )
        )
    return lines
