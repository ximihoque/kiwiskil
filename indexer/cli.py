# indexer/cli.py
from __future__ import annotations
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import click

from indexer.config import Config, load_config, save_config
from indexer.manifest import load_manifest, save_manifest, compute_hash, FileEntry
from indexer.git import (
    staged_files, all_tracked_files, current_commit,
    changed_files_since, is_git_repo
)
from indexer.ast_parser import parse_file, load_cached_nodes, save_cached_nodes, compute_hash_short
from indexer.llm import describe_nodes, describe_files, deep_enrich_page, deep_enrich_index, synthesize_commit_message
from indexer.grouper import density_group
from indexer.wiki import build_page, build_index, write_page, write_index, PageContext, IndexEntry, TEMPLATES_DIR
from indexer.hooks import install_hook, remove_hook

CLAUDEMD_SNIPPET = """
## Codebase Navigation

This repo is indexed. Before reading source files:
- Load `wiki/INDEX.md` for the full structure map
- Use `.indexer/skills/codebase.md` as a skill for structured lookup tools
- Wiki pages are in `wiki/` — grouped by logical density, not mirroring directory structure exactly
- Component IDs follow `file::Class.method` format throughout
"""


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
        install_hook(root)
        click.echo("Installed pre-commit hook.")

    claude_md = root / "CLAUDE.md"
    if claude_md.exists():
        existing = claude_md.read_text()
        if "Codebase Navigation" not in existing:
            claude_md.write_text(existing + "\n" + CLAUDEMD_SNIPPET)
            click.echo("Appended to CLAUDE.md.")
    else:
        claude_md.write_text(CLAUDEMD_SNIPPET.lstrip())
        click.echo("Created CLAUDE.md.")


@main.command()
@click.option("--staged", is_flag=True, help="Incremental: only staged files (used by hook)")
@click.option("--force", is_flag=True, help="Force full re-index regardless of manifest")
@click.option("--deep", is_flag=True, help="Generate narrative, data flows, and design constraints (slower, more tokens)")
def run(staged: bool, force: bool, deep: bool):
    """Index the codebase and generate wiki pages."""
    root = Path.cwd()
    cfg = load_config(root)
    manifest = load_manifest(root)

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
    click.echo(f"\n  kiwiskil  —  {mode}  —  {len(candidates)} file(s)\n")

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
        return

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

    # ── Phase 5a: Deep enrichment per page (--deep only) ─────────────────────
    page_enrichments: dict[str, dict] = {}
    if deep:
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

    # ── Phase 6: INDEX + skill ────────────────────────────────────────────────
    commit = current_commit(root) or "unknown"
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    index_overview = ""
    index_flows: list[str] = []
    if deep:
        click.echo("\n  Deep enrichment  (INDEX overview)  ...", nl=False)
        skill_pages_for_deep = [
            {"label": e.path.split("/")[-1].replace(".md", ""), "covers": e.covers, "entry_points": e.entry_points}
            for e in index_entries
        ]
        idx_enrichment = deep_enrich_index(skill_pages_for_deep, cfg)
        index_overview = idx_enrichment.get("overview", "")
        index_flows = idx_enrichment.get("flows", [])
        click.echo(f"  {'overview + ' + str(len(index_flows)) + ' flows' if index_overview else 'empty'}\n")

    index_content = build_index(index_entries, commit, today, overview=index_overview, flows=index_flows)
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
        total_files=len(candidates),
        commit=commit,
        indexed_date=today,
    )
    (skill_dir / "codebase.md").write_text(skill_content)
    click.echo(f"    ✓  .indexer/skills/codebase.md")

    # ── Update manifest ────────────────────────────────────────────────────────
    now = datetime.now(timezone.utc).isoformat()
    for rel_path in candidates:
        abs_path = root / rel_path
        if abs_path.exists():
            file_hash = compute_hash(abs_path)
            group = groups.get(rel_path, rel_path)
            manifest.files[rel_path] = FileEntry(
                hash=file_hash,
                wiki_page=f"{cfg.wiki_dir}/{group}.md",
                component_ids=[n.id for n in all_nodes if n.file == rel_path],
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
    install_hook(root)
    click.echo("Pre-commit hook installed.")


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
    from fnmatch import fnmatch
    p = Path(path)
    if p.suffix not in {".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rb", ".rs"}:
        return False
    for pattern in cfg.ignore:
        if any(fnmatch(part, pattern) for part in p.parts):
            return False
        if fnmatch(path, pattern):
            return False
    return True
