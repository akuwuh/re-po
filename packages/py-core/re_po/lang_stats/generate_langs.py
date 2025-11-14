"""
GitHub Language Statistics Generator CLI leveraging the new service architecture.

This script fetches repository language statistics, applies optional filters,
and either writes SVG artifacts or updates README content inline.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Iterable, List, Optional

from .core import LanguageStatsService, RenderConfig
from .domain import StatsCollection
from .rendering.svg import SVGRenderer
from .rendering.text import TextRenderer
from .utils.readme_updater import update_readme_section

DEFAULT_EXCLUDED_LANGUAGES = ['JavaScript', 'HTML', 'CSS', 'SCSS']
DEFAULT_OUTPUT_MODE = 'text'
SVG_LIGHT_FILE = 'langs-mono-light.svg'
SVG_DARK_FILE = 'langs-mono-dark.svg'


def _parse_list_env(name: str) -> List[str]:
    value = os.environ.get(name)
    if value is None:
        return []
    return [item.strip() for item in value.split(',') if item.strip()]


def _parse_float_env(name: str) -> Optional[float]:
    value = os.environ.get(name)
    if value is None or value.strip() == '':
        return None
    try:
        return float(value)
    except ValueError:
        print(f"Warning: Invalid float for {name} ({value}), ignoring.")
        return None


def _parse_int_env(name: str) -> Optional[int]:
    value = os.environ.get(name)
    if value is None or value.strip() == '':
        return None
    try:
        return int(value)
    except ValueError:
        print(f"Warning: Invalid integer for {name} ({value}), ignoring.")
        return None


def _resolve_excluded_languages() -> List[str]:
    base = _parse_list_env('LANG_STATS_EXCLUDED_LANGUAGES')
    base_list = base if base else list(DEFAULT_EXCLUDED_LANGUAGES)
    extras = _parse_list_env('LANG_STATS_EXTRA_EXCLUDED_LANGUAGES')

    normalized = []
    seen = set()
    for name in [*base_list, *extras]:
        lowered = name.lower()
        if lowered not in seen:
            seen.add(lowered)
            normalized.append(name)
    return normalized


def _apply_filters(
    stats: StatsCollection,
    excluded: Iterable[str],
    min_percentage: Optional[float],
    max_languages: Optional[int],
) -> StatsCollection:
    filtered = stats
    if excluded:
        filtered = filtered.exclude_languages(excluded)
    if min_percentage is not None:
        filtered = filtered.filter_by_threshold(min_percentage)
    if max_languages is not None:
        filtered = filtered.limit(max_languages)
    return filtered


def _lines_to_html(lines: List[str]) -> str:
    html_lines = [line.replace(' ', '&nbsp;') for line in lines]
    stats_html = '<br>\n'.join(html_lines)
    return f'<div align="center">\n<samp>\n{stats_html}\n</samp>\n</div>'


def _render_svg(stats: StatsCollection, theme: str, destination: str) -> None:
    config = RenderConfig.default_light() if theme == 'light' else RenderConfig.default_dark()
    renderer = SVGRenderer(config)
    svg_content = renderer.render(stats)
    Path(destination).write_text(svg_content, encoding='utf-8')
    print(f"✓ Saved {destination}")


def _log_stats(stats: StatsCollection) -> None:
    print(f"Found {len(stats)} languages after filtering:")
    for stat in stats:
        print(f"  {stat.name}: {stat.percentage:.1f}%")


def main() -> None:
    """Entry point invoked by the console script."""

    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN not found")
        sys.exit(1)

    username = os.environ.get('GITHUB_ACTOR') or os.environ.get('LANG_STATS_USERNAME') or 'akuwuh'
    output_mode = (os.environ.get('OUTPUT_MODE') or DEFAULT_OUTPUT_MODE).strip().lower()
    excluded_languages = _resolve_excluded_languages()
    min_percentage = _parse_float_env('LANG_STATS_MIN_PERCENTAGE')
    max_languages = _parse_int_env('LANG_STATS_MAX_LANGUAGES')

    readme_path = os.environ.get('LANG_STATS_README_PATH', 'README.md')
    start_marker = os.environ.get('LANG_STATS_START_MARKER')
    end_marker = os.environ.get('LANG_STATS_END_MARKER')

    print(f"Fetching language stats for {username}...")
    with LanguageStatsService(github_token=token, username=username) as service:
        try:
            stats = service.get_stats(username)
        except Exception as exc:
            print(f"Error: failed to fetch language stats - {exc}")
            sys.exit(1)

    try:
        filtered_stats = _apply_filters(stats, excluded_languages, min_percentage, max_languages)
    except ValueError as exc:
        print(f"Error while filtering languages: {exc}")
        sys.exit(1)

    _log_stats(filtered_stats)

    if output_mode == 'vector':
        print("\nVector mode selected. Generating SVG assets...")
        _render_svg(filtered_stats, 'light', SVG_LIGHT_FILE)
        _render_svg(filtered_stats, 'dark', SVG_DARK_FILE)
        print("\nAdd the following snippet to your README:")
        print('<picture>')
        print('  <source media="(prefers-color-scheme: dark)" srcset="langs-mono-dark.svg">')
        print('  <source media="(prefers-color-scheme: light)" srcset="langs-mono-light.svg">')
        print('  <img alt="Language Statistics" src="langs-mono-light.svg">')
        print('</picture>')
        return

    if output_mode not in ('text', ''):
        print(f"Warning: Unknown OUTPUT_MODE '{output_mode}', defaulting to text.")

    print("\nText mode selected. Rendering README snippet...")
    text_renderer = TextRenderer()
    text_lines = text_renderer.render(filtered_stats)
    html_block = _lines_to_html(text_lines)

    try:
        update_readme_section(
            html_block,
            readme_path=readme_path,
            start_marker=start_marker,
            end_marker=end_marker,
        )
        print(f"✓ Updated {readme_path}")
    except Exception as exc:
        print(f"Error updating README: {exc}")
        sys.exit(1)


if __name__ == '__main__':
    main()

