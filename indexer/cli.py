# indexer/cli.py
from __future__ import annotations
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import click

from indexer.config import Config, load_config, save_config
from indexer.langs import is_indexable
from indexer.manifest import load_manifest, save_manifest, compute_hash, file_entry_for
from indexer.git import (
    staged_files, all_tracked_files, current_commit,
    changed_files_since, is_git_repo
)
from indexer.ast_parser import parse_file, load_cached_nodes, save_cached_nodes, compute_hash_short
from indexer.llm import describe_nodes, describe_files, deep_enrich_page, deep_enrich_index, synthesize_commit_message
from indexer.grouper import density_group
from indexer.graph import build_blast_radius_map, god_nodes, repo_map
from indexer.wiki import build_page, build_index, write_page, write_index, PageContext, IndexEntry, TEMPLATES_DIR, page_relpath
from indexer.hooks import install_hook, remove_hook

# Shared navigation guidance, written to both CLAUDE.md and AGENTS.md. The
# "Codebase Navigation" heading doubles as the idempotency marker (also used by
# verify.py's CLAUDE_MD_MARKER).
NAV_GUIDANCE = """
## Codebase Navigation

This repo is indexed with kiwiskil. Before reading any source file or answering any code question:

1. Load `.indexer/skills/codebase.md` as a skill — it contains the full navigation workflow.
2. Read `wiki/INDEX.md` for the system overview and module map.
3. Match the question to a wiki page, look up symbols there, and only read source when you know the exact file and line range.

Do not read source files speculatively. The wiki gives you structure and relationships in a fraction of the tokens.

- Wiki pages: `wiki/` — grouped by logical density, not directory structure
- Manifest: `.indexer/manifest.json` — maps every file to its wiki page and component IDs
- Component IDs: `relative/path.py::ClassName.method_name`
"""

# Backwards-compatible alias (repair.py and verify imports rely on this name).
CLAUDEMD_SNIPPET = NAV_GUIDANCE

# The heading used to detect whether guidance has already been written.
NAV_GUIDANCE_MARKER = "Codebase Navigation"


def _ensure_nav_guidance(target: Path, label: str) -> None:
    """Write NAV_GUIDANCE to `target`, appending if the file exists and creating
    it otherwise. Idempotent: skips if the marker is already present."""
    if target.exists():
        existing = target.read_text()
        if NAV_GUIDANCE_MARKER in existing:
            return  # already present — do not duplicate
        target.write_text(existing + "\n" + NAV_GUIDANCE)
        click.echo(f"Appended to {label}.")
    else:
        target.write_text(NAV_GUIDANCE.lstrip())
        click.echo(f"Created {label}.")


@click.group()
def main():
    pass


@main.command()
def init():
    """Create .indexer.toml, install pre-commit hook, append to CLAUDE.md."""
    root = Path.cwd()
    cfg = load_config(root)
    save_config(root, cfg)
    click.echo(f"Created {root / '.indexer.toml'}")

    _ensure_cache_gitignore(root, verbose=True)

    if is_git_repo(root) and cfg.pre_commit:
        install_hook(root, skip_deep=not cfg.deep_hook)
        mode = "--staged --skip-deep" if not cfg.deep_hook else "--staged"
        click.echo(f"Installed pre-commit hook  (kiwiskil run {mode})")

    # Navigation guidance for AI agents — same content in both files, one source.
    _ensure_nav_guidance(root / "CLAUDE.md", "CLAUDE.md")
    _ensure_nav_guidance(root / "AGENTS.md", "AGENTS.md")


@main.command()
@click.option("--staged", is_flag=True, help="Incremental: only staged files (used by hook)")
@click.option("--force", is_flag=True, help="Force full re-index regardless of manifest")
@click.option("--smart", is_flag=True, help="Verify generated artifacts and repair only what's broken")
@click.option("--dry-run", is_flag=True, help="With --smart: report drift without fixing anything")
@click.option("--skip-deep", is_flag=True, help="Skip narrative, data flows, and design constraints (faster, fewer tokens)")
def run(staged: bool, force: bool, smart: bool, dry_run: bool, skip_deep: bool):
    """Index the codebase and generate wiki pages."""
    root = Path.cwd()
    cfg = load_config(root)
    manifest = load_manifest(root)

    if smart and (force or staged):
        raise click.UsageError("--smart is mutually exclusive with --force and --staged")
    if dry_run and not smart:
        raise click.UsageError("--dry-run can only be used with --smart")

    if smart:
        _run_smart(root, cfg, manifest, dry_run=dry_run, skip_deep=skip_deep)
        return

    # Ensure cache is gitignored even if user skipped init
    _ensure_cache_gitignore(root)

    # Determine which files to process
    if staged:
        candidates = staged_files(root)
    elif force or manifest.last_indexed_commit is None:
        candidates = [f for f in all_tracked_files(root) if _is_indexable(f, cfg)]
    else:
        git_changed = changed_files_since(root, manifest.last_indexed_commit) if is_git_repo(root) else []
        all_files = [f for f in all_tracked_files(root) if _is_indexable(f, cfg)]
        stale = manifest.stale_files(root, all_files)
        candidates = list(set(git_changed + stale))

    candidates = [f for f in candidates if _is_indexable(f, cfg)]

    if not candidates:
        click.echo("  Nothing to index.")
        return

    mode = "staged" if staged else ("full re-index" if force else "incremental")
    _index_and_persist(root, cfg, manifest, candidates, skip_deep, mode=mode, staged=staged)


@main.command()
def status():
    """Show last indexed commit, stale files, manifest stats."""
    root = Path.cwd()
    cfg = load_config(root)
    manifest = load_manifest(root)

    click.echo(f"Last indexed commit: {manifest.last_indexed_commit or 'never'}")
    click.echo(f"Indexed at:          {manifest.indexed_at or 'n/a'}")
    click.echo(f"Tracked files:       {len(manifest.files)}")

    if is_git_repo(root):
        all_files = [f for f in all_tracked_files(root) if _is_indexable(f, cfg)]
        stale = manifest.stale_files(root, all_files)
        click.echo(f"Stale files:         {len(stale)}")
        if stale:
            for f in stale[:10]:
                click.echo(f"  {f}")


@main.group()
def hook():
    """Manage the pre-commit hook."""
    pass


@hook.command("install")
def hook_install():
    """Install the pre-commit hook in the current repo."""
    root = Path.cwd()
    cfg = load_config(root)
    install_hook(root, skip_deep=not cfg.deep_hook)
    mode = "--staged --skip-deep" if not cfg.deep_hook else "--staged"
    click.echo(f"Pre-commit hook installed  (kiwiskil run {mode})")


@hook.command("remove")
def hook_remove():
    """Remove the pre-commit hook from the current repo."""
    root = Path.cwd()
    remove_hook(root)
    click.echo("Pre-commit hook removed.")


CACHE_GITIGNORE_ENTRY = ".indexer/cache/"


def _ensure_cache_gitignore(root: Path, verbose: bool = False) -> None:
    """Add .indexer/cache/ to the root .gitignore, creating it if needed."""
    gitignore = root / ".gitignore"
    if gitignore.exists():
        content = gitignore.read_text()
        if CACHE_GITIGNORE_ENTRY in content:
            return  # already present
        updated = content.rstrip() + "\n\n# kiwiskil\n" + CACHE_GITIGNORE_ENTRY + "\n"
        gitignore.write_text(updated)
        if verbose:
            click.echo(f"Added {CACHE_GITIGNORE_ENTRY} to .gitignore")
    else:
        gitignore.write_text(f"# kiwiskil\n{CACHE_GITIGNORE_ENTRY}\n")
        if verbose:
            click.echo(f"Created .gitignore with {CACHE_GITIGNORE_ENTRY}")


def _is_indexable(path: str, cfg: Config) -> bool:
    return is_indexable(path, cfg.ignore)


def _index_files(
    root: Path,
    cfg: Config,
    candidates: list[str],
    skip_deep: bool,
) -> tuple[dict, dict, list, dict, dict, list]:
    """
    Run Phases 1-5 of the indexing pipeline on a candidate file list.

    Returns:
      (descriptions, file_descriptions, all_nodes, page_enrichments, groups, index_entries)

    Side effects: writes AST cache files; writes wiki pages for the touched
    groups. Does NOT touch INDEX.md, skill file, manifest, gitignore, hook, or
    CLAUDE.md — callers (`run` and `repair.execute`) finalise those.
    """
    # ── Phase 1: Parse ────────────────────────────────────────────────────────
    click.echo("  Parsing")
    all_nodes = []
    cached_count = 0
    for rel_path in candidates:
        abs_path = root / rel_path
        file_hash = compute_hash_short(abs_path)
        cached = load_cached_nodes(root, file_hash)
        if cached is not None:
            all_nodes.extend(cached)
            cached_count += 1
            click.echo(f"    ✓  {rel_path}  (cached)")
        else:
            nodes = parse_file(abs_path, root)
            save_cached_nodes(root, file_hash, nodes)
            all_nodes.extend(nodes)
            symbol_count = len(nodes)
            click.echo(f"    ✓  {rel_path}  ({symbol_count} symbol{'s' if symbol_count != 1 else ''})")

    if not all_nodes:
        click.echo("\n  No symbols found.")
        return {}, {}, [], {}, {}, []

    total_symbols = len(all_nodes)
    click.echo(f"\n    {total_symbols} symbols across {len(candidates)} files  ({cached_count} from cache)\n")

    # ── Phase 2: Cross-reference ──────────────────────────────────────────────
    click.echo("  Cross-referencing calls")
    call_index: dict[str, list[str]] = {}
    for node in all_nodes:
        for callee_name in node.calls:
            call_index.setdefault(callee_name, []).append(node.id)
    for node in all_nodes:
        bare_name = node.id.split("::")[-1]
        node.called_by = call_index.get(bare_name, [])
    linked = sum(1 for n in all_nodes if n.called_by)
    click.echo(f"    {linked} symbols linked via call graph\n")

    # ── Phase 3: LLM descriptions ─────────────────────────────────────────────
    descriptions: dict[str, str] = {}
    batch, batch_size = [], 0
    batches = []
    for node in all_nodes:
        node_size = len(node.docstring or "") + len(" ".join(node.calls)) + 50
        if batch_size + node_size > cfg.max_tokens_per_batch and batch:
            batches.append(batch)
            batch, batch_size = [], 0
        batch.append(node)
        batch_size += node_size
    if batch:
        batches.append(batch)

    click.echo(f"  Describing symbols  ({len(batches)} LLM batch{'es' if len(batches) != 1 else ''})")
    for i, b in enumerate(batches, 1):
        click.echo(f"    batch {i}/{len(batches)}  ({len(b)} symbols)  ...", nl=False)
        result = describe_nodes(b, cfg)
        descriptions.update(result)
        filled = sum(1 for v in result.values() if v)
        click.echo(f"  {filled}/{len(b)} described")

    # ── Phase 4: File-level descriptions ─────────────────────────────────────
    click.echo(f"\n  Describing modules  ({len(set(n.file for n in all_nodes))} files)  ...", nl=False)
    file_nodes: dict[str, list] = {}
    for node in all_nodes:
        file_nodes.setdefault(node.file, []).append(node)
    file_descriptions = describe_files(file_nodes, cfg)
    filled_files = sum(1 for v in file_descriptions.values() if v)
    click.echo(f"  {filled_files}/{len(file_nodes)} described\n")

    # ── Phase 5: Group → wiki pages ───────────────────────────────────────────
    click.echo("  Writing wiki")
    groups = density_group(candidates, merge_threshold=cfg.merge_threshold)
    group_nodes: dict[str, list] = {}
    for node in all_nodes:
        group = groups.get(node.file, node.file)
        group_nodes.setdefault(group, []).append(node)

    wiki_dir = root / cfg.wiki_dir
    index_entries = []

    page_enrichments: dict[str, dict] = {}
    if not skip_deep:
        click.echo(f"\n  Deep enrichment  ({len(group_nodes)} page{'s' if len(group_nodes) != 1 else ''})  —  narrative + flows + constraints")
        for group_label, nodes in group_nodes.items():
            click.echo(f"    {group_label}  ...", nl=False)
            enrichment = deep_enrich_page(
                group_label=group_label,
                files=list({n.file for n in nodes}),
                nodes=nodes,
                descriptions=descriptions,
                cfg=cfg,
            )
            page_enrichments[group_label] = enrichment
            parts = []
            if enrichment["narrative"]: parts.append("narrative")
            if enrichment["data_flows"]: parts.append(f"{len(enrichment['data_flows'])} flows")
            if enrichment["constraints"]: parts.append(f"{len(enrichment['constraints'])} constraints")
            click.echo(f"  {', '.join(parts) or 'empty'}")
        click.echo()

    # Timestamp (computed here, NEVER in a template) and blast-radius map
    # (reverse-BFS over called_by) threaded into every PageContext.
    page_timestamp = datetime.now(timezone.utc).isoformat()
    radius_map = build_blast_radius_map(all_nodes)

    for group_label, nodes in group_nodes.items():
        enrichment = page_enrichments.get(group_label, {})
        ctx = PageContext(
            group_label=group_label,
            files=list({n.file for n in nodes}),
            nodes=nodes,
            descriptions=descriptions,
            file_descriptions=file_descriptions,
            narrative=enrichment.get("narrative", ""),
            data_flows=enrichment.get("data_flows", []),
            constraints=enrichment.get("constraints", []),
            timestamp=page_timestamp,
            blast_radius_map=radius_map,
            deep=not skip_deep,
        )
        content = build_page(ctx)
        page_path = write_page(wiki_dir, group_label, content)
        entry_points = [n.id.split("::")[-1] for n in nodes if not n.called_by]
        index_entries.append(IndexEntry(
            path=str(page_path.relative_to(root)),
            covers=", ".join(sorted({n.file for n in nodes})),
            entry_points=entry_points,
        ))
        click.echo(f"    ✓  {page_path.relative_to(root)}  ({len(nodes)} symbols)")

    return descriptions, file_descriptions, all_nodes, page_enrichments, groups, index_entries


def _finalise_index_and_skill(
    root: Path,
    cfg: Config,
    index_entries: list,
    page_enrichments: dict,
    total_symbols: int,
    total_files: int,
    skip_deep: bool,
    all_nodes: list | None = None,
) -> None:
    """Build wiki/INDEX.md and .indexer/skills/codebase.md. Always runs at the end.

    `all_nodes` (when available) is used to compute the INDEX "Core abstractions"
    list (god nodes). Smart-mode repair may not have the full node set, in which
    case the section is simply omitted.
    """
    wiki_dir = root / cfg.wiki_dir
    commit = current_commit(root) or "unknown"
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Core abstractions for INDEX — top-N highest-degree symbols.
    top_god_nodes = god_nodes(all_nodes, 8) if all_nodes else []
    # Ranked, token-budgeted repo-map spine (PageRank over the call graph).
    repo_map_text = repo_map(all_nodes, max_tokens=cfg.map_tokens) if all_nodes else ""

    index_overview = ""
    index_flows: list[str] = []
    if not skip_deep:
        click.echo("\n  Deep enrichment  (INDEX overview)  ...", nl=False)
        skill_pages_for_deep = [
            {"label": e.path.split("/")[-1].replace(".md", ""), "covers": e.covers, "entry_points": e.entry_points}
            for e in index_entries
        ]
        idx_enrichment = deep_enrich_index(skill_pages_for_deep, cfg)
        index_overview = idx_enrichment.get("overview", "")
        index_flows = idx_enrichment.get("flows", [])
        click.echo(f"  {'overview + ' + str(len(index_flows)) + ' flows' if index_overview else 'empty'}\n")

    index_content = build_index(index_entries, commit, today, overview=index_overview, flows=index_flows, god_nodes=top_god_nodes, repo_map=repo_map_text)
    write_index(wiki_dir, index_content)
    click.echo(f"    ✓  {cfg.wiki_dir}/INDEX.md")

    from jinja2 import Environment, FileSystemLoader
    skill_dir = root / ".indexer" / "skills"
    skill_dir.mkdir(parents=True, exist_ok=True)
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), trim_blocks=True, lstrip_blocks=True)
    skill_pages = [
        {
            "label": e.path.split("/")[-1].replace(".md", ""),
            "path": e.path,
            "covers": e.covers,
            "entry_points": e.entry_points[:5],
            "enrichment": page_enrichments.get(e.path.split("/")[-1].replace(".md", ""), {}),
        }
        for e in index_entries
    ]
    skill_content = env.get_template("skill.md.j2").render(
        wiki_dir=cfg.wiki_dir,
        pages=skill_pages,
        overview=index_overview,
        key_flows=index_flows,
        total_symbols=total_symbols,
        total_files=total_files,
        commit=commit,
        indexed_date=today,
        repo_map=repo_map_text,
    )
    (skill_dir / "codebase.md").write_text(skill_content)
    click.echo(f"    ✓  .indexer/skills/codebase.md")


def _index_and_persist(
    root: Path,
    cfg: Config,
    manifest,
    candidates: list[str],
    skip_deep: bool,
    mode: str = "full re-index",
    staged: bool = False,
) -> None:
    """
    Run the full index pipeline on ``candidates`` and persist all generated
    artifacts: wiki pages, INDEX, skill, and manifest.

    Shared by ``run`` (full/incremental/forced) and ``--smart``'s
    no-manifest / fresh-repo fill path so both produce identical output.
    """
    click.echo(f"\n  kiwiskil  —  {mode}  —  {len(candidates)} file(s)\n")

    result = _index_files(root, cfg, candidates, skip_deep)
    descriptions, file_descriptions, all_nodes, page_enrichments, groups, index_entries = result

    if not all_nodes:
        return

    total_symbols = len(all_nodes)
    _finalise_index_and_skill(
        root, cfg, index_entries, page_enrichments, total_symbols, len(candidates), skip_deep,
        all_nodes=all_nodes,
    )

    # ── Update manifest ────────────────────────────────────────────────────────
    now = datetime.now(timezone.utc).isoformat()
    commit = current_commit(root) or "unknown"
    for rel_path in candidates:
        abs_path = root / rel_path
        if abs_path.exists():
            file_hash = compute_hash(abs_path)
            group = groups.get(rel_path, rel_path)
            manifest.files[rel_path] = file_entry_for(
                file_hash,
                page_relpath(cfg.wiki_dir, group),
                [n for n in all_nodes if n.file == rel_path],
            )
    manifest.last_indexed_commit = commit
    manifest.indexed_at = now

    if is_git_repo(root):
        tracked = set(all_tracked_files(root))
        stale_keys = [k for k in manifest.files if k not in tracked]
        for k in stale_keys:
            del manifest.files[k]

    save_manifest(root, manifest)

    # ── Auto-stage ALL generated files (pre-commit hook) ──────────────────────
    # Must happen before commit message synthesis so output is clean,
    # and before git finalises the commit object.
    if staged and is_git_repo(root):
        subprocess.run(
            ["git", "add",
             cfg.wiki_dir,
             ".indexer/manifest.json",
             ".indexer/skills/codebase.md",
             ".gitignore"],
            cwd=root,
        )
        click.echo(f"\n  Staged wiki + manifest + skill file")

    # ── Commit message synthesis ───────────────────────────────────────────────
    if cfg.synthesize_commit_message and staged:
        click.echo("  Synthesizing commit message  ...", nl=False)
        msg = synthesize_commit_message(candidates, descriptions, cfg)
        if msg:
            click.echo(f"\n\n  Suggested commit message:\n    {msg}\n")
        else:
            click.echo("  (skipped)\n")

    click.echo(f"\n  Done  —  {len(index_entries)} wiki page(s)  —  {total_symbols} symbols indexed\n")


def _run_smart(root: Path, cfg: Config, manifest, dry_run: bool, skip_deep: bool) -> None:
    from indexer import verify as verify_mod
    from indexer import repair as repair_mod

    report = verify_mod.scan(root, cfg, manifest, skip_deep=skip_deep)
    verify_mod.print_report(report)

    # ── No manifest yet: FILL (full initial index) instead of bailing. ─────────
    # A fresh / never-indexed repo is drift too. If there are indexable tracked
    # source files, --smart builds the whole index from scratch (like a full
    # `run`). Only bail when there is genuinely nothing to index.
    if report.manifest_missing:
        candidates = [f for f in all_tracked_files(root) if _is_indexable(f, cfg)]
        if not candidates:
            click.echo("\n  Nothing to index — no indexable source files found.")
            raise click.exceptions.Exit(1)

        if dry_run:
            click.echo(
                f"\n  Would do a full initial index of {len(candidates)} file(s)."
            )
            click.echo("  Dry run — no changes made.")
            # Drift present (nothing indexed yet) -> non-zero for the CI gate.
            raise click.exceptions.Exit(1)

        _ensure_cache_gitignore(root)
        _index_and_persist(
            root, cfg, manifest, candidates, skip_deep, mode="full initial index",
        )
        return

    if report.is_clean():
        return

    if dry_run:
        click.echo("\n  Dry run — no changes made.")
        # Drift present -> non-zero exit so CI can gate on `--smart --dry-run`.
        raise click.exceptions.Exit(1)

    plan_obj = repair_mod.plan(report, root, cfg, manifest, skip_deep=skip_deep)
    if not plan_obj.has_work():
        return

    repair_mod.execute(plan_obj, root, cfg, manifest, skip_deep=skip_deep)
    click.echo(f"\n  Done  —  {report.total_issues()} issue(s) resolved\n")
