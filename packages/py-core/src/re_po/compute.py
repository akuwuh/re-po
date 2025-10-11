"""Transform raw GitHub data into renderable structures."""

from __future__ import annotations

from typing import List

from .config import RepoConfig
from .model import LanguageStat, RenderOptions, StatsSnapshot


def select_languages(snapshot: StatsSnapshot, opts: RenderOptions, config: RepoConfig) -> List[LanguageStat]:
    """Return the languages to show on the card."""

    limit = opts.max_languages or config.max_languages
    if limit <= 0:
        return []

    excluded = set(config.excluded_languages)
    filtered = {name: size for name, size in snapshot.languages.items() if name not in excluded and size > 0}
    if not filtered:
        return []

    total = sum(filtered.values()) or 1
    sorted_langs = sorted(filtered.items(), key=lambda item: item[1], reverse=True)

    languages: List[LanguageStat] = []
    for name, size in sorted_langs[:limit]:
        percentage = round((size / total) * 100, 1)
        languages.append(LanguageStat(name=name, bytes=size, percentage=percentage))
    return languages
