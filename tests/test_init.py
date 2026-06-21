# tests/test_init.py
"""Slice C item 3 — `kiwiskil init` writes navigation guidance to both CLAUDE.md
and AGENTS.md from a shared constant, idempotently."""
import subprocess
from pathlib import Path

from click.testing import CliRunner

from indexer.cli import main, NAV_GUIDANCE


def _bootstrap_repo(root: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=root, check=True)


# The marker both CLAUDE.md and AGENTS.md are keyed on (matches verify.py).
MARKER = "Codebase Navigation"


def test_init_creates_agents_md():
    runner = CliRunner()
    with runner.isolated_filesystem() as d:
        root = Path(d)
        _bootstrap_repo(root)
        result = runner.invoke(main, ["init"])
        assert result.exit_code == 0, result.output
        agents = root / "AGENTS.md"
        assert agents.exists()
        assert MARKER in agents.read_text()


def test_init_creates_claude_md_unchanged_behavior():
    runner = CliRunner()
    with runner.isolated_filesystem() as d:
        root = Path(d)
        _bootstrap_repo(root)
        runner.invoke(main, ["init"])
        claude = root / "CLAUDE.md"
        assert claude.exists()
        assert MARKER in claude.read_text()


def test_init_appends_to_existing_agents_md():
    runner = CliRunner()
    with runner.isolated_filesystem() as d:
        root = Path(d)
        _bootstrap_repo(root)
        (root / "AGENTS.md").write_text("# My agents file\n\nExisting content.\n")
        runner.invoke(main, ["init"])
        text = (root / "AGENTS.md").read_text()
        assert "Existing content." in text  # preserved
        assert MARKER in text                # appended


def test_init_does_not_duplicate_agents_md_guidance():
    runner = CliRunner()
    with runner.isolated_filesystem() as d:
        root = Path(d)
        _bootstrap_repo(root)
        runner.invoke(main, ["init"])
        first = (root / "AGENTS.md").read_text()
        # second init must not duplicate the block
        runner.invoke(main, ["init"])
        second = (root / "AGENTS.md").read_text()
        assert first == second
        assert second.count(MARKER) == 1


def test_claude_and_agents_share_guidance_constant():
    # Both files derive from the same NAV_GUIDANCE constant.
    runner = CliRunner()
    with runner.isolated_filesystem() as d:
        root = Path(d)
        _bootstrap_repo(root)
        runner.invoke(main, ["init"])
        assert NAV_GUIDANCE.strip() in (root / "AGENTS.md").read_text()
        assert NAV_GUIDANCE.strip() in (root / "CLAUDE.md").read_text()
