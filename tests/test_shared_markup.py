from __future__ import annotations

from repo.core.shared.markup import mono_lines_to_html


def test_mono_lines_to_html_preserves_spaces() -> None:
    html = mono_lines_to_html(["a  b", " c "])
    assert "a&nbsp;&nbsp;b" in html
    assert "&nbsp;c&nbsp;" in html


def test_mono_lines_to_html_wraps_in_samp_block() -> None:
    html = mono_lines_to_html(["row"])
    assert html.startswith("<div align=\"center\">")
    assert "<samp>" in html
    assert "row" in html
    assert html.endswith("</div>")
