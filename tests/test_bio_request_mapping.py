from __future__ import annotations

from repo.core.feature_registry import FeatureConfig
from repo.features.bio.generate_bio import (
    _build_request_from_env,
    _build_request_from_feature_config,
)


ROWS_JSON = '[{"label":"age","value":"22"},{"label":"location","value":"toronto, ca","align":"right","pad":2}]'


def test_build_request_from_feature_config_maps_options() -> None:
    config = FeatureConfig(
        token="abc123",
        actor="actor-name",
        readme_path="README.md",
        options={
            "rows": ROWS_JSON,
            "title": "isaac",
            "output_mode": "vector",
            "update_readme": "false",
            "start_marker": "<!--S-->",
            "end_marker": "<!--E-->",
            "svg_light_file": "bio-light.svg",
            "svg_dark_file": "bio-dark.svg",
        },
    )

    request = _build_request_from_feature_config(config)

    assert request.token == "abc123"
    assert request.username == "actor-name"
    assert request.title == "isaac"
    assert request.output_mode == "vector"
    assert request.update_readme is False
    assert request.start_marker == "<!--S-->"
    assert request.end_marker == "<!--E-->"
    assert request.svg_light_file == "bio-light.svg"
    assert request.svg_dark_file == "bio-dark.svg"
    assert len(request.rows) == 2
    assert request.rows[1].align == "right"
    assert request.rows[1].pad == 2


def test_build_request_from_env_maps_defaults(monkeypatch) -> None:
    monkeypatch.setenv("GITHUB_TOKEN", "env-token")
    monkeypatch.setenv("GITHUB_ACTOR", "env-actor")
    monkeypatch.setenv("BIO_ROWS", '[{"label":"learning","value":"infra"}]')
    monkeypatch.delenv("BIO_OUTPUT_MODE", raising=False)
    monkeypatch.delenv("BIO_TITLE", raising=False)

    request = _build_request_from_env()

    assert request.token == "env-token"
    assert request.username == "env-actor"
    assert request.title == "env-actor"
    assert request.output_mode == "vector"
    assert request.update_readme is True
    assert request.readme_path == "README.md"
    assert request.start_marker == "<!--START_SECTION:bio-->"
    assert request.end_marker == "<!--END_SECTION:bio-->"
    assert request.svg_light_file == "bio-card-light.svg"
    assert request.svg_dark_file == "bio-card-dark.svg"
