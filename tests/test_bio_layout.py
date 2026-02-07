from __future__ import annotations

import pytest

from repo.features.bio.core.request import BioRequest, BioRow
from repo.features.bio.rendering.svg.layout import BioLayoutConfig, build_layout


def _request(rows: tuple[BioRow, ...]) -> BioRequest:
    return BioRequest(
        token="token",
        username="isaac",
        title="isaac",
        rows=rows,
        output_mode="vector",
    )


def test_layout_single_row_respects_min_width() -> None:
    request = _request((BioRow(label="age", value="22"),))
    layout = build_layout(request)
    assert layout.box_width >= BioLayoutConfig().min_box_width
    assert len(layout.rows) == 1


def test_layout_expands_for_long_content() -> None:
    request = _request(
        (
            BioRow(label="learning focus", value="distributed systems and observability"),
            BioRow(label="favorite", value="steins;gate"),
        )
    )
    layout = build_layout(request)
    assert layout.box_width > BioLayoutConfig().min_box_width


def test_layout_handles_right_align_and_max_pad() -> None:
    request = _request(
        (
            BioRow(label="location", value="toronto, ca", align="right", pad=8),
            BioRow(label="age", value="22", align="right", pad=8),
        )
    )
    layout = build_layout(request)
    assert len(layout.rows) == 2
    assert all(row.text.startswith("  │  ") for row in layout.rows)


def test_layout_config_validation_rejects_invalid_values() -> None:
    with pytest.raises(ValueError, match="char_width must be positive"):
        BioLayoutConfig(char_width=0)
