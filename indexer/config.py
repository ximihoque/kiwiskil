# indexer/config.py
from __future__ import annotations
import tomllib
import tomli_w
from dataclasses import dataclass, field
from pathlib import Path

FILENAME = ".indexer.toml"

@dataclass
class Config:
    provider: str = "anthropic/claude-sonnet-4-6"
    api_key_env: str = "ANTHROPIC_API_KEY"
    wiki_dir: str = "wiki"
    ignore: list[str] = field(default_factory=lambda: [
        "node_modules", ".venv", "dist", "build", "__pycache__", "*.test.*"
    ])
    max_tokens_per_batch: int = 8000
    pre_commit: bool = True
    synthesize_commit_message: bool = True

def load_config(repo_root: Path) -> Config:
    path = repo_root / FILENAME
    if not path.exists():
        return Config()
    with open(path, "rb") as f:
        data = tomllib.load(f)
    llm = data.get("llm", {})
    idx = data.get("indexer", {})
    hooks = data.get("hooks", {})
    return Config(
        provider=llm.get("provider", Config.provider),
        api_key_env=llm.get("api_key_env", Config.api_key_env),
        wiki_dir=idx.get("wiki_dir", Config.wiki_dir),
        ignore=idx.get("ignore", Config().ignore),
        max_tokens_per_batch=idx.get("max_tokens_per_batch", Config.max_tokens_per_batch),
        pre_commit=hooks.get("pre_commit", Config.pre_commit),
        synthesize_commit_message=hooks.get("synthesize_commit_message", Config.synthesize_commit_message),
    )

def save_config(repo_root: Path, cfg: Config) -> None:
    data = {
        "llm": {"provider": cfg.provider, "api_key_env": cfg.api_key_env},
        "indexer": {"wiki_dir": cfg.wiki_dir, "ignore": cfg.ignore, "max_tokens_per_batch": cfg.max_tokens_per_batch},
        "hooks": {"pre_commit": cfg.pre_commit, "synthesize_commit_message": cfg.synthesize_commit_message},
    }
    with open(repo_root / FILENAME, "wb") as f:
        tomli_w.dump(data, f)
