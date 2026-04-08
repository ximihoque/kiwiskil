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

def load_manifest(repo_root: Path) -> Manifest:
    path = repo_root / MANIFEST_PATH
    if not path.exists():
        return Manifest(last_indexed_commit=None, indexed_at="", files={})
    data = json.loads(path.read_text())
    files = {
        k: FileEntry(**v)
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
