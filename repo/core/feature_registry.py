"""
Lightweight registry that exposes feature runners to both the CLI and the
GitHub Action entrypoint.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class FeatureConfig:
    """Normalized data shared with feature runners."""

    token: str
    actor: Optional[str] = None
    username: Optional[str] = None
    readme_path: str = "README.md"
    options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FeatureResult:
    """Return value from a feature run (for logging/reporting)."""

    assets: List[str] = field(default_factory=list)
    html_block: Optional[str] = None
    start_marker: Optional[str] = None
    end_marker: Optional[str] = None
    summary: Optional[str] = None


FeatureHandler = Callable[[FeatureConfig], FeatureResult]
_REGISTRY: Dict[str, FeatureHandler] = {}


def register_feature(name: str) -> Callable[[FeatureHandler], FeatureHandler]:
    """Decorator used by features to register themselves."""

    def decorator(func: FeatureHandler) -> FeatureHandler:
        _REGISTRY[name] = func
        return func

    return decorator


def get_feature(name: str) -> FeatureHandler:
    """Return the handler for ``name``."""

    try:
        return _REGISTRY[name]
    except KeyError as exc:
        known = ", ".join(sorted(_REGISTRY))
        raise KeyError(f"Unknown feature '{name}'. Known features: {known}") from exc


