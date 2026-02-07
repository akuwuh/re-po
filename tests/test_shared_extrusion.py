from __future__ import annotations

from repo.core.shared.extrusion import ExtrusionStyleFactory


def test_extrusion_factory_returns_supported_styles() -> None:
    style1 = ExtrusionStyleFactory.create(1, stroke_width=2)
    style2 = ExtrusionStyleFactory.create(2, stroke_width=2)
    assert style1.__class__.__name__ == "BackBoxExtrusion"
    assert style2.__class__.__name__ == "ConnectedExtrusion"


def test_style1_render_emits_front_and_back_segments() -> None:
    style = ExtrusionStyleFactory.create(1, stroke_width=2)
    elements = style.render(20, 20, 100, 60, 15, 15, "#fff")
    assert any(element.startswith("<rect ") for element in elements)
    assert sum(1 for element in elements if element.startswith("<line ")) >= 4


def test_style2_render_emits_paths_and_connectors() -> None:
    style = ExtrusionStyleFactory.create(2, stroke_width=2)
    elements = style.render(20, 20, 100, 60, 15, 15, "#fff")
    assert sum(1 for element in elements if element.startswith("<path ")) >= 2
    assert sum(1 for element in elements if element.startswith("<line ")) >= 3
