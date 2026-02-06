"""
Layout primitives for bio SVG rendering.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from ...core.request import BioRequest, BioRow


@dataclass(frozen=True)
class RowLayout:
    row: BioRow
    text: str
    y: float
    is_last: bool


@dataclass(frozen=True)
class BioLayout:
    title_x: float
    title_y: float
    rows_x: float
    box_x: float
    box_y: float
    box_width: float
    box_height: float
    shadow_offset: float
    svg_width: float
    svg_height: float
    char_width: float
    line_height: float
    label_width_chars: int
    value_width_chars: int
    font_size: int
    rows: Tuple[RowLayout, ...]


def _format_row_text(
    row: BioRow,
    *,
    is_last: bool,
    label_width_chars: int,
    value_width_chars: int,
) -> str:
    branch = "└─" if is_last else "├─"
    label_part = row.label.ljust(label_width_chars)
    value_raw = f"{row.prefix}{row.value}"
    if row.align == "right":
        value_part = value_raw.rjust(value_width_chars)
    else:
        value_part = value_raw.ljust(value_width_chars)
    # Match text-mode semantics exactly so SVG and text output stay visually aligned.
    return f"{branch} {label_part}{' ' * row.pad}{value_part}"


def build_layout(request: BioRequest) -> BioLayout:
    font_size = 16
    char_width = 9.6
    line_height = 36.0
    box_x = 20.0
    box_y = 20.0
    shadow_offset = 18.0
    padding_x = 30.0
    padding_y = 18.0

    label_width_chars = max(len(row.label) for row in request.rows)
    value_width_chars = max(len(f"{row.prefix}{row.value}") for row in request.rows)

    title_x = box_x + padding_x
    title_y = box_y + padding_y + line_height
    rows_x = title_x

    row_layouts = []
    max_row_chars = 0
    for index, row in enumerate(request.rows):
        is_last = index == len(request.rows) - 1
        row_text = _format_row_text(
            row,
            is_last=is_last,
            label_width_chars=label_width_chars,
            value_width_chars=value_width_chars,
        )
        max_row_chars = max(max_row_chars, len(row_text))
        row_layouts.append(
            RowLayout(
                row=row,
                text=row_text,
                y=title_y + line_height + (index * line_height),
                is_last=is_last,
            )
        )

    title_width = len(request.title) * char_width
    row_width = max_row_chars * char_width
    content_width = max(title_width, row_width)
    box_width = content_width + (padding_x * 2)
    box_height = (padding_y * 2) + (line_height * (len(request.rows) + 1))

    svg_width = box_width + shadow_offset + 40.0
    svg_height = box_height + shadow_offset + 40.0

    return BioLayout(
        title_x=title_x,
        title_y=title_y,
        rows_x=rows_x,
        box_x=box_x,
        box_y=box_y,
        box_width=box_width,
        box_height=box_height,
        shadow_offset=shadow_offset,
        svg_width=svg_width,
        svg_height=svg_height,
        char_width=char_width,
        line_height=line_height,
        label_width_chars=label_width_chars,
        value_width_chars=value_width_chars,
        font_size=font_size,
        rows=tuple(row_layouts),
    )
