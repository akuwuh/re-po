from __future__ import annotations

import importlib
import warnings


def test_extrusion_shim_emits_deprecation_warning() -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", DeprecationWarning)
        module = importlib.import_module("repo.features.languages.extrusion_styles")
        importlib.reload(module)

    assert any("deprecated" in str(item.message).lower() for item in caught)
    assert hasattr(module, "ExtrusionStyleFactory")


def test_extrusion_shim_factory_is_functional() -> None:
    from repo.features.languages.extrusion_styles.factory import ExtrusionStyleFactory

    style = ExtrusionStyleFactory.create(1, stroke_width=2)
    assert style.__class__.__name__ == "BackBoxExtrusion"
