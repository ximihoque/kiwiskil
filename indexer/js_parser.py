from __future__ import annotations
from pathlib import Path
from typing import Optional
from indexer.ast_parser import ASTNode

def _rel(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def _get_language(suffix: str):
    """Return the tree-sitter Language object for the given file suffix."""
    if suffix in {".js", ".jsx", ".mjs", ".cjs"}:
        import tree_sitter_javascript as tjs
        from tree_sitter import Language
        return Language(tjs.language())
    elif suffix in {".ts", ".tsx"}:
        import tree_sitter_typescript as tts
        from tree_sitter import Language
        if suffix == ".tsx":
            return Language(tts.language_tsx())
        return Language(tts.language_typescript())
    return None


def _node_text(node, source: bytes) -> str:
    return source[node.start_byte:node.end_byte].decode("utf-8", errors="replace")


def _extract_jsdoc(node, source: bytes) -> Optional[str]:
    """Look for a JSDoc comment immediately before this node."""
    prev = node.prev_named_sibling
    if prev and prev.type == "comment":
        text = _node_text(prev, source).strip()
        if text.startswith("/**"):
            # Strip /** ... */ and leading * from each line
            lines = text[3:-2].splitlines()
            cleaned = []
            for line in lines:
                line = line.strip().lstrip("*").strip()
                if line:
                    cleaned.append(line)
            return " ".join(cleaned) or None
    return None


def _extract_imports(tree, source: bytes) -> list[str]:
    imports = []
    cursor = tree.walk()

    def visit(node):
        if node.type in ("import_statement", "import_declaration"):
            imports.append(_node_text(node, source).split("\n")[0][:80])
        for child in node.children:
            visit(child)

    visit(tree.root_node)
    return imports


def _extract_calls(node, source: bytes) -> list[str]:
    """Recursively extract all function call names from a node."""
    calls = set()

    def visit(n):
        if n.type == "call_expression":
            fn = n.child_by_field_name("function")
            if fn:
                if fn.type == "identifier":
                    calls.add(_node_text(fn, source))
                elif fn.type == "member_expression":
                    prop = fn.child_by_field_name("property")
                    if prop:
                        calls.add(_node_text(prop, source))
        for child in n.children:
            visit(child)

    visit(node)
    return list(calls)


def _get_name(node, source: bytes) -> Optional[str]:
    """Extract name from a function/class/method node."""
    name_node = node.child_by_field_name("name")
    if name_node:
        return _node_text(name_node, source)
    return None


def parse_js_file(path: Path, repo_root: Path) -> list[ASTNode]:
    """Parse a JS/TS file using tree-sitter and return ASTNode list."""
    try:
        from tree_sitter import Parser
    except ImportError as e:
        import warnings
        warnings.warn(f"tree-sitter not installed, skipping {path}: {e}")
        return []

    suffix = path.suffix.lower()
    language = _get_language(suffix)
    if language is None:
        return []

    try:
        source = path.read_bytes()
        parser = Parser(language)
        tree = parser.parse(source)
    except Exception as e:
        import warnings
        warnings.warn(f"Failed to parse {path}: {e}")
        return []

    rel_path = _rel(path, repo_root)
    file_imports = _extract_imports(tree, source)
    nodes: list[ASTNode] = []

    def visit(node, class_name: Optional[str] = None):
        # ── Class declaration ──────────────────────────────────────────────
        if node.type in ("class_declaration", "class"):
            name = _get_name(node, source)
            if name:
                nodes.append(ASTNode(
                    id=f"{rel_path}::{name}",
                    type="class",
                    file=rel_path,
                    line_start=node.start_point[0] + 1,
                    line_end=node.end_point[0] + 1,
                    docstring=_extract_jsdoc(node, source),
                    imports=list(file_imports),
                    calls=[],
                ))
                # Visit class body with class_name context
                body = node.child_by_field_name("body")
                if body:
                    for child in body.children:
                        visit(child, class_name=name)
                return  # Don't double-visit body below

        # ── Method definition (inside class) ──────────────────────────────
        elif node.type == "method_definition" and class_name:
            name = _get_name(node, source)
            if name:
                body = node.child_by_field_name("body")
                calls = _extract_calls(body, source) if body else []
                nodes.append(ASTNode(
                    id=f"{rel_path}::{class_name}.{name}",
                    type="method",
                    file=rel_path,
                    line_start=node.start_point[0] + 1,
                    line_end=node.end_point[0] + 1,
                    docstring=_extract_jsdoc(node, source),
                    imports=list(file_imports),
                    calls=calls,
                ))
            return

        # ── Function declaration ───────────────────────────────────────────
        elif node.type == "function_declaration" and not class_name:
            name = _get_name(node, source)
            if name:
                body = node.child_by_field_name("body")
                calls = _extract_calls(body, source) if body else []
                nodes.append(ASTNode(
                    id=f"{rel_path}::{name}",
                    type="function",
                    file=rel_path,
                    line_start=node.start_point[0] + 1,
                    line_end=node.end_point[0] + 1,
                    docstring=_extract_jsdoc(node, source),
                    imports=list(file_imports),
                    calls=calls,
                ))
            return

        # ── const/let/var = arrow function or function expression ──────────
        elif node.type in ("lexical_declaration", "variable_declaration") and not class_name:
            for declarator in node.children:
                if declarator.type == "variable_declarator":
                    name_node = declarator.child_by_field_name("name")
                    value_node = declarator.child_by_field_name("value")
                    if name_node and value_node and value_node.type in (
                        "arrow_function", "function", "function_expression"
                    ):
                        name = _node_text(name_node, source)
                        calls = _extract_calls(value_node, source)
                        nodes.append(ASTNode(
                            id=f"{rel_path}::{name}",
                            type="function",
                            file=rel_path,
                            line_start=node.start_point[0] + 1,
                            line_end=node.end_point[0] + 1,
                            docstring=_extract_jsdoc(node, source),
                            imports=list(file_imports),
                            calls=calls,
                        ))
            return

        # ── Recurse into children ──────────────────────────────────────────
        for child in node.children:
            visit(child, class_name=class_name)

    visit(tree.root_node)
    return nodes