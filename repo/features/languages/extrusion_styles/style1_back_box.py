"""
Style 1: Back box extrusion (no diagonal connections)
"""

from typing import List
from .base import ExtrusionStyle


class BackBoxExtrusion(ExtrusionStyle):
    """
    Style 1: Back box extrusion.
    
    Creates the appearance of a box behind the main box without
    diagonal connection lines. This gives a clean, layered look.
    """
    
    def render_front_face(self, x: float, y: float, width: float, height: float, color: str) -> str:
        """Render the front face rectangle."""
        return f'''<rect x="{x}" y="{y}" width="{width}" height="{height}" 
        fill="none" stroke="{color}" stroke-width="{self.stroke_width}" 
        rx="{self.corner_radius}" />'''
    
    def render_extrusion(self, x: float, y: float, width: float, height: float,
                        extrude_x: float, extrude_y: float, color: str) -> List[str]:
        """
        Render the back box extrusion.
        
        Left side: vertical line with height equal to the Y extrusion offset.
        Top side: horizontal line with width equal to the X extrusion offset.
        Bottom side: full bottom edge of the back box.
        Right side: full right edge of the back box.
        
        All lines are adjusted by half the stroke width to ensure corners are flush.
        """
        half_stroke = self.stroke_width / 2
        
        # Left side of back box: vertical line from bottom of front box to bottom of back box
        # Height = extrude_y (Y offset between front and back)
        # Extended by half stroke width at bottom to meet bottom_side
        left_side = f'''<line x1="{x + extrude_x}" y1="{y + height}" 
            x2="{x + extrude_x}" y2="{y + height + extrude_y + half_stroke}" 
            stroke="{color}" stroke-width="{self.stroke_width}" />'''
        
        # Top side of back box: horizontal line from right of front box to right of back box
        # Width = extrude_x (X offset between front and back)
        # Extended by half stroke width at right to meet right_side
        top_side = f'''<line x1="{x + width}" y1="{y + extrude_y}" 
            x2="{x + width + extrude_x + half_stroke}" y2="{y + extrude_y}" 
            stroke="{color}" stroke-width="{self.stroke_width}" />'''
        
        # Bottom side of back box: full bottom edge
        # Extended by half stroke width on both ends to meet left_side and right_side
        bottom_side = f'''<line x1="{x + extrude_x - half_stroke}" y1="{y + height + extrude_y}" 
            x2="{x + width + extrude_x + half_stroke}" y2="{y + height + extrude_y}" 
            stroke="{color}" stroke-width="{self.stroke_width}" />'''
        
        # Right side of back box: full right edge
        # Extended by half stroke width on both ends to meet top_side and bottom_side
        right_side = f'''<line x1="{x + width + extrude_x}" y1="{y + extrude_y - half_stroke}" 
            x2="{x + width + extrude_x}" y2="{y + height + extrude_y + half_stroke}" 
            stroke="{color}" stroke-width="{self.stroke_width}" />'''
        
        return [left_side, top_side, bottom_side, right_side]

