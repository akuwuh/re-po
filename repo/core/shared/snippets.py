"""Shared snippet composition helpers."""

from __future__ import annotations


def build_picture_snippet(light: str, dark: str, alt: str) -> str:
    return (
        "<picture>\n"
        f'  <source media="(prefers-color-scheme: dark)" srcset="{dark}">\n'
        f'  <source media="(prefers-color-scheme: light)" srcset="{light}">\n'
        f'  <img alt="{alt}" src="{light}">\n'
        "</picture>"
    )
