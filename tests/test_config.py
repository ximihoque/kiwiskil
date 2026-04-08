# tests/test_config.py
import tempfile
from pathlib import Path
from indexer.config import Config, load_config, save_config

def test_load_defaults():
    with tempfile.TemporaryDirectory() as d:
        cfg = load_config(Path(d))
        assert cfg == Config()

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
        assert reloaded == cfg

def test_partial_toml_uses_defaults():
    with tempfile.TemporaryDirectory() as d:
        toml_content = b"[llm]\nprovider = \"openai/gpt-4o\"\n"
        (Path(d) / ".indexer.toml").write_bytes(toml_content)
        cfg = load_config(Path(d))
        assert cfg.provider == "openai/gpt-4o"
        assert cfg.wiki_dir == Config().wiki_dir  # default preserved
        assert cfg.pre_commit == Config().pre_commit  # default preserved
