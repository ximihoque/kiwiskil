# tests/test_langs.py
"""The canonical INDEXABLE_SUFFIXES set must stay in sync with what the parsers
actually dispatch, and is_indexable must honour ignore globs."""
from indexer.langs import (
    INDEXABLE_SUFFIXES,
    PYTHON_SUFFIXES,
    JS_TS_SUFFIXES,
    OTHER_SUFFIXES,
    is_indexable,
)


def test_indexable_suffixes_is_union_of_parser_sets():
    assert INDEXABLE_SUFFIXES == PYTHON_SUFFIXES | JS_TS_SUFFIXES | OTHER_SUFFIXES


def test_other_suffixes_match_ts_extract_lang_configs():
    """Every non-JS/TS/Python suffix we claim to index must have a tree-sitter
    LANG_CONFIG, and vice versa — so a language added to one but not the other
    fails here instead of silently mis-indexing."""
    from indexer.ts_extract import LANG_CONFIGS
    assert set(LANG_CONFIGS.keys()) == OTHER_SUFFIXES


def test_js_ts_suffixes_match_dispatch():
    """JS_TS_SUFFIXES must match the set ast_parser routes to the JS parser."""
    import inspect
    from indexer import ast_parser
    src = inspect.getsource(ast_parser.parse_file)
    for suffix in JS_TS_SUFFIXES:
        assert repr(suffix) in src or suffix in src


def test_is_indexable_accepts_known_suffixes():
    for suffix in INDEXABLE_SUFFIXES:
        assert is_indexable(f"src/file{suffix}", ignore=[])


def test_is_indexable_rejects_unknown_suffix():
    assert not is_indexable("README.md", ignore=[])
    assert not is_indexable("data.json", ignore=[])


def test_is_indexable_honours_part_glob():
    assert not is_indexable("node_modules/pkg/index.js", ignore=["node_modules"])
    assert is_indexable("src/index.js", ignore=["node_modules"])


def test_is_indexable_honours_path_glob():
    assert not is_indexable("src/foo.test.py", ignore=["*.test.*"])
    assert is_indexable("src/foo.py", ignore=["*.test.*"])
