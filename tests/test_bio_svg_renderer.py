from __future__ import annotations

from repo.features.bio.core.request import BioRequest, BioRow
from repo.features.bio.rendering.svg.renderer import render_svg


def _request() -> BioRequest:
    return BioRequest(
        token="token",
        username="isaac",
        title="isaac",
        rows=(
            BioRow(label="age", value="22"),
            BioRow(label="location", value="toronto, ca", align="right", pad=2),
        ),
    )


def test_svg_renderer_emits_deterministic_structure() -> None:
    svg = render_svg(_request(), "light")
    assert svg.startswith("<svg ")
    assert "id=\"boxes\"" in svg
    assert "id=\"content\"" in svg
    assert svg.count("<rect ") == 2
    assert svg.count("class=\"bio-text\"") >= 1
    assert "isaac" in svg
    assert "age" in svg
    assert "location" in svg


def test_svg_renderer_uses_theme_palette() -> None:
    light_svg = render_svg(_request(), "light")
    dark_svg = render_svg(_request(), "dark")
    assert 'fill="transparent"' in light_svg
    assert 'fill="transparent"' in dark_svg
    assert "#111111" in light_svg
    assert "#f0f6fc" in dark_svg
