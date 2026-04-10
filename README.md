<p align="center">
  <img src="assets/logo.svg" width="100" alt="kiwiskil logo"/>
</p>

<h1 align="center">kiwiskil</h1>

<p align="center">
  <strong>Your codebase, understood by any LLM.</strong><br/>
  Generate a checked-in wiki and skill files from any repo — no cloud, no lock-in.
</p>

<p align="center">
  <a href="https://pypi.org/project/kiwiskil/"><img src="https://img.shields.io/pypi/v/kiwiskil.svg" alt="PyPI version"/></a>
  <a href="https://pypi.org/project/kiwiskil/"><img src="https://img.shields.io/pypi/pyversions/kiwiskil.svg" alt="Python versions"/></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"/></a>
  <a href="https://pypi.org/project/kiwiskil/"><img src="https://img.shields.io/pypi/dm/kiwiskil.svg" alt="PyPI downloads"/></a>
</p>

<p align="center">
  <a href="#install">Install</a> · <a href="#quick-start">Quick start</a> · <a href="#cli">CLI</a> · <a href="#configuration">Configuration</a> · <a href="CONTRIBUTING.md">Contributing</a>
</p>

---

<p align="center">
  <img src="assets/diagram.svg" width="500" alt="kiwiskil architecture diagram"/>
</p>

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
pip install kiwiskil
```

---

## Quick start

```bash
# In any git repo
kiwiskil init       # creates .indexer.toml, installs pre-commit hook, appends CLAUDE.md
kiwiskil run        # generates wiki/ and .indexer/skills/codebase.md
```

On every subsequent commit, the pre-commit hook runs `kiwiskil run --staged` automatically — only changed files are re-indexed.

---

## CLI

```bash
kiwiskil init              # set up config, hook, and CLAUDE.md
kiwiskil run               # smart incremental + deep enrichment (default)
kiwiskil run --skip-deep   # skip narrative/flows/constraints enrichment (faster)
kiwiskil run --force       # force full re-index of all files
kiwiskil run --staged      # incremental on staged files only (used by hook)
kiwiskil status            # show last indexed commit, stale files, stats
kiwiskil hook install      # manually install pre-commit hook
kiwiskil hook remove       # remove pre-commit hook
```

### Deep mode

By default, `kiwiskil run` performs a **deep enrichment** pass after structural indexing. This uses your configured LLM to generate:

- **System narrative** — a plain-English overview of what the codebase does
- **Key request flows** — end-to-end data flows across modules
- **Design constraints** — per-module gotchas, invariants, and non-obvious rules

These appear in `wiki/INDEX.md` and in the skill file, giving agents richer context without reading source. Use `--skip-deep` to run structural-only indexing when speed matters.

---

## Output

### `wiki/INDEX.md`
Top-level map of the entire codebase — which wiki page covers which files, entry points for each group, system overview, and key request flows (when deep mode is enabled).

### `wiki/<group>.md`
One page per logical folder cluster. Each page contains:
- **Modules** — files covered
- **Key Symbols** — functions, classes, methods with one-line descriptions
- **Relationships** — what this group calls, what calls it, what it imports
- **Entry Points** — symbols with no callers (architectural roots)
- **Data Flows** — end-to-end flows through this module *(deep mode)*
- **Design Constraints** — invariants and non-obvious rules to respect *(deep mode)*

### `.indexer/skills/codebase.md`
A skill file compatible with Claude Code, Cursor, Copilot, and other LLM agents. Drop it into your agent's skill directory to unlock structured codebase navigation. The skill file includes:

- Codebase stats (symbol count, file count, index date, commit)
- System overview and key request flows
- Wiki page index with entry points
- Critical constraints extracted per module
- Step-by-step navigation guide for agents
- Component ID format reference and manifest lookup instructions

**Navigation tools exposed to agents:**

| Tool | Description |
|------|-------------|
| `find_module(query)` | Search wiki pages by keyword |
| `get_symbol(id)` | Look up any symbol by component ID (`file::Class.method`) |
| `trace_callers(symbol_id)` | Find what calls a given symbol |
| `what_changed(since_commit)` | List changed files with their wiki pages |
| `entry_points()` | List all architectural entry points |

---

## Configuration

`.indexer.toml` is created by `kiwiskil init` and checked into the repo:

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
deep = true           # set false to skip --deep on commits (faster, structural only)
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

| Language | Status | Parser |
|----------|--------|--------|
| Python | Supported | stdlib `ast` |
| JavaScript (`.js`, `.jsx`, `.mjs`, `.cjs`) | Supported | tree-sitter |
| TypeScript (`.ts`, `.tsx`) | Supported | tree-sitter |
| Go, Rust, Java, Ruby | Planned | tree-sitter |

---

## License

MIT
