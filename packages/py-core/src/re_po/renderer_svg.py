from __future__ import annotations

import html
from typing import Iterable, List

from .model import LanguageStat, Theme


SVG_NAMESPACE = "http://www.w3.org/2000/svg"
DEFAULT_MARGIN = 20


def _fmt(value: float) -> str:
    if int(value) == value:
        return str(int(value))
    return f"{value:.2f}".rstrip("0").rstrip(".")


def _prepare_rows(languages: Iterable[LanguageStat], theme: Theme) -> tuple[List[dict], float]:
    rows: List[dict] = []
    max_text_width = 0.0
    placeholder = " " * theme.progress_bar_blocks

    for stat in languages:
        lang_display = stat.name.ljust(theme.lang_name_width)
        line_text = f"{lang_display}  {placeholder}  {stat.percentage:5.1f} %"
        text_width = len(line_text) * theme.char_width
        max_text_width = max(max_text_width, text_width)
        filled_blocks = min(round((stat.percentage / 100) * theme.progress_bar_blocks), theme.progress_bar_blocks)
        rows.append({"stat": stat, "filled_blocks": filled_blocks, "line_text": line_text})

    return rows, max_text_width


def _calculate_dimensions(languages: Iterable[LanguageStat], theme: Theme) -> dict:
    rows, max_text_width = _prepare_rows(languages, theme)

    box_width = max_text_width + (theme.box_padding_x * 2)
    box_height = len(rows) * (theme.char_height + theme.line_spacing) + (theme.box_padding_y * 2)

    extrude_x = max(theme.extrusion_depth_x, 0)
    extrude_y = max(theme.extrusion_depth_y, 0)
    svg_width = box_width + extrude_x + (DEFAULT_MARGIN * 2)
    svg_height = box_height + extrude_y + (DEFAULT_MARGIN * 2)

    return {
        "rows": rows,
        "box_width": box_width,
        "box_height": box_height,
        "svg_width": svg_width,
        "svg_height": svg_height,
    }


def _render_extrusion_elements(theme: Theme, box_x: float, box_y: float, box_width: float, box_height: float) -> List[str]:
    color = theme.colors.get("border", "#000000")
    stroke_width = _fmt(theme.stroke_width)
    rx = _fmt(theme.corner_radius)
    ry = _fmt(theme.corner_radius)

    elements = [
        f'    <rect class="card-bg" x="{_fmt(box_x)}" y="{_fmt(box_y)}" '
        f'width="{_fmt(box_width)}" height="{_fmt(box_height)}" rx="{rx}" ry="{ry}" />'
    ]

    extrude_x = max(theme.extrusion_depth_x, 0)
    extrude_y = max(theme.extrusion_depth_y, 0)
    style = (theme.extrusion_style or "").lower()

    if extrude_x <= 0 or extrude_y <= 0 or style == "none":
        return elements

    if style == "connected":
        elements.append(
            f'    <path d="M {_fmt(box_x + box_width)} {_fmt(box_y)} '
            f'L {_fmt(box_x + box_width + extrude_x)} {_fmt(box_y + extrude_y)} '
            f'L {_fmt(box_x + box_width + extrude_x)} {_fmt(box_y + box_height + extrude_y)} '
            f'L {_fmt(box_x + box_width)} {_fmt(box_y + box_height)} Z" '
            f'fill="none" stroke="{color}" stroke-width="{stroke_width}" />'
        )
        elements.append(
            f'    <path d="M {_fmt(box_x)} {_fmt(box_y + box_height)} '
            f'L {_fmt(box_x + extrude_x)} {_fmt(box_y + box_height + extrude_y)} '
            f'L {_fmt(box_x + box_width + extrude_x)} {_fmt(box_y + box_height + extrude_y)} '
            f'L {_fmt(box_x + box_width)} {_fmt(box_y + box_height)} Z" '
            f'fill="none" stroke="{color}" stroke-width="{stroke_width}" />'
        )
        elements.extend(
            [
                f'    <line x1="{_fmt(box_x + box_width)}" y1="{_fmt(box_y)}" '
                f'x2="{_fmt(box_x + box_width + extrude_x)}" y2="{_fmt(box_y + extrude_y)}" '
                f'stroke="{color}" stroke-width="{stroke_width}" />',
                f'    <line x1="{_fmt(box_x)}" y1="{_fmt(box_y + box_height)}" '
                f'x2="{_fmt(box_x + extrude_x)}" y2="{_fmt(box_y + box_height + extrude_y)}" '
                f'stroke="{color}" stroke-width="{stroke_width}" />',
                f'    <line x1="{_fmt(box_x + box_width)}" y1="{_fmt(box_y + box_height)}" '
                f'x2="{_fmt(box_x + box_width + extrude_x)}" y2="{_fmt(box_y + box_height + extrude_y)}" '
                f'stroke="{color}" stroke-width="{stroke_width}" />',
            ]
        )
        return elements

    # Default to back-box extrusion style
    elements.extend(
        [
            f'    <line x1="{_fmt(box_x + extrude_x)}" y1="{_fmt(box_y + box_height)}" '
            f'x2="{_fmt(box_x + extrude_x)}" y2="{_fmt(box_y + box_height + extrude_y)}" '
            f'stroke="{color}" stroke-width="{stroke_width}" />',
            f'    <line x1="{_fmt(box_x + box_width)}" y1="{_fmt(box_y + extrude_y)}" '
            f'x2="{_fmt(box_x + box_width + extrude_x)}" y2="{_fmt(box_y + extrude_y)}" '
            f'stroke="{color}" stroke-width="{stroke_width}" />',
            f'    <line x1="{_fmt(box_x + extrude_x)}" y1="{_fmt(box_y + box_height + extrude_y)}" '
            f'x2="{_fmt(box_x + box_width + extrude_x)}" y2="{_fmt(box_y + box_height + extrude_y)}" '
            f'stroke="{color}" stroke-width="{stroke_width}" />',
            f'    <line x1="{_fmt(box_x + box_width + extrude_x)}" y1="{_fmt(box_y + extrude_y)}" '
            f'x2="{_fmt(box_x + box_width + extrude_x)}" y2="{_fmt(box_y + box_height + extrude_y)}" '
            f'stroke="{color}" stroke-width="{stroke_width}" />',
        ]
    )
    return elements


def render_svg(languages: Iterable[LanguageStat], theme: Theme, *, width: int | None = None) -> str:
    languages = list(languages)
    if not languages:
        return f'<svg xmlns="{SVG_NAMESPACE}" width="0" height="0"></svg>'

    dims = _calculate_dimensions(languages, theme)
    rows: List[dict] = dims["rows"]

    base_width = dims["svg_width"]
    base_height = dims["svg_height"]
    target_width = float(width) if width else base_width
    scale = target_width / base_width if base_width else 1.0
    target_height = base_height * scale

    pattern_id = f"checkered-pattern-{theme.id}"
    colors = theme.colors
    text_color = colors.get("text", "#000000")
    border_color = colors.get("border", text_color)
    background_color = colors.get("background", "transparent")
    filled_color = colors.get("filled_bar", text_color)

    box_x = DEFAULT_MARGIN
    box_y = DEFAULT_MARGIN

    svg_parts = [
        f'<svg xmlns="{SVG_NAMESPACE}" width="{_fmt(target_width)}" height="{_fmt(target_height)}" '
        f'viewBox="0 0 {_fmt(base_width)} {_fmt(base_height)}">',
        "  <defs>",
        f"    <pattern id=\"{pattern_id}\" x=\"0\" y=\"0\" width=\"4\" height=\"4\" patternUnits=\"userSpaceOnUse\">",
        f"      <rect width=\"2\" height=\"2\" x=\"0\" y=\"0\" fill=\"none\" />",
        f"      <rect width=\"2\" height=\"2\" x=\"2\" y=\"0\" fill=\"{text_color}\" />",
        f"      <rect width=\"2\" height=\"2\" x=\"0\" y=\"2\" fill=\"{text_color}\" />",
        f"      <rect width=\"2\" height=\"2\" x=\"2\" y=\"2\" fill=\"none\" />",
        "    </pattern>",
        "    <style>",
        f"      .lang-text {{ font-family: {theme.font_family}; font-size: {theme.font_size}px; fill: {text_color}; white-space: pre; }}",
        f"      .card-bg {{ fill: {background_color}; stroke: {border_color}; stroke-width: {theme.stroke_width}; }}",
        f"      .bar-filled {{ fill: {filled_color}; }}",
        f"      .bar-empty {{ fill: url(#{pattern_id}); stroke: {border_color}; stroke-width: 0.5; }}",
        "    </style>",
        "  </defs>",
        "  <g id=\"box-borders\">",
    ]

    svg_parts.extend(_render_extrusion_elements(theme, box_x, box_y, dims["box_width"], dims["box_height"]))
    svg_parts.append("  </g>")
    svg_parts.append("  <g id=\"content\">")

    block_width = theme.char_width * theme.bar_width_scale
    bar_width = theme.progress_bar_blocks * block_width
    bar_x_offset = theme.box_padding_x + (theme.lang_name_width + 2) * theme.char_width

    y_pos = box_y + theme.box_padding_y + theme.char_height
    for row in rows:
        stat: LanguageStat = row["stat"]
        lang_text = html.escape(stat.name.ljust(theme.lang_name_width))
        percent_str = f"{stat.percentage:5.1f} %"

        svg_parts.append(
            f"    <text class=\"lang-text\" x=\"{_fmt(box_x + theme.box_padding_x)}\" y=\"{_fmt(y_pos)}\">{lang_text}</text>"
        )

        bar_y = y_pos - theme.char_height + theme.bar_y_offset
        filled_width = max(0.0, min(bar_width, row["filled_blocks"] * block_width))
        empty_width = max(bar_width - filled_width, 0.0)

        if filled_width > 0:
            svg_parts.append(
                f"    <rect class=\"bar-filled\" x=\"{_fmt(box_x + bar_x_offset)}\" y=\"{_fmt(bar_y)}\" "
                f"width=\"{_fmt(filled_width)}\" height=\"{_fmt(theme.bar_height)}\" />"
            )
        if empty_width > 0:
            svg_parts.append(
                f"    <rect class=\"bar-empty\" x=\"{_fmt(box_x + bar_x_offset + filled_width)}\" y=\"{_fmt(bar_y)}\" "
                f"width=\"{_fmt(empty_width)}\" height=\"{_fmt(theme.bar_height)}\" />"
            )

        percent_x = box_x + bar_x_offset + bar_width + (2 * theme.char_width)
        svg_parts.append(
            f"    <text class=\"lang-text\" x=\"{_fmt(percent_x)}\" y=\"{_fmt(y_pos)}\">{percent_str}</text>"
        )

        y_pos += theme.char_height + theme.line_spacing

    svg_parts.append("  </g>")
    svg_parts.append("</svg>")
    return "\n".join(svg_parts)
