"""Compatibility shim for shared style1 extrusion."""

from __future__ import annotations

import warnings

from repo.core.shared.extrusion import BackBoxExtrusion

warnings.warn(
    "repo.features.languages.extrusion_styles.style1_back_box is deprecated; "
    "use repo.core.shared.extrusion.style1_back_box instead.",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["BackBoxExtrusion"]
