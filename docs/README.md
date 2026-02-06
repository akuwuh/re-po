# 📚 Documentation Index

All re-po documentation lives in this folder. The current architecture is fully
modular: shared utilities live under `repo/core/`, while each card exists inside
`repo/features/<name>/`.

## 📂 Directory Map

```
docs/
├── README.md                     ← You are here
├── ARCHITECTURE.md               ← Project structure & flow
├── CONTRIBUTING_FEATURES.md      ← How to implement new cards
├── features/
│   ├── languages.md              ← Languages feature guide
│   └── bio.md                    ← Bio feature guide
├── IMPLEMENTATION_SUMMARY.md     ← Historical notes
├── GITIGNORE_SETUP.md            ← Git ignore documentation
└── VECTORIZING_GUIDE.md          ← SVG/vector tips (legacy)
```

## 🚀 Start Here

1. **Architecture:** [`ARCHITECTURE.md`](ARCHITECTURE.md) – high-level layout
   and how the GitHub Action dispatches features.
2. **Feature contributions:** [`CONTRIBUTING_FEATURES.md`](CONTRIBUTING_FEATURES.md)
   – required steps for adding new cards (no duplication, minimal surface area).
3. **Feature catalog:** [`features/languages.md`](features/languages.md) and
   [`features/bio.md`](features/bio.md) – inputs, outputs, and workflow samples
   for currently supported cards.

Legacy docs from the previous `re_po/lang_stats` package are preserved under
`docs/IMPLEMENTATION_SUMMARY.md`, `docs/VECTORIZING_GUIDE.md`, etc. They are
useful for historical context but no longer describe the active architecture.

## 🧭 Guidelines

- **No overlapping responsibilities.** Shared helpers belong in `repo/core/`.
- **Minimal implementations.** Only build what the feature requires; keep PRs
  scoped to the smallest change that satisfies the plan.
- **Documentation parity.** Every feature addition must include a page in
  `docs/features/` plus any contributor/architecture updates it touches.

