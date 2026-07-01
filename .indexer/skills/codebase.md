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

- **373 symbols** across **37 files** — indexed 2026-07-01 @ `76002e95`
- Wiki: `wiki/` — 3 page(s)
- Manifest: `.indexer/manifest.json` — maps every file to its wiki page and component IDs

## System Overview

kiwiskil is a polyglot codebase indexing engine that transforms a git repository into a structured, LLM-navigable wiki. The pipeline runs through five sequential phases orchestrated by `cli.py` (`_index_files` → `_finalise_index_and_skill`): source files are discovered via `git.py`, parsed into `ASTNode` records by `ast_parser.py` (Python stdlib AST), `js_parser.py` (tree-sitter JS/TS), and `ts_extract.py` (tree-sitter Go/Java/Ruby/Rust), then described by `llm.py` (Anthropic SDK / claude CLI / LiteLLM). `grouper.py` clusters files into wiki pages by density-based folder merging; `wiki.py` renders Jinja2 templates into `wiki/*.md` and `wiki/INDEX.md`; `manifest.py` persists file hashes and SCIP component IDs for incremental re-indexing. `graph.py` computes PageRank, blast radius, and god-node rankings over the call graph to drive `repo_map` and per-symbol relationship sections. `verify.py` detects drift (stale files, missing pages, orphaned entries), and `repair.py` translates a `VerifyReport` into a `RepairPlan` that `_run_smart` executes without a full re-index.
## Key Request Flows
- Full index run: `cli.run` → `git.all_tracked_files` → `_index_and_persist` → `_index_files` (parse → `llm.describe_nodes`/`describe_files`/`deep_enrich_page` → `build_blast_radius_map` → `wiki.build_page`/`write_page`) → `_finalise_index_and_skill` (`graph.repo_map`/`god_nodes` → `llm.deep_enrich_index` → `wiki.build_index`/`write_index`) → `manifest.save_manifest`
- Smart incremental repair: `cli.run --smart` → `_run_smart` → `verify.scan` (VerifyReport) → `repair.plan` (RepairPlan) → `repair.execute` → `_index_files` (stale files only) → `_finalise_index_and_skill` → `save_manifest`
- LLM dispatch: `llm.describe_nodes`/`deep_enrich_page`/`deep_enrich_index` → `_complete` → `_is_anthropic` branch: `_anthropic_completion` (Anthropic SDK) | `_claude_cli_completion` (subprocess claude CLI) | `completion` (LiteLLM) → `_clean_json` (parse fenced/bare JSON response)
- Source parsing: `_index_files` → `ast_parser.parse_file` → Python: stdlib `ast.walk` | JS/TS: `js_parser.parse_js_file` (tree-sitter) | Go/Java/Ruby/Rust: `ts_extract.extract_generic` (tree-sitter LangConfig) → `ASTNode` list → `scip.scip_symbol` → `manifest.file_entry_for` → `Manifest`
- Pre-commit hook flow: `hooks.install_hook` (writes `.git/hooks/pre-commit` via `_hook_script_fresh`/`_hook_script_append`) → git commit triggers hook → `cli.run --staged` → `git.staged_files` → `_index_and_persist` (staged files expanded to groups via `_expand_candidates_to_groups`) → `manifest.save_manifest` → `synthesize_commit_message`

## Wiki Pages

| Page | Covers | Key Entry Points |
|------|--------|-----------------|
| [indexer](../wiki/indexer.md) | indexer/__init__.py, indexer/ast_parser.py, indexer/cli.py, indexer/config.py, indexer/git.py, indexer/graph.py, indexer/grouper.py, indexer/hooks.py, indexer/js_parser.py, indexer/langs.py, indexer/llm.py, indexer/manifest.py, indexer/repair.py, indexer/scip.py, indexer/ts_extract.py, indexer/verify.py, indexer/wiki.py |  |
| [tests](../wiki/tests.md) | tests/__init__.py, tests/test_ast_parser.py, tests/test_config.py, tests/test_graph.py, tests/test_grouper.py, tests/test_init.py, tests/test_langs.py, tests/test_llm_dispatch.py, tests/test_manifest.py, tests/test_multilang.py, tests/test_repair_plan.py, tests/test_scip.py, tests/test_smart_integration.py, tests/test_verify.py, tests/test_wiki.py |  |
| [tests_fixtures](../wiki/tests_fixtures.md) | tests/fixtures/sample_go/server.go, tests/fixtures/sample_java/Widget.java, tests/fixtures/sample_py/auth.py, tests/fixtures/sample_ruby/widget.rb, tests/fixtures/sample_rust/widget.rs |  |
## Critical Constraints (read before editing)
**indexer**
- full_repo=True is required to enable destructive cleanup (manifest prune + orphan wiki page deletion); on partial/staged runs this flag MUST be False or the entire wiki is wiped for every file not in the current candidate set
- called_by on ASTNode is always empty after parse_file(); it is populated only in the cross-reference pass inside _index_files() by matching bare function names across all nodes — meaning cached nodes loaded from disk also have empty called_by and are re-linked each run
- AST cache keys are the first 16 hex chars of the file sha256, stored at .indexer/cache/<hash>.json; cache is never invalidated by time, only by file content hash change — a corrupted cache file returns None (re-parses silently) but a structurally valid but semantically stale cache (e.g. bug in old parse logic) will be used as-is until the file changes
- staged_files() uses --diff-filter=ACM, so deleted files are never returned; deletion reconciliation only happens via _prune_deleted() on a no-candidates run or as part of full_repo cleanup — a staged deletion without any other staged file will not trigger wiki cleanup until the next non-staged run
- Config.merge_threshold controls density_group() page merging; changing it mid-life restructures the entire wiki layout, making every incremental run produce different page assignments than the existing manifest — a full re-index (--force) is required after changing this value
- NAV_GUIDANCE_MARKER ('Codebase Navigation') is used as an idempotency sentinel in both _ensure_nav_guidance() and verify.py; if the heading text changes in one place but not the other, guidance will be written twice or the verify check will falsely report drift
**tests**
- blast_radius uses called_by (pre-resolved component IDs), not calls (bare names); callers_of reads called_by directly while callees_of performs bare-name resolution against the node list — mixing the two fields incorrectly will silently return wrong results
- callees_of drops any bare name that cannot be resolved to a known node ID; external stdlib calls (e.g. 'print') are silently discarded, not errored
- blast_radius excludes the queried symbol itself from its result set and must terminate on cycles — tests confirm both; any implementation that includes self or loops infinitely fails
- god_nodes degree is sum of len(called_by) + len(calls) per node (both directions), not just in-degree; the test fixture confirms hub with 3 callers + 2 callees scores 5
- pagerank must sum to 1.0 within 1e-6 tolerance and be deterministic across repeated calls on the same input; symmetric mutual-call pairs must yield equal rank
- load_config merges a partial TOML file with Config() defaults field-by-field — missing TOML keys fall back to the dataclass default, not to None; base_url defaults to empty string '', not None

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