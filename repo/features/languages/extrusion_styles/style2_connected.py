"""Compatibility shim for shared style2 extrusion."""

from __future__ import annotations

import warnings

from repo.core.shared.extrusion import ConnectedExtrusion

warnings.warn(
    "repo.features.languages.extrusion_styles.style2_connected is deprecated; "
    "use repo.core.shared.extrusion.style2_connected instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["ConnectedExtrusion"]
