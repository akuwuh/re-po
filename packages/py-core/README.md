# re-po Python package

This package exposes the reusable logic that powers the re-po stats card. Install it locally or in GitHub Actions to fetch repository language statistics and render ASCII or SVG cards.

## Installation

```bash
pip install ./packages/py-core
```

## CLI usage

The Typer-based CLI ships with the package as the `re-po` command.

```bash
re-po render --user akuwuh --format txt --theme terminal
```

### Options

- `--user` – GitHub username to inspect.
- `--format` – `txt` or `svg`.
- `--theme` – Theme ID from `re-po.config.yml`.
- `--width` – Optional width override for SVG cards.
- `--out` – Optional output path (otherwise prints to stdout).

The command automatically reads the `GITHUB_TOKEN` environment variable when present to increase rate limits.

## Library usage

```python
from re_po.cli import render_card

result = render_card(user="akuwuh", format="svg")
print(result.content)
```

The same functions are shared with the API and GitHub Action wrappers, keeping behavior consistent across delivery channels.
