"""Shared extrusion strategy exports."""

from .base import ExtrusionStyle
from .factory import ExtrusionStyleFactory
from .style1_back_box import BackBoxExtrusion
from .style2_connected import ConnectedExtrusion

__all__ = [
    "ExtrusionStyle",
    "ExtrusionStyleFactory",
    "BackBoxExtrusion",
    "ConnectedExtrusion",
]
