"""
Command-line entry that dispatches to the requested feature.
"""

from __future__ import annotations

import argparse
import sys
from importlib import import_module
from typing import List

from .feature_registry import FeatureConfig, FeatureResult, get_feature


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a re-po feature.")
    parser.add_argument("--card", required=True, help="Feature identifier (e.g. languages)")
    parser.add_argument("--token", required=True, help="GitHub token")
    parser.add_argument("--actor", default="", help="Repository owner or actor")
    parser.add_argument("--username", default="", help="Target username for the card")
    parser.add_argument("--readme-path", default="README.md")
    parser.add_argument(
        "--option",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Optional feature-specific setting (repeatable)",
    )
    return parser


def _parse_options(option_args: List[str]) -> dict:
    options: dict = {}
    for raw in option_args:
        if "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        if value == "":
            continue
        options[key.replace("-", "_")] = value
    return options


def run(argv: List[str] | None = None) -> FeatureResult:
    parser = _build_parser()
    args = parser.parse_args(argv)

    # Lazy-load the requested feature so it can register itself.
    base_module = f"repo.features.{args.card}"
    import_module(base_module)
    try:
        import_module(f"{base_module}.generate_{args.card}")
    except ModuleNotFoundError:
        # Some features may register directly from __init__.py.
        pass

    handler = get_feature(args.card)
    config = FeatureConfig(
        token=args.token,
        actor=args.actor or None,
        username=args.username or None,
        readme_path=args.readme_path,
        options=_parse_options(args.option),
    )
    return handler(config)


def main() -> None:
    run(sys.argv[1:])


if __name__ == "__main__":
    main()


