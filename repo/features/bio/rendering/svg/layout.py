"""
Layout primitives for bio SVG rendering.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from ...core.request import BioRequest, BioRow
from ..text import render_text_lines


@dataclass(frozen=True)
class RowLayout:
    row: BioRow
    text: str
    y: float
    is_last: bool


@dataclass(frozen=True)
class BioLayoutConfig:
    font_size: int = 16
    char_width: float = 9.6
    line_height: float = 28.0
    box_x: float = 20.0
    box_y: float = 20.0
    shadow_offset: float = 15.0
    padding_x: float = 20.0
    padding_y: float = 18.0
    content_right_gutter_chars: int = 6
    min_box_width: float = 280.0

    def __post_init__(self) -> None:
        if self.font_size <= 0:
            raise ValueError("font_size must be positive")
        if self.char_width <= 0:
            raise ValueError("char_width must be positive")
        if self.line_height <= 0:
            raise ValueError("line_height must be positive")
        if self.padding_x < 0 or self.padding_y < 0:
            raise ValueError("padding values must be non-negative")
        if self.content_right_gutter_chars < 0:
            raise ValueError("content_right_gutter_chars must be non-negative")
        if self.min_box_width <= 0:
            raise ValueError("min_box_width must be positive")


@dataclass(frozen=True)
class BioLayout:
    title_text: str
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

def build_layout(request: BioRequest, config: BioLayoutConfig | None = None) -> BioLayout:
    active_config = config or BioLayoutConfig()

    label_width_chars = max(len(row.label) for row in request.rows)
    value_width_chars = max(len(f"{row.prefix}{row.value}") for row in request.rows)

    text_lines = render_text_lines(request)
    title_text = text_lines[0]
    row_text_lines = text_lines[1:]
    max_line_chars = max(len(line) for line in text_lines)

    title_x = active_config.box_x + active_config.padding_x
    title_y = active_config.box_y + active_config.padding_y + active_config.line_height
    rows_x = title_x

    row_layouts = []
    for index, row in enumerate(request.rows):
        is_last = index == len(request.rows) - 1
        row_text = row_text_lines[index]
        row_layouts.append(
            RowLayout(
                row=row,
                text=row_text,
                y=title_y + active_config.line_height + (index * active_config.line_height),
                is_last=is_last,
            )
        )

    content_width = (max_line_chars + active_config.content_right_gutter_chars) * active_config.char_width
    box_width = max(content_width + (active_config.padding_x * 2), active_config.min_box_width)
    box_height = (active_config.padding_y * 2) + (
        active_config.line_height * (len(request.rows) + 1)
    )

    svg_width = box_width + active_config.shadow_offset + 40.0
    svg_height = box_height + active_config.shadow_offset + 40.0

    return BioLayout(
        title_text=title_text,
        title_x=title_x,
        title_y=title_y,
        rows_x=rows_x,
        box_x=active_config.box_x,
        box_y=active_config.box_y,
        box_width=box_width,
        box_height=box_height,
        shadow_offset=active_config.shadow_offset,
        svg_width=svg_width,
        svg_height=svg_height,
        char_width=active_config.char_width,
        line_height=active_config.line_height,
        label_width_chars=label_width_chars,
        value_width_chars=value_width_chars,
        font_size=active_config.font_size,
        rows=tuple(row_layouts),
    )
