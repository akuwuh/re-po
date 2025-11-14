from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

from repo.core.feature_registry import FeatureConfig, FeatureResult, register_feature
from repo.core.readme_updater import update_section

from .core import LanguageStatsService, RenderConfig
from .domain import StatsCollection
from .rendering.svg import SVGRenderer
from .rendering.text import TextRenderer

DEFAULT_EXCLUDED_LANGUAGES = ['JavaScript', 'HTML', 'CSS', 'SCSS']
DEFAULT_OUTPUT_MODE = 'text'
SVG_LIGHT_FILE = 'langs-mono-light.svg'
SVG_DARK_FILE = 'langs-mono-dark.svg'
DEFAULT_START_MARKER = '<!--START_SECTION:languages-->'
DEFAULT_END_MARKER = '<!--END_SECTION:languages-->'


@dataclass
class LanguageOptions:
    token: str
    username: str
    output_mode: str = DEFAULT_OUTPUT_MODE
    excluded_languages: List[str] = None  # type: ignore[assignment]
    min_percentage: Optional[float] = None
    max_languages: Optional[int] = None
    readme_path: str = 'README.md'
    start_marker: str = DEFAULT_START_MARKER
    end_marker: str = DEFAULT_END_MARKER

    def __post_init__(self) -> None:
        if self.excluded_languages is None:
            self.excluded_languages = list(DEFAULT_EXCLUDED_LANGUAGES)
        else:
            self.excluded_languages = list(self.excluded_languages)


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


def _run_job(options: LanguageOptions) -> FeatureResult:
    print(f"Fetching language stats for {options.username}...")
    with LanguageStatsService(github_token=options.token, username=options.username) as service:
        stats = service.get_stats(options.username)

    filtered_stats = _apply_filters(
        stats,
        [name for name in options.excluded_languages],
        options.min_percentage,
        options.max_languages,
    )
    _log_stats(filtered_stats)

    result = FeatureResult()

    if options.output_mode == 'vector':
        print("\nVector mode selected. Generating SVG assets...")
        _render_svg(filtered_stats, 'light', SVG_LIGHT_FILE)
        _render_svg(filtered_stats, 'dark', SVG_DARK_FILE)
        result.assets.extend([SVG_LIGHT_FILE, SVG_DARK_FILE])
        snippet = (
            '<picture>\n'
            '  <source media="(prefers-color-scheme: dark)" srcset="langs-mono-dark.svg">\n'
            '  <source media="(prefers-color-scheme: light)" srcset="langs-mono-light.svg">\n'
            '  <img alt="Language Statistics" src="langs-mono-light.svg">\n'
            '</picture>'
        )
        print("\nAdd the following snippet to your README:\n")
        print(snippet)
        result.summary = "Generated langs-mono SVG assets."
        return result

    if options.output_mode not in ('text', ''):
        print(f"Warning: Unknown output_mode '{options.output_mode}', defaulting to text.")

    print("\nText mode selected. Rendering README snippet...")
    text_renderer = TextRenderer()
    text_lines = text_renderer.render(filtered_stats)
    html_block = _lines_to_html(text_lines)

    update_section(
            html_block,
        readme_path=options.readme_path,
        start_marker=options.start_marker,
        end_marker=options.end_marker,
        )
    print(f"✓ Updated {options.readme_path}")
    result.html_block = html_block
    result.start_marker = options.start_marker
    result.end_marker = options.end_marker
    result.summary = "Updated README section."
    return result


def _parse_float(value: Optional[object]) -> Optional[float]:
    if value in (None, ''):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).strip())
    except (ValueError, AttributeError):
        print(f"Warning: Invalid float '{value}', ignoring.")
        return None


def _parse_int(value: Optional[object]) -> Optional[int]:
    if value in (None, ''):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    try:
        return int(str(value).strip())
    except (ValueError, AttributeError):
        print(f"Warning: Invalid integer '{value}', ignoring.")
        return None


def _parse_list(value: Optional[object]) -> List[str]:
    if value in (None, ''):
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value).split(',') if item.strip()]


def _build_options_from_env() -> LanguageOptions:
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN not found")
        sys.exit(1)

    username = (
        os.environ.get('GITHUB_ACTOR')
        or os.environ.get('LANG_STATS_USERNAME')
        or 'akuwuh'
    )
    output_mode = (os.environ.get('OUTPUT_MODE') or DEFAULT_OUTPUT_MODE).strip().lower()
    excluded_languages = (
        _parse_list(os.environ.get('LANG_STATS_EXCLUDED_LANGUAGES'))
        or list(DEFAULT_EXCLUDED_LANGUAGES)
    )
    extra = _parse_list(os.environ.get('LANG_STATS_EXTRA_EXCLUDED_LANGUAGES'))
    excluded = excluded_languages + [lang for lang in extra if lang.lower() not in
                                     {item.lower() for item in excluded_languages}]

    return LanguageOptions(
        token=token,
        username=username,
        output_mode=output_mode,
        excluded_languages=excluded,
        min_percentage=_parse_float(os.environ.get('LANG_STATS_MIN_PERCENTAGE')),
        max_languages=_parse_int(os.environ.get('LANG_STATS_MAX_LANGUAGES')),
        readme_path=os.environ.get('LANG_STATS_README_PATH', 'README.md'),
        start_marker=os.environ.get('LANG_STATS_START_MARKER', DEFAULT_START_MARKER),
        end_marker=os.environ.get('LANG_STATS_END_MARKER', DEFAULT_END_MARKER),
    )


@register_feature("languages")
def run_feature(config: FeatureConfig) -> FeatureResult:
    username = (
        config.options.get('username')
        or config.username
        or config.actor
        or 'akuwuh'
    )
    excluded = _parse_list(config.options.get('excluded_languages'))
    extra = _parse_list(config.options.get('extra_excluded_languages'))
    if not excluded:
        excluded = list(DEFAULT_EXCLUDED_LANGUAGES)
    normalized = []
    seen = set()
    for name in [*excluded, *extra]:
        lowered = name.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        normalized.append(name)

    options = LanguageOptions(
        token=config.token,
        username=username,
        output_mode=(config.options.get('output_mode') or DEFAULT_OUTPUT_MODE).lower(),
        excluded_languages=normalized,
        min_percentage=_parse_float(config.options.get('min_percentage')),
        max_languages=_parse_int(config.options.get('max_languages')),
        readme_path=config.options.get('readme_path') or config.readme_path,
        start_marker=config.options.get('start_marker') or DEFAULT_START_MARKER,
        end_marker=config.options.get('end_marker') or DEFAULT_END_MARKER,
    )
    return _run_job(options)


def main() -> None:
    """Entry point invoked by the console script."""
    options = _build_options_from_env()
    _run_job(options)


if __name__ == '__main__':
    main()

