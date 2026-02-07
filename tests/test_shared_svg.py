from __future__ import annotations

from repo.core.shared.svg import escape_xml


def test_escape_xml_escapes_special_characters() -> None:
    value = "\"<&>'"
    escaped = escape_xml(value)
    assert escaped == "&quot;&lt;&amp;&gt;&apos;"


def test_escape_xml_keeps_plain_text() -> None:
    assert escape_xml("plain text") == "plain text"
