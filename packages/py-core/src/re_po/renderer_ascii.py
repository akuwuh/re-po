"""ASCII rendering for stats cards."""

from __future__ import annotations

from typing import Iterable, List

from .model import LanguageStat, Theme


def render_ascii(languages: Iterable[LanguageStat], theme: Theme) -> str:
    """Render language stats as an ASCII table."""

    lines: List[str] = []
    for stat in languages:
        lang_display = stat.name.ljust(theme.lang_name_width)
        filled_blocks = round((stat.percentage / 100) * theme.progress_bar_blocks)
        empty_blocks = max(theme.progress_bar_blocks - filled_blocks, 0)
        progress_bar = "█" * filled_blocks + "░" * empty_blocks
        percent_str = f"{stat.percentage:5.1f} %"
        lines.append(f"{lang_display}  {progress_bar}  {percent_str}")

    return "\n".join(lines)
