# Tests

This directory contains test scripts for the language statistics generator.

## Test Files

### `test_output_modes.py`
Comprehensive test script that tests all output modes:
- Text mode with box-drawing characters
- Vector mode with graphical bars (light and dark themes)
- Vector mode with text-based bars
- Simple border mode (no 3D)
- Saves sample outputs to `test_output/` directory

**Run it:**
```bash
cd packages/py-core
python tests/test_output_modes.py
```

### `test_vector_file_generation.py`
Tests the vector mode SVG file generation workflow:
- Generates both light and dark theme SVGs
- Saves them to the workspace root (simulating the GitHub Actions workflow)
- Useful for testing the actual file output

**Run it:**
```bash
cd packages/py-core
python tests/test_vector_file_generation.py
```

## Output

Test outputs are saved to:
- `packages/py-core/test_output/` - Sample outputs from `test_output_modes.py`
- Workspace root - SVG files from `test_vector_file_generation.py`

