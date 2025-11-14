"""
Utilities for patching README sections between custom markers.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional


def update_section(
    content: str,
    readme_path: str = "README.md",
    start_marker: Optional[str] = None,
    end_marker: Optional[str] = None,
) -> None:
    """
    Replace the content between markers with ``content``.

    Parameters
    ----------
    content:
        HTML/text block to insert.
    readme_path:
        Path to the README file to update.
    start_marker / end_marker:
        Markers delimiting the injected section. If omitted, defaults are
        inferred from the filename (``<!--START_SECTION:languages-->`` etc.).
    """

    path = Path(readme_path)
    if not path.exists():
        raise FileNotFoundError(f"{readme_path} not found")

    start = start_marker or "<!--START_SECTION:languages-->"
    end = end_marker or "<!--END_SECTION:languages-->"

    current = path.read_text(encoding="utf-8")
    if start not in current or end not in current:
        raise ValueError(
            f"Markers not found in {readme_path}. "
            f"Please include {start} and {end}."
        )

    pattern = re.compile(f"{re.escape(start)}.*?{re.escape(end)}", re.DOTALL)
    replacement = f"{start}\n{content}\n{end}"
    updated = pattern.sub(replacement, current)

    path.write_text(updated, encoding="utf-8")


