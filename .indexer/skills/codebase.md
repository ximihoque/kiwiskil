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

- **344 symbols** across **37 files** — indexed 2026-06-21 @ `b950860b`
- Wiki: `wiki/` — 3 page(s)
- Manifest: `.indexer/manifest.json` — maps every file to its wiki page and component IDs

## System Overview

kiwiskil is a codebase indexer that transforms source repositories into a checked-in, LLM-navigable knowledge artifact — wiki pages, a manifest, and a skill file — without requiring a running server or cloud service. The pipeline flows: `langs.py` filters indexable files → `ast_parser.py`/`js_parser.py`/`ts_extract.py` parse symbols and call graphs → `grouper.py` clusters files into pages by density threshold → `llm.py` enriches with LLM-generated descriptions and narratives (via Anthropic SDK, claude CLI, or LiteLLM) → `wiki.py` renders Jinja2-templated markdown pages with OKF YAML frontmatter → `manifest.py` persists file→component-ID mappings. `graph.py` precomputes PageRank and blast radius over the call graph for every symbol. `verify.py` detects drift between filesystem, manifest, and wiki; `repair.py` computes a minimal `RepairPlan` and executes it. `cli.py` orchestrates all modes (`run`, `run --smart`, `run --staged`, `status`, `init`, `hook`) and `hooks.py` manages the pre-commit hook that triggers incremental re-indexing on every commit.
## Key Request Flows
- Full index run: cli.run → git.all_tracked_files → langs.is_indexable → cli._index_and_persist → cli._index_files [parse_file/parse_js_file/extract_generic → grouper.density_group → llm.describe_nodes/describe_files/deep_enrich_page → graph.build_blast_radius_map → wiki.build_page/write_page] → cli._finalise_index_and_skill [graph.repo_map + llm.deep_enrich_index → wiki.build_index/write_index] → manifest.save_manifest
- Incremental staged index (pre-commit hook): cli.run --staged → git.staged_files → langs.is_indexable → cli._index_and_persist (only changed files, hash-checked via manifest.Manifest.stale_files) → same _index_files/_finalise_index_and_skill pipeline → manifest.save_manifest → llm.synthesize_commit_message
- Smart repair flow: cli.run --smart → cli._run_smart → verify.scan [checks manifest vs filesystem vs wiki pages for drift] → repair.plan [VerifyReport → RepairPlan: re-index dirty files, delete orphan pages, prune dangling entries] → repair.execute [cli._index_files + cli._finalise_index_and_skill + manifest.save_manifest + cli._ensure_nav_guidance]
- LLM dispatch: llm._complete → llm._resolve_api_key (env var priority) → if Anthropic key: llm._anthropic_completion (Anthropic SDK); else if claude CLI on PATH: llm._claude_cli_completion (subprocess); else raise → llm._clean_json strips fences/preamble → caller (describe_nodes/deep_enrich_page/deep_enrich_index) extracts structured dict
- Blast radius tracing: graph.blast_radius(symbol, all_nodes) → BFS over reverse call edges via _index_by_id → returns transitive set of all component IDs whose behavior could change → precomputed for all nodes by build_blast_radius_map in _index_files → rendered inline per symbol in wiki.py._symbol_relationships → exposed in wiki page 'Editing this affects' lists

## Repo Map (ranked by importance)

The most load-bearing symbols first (PageRank over the call graph). Start here to orient before reading any wiki page or source file:

- indexer/ast_parser.py::ASTNode  (callers: 11)
- indexer/cli.py::run  (callers: 15)
- indexer/ast_parser.py::parse_file  (callers: 36)
- indexer/js_parser.py::_node_text  (callers: 12)
- indexer/ts_extract.py::_node_text  (callers: 12)
- indexer/config.py::Config  (callers: 30)
- indexer/langs.py::is_indexable  (callers: 6)
- indexer/git.py::_run  (callers: 4)
- indexer/manifest.py::Manifest  (callers: 25)
- tests/test_multilang.py::_by_id  (callers: 22)
- indexer/graph.py::_index_by_id  (callers: 4)
- indexer/js_parser.py::visit  (callers: 8)
- indexer/ts_extract.py::visit  (callers: 8)
- tests/test_graph.py::_node  (callers: 19)
- tests/test_scip.py::_node  (callers: 19)
- indexer/manifest.py::FileEntry  (callers: 25)
- indexer/llm.py::_clean_json  (callers: 10)
- indexer/grouper.py::density_group  (callers: 8)
- indexer/verify.py::VerifyReport  (callers: 13)
- tests/test_graph.py::_chain_nodes  (callers: 13)
- indexer/js_parser.py::_get_name  (callers: 5)
- indexer/ts_extract.py::_get_name  (callers: 5)
- indexer/graph.py::_adjacency  (callers: 1)
- indexer/graph.py::pagerank  (callers: 6)
- indexer/llm.py::_complete  (callers: 9)
- indexer/ts_extract.py::_emit_method  (callers: 3)
- indexer/wiki.py::page_basename  (callers: 4)
- indexer/manifest.py::compute_hash  (callers: 16)
- indexer/ast_parser.py::_extract_calls  (callers: 4)
- indexer/js_parser.py::_extract_calls  (callers: 4)
- indexer/ts_extract.py::_extract_calls  (callers: 4)
- indexer/manifest.py::load_manifest  (callers: 7)
- indexer/verify.py::scan  (callers: 17)
- indexer/wiki.py::PageContext  (callers: 16)
- indexer/wiki.py::build_page  (callers: 16)
- tests/test_wiki.py::_make_node  (callers: 15)
- indexer/config.py::load_config  (callers: 7)
- indexer/graph.py::blast_radius  (callers: 7)
- indexer/ts_extract.py::_last_identifier  (callers: 2)
- tests/test_init.py::_bootstrap_repo  (callers: 14)
- tests/test_smart_integration.py::_bootstrap_repo  (callers: 14)
- indexer/graph.py::callees_of  (callers: 3)
- indexer/git.py::all_tracked_files  (callers: 5)
- indexer/git.py::is_git_repo  (callers: 6)
- indexer/scip.py::_split_id  (callers: 1)
- indexer/grouper.py::folder_of  (callers: 2)
- indexer/grouper.py::prefixes  (callers: 2)
- indexer/cli.py::_is_indexable  (callers: 4)
- indexer/verify.py::_is_indexable  (callers: 4)
- indexer/hooks.py::_hook_command  (callers: 3)
- indexer/scip.py::scip_symbol  (callers: 9)
- indexer/ts_extract.py::_extract_doc  (callers: 3)
- indexer/repair.py::RepairPlan  (callers: 3)
- indexer/cli.py::_ensure_cache_gitignore  (callers: 4)
- indexer/wiki.py::IndexEntry  (callers: 5)
- indexer/graph.py::repo_map  (callers: 6)
- indexer/js_parser.py::_extract_jsdoc  (callers: 2)
- indexer/llm.py::_claude_cli_path  (callers: 2)
- indexer/graph.py::god_nodes  (callers: 5)
- indexer/cli.py::_index_and_persist  (callers: 2)
- indexer/ts_extract.py::_resolve_class_node  (callers: 2)
- indexer/ts_extract.py::find_methods_in_body  (callers: 2)
- indexer/graph.py::ranked_symbols  (callers: 3)
- indexer/grouper.py::resolve_group  (callers: 1)
- tests/test_llm_dispatch.py::_cfg  (callers: 5)
- indexer/cli.py::_run_smart  (callers: 1)
- indexer/git.py::changed_files_since  (callers: 1)
- indexer/git.py::staged_files  (callers: 1)
- indexer/graph.py::_bare_name  (callers: 1)
- indexer/llm.py::_claude_cli_completion  (callers: 3)
- indexer/ast_parser.py::_extract_imports  (callers: 3)
- indexer/js_parser.py::_extract_imports  (callers: 3)
- indexer/ts_extract.py::_extract_imports  (callers: 3)
- tests/test_llm_dispatch.py::FakeProc  (callers: 3)
- tests/test_verify.py::_seed_valid_state  (callers: 6)
- indexer/ast_parser.py::_rel  (callers: 2)
- indexer/js_parser.py::_rel  (callers: 2)
- indexer/repair.py::plan  (callers: 8)
- indexer/wiki.py::_jinja_env  (callers: 2)
- indexer/wiki.py::_yaml_frontmatter  (callers: 2)
- indexer/ast_parser.py::_get_class_method_ids  (callers: 1)
- indexer/js_parser.py::parse_js_file  (callers: 1)
- indexer/ts_extract.py::extract_generic  (callers: 1)
- indexer/wiki.py::_short  (callers: 2)
- indexer/wiki.py::build_index  (callers: 4)
- indexer/manifest.py::save_manifest  (callers: 9)

## Wiki Pages

| Page | Covers | Key Entry Points |
|------|--------|-----------------|
| [indexer](../wiki/indexer.md) | indexer/ast_parser.py, indexer/cli.py, indexer/config.py, indexer/git.py, indexer/graph.py, indexer/grouper.py, indexer/hooks.py, indexer/js_parser.py, indexer/langs.py, indexer/llm.py, indexer/manifest.py, indexer/repair.py, indexer/scip.py, indexer/ts_extract.py, indexer/verify.py, indexer/wiki.py | main, init, status, hook, hook_install |
| [tests_fixtures](../wiki/tests_fixtures.md) | tests/fixtures/sample_go/server.go, tests/fixtures/sample_java/Widget.java, tests/fixtures/sample_py/auth.py, tests/fixtures/sample_ruby/widget.rb, tests/fixtures/sample_rust/widget.rs | Server, Start, Widget, Widget.bump, Widget.helper |
| [tests](../wiki/tests.md) | tests/test_ast_parser.py, tests/test_config.py, tests/test_graph.py, tests/test_grouper.py, tests/test_init.py, tests/test_langs.py, tests/test_llm_dispatch.py, tests/test_manifest.py, tests/test_multilang.py, tests/test_repair_plan.py, tests/test_scip.py, tests/test_smart_integration.py, tests/test_verify.py, tests/test_wiki.py | test_parse_returns_nodes, test_function_node, test_method_node, test_class_node, test_docstring_extracted |
## Critical Constraints (read before editing)
**indexer**
- Cache keys are the first 16 chars of SHA256 of raw file bytes — two files with identical content share a cache entry, which is intentional but means renaming a file does not invalidate the cache if content is unchanged.
- changed_files_since returns paths relative to repo root as strings, not Path objects; callers in cli.py must convert before passing to is_indexable or open.
- _index_files uses setdefault to bucket symbols by density group, meaning a file whose group changes between runs will appear in the new bucket only after a full re-index — incremental runs do not remove stale group assignments from the manifest.
- _finalise_index_and_skill calls repo_map which reads the manifest, so save_manifest must be called before _finalise or INDEX.md reflects the previous run's state.
- ASTNode.calls is deduplicated at extraction time (_extract_calls uses a set); ordering is non-deterministic across Python versions — do not rely on call order for dependency graphs.
- The navigation guidance block in CLAUDE.md is gated on a marker string via lstrip+in check; if the user edits CLAUDE.md and removes only the marker (not the block), _ensure_nav_guidance will re-append a duplicate block.
**tests**
- blast_radius uses called_by (pre-populated component ids) for reverse traversal, NOT calls; tests confirm it excludes self and terminates on cycles via BFS/DFS with a visited set — callers must ensure called_by is cross-referenced before calling blast_radius
- callees_of resolves bare callee names (from .calls) to full component ids by matching the bare name suffix against known node ids; names that don't match any node id are silently dropped — external stdlib calls like 'print' vanish without error
- god_nodes degree = len(called_by) + len(calls) (raw list lengths, NOT resolved ids); unresolvable external names in .calls still inflate degree counts
- pagerank scores sum to exactly 1.0 (±1e-6) and are deterministic; mutual-cycle nodes receive equal scores; empty input returns {} not an error
- repo_map accepts max_tokens as a hard budget using a ~4 chars/token heuristic; symbols are emitted in descending pagerank order and output is truncated when the budget is reached — the trailing symbols are silently omitted, not indicated with ellipsis
- load_config returns Config() defaults (not raises) when no .indexer.toml exists; partial TOML merges only the specified keys and preserves dataclass defaults for all others — the TOML section key is [llm], not [indexer] or [config]

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