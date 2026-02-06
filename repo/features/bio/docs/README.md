# Bio Card Feature

`bio` is a pluggable card feature for `re-po` that renders an ordered bio card
from JSON rows.

## Feature ID

Use `card=bio` when invoking `run-card`.

## Rows Schema

Pass rows as a JSON array:

```json
[
  {"label": "age", "value": "22"},
  {"label": "location", "value": "toronto, ca", "align": "right", "pad": 2},
  {"label": "learning", "value": "infra", "prefix": "// "}
]
```

Row fields:
- `label` (required)
- `value` (required)
- `align` (`left` or `right`, default `left`)
- `pad` (0 to 8, default `1`)
- `prefix` (default `"// "`)

## GitHub Action Example

```yaml
- uses: your-org/re-po@main
  with:
    card: bio
    token: ${{ secrets.GITHUB_TOKEN }}
    username: yourusername
    bio_rows: >
      [{"label":"age","value":"22"},{"label":"location","value":"toronto, ca"}]
    bio_output_mode: vector
    bio_update_readme: true
```

## Output

- Vector mode: generates `bio-card-light.svg` and `bio-card-dark.svg`.
- Text mode: writes a monospace HTML snippet between markers.
