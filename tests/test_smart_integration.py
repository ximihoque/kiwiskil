import tempfile
import subprocess
from pathlib import Path

from click.testing import CliRunner

from indexer.cli import main
from indexer.manifest import Manifest, FileEntry, save_manifest, load_manifest, compute_hash


def _bootstrap_repo(root: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=root, check=True)


def test_smart_rejects_combo_with_force():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(main, ["run", "--smart", "--force"])
        assert result.exit_code != 0
        assert "mutually exclusive" in result.output.lower() or "cannot" in result.output.lower()


def test_smart_rejects_combo_with_staged():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(main, ["run", "--smart", "--staged"])
        assert result.exit_code != 0


def test_smart_bails_when_no_indexable_files():
    # No manifest AND no indexable source: genuinely nothing to do -> bail.
    runner = CliRunner()
    with runner.isolated_filesystem() as d:
        root = Path(d)
        _bootstrap_repo(root)
        (root / "README.md").write_text("# not indexable\n")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=root, check=True)
        result = runner.invoke(main, ["run", "--smart", "--skip-deep"])
        assert result.exit_code != 0
        assert "nothing to index" in result.output.lower() or "no indexable" in result.output.lower()


def test_smart_dry_run_does_not_modify_filesystem():
    runner = CliRunner()
    with runner.isolated_filesystem() as d:
        root = Path(d)
        _bootstrap_repo(root)
        (root / "a.py").write_text("def a(): pass\n")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=root, check=True)
        manifest = Manifest(
            last_indexed_commit="abc",
            indexed_at="now",
            files={
                "a.py": FileEntry(hash="sha256:stale", wiki_page="wiki/root.md", component_ids=[]),
            },
        )
        save_manifest(root, manifest)
        before = (root / ".indexer" / "manifest.json").read_text()

        result = runner.invoke(main, ["run", "--smart", "--dry-run", "--skip-deep"])
        # Drift present -> non-zero exit (CI gate); but filesystem unchanged.
        assert result.exit_code != 0, result.output
        after = (root / ".indexer" / "manifest.json").read_text()
        assert before == after
        assert "stale" in result.output.lower()


def _stub_llm(monkeypatch):
    monkeypatch.setattr(
        "indexer.cli.describe_nodes",
        lambda nodes, cfg: {n.id: f"desc for {n.id}" for n in nodes},
    )
    monkeypatch.setattr(
        "indexer.cli.describe_files",
        lambda file_nodes, cfg: {f: f"module {f}" for f in file_nodes},
    )
    monkeypatch.setattr(
        "indexer.cli.deep_enrich_page",
        lambda **kwargs: {"narrative": "", "data_flows": [], "constraints": []},
    )
    monkeypatch.setattr(
        "indexer.cli.deep_enrich_index",
        lambda pages, cfg: {"overview": "", "flows": []},
    )


def test_smart_repairs_missing_wiki_page(monkeypatch):
    runner = CliRunner()
    with runner.isolated_filesystem() as d:
        root = Path(d)
        _bootstrap_repo(root)
        (root / "a.py").write_text("def a(): pass\n")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=root, check=True)

        a_hash = compute_hash(root / "a.py")
        manifest = Manifest(
            last_indexed_commit="abc",
            indexed_at="now",
            files={
                "a.py": FileEntry(hash=a_hash, wiki_page="wiki/root.md", component_ids=[]),
            },
        )
        save_manifest(root, manifest)

        _stub_llm(monkeypatch)

        result = runner.invoke(main, ["run", "--smart", "--skip-deep"])
        assert result.exit_code == 0, result.output
        assert (root / "wiki" / "root.md").exists()


def test_smart_clean_state_is_noop(monkeypatch):
    runner = CliRunner()
    with runner.isolated_filesystem() as d:
        root = Path(d)
        _bootstrap_repo(root)
        (root / "a.py").write_text("def a(): pass\n")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=root, check=True)

        # Fully consistent state
        wiki = root / "wiki"
        wiki.mkdir()
        (wiki / "root.md").write_text("# root/\n\n## Modules\n")
        (wiki / "INDEX.md").write_text("# index")
        (root / ".indexer" / "skills").mkdir(parents=True)
        (root / ".indexer" / "skills" / "codebase.md").write_text("skill")
        (root / ".gitignore").write_text(".indexer/cache/\n")
        (root / "CLAUDE.md").write_text("Codebase Navigation\n")
        (root / "AGENTS.md").write_text("Codebase Navigation\n")
        (root / ".git" / "hooks" / "pre-commit").write_text(
            "#!/bin/sh\n# managed by kiwiskil\nkiwiskil run --staged\n"
        )

        a_hash = compute_hash(root / "a.py")
        manifest = Manifest(
            last_indexed_commit="abc",
            indexed_at="now",
            files={
                "a.py": FileEntry(hash=a_hash, wiki_page="wiki/root.md", component_ids=[]),
            },
        )
        save_manifest(root, manifest)

        cfg_path = root / ".indexer.toml"
        cfg_path.write_text(
            '[llm]\nprovider="anthropic/claude-sonnet-4-6"\napi_key_env=""\n'
            '[indexer]\nwiki_dir="wiki"\nignore=[]\nmax_tokens_per_batch=8000\nmerge_threshold=2\n'
            '[hooks]\npre_commit=true\nsynthesize_commit_message=false\ndeep=false\n'
        )

        _stub_llm(monkeypatch)

        result = runner.invoke(main, ["run", "--smart", "--skip-deep"])
        assert result.exit_code == 0, result.output
        assert "Clean" in result.output or "nothing to repair" in result.output.lower()


def test_smart_fills_fresh_repo_with_no_manifest(monkeypatch):
    # No manifest at all, but there ARE indexable tracked files:
    # --smart should perform a full initial index instead of bailing.
    runner = CliRunner()
    with runner.isolated_filesystem() as d:
        root = Path(d)
        _bootstrap_repo(root)
        (root / "a.py").write_text("def a(): pass\n")
        (root / "b.py").write_text("def b(): pass\n")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=root, check=True)

        _stub_llm(monkeypatch)

        result = runner.invoke(main, ["run", "--smart", "--skip-deep"])
        assert result.exit_code == 0, result.output
        # Full index ran: manifest + wiki + INDEX + skill all created.
        manifest_path = root / ".indexer" / "manifest.json"
        assert manifest_path.exists()
        manifest = load_manifest(root)
        assert "a.py" in manifest.files
        assert "b.py" in manifest.files
        assert (root / "wiki" / "INDEX.md").exists()
        assert (root / ".indexer" / "skills" / "codebase.md").exists()


def test_smart_dry_run_reports_full_initial_index_without_changes(monkeypatch):
    # Dry-run on a fresh repo (no manifest) must REPORT a full initial index
    # of N files and change nothing.
    runner = CliRunner()
    with runner.isolated_filesystem() as d:
        root = Path(d)
        _bootstrap_repo(root)
        (root / "a.py").write_text("def a(): pass\n")
        (root / "b.py").write_text("def b(): pass\n")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=root, check=True)

        _stub_llm(monkeypatch)

        result = runner.invoke(main, ["run", "--smart", "--dry-run", "--skip-deep"])
        # Drift present (nothing indexed yet) -> non-zero exit for CI gate.
        assert result.exit_code != 0, result.output
        assert "full initial index" in result.output.lower()
        assert "2 file" in result.output
        # Nothing written.
        assert not (root / ".indexer" / "manifest.json").exists()
        assert not (root / "wiki").exists()


def test_smart_fills_never_indexed_tracked_file(monkeypatch):
    # Manifest exists and is otherwise consistent, but a new tracked file was
    # never indexed. --smart must index it (untracked_files path).
    runner = CliRunner()
    with runner.isolated_filesystem() as d:
        root = Path(d)
        _bootstrap_repo(root)
        (root / "a.py").write_text("def a(): pass\n")
        (root / "b.py").write_text("def b(): pass\n")  # never-indexed
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=root, check=True)

        # Consistent state covering only a.py
        wiki = root / "wiki"
        wiki.mkdir()
        (wiki / "root.md").write_text("# root/\n\n## Modules\n")
        (wiki / "INDEX.md").write_text("# index")
        (root / ".indexer" / "skills").mkdir(parents=True)
        (root / ".indexer" / "skills" / "codebase.md").write_text("skill")
        (root / ".gitignore").write_text(".indexer/cache/\n")
        (root / "CLAUDE.md").write_text("Codebase Navigation\n")
        (root / "AGENTS.md").write_text("Codebase Navigation\n")
        (root / ".git" / "hooks" / "pre-commit").write_text(
            "#!/bin/sh\n# managed by kiwiskil\nkiwiskil run --staged\n"
        )
        cfg_path = root / ".indexer.toml"
        cfg_path.write_text(
            '[llm]\nprovider="anthropic/claude-sonnet-4-6"\napi_key_env=""\n'
            '[indexer]\nwiki_dir="wiki"\nignore=[]\nmax_tokens_per_batch=8000\nmerge_threshold=2\n'
            '[hooks]\npre_commit=true\nsynthesize_commit_message=false\ndeep=false\n'
        )

        manifest = Manifest(
            last_indexed_commit="abc",
            indexed_at="now",
            files={
                "a.py": FileEntry(hash=compute_hash(root / "a.py"), wiki_page="wiki/root.md", component_ids=[]),
            },
        )
        save_manifest(root, manifest)

        _stub_llm(monkeypatch)

        result = runner.invoke(main, ["run", "--smart", "--skip-deep"])
        assert result.exit_code == 0, result.output
        manifest = load_manifest(root)
        assert "b.py" in manifest.files


def test_smart_dry_run_clean_repo_exits_zero(monkeypatch):
    # CI gate: a clean repo under --smart --dry-run must exit 0.
    runner = CliRunner()
    with runner.isolated_filesystem() as d:
        root = Path(d)
        _bootstrap_repo(root)
        (root / "a.py").write_text("def a(): pass\n")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=root, check=True)

        wiki = root / "wiki"
        wiki.mkdir()
        (wiki / "root.md").write_text("# root/\n\n## Modules\n")
        (wiki / "INDEX.md").write_text("# index")
        (root / ".indexer" / "skills").mkdir(parents=True)
        (root / ".indexer" / "skills" / "codebase.md").write_text("skill")
        (root / ".gitignore").write_text(".indexer/cache/\n")
        (root / "CLAUDE.md").write_text("Codebase Navigation\n")
        (root / "AGENTS.md").write_text("Codebase Navigation\n")
        (root / ".git" / "hooks" / "pre-commit").write_text(
            "#!/bin/sh\n# managed by kiwiskil\nkiwiskil run --staged\n"
        )
        cfg_path = root / ".indexer.toml"
        cfg_path.write_text(
            '[llm]\nprovider="anthropic/claude-sonnet-4-6"\napi_key_env=""\n'
            '[indexer]\nwiki_dir="wiki"\nignore=[]\nmax_tokens_per_batch=8000\nmerge_threshold=2\n'
            '[hooks]\npre_commit=true\nsynthesize_commit_message=false\ndeep=false\n'
        )
        manifest = Manifest(
            last_indexed_commit="abc",
            indexed_at="now",
            files={
                "a.py": FileEntry(hash=compute_hash(root / "a.py"), wiki_page="wiki/root.md", component_ids=[]),
            },
        )
        save_manifest(root, manifest)

        _stub_llm(monkeypatch)

        result = runner.invoke(main, ["run", "--smart", "--dry-run", "--skip-deep"])
        assert result.exit_code == 0, result.output


def test_smart_dry_run_drift_exits_nonzero():
    # CI gate: drift present (stale file) under --smart --dry-run must exit non-zero.
    runner = CliRunner()
    with runner.isolated_filesystem() as d:
        root = Path(d)
        _bootstrap_repo(root)
        (root / "a.py").write_text("def a(): pass\n")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=root, check=True)
        manifest = Manifest(
            last_indexed_commit="abc",
            indexed_at="now",
            files={
                "a.py": FileEntry(hash="sha256:stale", wiki_page="wiki/root.md", component_ids=[]),
            },
        )
        save_manifest(root, manifest)

        result = runner.invoke(main, ["run", "--smart", "--dry-run", "--skip-deep"])
        assert result.exit_code != 0, result.output


def test_run_deletes_orphan_page_when_source_deleted(monkeypatch):
    """Deleting the last source file in a group must remove its wiki page on the
    next plain `run` — not just prune the manifest entry (the bug)."""
    _stub_llm(monkeypatch)
    runner = CliRunner()
    with runner.isolated_filesystem() as d:
        root = Path(d)
        _bootstrap_repo(root)
        # merge_threshold=1 so each folder is its own group -> its own page.
        (root / ".indexer.toml").write_text(
            '[llm]\nprovider="anthropic/claude-sonnet-4-6"\napi_key_env=""\n'
            '[indexer]\nwiki_dir="wiki"\nignore=[]\nmax_tokens_per_batch=8000\nmerge_threshold=1\n'
            '[hooks]\npre_commit=true\nsynthesize_commit_message=false\ndeep=false\n'
        )
        (root / "alpha").mkdir()
        (root / "beta").mkdir()
        (root / "alpha" / "a.py").write_text("def a(): pass\n")
        (root / "beta" / "b.py").write_text("def b(): pass\n")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=root, check=True)

        # Initial full index.
        r1 = runner.invoke(main, ["run", "--force", "--skip-deep"])
        assert r1.exit_code == 0, r1.output
        pages = {p.name for p in (root / "wiki").glob("*.md")}
        assert "beta.md" in pages, pages

        # Delete beta's only file and commit the deletion.
        (root / "beta" / "b.py").unlink()
        subprocess.run(["git", "add", "-A"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "rm beta"], cwd=root, check=True)

        # Plain incremental run should now clean up the orphan page.
        r2 = runner.invoke(main, ["run", "--skip-deep"])
        assert r2.exit_code == 0, r2.output

        pages_after = {p.name for p in (root / "wiki").glob("*.md")}
        assert "beta.md" not in pages_after, f"orphan page lingered: {pages_after}"
        assert "alpha.md" in pages_after
        # Manifest no longer references the deleted file.
        m = load_manifest(root)
        assert "beta/b.py" not in m.files
