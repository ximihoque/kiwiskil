# indexer/graph.py
"""Pure, in-memory graph analysis over a list of ASTNodes.

NO serialization, NO graph.json, NO filesystem, NO LLM. Every function takes a
``list[ASTNode]`` and returns plain data structures.

Edge model — we use ONLY what ast_parser actually extracts:
  - ``node.calls``      : bare callee names this symbol invokes (e.g. "verify").
  - ``node.called_by``  : component *ids* of symbols that call this one, as
                          populated by the cross-reference pass in cli.py.
  - ``node.imports``    : module import strings (not used for the call graph).

There are NO inheritance edges (ast_parser does not extract them); do not add
``inherits``/``implements`` here.

"Blast radius" of a symbol = the set of symbols that transitively depend on it,
i.e. everything reachable by walking ``called_by`` edges in reverse-BFS.
"Editing this symbol affects these." Self is excluded; cycles are handled with a
visited set.
"""
from __future__ import annotations

from collections import deque


def _index_by_id(nodes: list) -> dict:
    """Map component id -> ASTNode. Last write wins on duplicate ids."""
    return {n.id: n for n in nodes}


def _bare_name(node_id: str) -> str:
    """Component id 'path.py::Class.method' -> bare callable name 'method'."""
    return node_id.split("::")[-1].split(".")[-1]


def callers_of(nodes: list, symbol_id: str) -> list[str]:
    """Direct callers of ``symbol_id`` as a sorted list of component ids.

    Reads ``called_by`` directly (already id-based from the cross-ref pass).
    Returns [] for unknown symbols.
    """
    by_id = _index_by_id(nodes)
    node = by_id.get(symbol_id)
    if node is None:
        return []
    return sorted(set(node.called_by))


def callees_of(nodes: list, symbol_id: str) -> list[str]:
    """Direct callees of ``symbol_id`` resolved to component ids, sorted.

    ``node.calls`` holds *bare* names; we resolve each to known component ids by
    matching the bare name. Unresolvable names (external/stdlib) are dropped. A
    bare name may resolve to several ids (overloaded names) — all are included.
    Self-references are excluded.
    """
    by_id = _index_by_id(nodes)
    node = by_id.get(symbol_id)
    if node is None:
        return []

    # bare name -> list of ids that expose it
    by_bare: dict[str, list[str]] = {}
    for n in nodes:
        by_bare.setdefault(_bare_name(n.id), []).append(n.id)

    resolved: set[str] = set()
    for call in node.calls:
        for candidate in by_bare.get(call, []):
            if candidate != symbol_id:
                resolved.add(candidate)
    return sorted(resolved)


def blast_radius(nodes: list, symbol_id: str) -> set[str]:
    """Transitive reverse-reachability over ``called_by`` (the blast radius).

    Returns the set of component ids that transitively depend on ``symbol_id``
    ("editing this affects these"). Excludes ``symbol_id`` itself. Safe on
    cycles (visited set) and on unknown symbols (returns empty set).
    """
    by_id = _index_by_id(nodes)
    if symbol_id not in by_id:
        return set()

    affected: set[str] = set()
    queue: deque[str] = deque([symbol_id])
    visited: set[str] = {symbol_id}

    while queue:
        current = queue.popleft()
        node = by_id.get(current)
        if node is None:
            continue
        for caller_id in node.called_by:
            if caller_id in visited:
                continue
            visited.add(caller_id)
            affected.add(caller_id)
            queue.append(caller_id)

    affected.discard(symbol_id)
    return affected


def build_blast_radius_map(nodes: list) -> dict[str, set[str]]:
    """Precompute ``{symbol_id: blast_radius(symbol_id)}`` for every node.

    Convenience for callers that render a block per page without recomputing the
    BFS each time.
    """
    return {n.id: blast_radius(nodes, n.id) for n in nodes}


def god_nodes(nodes: list, n: int) -> list[tuple[str, int]]:
    """Top-``n`` highest-degree symbols as ``(component_id, degree)`` pairs.

    Degree = number of distinct direct callers + number of distinct resolved
    direct callees. Sorted by degree descending, then by id for stability.
    Returns at most ``min(n, len(nodes))`` pairs.
    """
    if n <= 0:
        return []

    scored: list[tuple[str, int]] = []
    for node in nodes:
        callers = len(set(node.called_by))
        callees = len(callees_of(nodes, node.id))
        scored.append((node.id, callers + callees))

    scored.sort(key=lambda pair: (-pair[1], pair[0]))
    return scored[:n]


# ── PageRank importance + token-budgeted repo map ─────────────────────────────
#
# Aider's "repo map" insight: rank symbols by importance over the call graph
# (PageRank), then fit the most important ones into a token budget. We do a
# pure-Python power-iteration PageRank (no networkx dependency, preserving the
# no-heavy-deps promise) over the directed call graph.
#
# Edge direction for PageRank: caller -> callee. A symbol gains rank from the
# symbols that call it, so heavily-called "load-bearing" code floats to the top.
# We derive caller->callee edges from each node's `called_by` (id-based, exact).

_PR_DAMPING = 0.85
_PR_MAX_ITER = 100
_PR_TOL = 1e-9


def _adjacency(nodes: list) -> dict[str, list[str]]:
    """Directed caller -> callee adjacency over known component ids only.

    Built from `called_by` (exact ids): for each node C and each caller P in
    C.called_by, add edge P -> C. External/unknown callers are ignored.
    """
    ids = {n.id for n in nodes}
    out: dict[str, list[str]] = {nid: [] for nid in ids}
    for node in nodes:
        for caller_id in node.called_by:
            if caller_id in ids:
                out[caller_id].append(node.id)
    # de-dup callees per caller for stable, weight-1 edges
    return {src: sorted(set(dsts)) for src, dsts in out.items()}


def pagerank(nodes: list, damping: float = _PR_DAMPING) -> dict[str, float]:
    """PageRank score per component id; scores sum to 1.0.

    Pure-Python power iteration over the caller->callee graph. Deterministic
    (fixed init + iteration order), cycle-safe, and dangling-node-safe (a node
    with no out-edges redistributes its mass uniformly). Returns {} for [].
    """
    ids = [n.id for n in nodes]
    N = len(ids)
    if N == 0:
        return {}

    adj = _adjacency(nodes)
    rank = {nid: 1.0 / N for nid in ids}
    base = (1.0 - damping) / N

    for _ in range(_PR_MAX_ITER):
        # mass from dangling nodes (no out-edges) is spread to everyone
        dangling = sum(rank[nid] for nid in ids if not adj.get(nid))
        new = {nid: base + damping * dangling / N for nid in ids}
        for src in ids:
            dsts = adj.get(src) or []
            if not dsts:
                continue
            share = damping * rank[src] / len(dsts)
            for dst in dsts:
                new[dst] += share
        delta = sum(abs(new[nid] - rank[nid]) for nid in ids)
        rank = new
        if delta < _PR_TOL:
            break

    # normalise (guards against tiny float drift)
    total = sum(rank.values()) or 1.0
    return {nid: rank[nid] / total for nid in ids}


def ranked_symbols(nodes: list) -> list[str]:
    """Component ids ordered by PageRank descending (ties broken by id)."""
    pr = pagerank(nodes)
    return sorted(pr, key=lambda nid: (-pr[nid], nid))


def _approx_tokens(text: str) -> int:
    """Cheap token proxy: ~4 chars per token. Avoids a tokenizer dependency."""
    return max(1, len(text) // 4)


def repo_map(nodes: list, max_tokens: int = 1024) -> str:
    """A token-budgeted, importance-ranked spine of the codebase.

    Renders the highest-PageRank symbols (one per line, grouped by file) until
    the approximate token budget is exhausted. This is the compact "where the
    load-bearing code lives" view an agent reads first. Returns "" for [].

    The line format is intentionally terse: ``- <component_id>  (callers: N)``.
    """
    if not nodes:
        return ""

    by_id = _index_by_id(nodes)
    order = ranked_symbols(nodes)

    lines: list[str] = []
    used = 0
    for nid in order:
        node = by_id.get(nid)
        n_callers = len(set(node.called_by)) if node else 0
        line = f"- {nid}  (callers: {n_callers})"
        cost = _approx_tokens(line + "\n")
        if used + cost > max_tokens and lines:
            break
        lines.append(line)
        used += cost

    return "\n".join(lines)
