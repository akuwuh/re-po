from __future__ import annotations

from repo.features.bio.core.request import BioRequest, BioRow
from repo.features.bio.core.use_case import execute_bio


def _request(**overrides) -> BioRequest:
    base = BioRequest(
        token="token",
        username="isaac",
        title="isaac",
        rows=(
            BioRow(label="age", value="22"),
            BioRow(label="location", value="toronto"),
        ),
        output_mode="vector",
        update_readme=True,
    )
    data = {**base.__dict__, **overrides}
    return BioRequest(**data)


def test_execute_bio_vector_mode_updates_readme() -> None:
    request = _request(output_mode="vector", update_readme=True)
    calls = {"write": [], "update": []}

    def write_text_file(path: str, content: str) -> None:
        calls["write"].append((path, content))

    def update_readme_section(content: str, readme_path: str, start_marker: str, end_marker: str) -> None:
        calls["update"].append((content, readme_path, start_marker, end_marker))

    result = execute_bio(
        request,
        render_text_lines=lambda _: [],
        render_svg=lambda _, theme: f"<svg data-theme='{theme}'/>",
        write_text_file=write_text_file,
        update_readme_section=update_readme_section,
        logger=lambda _: None,
    )

    assert [item[0] for item in calls["write"]] == [request.svg_light_file, request.svg_dark_file]
    assert len(calls["update"]) == 1
    assert "<picture>" in calls["update"][0][0]
    assert result.assets == [request.svg_light_file, request.svg_dark_file]


def test_execute_bio_vector_mode_can_skip_readme_update() -> None:
    request = _request(output_mode="vector", update_readme=False)
    calls = {"update": []}

    result = execute_bio(
        request,
        render_text_lines=lambda _: [],
        render_svg=lambda _, theme: f"<svg data-theme='{theme}'/>",
        write_text_file=lambda *_: None,
        update_readme_section=lambda *args: calls["update"].append(args),
        logger=lambda _: None,
    )

    assert calls["update"] == []
    assert result.summary == "Generated bio SVG assets."


def test_execute_bio_text_mode_updates_readme() -> None:
    request = _request(output_mode="text", update_readme=True)
    calls = {"update": []}

    result = execute_bio(
        request,
        render_text_lines=lambda _: ["isaac", "└ age // 22"],
        render_svg=lambda *_: "<svg/>",
        write_text_file=lambda *_: None,
        update_readme_section=lambda *args: calls["update"].append(args),
        logger=lambda _: None,
    )

    assert len(calls["update"]) == 1
    assert "isaac" in calls["update"][0][0]
    assert "&nbsp;" in calls["update"][0][0]
    assert result.summary == "Rendered bio text card."
