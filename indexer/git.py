# indexer/git.py
from __future__ import annotations
import subprocess
from pathlib import Path
from typing import Optional

def _run(cmd: list[str], cwd: Path) -> str:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result.stdout.strip()

def current_commit(repo_root: Path) -> Optional[str]:
    out = _run(["git", "rev-parse", "HEAD"], cwd=repo_root)
    return out if out else None

def staged_files(repo_root: Path) -> list[str]:
    out = _run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"], cwd=repo_root)
    return [line for line in out.splitlines() if line]

def changed_files_since(repo_root: Path, since_commit: str) -> list[str]:
    out = _run(["git", "diff", "--name-only", "--diff-filter=ACM", since_commit, "HEAD"], cwd=repo_root)
    return [line for line in out.splitlines() if line]

def all_tracked_files(repo_root: Path) -> list[str]:
    out = _run(["git", "ls-files"], cwd=repo_root)
    return [line for line in out.splitlines() if line]

def is_git_repo(repo_root: Path) -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=repo_root, capture_output=True
    )
    return result.returncode == 0
