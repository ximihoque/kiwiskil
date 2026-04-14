# Contributing to kiwiskil

Thanks for your interest in contributing. This document covers how to set up a dev environment, submit changes, and what we look for in PRs.

---

## Dev setup

```bash
git clone https://github.com/ximihoque/kiwiskil.git
cd kiwiskil
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

No test runner is configured yet — if you're adding a feature, a quick manual smoke test with `kiwiskil run` on a real repo is the baseline.

---

## How to contribute

1. **Open an issue first** for anything beyond a small bug fix — alignment before code saves everyone time
2. Fork the repo and create a branch: `git checkout -b feat/your-feature`
3. Make your changes
4. Run a manual smoke test: `cd /some/repo && kiwiskil run --force`
5. Open a PR against `main` with a clear description of what and why

---

## What we welcome

- Bug fixes
- New language support via tree-sitter
- LLM provider improvements
- Wiki and skill template improvements
- CLI UX improvements

## What to avoid

- Adding cloud dependencies or network calls outside of LLM providers
- Breaking the "wiki is plain markdown" contract
- Adding prose or opinion to the structural wiki output — facts only

---

## Code style

- Python 3.11+, standard library where possible
- `from __future__ import annotations` at the top of every module
- No `type: ignore` comments — fix the types
- Keep modules focused — one responsibility per file

---

## Adding a new language

Language parsers live alongside `indexer/ast_parser.py` (Python) and `indexer/js_parser.py` (JavaScript/TypeScript). To add a new language:

1. **Add the file extensions** to `_is_indexable` in `indexer/cli.py`
2. **Create a parser module** `indexer/<lang>_parser.py` that exports a `parse_file(path, repo_root) -> list[ASTNode]` function
3. **Dispatch from `ast_parser.py`** — call your parser from `parse_file` based on `path.suffix`

The `ASTNode` schema is language-agnostic — map your language's constructs to `type: "class" | "function" | "method"`. Look at `indexer/js_parser.py` as the reference implementation: it uses tree-sitter, extracts JSDoc comments, handles imports, and resolves `var f = function()` assignments.

**tree-sitter packages** follow the pattern `tree-sitter-<lang>` on PyPI. Add the dependency to `pyproject.toml` and import it lazily inside `_get_language()` (see `js_parser.py` for the pattern).

### Currently supported

| Language | Extensions | Parser |
|----------|-----------|--------|
| Python | `.py` | `ast_parser.py` — stdlib `ast` |
| JavaScript | `.js`, `.jsx`, `.mjs`, `.cjs` | `js_parser.py` — tree-sitter |
| TypeScript | `.ts`, `.tsx` | `js_parser.py` — tree-sitter |

### Planned

Go, Rust, Java, Ruby — contributions welcome.

---

## Releasing (maintainers)

```bash
# Bump version in pyproject.toml
git commit -m "chore: bump version to X.Y.Z"
git push origin main

# Build and upload
rm -rf dist/
python -m build
twine upload dist/* -u __token__ -p pypi-<token>
```

> Note: PyPI does not allow re-uploading a file with the same version. Always bump the version before building.
