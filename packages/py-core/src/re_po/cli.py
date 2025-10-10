"""Typer CLI entrypoint for re-po."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

import typer

from . import compute, fetcher
from .config import load_config
from .model import FetchOptions, RenderOptions, RenderResult
from .renderer_ascii import render_ascii
from .renderer_svg import render_svg

app = typer.Typer(add_completion=False)


@app.callback()
def main() -> None:
    """Render GitHub stats cards."""
    return None


def render_card(
    *,
    user: str,
    format: str = "txt",
    theme: Optional[str] = None,
    width: Optional[int] = None,
    max_languages: Optional[int] = None,
) -> RenderResult:
    """Shared render pipeline used by CLI, API, and Actions."""

    config_path = os.getenv("RE_PO_CONFIG_PATH")
    config = load_config(config_path)

    render_opts = RenderOptions(
        user=user,
        format=format,  # type: ignore[arg-type]
        theme=theme or config.default_theme,
        width=width,
        max_languages=max_languages or config.max_languages,
    )

    fetch_opts = FetchOptions(user=user, token=os.getenv("GITHUB_TOKEN"))
    snapshot = fetcher.fetch_stats(fetch_opts)

    theme_obj = config.get_theme(render_opts.theme)
    languages = compute.select_languages(snapshot, render_opts, config)

    if render_opts.format == "txt":
        content = render_ascii(languages, theme_obj)
        content_type = "text/plain; charset=utf-8"
    else:
        content = render_svg(languages, theme_obj, width=render_opts.width)
        content_type = "image/svg+xml"

    fingerprint = [
        json.dumps(render_opts.model_dump(), sort_keys=True),
        json.dumps(snapshot.model_dump(), sort_keys=True, default=str),
        json.dumps(theme_obj.model_dump(), sort_keys=True),
    ]
    return RenderResult.from_content(content, content_type, fingerprint_parts=fingerprint)


@app.command("render")
def render(
    user: str = typer.Option(..., help="GitHub username"),
    format: str = typer.Option("txt", case_sensitive=False, help="Output format: txt or svg"),
    theme: Optional[str] = typer.Option(None, help="Theme ID from config"),
    width: Optional[int] = typer.Option(None, help="Optional width override for SVG"),
    out: Optional[Path] = typer.Option(None, help="File path to write output"),
    max_languages: Optional[int] = typer.Option(None, help="Limit number of languages shown"),
):
    """Render a stats card."""

    result = render_card(
        user=user,
        format=format.lower(),
        theme=theme,
        width=width,
        max_languages=max_languages,
    )

    if out:
        out.write_text(result.content)
    else:
        typer.echo(result.content)

    return 0


if __name__ == "__main__":
    app()
