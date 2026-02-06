"""
SVG renderer for bio card output.
"""

from __future__ import annotations

from typing import Dict

from ...core.request import BioRequest
from .layout import build_layout


THEME_COLORS: Dict[str, Dict[str, str]] = {
    "light": {
        "bg": "transparent",
        "text": "#111111",
        "border": "#111111",
    },
    "dark": {
        "bg": "transparent",
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
        "      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;",
        f"      font-size: {layout.font_size}px;",
        f'      fill: {colors["text"]};',
        "      font-weight: 500;",
        "      white-space: pre;",
        "      dominant-baseline: middle;",
        "    }",
        "  </style>",
        "",
        "  <g id=\"boxes\">",
        (
            f'    <rect x="{layout.box_x + layout.shadow_offset}" '
            f'y="{layout.box_y + layout.shadow_offset}" '
            f'width="{layout.box_width}" height="{layout.box_height}" '
            f'fill="none" stroke="{colors["border"]}" stroke-width="2" />'
        ),
        (
            f'    <rect x="{layout.box_x}" y="{layout.box_y}" width="{layout.box_width}" '
            f'height="{layout.box_height}" fill="{colors["bg"]}" stroke="{colors["border"]}" stroke-width="2" />'
        ),
        # Connect front/back boxes to preserve the continuous pseudo-3D border look.
        (
            f'    <line x1="{layout.box_x + layout.box_width}" y1="{layout.box_y}" '
            f'x2="{layout.box_x + layout.box_width + layout.shadow_offset}" y2="{layout.box_y}" '
            f'stroke="{colors["border"]}" stroke-width="2" />'
        ),
        (
            f'    <line x1="{layout.box_x + layout.box_width + layout.shadow_offset}" y1="{layout.box_y}" '
            f'x2="{layout.box_x + layout.box_width + layout.shadow_offset}" y2="{layout.box_y + layout.shadow_offset}" '
            f'stroke="{colors["border"]}" stroke-width="2" />'
        ),
        (
            f'    <line x1="{layout.box_x}" y1="{layout.box_y + layout.box_height}" '
            f'x2="{layout.box_x}" y2="{layout.box_y + layout.box_height + layout.shadow_offset}" '
            f'stroke="{colors["border"]}" stroke-width="2" />'
        ),
        (
            f'    <line x1="{layout.box_x}" y1="{layout.box_y + layout.box_height + layout.shadow_offset}" '
            f'x2="{layout.box_x + layout.shadow_offset}" y2="{layout.box_y + layout.box_height + layout.shadow_offset}" '
            f'stroke="{colors["border"]}" stroke-width="2" />'
        ),
        "  </g>",
        "",
        "  <g id=\"content\">",
        f'    <text x="{layout.title_x}" y="{layout.title_y}" class="bio-text">{_escape_xml(request.title)}</text>',
    ]

    for row_layout in layout.rows:
        row_text = row_layout.text
        parts.append(
            f'    <text x="{layout.rows_x}" y="{row_layout.y}" class="bio-text">{_escape_xml(row_text)}</text>'
        )

    parts.extend(["  </g>", "</svg>"])
    return "\n".join(parts)
