"""
Domain model for a collection of language statistics
"""

from typing import Iterable, Iterator, List
from .language_stat import LanguageStat


class StatsCollection:
    """
    Domain aggregate for managing a collection of language statistics.
    
    Enforces business rules and provides domain operations.
    """
    
    def __init__(self, stats: List[LanguageStat]):
        """
        Initialize with a list of language statistics.
        
        Args:
            stats: List of LanguageStat objects
            
        Raises:
            ValueError: If stats is empty or percentages don't sum to ~100
        """
        if not stats:
            raise ValueError("Stats collection cannot be empty")
        
        self._stats = sorted(stats, key=lambda s: s.percentage, reverse=True)
        self._validate_percentages()
    
    def _validate_percentages(self):
        """Validate that percentages sum to approximately 100%"""
        total = sum(stat.percentage for stat in self._stats)
        if not (99.0 <= total <= 101.0):  # Allow for rounding
            raise ValueError(f"Percentages must sum to ~100%, got {total:.2f}%")

    @staticmethod
    def _normalize(stats: List[LanguageStat]) -> List[LanguageStat]:
        """Normalize percentages to sum to ~100 based on bytes when available."""
        if not stats:
            raise ValueError("Stats collection cannot be empty")

        total_bytes = sum(stat.bytes for stat in stats if stat.bytes > 0)
        if total_bytes > 0:
            return [
                LanguageStat(
                    name=stat.name,
                    percentage=(stat.bytes / total_bytes) * 100,
                    bytes=stat.bytes,
                )
                for stat in stats
            ]

        total_percentage = sum(stat.percentage for stat in stats)
        if total_percentage <= 0:
            raise ValueError("Cannot normalize statistics with zero total percentage")

        return [
            LanguageStat(
                name=stat.name,
                percentage=(stat.percentage / total_percentage) * 100,
                bytes=stat.bytes,
            )
            for stat in stats
        ]

    @classmethod
    def _from_filtered(cls, stats: List[LanguageStat]) -> 'StatsCollection':
        """Create new StatsCollection from filtered stats."""
        normalized = cls._normalize(stats)
        return cls(normalized)
    
    @property
    def stats(self) -> List[LanguageStat]:
        """Get immutable copy of statistics"""
        return list(self._stats)
    
    @property
    def top_language(self) -> LanguageStat:
        """Get the most used language"""
        return self._stats[0]
    
    @property
    def count(self) -> int:
        """Get number of languages"""
        return len(self._stats)
    
    def get_top_n(self, n: int) -> List[LanguageStat]:
        """
        Get top N languages by usage.
        
        Args:
            n: Number of languages to return
            
        Returns:
            List of top N LanguageStat objects
        """
        return self._stats[:n]
    
    def exclude_languages(self, languages: Iterable[str]) -> 'StatsCollection':
        """
        Create a new collection without the specified languages.

        Args:
            languages: Iterable of language names to exclude (case-insensitive)

        Returns:
            New StatsCollection with excluded languages removed and percentages normalized.
        """
        exclusions = {lang.strip().lower() for lang in languages if lang and lang.strip()}
        if not exclusions:
            return self

        filtered = [stat for stat in self._stats if stat.name.lower() not in exclusions]
        if not filtered:
            raise ValueError("All languages were excluded; a minimum of one language is required")

        return self._from_filtered(filtered)

    def filter_by_threshold(self, min_percentage: float) -> 'StatsCollection':
        """
        Get new collection with languages above threshold.
        
        Args:
            min_percentage: Minimum percentage to include
            
        Returns:
            New StatsCollection with filtered stats
        """
        filtered = [s for s in self._stats if s.percentage >= min_percentage]
        if not filtered:
            raise ValueError(f"No languages above {min_percentage}% threshold")
        return self._from_filtered(filtered)

    def limit(self, max_languages: int) -> 'StatsCollection':
        """
        Limit the collection to the top N languages.

        Args:
            max_languages: Maximum number of languages to keep

        Returns:
            New StatsCollection with at most N languages
        """
        if max_languages <= 0:
            raise ValueError("max_languages must be greater than zero")

        if len(self._stats) <= max_languages:
            return self

        limited = self._stats[:max_languages]
        return self._from_filtered(limited)
    
    def to_tuples(self) -> List[tuple]:
        """
        Convert to list of (name, percentage) tuples for backward compatibility.
        
        Returns:
            List of (language_name, percentage) tuples
        """
        return [(stat.name, stat.percentage) for stat in self._stats]
    
    def __iter__(self) -> Iterator[LanguageStat]:
        """Make collection iterable"""
        return iter(self._stats)
    
    def __len__(self) -> int:
        """Get collection length"""
        return len(self._stats)
    
    def __getitem__(self, index: int) -> LanguageStat:
        """Get stat by index"""
        return self._stats[index]
    
    def __str__(self) -> str:
        return f"StatsCollection({self.count} languages)"
    
    def __repr__(self) -> str:
        return f"StatsCollection({self._stats})"

