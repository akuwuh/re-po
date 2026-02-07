"""Shared markup helpers."""

from __future__ import annotations

from typing import Iterable


def mono_lines_to_html(lines: Iterable[str]) -> str:
    escaped_lines = [line.replace(" ", "&nbsp;") for line in lines]
    body = "<br>\n".join(escaped_lines)
    return f"<div align=\"center\">\n<samp>\n{body}\n</samp>\n</div>"
