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
    if request.output_mode == "vector":
        logger("Vector mode selected. Generating bio SVG assets...")
        light_svg = render_svg(request, "light")
        dark_svg = render_svg(request, "dark")
        write_text_file(request.svg_light_file, light_svg)
        write_text_file(request.svg_dark_file, dark_svg)
        logger(f"✓ Saved {request.svg_light_file}")
        logger(f"✓ Saved {request.svg_dark_file}")

        snippet = (
            "<picture>\n"
            f'  <source media="(prefers-color-scheme: dark)" srcset="{request.svg_dark_file}">\n'
            f'  <source media="(prefers-color-scheme: light)" srcset="{request.svg_light_file}">\n'
            f'  <img alt="Bio Card" src="{request.svg_light_file}">\n'
            "</picture>"
        )
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

    _ = (render_text_lines,)
    raise NotImplementedError("text mode is implemented incrementally")
