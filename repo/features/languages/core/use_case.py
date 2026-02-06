"""
Application use case for executing the languages card.
"""

from __future__ import annotations

from typing import Callable, Iterable, List

from repo.core.feature_registry import FeatureResult

from ..domain import StatsCollection
from .request import LanguagesRequest

FetchStats = Callable[[str], StatsCollection]
RenderTextLines = Callable[[StatsCollection], List[str]]
RenderSvg = Callable[[StatsCollection, str], str]
WriteTextFile = Callable[[str, str], None]
UpdateReadmeSection = Callable[[str, str, str, str], None]
Logger = Callable[[str], None]


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
    _ = (request, fetch_stats, render_text_lines, render_svg, write_text_file, update_readme_section, logger)
    raise NotImplementedError("execute_languages is implemented incrementally")
