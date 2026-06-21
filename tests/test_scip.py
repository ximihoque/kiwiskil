# tests/test_scip.py
"""SCIP symbol-descriptor derivation from kiwiskil component IDs.

We derive a SCIP-style symbol string from the existing `path::Class.method` id
(additive — the primary id is unchanged). The SCIP descriptor grammar we target
(local scheme, no package coordinates we can't know):
  - namespace/file component:  <path>/
  - type (class):              <Name>#
  - method:                    <Class>#<method>().
  - top-level function:        <name>().
See https://github.com/sourcegraph/scip — descriptor suffixes:
  `/` namespace, `#` type, `.` term, `().` method.
"""
from indexer.ast_parser import ASTNode
from indexer.scip import scip_symbol


def _node(id, type):
    return ASTNode(
        id=id, type=type, file=id.split("::")[0],
        line_start=1, line_end=2, docstring=None,
    )


def test_top_level_function():
    n = _node("pkg/mod.py::do_thing", "function")
    assert scip_symbol(n) == "pkg/mod.py/ do_thing()."


def test_class():
    n = _node("pkg/mod.py::Widget", "class")
    assert scip_symbol(n) == "pkg/mod.py/ Widget#"


def test_method():
    n = _node("pkg/mod.py::Widget.bump", "method")
    assert scip_symbol(n) == "pkg/mod.py/ Widget#bump()."


def test_method_with_dotted_class_path_uses_last_segment_as_member():
    # Defensive: only the final ".member" is the method; everything before is the type.
    n = _node("a/b.py::Outer.Inner.run", "method")
    # Outer.Inner is the (nested) type; run is the method.
    assert scip_symbol(n) == "a/b.py/ Outer.Inner#run()."


def test_root_level_file():
    n = _node("main.py::main", "function")
    assert scip_symbol(n) == "main.py/ main()."


def test_is_deterministic():
    n = _node("pkg/mod.py::Widget.bump", "method")
    assert scip_symbol(n) == scip_symbol(n)


def test_unknown_type_falls_back_to_term():
    n = _node("pkg/mod.py::thing", "variable")
    # Unknown/other types -> treat as a plain term (`.` suffix), never crash.
    assert scip_symbol(n) == "pkg/mod.py/ thing."


def test_malformed_id_without_separator_is_safe():
    n = _node("weird_id_no_sep", "function")
    # No "::" -> we still produce *something* deterministic, never raise.
    assert scip_symbol(n)  # non-empty, no exception
