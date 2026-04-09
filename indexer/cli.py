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
from indexer.llm import describe_nodes, synthesize_commit_message
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
def run(staged: bool, force: bool):
    """Index the codebase and generate wiki pages."""
    root = Path.cwd()
    cfg = load_config(root)
    manifest = load_manifest(root)

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
        click.echo("Nothing to index.")
        return

    click.echo(f"Indexing {len(candidates)} file(s)...")

    # Parse AST (use cache for unchanged files, fresh parse for changed)
    all_nodes = []
    for rel_path in candidates:
        abs_path = root / rel_path
        file_hash = compute_hash_short(abs_path)
        cached = load_cached_nodes(root, file_hash)
        if cached is not None:
            all_nodes.extend(cached)
        else:
            nodes = parse_file(abs_path, root)
            save_cached_nodes(root, file_hash, nodes)
            all_nodes.extend(nodes)

    if not all_nodes:
        click.echo("No symbols found.")
        return

    # Cross-reference pass: populate called_by from calls graph
    # Note: calls stores bare function/method names (e.g. "sign_payload"), not full component IDs.
    # This is best-effort: correctly links calls within the same codebase batch.
    call_index: dict[str, list[str]] = {}
    for node in all_nodes:
        for callee_name in node.calls:
            call_index.setdefault(callee_name, []).append(node.id)
    for node in all_nodes:
        # Match by bare name (last part of component ID after "::")
        bare_name = node.id.split("::")[-1]
        node.called_by = call_index.get(bare_name, [])

    # LLM: describe nodes in batches by token budget
    descriptions: dict[str, str] = {}
    batch, batch_size = [], 0
    for node in all_nodes:
        node_size = len(node.docstring or "") + len(" ".join(node.calls)) + 50
        if batch_size + node_size > cfg.max_tokens_per_batch and batch:
            descriptions.update(describe_nodes(batch, cfg))
            batch, batch_size = [], 0
        batch.append(node)
        batch_size += node_size
    if batch:
        descriptions.update(describe_nodes(batch, cfg))

    # Group files → wiki page labels
    groups = density_group(candidates)
    group_nodes: dict[str, list] = {}
    for node in all_nodes:
        group = groups.get(node.file, node.file)
        group_nodes.setdefault(group, []).append(node)

    # Write wiki pages
    wiki_dir = root / cfg.wiki_dir
    index_entries = []
    for group_label, nodes in group_nodes.items():
        ctx = PageContext(
            group_label=group_label,
            files=list({n.file for n in nodes}),
            nodes=nodes,
            descriptions=descriptions,
        )
        content = build_page(ctx)
        page_path = write_page(wiki_dir, group_label, content)
        entry_points = [n.id.split("::")[-1] for n in nodes if not n.called_by]
        index_entries.append(IndexEntry(
            path=str(page_path.relative_to(root)),
            covers=", ".join(sorted({n.file for n in nodes})),
            entry_points=entry_points,
        ))

    # Write INDEX.md
    commit = current_commit(root) or "unknown"
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    index_content = build_index(index_entries, commit, today)
    write_index(wiki_dir, index_content)

    # Write skill file
    from jinja2 import Environment, FileSystemLoader
    skill_dir = root / ".indexer" / "skills"
    skill_dir.mkdir(parents=True, exist_ok=True)
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), trim_blocks=True, lstrip_blocks=True)
    skill_content = env.get_template("skill.md.j2").render(wiki_dir=cfg.wiki_dir)
    (skill_dir / "codebase.md").write_text(skill_content)

    # Update manifest
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

    # Prune manifest entries for files no longer tracked by git
    if is_git_repo(root):
        tracked = set(all_tracked_files(root))
        stale_keys = [k for k in manifest.files if k not in tracked]
        for k in stale_keys:
            del manifest.files[k]

    save_manifest(root, manifest)

    # Synthesize commit message
    if cfg.synthesize_commit_message and staged:
        msg = synthesize_commit_message(candidates, descriptions, cfg)
        if msg:
            click.echo(f"\nSuggested commit message:\n  {msg}")

    # Auto-stage wiki + manifest when running as pre-commit hook
    if staged and is_git_repo(root):
        subprocess.run(["git", "add", cfg.wiki_dir, ".indexer/manifest.json"], cwd=root)

    click.echo(f"Done. Wiki written to {wiki_dir}/")


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
