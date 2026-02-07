"""Style 2: connected extrusion with diagonal connectors."""

from __future__ import annotations

from typing import List

from .base import ExtrusionStyle


class ConnectedExtrusion(ExtrusionStyle):
    def render_front_face(self, x: float, y: float, width: float, height: float, color: str) -> str:
        return (
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
            f'fill="none" stroke="{color}" stroke-width="{self.stroke_width}" '
            f'rx="{self.corner_radius}" />'
        )

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
        right_face = (
            f'<path d="M {x + width} {y} '
            f'L {x + width + extrude_x} {y + extrude_y} '
            f'L {x + width + extrude_x} {y + height + extrude_y} '
            f'L {x + width} {y + height} Z" '
            f'fill="none" stroke="{color}" stroke-width="{self.stroke_width}" />'
        )
        bottom_face = (
            f'<path d="M {x} {y + height} '
            f'L {x + extrude_x} {y + height + extrude_y} '
            f'L {x + width + extrude_x} {y + height + extrude_y} '
            f'L {x + width} {y + height} Z" '
            f'fill="none" stroke="{color}" stroke-width="{self.stroke_width}" />'
        )
        top_right = (
            f'<line x1="{x + width}" y1="{y}" '
            f'x2="{x + width + extrude_x}" y2="{y + extrude_y}" '
            f'stroke="{color}" stroke-width="{self.stroke_width}" />'
        )
        bottom_left = (
            f'<line x1="{x}" y1="{y + height}" '
            f'x2="{x + extrude_x}" y2="{y + height + extrude_y}" '
            f'stroke="{color}" stroke-width="{self.stroke_width}" />'
        )
        bottom_right = (
            f'<line x1="{x + width}" y1="{y + height}" '
            f'x2="{x + width + extrude_x}" y2="{y + height + extrude_y}" '
            f'stroke="{color}" stroke-width="{self.stroke_width}" />'
        )
        return [right_face, bottom_face, top_right, bottom_left, bottom_right]
