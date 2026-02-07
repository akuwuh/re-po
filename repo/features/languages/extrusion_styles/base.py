"""Compatibility shim for shared extrusion base."""

from __future__ import annotations

import warnings

from repo.core.shared.extrusion import ExtrusionStyle

warnings.warn(
    "repo.features.languages.extrusion_styles.base is deprecated; "
    "use repo.core.shared.extrusion.base instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["ExtrusionStyle"]
