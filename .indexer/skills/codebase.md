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

- **353 symbols** across **37 files** — indexed 2026-06-22 @ `2f65edbc`
- Wiki: `wiki/` — 3 page(s)
- Manifest: `.indexer/manifest.json` — maps every file to its wiki page and component IDs

## System Overview

kiwiskil is a codebase indexer that transforms source repos into a checked-in, LLM-navigable knowledge artifact (wiki pages + manifest + skill file) with no running server. The pipeline entry point is `cli.py` (`run`/`run --smart`/`run --staged`/`status`/`init`/`hook`): language filtering via `langs.py`, multi-language symbol/call-graph extraction via `ast_parser.py`, `js_parser.py`, and `ts_extract.py`, file clustering via `grouper.py` (density threshold), and markdown wiki generation via `wiki.py` (Jinja2 + OKF YAML frontmatter). `llm.py` drives all LLM calls (Anthropic SDK or `claude` CLI subprocess fallback) for node descriptions and page enrichment; `graph.py` computes PageRank and blast-radius over the call graph; `manifest.py` persists file→component-ID hash mappings; and `verify.py`/`repair.py` detect and resolve drift between filesystem, manifest, and wiki. `hooks.py` wires the pre-commit hook for incremental re-indexing.
## Key Request Flows
- Full index: cli.run → git.all_tracked_files → langs.is_indexable → cli._index_and_persist → ast_parser.parse_file / js_parser.parse_js_file / ts_extract.extract_generic → grouper.density_group → llm.describe_nodes / deep_enrich_page → graph.build_blast_radius_map → wiki.build_page / write_page → cli._finalise_index_and_skill [graph.repo_map + llm.deep_enrich_index → wiki.build_index] → manifest.save_manifest
- Incremental staged (pre-commit hook): hooks.py triggers cli.run --staged → git.staged_files → langs.is_indexable → manifest.Manifest.stale_files (hash check) → cli._index_and_persist (changed files only) → same _index_files/_finalise pipeline → manifest.save_manifest → llm.synthesize_commit_message
- Smart repair: cli.run --smart → cli._run_smart → verify.scan [manifest vs filesystem vs wiki drift → VerifyReport] → repair.plan [VerifyReport → RepairPlan] → repair.execute [cli._index_files + cli._finalise_index_and_skill + manifest.save_manifest + cli._ensure_nav_guidance]
- LLM dispatch: llm._complete → llm._resolve_api_key → Anthropic SDK (llm._anthropic_completion) OR claude CLI subprocess fallback (llm._claude_cli_completion) → llm._clean_json strips fences/preamble → structured dict returned to describe_nodes / deep_enrich_page / deep_enrich_index
- Blast radius tracing: graph.blast_radius(symbol) → BFS over reverse call edges via graph._index_by_id → transitive impacted component IDs → precomputed by graph.build_blast_radius_map during _index_files → rendered per symbol in wiki.py._symbol_relationships as 'Editing this affects' lists

## Wiki Pages

| Page | Covers | Key Entry Points |
|------|--------|-----------------|
| [indexer](../wiki/indexer.md) | indexer/__init__.py, indexer/ast_parser.py, indexer/cli.py, indexer/config.py, indexer/git.py, indexer/graph.py, indexer/grouper.py, indexer/hooks.py, indexer/js_parser.py, indexer/langs.py, indexer/llm.py, indexer/manifest.py, indexer/repair.py, indexer/scip.py, indexer/ts_extract.py, indexer/verify.py, indexer/wiki.py |  |
| [tests](../wiki/tests.md) | tests/__init__.py, tests/test_ast_parser.py, tests/test_config.py, tests/test_graph.py, tests/test_grouper.py, tests/test_init.py, tests/test_langs.py, tests/test_llm_dispatch.py, tests/test_manifest.py, tests/test_multilang.py, tests/test_repair_plan.py, tests/test_scip.py, tests/test_smart_integration.py, tests/test_verify.py, tests/test_wiki.py |  |
| [tests_fixtures](../wiki/tests_fixtures.md) | tests/fixtures/sample_go/server.go, tests/fixtures/sample_java/Widget.java, tests/fixtures/sample_py/auth.py, tests/fixtures/sample_ruby/widget.rb, tests/fixtures/sample_rust/widget.rs |  |
## Critical Constraints (read before editing)
**indexer**
- ASTNode.called_by is NEVER populated by ast_parser — it is always `[]` at parse time and only filled by the cross-reference pass in `_index_files` (cli.py Phase 2); cached nodes therefore also have empty called_by and must go through cross-reference again on every run
- Orphan wiki page deletion and manifest pruning are ONLY safe when `full_repo=True`; on --staged or incremental runs these destructive operations are explicitly skipped because the manifest only reflects the touched subset, and deleting based on a partial view would wipe all untouched pages' entries
- `_expand_candidates_to_groups()` computes grouping over the ENTIRE tracked repo (not just candidates) so that partial runs produce byte-identical page output to full runs for touched groups — if you call `density_group` on candidates only, you get a different bucketing and split pages
- `staged_files()` and `changed_files_since()` both use `--diff-filter=ACM` — deletions (D) are excluded; deleted-file cleanup only happens via `_prune_deleted()` called explicitly in the no-candidates branch of `run`, meaning a delete-only commit is NOT reconciled by the pre-commit hook, only by a subsequent plain `run`
- `load_cached_nodes()` returns `None` (not raises) on cache miss or JSON corruption; `parse_file()` returns `[]` (not raises) on syntax error or unknown suffix — callers must handle empty returns gracefully
- Config TOML has three top-level sections (`llm`, `indexer`, `hooks`); `load_config` silently returns `Config()` defaults if `.indexer.toml` is absent — there is no validation or error on a malformed file, missing keys just fall back to defaults
**tests**
- imports on ASTNode are file-level; every node from a given file carries the full import list, not just the imports visible in that node's scope
- callees_of resolves bare callee names (the strings in node.calls) against known node IDs by suffix match; unresolvable names (builtins, third-party) are silently dropped—callers must not assume completeness
- blast_radius uses called_by (pre-resolved component IDs) for traversal, NOT calls; the cross-ref pass in cli.py::_index_files must populate called_by before graph functions are meaningful
- blast_radius returns empty set for an unknown symbol ID rather than raising—callers cannot distinguish 'no upstream callers' from 'symbol not in graph'
- god_nodes degree = len(called_by) + len(calls) on the raw node fields; it does NOT resolve bare names, so external calls that appear in calls inflate degree artificially
- repo_map token budget is approximate (not exact tokenization); the test uses ~4 chars/token with a 6× slack factor, meaning output can exceed max_tokens in characters if symbol names are short

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