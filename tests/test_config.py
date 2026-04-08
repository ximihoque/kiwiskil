# tests/test_config.py
import tempfile
from pathlib import Path
from indexer.config import Config, load_config, save_config

def test_load_defaults():
    with tempfile.TemporaryDirectory() as d:
        cfg = load_config(Path(d))
        assert cfg.wiki_dir == "wiki"
        assert cfg.max_tokens_per_batch == 8000

def test_save_and_reload():
    with tempfile.TemporaryDirectory() as d:
        cfg = Config(
            provider="openai/gpt-4o",
            api_key_env="OPENAI_API_KEY",
            wiki_dir="docs/wiki",
            ignore=["node_modules"],
            max_tokens_per_batch=4000,
            pre_commit=True,
            synthesize_commit_message=False,
        )
        save_config(Path(d), cfg)
        reloaded = load_config(Path(d))
        assert reloaded.provider == "openai/gpt-4o"
        assert reloaded.wiki_dir == "docs/wiki"
        assert reloaded.max_tokens_per_batch == 4000
