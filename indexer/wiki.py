# indexer/wiki.py
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = Path(__file__).parent / "templates"

# OKF (Open Knowledge Format) constants.
# A bundle = a directory of markdown files, each with YAML frontmatter. The only
# required frontmatter field is `type` (a producer-defined string). OKF defines
# no code types — "Code Group" is ours.
OKF_VERSION = "0.1"
PAGE_TYPE = "Code Group"

# How many entries to show before truncating a relationships list.
RELATIONSHIPS_CAP = 8


@dataclass
class PageContext:
    group_label: str
    files: list[str]
    nodes: list  # list[ASTNode]
    descriptions: dict[str, str]
    file_descriptions: dict[str, str] = field(default_factory=dict)
    # deep enrichment fields (populated only with --deep)
    narrative: str = ""
    data_flows: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    # Slice C — OKF frontmatter. timestamp is an ISO-8601 string computed by the
    # caller (cli.py); NEVER call datetime in a template or here at render time.
    timestamp: str = ""
    # Slice B — precomputed blast-radius map: {symbol_id: set[affected_ids]}.
    blast_radius_map: dict[str, set] = field(default_factory=dict)
    # True when deep enrichment ran for this page (regardless of whether the LLM
    # returned a non-empty narrative). Drives an always-present deep marker so
    # verify can distinguish "deep ran, narrative empty" from "deep never ran"
    # and not loop forever flagging the page as missing deep sections.
    deep: bool = False


@dataclass
class IndexEntry:
    path: str
    covers: str
    entry_points: list[str]
    # deep enrichment fields (populated only with --deep)
    overview: str = ""
    flows: list[str] = field(default_factory=list)


def _jinja_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def _first_sentence(text: str) -> str:
    """First sentence of `text` (up to and including the first period)."""
    text = text.strip()
    if not text:
        return ""
    idx = text.find(". ")
    if idx != -1:
        return text[: idx + 1]
    # single sentence, possibly ending in a period
    return text if text.endswith(".") else text + "."


def _tags_from_path(group_label: str) -> list[str]:
    """Derive frontmatter tags from a group path's segments.

    'api/auth' -> ['api', 'auth']; strips a trailing slash and empty parts.
    """
    parts = [p for p in group_label.strip("/").split("/") if p and p != "."]
    # de-dup preserving order
    seen, tags = set(), []
    for p in parts:
        if p not in seen:
            seen.add(p)
            tags.append(p)
    return tags or [group_label] if group_label else []


def _short(node_id: str) -> str:
    """Component id -> short, page-local symbol label."""
    return node_id.split("::")[-1]


def _capped(items: list[str], cap: int = RELATIONSHIPS_CAP) -> tuple[list[str], int]:
    """Return (first `cap` items, count of remaining)."""
    if len(items) <= cap:
        return items, 0
    return items[:cap], len(items) - cap


def _symbol_relationships(ctx: PageContext) -> list[dict]:
    """Build the per-symbol inline relationships block for the page.

    For each node we render: callers (from `called_by`), calls (bare names), and
    the blast radius ("editing this affects:"). Lists are capped and labelled
    with their *full* count so the page is honest about truncation.
    """
    blocks = []
    for n in ctx.nodes:
        callers = sorted({_short(c) for c in n.called_by})
        calls = sorted(set(n.calls))
        affected = sorted({_short(a) for a in ctx.blast_radius_map.get(n.id, set())})

        callers_shown, callers_more = _capped(callers)
        calls_shown, calls_more = _capped(calls)
        affected_shown, affected_more = _capped(affected)

        # Skip symbols with nothing to say.
        if not (callers or calls or affected):
            continue

        blocks.append({
            "symbol": _short(n.id),
            "callers_count": len(callers),
            "callers_shown": callers_shown,
            "callers_more": callers_more,
            "calls_shown": calls_shown,
            "calls_more": calls_more,
            "affected_shown": affected_shown,
            "affected_more": affected_more,
        })
    return blocks


def build_page(ctx: PageContext) -> str:
    env = _jinja_env()
    tmpl = env.get_template("page.md.j2")

    # modules dict: file -> LLM-generated purpose
    modules = {f: ctx.file_descriptions.get(f, "") for f in ctx.files}

    # Aggregate relationships across all nodes in this page
    all_calls = sorted({c for n in ctx.nodes for c in n.calls})
    all_called_by = sorted({c for n in ctx.nodes for c in n.called_by})
    all_imports = sorted({i for n in ctx.nodes for i in n.imports})

    # Entry points: only classes and top-level functions not called by anything in this page
    # Exclude private helpers (starting with _)
    entry_points = [
        n.id.split("::")[-1]
        for n in ctx.nodes
        if n.type in ("class", "function")
        and not n.called_by
        and not n.id.split("::")[-1].startswith("_")
    ]

    # ── OKF frontmatter (Slice C) ─────────────────────────────────────────────
    description = _first_sentence(ctx.narrative) if ctx.narrative else (
        f"Code group covering {', '.join(ctx.files)}." if ctx.files
        else f"Code group: {ctx.group_label}."
    )
    frontmatter = {
        "type": PAGE_TYPE,
        "title": ctx.group_label,
        "description": description,
        "tags": _tags_from_path(ctx.group_label),
        "timestamp": ctx.timestamp,
        "resource": ctx.group_label,
    }

    # ── Inline relationships / blast radius (Slice B) ─────────────────────────
    relationships = _symbol_relationships(ctx)

    return tmpl.render(
        frontmatter=_yaml_frontmatter(frontmatter),
        group_label=ctx.group_label,
        modules=modules,
        nodes=ctx.nodes,
        descriptions=ctx.descriptions,
        all_calls=all_calls,
        all_called_by=all_called_by,
        all_imports=all_imports,
        entry_points=entry_points,
        narrative=ctx.narrative,
        data_flows=ctx.data_flows,
        constraints=ctx.constraints,
        relationships=relationships,
        deep=ctx.deep,
    )


def _yaml_frontmatter(data: dict) -> str:
    """Serialize a dict to a YAML frontmatter body (no delimiters).

    Uses PyYAML for correct escaping/quoting; templates only emit the `---`
    delimiters around this string. Keys keep insertion order.
    """
    import yaml
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, default_flow_style=False).rstrip()


def build_index(
    entries: list[IndexEntry],
    last_commit: str,
    indexed_date: str,
    overview: str = "",
    flows: list[str] = [],
    god_nodes: list[tuple[str, int]] = [],
    repo_map: str = "",
) -> str:
    env = _jinja_env()
    tmpl = env.get_template("index.md.j2")
    frontmatter = _yaml_frontmatter({
        "type": "Code Index",
        "okf_version": OKF_VERSION,
        "title": "Codebase Index",
    })
    # Render god_nodes as (short_label, full_id, degree) for the template.
    core_abstractions = [(_short(gid), gid, deg) for gid, deg in god_nodes]
    return tmpl.render(
        frontmatter=frontmatter,
        pages=entries,
        last_commit=last_commit,
        indexed_date=indexed_date,
        overview=overview,
        flows=flows,
        core_abstractions=core_abstractions,
        repo_map=repo_map,
    )


def page_basename(group_label: str) -> str:
    """The sanitised page filename stem for a group label.

    Single source of truth: "/" -> "_", strip leading/trailing "_"/".", and the
    root group "." -> "root". The manifest's `wiki_page` MUST be derived from
    this (not from the raw group label) or `--smart` will see a phantom
    missing-page (manifest path) + orphan-page (actual file) for any group whose
    label needs sanitising (root files, nested groups).
    """
    return group_label.replace("/", "_").strip("_").strip(".") or "root"


def page_relpath(wiki_dir: str, group_label: str) -> str:
    """Repo-relative wiki page path for a group, matching what write_page emits."""
    return f"{wiki_dir}/{page_basename(group_label)}.md"


def write_page(wiki_dir: Path, group_label: str, content: str) -> Path:
    page_path = wiki_dir / f"{page_basename(group_label)}.md"
    page_path.parent.mkdir(parents=True, exist_ok=True)
    page_path.write_text(content)
    return page_path


def write_index(wiki_dir: Path, content: str) -> Path:
    wiki_dir.mkdir(parents=True, exist_ok=True)
    index_path = wiki_dir / "INDEX.md"
    index_path.write_text(content)
    return index_path
