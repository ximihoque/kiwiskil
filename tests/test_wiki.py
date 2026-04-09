# tests/test_wiki.py
from pathlib import Path
from indexer.ast_parser import ASTNode
from indexer.wiki import build_page, build_index, PageContext, IndexEntry

def _make_node(**kwargs):
    defaults = dict(
        id="auth/middleware.py::require_auth",
        type="function",
        file="auth/middleware.py",
        line_start=1, line_end=5,
        docstring="Guards routes",
        imports=["utils.crypto"],
        calls=["verify_token"],
        called_by=["api/routes.py::login_handler"],
    )
    defaults.update(kwargs)
    return ASTNode(**defaults)

def test_build_page_contains_symbol():
    nodes = [_make_node()]
    descriptions = {"auth/middleware.py::require_auth": "Guards routes, validates bearer token"}
    ctx = PageContext(
        group_label="auth",
        files=["auth/middleware.py"],
        nodes=nodes,
        descriptions=descriptions,
    )
    md = build_page(ctx)
    assert "require_auth" in md
    assert "Guards routes, validates bearer token" in md

def test_build_page_contains_calls():
    nodes = [_make_node()]
    ctx = PageContext(group_label="auth", files=["auth/middleware.py"], nodes=nodes, descriptions={})
    md = build_page(ctx)
    assert "verify_token" in md

def test_build_page_contains_called_by():
    nodes = [_make_node()]
    ctx = PageContext(group_label="auth", files=["auth/middleware.py"], nodes=nodes, descriptions={})
    md = build_page(ctx)
    assert "login_handler" in md

def test_build_page_no_agent_hints():
    nodes = [_make_node()]
    ctx = PageContext(group_label="auth", files=["auth/middleware.py"], nodes=nodes, descriptions={})
    md = build_page(ctx)
    assert "start here" not in md.lower()
    assert "this is the" not in md.lower()

def test_build_index_contains_page():
    entries = [IndexEntry(path="wiki/auth.md", covers="auth/middleware.py", entry_points=["require_auth"])]
    md = build_index(entries, last_commit="abc123", indexed_date="2026-04-09")
    assert "wiki/auth.md" in md
    assert "abc123" in md
    assert "require_auth" in md

def test_write_page_creates_file():
    import tempfile
    from indexer.wiki import write_page
    with tempfile.TemporaryDirectory() as d:
        wiki_dir = Path(d) / "wiki"
        nodes = [_make_node()]
        ctx = PageContext(group_label="auth", files=["auth/middleware.py"], nodes=nodes, descriptions={})
        content = build_page(ctx)
        path = write_page(wiki_dir, "auth", content)
        assert path.exists()
        assert "require_auth" in path.read_text()
