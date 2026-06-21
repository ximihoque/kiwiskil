from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path

import click

from indexer.config import Config
from indexer.git import all_tracked_files, is_git_repo
from indexer.hooks import HOOK_MARKER
from indexer.langs import is_indexable
from indexer.manifest import Manifest

CLAUDE_MD_MARKER = "Codebase Navigation"
CACHE_GITIGNORE_ENTRY = ".indexer/cache/"
# Always written to a page when deep enrichment ran (see templates/page.md.j2),
# even if the narrative came back empty. Keep in sync with the template.
DEEP_MARKER = "<!-- kiwiskil:deep -->"


def _is_indexable(path: str, cfg: Config) -> bool:
    return is_indexable(path, cfg.ignore)


@dataclass
class VerifyReport:
    stale_files: list[str] = field(default_factory=list)
    untracked_files: list[str] = field(default_factory=list)
    dangling_manifest_entries: list[str] = field(default_factory=list)
    missing_wiki_pages: list[str] = field(default_factory=list)
    orphan_wiki_pages: list[str] = field(default_factory=list)
    pages_missing_deep: list[str] = field(default_factory=list)
    skill_missing: bool = False
    index_missing: bool = False
    manifest_missing: bool = False
    claude_md_snippet_missing: bool = False
    agents_md_snippet_missing: bool = False
    gitignore_entry_missing: bool = False
    hook_drift: bool = False

    def total_issues(self) -> int:
        n = (
            len(self.stale_files)
            + len(self.untracked_files)
            + len(self.dangling_manifest_entries)
            + len(self.missing_wiki_pages)
            + len(self.orphan_wiki_pages)
            + len(self.pages_missing_deep)
        )
        for b in (
            self.skill_missing,
            self.index_missing,
            self.manifest_missing,
            self.claude_md_snippet_missing,
            self.agents_md_snippet_missing,
            self.gitignore_entry_missing,
            self.hook_drift,
        ):
            if b:
                n += 1
        return n

    def is_clean(self) -> bool:
        return self.total_issues() == 0


def scan(root: Path, cfg: Config, manifest: Manifest, skip_deep: bool = False, check_hook: bool = True) -> VerifyReport:
    """
    Verify the state of generated artifacts against the manifest and filesystem.
    Deterministic: no LLM, no re-parse.

    Returns a VerifyReport listing every drift class found. If the manifest has
    never been written (last_indexed_commit is None and files is empty), the
    report flags manifest_missing and skips all other checks; the caller
    (`cli._run_smart`) treats this as a fill signal and performs a full initial
    index (a never-indexed repo is drift too), bailing only when there are no
    indexable source files.
    """
    report = VerifyReport()

    if manifest.last_indexed_commit is None and not manifest.files:
        report.manifest_missing = True
        return report

    # Source file drift (requires git)
    if is_git_repo(root):
        tracked = [f for f in all_tracked_files(root) if _is_indexable(f, cfg)]
        tracked_set = set(tracked)
        report.stale_files = manifest.stale_files(root, tracked)
        report.untracked_files = sorted(tracked_set - set(manifest.files.keys()))
        report.dangling_manifest_entries = sorted(set(manifest.files.keys()) - tracked_set)

    # Wiki page drift
    wiki_dir = root / cfg.wiki_dir
    referenced_pages = {entry.wiki_page for entry in manifest.files.values()}
    for page in sorted(referenced_pages):
        if not (root / page).exists():
            report.missing_wiki_pages.append(page)

    if wiki_dir.exists():
        actual_pages = {
            f"{cfg.wiki_dir}/{p.name}"
            for p in wiki_dir.glob("*.md")
            if p.name != "INDEX.md"
        }
        report.orphan_wiki_pages = sorted(actual_pages - referenced_pages)

    # INDEX + skill file existence
    if not (wiki_dir / "INDEX.md").exists():
        report.index_missing = True
    if not (root / ".indexer" / "skills" / "codebase.md").exists():
        report.skill_missing = True

    # CLAUDE.md snippet
    claude_md = root / "CLAUDE.md"
    if claude_md.exists():
        if CLAUDE_MD_MARKER not in claude_md.read_text():
            report.claude_md_snippet_missing = True
    else:
        report.claude_md_snippet_missing = True

    # AGENTS.md snippet (cross-tool nav guidance; written by `init` alongside CLAUDE.md)
    agents_md = root / "AGENTS.md"
    if agents_md.exists():
        if CLAUDE_MD_MARKER not in agents_md.read_text():
            report.agents_md_snippet_missing = True
    else:
        report.agents_md_snippet_missing = True

    # .gitignore cache entry
    gitignore = root / ".gitignore"
    if gitignore.exists():
        if CACHE_GITIGNORE_ENTRY not in gitignore.read_text():
            report.gitignore_entry_missing = True
    else:
        report.gitignore_entry_missing = True

    # Pre-commit hook. Lives in .git/hooks (not committed, absent on fresh CI
    # checkouts), so a committed-tree drift-gate passes check_hook=False to skip
    # it — otherwise it would always fail in CI for everyone.
    if check_hook and cfg.pre_commit and is_git_repo(root):
        hook_path = root / ".git" / "hooks" / "pre-commit"
        if not hook_path.exists() or HOOK_MARKER not in hook_path.read_text():
            report.hook_drift = True

    # Deep-mode section check — only when deep mode is active for this run.
    # We look for the always-present `<!-- kiwiskil:deep -->` marker, NOT the
    # optional `## Overview` heading: the LLM can legitimately return an empty
    # narrative, so a page can be deep-enriched yet have no Overview section.
    # Keying on the marker avoids a perpetual drift loop on contentless groups.
    if cfg.deep_hook and not skip_deep:
        for page in sorted(referenced_pages):
            page_path = root / page
            if not page_path.exists():
                continue  # already counted as missing
            content = page_path.read_text()
            if DEEP_MARKER not in content:
                report.pages_missing_deep.append(page)

    return report


def print_report(report: VerifyReport) -> None:
    """Pretty-print a VerifyReport to stdout via click.echo."""
    if report.is_clean():
        click.echo("  ✓  Clean — nothing to repair.")
        return

    click.echo("  Verifying")

    if report.manifest_missing:
        click.echo("    ✗  no index yet — a full initial index is needed")
        return

    if report.stale_files:
        click.echo(f"    ✗  {len(report.stale_files)} stale file(s) (hash mismatch)")
        for f in report.stale_files:
            click.echo(f"         {f}")
    if report.untracked_files:
        click.echo(f"    ✗  {len(report.untracked_files)} untracked source file(s)")
        for f in report.untracked_files:
            click.echo(f"         {f}")
    if report.dangling_manifest_entries:
        click.echo(f"    ✗  {len(report.dangling_manifest_entries)} dangling manifest entry(ies)")
        for f in report.dangling_manifest_entries:
            click.echo(f"         {f}")
    if report.missing_wiki_pages:
        click.echo(f"    ✗  {len(report.missing_wiki_pages)} missing wiki page(s)")
        for f in report.missing_wiki_pages:
            click.echo(f"         {f}")
    if report.orphan_wiki_pages:
        click.echo(f"    ✗  {len(report.orphan_wiki_pages)} orphan wiki page(s)")
        for f in report.orphan_wiki_pages:
            click.echo(f"         {f}")
    if report.pages_missing_deep:
        click.echo(f"    ✗  {len(report.pages_missing_deep)} page(s) missing deep sections")
        for f in report.pages_missing_deep:
            click.echo(f"         {f}")
    if report.index_missing:
        click.echo("    ✗  wiki/INDEX.md missing")
    if report.skill_missing:
        click.echo("    ✗  .indexer/skills/codebase.md missing")
    if report.claude_md_snippet_missing:
        click.echo("    ✗  CLAUDE.md snippet missing")
    if report.agents_md_snippet_missing:
        click.echo("    ✗  AGENTS.md snippet missing")
    if report.gitignore_entry_missing:
        click.echo("    ✗  .gitignore cache entry missing")
    if report.hook_drift:
        click.echo("    ✗  pre-commit hook drift")

    click.echo(f"\n  {report.total_issues()} issue(s) found")
