"""
Application use case for executing the bio card.
"""

from __future__ import annotations

from typing import Callable, List

from repo.core.feature_registry import FeatureResult

from .request import BioRequest

RenderTextLines = Callable[[BioRequest], List[str]]
RenderSvg = Callable[[BioRequest, str], str]
WriteTextFile = Callable[[str, str], None]
UpdateReadmeSection = Callable[[str, str, str, str], None]
Logger = Callable[[str], None]


def execute_bio(
    request: BioRequest,
    *,
    render_text_lines: RenderTextLines,
    render_svg: RenderSvg,
    write_text_file: WriteTextFile,
    update_readme_section: UpdateReadmeSection,
    logger: Logger = print,
) -> FeatureResult:
    _ = (request, render_text_lines, render_svg, write_text_file, update_readme_section, logger)
    raise NotImplementedError("execute_bio is implemented incrementally")
