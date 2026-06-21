# indexer/langs.py
"""Single source of truth for which files kiwiskil indexes.

The indexable-suffix set was previously duplicated in cli.py and verify.py and
had to be kept in sync by hand with the parser dispatch in ast_parser.py /
js_parser.py / ts_extract.py. That drift risk is real now that languages are
added via per-grammar config. This module owns the canonical set and the
`is_indexable` predicate so there is exactly one place to update.

Keep INDEXABLE_SUFFIXES in sync with the parser dispatch:
  - Python: ".py"            (ast_parser, stdlib ast)
  - JS/TS:  JS_TS_SUFFIXES   (js_parser, tree-sitter)
  - others: ts_extract.LANG_CONFIGS keys (Go/Java/Ruby/Rust, tree-sitter)
tests/test_langs.py asserts this set equals the union the parsers actually
dispatch, so a new language that's added to a parser but not here (or vice
versa) fails the test rather than silently mis-indexing.
"""
from __future__ import annotations
from fnmatch import fnmatch
from pathlib import Path

PYTHON_SUFFIXES = {".py"}
JS_TS_SUFFIXES = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}
# Other languages are extracted via ts_extract.LANG_CONFIGS; list their suffixes
# here too (kept in sync by tests/test_langs.py).
OTHER_SUFFIXES = {".java", ".go", ".rb", ".rs"}

INDEXABLE_SUFFIXES = PYTHON_SUFFIXES | JS_TS_SUFFIXES | OTHER_SUFFIXES


def is_indexable(path: str, ignore: list[str]) -> bool:
    """True if `path` has an indexable suffix and matches no `ignore` glob.

    `ignore` patterns match either a full path glob or any individual path part
    (so "node_modules" excludes anything under a node_modules/ directory).
    """
    p = Path(path)
    if p.suffix not in INDEXABLE_SUFFIXES:
        return False
    for pattern in ignore:
        if any(fnmatch(part, pattern) for part in p.parts):
            return False
        if fnmatch(path, pattern):
            return False
    return True
