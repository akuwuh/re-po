from __future__ import annotations

from repo.features.languages.core.request import LanguagesRequest
from repo.features.languages.core.use_case import execute_languages
from repo.features.languages.domain import LanguageStat, StatsCollection


def _sample_stats() -> StatsCollection:
    return StatsCollection(
        [
            LanguageStat(name="Python", percentage=70.0, bytes=700),
            LanguageStat(name="Rust", percentage=30.0, bytes=300),
        ]
    )


def test_execute_languages_vector_mode() -> None:
    request = LanguagesRequest(
        token="token",
        username="octocat",
        output_mode="vector",
        excluded_languages=(),
    )
    stats = _sample_stats()
    calls = {"fetch": [], "svg": [], "write": [], "update": []}
    logs = []

    def fetch_stats(username: str) -> StatsCollection:
        calls["fetch"].append(username)
        return stats

    def render_text_lines(_: StatsCollection) -> list[str]:
        raise AssertionError("text renderer should not be used in vector mode")

    def render_svg(_: StatsCollection, theme: str) -> str:
        calls["svg"].append(theme)
        return f"<svg data-theme='{theme}'/>"

    def write_text_file(path: str, content: str) -> None:
        calls["write"].append((path, content))

    def update_readme_section(content: str, readme_path: str, start_marker: str, end_marker: str) -> None:
        calls["update"].append((content, readme_path, start_marker, end_marker))

    result = execute_languages(
        request,
        fetch_stats=fetch_stats,
        render_text_lines=render_text_lines,
        render_svg=render_svg,
        write_text_file=write_text_file,
        update_readme_section=update_readme_section,
        logger=logs.append,
    )

    assert calls["fetch"] == ["octocat"]
    assert calls["svg"] == ["light", "dark"]
    assert [item[0] for item in calls["write"]] == ["langs-mono-light.svg", "langs-mono-dark.svg"]
    assert calls["update"] == []
    assert result.assets == ["langs-mono-light.svg", "langs-mono-dark.svg"]
    assert result.summary == "Generated langs-mono SVG assets."


def test_execute_languages_text_mode_updates_readme() -> None:
    request = LanguagesRequest(
        token="token",
        username="octocat",
        output_mode="text",
        excluded_languages=(),
        readme_path="README.md",
        start_marker="<!--A-->",
        end_marker="<!--B-->",
    )
    stats = _sample_stats()
    calls = {"update": [], "write": []}

    def fetch_stats(_: str) -> StatsCollection:
        return stats

    def render_text_lines(_: StatsCollection) -> list[str]:
        return ["Python  ██████████████████░░░░░░░  70.0 %"]

    def render_svg(_: StatsCollection, __: str) -> str:
        raise AssertionError("svg renderer should not be used in text mode")

    def write_text_file(path: str, content: str) -> None:
        calls["write"].append((path, content))

    def update_readme_section(content: str, readme_path: str, start_marker: str, end_marker: str) -> None:
        calls["update"].append((content, readme_path, start_marker, end_marker))

    result = execute_languages(
        request,
        fetch_stats=fetch_stats,
        render_text_lines=render_text_lines,
        render_svg=render_svg,
        write_text_file=write_text_file,
        update_readme_section=update_readme_section,
        logger=lambda _: None,
    )

    assert calls["write"] == []
    assert len(calls["update"]) == 1
    assert "Python&nbsp;&nbsp;██████████████████░░░░░░░&nbsp;&nbsp;70.0&nbsp;%" in calls["update"][0][0]
    assert calls["update"][0][1:] == ("README.md", "<!--A-->", "<!--B-->")
    assert result.summary == "Updated README section."
    assert result.start_marker == "<!--A-->"
    assert result.end_marker == "<!--B-->"


def test_execute_languages_unknown_mode_defaults_to_text() -> None:
    request = LanguagesRequest(
        token="token",
        username="octocat",
        output_mode="other",
        excluded_languages=(),
    )
    stats = _sample_stats()
    logs = []

    result = execute_languages(
        request,
        fetch_stats=lambda _: stats,
        render_text_lines=lambda _: ["row"],
        render_svg=lambda *_: "<svg/>",
        write_text_file=lambda *_: None,
        update_readme_section=lambda *_: None,
        logger=logs.append,
    )

    assert result.summary == "Updated README section."
    assert any("Unknown output_mode 'other'" in line for line in logs)
