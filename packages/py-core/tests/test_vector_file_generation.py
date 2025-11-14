#!/usr/bin/env python3
"""
Smoke-test for the modern SVG renderer.

It mirrors the GitHub Actions workflow by writing the generated cards to the
repository root (`langs-mono-light.svg` / `langs-mono-dark.svg`).
"""

from __future__ import annotations

from pathlib import Path

from re_po.lang_stats.core import RenderConfig
from re_po.lang_stats.domain import LanguageStat, StatsCollection
from re_po.lang_stats.rendering.svg import SVGRenderer

SAMPLE_DATA = [
    ('TypeScript', 34.3),
    ('Python', 33.6),
    ('C', 21.4),
    ('C++', 8.9),
    ('Svelte', 1.2),
]

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]


def _build_stats() -> StatsCollection:
    stats = [LanguageStat(name=name, percentage=pct) for name, pct in SAMPLE_DATA]
    return StatsCollection(stats)


def _render_svg(stats: StatsCollection, theme: str, filename: str) -> Path:
    config = RenderConfig.default_light() if theme == 'light' else RenderConfig.default_dark()
    renderer = SVGRenderer(config)
    svg = renderer.render(stats)
    destination = WORKSPACE_ROOT / filename
    destination.write_text(svg, encoding='utf-8')
    return destination


def main() -> None:
    stats = _build_stats()
    print("Testing vector renderer output…")
    print("=" * 80)

    light_path = _render_svg(stats, 'light', 'langs-mono-light.svg')
    print(f"✓ Saved light theme SVG: {light_path}")

    dark_path = _render_svg(stats, 'dark', 'langs-mono-dark.svg')
    print(f"✓ Saved dark theme SVG:  {dark_path}")

    print("\nEmbed snippet:")
    print('<picture>')
    print('  <source media="(prefers-color-scheme: dark)" srcset="langs-mono-dark.svg">')
    print('  <source media="(prefers-color-scheme: light)" srcset="langs-mono-light.svg">')
    print('  <img alt="Language Statistics" src="langs-mono-light.svg">')
    print('</picture>')


if __name__ == '__main__':
    main()

