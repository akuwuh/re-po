"""GitHub data fetching utilities."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Dict, Iterable, List

import httpx

from .model import FetchOptions, RepoLanguageBreakdown, StatsSnapshot

GITHUB_API = "https://api.github.com"


def _github_headers(token: str | None) -> Dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "re-po-stats",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_language_breakdowns(opts: FetchOptions) -> List[RepoLanguageBreakdown]:
    """Return language breakdown for each repo owned by the user."""

    params = {
        "per_page": opts.per_page,
        "type": "owner",
        "sort": "updated",
    }

    results: List[RepoLanguageBreakdown] = []
    with httpx.Client(timeout=opts.timeout, headers=_github_headers(opts.token)) as client:
        response = client.get(f"{GITHUB_API}/users/{opts.user}/repos", params=params)
        response.raise_for_status()
        repos = response.json()

        for repo in repos:
            if not opts.include_forks and repo.get("fork"):
                continue

            languages_url = repo.get("languages_url")
            if not languages_url:
                continue

            lang_response = client.get(languages_url)
            lang_response.raise_for_status()
            languages: Dict[str, int] = lang_response.json()

            if not languages:
                continue

            results.append(
                RepoLanguageBreakdown(
                    repo=repo["name"],
                    languages=languages,
                )
            )
    return results


def consolidate_languages(breakdowns: Iterable[RepoLanguageBreakdown], *, user: str) -> StatsSnapshot:
    aggregate: Dict[str, int] = {}
    for breakdown in breakdowns:
        for lang, size in breakdown.languages.items():
            aggregate[lang] = aggregate.get(lang, 0) + int(size)

    return StatsSnapshot(user=user, languages=aggregate, fetched_at=datetime.now(UTC))


def fetch_stats(opts: FetchOptions) -> StatsSnapshot:
    breakdowns = fetch_language_breakdowns(opts)
    return consolidate_languages(breakdowns, user=opts.user)
