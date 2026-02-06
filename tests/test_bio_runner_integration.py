from __future__ import annotations

from pathlib import Path

from repo.core.runner import run


def test_runner_dispatches_bio_feature(tmp_path: Path) -> None:
    readme_path = tmp_path / "README.md"
    readme_path.write_text(
        "# Demo\n\n<!--START_SECTION:bio-->\nold\n<!--END_SECTION:bio-->\n",
        encoding="utf-8",
    )

    rows = '[{"label":"age","value":"22"},{"label":"location","value":"toronto"}]'
    result = run(
        [
            "--card",
            "bio",
            "--token",
            "token-123",
            "--username",
            "isaac",
            "--readme-path",
            str(readme_path),
            "--option",
            f"rows={rows}",
            "--option",
            "output_mode=text",
        ]
    )

    updated = readme_path.read_text(encoding="utf-8")
    assert result.summary == "Rendered bio text card."
    assert result.html_block is not None
    assert "isaac" in updated
    assert "<!--START_SECTION:bio-->" in updated
    assert "<!--END_SECTION:bio-->" in updated
