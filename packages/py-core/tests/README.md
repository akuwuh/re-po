# Tests

This directory contains test scripts for the language statistics generator.

## Test Files

### `test_output_modes.py`
Renders the sample dataset using the new DDD pipeline:
- Text renderer preview (saved to `tests/test_output/sample_text.html`)
- SVG renderer preview (light + dark) saved to `tests/test_output/`

**Run it**
```
cd packages/py-core
python tests/test_output_modes.py
```

### `test_vector_file_generation.py`
Recreates the GitHub Actions step locally:
- Generates the final `langs-mono-light.svg` and `langs-mono-dark.svg`
- Writes them to the repository root for quick iteration

**Run it**
```
cd packages/py-core
python tests/test_vector_file_generation.py
```

## Output

Test outputs are saved to:
- `packages/py-core/tests/test_output/` - Sample outputs from `test_output_modes.py`
- Workspace root - SVG files from `test_vector_file_generation.py`

