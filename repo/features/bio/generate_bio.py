from __future__ import annotations

import os
import sys
from pathlib import Path

from repo.core.feature_registry import FeatureConfig, FeatureResult, register_feature
from repo.core.readme_updater import update_section

from .core import BioRequest
from .core.parsing import parse_bool, parse_rows_json, parse_str
from .core.request import (
    DEFAULT_DARK_FILE,
    DEFAULT_END_MARKER,
    DEFAULT_LIGHT_FILE,
    DEFAULT_OUTPUT_MODE,
    DEFAULT_START_MARKER,
)
from .core.use_case import execute_bio
from .rendering.svg.renderer import render_svg
from .rendering.text import render_text_lines


def _build_request_from_feature_config(config: FeatureConfig) -> BioRequest:
    username = (
        config.options.get("username")
        or config.username
        or config.actor
        or "akuwuh"
    )
    rows = parse_rows_json(config.options.get("rows"))
    return BioRequest(
        token=config.token,
        username=username,
        rows=rows,
        title=parse_str(config.options.get("title"), default=username),
        output_mode=parse_str(config.options.get("output_mode"), default=DEFAULT_OUTPUT_MODE).strip().lower(),
        update_readme=parse_bool(config.options.get("update_readme"), default=True),
        readme_path=parse_str(config.options.get("readme_path"), default=config.readme_path),
        start_marker=parse_str(config.options.get("start_marker"), default=DEFAULT_START_MARKER),
        end_marker=parse_str(config.options.get("end_marker"), default=DEFAULT_END_MARKER),
        svg_light_file=parse_str(config.options.get("svg_light_file"), default=DEFAULT_LIGHT_FILE),
        svg_dark_file=parse_str(config.options.get("svg_dark_file"), default=DEFAULT_DARK_FILE),
    )


def _build_request_from_env() -> BioRequest:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN not found")

    username = (
        os.environ.get("GITHUB_ACTOR")
        or os.environ.get("BIO_USERNAME")
        or "akuwuh"
    )

    return BioRequest(
        token=token,
        username=username,
        rows=parse_rows_json(os.environ.get("BIO_ROWS")),
        title=parse_str(os.environ.get("BIO_TITLE"), default=username),
        output_mode=parse_str(os.environ.get("BIO_OUTPUT_MODE"), default=DEFAULT_OUTPUT_MODE).strip().lower(),
        update_readme=parse_bool(os.environ.get("BIO_UPDATE_README"), default=True),
        readme_path=parse_str(os.environ.get("BIO_README_PATH"), default="README.md"),
        start_marker=parse_str(os.environ.get("BIO_START_MARKER"), default=DEFAULT_START_MARKER),
        end_marker=parse_str(os.environ.get("BIO_END_MARKER"), default=DEFAULT_END_MARKER),
        svg_light_file=parse_str(os.environ.get("BIO_SVG_LIGHT_FILE"), default=DEFAULT_LIGHT_FILE),
        svg_dark_file=parse_str(os.environ.get("BIO_SVG_DARK_FILE"), default=DEFAULT_DARK_FILE),
    )


@register_feature("bio")
def run_feature(config: FeatureConfig) -> FeatureResult:
    return _run_job(_build_request_from_feature_config(config))


def _run_job(request: BioRequest) -> FeatureResult:
    def _write_text_file(path: str, content: str) -> None:
        Path(path).write_text(content, encoding="utf-8")

    def _update_readme_section(content: str, readme_path: str, start_marker: str, end_marker: str) -> None:
        update_section(
            content,
            readme_path=readme_path,
            start_marker=start_marker,
            end_marker=end_marker,
        )

    return execute_bio(
        request,
        render_text_lines=render_text_lines,
        render_svg=render_svg,
        write_text_file=_write_text_file,
        update_readme_section=_update_readme_section,
    )


def main() -> None:
    try:
        request = _build_request_from_env()
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)
    _run_job(request)


if __name__ == "__main__":
    main()
