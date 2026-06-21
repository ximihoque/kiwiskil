from __future__ import annotations
import json, hashlib
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

MANIFEST_PATH = ".indexer/manifest.json"

@dataclass
class FileEntry:
    hash: str
    wiki_page: str
    component_ids: list[str]
    # Additive SCIP interop: maps each component_id -> its SCIP descriptor
    # string (see indexer.scip). The primary key stays component_ids; this is
    # extra metadata for SCIP-aware consumers. Optional/back-compatible: older
    # manifests without it load fine and default to {}.
    scip: dict[str, str] = field(default_factory=dict)

@dataclass
class Manifest:
    last_indexed_commit: Optional[str]
    indexed_at: str
    files: dict[str, FileEntry] = field(default_factory=dict)

    def stale_files(self, repo_root: Path, candidate_paths: list[str]) -> list[str]:
        stale = []
        for rel_path in candidate_paths:
            abs_path = repo_root / rel_path
            if not abs_path.exists():
                continue
            current_hash = compute_hash(abs_path)
            entry = self.files.get(rel_path)
            if entry is None or entry.hash != current_hash:
                stale.append(rel_path)
        return stale

def compute_hash(path: Path) -> str:
    h = hashlib.sha256(path.read_bytes()).hexdigest()
    return f"sha256:{h}"


def file_entry_for(file_hash: str, wiki_page: str, file_nodes: list) -> "FileEntry":
    """Build a FileEntry for one source file from its ASTNodes.

    Single source of truth for both `kiwiskil run` and `--smart` repair so the
    manifest (primary component_ids + additive SCIP descriptors) is always
    constructed identically. `file_nodes` are the ASTNodes whose .file == this
    file.
    """
    from indexer.scip import scip_symbol
    return FileEntry(
        hash=file_hash,
        wiki_page=wiki_page,
        component_ids=[n.id for n in file_nodes],
        scip={n.id: scip_symbol(n) for n in file_nodes},
    )

def load_manifest(repo_root: Path) -> Manifest:
    path = repo_root / MANIFEST_PATH
    if not path.exists():
        return Manifest(last_indexed_commit=None, indexed_at="", files={})
    data = json.loads(path.read_text())
    files = {
        k: FileEntry(
            hash=v["hash"],
            wiki_page=v["wiki_page"],
            component_ids=v.get("component_ids", []),
            scip=v.get("scip", {}),
        )
        for k, v in data.get("files", {}).items()
    }
    return Manifest(
        last_indexed_commit=data.get("last_indexed_commit"),
        indexed_at=data.get("indexed_at", ""),
        files=files,
    )

def save_manifest(repo_root: Path, manifest: Manifest) -> None:
    path = repo_root / MANIFEST_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "last_indexed_commit": manifest.last_indexed_commit,
        "indexed_at": manifest.indexed_at,
        "files": {k: asdict(v) for k, v in manifest.files.items()},
    }
    path.write_text(json.dumps(data, indent=2))
