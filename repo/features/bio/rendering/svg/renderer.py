"""
SVG renderer for bio card output.
"""

from __future__ import annotations

from typing import Dict

from repo.features.languages.extrusion_styles import ExtrusionStyleFactory

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


def _escape_xml(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


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
        "      font-weight: 500;",
        "      white-space: pre;",
        "      dominant-baseline: middle;",
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
            f'    <text x="{layout.title_x}" y="{layout.title_y}" class="bio-text">{_escape_xml(layout.title_text)}</text>',
        ]
    )

    for row_layout in layout.rows:
        row_text = row_layout.text
        parts.append(
            f'    <text x="{layout.rows_x}" y="{row_layout.y}" class="bio-text">{_escape_xml(row_text)}</text>'
        )

    parts.extend(["  </g>", "</svg>"])
    return "\n".join(parts)
