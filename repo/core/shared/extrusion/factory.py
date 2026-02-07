"""Factory for shared extrusion style instances."""

from __future__ import annotations

from typing import Dict, List, Type

from .base import ExtrusionStyle
from .style1_back_box import BackBoxExtrusion
from .style2_connected import ConnectedExtrusion


class ExtrusionStyleFactory:
    _styles: Dict[int, Type[ExtrusionStyle]] = {
        1: BackBoxExtrusion,
        2: ConnectedExtrusion,
    }

    @classmethod
    def create(cls, style_number: int, stroke_width: float, corner_radius: float = 0) -> ExtrusionStyle:
        if style_number not in cls._styles:
            available = ", ".join(str(key) for key in sorted(cls._styles))
            raise ValueError(f"Unknown extrusion style: {style_number}. Available styles: {available}")
        return cls._styles[style_number](stroke_width, corner_radius)

    @classmethod
    def register_style(cls, style_number: int, style_class: Type[ExtrusionStyle]) -> None:
        cls._styles[style_number] = style_class

    @classmethod
    def available_styles(cls) -> List[int]:
        return sorted(cls._styles)
