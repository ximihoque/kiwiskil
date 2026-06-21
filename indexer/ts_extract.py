"""Generic, config-driven tree-sitter symbol extraction.

This is the single extraction path for languages whose grammars expose a
broadly similar shape (function/class/method declarations with a `name`
field). It produces exactly the same ``ASTNode`` shape as the dedicated
Python and JS/TS parsers:

    id          "relpath::Class.method" | "relpath::func"
    type        "class" | "function" | "method"
    file        repo-relative path
    line_start  1-based
    line_end    1-based
    docstring   leading doc-comment text, or None
    imports     file-level import strings
    calls       names of functions/methods called within the body
    called_by   always [] at parse time (filled later by cli.py)

A ``LangConfig`` maps a language's concrete tree-sitter node types onto these
needs. Adding a language is (mostly) a matter of adding a config entry in
``LANG_CONFIGS`` plus pointing ``parse_file`` at the grammar module.

Design notes / honest limitations:
- ``class_in_body`` controls whether methods are discovered by descending into
  a class's body (Java, Ruby) or whether the language places "methods" at the
  top level with a receiver (Go) — in which case they are emitted as standalone
  functions keyed by their own name (we cannot cheaply attribute a Go method to
  its receiver type without resolving the receiver, which is out of scope here).
- ``impl_node`` (Rust) lets methods declared inside an ``impl T {}`` block be
  attributed to type ``T`` even though they are syntactically free functions.
- Call extraction is best-effort: we collect identifiers used in call/invocation
  positions. It is intentionally permissive (may include a few false positives)
  rather than silent-zero.
"""
from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

from indexer.ast_parser import ASTNode

# Grammar modules that emitted a warning already (warn-once semantics).
_WARNED: set[str] = set()


@dataclass
class LangConfig:
    # Python module providing the grammar, e.g. "tree_sitter_go".
    grammar_module: str
    # Optional attribute on the module to call for the Language capsule.
    # Defaults to "language"; TS uses language_typescript / language_tsx.
    language_attr: str = "language"

    # Node types that declare a class-like symbol (struct/class/module/trait...).
    class_types: tuple[str, ...] = ()
    # Some grammars wrap the named type one level down (Go: type_declaration ->
    # type_spec). If set, when we see a key of this dict we descend to the child
    # node type (the value) before reading its name. e.g. {"type_declaration": "type_spec"}
    class_unwrap: dict[str, str] = field(default_factory=dict)

    # Node types that declare a free function.
    function_types: tuple[str, ...] = ()
    # Node types that declare a method (only meaningful when found inside a
    # class body / impl block).
    method_types: tuple[str, ...] = ()

    # If True, methods are found by descending into the class node's body and
    # are attributed to the enclosing class (Java, Ruby). If False, method_types
    # found at top level are emitted as standalone functions (Go).
    class_in_body: bool = True
    # Field name (or None) used to reach a class's body node. If None we just
    # iterate the class node's named children looking for method_types.
    body_field: Optional[str] = None

    # Rust-style: methods live inside `impl_item -> declaration_list`. The impl
    # node carries a type_identifier naming the type the methods belong to.
    impl_node: Optional[str] = None

    # Call extraction.
    call_types: tuple[str, ...] = ()           # e.g. ("call_expression",)
    call_function_field: Optional[str] = "function"  # field holding the callee
    # Node types whose text (last identifier segment) names the callee.
    callee_name_types: tuple[str, ...] = (
        "identifier", "field_identifier", "property_identifier",
    )

    # Imports.
    import_types: tuple[str, ...] = ()
    # Ruby has no import node; `require` shows up as a `call` to `require`.
    import_call_names: tuple[str, ...] = ()

    # Doc comments: comment node types and the prefix marking a doc comment.
    # If doc_prefix is None, any immediately-preceding comment counts.
    comment_types: tuple[str, ...] = ()
    doc_prefix: Optional[str] = None
    # If the comment node nests its text in a child of this type (Rust:
    # line_comment -> doc_comment), read that child's text instead.
    doc_text_child: Optional[str] = None


def _node_text(node, source: bytes) -> str:
    return source[node.start_byte:node.end_byte].decode("utf-8", errors="replace")


def _get_name(node, source: bytes) -> Optional[str]:
    name_node = node.child_by_field_name("name")
    if name_node is not None:
        return _node_text(name_node, source)
    return None


def _clean_comment(text: str, doc_prefix: Optional[str]) -> Optional[str]:
    """Strip comment markers and join into a single doc string."""
    text = text.strip()
    # Block comment /** ... */
    if text.startswith("/**") and text.endswith("*/"):
        inner = text[3:-2]
    elif text.startswith("/*") and text.endswith("*/"):
        inner = text[2:-2]
    else:
        # Line comments: strip leading // /// # markers per line.
        lines = []
        for raw in text.splitlines():
            line = raw.strip()
            for marker in ("///", "//", "#"):
                if line.startswith(marker):
                    line = line[len(marker):]
                    break
            lines.append(line.strip())
        inner = "\n".join(lines)
    cleaned = []
    for line in inner.splitlines():
        line = line.strip().lstrip("*").strip()
        if line:
            cleaned.append(line)
    return " ".join(cleaned) or None


def _doc_anchor(node):
    """The node whose preceding siblings carry the doc comment.

    Some grammars (Ruby) wrap a declaration in a ``body_statement`` whose own
    preceding sibling is the comment, so the declaration has no prev sibling of
    its own. In that case look one level up.
    """
    if node.prev_named_sibling is None and node.parent is not None \
            and node.parent.type == "body_statement":
        return node.parent
    return node


def _extract_doc(node, source: bytes, cfg: LangConfig) -> Optional[str]:
    """Collect contiguous doc-comment siblings immediately above ``node``."""
    if not cfg.comment_types:
        return None
    parts: list[str] = []
    prev = _doc_anchor(node).prev_named_sibling
    while prev is not None and prev.type in cfg.comment_types:
        raw = _node_text(prev, source)
        if cfg.doc_prefix is not None and not raw.strip().startswith(cfg.doc_prefix):
            break
        if cfg.doc_text_child:
            child = next(
                (c for c in prev.children if c.type == cfg.doc_text_child), None
            )
            text = _node_text(child, source) if child is not None else raw
        else:
            text = raw
        parts.append(text)
        prev = prev.prev_named_sibling

    if not parts:
        return None
    parts.reverse()
    joined = "\n".join(parts)
    return _clean_comment(joined, cfg.doc_prefix)


def _extract_imports(root, source: bytes, cfg: LangConfig) -> list[str]:
    imports: list[str] = []

    def visit(n):
        if n.type in cfg.import_types:
            imports.append(_node_text(n, source).split("\n")[0][:80])
        elif cfg.import_call_names and n.type == "call":
            head = n.named_children[0] if n.named_children else None
            if head is not None and _node_text(head, source) in cfg.import_call_names:
                imports.append(_node_text(n, source).split("\n")[0][:80])
        for child in n.children:
            visit(child)

    visit(root)
    return imports


def _last_identifier(node, source: bytes, cfg: LangConfig) -> Optional[str]:
    """Given a callee node, return the trailing identifier (the method/fn name)."""
    if node.type in cfg.callee_name_types:
        return _node_text(node, source)
    # scoped/member/selector expressions: take the last name-like named child.
    for child in reversed(node.named_children):
        if child.type in cfg.callee_name_types:
            return _node_text(child, source)
    # Fallback: last token of the dotted/scoped text.
    text = _node_text(node, source)
    for sep in ("::", "."):
        if sep in text:
            text = text.split(sep)[-1]
    text = text.strip()
    return text or None


def _extract_calls(node, source: bytes, cfg: LangConfig) -> list[str]:
    calls: set[str] = set()

    def visit(n):
        if n.type in cfg.call_types:
            callee = None
            if cfg.call_function_field:
                callee = n.child_by_field_name(cfg.call_function_field)
            if callee is None:
                # Ruby `call` node: method name is a child identifier.
                callee = n.named_children[0] if n.named_children else None
            if callee is not None:
                name = _last_identifier(callee, source, cfg)
                if name:
                    calls.add(name)
        for child in n.children:
            visit(child)

    visit(node)
    return list(calls)


def _load_language(cfg: LangConfig):
    """Import the grammar and build a tree_sitter.Language. Returns None and
    warns-once if the grammar package is not installed."""
    try:
        from tree_sitter import Language
    except ImportError as e:  # core tree-sitter missing
        if "tree_sitter_core" not in _WARNED:
            warnings.warn(f"tree-sitter not installed: {e}")
            _WARNED.add("tree_sitter_core")
        return None

    mod_name = cfg.grammar_module
    try:
        mod = __import__(mod_name)
    except ImportError as e:
        if mod_name not in _WARNED:
            warnings.warn(
                f"grammar '{mod_name}' not installed; skipping its files: {e}"
            )
            _WARNED.add(mod_name)
        return None

    try:
        lang_fn = getattr(mod, cfg.language_attr)
        return Language(lang_fn())
    except Exception as e:  # noqa: BLE001 - degrade, never crash the run
        if mod_name not in _WARNED:
            warnings.warn(f"failed to load grammar '{mod_name}': {e}")
            _WARNED.add(mod_name)
        return None


def _resolve_class_node(node, cfg: LangConfig):
    """Apply class_unwrap (e.g. Go type_declaration -> type_spec)."""
    if node.type in cfg.class_unwrap:
        target = cfg.class_unwrap[node.type]
        for child in node.named_children:
            if child.type == target:
                return child
        return None
    return node


def _emit_method(node, rel_path, source, cfg, class_name, nodes):
    name = _get_name(node, source)
    if not name:
        return
    body = node.child_by_field_name("body")
    calls = _extract_calls(body, source, cfg) if body else _extract_calls(node, source, cfg)
    nid = f"{rel_path}::{class_name}.{name}" if class_name else f"{rel_path}::{name}"
    nodes.append(ASTNode(
        id=nid,
        type="method" if class_name else "function",
        file=rel_path,
        line_start=node.start_point[0] + 1,
        line_end=node.end_point[0] + 1,
        docstring=_extract_doc(node, source, cfg),
        imports=[],  # filled by caller
        calls=calls,
    ))


def extract_generic(
    path: Path, repo_root: Path, cfg: LangConfig, rel: Callable[[Path, Path], str]
) -> list[ASTNode]:
    language = _load_language(cfg)
    if language is None:
        return []

    try:
        from tree_sitter import Parser
        source = path.read_bytes()
        parser = Parser(language)
        tree = parser.parse(source)
    except Exception as e:  # noqa: BLE001 - degrade, never crash the run
        warnings.warn(f"failed to parse {path}: {e}")
        return []

    rel_path = rel(path, repo_root)
    file_imports = _extract_imports(tree.root_node, source, cfg)
    nodes: list[ASTNode] = []

    def find_methods_in_body(class_node, class_name):
        # Determine the body container.
        body = None
        if cfg.body_field:
            body = class_node.child_by_field_name(cfg.body_field)
        container = body if body is not None else class_node
        for child in container.named_children:
            if child.type in cfg.method_types:
                _emit_method(child, rel_path, source, cfg, class_name, nodes)
            # Ruby nests methods in a body_statement node.
            elif child.type == "body_statement":
                for inner in child.named_children:
                    if inner.type in cfg.method_types:
                        _emit_method(inner, rel_path, source, cfg, class_name, nodes)

    def visit(node):
        # ── class-like ────────────────────────────────────────────────────
        if node.type in cfg.class_types or node.type in cfg.class_unwrap:
            cnode = _resolve_class_node(node, cfg)
            if cnode is not None:
                name = _get_name(cnode, source)
                if name:
                    nodes.append(ASTNode(
                        id=f"{rel_path}::{name}",
                        type="class",
                        file=rel_path,
                        line_start=node.start_point[0] + 1,
                        line_end=node.end_point[0] + 1,
                        docstring=_extract_doc(node, source, cfg),
                        imports=[],
                        calls=[],
                    ))
                    if cfg.class_in_body:
                        find_methods_in_body(cnode, name)
            # Don't recurse further into a class body when methods are
            # discovered via the body walk (avoids double emission).
            if cfg.class_in_body:
                return

        # ── Rust impl block: methods attributed to the impl'd type ─────────
        if cfg.impl_node and node.type == cfg.impl_node:
            type_node = next(
                (c for c in node.named_children if c.type == "type_identifier"), None
            )
            type_name = _node_text(type_node, source) if type_node is not None else None
            decls = node.child_by_field_name("body")
            if decls is None:
                decls = next(
                    (c for c in node.named_children if c.type == "declaration_list"),
                    None,
                )
            if decls is not None:
                for child in decls.named_children:
                    if child.type in cfg.method_types or child.type in cfg.function_types:
                        _emit_method(child, rel_path, source, cfg, type_name, nodes)
            return

        # ── free function (or top-level method emitted as a function) ──────
        # - function_types are always free functions.
        # - Go-style: methods carry a receiver and live at top level -> function.
        # - Ruby-style: a `method` node reached here is NOT inside a class body
        #   (those are consumed by find_methods_in_body), so it is top-level.
        if node.type in cfg.function_types or node.type in cfg.method_types:
            _emit_method(node, rel_path, source, cfg, None, nodes)
            return

        for child in node.children:
            visit(child)

    visit(tree.root_node)

    for n in nodes:
        n.imports = list(file_imports)
    return nodes


# ──────────────────────────────────────────────────────────────────────────
# Per-language configs
# ──────────────────────────────────────────────────────────────────────────
LANG_CONFIGS: dict[str, LangConfig] = {
    ".go": LangConfig(
        grammar_module="tree_sitter_go",
        class_unwrap={"type_declaration": "type_spec"},
        function_types=("function_declaration",),
        method_types=("method_declaration",),
        class_in_body=False,  # Go methods carry a receiver, emitted standalone
        call_types=("call_expression",),
        call_function_field="function",
        import_types=("import_declaration",),
        comment_types=("comment",),
        doc_prefix="//",
    ),
    ".java": LangConfig(
        grammar_module="tree_sitter_java",
        class_types=("class_declaration", "interface_declaration", "enum_declaration"),
        method_types=("method_declaration", "constructor_declaration"),
        class_in_body=True,
        body_field="body",
        call_types=("method_invocation",),
        call_function_field="name",
        import_types=("import_declaration",),
        comment_types=("block_comment", "line_comment"),
        doc_prefix="/**",
    ),
    ".rb": LangConfig(
        grammar_module="tree_sitter_ruby",
        class_types=("class", "module"),
        method_types=("method", "singleton_method"),
        class_in_body=True,
        body_field=None,  # methods live directly under the class node
        call_types=("call",),
        call_function_field=None,  # Ruby `call`: name is first named child
        import_types=(),
        import_call_names=("require", "require_relative", "load"),
        comment_types=("comment",),
        doc_prefix="#",
    ),
    ".rs": LangConfig(
        grammar_module="tree_sitter_rust",
        class_types=("struct_item", "trait_item", "enum_item"),
        function_types=("function_item",),
        method_types=("function_item", "function_signature_item"),
        class_in_body=False,  # methods are discovered via impl blocks
        impl_node="impl_item",
        call_types=("call_expression", "macro_invocation"),
        call_function_field="function",
        import_types=("use_declaration",),
        comment_types=("line_comment", "block_comment"),
        doc_prefix="///",
        doc_text_child="doc_comment",
    ),
}
