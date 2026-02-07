"""
Application use case for executing the bio card.
"""

from __future__ import annotations

from typing import Callable, List

from repo.core.feature_registry import FeatureResult
from repo.core.shared.markup import mono_lines_to_html
from repo.core.shared.snippets import build_picture_snippet

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
    if request.output_mode == "vector":
        logger("Vector mode selected. Generating bio SVG assets...")
        light_svg = render_svg(request, "light")
        dark_svg = render_svg(request, "dark")
        write_text_file(request.svg_light_file, light_svg)
        write_text_file(request.svg_dark_file, dark_svg)
        logger(f"✓ Saved {request.svg_light_file}")
        logger(f"✓ Saved {request.svg_dark_file}")

        snippet = build_picture_snippet(request.svg_light_file, request.svg_dark_file, "Bio Card")
        if request.update_readme:
            update_readme_section(
                snippet,
                request.readme_path,
                request.start_marker,
                request.end_marker,
            )
            logger(f"✓ Updated {request.readme_path}")
        else:
            logger("Skipping README update (update_readme=false).")

        return FeatureResult(
            assets=[request.svg_light_file, request.svg_dark_file],
            summary="Generated bio SVG assets.",
        )

    logger("Text mode selected. Rendering bio snippet...")
    text_lines = render_text_lines(request)
    html_block = mono_lines_to_html(text_lines)
    if request.update_readme:
        update_readme_section(
            html_block,
            request.readme_path,
            request.start_marker,
            request.end_marker,
        )
        logger(f"✓ Updated {request.readme_path}")
    else:
        logger("Skipping README update (update_readme=false).")

    return FeatureResult(
        html_block=html_block,
        start_marker=request.start_marker,
        end_marker=request.end_marker,
        summary="Rendered bio text card.",
    )
