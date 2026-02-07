"""Style 1: back-box extrusion with no diagonal connectors."""

from __future__ import annotations

from typing import List

from .base import ExtrusionStyle


class BackBoxExtrusion(ExtrusionStyle):
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
        half_stroke = self.stroke_width / 2
        left_side = (
            f'<line x1="{x + extrude_x}" y1="{y + height}" '
            f'x2="{x + extrude_x}" y2="{y + height + extrude_y + half_stroke}" '
            f'stroke="{color}" stroke-width="{self.stroke_width}" />'
        )
        top_side = (
            f'<line x1="{x + width}" y1="{y + extrude_y}" '
            f'x2="{x + width + extrude_x + half_stroke}" y2="{y + extrude_y}" '
            f'stroke="{color}" stroke-width="{self.stroke_width}" />'
        )
        bottom_side = (
            f'<line x1="{x + extrude_x - half_stroke}" y1="{y + height + extrude_y}" '
            f'x2="{x + width + extrude_x + half_stroke}" y2="{y + height + extrude_y}" '
            f'stroke="{color}" stroke-width="{self.stroke_width}" />'
        )
        right_side = (
            f'<line x1="{x + width + extrude_x}" y1="{y + extrude_y - half_stroke}" '
            f'x2="{x + width + extrude_x}" y2="{y + height + extrude_y + half_stroke}" '
            f'stroke="{color}" stroke-width="{self.stroke_width}" />'
        )
        return [left_side, top_side, bottom_side, right_side]
