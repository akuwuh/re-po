"""SVG rendering for stats cards."""

from __future__ import annotations

import html
from typing import Iterable

from .model import LanguageStat, Theme


SVG_NAMESPACE = "http://www.w3.org/2000/svg"


def _calculate_dimensions(languages: Iterable[LanguageStat], theme: Theme):
    languages = list(languages)
    max_text_width = 0
    rows = []
    for stat in languages:
        lang_display = stat.name.ljust(theme.lang_name_width)
        line_text = f"{lang_display}  {' ' * theme.progress_bar_blocks}  {stat.percentage:5.1f} %"
        text_width = len(line_text) * theme.char_width
        max_text_width = max(max_text_width, text_width)
        filled_blocks = round((stat.percentage / 100) * theme.progress_bar_blocks)
        rows.append((stat, filled_blocks))

    box_width = max_text_width + (theme.box_padding_x * 2)
    box_height = len(rows) * (theme.char_height + theme.line_spacing) + (theme.box_padding_y * 2)
    svg_width = box_width + theme.extrusion_depth_x + 40
    svg_height = box_height + theme.extrusion_depth_y + 40

    return {
        "rows": rows,
        "box_width": box_width,
        "box_height": box_height,
        "svg_width": svg_width,
        "svg_height": svg_height,
    }


def render_svg(languages: Iterable[LanguageStat], theme: Theme, *, width: int | None = None) -> str:
    languages = list(languages)
    dims = _calculate_dimensions(languages, theme)

    svg_width = width or dims["svg_width"]
    svg_height = dims["svg_height"]

    pattern_id = f"checkered-pattern-{theme.id}"

    bar_x_offset = theme.box_padding_x + (theme.lang_name_width + 2) * theme.char_width
    svg_parts = [
        f'<svg xmlns="{SVG_NAMESPACE}" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">',
        "  <defs>",
        f"    <pattern id=\"{pattern_id}\" width=\"4\" height=\"4\" patternUnits=\"userSpaceOnUse\">",
        f"      <rect width=\"4\" height=\"4\" fill=\"{theme.colors['background']}\" />",
        f"      <path d=\"M0,0 L4,4 M4,0 L0,4\" stroke=\"{theme.colors['text']}\" stroke-width=\"0.5\" opacity=\"0.2\" />",
        "    </pattern>",
        "    <style>",
        f"      .lang-text {{ font-family: {theme.font_family}; font-size: {theme.font_size}px; fill: {theme.colors['text']}; }}",
        f"      .bar-filled {{ fill: {theme.colors['filled_bar']}; }}",
        f"      .bar-empty {{ fill: url(#{pattern_id}); stroke: {theme.colors['text']}; stroke-width: 0.5; opacity: 0.4; }}",
        f"      .card-bg {{ fill: {theme.colors['background']}; stroke: {theme.colors['border']}; stroke-width: {theme.stroke_width}; }}",
        "    </style>",
        "  </defs>",
    ]

    box_x = 20
    box_y = 20

    svg_parts.append(
        f"  <rect class=\"card-bg\" x=\"{box_x}\" y=\"{box_y}\" width=\"{dims['box_width']}\" height=\"{dims['box_height']}\" rx=\"{theme.corner_radius}\" ry=\"{theme.corner_radius}\" />"
    )

    y_pos = box_y + theme.box_padding_y + theme.char_height
    for stat, filled_blocks in dims["rows"]:
        lang_text = html.escape(stat.name.ljust(theme.lang_name_width))
        percent_str = f"{stat.percentage:5.1f} %"
        svg_parts.append(
            f"  <text class=\"lang-text\" x=\"{box_x + theme.box_padding_x}\" y=\"{y_pos}\">{lang_text}</text>"
        )

        bar_y = y_pos - theme.char_height + 6
        bar_width = theme.progress_bar_blocks * theme.char_width * 0.95
        filled_width = filled_blocks * theme.char_width * 0.95
        empty_width = max(bar_width - filled_width, 0)

        if filled_width:
            svg_parts.append(
                f"  <rect class=\"bar-filled\" x=\"{box_x + bar_x_offset}\" y=\"{bar_y}\" width=\"{filled_width}\" height=\"{theme.bar_height}\" />"
            )
        if empty_width:
            svg_parts.append(
                f"  <rect class=\"bar-empty\" x=\"{box_x + bar_x_offset + filled_width}\" y=\"{bar_y}\" width=\"{empty_width}\" height=\"{theme.bar_height}\" />"
            )

        percent_x = box_x + bar_x_offset + bar_width + (2 * theme.char_width)
        svg_parts.append(
            f"  <text class=\"lang-text\" x=\"{percent_x}\" y=\"{y_pos}\">{percent_str}</text>"
        )

        y_pos += theme.char_height + theme.line_spacing

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)
