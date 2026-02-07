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
    label_text: str
    value_text: str
    value_x: float
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
    left_margin_chars: int = 2
    guide_to_branch_chars: int = 3
    branch_chars: int = 2
    label_gap_chars: int = 1

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
        if self.left_margin_chars < 0:
            raise ValueError("left_margin_chars must be non-negative")
        if self.guide_to_branch_chars < 0:
            raise ValueError("guide_to_branch_chars must be non-negative")
        if self.branch_chars <= 0:
            raise ValueError("branch_chars must be positive")
        if self.label_gap_chars < 0:
            raise ValueError("label_gap_chars must be non-negative")


@dataclass(frozen=True)
class BioLayout:
    title_text: str
    title_x: float
    title_y: float
    guide_x: float
    branch_x: float
    branch_end_x: float
    label_x: float
    trunk_top_y: float
    trunk_bottom_y: float
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

    base_x = active_config.box_x + active_config.padding_x
    guide_x = base_x + (active_config.left_margin_chars * active_config.char_width)
    branch_x = guide_x + (active_config.guide_to_branch_chars * active_config.char_width)
    label_x = branch_x + (
        (active_config.branch_chars + active_config.label_gap_chars) * active_config.char_width
    )
    title_x = branch_x
    title_y = active_config.box_y + active_config.padding_y + active_config.line_height
    row_count = len(request.rows) + 1

    row_layouts = []
    max_right = title_x + (len(request.title) * active_config.char_width)
    for index, row in enumerate(request.rows):
        is_last = index == len(request.rows) - 1
        value_raw = f"{row.prefix}{row.value}"
        if row.align == "right":
            value_text = value_raw.rjust(value_width_chars)
        else:
            value_text = value_raw.ljust(value_width_chars)
        value_x = label_x + ((label_width_chars + row.pad) * active_config.char_width)
        row_right = value_x + (len(value_text) * active_config.char_width)
        max_right = max(max_right, row_right)
        row_layouts.append(
            RowLayout(
                row=row,
                label_text=row.label,
                value_text=value_text,
                value_x=value_x,
                y=title_y + active_config.line_height + (index * active_config.line_height),
                is_last=is_last,
            )
        )

    branch_end_x = label_x - (active_config.char_width * 0.5)
    content_right = max_right + (active_config.content_right_gutter_chars * active_config.char_width)
    box_width = max((content_right - active_config.box_x) + active_config.padding_x, active_config.min_box_width)
    box_height = (active_config.padding_y * 2) + (active_config.line_height * row_count)
    trunk_top_y = title_y - (active_config.line_height * 0.45)
    trunk_bottom_y = row_layouts[-1].y

    svg_width = box_width + active_config.shadow_offset + 40.0
    svg_height = box_height + active_config.shadow_offset + 40.0

    return BioLayout(
        title_text=request.title,
        title_x=title_x,
        title_y=title_y,
        guide_x=guide_x,
        branch_x=branch_x,
        branch_end_x=branch_end_x,
        label_x=label_x,
        trunk_top_y=trunk_top_y,
        trunk_bottom_y=trunk_bottom_y,
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
