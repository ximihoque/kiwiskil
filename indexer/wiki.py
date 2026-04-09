# indexer/wiki.py
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = Path(__file__).parent / "templates"


@dataclass
class PageContext:
    group_label: str
    files: list[str]
    nodes: list  # list[ASTNode]
    descriptions: dict[str, str]


@dataclass
class IndexEntry:
    path: str
    covers: str
    entry_points: list[str]


def _jinja_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def build_page(ctx: PageContext) -> str:
    env = _jinja_env()
    tmpl = env.get_template("page.md.j2")

    # modules dict: file -> empty string (descriptions come from LLM per symbol, not per file)
    modules = {f: "" for f in ctx.files}

    # Aggregate relationships across all nodes in this page
    all_calls = sorted({c for n in ctx.nodes for c in n.calls})
    all_called_by = sorted({c for n in ctx.nodes for c in n.called_by})
    all_imports = sorted({i for n in ctx.nodes for i in n.imports})

    # Entry points: nodes that nothing calls (called_by is empty)
    entry_points = [n.id.split("::")[-1] for n in ctx.nodes if not n.called_by]

    return tmpl.render(
        group_label=ctx.group_label,
        modules=modules,
        nodes=ctx.nodes,
        descriptions=ctx.descriptions,
        all_calls=all_calls,
        all_called_by=all_called_by,
        all_imports=all_imports,
        entry_points=entry_points,
    )


def build_index(entries: list[IndexEntry], last_commit: str, indexed_date: str) -> str:
    env = _jinja_env()
    tmpl = env.get_template("index.md.j2")
    return tmpl.render(pages=entries, last_commit=last_commit, indexed_date=indexed_date)


def write_page(wiki_dir: Path, group_label: str, content: str) -> Path:
    # Sanitise group_label for use as filename: replace "/" with "_"
    safe_name = group_label.replace("/", "_").strip("_") or "root"
    page_path = wiki_dir / f"{safe_name}.md"
    page_path.parent.mkdir(parents=True, exist_ok=True)
    page_path.write_text(content)
    return page_path


def write_index(wiki_dir: Path, content: str) -> Path:
    wiki_dir.mkdir(parents=True, exist_ok=True)
    index_path = wiki_dir / "INDEX.md"
    index_path.write_text(content)
    return index_path
