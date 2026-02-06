from __future__ import annotations

import os
import sys

from repo.core.feature_registry import FeatureConfig, FeatureResult, register_feature

from .core import BioRequest
from .core.parsing import parse_bool, parse_rows_json, parse_str
from .core.request import (
    DEFAULT_DARK_FILE,
    DEFAULT_END_MARKER,
    DEFAULT_LIGHT_FILE,
    DEFAULT_OUTPUT_MODE,
    DEFAULT_START_MARKER,
)


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
    _ = config
    raise NotImplementedError("Bio feature adapter is wired incrementally")


def main() -> None:
    if not os.environ.get("GITHUB_TOKEN"):
        print("Error: GITHUB_TOKEN not found")
        sys.exit(1)
    raise NotImplementedError("Bio feature adapter is wired incrementally")


if __name__ == "__main__":
    main()
