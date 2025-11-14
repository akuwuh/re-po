# 📚 Scripts Documentation

All documentation for `.github/scripts/` is organized here.

## 📂 Documentation Structure

```
docs/
├── README.md                      ← You are here
│
├── re_po/lang_stats/                    ← Lang Stats package docs
│   ├── DDD_RESPONSIBILITIES.md    → What each module does
│   ├── README_NEW_ARCHITECTURE.md → Quick start guide
│   ├── PROJECT_STRUCTURE.md       → Detailed structure
│   ├── ARCHITECTURE.md            → Architecture deep dive
│   ├── COMPLETE_REFACTORING.md    → Full refactoring details
│   └── REFACTORING_SUMMARY.md     → Summary
│
├── IMPLEMENTATION_SUMMARY.md      ← Implementation notes
├── GITIGNORE_SETUP.md             ← Git ignore documentation
├── VECTORIZING_GUIDE.md           ← SVG vectorization guide
└── REFACTORING_COMPLETE.txt       ← Refactoring summary
```

## 🚀 Quick Links

### For Lang Stats Usage
**Start here**: [`re_po/lang_stats/DDD_RESPONSIBILITIES.md`](re_po/lang_stats/DDD_RESPONSIBILITIES.md)
- Explains what each module does
- Single Responsibility Principle
- How to use the clean API

### For Project Setup
- **Git Setup**: [`GITIGNORE_SETUP.md`](GITIGNORE_SETUP.md)
- **Implementation Notes**: [`IMPLEMENTATION_SUMMARY.md`](IMPLEMENTATION_SUMMARY.md)

### For Development
- **Vectorization**: [`VECTORIZING_GUIDE.md`](VECTORIZING_GUIDE.md)
- **Architecture**: [`re_po/lang_stats/ARCHITECTURE.md`](re_po/lang_stats/ARCHITECTURE.md)

## 📦 Main Projects

### Lang Stats (`re_po/lang_stats/`)
Professional Python package for GitHub language statistics visualization.

**Entry Point**: `core/service.py`

```python
from re_po.lang_stats import LanguageStatsService, RenderConfig

service = LanguageStatsService(username="user")
svg = service.generate_svg()
```

**Documentation**: See `re_po/lang_stats/` subdirectory for complete docs.

## 🎯 Documentation Guidelines

### Adding New Documentation

1. **Package-specific docs** → Put in `docs/re_po/lang_stats/`
2. **Script-level docs** → Put in `docs/`
3. **Project-root docs** → Put in project root (README.md, LICENSE, etc.)

### Documentation Types

- **README.md** - Quick start and overview
- **ARCHITECTURE.md** - System design and patterns
- **GUIDE.md** - Step-by-step tutorials
- **REFERENCE.md** - API documentation
- **SUMMARY.md** - Brief overviews

## 🗂️ Where Things Go

| Type | Location | Example |
|------|----------|---------|
| Package API docs | `docs/re_po/lang_stats/` | How to use lang_stats |
| Implementation notes | `docs/` | IMPLEMENTATION_SUMMARY.md |
| Setup guides | `docs/` | GITIGNORE_SETUP.md |
| Project README | Project root | `../../../README.md` |
| Code comments | In code | Docstrings, inline comments |

## 📖 Reading Order

For new developers:

1. **Project README** (root) - What is this project?
2. **This file** - What docs exist?
3. **`re_po/lang_stats/DDD_RESPONSIBILITIES.md`** - How is code organized?
4. **`re_po/lang_stats/ARCHITECTURE.md`** - Why these design choices?
5. **Implementation/Guide docs** - Specific topics as needed

---

**All documentation consolidated in this directory!**  
**No more scattered docs.** ✅

