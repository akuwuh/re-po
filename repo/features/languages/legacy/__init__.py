"""
Legacy compatibility API for the languages feature.

This package is kept for backward compatibility and will be removed in a
future major release.
"""

from __future__ import annotations

import warnings

from .fetcher import fetch_language_stats
from .generator import generate_language_stats
from .readme_updater import update_readme
from .svg_generator import generate_language_stats_svg


def warn_legacy_api(api_name: str) -> None:
    warnings.warn(
        (
            f"`repo.features.languages.legacy.{api_name}` is deprecated and kept only "
            "for compatibility. Prefer `repo.features.languages.core` + "
            "`repo.features.languages.generate_languages`."
        ),
        DeprecationWarning,
        stacklevel=2,
    )


__all__ = [
    "fetch_language_stats",
    "generate_language_stats",
    "generate_language_stats_svg",
    "update_readme",
    "warn_legacy_api",
]
