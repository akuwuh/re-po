"""Transform raw GitHub data into renderable structures."""

from __future__ import annotations

from typing import List

from .config import RepoConfig
from .model import LanguageStat, RenderOptions, StatsSnapshot


def select_languages(snapshot: StatsSnapshot, opts: RenderOptions, config: RepoConfig) -> List[LanguageStat]:
    """Return the languages to show on the card."""

    limit = opts.max_languages or config.max_languages
    return list(snapshot.iter_percentages(limit=limit))
