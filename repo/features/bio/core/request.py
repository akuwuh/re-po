"""
Typed request contract for the bio feature.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Optional, Tuple


DEFAULT_OUTPUT_MODE = "vector"
DEFAULT_START_MARKER = "<!--START_SECTION:bio-->"
DEFAULT_END_MARKER = "<!--END_SECTION:bio-->"
DEFAULT_LIGHT_FILE = "bio-card-light.svg"
DEFAULT_DARK_FILE = "bio-card-dark.svg"


def _normalize_text(value: object) -> str:
    return str(value).strip()


@dataclass(frozen=True)
class BioRow:
    label: str
    value: str
    align: str = "left"
    pad: int = 1
    prefix: str = "// "

    def __post_init__(self) -> None:
        label = _normalize_text(self.label)
        value = _normalize_text(self.value)
        align = _normalize_text(self.align).lower() or "left"
        prefix = str(self.prefix)

        if not label:
            raise ValueError("bio row label is required")
        if not value:
            raise ValueError("bio row value is required")
        if align not in ("left", "right"):
            raise ValueError("bio row align must be 'left' or 'right'")
        if self.pad < 0 or self.pad > 8:
            raise ValueError("bio row pad must be between 0 and 8")

        object.__setattr__(self, "label", label)
        object.__setattr__(self, "value", value)
        object.__setattr__(self, "align", align)
        object.__setattr__(self, "prefix", prefix)


def _normalize_rows(rows: Iterable[BioRow]) -> Tuple[BioRow, ...]:
    normalized = []
    for row in rows:
        if not isinstance(row, BioRow):
            raise ValueError("rows must contain BioRow instances")
        normalized.append(row)
    if not normalized:
        raise ValueError("rows must contain at least one entry")
    return tuple(normalized)


@dataclass(frozen=True)
class BioRequest:
    token: str
    username: str
    rows: Tuple[BioRow, ...] = field(default_factory=tuple)
    title: Optional[str] = None
    output_mode: str = DEFAULT_OUTPUT_MODE
    update_readme: bool = True
    readme_path: str = "README.md"
    start_marker: str = DEFAULT_START_MARKER
    end_marker: str = DEFAULT_END_MARKER
    svg_light_file: str = DEFAULT_LIGHT_FILE
    svg_dark_file: str = DEFAULT_DARK_FILE

    def __post_init__(self) -> None:
        token = _normalize_text(self.token)
        username = _normalize_text(self.username)
        title = _normalize_text(self.title) if self.title is not None else ""
        output_mode = _normalize_text(self.output_mode).lower() or DEFAULT_OUTPUT_MODE
        readme_path = _normalize_text(self.readme_path) or "README.md"
        start_marker = _normalize_text(self.start_marker) or DEFAULT_START_MARKER
        end_marker = _normalize_text(self.end_marker) or DEFAULT_END_MARKER
        light_file = _normalize_text(self.svg_light_file) or DEFAULT_LIGHT_FILE
        dark_file = _normalize_text(self.svg_dark_file) or DEFAULT_DARK_FILE

        if not token:
            raise ValueError("token is required")
        if not username:
            raise ValueError("username is required")
        if output_mode not in ("vector", "text"):
            raise ValueError("output_mode must be 'vector' or 'text'")

        object.__setattr__(self, "token", token)
        object.__setattr__(self, "username", username)
        object.__setattr__(self, "title", title or username)
        object.__setattr__(self, "output_mode", output_mode)
        object.__setattr__(self, "readme_path", readme_path)
        object.__setattr__(self, "start_marker", start_marker)
        object.__setattr__(self, "end_marker", end_marker)
        object.__setattr__(self, "svg_light_file", light_file)
        object.__setattr__(self, "svg_dark_file", dark_file)
        object.__setattr__(self, "rows", _normalize_rows(self.rows))
