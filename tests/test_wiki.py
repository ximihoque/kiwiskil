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


# ── Slice C: OKF frontmatter ──────────────────────────────────────────────────

def _parse_frontmatter(md: str) -> dict:
    """Extract and YAML-parse the leading --- frontmatter block. Asserts shape."""
    import yaml
    assert md.startswith("---\n"), "page must start with frontmatter delimiter"
    _, fm, _body = md.split("---\n", 2)
    return yaml.safe_load(fm)


def test_page_starts_with_frontmatter_delimiter():
    ctx = PageContext(group_label="auth", files=["auth/middleware.py"], nodes=[_make_node()], descriptions={})
    md = build_page(ctx)
    assert md.startswith("---\n")
    # closing delimiter present
    assert md.count("---\n") >= 2


def test_page_frontmatter_is_valid_yaml_with_required_type():
    ctx = PageContext(group_label="auth", files=["auth/middleware.py"], nodes=[_make_node()], descriptions={})
    fm = _parse_frontmatter(build_page(ctx))
    assert fm["type"] == "Code Group"


def test_page_frontmatter_title_and_resource():
    ctx = PageContext(group_label="auth", files=["auth/middleware.py"], nodes=[_make_node()], descriptions={})
    fm = _parse_frontmatter(build_page(ctx))
    assert fm["title"] == "auth"
    assert fm["resource"] == "auth"


def test_page_frontmatter_tags_from_path_segments():
    ctx = PageContext(group_label="api/auth", files=["api/auth/mw.py"], nodes=[_make_node()], descriptions={})
    fm = _parse_frontmatter(build_page(ctx))
    assert "api" in fm["tags"]
    assert "auth" in fm["tags"]
    assert isinstance(fm["tags"], list)


def test_page_frontmatter_timestamp_passed_in_not_computed():
    ctx = PageContext(
        group_label="auth", files=["auth/mw.py"], nodes=[_make_node()],
        descriptions={}, timestamp="2026-06-20T00:00:00+00:00",
    )
    fm = _parse_frontmatter(build_page(ctx))
    assert fm["timestamp"] == "2026-06-20T00:00:00+00:00"


def test_page_frontmatter_description_from_narrative_first_sentence():
    ctx = PageContext(
        group_label="auth", files=["auth/mw.py"], nodes=[_make_node()], descriptions={},
        narrative="Handles request authentication. It also rate-limits.",
    )
    fm = _parse_frontmatter(build_page(ctx))
    assert fm["description"] == "Handles request authentication."


def test_page_frontmatter_description_generic_when_no_narrative():
    ctx = PageContext(group_label="auth", files=["auth/mw.py"], nodes=[_make_node()], descriptions={})
    fm = _parse_frontmatter(build_page(ctx))
    assert fm["description"]  # non-empty generic fallback


def test_page_body_sections_preserved_below_frontmatter():
    # frontmatter is additive — body must still contain the old sections
    ctx = PageContext(group_label="auth", files=["auth/middleware.py"], nodes=[_make_node()], descriptions={})
    md = build_page(ctx)
    _, _fm, body = md.split("---\n", 2)
    assert "## Modules" in body
    assert "## Key Symbols" in body
    assert "require_auth" in body


def test_index_frontmatter_has_okf_version():
    import yaml
    entries = [IndexEntry(path="wiki/auth.md", covers="auth/mw.py", entry_points=["require_auth"])]
    md = build_index(entries, last_commit="abc123", indexed_date="2026-04-09")
    assert md.startswith("---\n")
    _, fm, _body = md.split("---\n", 2)
    data = yaml.safe_load(fm)
    assert data["okf_version"] == "0.1"


# ── Slice B: inline relationships / blast radius block ────────────────────────

def test_page_renders_relationships_block_per_symbol():
    callee = _make_node(
        id="auth/middleware.py::verify_token", calls=[], called_by=["auth/middleware.py::require_auth"],
    )
    caller = _make_node(
        id="auth/middleware.py::require_auth", calls=["verify_token"], called_by=[],
    )
    blast = {
        "auth/middleware.py::verify_token": {"auth/middleware.py::require_auth"},
        "auth/middleware.py::require_auth": set(),
    }
    ctx = PageContext(
        group_label="auth", files=["auth/middleware.py"],
        nodes=[caller, callee], descriptions={}, blast_radius_map=blast,
    )
    md = build_page(ctx)
    assert "Callers" in md
    assert "Calls:" in md
    assert "Editing this affects:" in md
    # verify_token is affected-by require_auth
    assert "require_auth" in md


def test_page_relationships_block_caps_long_lists():
    callers = [f"m.py::caller_{i}" for i in range(20)]
    node = _make_node(id="m.py::hot", calls=[], called_by=callers)
    blast = {"m.py::hot": set(callers)}
    ctx = PageContext(
        group_label="m", files=["m.py"], nodes=[node], descriptions={}, blast_radius_map=blast,
    )
    md = build_page(ctx)
    assert "more)" in md  # "… (+k more)" truncation marker


def test_index_renders_core_abstractions():
    entries = [IndexEntry(path="wiki/auth.md", covers="auth/mw.py", entry_points=["require_auth"])]
    god = [("auth/mw.py::require_auth", 7), ("auth/mw.py::verify_token", 3)]
    md = build_index(entries, last_commit="abc", indexed_date="2026-04-09", god_nodes=god)
    assert "Core abstractions" in md
    assert "require_auth" in md


# ── page path sanitization (manifest must match write_page) ───────────────────

def test_page_basename_root_group():
    from indexer.wiki import page_basename
    assert page_basename(".") == "root"


def test_page_basename_nested_group():
    from indexer.wiki import page_basename
    assert page_basename("a/b/c") == "a_b_c"


def test_page_relpath_matches_write_page(tmp_path):
    """The manifest's wiki_page (via page_relpath) must equal the file that
    write_page actually creates — for root and nested groups alike."""
    from indexer.wiki import page_relpath, write_page
    for group in [".", "a/b", "pkg"]:
        rel = page_relpath("wiki", group)
        written = write_page(tmp_path / "wiki", group, "# x")
        assert rel == f"wiki/{written.name}"


# ── orphan page deletion (shared by run + repair) ─────────────────────────────

def test_delete_orphan_pages_removes_unreferenced(tmp_path):
    from indexer.wiki import delete_orphan_pages
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    (wiki / "INDEX.md").write_text("# i")          # never an orphan
    (wiki / "kept.md").write_text("# kept")        # referenced
    (wiki / "gone.md").write_text("# gone")        # orphan
    referenced = {"wiki/kept.md"}
    deleted = delete_orphan_pages(tmp_path, "wiki", referenced)
    assert deleted == ["wiki/gone.md"]
    assert not (wiki / "gone.md").exists()
    assert (wiki / "kept.md").exists()
    assert (wiki / "INDEX.md").exists()


def test_delete_orphan_pages_noop_when_all_referenced(tmp_path):
    from indexer.wiki import delete_orphan_pages
    wiki = tmp_path / "wiki"
    wiki.mkdir()
    (wiki / "INDEX.md").write_text("# i")
    (wiki / "a.md").write_text("# a")
    deleted = delete_orphan_pages(tmp_path, "wiki", {"wiki/a.md"})
    assert deleted == []
    assert (wiki / "a.md").exists()


def test_delete_orphan_pages_missing_wiki_dir(tmp_path):
    from indexer.wiki import delete_orphan_pages
    # No wiki dir at all -> no error, nothing deleted.
    assert delete_orphan_pages(tmp_path, "wiki", set()) == []
