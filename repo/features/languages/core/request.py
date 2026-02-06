"""
Typed request contract for the languages feature use case.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Optional, Tuple


DEFAULT_OUTPUT_MODE = "text"
DEFAULT_START_MARKER = "<!--START_SECTION:languages-->"
DEFAULT_END_MARKER = "<!--END_SECTION:languages-->"


def _normalize_languages(values: Iterable[str]) -> Tuple[str, ...]:
    normalized = []
    seen = set()
    for raw in values:
        name = str(raw).strip()
        if not name:
            continue
        lowered = name.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        normalized.append(name)
    return tuple(normalized)


@dataclass(frozen=True)
class LanguagesRequest:
    token: str
    username: str
    output_mode: str = DEFAULT_OUTPUT_MODE
    excluded_languages: Tuple[str, ...] = field(default_factory=tuple)
    min_percentage: Optional[float] = None
    max_languages: Optional[int] = None
    readme_path: str = "README.md"
    start_marker: str = DEFAULT_START_MARKER
    end_marker: str = DEFAULT_END_MARKER

    def __post_init__(self) -> None:
        token = self.token.strip()
        username = self.username.strip()
        output_mode = (self.output_mode or DEFAULT_OUTPUT_MODE).strip().lower()
        readme_path = (self.readme_path or "README.md").strip()
        start_marker = (self.start_marker or DEFAULT_START_MARKER).strip()
        end_marker = (self.end_marker or DEFAULT_END_MARKER).strip()

        if not token:
            raise ValueError("token is required")
        if not username:
            raise ValueError("username is required")
        if not readme_path:
            raise ValueError("readme_path is required")
        if not start_marker or not end_marker:
            raise ValueError("start_marker and end_marker are required")

        if self.min_percentage is not None and not (0 <= self.min_percentage <= 100):
            raise ValueError("min_percentage must be between 0 and 100")
        if self.max_languages is not None and self.max_languages <= 0:
            raise ValueError("max_languages must be greater than zero")

        object.__setattr__(self, "token", token)
        object.__setattr__(self, "username", username)
        object.__setattr__(self, "output_mode", output_mode)
        object.__setattr__(self, "excluded_languages", _normalize_languages(self.excluded_languages))
        object.__setattr__(self, "readme_path", readme_path)
        object.__setattr__(self, "start_marker", start_marker)
        object.__setattr__(self, "end_marker", end_marker)

    @property
    def effective_output_mode(self) -> str:
        if self.output_mode == "vector":
            return "vector"
        return "text"
