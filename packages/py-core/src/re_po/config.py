"""Configuration helpers."""

from __future__ import annotations

from functools import lru_cache
from importlib import resources
from pathlib import Path
from typing import Dict, Optional

import yaml
from pydantic import BaseModel

from .model import Theme

CONFIG_FILENAME = "re-po.config.yml"


class RepoConfig(BaseModel):
    default_theme: str
    themes: Dict[str, Theme]
    max_languages: int = 10

    def get_theme(self, theme_id: Optional[str]) -> Theme:
        key = theme_id or self.default_theme
        if key not in self.themes:
            raise KeyError(f"Theme '{key}' not defined in configuration")
        theme = self.themes[key]
        if theme.id != key:
            theme = theme.copy(update={"id": key})
        return theme


def _find_config_path(explicit_path: Optional[str] = None) -> Path:
    if explicit_path:
        path = Path(explicit_path)
        if not path.exists():
            raise FileNotFoundError(explicit_path)
        return path

    cwd = Path.cwd()
    for candidate in [cwd, *cwd.parents]:
        config_path = candidate / CONFIG_FILENAME
        if config_path.exists():
            return config_path
    raise FileNotFoundError(f"Could not locate {CONFIG_FILENAME}")


@lru_cache(maxsize=1)
def load_config(path: Optional[str] = None) -> RepoConfig:
    if path:
        config_path = _find_config_path(path)
        data = yaml.safe_load(config_path.read_text())
    else:
        try:
            config_path = _find_config_path(None)
            data = yaml.safe_load(config_path.read_text())
        except FileNotFoundError:
            with resources.files("re_po").joinpath("default_config.yml").open("r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh.read())

    themes = {key: Theme(id=key, **value) for key, value in data.get("themes", {}).items()}

    return RepoConfig(
        default_theme=data.get("default_theme", next(iter(themes)) if themes else "terminal"),
        themes=themes,
        max_languages=data.get("max_languages", 10),
    )


def get_theme(theme_id: Optional[str]) -> Theme:
    config = load_config()
    return config.get_theme(theme_id)
