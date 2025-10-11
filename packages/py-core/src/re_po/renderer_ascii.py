"""ASCII rendering for stats cards."""

from __future__ import annotations

from typing import Iterable, List

from .model import LanguageStat, Theme


def _format_content_lines(languages: Iterable[LanguageStat], theme: Theme) -> List[str]:
    lines: List[str] = []
    for stat in languages:
        lang_display = stat.name.ljust(theme.lang_name_width)
        filled_blocks = round((stat.percentage / 100) * theme.progress_bar_blocks)
        empty_blocks = max(theme.progress_bar_blocks - filled_blocks, 0)
        progress_bar = theme.filled_block * filled_blocks + theme.empty_block * empty_blocks
        percent_str = f"{stat.percentage:5.1f} %"
        lines.append(f"{lang_display}  {progress_bar}  {percent_str}")
    return lines


def _draw_simple_border(content_lines: List[str], theme: Theme) -> List[str]:
    if not content_lines:
        return []

    inner_width = theme.ascii_left_padding + max(len(line) for line in content_lines) + theme.ascii_right_padding
    lines: List[str] = [f"┌{'─' * inner_width}┐"]

    for content in content_lines:
        padded = f"{' ' * theme.ascii_left_padding}{content}".ljust(inner_width)
        lines.append(f"│{padded}│")

    lines.append(f"└{'─' * inner_width}┘")
    return lines


def _draw_3d_border(content_lines: List[str], theme: Theme) -> List[str]:
    if not content_lines:
        return []

    inner_width = theme.ascii_left_padding + max(len(line) for line in content_lines) + theme.ascii_right_padding
    lines: List[str] = [f"┌{'─' * inner_width}┐"]

    indent1 = " " * theme.ascii_indent_level_1
    indent2 = " " * theme.ascii_indent_level_2

    for index, content in enumerate(content_lines):
        padded = f"{' ' * theme.ascii_left_padding}{content}".ljust(inner_width)
        if index == 0:
            lines.append(f"{indent1}│{padded}├─┐")
        else:
            lines.append(f"{indent1}│{padded}│ │")

    lines.append(f"{indent1}└┬{'─' * (inner_width - 1)}┘ │")
    lines.append(f"{indent2}└{'─' * (inner_width + 1)}┘")
    return lines


def render_ascii(languages: Iterable[LanguageStat], theme: Theme) -> str:
    """Render language stats using the original bordered layout."""

    content_lines = _format_content_lines(languages, theme)
    if not content_lines:
        return ""

    style = (theme.extrusion_style or "").lower()
    if style == "none":
        box_lines = _draw_simple_border(content_lines, theme)
    else:
        box_lines = _draw_3d_border(content_lines, theme)
    return "\n".join(box_lines)
