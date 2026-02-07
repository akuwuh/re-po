from __future__ import annotations

from repo.core.shared.snippets import build_picture_snippet


def test_build_picture_snippet_contains_dark_and_light_sources() -> None:
    snippet = build_picture_snippet("light.svg", "dark.svg", "Card")
    assert 'srcset="dark.svg"' in snippet
    assert 'srcset="light.svg"' in snippet
    assert '<img alt="Card" src="light.svg">' in snippet


def test_build_picture_snippet_has_picture_wrapper() -> None:
    snippet = build_picture_snippet("a.svg", "b.svg", "X")
    assert snippet.startswith("<picture>")
    assert snippet.endswith("</picture>")
