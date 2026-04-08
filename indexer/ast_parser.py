from __future__ import annotations
import ast, json, hashlib
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

@dataclass
class ASTNode:
    id: str                          # "rel/path.py::Class.method"
    type: str                        # "function" | "method" | "class"
    file: str                        # repo-relative path
    line_start: int
    line_end: int
    docstring: Optional[str]
    imports: list[str] = field(default_factory=list)
    calls: list[str] = field(default_factory=list)
    called_by: list[str] = field(default_factory=list)

def _rel(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)

def _extract_imports(tree: ast.Module) -> list[str]:
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for alias in node.names:
                imports.append(f"{mod}.{alias.name}" if mod else alias.name)
    return imports

def _extract_calls(func_node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    calls = []
    for node in ast.walk(func_node):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.append(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                calls.append(node.func.attr)
    return list(set(calls))

def _get_class_method_ids(tree: ast.Module) -> set[int]:
    """Return AST node ids of functions that are direct children of a class body."""
    ids = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    ids.add(id(item))
    return ids

def parse_file(path: Path, repo_root: Path) -> list[ASTNode]:
    """Parse a Python file and return ASTNode list. Returns [] on syntax error."""
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source)
    except SyntaxError:
        return []

    rel_path = _rel(path, repo_root)
    file_imports = _extract_imports(tree)
    method_ids = _get_class_method_ids(tree)
    nodes: list[ASTNode] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            nodes.append(ASTNode(
                id=f"{rel_path}::{node.name}",
                type="class",
                file=rel_path,
                line_start=node.lineno,
                line_end=node.end_lineno or node.lineno,
                docstring=ast.get_docstring(node),
                imports=list(file_imports),
                calls=[],
            ))
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    nodes.append(ASTNode(
                        id=f"{rel_path}::{node.name}.{item.name}",
                        type="method",
                        file=rel_path,
                        line_start=item.lineno,
                        line_end=item.end_lineno or item.lineno,
                        docstring=ast.get_docstring(item),
                        imports=list(file_imports),
                        calls=_extract_calls(item),
                    ))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if id(node) not in method_ids:
                nodes.append(ASTNode(
                    id=f"{rel_path}::{node.name}",
                    type="function",
                    file=rel_path,
                    line_start=node.lineno,
                    line_end=node.end_lineno or node.lineno,
                    docstring=ast.get_docstring(node),
                    imports=list(file_imports),
                    calls=_extract_calls(node),
                ))

    return nodes


def compute_hash_short(path: Path) -> str:
    """Returns first 16 chars of sha256 hex digest — used for cache filenames only."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def load_cached_nodes(repo_root: Path, file_hash: str) -> Optional[list[ASTNode]]:
    p = repo_root / ".indexer" / "cache" / f"{file_hash}.json"
    if not p.exists():
        return None
    data = json.loads(p.read_text())
    return [ASTNode(**n) for n in data]


def save_cached_nodes(repo_root: Path, file_hash: str, nodes: list[ASTNode]) -> None:
    p = repo_root / ".indexer" / "cache" / f"{file_hash}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps([asdict(n) for n in nodes], indent=2))
