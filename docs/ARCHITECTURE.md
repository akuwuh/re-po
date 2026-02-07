# Architecture Overview

```
re-po/
├── action.yml                 # GitHub Action entrypoint
├── repo/                      # Python package
│   ├── core/
│   │   ├── feature_registry.py
│   │   ├── runner.py
│   │   ├── readme_updater.py
│   │   └── file_utils.py
│   │   └── shared/
│   │       ├── markup.py
│   │       ├── snippets.py
│   │       ├── svg.py
│   │       └── extrusion/
│   └── features/
│       ├── languages/
│       │   ├── domain/
│       │   ├── infrastructure/
│       │   ├── rendering/
│       │   └── generate_languages.py
│       └── bio/
│           ├── core/
│           ├── rendering/
│           └── generate_bio.py
├── docs/
└── tests/
```

## Execution Flow

1. **GitHub Action** – `action.yml` installs the package (`pip install .`) and
   runs `python -m repo.core.runner ...`.
2. **Runner** – `repo/core/runner.py` looks up the configured feature via the
   registry and builds a `FeatureConfig`.
3. **Feature handler** – e.g., `repo/features/languages/generate_languages.py`
   fetches data, writes SVGs or updates the README, and returns a `FeatureResult`
   used only for logging/diagnostics.
4. **Shared kernel utilities** – `repo/core/shared` contains reusable helpers
   used by multiple features (HTML wrappers, picture snippets, XML escaping,
   and extrusion strategies).
5. **Feature bounded contexts** – each feature keeps its own `domain/` and
   `infrastructure/` modules for card-specific business logic and external IO.

## Adding Features

- Drop the new feature under `repo/features/<name>/`.
- Register it with `@register_feature("<name>")`.
- Document it in `docs/features/<name>.md`.
- Keep the implementation minimal; reusable helpers belong in `repo/core/shared/`.
- Do not import one feature package from another feature package directly.

This layout allows us to ship one Python distribution (`pip install
"git+https://github.com/akuwuh/re-po.git"`) while keeping the Action entrypoint
lean and reusable (`uses: akuwuh/re-po@v1` with `card=<name>`).
