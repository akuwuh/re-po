#!/usr/bin/env python3
"""
Showcase script for the new DDD-based rendering pipeline.

Runs through text + SVG renderers so designers can visually inspect the cards.
"""

from __future__ import annotations

from pathlib import Path

from re_po.lang_stats.core import RenderConfig
from re_po.lang_stats.domain import LanguageStat, StatsCollection
from re_po.lang_stats.rendering.svg import SVGRenderer
from re_po.lang_stats.rendering.text import TextRenderer

SAMPLE_DATA = [
    ('TypeScript', 34.3),
    ('Python', 33.6),
    ('C', 21.4),
    ('C++', 8.9),
    ('Svelte', 1.2),
]

OUTPUT_DIR = Path(__file__).resolve().parent / 'test_output'


def _build_stats() -> StatsCollection:
    stats = [LanguageStat(name=name, percentage=pct) for name, pct in SAMPLE_DATA]
    return StatsCollection(stats)


def _render_text_block(stats: StatsCollection) -> str:
    renderer = TextRenderer()
    lines = renderer.render(stats)
    html_lines = [line.replace(' ', '&nbsp;') for line in lines]
    stats_html = '<br>\n'.join(html_lines)
    return f'<div align="center">\n<samp>\n{stats_html}\n</samp>\n</div>'


def _render_svg(stats: StatsCollection, theme: str, filename: str) -> Path:
    config = RenderConfig.default_light() if theme == 'light' else RenderConfig.default_dark()
    renderer = SVGRenderer(config)
    svg = renderer.render(stats)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT_DIR / filename
    destination.write_text(svg, encoding='utf-8')
    return destination


def test_output_modes() -> None:
    stats = _build_stats()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("LANG STATS RENDERING SHOWCASE (DDD PIPELINE)")
    print("=" * 80)

    print("\nTEXT MODE (monospace progress bars)")
    print("-" * 80)
    text_block = _render_text_block(stats)
    print(text_block)
    html_path = OUTPUT_DIR / 'sample_text.html'
    html_path.write_text(
        f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Language Stats - Text Mode</title></head>
<body style="font-family:Arial;padding:20px;background:#f5f5f5;">
  <div style="max-width:800px;margin:0 auto;background:white;padding:20px;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);">
    <h1>Language Stats - Text Mode</h1>
    {text_block}
  </div>
</body>
</html>
""",
        encoding='utf-8',
    )
    print(f"✓ Saved text preview: {html_path}")

    print("\nSVG MODE (vector cards)")
    print("-" * 80)
    light_path = _render_svg(stats, 'light', 'sample_light.svg')
    dark_path = _render_svg(stats, 'dark', 'sample_dark.svg')
    print(f"✓ Saved light theme SVG: {light_path}")
    print(f"✓ Saved dark theme SVG:  {dark_path}")

    print("\nDone! Open the generated files for a visual inspection.")
    print(f"  - file://{html_path}")
    print(f"  - file://{light_path}")
    print(f"  - file://{dark_path}")
    print("\nUse this script as a template for future card types.")


if __name__ == '__main__':
    test_output_modes()

