"""
Utilities for updating README sections with generated content.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

DEFAULT_START_MARKER = '<!--START_SECTION:languages-->'
DEFAULT_END_MARKER = '<!--END_SECTION:languages-->'


def update_readme_section(
    content: str,
    readme_path: str = 'README.md',
    start_marker: Optional[str] = None,
    end_marker: Optional[str] = None,
) -> None:
    """
    Replace the content between markers in the README with the provided block.

    Args:
        content: HTML string to insert.
        readme_path: Path to the README file.
        start_marker: Custom start marker (defaults to <!--START_SECTION:languages-->)
        end_marker: Custom end marker (defaults to <!--END_SECTION:languages-->)
    """
    path = Path(readme_path)
    if not path.exists():
        raise FileNotFoundError(f"{readme_path} not found")

    start = start_marker or DEFAULT_START_MARKER
    end = end_marker or DEFAULT_END_MARKER

    current = path.read_text(encoding='utf-8')
    if start not in current or end not in current:
        raise ValueError(
            f"Markers not found in {readme_path}. Please include {start} and {end}."
        )

    pattern = re.compile(f'{re.escape(start)}.*?{re.escape(end)}', re.DOTALL)
    replacement = f'{start}\n{content}\n{end}'
    updated = pattern.sub(replacement, current)

    path.write_text(updated, encoding='utf-8')

