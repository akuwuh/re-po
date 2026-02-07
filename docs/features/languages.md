# Languages Card

The **languages** feature fetches the target user's public repositories, applies
basic filtering (exclusions, minimum percentage, max language count), and either
updates a README snippet (text mode) or renders two SVG assets
(`langs-mono-light.svg`, `langs-mono-dark.svg`).

## Inputs

| Input | Description | Default |
| --- | --- | --- |
| `card` | Must be `languages` | – |
| `token` | GitHub token with `repo` scope | – |
| `actor` | Repository owner / fallback username | empty |
| `username` | Override for the analyzed account | `actor` |
| `readme_path` | README to update when in text mode | `README.md` |
| `languages_output_mode` | `vector` or `text` | `vector` |
| `languages_max_languages` | Limit of languages displayed (number or quoted string) | unset |
| `languages_excluded_languages` | Comma-separated values | `JavaScript,HTML,CSS,SCSS` |
| `languages_extra_excluded_languages` | Additional exclusions | unset |
| `languages_min_percentage` | Drop languages below this percentage | unset |
| `languages_start_marker` | README start marker | `<!--START_SECTION:languages-->` |
| `languages_end_marker` | README end marker | `<!--END_SECTION:languages-->` |
| `languages_username` | Override the analyzed username | inherits `username` input |

## Outputs

- `langs-mono-light.svg` and `langs-mono-dark.svg` (vector mode).
- README section replaced between the configured markers (text mode).
- Console log summarising the files that changed.

## Internal Architecture Notes

- `domain/` and `infrastructure/` remain languages-specific bounded contexts.
- Shared rendering primitives (extrusion styles, XML escaping, snippet helpers)
  are consumed from `repo/core/shared/`.
- The feature runner path is `repo/features/languages/generate_languages.py`,
  which maps inputs into `LanguagesRequest` and executes the use case.

## Workflow Examples

### Using the GitHub Action (recommended)

```yaml
- name: Languages card
  uses: akuwuh/re-po@v1
  with:
    card: languages
    token: ${{ secrets.GITHUB_TOKEN }}
    actor: ${{ github.repository_owner }}
    languages_output_mode: vector
    languages_max_languages: 6
    languages_excluded_languages: "HTML,CSS"
```

### Using the CLI directly

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.x'

- name: Install re-po
  run: |
    python -m pip install --upgrade pip
    pip install "git+https://github.com/akuwuh/re-po.git"

- name: Generate languages card
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    GITHUB_ACTOR: ${{ github.repository_owner }}
  run: |
    generate-languages \
      --option output_mode=vector \
      --option max_languages=6 \
      --option excluded_languages=HTML,CSS
```

Add the following snippet to your README when using vector mode:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="langs-mono-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="langs-mono-light.svg">
  <img alt="Language Statistics" src="langs-mono-light.svg">
</picture>
```

