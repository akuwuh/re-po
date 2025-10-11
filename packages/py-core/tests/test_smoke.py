from pathlib import Path

from typer.testing import CliRunner

from re_po.cli import app

runner = CliRunner()
TEST_USER = "akuwuh"


def test_render_txt():
    result = runner.invoke(app, ["render", "--user", TEST_USER, "--format", "txt"])
    assert result.exit_code == 0
    assert "┌" in result.stdout
    assert "%" in result.stdout


def test_render_svg(tmp_path: Path):
    output_file = tmp_path / "card.svg"
    result = runner.invoke(
        app,
        ["render", "--user", TEST_USER, "--format", "svg", "--out", str(output_file)],
    )
    assert result.exit_code == 0
    assert output_file.exists()
    svg = output_file.read_text()
    assert svg.startswith("<svg")
    assert "<pattern" in svg
