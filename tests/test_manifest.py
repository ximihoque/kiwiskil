import tempfile, json
from pathlib import Path
from indexer.manifest import FileEntry, Manifest, load_manifest, save_manifest, compute_hash

def test_compute_hash_stable():
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write("def foo(): pass\n")
        path = Path(f.name)
    h1 = compute_hash(path)
    h2 = compute_hash(path)
    assert h1 == h2
    assert h1.startswith("sha256:")

def test_empty_manifest_on_missing():
    with tempfile.TemporaryDirectory() as d:
        m = load_manifest(Path(d))
        assert m.last_indexed_commit is None
        assert m.files == {}

def test_save_and_reload():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        m = Manifest(
            last_indexed_commit="abc123",
            indexed_at="2026-04-09T10:00:00Z",
            files={
                "auth/middleware.py": FileEntry(
                    hash="sha256:abc",
                    wiki_page="wiki/auth.md",
                    component_ids=["auth/middleware.py::require_auth"],
                )
            }
        )
        save_manifest(root, m)
        reloaded = load_manifest(root)
        assert reloaded.last_indexed_commit == "abc123"
        assert "auth/middleware.py" in reloaded.files
        assert reloaded.files["auth/middleware.py"].wiki_page == "wiki/auth.md"

def test_stale_files_detected():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        src = root / "foo.py"
        src.write_text("def foo(): pass\n")
        m = Manifest(
            last_indexed_commit="abc",
            indexed_at="2026-04-09T10:00:00Z",
            files={"foo.py": FileEntry(hash="sha256:stale", wiki_page="wiki/foo.md", component_ids=[])}
        )
        stale = m.stale_files(root, ["foo.py"])
        assert "foo.py" in stale

def test_fresh_file_not_stale():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        src = root / "bar.py"
        src.write_text("def bar(): pass\n")
        real_hash = compute_hash(src)
        m = Manifest(
            last_indexed_commit="abc",
            indexed_at="2026-04-09T10:00:00Z",
            files={"bar.py": FileEntry(hash=real_hash, wiki_page="wiki/bar.md", component_ids=[])}
        )
        stale = m.stale_files(root, ["bar.py"])
        assert "bar.py" not in stale
