from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List

from repo.core.feature_registry import FeatureConfig, FeatureResult, register_feature
from repo.core.readme_updater import update_section

from .core import LanguageStatsService, LanguagesRequest, RenderConfig
from .core.parsing import parse_float, parse_int, parse_list
from .core.request import DEFAULT_END_MARKER, DEFAULT_OUTPUT_MODE, DEFAULT_START_MARKER
from .core.use_case import execute_languages
from .domain import StatsCollection
from .rendering.svg import SVGRenderer
from .rendering.text import TextRenderer

DEFAULT_EXCLUDED_LANGUAGES = ['JavaScript', 'HTML', 'CSS', 'SCSS']

def _merge_exclusions(excluded: List[str], extra: List[str]) -> tuple[str, ...]:
    base = excluded or list(DEFAULT_EXCLUDED_LANGUAGES)
    return tuple([*base, *extra])


def _build_request_from_feature_config(config: FeatureConfig) -> LanguagesRequest:
    username = (
        config.options.get('username')
        or config.username
        or config.actor
        or 'akuwuh'
    )
    excluded = parse_list(config.options.get('excluded_languages'))
    extra = parse_list(config.options.get('extra_excluded_languages'))
    return LanguagesRequest(
        token=config.token,
        username=username,
        output_mode=(config.options.get('output_mode') or DEFAULT_OUTPUT_MODE).lower(),
        excluded_languages=_merge_exclusions(excluded, extra),
        min_percentage=parse_float(config.options.get('min_percentage')),
        max_languages=parse_int(config.options.get('max_languages')),
        readme_path=config.options.get('readme_path') or config.readme_path,
        start_marker=config.options.get('start_marker') or DEFAULT_START_MARKER,
        end_marker=config.options.get('end_marker') or DEFAULT_END_MARKER,
    )


def _build_request_from_env() -> LanguagesRequest:
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
    excluded = parse_list(os.environ.get('LANG_STATS_EXCLUDED_LANGUAGES'))
    extra = parse_list(os.environ.get('LANG_STATS_EXTRA_EXCLUDED_LANGUAGES'))
    return LanguagesRequest(
        token=token,
        username=username,
        output_mode=output_mode,
        excluded_languages=_merge_exclusions(excluded, extra),
        min_percentage=parse_float(os.environ.get('LANG_STATS_MIN_PERCENTAGE')),
        max_languages=parse_int(os.environ.get('LANG_STATS_MAX_LANGUAGES')),
        readme_path=os.environ.get('LANG_STATS_README_PATH', 'README.md'),
        start_marker=os.environ.get('LANG_STATS_START_MARKER', DEFAULT_START_MARKER),
        end_marker=os.environ.get('LANG_STATS_END_MARKER', DEFAULT_END_MARKER),
    )


def _run_job(request: LanguagesRequest) -> FeatureResult:
    with LanguageStatsService(github_token=request.token, username=request.username) as service:
        text_renderer = TextRenderer()

        def _fetch_stats(username: str) -> StatsCollection:
            return service.get_stats(username)

        def _render_text_lines(stats: StatsCollection) -> List[str]:
            return text_renderer.render(stats)

        def _render_svg(stats: StatsCollection, theme: str) -> str:
            config = RenderConfig.default_light() if theme == 'light' else RenderConfig.default_dark()
            renderer = SVGRenderer(config)
            return renderer.render(stats)

        def _write_text_file(path: str, content: str) -> None:
            Path(path).write_text(content, encoding='utf-8')

        def _update_readme_section(content: str, readme_path: str, start_marker: str, end_marker: str) -> None:
            update_section(
                content,
                readme_path=readme_path,
                start_marker=start_marker,
                end_marker=end_marker,
            )

        return execute_languages(
            request,
            fetch_stats=_fetch_stats,
            render_text_lines=_render_text_lines,
            render_svg=_render_svg,
            write_text_file=_write_text_file,
            update_readme_section=_update_readme_section,
        )


@register_feature("languages")
def run_feature(config: FeatureConfig) -> FeatureResult:
    return _run_job(_build_request_from_feature_config(config))


def main() -> None:
    """Entry point invoked by the console script."""
    _run_job(_build_request_from_env())


if __name__ == '__main__':
    main()
