"""Compatibility shim for shared extrusion factory."""

from __future__ import annotations

import warnings

from repo.core.shared.extrusion import ExtrusionStyleFactory

warnings.warn(
    "repo.features.languages.extrusion_styles.factory is deprecated; "
    "use repo.core.shared.extrusion.factory instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["ExtrusionStyleFactory"]
