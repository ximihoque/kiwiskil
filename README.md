# kiwiskil

> Chat with your codebase using any LLM.

kiwiskil generates a checked-in structural wiki and skill files from any codebase. It enables LLM agents to navigate code without reading source files — using a knowledge graph built from your repo and checked into git.

---

## How it works

1. **AST parsing** extracts symbols, imports, and call graphs from your source files (deterministic, free)
2. **LiteLLM** adds one-line descriptions per symbol using any provider you configure
3. **A density-based grouper** organises files into wiki pages by logical density, not directory structure
4. **A pre-commit hook** keeps the wiki in sync — every commit includes updated wiki pages atomically
5. **A skill file** is generated at `.indexer/skills/codebase.md` so any LLM agent can navigate your codebase via structured tools

The wiki is plain markdown checked into your repo. No cloud service, no search index, no lock-in.

---

## Install

```bash
pip install codeindexer
```

---

## Quick start

```bash
# In any git repo
indexer init       # creates .indexer.toml, installs pre-commit hook, appends CLAUDE.md
indexer run        # generates wiki/ and .indexer/skills/codebase.md
```

On every subsequent commit, the pre-commit hook runs `indexer run --staged` automatically — only changed files are re-indexed.

---

## CLI

```bash
indexer init              # set up config, hook, and CLAUDE.md
indexer run               # smart: incremental if indexed before, full if not
indexer run --force       # force full re-index
indexer run --staged      # incremental on staged files only (used by hook)
indexer status            # show last indexed commit, stale files, stats
indexer hook install      # manually install pre-commit hook
indexer hook remove       # remove pre-commit hook
```

---

## Output

### `wiki/INDEX.md`
Top-level map of the entire codebase — which wiki page covers which files, and the entry points for each.

### `wiki/<group>.md`
One page per logical folder cluster. Each page contains:
- **Modules** — files covered
- **Key Symbols** — functions, classes, methods with one-line descriptions
- **Relationships** — what this group calls, what calls it, what it imports
- **Entry Points** — symbols with no callers (architectural roots)

### `.indexer/skills/codebase.md`
A skill file compatible with Claude Code, Cursor, Copilot, and other LLM agents. Drop it into your agent's skill directory to unlock:

- `find_module(query)` — search wiki pages by keyword
- `get_symbol(id)` — look up any symbol by component ID (`file::Class.method`)
- `trace_callers(symbol_id)` — find what calls a given symbol
- `what_changed(since_commit)` — list changed files with their wiki pages
- `entry_points()` — list all architectural entry points

---

## Configuration

`.indexer.toml` is created by `indexer init` and checked into your repo:

```toml
[llm]
provider = "anthropic/claude-sonnet-4-6"  # any LiteLLM-compatible model string
api_key_env = "ANTHROPIC_API_KEY"         # env var name, not the key itself

[indexer]
wiki_dir = "wiki"
ignore = ["node_modules", ".venv", "dist", "build", "__pycache__", "*.test.*"]
max_tokens_per_batch = 8000

[hooks]
pre_commit = true
synthesize_commit_message = true
```

Any LiteLLM-compatible provider works: OpenAI, Anthropic, Gemini, Ollama, local models.

---

## Commit message synthesis

When running as a pre-commit hook, kiwiskil synthesises a commit message from the code changes and prints it to stdout. You can use it, edit it, or ignore it — your choice.

---

## Design principles

- **Structural facts only** — wiki pages contain symbols, relationships, and entry points. No prose summaries, no architectural opinions. The client LLM draws its own conclusions.
- **Checked in, not served** — the wiki is plain markdown in your repo. It travels with your code, is tracked by git, and is readable by humans and agents alike.
- **Incremental by default** — git diff + content hash manifest means only changed files are re-processed on each commit.
- **Provider-agnostic** — LiteLLM means you can use any model, local or cloud, without changing the tool.

---

## Supported languages

Python (stdlib `ast`). JS, TS, Go, Rust, Java, Ruby support planned via tree-sitter.

---

## License

MIT
