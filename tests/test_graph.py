# tests/test_graph.py
"""Unit tests for indexer.graph — pure functions over list[ASTNode].

All synthetic ASTNodes; no LLM, no filesystem. The cross-reference convention
mirrors cli.py::_index_files: a node's `called_by` holds the *component ids* of
nodes that call it (matched by bare name), and `calls` holds bare callee names.
"""
from indexer.ast_parser import ASTNode
from indexer.graph import (
    callers_of,
    callees_of,
    blast_radius,
    god_nodes,
    build_blast_radius_map,
    pagerank,
    ranked_symbols,
    repo_map,
)


def _node(id, calls=None, called_by=None, type="function"):
    return ASTNode(
        id=id,
        type=type,
        file=id.split("::")[0],
        line_start=1,
        line_end=2,
        docstring=None,
        imports=[],
        calls=calls or [],
        called_by=called_by or [],
    )


# A simple chain: a -> b -> c  (a calls b, b calls c)
# called_by holds the *ids* of callers (as populated by the cross-ref pass).
def _chain_nodes():
    a = _node("m.py::a", calls=["b"], called_by=[])
    b = _node("m.py::b", calls=["c"], called_by=["m.py::a"])
    c = _node("m.py::c", calls=[], called_by=["m.py::b"])
    return [a, b, c]


def test_callers_of_returns_caller_ids():
    nodes = _chain_nodes()
    assert callers_of(nodes, "m.py::b") == ["m.py::a"]


def test_callers_of_empty_when_no_callers():
    nodes = _chain_nodes()
    assert callers_of(nodes, "m.py::a") == []


def test_callees_of_resolves_bare_names_to_ids():
    nodes = _chain_nodes()
    # b calls "c" (bare) -> resolves to m.py::c
    assert callees_of(nodes, "m.py::b") == ["m.py::c"]


def test_callees_of_skips_unresolvable_external_names():
    nodes = [_node("m.py::a", calls=["print", "b"]), _node("m.py::b")]
    # only "b" resolves to a known node; "print" is external -> dropped
    assert callees_of(nodes, "m.py::a") == ["m.py::b"]


def test_blast_radius_is_transitive_reverse_reachability():
    # editing c affects b (calls c) and a (calls b) transitively
    nodes = _chain_nodes()
    assert blast_radius(nodes, "m.py::c") == {"m.py::a", "m.py::b"}


def test_blast_radius_excludes_self():
    nodes = _chain_nodes()
    assert "m.py::c" not in blast_radius(nodes, "m.py::c")


def test_blast_radius_leaf_caller_is_empty():
    nodes = _chain_nodes()
    # nobody calls a -> editing a affects nobody upstream
    assert blast_radius(nodes, "m.py::a") == set()


def test_blast_radius_handles_cycles():
    # a <-> b cycle: a calls b, b calls a
    a = _node("m.py::a", calls=["b"], called_by=["m.py::b"])
    b = _node("m.py::b", calls=["a"], called_by=["m.py::a"])
    nodes = [a, b]
    # must terminate and exclude self
    assert blast_radius(nodes, "m.py::a") == {"m.py::b"}
    assert blast_radius(nodes, "m.py::b") == {"m.py::a"}


def test_blast_radius_diamond():
    #   a    b
    #    \  /
    #     c
    #     |
    #     d
    # d called_by c; c called_by a and b. editing d affects c, a, b.
    a = _node("m.py::a", calls=["c"], called_by=[])
    b = _node("m.py::b", calls=["c"], called_by=[])
    c = _node("m.py::c", calls=["d"], called_by=["m.py::a", "m.py::b"])
    d = _node("m.py::d", calls=[], called_by=["m.py::c"])
    nodes = [a, b, c, d]
    assert blast_radius(nodes, "m.py::d") == {"m.py::a", "m.py::b", "m.py::c"}


def test_blast_radius_unknown_symbol_is_empty():
    nodes = _chain_nodes()
    assert blast_radius(nodes, "m.py::does_not_exist") == set()


def test_god_nodes_ranks_by_degree():
    # hub is called by 3 and calls 2 -> degree 5; others lower
    hub = _node("m.py::hub", calls=["x", "y"], called_by=["m.py::p", "m.py::q", "m.py::r"])
    p = _node("m.py::p", calls=["hub"])
    q = _node("m.py::q", calls=["hub"])
    r = _node("m.py::r", calls=["hub"])
    x = _node("m.py::x", called_by=["m.py::hub"])
    y = _node("m.py::y", called_by=["m.py::hub"])
    nodes = [hub, p, q, r, x, y]
    top = god_nodes(nodes, 1)
    assert top[0][0] == "m.py::hub"
    assert top[0][1] == 5  # 3 callers + 2 callees


def test_god_nodes_respects_n():
    nodes = _chain_nodes()
    assert len(god_nodes(nodes, 2)) == 2


def test_god_nodes_empty_input():
    assert god_nodes([], 5) == []


def test_god_nodes_n_larger_than_nodes():
    nodes = _chain_nodes()
    assert len(god_nodes(nodes, 100)) == 3


def test_build_blast_radius_map_keys_every_node():
    nodes = _chain_nodes()
    m = build_blast_radius_map(nodes)
    assert set(m.keys()) == {"m.py::a", "m.py::b", "m.py::c"}
    assert m["m.py::c"] == {"m.py::a", "m.py::b"}
    assert m["m.py::a"] == set()


# ── PageRank ──────────────────────────────────────────────────────────────────

def test_pagerank_keys_every_node_and_sums_to_one():
    nodes = _chain_nodes()
    pr = pagerank(nodes)
    assert set(pr.keys()) == {"m.py::a", "m.py::b", "m.py::c"}
    assert abs(sum(pr.values()) - 1.0) < 1e-6


def test_pagerank_empty_input():
    assert pagerank([]) == {}


def test_pagerank_ranks_a_hub_above_leaves():
    # hub is called by three distinct symbols; leaves are called by none.
    hub = _node("m.py::hub", calls=[], called_by=["m.py::x", "m.py::y", "m.py::z"])
    x = _node("m.py::x", calls=["hub"], called_by=[])
    y = _node("m.py::y", calls=["hub"], called_by=[])
    z = _node("m.py::z", calls=["hub"], called_by=[])
    nodes = [hub, x, y, z]
    pr = pagerank(nodes)
    assert pr["m.py::hub"] > pr["m.py::x"]
    assert pr["m.py::hub"] > pr["m.py::y"]
    assert pr["m.py::hub"] > pr["m.py::z"]


def test_pagerank_is_deterministic():
    nodes = _chain_nodes()
    assert pagerank(nodes) == pagerank(nodes)


def test_pagerank_handles_cycles():
    # a -> b -> a  (mutual). Must converge, not loop forever.
    a = _node("m.py::a", calls=["b"], called_by=["m.py::b"])
    b = _node("m.py::b", calls=["a"], called_by=["m.py::a"])
    pr = pagerank([a, b])
    assert abs(sum(pr.values()) - 1.0) < 1e-6
    assert abs(pr["m.py::a"] - pr["m.py::b"]) < 1e-6  # symmetric


# ── ranked_symbols ────────────────────────────────────────────────────────────

def test_ranked_symbols_orders_by_pagerank_desc():
    hub = _node("m.py::hub", calls=[], called_by=["m.py::x", "m.py::y", "m.py::z"])
    x = _node("m.py::x", calls=["hub"], called_by=[])
    y = _node("m.py::y", calls=["hub"], called_by=[])
    z = _node("m.py::z", calls=["hub"], called_by=[])
    ranked = ranked_symbols([hub, x, y, z])
    assert ranked[0] == "m.py::hub"
    assert len(ranked) == 4


def test_ranked_symbols_empty():
    assert ranked_symbols([]) == []


# ── repo_map (token-budgeted) ─────────────────────────────────────────────────

def test_repo_map_returns_string():
    nodes = _chain_nodes()
    out = repo_map(nodes, max_tokens=1000)
    assert isinstance(out, str)
    assert "m.py::" in out


def test_repo_map_respects_token_budget():
    # Many nodes, tiny budget -> output must be small and not include everything.
    nodes = [_node(f"m.py::s{i}", calls=[], called_by=[]) for i in range(200)]
    out = repo_map(nodes, max_tokens=50)
    # rough token proxy: ~4 chars/token; allow generous slack but cap well below full
    assert len(out) <= 50 * 6
    assert out.count("\n") < 200  # didn't dump all 200


def test_repo_map_leads_with_highest_ranked():
    hub = _node("m.py::hub", calls=[], called_by=["m.py::x", "m.py::y", "m.py::z"])
    x = _node("m.py::x", calls=["hub"], called_by=[])
    y = _node("m.py::y", calls=["hub"], called_by=[])
    z = _node("m.py::z", calls=["hub"], called_by=[])
    out = repo_map([hub, x, y, z], max_tokens=1000)
    # hub should appear before the leaves in the rendered map
    assert out.index("hub") < out.index("m.py::x")


def test_repo_map_empty():
    assert repo_map([], max_tokens=1000) == ""


def test_repo_map_larger_budget_includes_more():
    nodes = [_node(f"m.py::s{i}", calls=[], called_by=[]) for i in range(100)]
    small = repo_map(nodes, max_tokens=30)
    large = repo_map(nodes, max_tokens=2000)
    assert len(large) > len(small)
