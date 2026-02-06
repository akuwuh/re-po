from __future__ import annotations

import os
import sys

from repo.core.feature_registry import FeatureConfig, FeatureResult, register_feature


@register_feature("bio")
def run_feature(config: FeatureConfig) -> FeatureResult:
    _ = config
    raise NotImplementedError("Bio feature adapter is wired incrementally")


def main() -> None:
    if not os.environ.get("GITHUB_TOKEN"):
        print("Error: GITHUB_TOKEN not found")
        sys.exit(1)
    raise NotImplementedError("Bio feature adapter is wired incrementally")


if __name__ == "__main__":
    main()
