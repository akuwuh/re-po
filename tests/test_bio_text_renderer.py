from __future__ import annotations

from repo.features.bio.core.request import BioRequest, BioRow
from repo.features.bio.rendering.text import render_text_lines


def _request(rows: tuple[BioRow, ...]) -> BioRequest:
    return BioRequest(
        token="token",
        username="isaac",
        title="isaac",
        rows=rows,
        output_mode="text",
    )


def test_text_renderer_preserves_row_order() -> None:
    request = _request(
        (
            BioRow(label="age", value="22"),
            BioRow(label="location", value="toronto"),
            BioRow(label="learning", value="infra"),
        )
    )

    lines = render_text_lines(request)
    assert lines[0] == "isaac"
    assert lines[1].startswith("├ age")
    assert lines[2].startswith("├ location")
    assert lines[3].startswith("└ learning")


def test_text_renderer_applies_alignment_padding_and_prefix() -> None:
    request = _request(
        (
            BioRow(label="short", value="x", align="left", pad=1, prefix="// "),
            BioRow(label="longer", value="123", align="right", pad=3, prefix="=> "),
        )
    )

    lines = render_text_lines(request)
    left_line = lines[1]
    right_line = lines[2]

    assert "// x" in left_line
    assert "=> 123" in right_line
    assert "   " in right_line  # pad=3 contributes visible spacing
