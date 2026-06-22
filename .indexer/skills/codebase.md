---
name: codebase
description: >
  Navigate this codebase. Activates when the user asks about code structure,
  where a function or class lives, how a module works, who calls a method,
  what a file does, how a request flows end-to-end, what changed, or where
  to make an edit. Trigger phrases include: "where is", "how does X work",
  "what does X do", "find the code for", "which file", "who calls", "trace
  the flow", "show me how", "explain the architecture", "what module",
  "read the source", "navigate the repo", "look at the codebase",
  "understand the code". Do NOT activate for general programming questions
  unrelated to this specific repo, writing new code from scratch, or tasks
  that require no codebase knowledge.
---

# Codebase Navigation

This repo is indexed. **Check the wiki before reading any source file.**
The wiki captures structure, relationships, and constraints in a fraction of the tokens.

## Stats

- **350 symbols** across **37 files** — indexed 2026-06-22 @ `8a10bfcb`
- Wiki: `wiki/` — 3 page(s)
- Manifest: `.indexer/manifest.json` — maps every file to its wiki page and component IDs

## System Overview

kiwiskil is a codebase indexer that transforms source repos into a checked-in, LLM-navigable knowledge artifact (wiki pages + manifest + skill file) with no running server. The pipeline is orchestrated by `cli.py` (`run`/`run --smart`/`run --staged`/`status`/`init`/`hook`): `langs.py` filters indexable files; `ast_parser.py`, `js_parser.py`, and `ts_extract.py` parse symbols and call graphs per language; `grouper.py` clusters files into wiki pages by density threshold; `llm.py` calls Anthropic SDK or falls back to the `claude` CLI subprocess to generate LLM descriptions; `wiki.py` renders Jinja2-templated markdown with OKF YAML frontmatter; and `manifest.py` persists file→component-ID hash mappings. `graph.py` computes PageRank and blast-radius over the call graph; `verify.py` detects drift between filesystem, manifest, and wiki; `repair.py` computes and executes a minimal `RepairPlan`; and `hooks.py` manages the pre-commit hook for incremental re-indexing.
## Key Request Flows
- Full index: cli.run → git.all_tracked_files → langs.is_indexable → cli._index_and_persist → ast_parser.parse_file / js_parser.parse_js_file / ts_extract.extract_generic → grouper.density_group → llm.describe_nodes / deep_enrich_page → graph.build_blast_radius_map → wiki.build_page / write_page → cli._finalise_index_and_skill [graph.repo_map + llm.deep_enrich_index → wiki.build_index] → manifest.save_manifest
- Incremental staged (pre-commit hook): hooks.py triggers cli.run --staged → git.staged_files → langs.is_indexable → manifest.Manifest.stale_files (hash check) → cli._index_and_persist (changed files only) → same _index_files/_finalise pipeline → manifest.save_manifest → llm.synthesize_commit_message
- Smart repair: cli.run --smart → cli._run_smart → verify.scan [manifest vs filesystem vs wiki drift detection → VerifyReport] → repair.plan [VerifyReport → RepairPlan: dirty re-index, orphan page delete, dangling entry prune] → repair.execute [cli._index_files + cli._finalise_index_and_skill + manifest.save_manifest + cli._ensure_nav_guidance]
- LLM dispatch: llm._complete → llm._resolve_api_key (env var priority) → Anthropic SDK path (llm._anthropic_completion) OR claude CLI subprocess fallback (llm._claude_cli_completion) → llm._clean_json strips fences/preamble → structured dict returned to describe_nodes / deep_enrich_page / deep_enrich_index
- Blast radius tracing: graph.blast_radius(symbol) → BFS over reverse call edges via graph._index_by_id → transitive set of impacted component IDs → precomputed for all nodes by graph.build_blast_radius_map during _index_files → rendered per symbol in wiki.py._symbol_relationships as 'Editing this affects' lists

## Wiki Pages

| Page | Covers | Key Entry Points |
|------|--------|-----------------|
| [indexer](../wiki/indexer.md) | indexer/__init__.py, indexer/ast_parser.py, indexer/cli.py, indexer/config.py, indexer/git.py, indexer/graph.py, indexer/grouper.py, indexer/hooks.py, indexer/js_parser.py, indexer/langs.py, indexer/llm.py, indexer/manifest.py, indexer/repair.py, indexer/scip.py, indexer/ts_extract.py, indexer/verify.py, indexer/wiki.py |  |
| [tests](../wiki/tests.md) | tests/__init__.py, tests/test_ast_parser.py, tests/test_config.py, tests/test_graph.py, tests/test_grouper.py, tests/test_init.py, tests/test_langs.py, tests/test_llm_dispatch.py, tests/test_manifest.py, tests/test_multilang.py, tests/test_repair_plan.py, tests/test_scip.py, tests/test_smart_integration.py, tests/test_verify.py, tests/test_wiki.py |  |
| [tests_fixtures](../wiki/tests_fixtures.md) | tests/fixtures/sample_go/server.go, tests/fixtures/sample_java/Widget.java, tests/fixtures/sample_py/auth.py, tests/fixtures/sample_ruby/widget.rb, tests/fixtures/sample_rust/widget.rs |  |
## Critical Constraints (read before editing)
**indexer**
- page_basename() is the single source of truth for wiki filename derivation — manifest's wiki_page field MUST use page_relpath() (which calls page_basename()), never the raw group label; divergence causes --smart to see phantom missing-page + orphan-page for the same group
- _index_files() writes wiki pages as a side effect but does NOT touch INDEX.md, the skill file, manifest, .gitignore, hooks, or CLAUDE.md — callers must call _finalise_index_and_skill() and save_manifest() separately or those artifacts will be stale
- PageContext.timestamp and blast_radius_map are computed in cli.py (_index_files), never inside wiki.py or templates — Date.now()-equivalent calls are banned inside rendering to preserve determinism and resume safety
- delete_orphan_pages() excludes INDEX.md by name check (p.name != 'INDEX.md') — all other wiki/*.md files not in the manifest's referenced_pages set are deleted unconditionally, including any hand-authored pages
- _ensure_nav_guidance() uses the string 'Codebase Navigation' as the idempotency marker, not a comment or sentinel line — editing that heading in CLAUDE.md/AGENTS.md causes the block to be appended again on next init or run
- --smart and --force/--staged are mutually exclusive at the CLI level (UsageError); --dry-run and --no-hook-check are only valid with --smart; these constraints are enforced before any I/O
**tests**
- Exit code is the CI gate signal: `--dry-run` exits nonzero on ANY drift (stale hash, missing wiki page, no manifest with indexable files) and exits zero only on fully clean state — callers must not treat nonzero as error in repair flows, only in CI checks.
- `--smart` is mutually exclusive with both `--force` and `--staged`; passing either combination fails before touching the filesystem.
- A repo with no indexable tracked files (e.g. only README.md) causes `--smart` to exit nonzero with a 'nothing to index' message — it does NOT silently succeed.
- `_stub_llm` must patch all four symbols in `indexer.cli` (not `indexer.llm` or module-local); tests that call LLM code paths without this stub will make real API calls or crash on missing keys.
- `page_basename('.')` returns `'root'` and nested paths use `_` as separator (`a/b/c` → `a_b_c`); the manifest's `wiki_page` field must be computed via `page_relpath` not by manual string construction — the two must stay in sync or orphan detection breaks.
- Blast-radius lists longer than ~10 entries are truncated with a `… (+k more)` marker in page output; tests assert on `'more)'` substring, so this truncation threshold is a tested invariant, not an implementation detail.

## Workflow — How to Answer Questions About This Codebase

Follow these steps in order. Do not skip ahead to reading source files.

1. **Orient** — Read `wiki/INDEX.md` first. It has the system overview, module map, and cross-cutting flows.

2. **Locate the module** — Match the question to a wiki page from the table above. Read that page only; do not read unrelated pages.

3. **Look up symbols** — Component IDs follow `relative/path.py::ClassName.method_name`. Find the relevant ID in the wiki page's Key Symbols table and read its description there.

4. **Trace calls without reading source** — Use the `## Relationships → Called by` section on the wiki page to trace callers. Use `## Relationships → Calls` to trace callees.

5. **Read source only when necessary** — Once you know the exact file and line range from the manifest or wiki, read only that range. Do not read whole files speculatively.

6. **Answer with specifics** — Include the component ID, file path, and line range (if known) in your answer so the user can navigate directly.

## Output Format

- Always name the specific file and component ID when identifying where code lives.
- For call traces, show the chain: `A → B → C`, one line per hop.
- For architecture questions, describe the flow in prose then list the files involved.
- Keep answers concise. Do not dump raw wiki content — summarise what is relevant.
- If a question requires reading source, state which file and lines you are about to read before reading them.

## When to Use Wiki vs Source

| Question type | Use |
|--------------|-----|
| What does X do? | Wiki — Key Symbols table |
| Who calls X? | Wiki — Relationships → Called by |
| What does this module own? | Wiki — Modules table |
| How does a request flow end-to-end? | Wiki — Data Flows section (if --deep indexed) |
| What are the gotchas or invariants? | Wiki — Design Constraints section (if --deep indexed) |
| What is the exact implementation? | Source — use line_start/line_end from manifest |
| Is X tested? | Source — check test files directly |

## Component ID Format

```
relative/path.py::ClassName.method_name   ← method
relative/path.py::ClassName               ← class
relative/path.py::function_name           ← top-level function
```

## Manifest Lookup

To find which wiki page covers a file:
```
.indexer/manifest.json → files["path/to/file.py"] → wiki_page
```

To find all symbols in a file:
```
.indexer/manifest.json → files["path/to/file.py"] → component_ids
```

## Edge Cases

- **Symbol not in wiki** — The index covers files tracked at index time. If a symbol is missing, it was added after the last `kiwiskil run`. Tell the user and read the source file directly.
- **Wiki page missing** — If a wiki page linked from the index does not exist, fall back to the manifest and source. Note the gap to the user.
- **Ambiguous name** — If multiple symbols share a name, list all matching component IDs and ask the user which they mean before proceeding.
- **Question spans multiple modules** — Read each relevant wiki page in turn. Do not conflate descriptions from different pages.