"""
Application use case for executing the languages card.
"""

from __future__ import annotations

from typing import Callable, Iterable, List, Optional

from repo.core.feature_registry import FeatureResult

from ..domain import StatsCollection
from .request import LanguagesRequest

FetchStats = Callable[[str], StatsCollection]
RenderTextLines = Callable[[StatsCollection], List[str]]
RenderSvg = Callable[[StatsCollection, str], str]
WriteTextFile = Callable[[str, str], None]
UpdateReadmeSection = Callable[[str, str, str, str], None]
Logger = Callable[[str], None]

SVG_LIGHT_FILE = "langs-mono-light.svg"
SVG_DARK_FILE = "langs-mono-dark.svg"


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
    html_lines = [line.replace(" ", "&nbsp;") for line in lines]
    stats_html = "<br>\n".join(html_lines)
    return f"<div align=\"center\">\n<samp>\n{stats_html}\n</samp>\n</div>"


def execute_languages(
    request: LanguagesRequest,
    *,
    fetch_stats: FetchStats,
    render_text_lines: RenderTextLines,
    render_svg: RenderSvg,
    write_text_file: WriteTextFile,
    update_readme_section: UpdateReadmeSection,
    logger: Logger = print,
) -> FeatureResult:
    """
    Execute the languages feature from a typed request.

    The concrete adapter functions are injected so this use case stays focused
    on orchestration and domain flow.
    """
    logger(f"Fetching language stats for {request.username}...")
    stats = fetch_stats(request.username)
    filtered_stats = _apply_filters(
        stats,
        request.excluded_languages,
        request.min_percentage,
        request.max_languages,
    )
    logger(f"Found {len(filtered_stats)} languages after filtering:")
    for stat in filtered_stats:
        logger(f"  {stat.name}: {stat.percentage:.1f}%")

    if request.effective_output_mode == "vector":
        logger("\nVector mode selected. Generating SVG assets...")
        light_svg = render_svg(filtered_stats, "light")
        dark_svg = render_svg(filtered_stats, "dark")
        write_text_file(SVG_LIGHT_FILE, light_svg)
        write_text_file(SVG_DARK_FILE, dark_svg)
        logger(f"✓ Saved {SVG_LIGHT_FILE}")
        logger(f"✓ Saved {SVG_DARK_FILE}")

        snippet = (
            "<picture>\n"
            '  <source media="(prefers-color-scheme: dark)" srcset="langs-mono-dark.svg">\n'
            '  <source media="(prefers-color-scheme: light)" srcset="langs-mono-light.svg">\n'
            '  <img alt="Language Statistics" src="langs-mono-light.svg">\n'
            "</picture>"
        )
        logger("\nAdd the following snippet to your README:\n")
        logger(snippet)
        return FeatureResult(
            assets=[SVG_LIGHT_FILE, SVG_DARK_FILE],
            summary="Generated langs-mono SVG assets.",
        )

    if request.output_mode not in ("text", ""):
        logger(f"Warning: Unknown output_mode '{request.output_mode}', defaulting to text.")

    logger("\nText mode selected. Rendering README snippet...")
    text_lines = render_text_lines(filtered_stats)
    html_block = _lines_to_html(text_lines)
    update_readme_section(
        html_block,
        request.readme_path,
        request.start_marker,
        request.end_marker,
    )
    logger(f"✓ Updated {request.readme_path}")
    return FeatureResult(
        html_block=html_block,
        start_marker=request.start_marker,
        end_marker=request.end_marker,
        summary="Updated README section.",
    )
