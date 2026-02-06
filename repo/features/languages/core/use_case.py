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

    _ = (render_text_lines, render_svg, write_text_file, update_readme_section)
    raise NotImplementedError("execute_languages is implemented incrementally")
