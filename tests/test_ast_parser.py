import tempfile, json
from pathlib import Path
from indexer.ast_parser import parse_file, ASTNode, compute_hash_short, load_cached_nodes, save_cached_nodes

FIXTURE = Path(__file__).parent / "fixtures/sample_py/auth.py"

def test_parse_returns_nodes():
    nodes = parse_file(FIXTURE, repo_root=FIXTURE.parent.parent.parent)
    assert len(nodes) > 0

def test_function_node():
    nodes = parse_file(FIXTURE, repo_root=FIXTURE.parent.parent.parent)
    ids = [n.id for n in nodes]
    assert any("require_auth" in i for i in ids)

def test_method_node():
    nodes = parse_file(FIXTURE, repo_root=FIXTURE.parent.parent.parent)
    ids = [n.id for n in nodes]
    assert any("TokenValidator.refresh" in i for i in ids)

def test_class_node():
    nodes = parse_file(FIXTURE, repo_root=FIXTURE.parent.parent.parent)
    ids = [n.id for n in nodes]
    assert any(i.endswith("::TokenValidator") for i in ids)

def test_docstring_extracted():
    nodes = parse_file(FIXTURE, repo_root=FIXTURE.parent.parent.parent)
    method = next(n for n in nodes if "TokenValidator.refresh" in n.id)
    assert method.docstring is not None
    assert "OAuth2" in method.docstring

def test_imports_extracted():
    nodes = parse_file(FIXTURE, repo_root=FIXTURE.parent.parent.parent)
    # imports are file-level; all nodes from this file should carry them
    method = next(n for n in nodes if "TokenValidator.refresh" in n.id)
    assert isinstance(method.imports, list)
    assert len(method.imports) > 0

def test_calls_extracted():
    nodes = parse_file(FIXTURE, repo_root=FIXTURE.parent.parent.parent)
    method = next(n for n in nodes if "TokenValidator.refresh" in n.id)
    assert "sign_payload" in method.calls

def test_cache_roundtrip():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        nodes = parse_file(FIXTURE, repo_root=FIXTURE.parent.parent.parent)
        file_hash = "abc123"
        save_cached_nodes(root, file_hash, nodes)
        loaded = load_cached_nodes(root, file_hash)
        assert loaded is not None
        assert len(loaded) == len(nodes)
        assert loaded[0].id == nodes[0].id
