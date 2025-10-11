"""Domain models for the stats card pipeline."""

from __future__ import annotations

from datetime import datetime
from hashlib import md5
from typing import Dict, Iterable, Literal, Optional

from pydantic import BaseModel, Field


class Theme(BaseModel):
    """Presentation configuration for the card."""

    id: str
    name: str
    colors: Dict[str, str]
    font_family: str = "DM Mono, monospace"
    font_size: int = 14
    progress_bar_blocks: int = 25
    bar_height: int = 12
    box_padding_x: int = 16
    box_padding_y: int = 20
    line_spacing: int = 10
    lang_name_width: int = 15
    char_width: float = 8.0
    char_height: float = 16.0
    extrusion_depth_x: int = 14
    extrusion_depth_y: int = 14
    extrusion_style: str = "angled"
    stroke_width: int = 2
    corner_radius: int = 8
    ascii_left_padding: int = 2
    ascii_right_padding: int = 3
    ascii_indent_level_1: int = 2
    ascii_indent_level_2: int = 3
    filled_block: str = "█"
    empty_block: str = "░"
    bar_y_offset: int = 6
    bar_width_scale: float = 0.95


class FetchOptions(BaseModel):
    """Inputs used when contacting the GitHub API."""

    user: str
    token: Optional[str] = None
    timeout: float = Field(default=15.0, gt=0)
    per_page: int = Field(default=100, gt=0, le=100)
    include_forks: bool = False


class RepoLanguageBreakdown(BaseModel):
    repo: str
    languages: Dict[str, int]


class StatsSnapshot(BaseModel):
    user: str
    languages: Dict[str, int]
    fetched_at: datetime

    @property
    def total(self) -> int:
        return sum(self.languages.values())

    def iter_percentages(self, limit: Optional[int] = None) -> Iterable["LanguageStat"]:
        total = self.total or 1
        sorted_langs = sorted(self.languages.items(), key=lambda item: item[1], reverse=True)
        if limit is not None:
            sorted_langs = sorted_langs[:limit]

        for name, size in sorted_langs:
            yield LanguageStat(name=name, bytes=size, percentage=round(size / total * 100, 1))


class LanguageStat(BaseModel):
    name: str
    bytes: int
    percentage: float


class RenderOptions(BaseModel):
    user: str
    format: Literal["txt", "svg"] = "txt"
    theme: str = "terminal"
    width: Optional[int] = None
    max_languages: int = 10


class RenderResult(BaseModel):
    content: str
    content_type: str
    etag: str

    @classmethod
    def from_content(cls, content: str, content_type: str, *, fingerprint_parts: Iterable[str]) -> "RenderResult":
        hasher = md5()
        for part in fingerprint_parts:
            hasher.update(part.encode("utf-8"))
        return cls(content=content, content_type=content_type, etag=hasher.hexdigest())
