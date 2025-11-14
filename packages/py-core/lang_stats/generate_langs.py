"""
GitHub Language Statistics Generator CLI.

This module fetches repository language statistics and produces either README
content or themed SVG exports depending on the configured output mode.
"""

from __future__ import annotations

import os
import sys

from lang_stats.legacy.fetcher import fetch_language_stats
from lang_stats.legacy.generator import generate_language_stats
from lang_stats.legacy.readme_updater import update_readme


def _to_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    return value.lower() in ('true', '1', 'yes')


def main() -> None:
    """Main workflow: fetch stats, generate box, update README/SVG."""

    token = os.environ.get('GITHUB_TOKEN')
    username = os.environ.get('GITHUB_ACTOR', 'akuwuh')

    output_mode = os.environ.get('OUTPUT_MODE')  # 'text' or 'vector'
    use_graphical_bars = _to_bool(os.environ.get('USE_GRAPHICAL_BARS'))
    svg_theme = os.environ.get('SVG_THEME')  # 'light' or 'dark'

    if not token:
        print("Error: GITHUB_TOKEN not found")
        sys.exit(1)

    print(f"Fetching language stats for {username}...")
    if output_mode:
        print(f"Output mode: {output_mode}")

    lang_stats = fetch_language_stats(username, token)

    if not lang_stats:
        print("No language data found")
        sys.exit(1)

    print(f"Found {len(lang_stats)} languages:")
    for lang, pct in lang_stats:
        print(f"  {lang}: {pct:.1f}%")

    mode_str = output_mode if output_mode else "default (text)"
    print(f"\nGenerating language stats with 3D box (mode: {mode_str})...")

    if output_mode == 'vector':
        print("Vector mode: Generating both light and dark theme SVGs...")

        svg_light = generate_language_stats(
            lang_stats,
            use_3d=True,
            output_mode='vector',
            use_graphical_bars=True if use_graphical_bars is None else use_graphical_bars,
            svg_theme='light',
        )

        svg_dark = generate_language_stats(
            lang_stats,
            use_3d=True,
            output_mode='vector',
            use_graphical_bars=True if use_graphical_bars is None else use_graphical_bars,
            svg_theme='dark',
        )

        svg_light_content = svg_light.replace('<div align="center">\n', '').replace('\n</div>', '')
        svg_dark_content = svg_dark.replace('<div align="center">\n', '').replace('\n</div>', '')

        with open('langs-mono-light.svg', 'w', encoding='utf-8') as f:
            f.write(svg_light_content)
        print("✓ Saved langs-mono-light.svg")

        with open('langs-mono-dark.svg', 'w', encoding='utf-8') as f:
            f.write(svg_dark_content)
        print("✓ Saved langs-mono-dark.svg")

        print("\n✓ Done! SVG files generated successfully.")
        print("\nTo use in README, add:")
        print('<picture>')
        print('  <source media="(prefers-color-scheme: dark)" srcset="langs-mono-dark.svg">')
        print('  <source media="(prefers-color-scheme: light)" srcset="langs-mono-light.svg">')
        print('  <img alt="Language Statistics" src="langs-mono-light.svg">')
        print('</picture>')
    else:
        stats_text = generate_language_stats(
            lang_stats,
            use_3d=True,
            output_mode=output_mode,
            use_graphical_bars=use_graphical_bars,
            svg_theme=svg_theme,
        )

        print("\nGenerated output preview:")
        print(stats_text[:200] + "...")

        print("\nUpdating README.md...")
        update_readme(stats_text)

        print("\n✓ Done! Language stats updated successfully.")


if __name__ == '__main__':
    main()

