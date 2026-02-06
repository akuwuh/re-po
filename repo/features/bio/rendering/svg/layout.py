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
    y: float
    is_last: bool


@dataclass(frozen=True)
class BioLayout:
    title_x: float
    title_y: float
    label_x: float
    value_x: float
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
    rows: Tuple[RowLayout, ...]


def build_layout(request: BioRequest) -> BioLayout:
    char_width = 10.0
    line_height = 38.0
    box_x = 20.0
    box_y = 20.0
    shadow_offset = 18.0
    padding_x = 28.0
    padding_y = 22.0

    label_width_chars = max(len(row.label) for row in request.rows)
    value_width_chars = max(len(f"{row.prefix}{row.value}") for row in request.rows)

    title_x = box_x + padding_x
    title_y = box_y + padding_y + line_height
    label_x = box_x + padding_x + (2 * char_width)
    value_x = label_x + (label_width_chars * char_width) + (3 * char_width)

    row_layouts = []
    for index, row in enumerate(request.rows):
        row_layouts.append(
            RowLayout(
                row=row,
                y=title_y + line_height + (index * line_height),
                is_last=index == len(request.rows) - 1,
            )
        )

    title_width = len(request.title) * char_width
    content_right = value_x + (value_width_chars * char_width)
    box_width = max(title_width + (padding_x * 2), (content_right - box_x) + padding_x)
    box_height = (padding_y * 2) + (line_height * (len(request.rows) + 1))

    svg_width = box_width + shadow_offset + 40.0
    svg_height = box_height + shadow_offset + 40.0

    return BioLayout(
        title_x=title_x,
        title_y=title_y,
        label_x=label_x,
        value_x=value_x,
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
        rows=tuple(row_layouts),
    )
