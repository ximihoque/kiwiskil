import tempfile
from pathlib import Path

from indexer.config import Config
from indexer.manifest import Manifest, FileEntry
from indexer.verify import VerifyReport
from indexer.repair import RepairPlan, plan, execute


def _empty_manifest():
    return Manifest(last_indexed_commit="abc", indexed_at="now", files={})


def test_clean_report_produces_empty_plan():
    with tempfile.TemporaryDirectory() as d:
        p = plan(VerifyReport(), Path(d), Config(), _empty_manifest(), skip_deep=False)
        assert p.files_to_reindex == []
        assert p.orphan_pages_to_delete == []
        assert p.dangling_entries_to_prune == []
        assert p.fix_claude_md is False
        assert p.fix_gitignore is False
        assert p.fix_hook is False


def test_stale_and_untracked_files_go_to_reindex():
    report = VerifyReport(stale_files=["a.py"], untracked_files=["b.py"])
    with tempfile.TemporaryDirectory() as d:
        p = plan(report, Path(d), Config(), _empty_manifest(), skip_deep=False)
        assert sorted(p.files_to_reindex) == ["a.py", "b.py"]


def test_missing_wiki_page_pulls_files_from_manifest():
    report = VerifyReport(missing_wiki_pages=["wiki/foo.md"])
    manifest = Manifest(
        last_indexed_commit="abc",
        indexed_at="now",
        files={
            "a.py": FileEntry(hash="x", wiki_page="wiki/foo.md", component_ids=[]),
            "b.py": FileEntry(hash="x", wiki_page="wiki/foo.md", component_ids=[]),
            "c.py": FileEntry(hash="x", wiki_page="wiki/other.md", component_ids=[]),
        },
    )
    with tempfile.TemporaryDirectory() as d:
        p = plan(report, Path(d), Config(), manifest, skip_deep=False)
        assert sorted(p.files_to_reindex) == ["a.py", "b.py"]


def test_pages_missing_deep_included_when_deep_active():
    report = VerifyReport(pages_missing_deep=["wiki/foo.md"])
    manifest = Manifest(
        last_indexed_commit="abc",
        indexed_at="now",
        files={"a.py": FileEntry(hash="x", wiki_page="wiki/foo.md", component_ids=[])},
    )
    with tempfile.TemporaryDirectory() as d:
        p = plan(report, Path(d), Config(), manifest, skip_deep=False)
        assert p.files_to_reindex == ["a.py"]


def test_pages_missing_deep_excluded_when_skip_deep():
    report = VerifyReport(pages_missing_deep=["wiki/foo.md"])
    manifest = Manifest(
        last_indexed_commit="abc",
        indexed_at="now",
        files={"a.py": FileEntry(hash="x", wiki_page="wiki/foo.md", component_ids=[])},
    )
    with tempfile.TemporaryDirectory() as d:
        p = plan(report, Path(d), Config(), manifest, skip_deep=True)
        assert p.files_to_reindex == []


def test_cleanup_ops_carried_through():
    report = VerifyReport(
        orphan_wiki_pages=["wiki/old.md"],
        dangling_manifest_entries=["gone.py"],
        claude_md_snippet_missing=True,
        agents_md_snippet_missing=True,
        gitignore_entry_missing=True,
        hook_drift=True,
    )
    with tempfile.TemporaryDirectory() as d:
        p = plan(report, Path(d), Config(), _empty_manifest(), skip_deep=False)
        assert p.orphan_pages_to_delete == ["wiki/old.md"]
        assert p.dangling_entries_to_prune == ["gone.py"]
        assert p.fix_claude_md is True
        assert p.fix_agents_md is True
        assert p.fix_gitignore is True
        assert p.fix_hook is True


def test_execute_restores_agents_md(tmp_path):
    from indexer.repair import execute
    report = VerifyReport(agents_md_snippet_missing=True)
    p = plan(report, tmp_path, Config(), _empty_manifest(), skip_deep=False)
    assert p.fix_agents_md is True
    execute(p, tmp_path, Config(), _empty_manifest(), skip_deep=False)
    agents = tmp_path / "AGENTS.md"
    assert agents.exists()
    assert "Codebase Navigation" in agents.read_text()


def test_execute_deletes_orphan_pages_and_prunes_manifest():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        wiki = root / "wiki"
        wiki.mkdir()
        (wiki / "orphan.md").write_text("# o")
        (wiki / "keep.md").write_text("# k")
        manifest = Manifest(
            last_indexed_commit="abc",
            indexed_at="now",
            files={
                "keep.py": FileEntry(hash="x", wiki_page="wiki/keep.md", component_ids=[]),
                "gone.py": FileEntry(hash="x", wiki_page="wiki/keep.md", component_ids=[]),
            },
        )
        p = RepairPlan(
            orphan_pages_to_delete=["wiki/orphan.md"],
            dangling_entries_to_prune=["gone.py"],
        )
        execute(p, root, Config(), manifest, skip_deep=True)
        assert not (wiki / "orphan.md").exists()
        assert (wiki / "keep.md").exists()
        assert "gone.py" not in manifest.files
        assert "keep.py" in manifest.files


def test_execute_runs_reindex_for_files(monkeypatch):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        manifest = Manifest(last_indexed_commit="abc", indexed_at="now", files={})
        p = RepairPlan(files_to_reindex=["a.py"], rebuild_index_and_skill=True)

        called = {}

        def fake_index_files(r, cfg, candidates, skip_deep):
            called["candidates"] = candidates
            return ({}, {}, [], {}, {}, [])

        def fake_finalise(*args, **kwargs):
            called["finalised"] = True

        monkeypatch.setattr("indexer.repair._index_files", fake_index_files)
        monkeypatch.setattr("indexer.repair._finalise_index_and_skill", fake_finalise)

        execute(p, root, Config(), manifest, skip_deep=True)
        assert called["candidates"] == ["a.py"]
        # all_nodes empty -> finalise skipped (mirrors run() behaviour)
        assert "finalised" not in called
