# indexer/scip.py
"""Derive SCIP-style symbol descriptors from kiwiskil component IDs.

This is ADDITIVE interop, not a replacement: kiwiskil's primary component id
stays `path::Class.method` (every downstream reader depends on it). `scip_symbol`
derives a human-readable SCIP descriptor string so the manifest can be made
SCIP-interoperable without changing the primary key.

We emit the descriptor portion of a SCIP symbol (no scheme/package coordinates —
those require a package manager + version we can't know for an arbitrary repo).
SCIP descriptor suffixes (https://github.com/sourcegraph/scip):
  `/` namespace · `#` type · `.` term · `().` method

Mapping from our component id `relpath::Owner.member`:
  - class:               `<relpath>/ <Name>#`
  - method:              `<relpath>/ <Owner>#<member>().`   (Owner = everything
                         before the final `.`; member = final segment)
  - top-level function:  `<relpath>/ <name>().`
  - anything else:       `<relpath>/ <name>.`               (plain term)

The function never raises; a malformed id still yields a deterministic string.
"""
from __future__ import annotations


def _split_id(component_id: str) -> tuple[str, str]:
    """(relpath, symbol_part) from `relpath::symbol`. Missing `::` -> ('', id)."""
    if "::" in component_id:
        relpath, symbol = component_id.split("::", 1)
        return relpath, symbol
    return "", component_id


def scip_symbol(node) -> str:
    """SCIP descriptor string for an ASTNode (see module docstring)."""
    relpath, symbol = _split_id(node.id)
    prefix = f"{relpath}/ " if relpath else ""
    ntype = getattr(node, "type", "")

    if ntype == "class":
        return f"{prefix}{symbol}#"

    if ntype == "method" and "." in symbol:
        owner, _, member = symbol.rpartition(".")
        return f"{prefix}{owner}#{member}()."

    if ntype in ("function", "method"):
        # method without a dotted owner is treated like a free function
        return f"{prefix}{symbol}()."

    # unknown/other kinds -> plain term
    return f"{prefix}{symbol}."
