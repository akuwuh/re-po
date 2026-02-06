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
