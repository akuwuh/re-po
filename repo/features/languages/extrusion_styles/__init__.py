"""Compatibility shim package for shared extrusion strategies."""

from repo.core.shared.extrusion import (
    BackBoxExtrusion,
    ConnectedExtrusion,
    ExtrusionStyle,
    ExtrusionStyleFactory,
)

__all__ = [
    'ExtrusionStyle',
    'ExtrusionStyleFactory',
    'BackBoxExtrusion',
    'ConnectedExtrusion',
]
