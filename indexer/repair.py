from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import click

from indexer.cli import (
    _index_files,
    _finalise_index_and_skill,
    _ensure_cache_gitignore,
    _ensure_nav_guidance,
)
from indexer.config import Config
from indexer.git import all_tracked_files, is_git_repo, current_commit
from indexer.hooks import install_hook
from indexer.manifest import Manifest, compute_hash, save_manifest, file_entry_for
from indexer.verify import VerifyReport
from indexer.wiki import IndexEntry, page_relpath


@dataclass
class RepairPlan:
    files_to_reindex: list[str] = field(default_factory=list)
    orphan_pages_to_delete: list[str] = field(default_factory=list)
    dangling_entries_to_prune: list[str] = field(default_factory=list)
    fix_claude_md: bool = False
    fix_agents_md: bool = False
    fix_gitignore: bool = False
    fix_hook: bool = False
    rebuild_index_and_skill: bool = False

    def has_work(self) -> bool:
        return bool(
            self.files_to_reindex
            or self.orphan_pages_to_delete
            or self.dangling_entries_to_prune
            or self.fix_claude_md
            or self.fix_agents_md
            or self.fix_gitignore
            or self.fix_hook
            or self.rebuild_index_and_skill
        )


def plan(report: VerifyReport, root: Path, cfg: Config, manifest: Manifest, skip_deep: bool) -> RepairPlan:
    """
    Compute the minimum set of repair operations from a VerifyReport.

    Source files referenced by missing wiki pages or pages-missing-deep are
    pulled from the existing manifest. Whole groups get re-indexed — no
    per-symbol patching.

    INDEX + skill rebuild whenever the wiki structure changes (any source-file
    reindex, orphan deletion, dangling prune) or when INDEX/skill is missing.
    Cosmetic fixes (CLAUDE.md, .gitignore, hook) don't trigger a rebuild on
    their own.
    """
    p = RepairPlan()

    if report.is_clean():
        return p

    files: set[str] = set()
    files.update(report.stale_files)
    files.update(report.untracked_files)

    pages_to_recover = set(report.missing_wiki_pages)
    if not skip_deep:
        pages_to_recover.update(report.pages_missing_deep)

    for rel_path, entry in manifest.files.items():
        if entry.wiki_page in pages_to_recover:
            files.add(rel_path)

    files -= set(report.dangling_manifest_entries)

    p.files_to_reindex = sorted(files)
    p.orphan_pages_to_delete = list(report.orphan_wiki_pages)
    p.dangling_entries_to_prune = list(report.dangling_manifest_entries)
    p.fix_claude_md = report.claude_md_snippet_missing
    p.fix_agents_md = report.agents_md_snippet_missing
    p.fix_gitignore = report.gitignore_entry_missing
    p.fix_hook = report.hook_drift

    structural_change = bool(
        p.files_to_reindex
        or p.orphan_pages_to_delete
        or p.dangling_entries_to_prune
    )
    p.rebuild_index_and_skill = (
        structural_change
        or report.index_missing
        or report.skill_missing
    )

    return p


def execute(plan_obj: RepairPlan, root: Path, cfg: Config, manifest: Manifest, skip_deep: bool) -> None:
    """
    Execute a RepairPlan against the filesystem and manifest.

    Order:
      1. Re-index dirty source files (LLM work — may fail mid-way).
      2. Delete orphan wiki pages.
      3. Prune dangling manifest entries.
      4. Restore CLAUDE.md / .gitignore / hook.
      5. Update manifest entries for successfully re-indexed files.
      6. Rebuild INDEX + skill (if planned).
      7. Persist manifest.
    """
    all_nodes: list = []
    page_enrichments: dict = {}
    groups: dict = {}

    # ── Step 1: re-index dirty source files ───────────────────────────────────
    if plan_obj.files_to_reindex:
        click.echo(f"\n  Repairing  ({len(plan_obj.files_to_reindex)} file(s))")
        result = _index_files(root, cfg, plan_obj.files_to_reindex, skip_deep)
        _descriptions, _file_descriptions, all_nodes, page_enrichments, groups, _entries = result

    # ── Step 2: delete orphan wiki pages ──────────────────────────────────────
    if plan_obj.orphan_pages_to_delete:
        click.echo("\n  Cleanup")
        for rel_page in plan_obj.orphan_pages_to_delete:
            page = root / rel_page
            if page.exists():
                page.unlink()
                click.echo(f"    ✓  pruned {rel_page}")

    # ── Step 3: prune dangling manifest entries ───────────────────────────────
    for rel_path in plan_obj.dangling_entries_to_prune:
        if rel_path in manifest.files:
            del manifest.files[rel_path]
            click.echo(f"    ✓  pruned manifest entry: {rel_path}")

    # ── Step 4: restore CLAUDE.md / AGENTS.md / .gitignore / hook ─────────────
    if plan_obj.fix_claude_md:
        _ensure_nav_guidance(root / "CLAUDE.md", "CLAUDE.md")
        click.echo("    ✓  restored CLAUDE.md snippet")

    if plan_obj.fix_agents_md:
        _ensure_nav_guidance(root / "AGENTS.md", "AGENTS.md")
        click.echo("    ✓  restored AGENTS.md snippet")

    if plan_obj.fix_gitignore:
        _ensure_cache_gitignore(root, verbose=False)
        click.echo("    ✓  restored .gitignore cache entry")

    if plan_obj.fix_hook and is_git_repo(root) and cfg.pre_commit:
        install_hook(root, skip_deep=not cfg.deep_hook)
        click.echo("    ✓  reinstalled pre-commit hook")

    # ── Step 5: update manifest entries for re-indexed files ──────────────────
    if all_nodes:
        for rel_path in plan_obj.files_to_reindex:
            abs_path = root / rel_path
            if abs_path.exists():
                file_hash = compute_hash(abs_path)
                group = groups.get(rel_path, rel_path)
                manifest.files[rel_path] = file_entry_for(
                    file_hash,
                    page_relpath(cfg.wiki_dir, group),
                    [n for n in all_nodes if n.file == rel_path],
                )

    # ── Step 6: rebuild INDEX + skill ─────────────────────────────────────────
    # We only rebuild if (a) repair changed structure and (b) we successfully
    # re-indexed something this run. Reconstruct full IndexEntry list from
    # the manifest so the INDEX covers the whole repo, not just touched groups.
    if plan_obj.rebuild_index_and_skill and all_nodes:
        full_entries = _index_entries_from_manifest(manifest)
        total_symbols = sum(len(fe.component_ids) for fe in manifest.files.values())
        # NOTE: `all_nodes` here is only the *repaired* groups' nodes, not the
        # whole repo. The Repo Map and Core Abstractions are global rankings, so
        # computing them from a partial node set would be silently WRONG (worse
        # than absent). Pass all_nodes=None to OMIT those sections during repair;
        # the next full `kiwiskil run` recomputes them over the complete graph.
        # (Same soft-degradation already accepted for INDEX entry points.)
        _finalise_index_and_skill(
            root, cfg, full_entries, page_enrichments,
            total_symbols=total_symbols,
            total_files=len(manifest.files),
            skip_deep=skip_deep,
            all_nodes=None,
        )

    # ── Step 7: persist manifest ──────────────────────────────────────────────
    manifest.last_indexed_commit = current_commit(root) or manifest.last_indexed_commit
    manifest.indexed_at = datetime.now(timezone.utc).isoformat()
    save_manifest(root, manifest)


def _index_entries_from_manifest(manifest: Manifest) -> list[IndexEntry]:
    """
    Reconstruct IndexEntry list from manifest state for INDEX rebuild.
    Entry points are left empty for non-regenerated groups — a soft
    degradation accepted by smart-mode (next full `kiwiskil run` repairs it).
    """
    by_page: dict[str, list[str]] = {}
    for rel_path, entry in manifest.files.items():
        by_page.setdefault(entry.wiki_page, []).append(rel_path)

    return [
        IndexEntry(
            path=page,
            covers=", ".join(sorted(files)),
            entry_points=[],
        )
        for page, files in sorted(by_page.items())
    ]
