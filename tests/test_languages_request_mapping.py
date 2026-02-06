from __future__ import annotations

from repo.core.feature_registry import FeatureConfig
from repo.features.languages.generate_languages import (
    DEFAULT_EXCLUDED_LANGUAGES,
    _build_request_from_env,
    _build_request_from_feature_config,
)


def test_build_request_from_feature_config_normalizes_values() -> None:
    config = FeatureConfig(
        token="token-123",
        actor="actor-name",
        username=None,
        readme_path="README.md",
        options={
            "username": "  cute-user  ",
            "output_mode": "VECTOR",
            "excluded_languages": "Python, Go",
            "extra_excluded_languages": "go, Rust",
            "min_percentage": "12.5",
            "max_languages": "6",
        },
    )

    request = _build_request_from_feature_config(config)

    assert request.token == "token-123"
    assert request.username == "cute-user"
    assert request.output_mode == "vector"
    assert request.effective_output_mode == "vector"
    assert request.excluded_languages == ("Python", "Go", "Rust")
    assert request.min_percentage == 12.5
    assert request.max_languages == 6


def test_build_request_from_feature_config_uses_default_exclusions() -> None:
    config = FeatureConfig(token="x", actor="octocat", options={})

    request = _build_request_from_feature_config(config)

    assert request.username == "octocat"
    assert request.excluded_languages == tuple(DEFAULT_EXCLUDED_LANGUAGES)


def test_build_request_from_env_maps_defaults(monkeypatch) -> None:
    monkeypatch.setenv("GITHUB_TOKEN", "env-token")
    monkeypatch.setenv("GITHUB_ACTOR", "env-actor")
    monkeypatch.delenv("LANG_STATS_USERNAME", raising=False)
    monkeypatch.delenv("LANG_STATS_EXCLUDED_LANGUAGES", raising=False)
    monkeypatch.delenv("LANG_STATS_EXTRA_EXCLUDED_LANGUAGES", raising=False)
    monkeypatch.setenv("LANG_STATS_MIN_PERCENTAGE", "9")
    monkeypatch.setenv("LANG_STATS_MAX_LANGUAGES", "4")

    request = _build_request_from_env()

    assert request.token == "env-token"
    assert request.username == "env-actor"
    assert request.output_mode == "text"
    assert request.excluded_languages == tuple(DEFAULT_EXCLUDED_LANGUAGES)
    assert request.min_percentage == 9.0
    assert request.max_languages == 4
