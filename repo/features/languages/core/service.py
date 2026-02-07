"""
Application service layer
"""

from __future__ import annotations

import warnings
from typing import Optional

from ..domain import StatsCollection
from ..infrastructure import GitHubClient
from ..rendering.svg import SVGRenderer
from ..rendering.text import TextRenderer
from .config import RenderConfig


class LanguageStatsService:
    """
    Compatibility facade for the legacy service-oriented API.

    New feature execution flows through the typed request + use-case boundary.
    """
    
    def __init__(self, github_token: Optional[str] = None, username: Optional[str] = None):
        """
        Initialize service.
        
        Args:
            github_token: GitHub API token
            username: Default GitHub username
        """
        warnings.warn(
            "LanguageStatsService is a compatibility facade. "
            "Prefer the typed use-case flow via run-card/generate_languages.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.github_client = GitHubClient(token=github_token, username=username)
    
    def generate_svg(self, username: Optional[str] = None,
                    config: Optional[RenderConfig] = None) -> str:
        """
        Generate SVG visualization of language statistics.
        
        Args:
            username: GitHub username (uses default if not provided)
            config: Render configuration (uses default if not provided)
            
        Returns:
            SVG string
        """
        warnings.warn(
            "LanguageStatsService.generate_svg is deprecated; use feature use-case flow instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        if config is None:
            config = RenderConfig.default_light()
        
        stats = self.github_client.fetch_language_stats(username)
        renderer = SVGRenderer(config)
        return renderer.render(stats)
    
    def generate_text(self, username: Optional[str] = None) -> list[str]:
        """
        Generate text-based visualization.
        
        Args:
            username: GitHub username
            
        Returns:
            List of formatted text lines
        """
        warnings.warn(
            "LanguageStatsService.generate_text is deprecated; use feature use-case flow instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        stats = self.github_client.fetch_language_stats(username)
        renderer = TextRenderer()
        return renderer.render(stats)
    
    def get_stats(self, username: Optional[str] = None) -> StatsCollection:
        """
        Get raw statistics collection.
        
        Args:
            username: GitHub username
            
        Returns:
            StatsCollection
        """
        warnings.warn(
            "LanguageStatsService.get_stats is deprecated; use GitHubClient directly.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.github_client.fetch_language_stats(username)
    
    def close(self):
        """Close resources"""
        self.github_client.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
