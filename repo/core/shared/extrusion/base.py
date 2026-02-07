"""Base class for shared extrusion styles."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class ExtrusionStyle(ABC):
    """Abstract base class for 3D box extrusion styles."""

    def __init__(self, stroke_width: float, corner_radius: float = 0) -> None:
        self.stroke_width = stroke_width
        self.corner_radius = corner_radius

    @abstractmethod
    def render_front_face(self, x: float, y: float, width: float, height: float, color: str) -> str:
        """Render the front face element."""

    @abstractmethod
    def render_extrusion(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        extrude_x: float,
        extrude_y: float,
        color: str,
    ) -> List[str]:
        """Render extrusion elements."""

    def render(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        extrude_x: float,
        extrude_y: float,
        color: str,
    ) -> List[str]:
        elements = [self.render_front_face(x, y, width, height, color)]
        elements.extend(self.render_extrusion(x, y, width, height, extrude_x, extrude_y, color))
        return elements
