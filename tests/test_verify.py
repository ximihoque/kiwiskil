import tempfile
from pathlib import Path

from indexer.config import Config
from indexer.manifest import Manifest, FileEntry, compute_hash
from indexer.verify import VerifyReport, scan, print_report


def _make_repo_with_manifest(root: Path, files_on_disk: dict[str, str], manifest_files: dict[str, FileEntry]) -> Manifest:
    for rel, content in files_on_disk.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return Manifest(
        last_indexed_commit="abc123",
        indexed_at="2026-05-29T00:00:00Z",
        files=manifest_files,
    )


def test_empty_report_is_clean():
    r = VerifyReport()
    assert r.is_clean() is True
    assert r.total_issues() == 0


def test_report_with_stale_files_not_clean():
    r = VerifyReport(stale_files=["a.py"])
    assert r.is_clean() is False
    assert r.total_issues() == 1


def test_report_counts_all_drift_classes():
    r = VerifyReport(
        stale_files=["a.py"],
        untracked_files=["b.py"],
        dangling_manifest_entries=["c.py"],
        missing_wiki_pages=["wiki/x.md"],
        orphan_wiki_pages=["wiki/y.md"],
        pages_missing_deep=["wiki/z.md"],
        skill_missing=True,
        index_missing=True,
        manifest_missing=False,
        claude_md_snippet_missing=True,
        gitignore_entry_missing=True,
        hook_drift=True,
    )
    # 6 list entries + 5 booleans (manifest_missing is False)
    assert r.total_issues() == 11
    assert r.is_clean() is False


def test_scan_flags_missing_manifest():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        cfg = Config()
        manifest = Manifest(last_indexed_commit=None, indexed_at="", files={})
        report = scan(root, cfg, manifest)
        assert report.manifest_missing is True
        assert report.stale_files == []
        assert report.untracked_files == []


def test_scan_detects_stale_files(monkeypatch):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        manifest = _make_repo_with_manifest(
            root,
            files_on_disk={"foo.py": "def foo(): pass\n"},
            manifest_files={
                "foo.py": FileEntry(hash="sha256:stale", wiki_page="wiki/root.md", component_ids=[])
            },
        )
        monkeypatch.setattr("indexer.verify.all_tracked_files", lambda r: ["foo.py"])
        monkeypatch.setattr("indexer.verify.is_git_repo", lambda r: True)
        report = scan(root, Config(), manifest)
        assert "foo.py" in report.stale_files


def test_scan_detects_dangling_manifest_entries(monkeypatch):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        manifest = _make_repo_with_manifest(
            root,
            files_on_disk={},
            manifest_files={
                "gone.py": FileEntry(hash="sha256:x", wiki_page="wiki/root.md", component_ids=[])
            },
        )
        monkeypatch.setattr("indexer.verify.all_tracked_files", lambda r: [])
        monkeypatch.setattr("indexer.verify.is_git_repo", lambda r: True)
        report = scan(root, Config(), manifest)
        assert "gone.py" in report.dangling_manifest_entries


def test_scan_detects_untracked_source_files(monkeypatch):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        manifest = _make_repo_with_manifest(
            root,
            files_on_disk={"new.py": "def n(): pass\n", "other.py": "def o(): pass\n"},
            manifest_files={
                "other.py": FileEntry(hash="sha256:x", wiki_page="wiki/root.md", component_ids=[])
            },
        )
        monkeypatch.setattr("indexer.verify.all_tracked_files", lambda r: ["new.py", "other.py"])
        monkeypatch.setattr("indexer.verify.is_git_repo", lambda r: True)
        report = scan(root, Config(), manifest)
        assert "new.py" in report.untracked_files
        assert "other.py" not in report.untracked_files


def test_scan_detects_missing_wiki_page(monkeypatch):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "foo.py").write_text("def f(): pass\n")
        manifest = Manifest(
            last_indexed_commit="abc",
            indexed_at="now",
            files={
                "foo.py": FileEntry(
                    hash=compute_hash(root / "foo.py"),
                    wiki_page="wiki/missing.md",
                    component_ids=[],
                )
            },
        )
        monkeypatch.setattr("indexer.verify.all_tracked_files", lambda r: ["foo.py"])
        monkeypatch.setattr("indexer.verify.is_git_repo", lambda r: True)
        report = scan(root, Config(), manifest)
        assert "wiki/missing.md" in report.missing_wiki_pages


def test_scan_detects_orphan_wiki_page(monkeypatch):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        wiki = root / "wiki"
        wiki.mkdir()
        (wiki / "INDEX.md").write_text("# index")
        (wiki / "covered.md").write_text("# covered")
        (wiki / "orphan.md").write_text("# orphan")
        (root / "foo.py").write_text("def f(): pass\n")
        manifest = Manifest(
            last_indexed_commit="abc",
            indexed_at="now",
            files={
                "foo.py": FileEntry(
                    hash=compute_hash(root / "foo.py"),
                    wiki_page="wiki/covered.md",
                    component_ids=[],
                )
            },
        )
        monkeypatch.setattr("indexer.verify.all_tracked_files", lambda r: ["foo.py"])
        monkeypatch.setattr("indexer.verify.is_git_repo", lambda r: True)
        report = scan(root, Config(), manifest)
        assert "wiki/orphan.md" in report.orphan_wiki_pages
        assert "wiki/INDEX.md" not in report.orphan_wiki_pages


def test_scan_detects_missing_index_and_skill(monkeypatch):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        wiki = root / "wiki"
        wiki.mkdir()
        (wiki / "covered.md").write_text("# covered")
        (root / "foo.py").write_text("def f(): pass\n")
        manifest = Manifest(
            last_indexed_commit="abc",
            indexed_at="now",
            files={
                "foo.py": FileEntry(
                    hash=compute_hash(root / "foo.py"),
                    wiki_page="wiki/covered.md",
                    component_ids=[],
                )
            },
        )
        monkeypatch.setattr("indexer.verify.all_tracked_files", lambda r: ["foo.py"])
        monkeypatch.setattr("indexer.verify.is_git_repo", lambda r: True)
        report = scan(root, Config(), manifest)
        assert report.index_missing is True
        assert report.skill_missing is True


def _seed_valid_state(root: Path) -> Manifest:
    """Helper: create a fully-valid filesystem + manifest, ready for drift tests."""
    (root / "foo.py").write_text("def f(): pass\n")
    (root / "wiki").mkdir()
    (root / "wiki" / "INDEX.md").write_text("# i")
    (root / "wiki" / "covered.md").write_text("# c")
    (root / ".indexer" / "skills").mkdir(parents=True)
    (root / ".indexer" / "skills" / "codebase.md").write_text("skill")
    return Manifest(
        last_indexed_commit="abc",
        indexed_at="now",
        files={
            "foo.py": FileEntry(
                hash=compute_hash(root / "foo.py"),
                wiki_page="wiki/covered.md",
                component_ids=[],
            )
        },
    )


def test_scan_detects_missing_claude_md_snippet(monkeypatch):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        manifest = _seed_valid_state(root)
        (root / "CLAUDE.md").write_text("# Some other content\n")
        monkeypatch.setattr("indexer.verify.all_tracked_files", lambda r: ["foo.py"])
        monkeypatch.setattr("indexer.verify.is_git_repo", lambda r: True)
        report = scan(root, Config(), manifest)
        assert report.claude_md_snippet_missing is True


def test_scan_detects_missing_agents_md_snippet(monkeypatch):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        manifest = _seed_valid_state(root)
        # CLAUDE.md present & valid, but AGENTS.md missing -> AGENTS flagged.
        (root / "CLAUDE.md").write_text("# Codebase Navigation\n")
        monkeypatch.setattr("indexer.verify.all_tracked_files", lambda r: ["foo.py"])
        monkeypatch.setattr("indexer.verify.is_git_repo", lambda r: True)
        report = scan(root, Config(), manifest)
        assert report.agents_md_snippet_missing is True
        assert report.claude_md_snippet_missing is False


def test_scan_agents_md_present_and_valid_not_flagged(monkeypatch):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        manifest = _seed_valid_state(root)
        (root / "CLAUDE.md").write_text("# Codebase Navigation\n")
        (root / "AGENTS.md").write_text("# Codebase Navigation\n")
        monkeypatch.setattr("indexer.verify.all_tracked_files", lambda r: ["foo.py"])
        monkeypatch.setattr("indexer.verify.is_git_repo", lambda r: True)
        report = scan(root, Config(), manifest)
        assert report.agents_md_snippet_missing is False


def test_scan_detects_missing_gitignore_entry(monkeypatch):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        manifest = _seed_valid_state(root)
        (root / ".gitignore").write_text("*.pyc\n")
        monkeypatch.setattr("indexer.verify.all_tracked_files", lambda r: ["foo.py"])
        monkeypatch.setattr("indexer.verify.is_git_repo", lambda r: True)
        report = scan(root, Config(), manifest)
        assert report.gitignore_entry_missing is True


def test_scan_detects_hook_drift(monkeypatch):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        manifest = _seed_valid_state(root)
        (root / ".git" / "hooks").mkdir(parents=True)
        (root / ".git" / "hooks" / "pre-commit").write_text("#!/bin/sh\necho hi\n")
        monkeypatch.setattr("indexer.verify.all_tracked_files", lambda r: ["foo.py"])
        monkeypatch.setattr("indexer.verify.is_git_repo", lambda r: True)
        cfg = Config()
        cfg.pre_commit = True
        report = scan(root, cfg, manifest)
        assert report.hook_drift is True


def test_scan_detects_pages_missing_deep_sections(monkeypatch):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        wiki = root / "wiki"
        wiki.mkdir()
        (wiki / "INDEX.md").write_text("# i")
        (wiki / "shallow.md").write_text("# shallow/\n\n## Modules\n\n## Key Symbols\n")
        (wiki / "deep.md").write_text(
            "# deep/\n<!-- kiwiskil:deep -->\n\n## Overview\n\nReal text here.\n\n## Data Flows\n- one\n\n## Design Constraints\n- a\n"
        )
        (root / "a.py").write_text("def a(): pass\n")
        (root / "b.py").write_text("def b(): pass\n")
        (root / ".indexer" / "skills").mkdir(parents=True)
        (root / ".indexer" / "skills" / "codebase.md").write_text("skill")
        manifest = Manifest(
            last_indexed_commit="abc",
            indexed_at="now",
            files={
                "a.py": FileEntry(
                    hash=compute_hash(root / "a.py"),
                    wiki_page="wiki/shallow.md",
                    component_ids=[],
                ),
                "b.py": FileEntry(
                    hash=compute_hash(root / "b.py"),
                    wiki_page="wiki/deep.md",
                    component_ids=[],
                ),
            },
        )
        monkeypatch.setattr("indexer.verify.all_tracked_files", lambda r: ["a.py", "b.py"])
        monkeypatch.setattr("indexer.verify.is_git_repo", lambda r: True)
        cfg = Config()
        cfg.deep_hook = True
        report = scan(root, cfg, manifest, skip_deep=False)
        assert "wiki/shallow.md" in report.pages_missing_deep
        assert "wiki/deep.md" not in report.pages_missing_deep


def test_scan_deep_page_with_empty_narrative_not_flagged(monkeypatch):
    """Regression: a deep-enriched page whose LLM narrative came back empty
    still carries the deep marker (but no `## Overview`). It must NOT be flagged
    as missing-deep, or `--smart` would loop forever re-LLMing it."""
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        wiki = root / "wiki"
        wiki.mkdir()
        (wiki / "INDEX.md").write_text("# i")
        # Deep ran (marker present) but narrative was empty -> no `## Overview`.
        (wiki / "empty_deep.md").write_text(
            "# empty_deep/\n<!-- kiwiskil:deep -->\n\n## Modules\n\n## Key Symbols\n"
        )
        (root / "a.py").write_text("def a(): pass\n")
        (root / ".indexer" / "skills").mkdir(parents=True)
        (root / ".indexer" / "skills" / "codebase.md").write_text("skill")
        manifest = Manifest(
            last_indexed_commit="abc",
            indexed_at="now",
            files={
                "a.py": FileEntry(
                    hash=compute_hash(root / "a.py"),
                    wiki_page="wiki/empty_deep.md",
                    component_ids=[],
                ),
            },
        )
        monkeypatch.setattr("indexer.verify.all_tracked_files", lambda r: ["a.py"])
        monkeypatch.setattr("indexer.verify.is_git_repo", lambda r: True)
        cfg = Config()
        cfg.deep_hook = True
        report = scan(root, cfg, manifest, skip_deep=False)
        assert "wiki/empty_deep.md" not in report.pages_missing_deep


def test_scan_skips_deep_check_when_skip_deep_true(monkeypatch):
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        wiki = root / "wiki"
        wiki.mkdir()
        (wiki / "INDEX.md").write_text("# i")
        (wiki / "shallow.md").write_text("# shallow/\n\n## Modules\n")
        (root / "a.py").write_text("def a(): pass\n")
        (root / ".indexer" / "skills").mkdir(parents=True)
        (root / ".indexer" / "skills" / "codebase.md").write_text("skill")
        manifest = Manifest(
            last_indexed_commit="abc",
            indexed_at="now",
            files={
                "a.py": FileEntry(
                    hash=compute_hash(root / "a.py"),
                    wiki_page="wiki/shallow.md",
                    component_ids=[],
                ),
            },
        )
        monkeypatch.setattr("indexer.verify.all_tracked_files", lambda r: ["a.py"])
        monkeypatch.setattr("indexer.verify.is_git_repo", lambda r: True)
        cfg = Config()
        cfg.deep_hook = True
        report = scan(root, cfg, manifest, skip_deep=True)
        assert report.pages_missing_deep == []


def test_print_report_clean(capsys):
    print_report(VerifyReport())
    out = capsys.readouterr().out
    assert "Clean" in out or "0 issue" in out


def test_print_report_lists_each_drift(capsys):
    r = VerifyReport(
        stale_files=["a.py", "b.py"],
        missing_wiki_pages=["wiki/x.md"],
        hook_drift=True,
    )
    print_report(r)
    out = capsys.readouterr().out
    assert "stale" in out.lower()
    assert "a.py" in out
    assert "b.py" in out
    assert "wiki/x.md" in out
    assert "hook" in out.lower()
