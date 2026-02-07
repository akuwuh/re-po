# Contributing New Features

This repository treats every card (languages, bio, ...) as an isolated
**feature** that plugs into the shared registry. To add a new one, follow the
checklist below—no duplicated helpers or overlapping responsibilities are
accepted, and implementations should remain as small as possible.

## 1. Directory Layout

```
repo/
  core/
    shared/
  features/
    <feature-name>/
      __init__.py
      domain/
      infrastructure/
      rendering/
      generate_<feature-name>.py
```

Only domain-specific logic lives here. Shared cross-feature helpers belong in
`repo/core/shared/`.

## 2. Register the Feature

Inside `generate_<feature>.py`:

1. Implement `run_feature(config: FeatureConfig) -> FeatureResult`.
2. Decorate it with `@register_feature("<feature-name>")`.
3. Keep a CLI entry point (`main()`) so users can still run the card directly.

Do **not** import other features when adding a new one.

## 3. Action Inputs

Update the root `action.yml`:

- Add optional inputs prefixed with `<feature>_`.
- Extend the shell command to append `--option key=value` arguments when the
  card matches. Keep the logic minimal.

## 4. Documentation

- Create `docs/features/<feature>.md` that explains purpose, inputs, outputs,
  README snippet, and shows both workflow patterns (GitHub Action + pip/CLI).
- Update `docs/README.md` to reference the new feature page if needed.

## 5. Tests / Examples

- Extend `tests/` or add a showcase script that exercises the new feature using
  the shared registry.

## 6. Project Standards

- Do not copy/paste helpers. Add reusable utilities to `repo/core/shared/`.
- Keep `domain/` and `infrastructure/` as feature-bounded contexts unless logic
  is truly generic across cards.
- Keep PRs focused on the smallest change that satisfies the requirements.
- Ensure docs and workflows stay in sync with the implementation.

