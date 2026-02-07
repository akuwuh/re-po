"""Compatibility shim package for shared extrusion strategies."""

from __future__ import annotations

import warnings

from repo.core.shared.extrusion import (
    BackBoxExtrusion,
    ConnectedExtrusion,
    ExtrusionStyle,
    ExtrusionStyleFactory,
)

warnings.warn(
    "repo.features.languages.extrusion_styles is deprecated; "
    "use repo.core.shared.extrusion instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    'ExtrusionStyle',
    'ExtrusionStyleFactory',
    'BackBoxExtrusion',
    'ConnectedExtrusion',
]
