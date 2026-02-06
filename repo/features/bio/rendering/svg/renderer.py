"""
SVG renderer for bio card output.
"""

from __future__ import annotations

from typing import Dict

from ...core.request import BioRequest
from .layout import build_layout


THEME_COLORS: Dict[str, Dict[str, str]] = {
    "light": {
        "bg": "#ffffff",
        "text": "#111111",
        "border": "#111111",
    },
    "dark": {
        "bg": "#0d1117",
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
        "      font-size: 35px;",
        f'      fill: {colors["text"]};',
        "      font-weight: 600;",
        "      dominant-baseline: middle;",
        "    }",
        "  </style>",
        "",
        "  <g id=\"boxes\">",
        (
            f'    <rect x="{layout.box_x + layout.shadow_offset}" '
            f'y="{layout.box_y + layout.shadow_offset}" '
            f'width="{layout.box_width}" height="{layout.box_height}" '
            f'fill="none" stroke="{colors["border"]}" stroke-width="3" />'
        ),
        (
            f'    <rect x="{layout.box_x}" y="{layout.box_y}" width="{layout.box_width}" '
            f'height="{layout.box_height}" fill="{colors["bg"]}" stroke="{colors["border"]}" stroke-width="3" />'
        ),
        "  </g>",
        "",
        "  <g id=\"content\">",
        f'    <text x="{layout.title_x}" y="{layout.title_y}" class="bio-text">{_escape_xml(request.title)}</text>',
    ]

    for row_layout in layout.rows:
        row = row_layout.row
        branch = "└" if row_layout.is_last else "├"
        value_raw = f"{row.prefix}{row.value}"
        if row.align == "right":
            value_text = value_raw.rjust(layout.value_width_chars)
        else:
            value_text = value_raw.ljust(layout.value_width_chars)
        value_x = layout.value_x + ((row.pad - 1) * layout.char_width)

        parts.append(
            f'    <text x="{layout.label_x - (2 * layout.char_width)}" y="{row_layout.y}" class="bio-text">{branch}</text>'
        )
        parts.append(
            f'    <text x="{layout.label_x}" y="{row_layout.y}" class="bio-text">{_escape_xml(row.label)}</text>'
        )
        parts.append(
            f'    <text x="{value_x}" y="{row_layout.y}" class="bio-text">{_escape_xml(value_text)}</text>'
        )

    parts.extend(["  </g>", "</svg>"])
    return "\n".join(parts)
