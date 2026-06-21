"""Tests for multi-language tree-sitter extraction (Go, Java, Ruby, Rust).

Each newly-supported language gets a small fixture and assertions on the
extracted ASTNodes (ids, types, line ranges). These mirror the style of
tests/test_ast_parser.py. A grammar package that is not installed should
degrade gracefully (return []), so language-specific tests skip themselves
when the grammar is unavailable rather than failing the suite.
"""
import pytest
from pathlib import Path
from indexer.ast_parser import parse_file

FIX = Path(__file__).parent / "fixtures"
REPO_ROOT = FIX  # use the fixtures dir as the repo root so rel paths are stable


def _grammar_available(module_name: str) -> bool:
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def _by_id(nodes):
    return {n.id: n for n in nodes}


# ──────────────────────────────────────────────────────────────────────────
# Go
# ──────────────────────────────────────────────────────────────────────────
GO_FIXTURE = FIX / "sample_go/server.go"
go_required = pytest.mark.skipif(
    not _grammar_available("tree_sitter_go"),
    reason="tree-sitter-go not installed",
)


@go_required
def test_go_yields_nonzero_symbols():
    """Regression for the bug: .go files used to extract ZERO symbols."""
    nodes = parse_file(GO_FIXTURE, repo_root=REPO_ROOT)
    assert len(nodes) > 0


@go_required
def test_go_function():
    nodes = _by_id(parse_file(GO_FIXTURE, repo_root=REPO_ROOT))
    n = nodes["sample_go/server.go::Greet"]
    assert n.type == "function"
    assert n.line_start == 9
    assert n.line_end == 12


@go_required
def test_go_struct_is_class():
    nodes = _by_id(parse_file(GO_FIXTURE, repo_root=REPO_ROOT))
    n = nodes["sample_go/server.go::Server"]
    assert n.type == "class"


@go_required
def test_go_method():
    nodes = _by_id(parse_file(GO_FIXTURE, repo_root=REPO_ROOT))
    # Go methods have a receiver, not a containing-class body. We extract them
    # as top-level functions keyed by their own name.
    assert "sample_go/server.go::Start" in nodes
    assert nodes["sample_go/server.go::Start"].type in ("function", "method")


@go_required
def test_go_docstring():
    nodes = _by_id(parse_file(GO_FIXTURE, repo_root=REPO_ROOT))
    n = nodes["sample_go/server.go::Greet"]
    assert n.docstring is not None
    assert "greeting" in n.docstring


@go_required
def test_go_calls():
    nodes = _by_id(parse_file(GO_FIXTURE, repo_root=REPO_ROOT))
    start = nodes["sample_go/server.go::Start"]
    assert "Greet" in start.calls


@go_required
def test_go_imports():
    nodes = _by_id(parse_file(GO_FIXTURE, repo_root=REPO_ROOT))
    n = nodes["sample_go/server.go::Greet"]
    assert len(n.imports) > 0


# ──────────────────────────────────────────────────────────────────────────
# Java
# ──────────────────────────────────────────────────────────────────────────
JAVA_FIXTURE = FIX / "sample_java/Widget.java"
java_required = pytest.mark.skipif(
    not _grammar_available("tree_sitter_java"),
    reason="tree-sitter-java not installed",
)


@java_required
def test_java_yields_nonzero_symbols():
    nodes = parse_file(JAVA_FIXTURE, repo_root=REPO_ROOT)
    assert len(nodes) > 0


@java_required
def test_java_class():
    nodes = _by_id(parse_file(JAVA_FIXTURE, repo_root=REPO_ROOT))
    n = nodes["sample_java/Widget.java::Widget"]
    assert n.type == "class"
    assert n.line_start == 7


@java_required
def test_java_method():
    nodes = _by_id(parse_file(JAVA_FIXTURE, repo_root=REPO_ROOT))
    n = nodes["sample_java/Widget.java::Widget.bump"]
    assert n.type == "method"
    assert n.line_start == 11


@java_required
def test_java_static_method():
    nodes = _by_id(parse_file(JAVA_FIXTURE, repo_root=REPO_ROOT))
    assert "sample_java/Widget.java::Widget.helper" in nodes


@java_required
def test_java_docstring():
    nodes = _by_id(parse_file(JAVA_FIXTURE, repo_root=REPO_ROOT))
    n = nodes["sample_java/Widget.java::Widget.bump"]
    assert n.docstring is not None
    assert "Increments" in n.docstring


@java_required
def test_java_calls():
    nodes = _by_id(parse_file(JAVA_FIXTURE, repo_root=REPO_ROOT))
    n = nodes["sample_java/Widget.java::Widget.bump"]
    assert "helper" in n.calls


@java_required
def test_java_imports():
    nodes = _by_id(parse_file(JAVA_FIXTURE, repo_root=REPO_ROOT))
    n = nodes["sample_java/Widget.java::Widget"]
    assert len(n.imports) > 0


# ──────────────────────────────────────────────────────────────────────────
# Ruby
# ──────────────────────────────────────────────────────────────────────────
RUBY_FIXTURE = FIX / "sample_ruby/widget.rb"
ruby_required = pytest.mark.skipif(
    not _grammar_available("tree_sitter_ruby"),
    reason="tree-sitter-ruby not installed",
)


@ruby_required
def test_ruby_yields_nonzero_symbols():
    nodes = parse_file(RUBY_FIXTURE, repo_root=REPO_ROOT)
    assert len(nodes) > 0


@ruby_required
def test_ruby_class_and_module():
    nodes = _by_id(parse_file(RUBY_FIXTURE, repo_root=REPO_ROOT))
    assert nodes["sample_ruby/widget.rb::Widget"].type == "class"
    assert nodes["sample_ruby/widget.rb::Greeter"].type == "class"


@ruby_required
def test_ruby_method():
    nodes = _by_id(parse_file(RUBY_FIXTURE, repo_root=REPO_ROOT))
    n = nodes["sample_ruby/widget.rb::Widget.bump"]
    assert n.type == "method"


@ruby_required
def test_ruby_top_level_function():
    nodes = _by_id(parse_file(RUBY_FIXTURE, repo_root=REPO_ROOT))
    n = nodes["sample_ruby/widget.rb::top_level"]
    assert n.type == "function"


@ruby_required
def test_ruby_docstring():
    nodes = _by_id(parse_file(RUBY_FIXTURE, repo_root=REPO_ROOT))
    n = nodes["sample_ruby/widget.rb::Widget.bump"]
    assert n.docstring is not None
    assert "Increments" in n.docstring


@ruby_required
def test_ruby_calls():
    nodes = _by_id(parse_file(RUBY_FIXTURE, repo_root=REPO_ROOT))
    n = nodes["sample_ruby/widget.rb::Widget.bump"]
    assert "helper" in n.calls


# ──────────────────────────────────────────────────────────────────────────
# Rust
# ──────────────────────────────────────────────────────────────────────────
RUST_FIXTURE = FIX / "sample_rust/widget.rs"
rust_required = pytest.mark.skipif(
    not _grammar_available("tree_sitter_rust"),
    reason="tree-sitter-rust not installed",
)


@rust_required
def test_rust_yields_nonzero_symbols():
    nodes = parse_file(RUST_FIXTURE, repo_root=REPO_ROOT)
    assert len(nodes) > 0


@rust_required
def test_rust_struct_and_trait_are_classes():
    nodes = _by_id(parse_file(RUST_FIXTURE, repo_root=REPO_ROOT))
    assert nodes["sample_rust/widget.rs::Widget"].type == "class"
    assert nodes["sample_rust/widget.rs::Speak"].type == "class"


@rust_required
def test_rust_free_function():
    nodes = _by_id(parse_file(RUST_FIXTURE, repo_root=REPO_ROOT))
    n = nodes["sample_rust/widget.rs::greet"]
    assert n.type == "function"


@rust_required
def test_rust_impl_method():
    nodes = _by_id(parse_file(RUST_FIXTURE, repo_root=REPO_ROOT))
    # method inside `impl Widget` is attributed to Widget
    n = nodes["sample_rust/widget.rs::Widget.bump"]
    assert n.type == "method"


@rust_required
def test_rust_docstring():
    nodes = _by_id(parse_file(RUST_FIXTURE, repo_root=REPO_ROOT))
    n = nodes["sample_rust/widget.rs::greet"]
    assert n.docstring is not None
    assert "Greets" in n.docstring


@rust_required
def test_rust_calls():
    nodes = _by_id(parse_file(RUST_FIXTURE, repo_root=REPO_ROOT))
    n = nodes["sample_rust/widget.rs::Widget.bump"]
    assert "helper" in n.calls


# ──────────────────────────────────────────────────────────────────────────
# Graceful degradation: an unsupported suffix returns []
# ──────────────────────────────────────────────────────────────────────────
def test_unsupported_suffix_returns_empty(tmp_path):
    f = tmp_path / "data.txt"
    f.write_text("not code")
    assert parse_file(f, repo_root=tmp_path) == []
