# Bio Card

The **bio** feature renders a profile card from ordered JSON rows and can output
either:
- dual-theme SVG files (`bio-card-light.svg`, `bio-card-dark.svg`), or
- a text/HTML snippet inserted between README markers.

## Inputs

| Input | Description | Default |
| --- | --- | --- |
| `card` | Must be `bio` | – |
| `token` | GitHub token (global requirement) | – |
| `actor` | Repository owner / fallback username | empty |
| `username` | Override username/title fallback | `actor` |
| `readme_path` | README path for marker updates | `README.md` |
| `bio_output_mode` | `vector` or `text` | `vector` |
| `bio_rows` | JSON array of row objects | required for useful output |
| `bio_title` | Title at top of card | `username` |
| `bio_update_readme` | Patch README markers after render | `true` |
| `bio_start_marker` | Start marker for bio section | `<!--START_SECTION:bio-->` |
| `bio_end_marker` | End marker for bio section | `<!--END_SECTION:bio-->` |
| `bio_svg_light_file` | Light theme SVG output file | `bio-card-light.svg` |
| `bio_svg_dark_file` | Dark theme SVG output file | `bio-card-dark.svg` |

## `bio_rows` Schema

JSON array preserving order:

```json
[
  {"label":"age","value":"22"},
  {"label":"location","value":"toronto, ca","align":"right","pad":2},
  {"label":"learning","value":"infra", "prefix":"// "}
]
```

Row object fields:
- `label` (required string)
- `value` (required string)
- `align` (`left` or `right`, default `left`)
- `pad` (integer `0..8`, default `1`)
- `prefix` (string, default `"// "`)

## Workflow Example

```yaml
- name: Bio card
  uses: akuwuh/re-po@v1
  with:
    card: bio
    token: ${{ secrets.GITHUB_TOKEN }}
    actor: ${{ github.repository_owner }}
    bio_rows: >
      [{"label":"age","value":"22"},{"label":"location","value":"toronto, ca"}]
    bio_output_mode: vector
    bio_update_readme: true
```
