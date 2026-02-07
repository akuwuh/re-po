"""
SVG renderer for bio card output.
"""

from __future__ import annotations

from typing import Dict

from repo.core.shared.extrusion import ExtrusionStyleFactory
from repo.core.shared.svg import escape_xml

from ...core.request import BioRequest
from .layout import build_layout


THEME_COLORS: Dict[str, Dict[str, str]] = {
    "light": {
        "text": "#111111",
        "border": "#111111",
    },
    "dark": {
        "text": "#f0f6fc",
        "border": "#f0f6fc",
    },
}
def render_svg(request: BioRequest, theme: str) -> str:
    colors = THEME_COLORS["dark"] if theme == "dark" else THEME_COLORS["light"]
    layout = build_layout(request)

    parts = [
        f'<svg width="{layout.svg_width}" height="{layout.svg_height}" xmlns="http://www.w3.org/2000/svg">',
        "  <style>",
        "    .bio-text {",
        "      font-family: 'Courier New', Courier, monospace;",
        f"      font-size: {layout.font_size}px;",
        f'      fill: {colors["text"]};',
        "      font-weight: 400;",
        "      white-space: pre;",
        "      dominant-baseline: middle;",
        "    }",
        "    .bio-guides {",
        f'      stroke: {colors["text"]};',
        "      stroke-width: 2;",
        "      fill: none;",
        "      shape-rendering: crispEdges;",
        "    }",
        "  </style>",
        "",
        '  <g id="boxes">',
    ]

    extrusion = ExtrusionStyleFactory.create(style_number=1, stroke_width=2, corner_radius=0)
    border_elements = extrusion.render(
        layout.box_x,
        layout.box_y,
        layout.box_width,
        layout.box_height,
        layout.shadow_offset,
        layout.shadow_offset,
        colors["border"],
    )
    for element in border_elements:
        parts.append(f"    {element}")

    parts.extend(
        [
            "  </g>",
            "",
            '  <g id="content">',
            f'    <line x1="{layout.guide_x}" y1="{layout.trunk_top_y}" x2="{layout.guide_x}" y2="{layout.trunk_bottom_y}" class="bio-guides" />',
            f'    <text x="{layout.title_x}" y="{layout.title_y}" class="bio-text">{escape_xml(layout.title_text)}</text>',
        ]
    )

    for row_layout in layout.rows:
        branch_y1 = row_layout.y - (layout.line_height * 0.22)
        branch_y2 = row_layout.y if row_layout.is_last else row_layout.y + (layout.line_height * 0.22)
        parts.append(
            f'    <line x1="{layout.branch_x}" y1="{row_layout.y}" x2="{layout.branch_end_x}" y2="{row_layout.y}" class="bio-guides" />'
        )
        parts.append(
            f'    <line x1="{layout.branch_x}" y1="{branch_y1}" x2="{layout.branch_x}" y2="{branch_y2}" class="bio-guides" />'
        )
        parts.append(
            f'    <text x="{layout.label_x}" y="{row_layout.y}" class="bio-text">{escape_xml(row_layout.label_text)}</text>'
        )
        parts.append(
            f'    <text x="{row_layout.value_x}" y="{row_layout.y}" class="bio-text">{escape_xml(row_layout.value_text)}</text>'
        )

    parts.extend(["  </g>", "</svg>"])
    return "\n".join(parts)
