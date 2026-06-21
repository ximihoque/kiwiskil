---
type: Code Group
title: indexer
description: The indexer module transforms a raw source codebase into a structured,
  incrementally-maintained knowledge artifact (wiki pages + manifest + skill file)
  that LLM agents can navigate token-efficiently.
tags:
- indexer
timestamp: '2026-06-21T20:09:33.562703+00:00'
resource: indexer
---
# indexer/
<!-- kiwiskil:deep -->

## Overview

The indexer module transforms a raw source codebase into a structured, incrementally-maintained knowledge artifact (wiki pages + manifest + skill file) that LLM agents can navigate token-efficiently. It solves the problem of LLMs needing to read entire source trees by pre-extracting symbols, grouping them by logical density, and caching parse results keyed on file content hashes. The pipeline flows through AST parsing (ast_parser.py, js_parser.py), language detection (langs.py), density grouping (grouper.py), LLM-driven wiki generation (llm.py, wiki.py), manifest tracking (manifest.py), and CLI orchestration (cli.py). git.py provides incremental diffing so only changed files re-index. repair.py and verify.py act as a self-healing layer that detects and fixes structural issues before artifact persistence.

## Modules
| File | Purpose |
|------|---------|
| indexer/ast_parser.py | Python AST parser extracting functions, classes, imports, and calls |
| indexer/js_parser.py | JavaScript and TypeScript parser using tree-sitter |
| indexer/langs.py | Language detection and indexability filtering by file suffix |
| indexer/git.py | Git repository utilities for file tracking and commit queries |
| indexer/config.py | Configuration loader and saver for indexer settings |
| indexer/repair.py | Repair planning and execution for drift correction |
| indexer/graph.py | Call graph analysis with PageRank and blast radius computation |
| indexer/verify.py | Drift detection between manifest, filesystem, and wiki pages |
| indexer/grouper.py | Wiki page grouping by density-based folder hierarchy |
| indexer/llm.py | LLM dispatcher for Anthropic SDK, CLI, and third-party providers |
| indexer/wiki.py | Wiki page and index markdown generation with Jinja templating |
| indexer/ts_extract.py | Tree-sitter extraction for Go, Java, Ruby, Rust docstrings |
| indexer/scip.py | SCIP symbol descriptor formatting for component IDs |
| indexer/cli.py | Command-line interface for indexing and managing codebase documentation |
| indexer/manifest.py | Manifest persistence mapping files to component IDs and pages |
| indexer/hooks.py | Pre-commit hook installation and management utilities |
## Key Symbols
| ID | Type | Description |
|----|------|-------------|
| `indexer/ast_parser.py::ASTNode` | class | Data class storing parsed symbol metadata: name, type, docstring, calls, line range |
| `indexer/ast_parser.py::_rel` | function | Convert absolute path to relative path string for display |
| `indexer/ast_parser.py::_extract_imports` | function | Walk AST and collect all import statements as list |
| `indexer/ast_parser.py::_extract_calls` | function | Walk AST, extract function/method calls, return deduplicated list |
| `indexer/ast_parser.py::_get_class_method_ids` | function | Return AST node IDs of functions that are direct class children |
| `indexer/ast_parser.py::parse_file` | function | Parse Python/JS file, extract symbols with docstrings, calls, imports |
| `indexer/ast_parser.py::compute_hash_short` | function | Return first 16 chars of SHA256 hex digest for cache filenames |
| `indexer/ast_parser.py::load_cached_nodes` | function | Deserialize ASTNode list from JSON cache file |
| `indexer/ast_parser.py::save_cached_nodes` | function | Serialize ASTNode list to JSON cache file |
| `indexer/cli.py::_ensure_nav_guidance` | function | Append navigation guidance marker to CLAUDE.md if absent |
| `indexer/cli.py::main` | function | CLI entry point group |
| `indexer/cli.py::init` | function | Create .indexer.toml, install pre-commit hook, update CLAUDE.md |
| `indexer/cli.py::run` | function | Index codebase, generate wiki pages, update manifest incrementally |
| `indexer/cli.py::status` | function | Display last indexed commit, stale files, manifest statistics |
| `indexer/cli.py::hook` | function | CLI group for pre-commit hook management |
| `indexer/cli.py::hook_install` | function | Install pre-commit hook in current repository |
| `indexer/cli.py::hook_remove` | function | Uninstall pre-commit hook from current repository |
| `indexer/cli.py::_ensure_cache_gitignore` | function | Add .indexer/cache/ to root .gitignore, create if needed |
| `indexer/cli.py::_is_indexable` | function | Check if file is indexable by configuration |
| `indexer/cli.py::_index_files` | function | Run indexing pipeline phases 1-5 on candidate files, write wiki pages |
| `indexer/cli.py::_finalise_index_and_skill` | function | Build INDEX.md and codebase.md skill file |
| `indexer/cli.py::_index_and_persist` | function | Full indexing pipeline with artifact persistence |
| `indexer/cli.py::_run_smart` | function | Smart indexing mode: detect issues, fix repairs, generate index |
| `indexer/config.py::Config` | class | Configuration data class with include/exclude patterns |
| `indexer/config.py::load_config` | function | Load TOML config file, return Config with defaults |
| `indexer/config.py::save_config` | function | Write Config to TOML file |
| `indexer/git.py::_run` | function | Execute git command, return stdout stripped |
| `indexer/git.py::current_commit` | function | Return current HEAD commit hash |
| `indexer/git.py::staged_files` | function | Return list of staged file paths |
| `indexer/git.py::changed_files_since` | function | Return files changed since given commit |
| `indexer/git.py::all_tracked_files` | function | Return all files tracked in repository |
| `indexer/git.py::is_git_repo` | function | Check if current directory is git repository |
| `indexer/graph.py::_index_by_id` | function | Map component ID to ASTNode, last write wins |
| `indexer/graph.py::_bare_name` | function | Extract bare callable name from component ID |
| `indexer/graph.py::callers_of` | function | Return sorted component IDs that call symbol |
| `indexer/graph.py::callees_of` | function | Resolve bare call names to component IDs, exclude self-references |
| `indexer/graph.py::blast_radius` | function | Transitive reverse-reachability set: components affected by edit |
| `indexer/graph.py::build_blast_radius_map` | function | Precompute blast radius for all nodes |
| `indexer/graph.py::god_nodes` | function | Top-N highest-degree symbols by caller+callee count |
| `indexer/graph.py::_adjacency` | function | Build directed caller→callee adjacency over known IDs |
| `indexer/graph.py::pagerank` | function | PageRank scores per component ID, deterministic iteration |
| `indexer/graph.py::ranked_symbols` | function | Component IDs ordered by PageRank descending |
| `indexer/graph.py::_approx_tokens` | function | Estimate token count: ~4 chars per token |
| `indexer/graph.py::repo_map` | function | Token-budgeted codebase spine ranked by PageRank, grouped by file until budget exhausted |
| `indexer/grouper.py::density_group` | function | Groups files into wiki pages by folder density threshold, merging sparse folders upward |
| `indexer/grouper.py::folder_of` | function | Extract parent folder path from file path |
| `indexer/grouper.py::prefixes` | function | Generate ancestor folder prefixes from deepest to shallowest |
| `indexer/grouper.py::resolve_group` | function | Find shallowest folder prefix meeting merge threshold for file |
| `indexer/hooks.py::_hook_command` | function | Build pre-commit hook command string |
| `indexer/hooks.py::_hook_script_fresh` | function | Create fresh pre-commit hook script |
| `indexer/hooks.py::_hook_script_append` | function | Append kiwiskil block to existing hook script |
| `indexer/hooks.py::install_hook` | function | Install or update pre-commit hook, handling fresh and existing cases |
| `indexer/hooks.py::remove_hook` | function | Remove kiwiskil-managed portion from pre-commit hook file |
| `indexer/js_parser.py::_rel` | function | Convert absolute path to relative path string |
| `indexer/js_parser.py::_get_language` | function | Return tree-sitter Language for JS/TS file suffix |
| `indexer/js_parser.py::_node_text` | function | Extract UTF-8 text from tree-sitter node |
| `indexer/js_parser.py::_extract_jsdoc` | function | Find and return JSDoc comment preceding a node |
| `indexer/js_parser.py::_extract_imports` | function | Extract all import statement paths from node |
| `indexer/js_parser.py::_extract_calls` | function | Recursively extract function call names from AST node |
| `indexer/js_parser.py::_get_name` | function | Extract identifier from function/class/method tree-sitter node |
| `indexer/js_parser.py::parse_js_file` | function | Parse JS/TS file with tree-sitter, return ASTNode list with calls and docs |
| `indexer/js_parser.py::visit` | function |  |
| `indexer/js_parser.py::visit` | function |  |
| `indexer/js_parser.py::visit` | function |  |
| `indexer/langs.py::is_indexable` | function | Check if file has indexable suffix and doesn't match ignore globs |
| `indexer/llm.py::_is_anthropic` | function | Check if provider string indicates Anthropic API |
| `indexer/llm.py::_claude_cli_path` | function | Find logged-in claude CLI path on PATH, return None if absent |
| `indexer/llm.py::_claude_cli_completion` | function | Run one-shot completion via authenticated claude CLI, return stdout |
| `indexer/llm.py::_complete` | function | Dispatch LLM call to API key, CLI, or raise; supports deep enrichment |
| `indexer/llm.py::_clean_json` | function | Parse JSON from model response, strip preamble and fences, tolerate wrapping |
| `indexer/llm.py::_resolve_api_key` | function | Resolve API key from env var name, direct value, or auto-detect |
| `indexer/llm.py::_anthropic_completion` | function | Call Anthropic SDK directly with provided API key |
| `indexer/llm.py::describe_nodes` | function | Describe batch of ASTNodes via LLM, return dict of 15-word descriptions |
| `indexer/llm.py::describe_files` | function | Describe each file's module-level purpose via LLM, return path->description dict |
| `indexer/llm.py::deep_enrich_page` | function | Generate narrative, data flows, constraints for wiki page group via LLM |
| `indexer/llm.py::deep_enrich_index` | function | Generate system overview and cross-cutting flows for INDEX.md via LLM |
| `indexer/llm.py::synthesize_commit_message` | function | Generate one-line commit message from changed files and symbol descriptions |
| `indexer/manifest.py::FileEntry` | class | Represents a single file entry in the codebase manifest |
| `indexer/manifest.py::Manifest` | class | Tracks source files and their component mappings, detects when files are stale. |
| `indexer/manifest.py::Manifest.stale_files` | method | Identifies source files with changed content hashes since last manifest save. |
| `indexer/manifest.py::compute_hash` | function | Computes SHA-256 hash of a file's bytes. |
| `indexer/manifest.py::file_entry_for` | function | Builds FileEntry for one source file from AST nodes, constructs manifest entries. |
| `indexer/manifest.py::load_manifest` | function | Deserializes manifest from JSON file, returns dict of FileEntry objects. |
| `indexer/manifest.py::save_manifest` | function | Serializes manifest to JSON file. |
| `indexer/repair.py::RepairPlan` | class | Plan for minimal set of repair operations from verification report. |
| `indexer/repair.py::RepairPlan.has_work` | method | Returns true if plan has any repair operations scheduled. |
| `indexer/repair.py::plan` | function | Compute minimum repair operations: re-index dirty files, delete orphans, prune dangling entries. |
| `indexer/repair.py::execute` | function | Execute RepairPlan: re-index files, delete orphans, prune manifest, rebuild INDEX and skill. |
| `indexer/repair.py::_index_entries_from_manifest` | function | Reconstruct IndexEntry list from manifest for INDEX rebuild. |
| `indexer/scip.py::_split_id` | function | Parse SCIP descriptor into (relpath, symbol_part) tuple. |
| `indexer/scip.py::scip_symbol` | function | Generate SCIP descriptor string for an ASTNode. |
| `indexer/ts_extract.py::LangConfig` | class | Configuration for tree-sitter language grammar and extraction rules. |
| `indexer/ts_extract.py::_node_text` | function | Extract UTF-8 text content from a tree-sitter node. |
| `indexer/ts_extract.py::_get_name` | function | Extract name field from tree-sitter node. |
| `indexer/ts_extract.py::_clean_comment` | function | Strip comment markers, join into single docstring. |
| `indexer/ts_extract.py::_doc_anchor` | function | Find node whose preceding siblings contain doc comment. |
| `indexer/ts_extract.py::_extract_doc` | function | Collect contiguous doc-comment siblings immediately above node. |
| `indexer/ts_extract.py::_extract_imports` | function | Extract imported module names from source node. |
| `indexer/ts_extract.py::_last_identifier` | function | Extract trailing identifier (method/function name) from callee node. |
| `indexer/ts_extract.py::_extract_calls` | function | Extract function/method call names from node's descendants. |
| `indexer/ts_extract.py::_load_language` | function | Import grammar package and build tree-sitter Language object. |
| `indexer/ts_extract.py::_resolve_class_node` | function | Apply class_unwrap rule (e.g. Go type_declaration to type_spec). |
| `indexer/ts_extract.py::_emit_method` | function | Extract method/function definition into ASTNode with doc and calls. |
| `indexer/ts_extract.py::extract_generic` | function | Parse source file with tree-sitter, extract ASTNodes for classes, methods, functions. |
| `indexer/ts_extract.py::visit` | function |  |
| `indexer/ts_extract.py::visit` | function |  |
| `indexer/ts_extract.py::find_methods_in_body` | function | Recursively find method definitions within class body node. |
| `indexer/ts_extract.py::visit` | function |  |
| `indexer/verify.py::_is_indexable` | function | Check if file is indexable per language config. |
| `indexer/verify.py::VerifyReport` | class | Report of drift issues: missing wiki pages, stale files, dangling manifest entries. |
| `indexer/verify.py::VerifyReport.total_issues` | method | Count of all issues across all drift categories. |
| `indexer/verify.py::VerifyReport.is_clean` | method | Returns true if total_issues is zero. |
| `indexer/verify.py::scan` | function | Verify generated artifacts against manifest and filesystem, detect all drift. |
| `indexer/verify.py::print_report` | function | Pretty-print VerifyReport to stdout. |
| `indexer/wiki.py::PageContext` | class | Context data for rendering a wiki page template. |
| `indexer/wiki.py::IndexEntry` | class | Entry for the INDEX manifest with entry points and tags. |
| `indexer/wiki.py::_jinja_env` | function | Create Jinja2 environment for wiki page template rendering. |
| `indexer/wiki.py::_first_sentence` | function | Extract first sentence from text (up to first period). |
| `indexer/wiki.py::_tags_from_path` | function | Derive frontmatter tags from group path segments. |
| `indexer/wiki.py::_short` | function | Convert component id to page-local symbol label. |
| `indexer/wiki.py::_capped` | function | Return first N items and count of remaining. |
| `indexer/wiki.py::_symbol_relationships` | function | Build per-symbol inline relationships block: callers, calls, blast radius. |
| `indexer/wiki.py::build_page` | function | Render wiki page from PageContext using Jinja2 template. |
| `indexer/wiki.py::_yaml_frontmatter` | function | Serialize dict to YAML frontmatter body (no delimiters). |
| `indexer/wiki.py::build_index` | function | Render INDEX manifest page. |
| `indexer/wiki.py::page_basename` | function | Sanitize page filename stem from group label: '/' → '_', strip leading/trailing '_/'/'.' |
| `indexer/wiki.py::page_relpath` | function | Return repo-relative wiki page path for a group |
| `indexer/wiki.py::write_page` | function | Write group documentation page to wiki directory |
| `indexer/wiki.py::write_index` | function | Write wiki index file listing all pages |
## Symbol Relationships
### `ASTNode`
- **Callers (9):** _emit_method, _make_node, _node, extract_generic, load_cached_nodes, parse_file, parse_js_file, test_describe_nodes_uses_cli_path_end_to_end … (+1 more)
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _chain_nodes, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_imports, _finalise_index_and_skill … (+148 more)
### `_rel`
- **Callers (2):** parse_file, parse_js_file
- **Calls:** relative_to, str
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+92 more)
### `_extract_imports`
- **Callers (3):** extract_generic, parse_file, parse_js_file
- **Calls:** append, isinstance, walk
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+93 more)
### `_extract_calls`
- **Callers (4):** _emit_method, parse_file, parse_js_file, visit
- **Calls:** append, isinstance, list, set, walk
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_imports, _finalise_index_and_skill, _index_and_persist … (+98 more)
### `_get_class_method_ids`
- **Callers (1):** parse_file
- **Calls:** add, id, isinstance, set, walk
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+91 more)
### `parse_file`
- **Callers (36):** _index_files, test_cache_roundtrip, test_calls_extracted, test_class_node, test_docstring_extracted, test_function_node, test_go_calls, test_go_docstring … (+28 more)
- **Calls:** ASTNode, _extract_calls, _extract_imports, _get_class_method_ids, _rel, append, extract_generic, get … (+9 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+90 more)
### `compute_hash_short`
- **Callers (1):** _index_files
- **Calls:** hexdigest, read_bytes, sha256
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+55 more)
### `load_cached_nodes`
- **Callers (2):** _index_files, test_cache_roundtrip
- **Calls:** ASTNode, exists, loads, read_text
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+56 more)
### `save_cached_nodes`
- **Callers (2):** _index_files, test_cache_roundtrip
- **Calls:** asdict, dumps, mkdir, write_text
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+56 more)
### `_ensure_nav_guidance`
- **Callers (2):** execute, init
- **Calls:** echo, exists, lstrip, read_text, write_text
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+55 more)
### `main`
- **Callers (0):** none
- **Calls:** group
- **Editing this affects:** none
### `init`
- **Callers (0):** none
- **Calls:** _ensure_cache_gitignore, _ensure_nav_guidance, command, cwd, echo, install_hook, is_git_repo, load_config … (+1 more)
- **Editing this affects:** none
### `run`
- **Callers (14):** _bootstrap_repo, _claude_cli_completion, _index_and_persist, _run, is_git_repo, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero … (+6 more)
- **Calls:** UsageError, _ensure_cache_gitignore, _index_and_persist, _is_indexable, _run_smart, all_tracked_files, changed_files_since, command … (+10 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+54 more)
### `status`
- **Callers (0):** none
- **Calls:** _is_indexable, all_tracked_files, command, cwd, echo, is_git_repo, len, load_config … (+2 more)
- **Editing this affects:** none
### `hook`
- **Callers (0):** none
- **Calls:** group
- **Editing this affects:** none
### `hook_install`
- **Callers (0):** none
- **Calls:** command, cwd, echo, install_hook, load_config
- **Editing this affects:** none
### `hook_remove`
- **Callers (0):** none
- **Calls:** command, cwd, echo, remove_hook
- **Editing this affects:** none
### `_ensure_cache_gitignore`
- **Callers (4):** _run_smart, execute, init, run
- **Calls:** echo, exists, read_text, rstrip, write_text
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+55 more)
### `_is_indexable`
- **Callers (4):** _run_smart, run, scan, status
- **Calls:** is_indexable
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+55 more)
### `_index_files`
- **Callers (2):** _index_and_persist, execute
- **Calls:** IndexEntry, PageContext, append, build_blast_radius_map, build_page, compute_hash_short, deep_enrich_page, density_group … (+25 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _run, _run_smart, all_tracked_files … (+54 more)
### `_finalise_index_and_skill`
- **Callers (2):** _index_and_persist, execute
- **Calls:** Environment, FileSystemLoader, build_index, current_commit, deep_enrich_index, echo, get, get_template … (+12 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _index_and_persist, _index_files, _run, _run_smart, all_tracked_files … (+54 more)
### `_index_and_persist`
- **Callers (2):** _run_smart, run
- **Calls:** _finalise_index_and_skill, _index_files, all_tracked_files, compute_hash, current_commit, echo, exists, file_entry_for … (+10 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_files, _run, _run_smart, all_tracked_files … (+54 more)
### `_run_smart`
- **Callers (1):** run
- **Calls:** Exit, _ensure_cache_gitignore, _index_and_persist, _is_indexable, all_tracked_files, echo, execute, has_work … (+6 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, all_tracked_files … (+54 more)
### `Config`
- **Callers (30):** _cfg, load_config, test_clean_report_produces_empty_plan, test_cleanup_ops_carried_through, test_execute_deletes_orphan_pages_and_prunes_manifest, test_execute_restores_agents_md, test_execute_runs_reindex_for_files, test_load_defaults … (+22 more)
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _cfg, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run … (+67 more)
### `load_config`
- **Callers (7):** hook_install, init, run, status, test_load_defaults, test_partial_toml_uses_defaults, test_save_and_reload
- **Calls:** Config, exists, get, list, load, open
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+59 more)
### `save_config`
- **Callers (2):** init, test_save_and_reload
- **Calls:** dump, open
- **Editing this affects:** init, test_save_and_reload
### `_run`
- **Callers (4):** all_tracked_files, changed_files_since, current_commit, staged_files
- **Calls:** run, strip
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run_smart, all_tracked_files … (+54 more)
### `current_commit`
- **Callers (3):** _finalise_index_and_skill, _index_and_persist, execute
- **Calls:** _run
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+54 more)
### `staged_files`
- **Callers (1):** run
- **Calls:** _run, splitlines
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+54 more)
### `changed_files_since`
- **Callers (1):** run
- **Calls:** _run, splitlines
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+54 more)
### `all_tracked_files`
- **Callers (5):** _index_and_persist, _run_smart, run, scan, status
- **Calls:** _run, splitlines
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+54 more)
### `is_git_repo`
- **Callers (6):** _index_and_persist, execute, init, run, scan, status
- **Calls:** run
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+54 more)
### `_index_by_id`
- **Callers (4):** blast_radius, callees_of, callers_of, repo_map
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+81 more)
### `_bare_name`
- **Callers (1):** callees_of
- **Calls:** split
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+63 more)
### `callers_of`
- **Callers (2):** test_callers_of_empty_when_no_callers, test_callers_of_returns_caller_ids
- **Calls:** _index_by_id, get, set, sorted
- **Editing this affects:** test_callers_of_empty_when_no_callers, test_callers_of_returns_caller_ids
### `callees_of`
- **Callers (3):** god_nodes, test_callees_of_resolves_bare_names_to_ids, test_callees_of_skips_unresolvable_external_names
- **Calls:** _bare_name, _index_by_id, add, append, get, set, setdefault, sorted
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+62 more)
### `blast_radius`
- **Callers (7):** build_blast_radius_map, test_blast_radius_diamond, test_blast_radius_excludes_self, test_blast_radius_handles_cycles, test_blast_radius_is_transitive_reverse_reachability, test_blast_radius_leaf_caller_is_empty, test_blast_radius_unknown_symbol_is_empty
- **Calls:** _index_by_id, add, append, deque, discard, get, popleft, set
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+63 more)
### `build_blast_radius_map`
- **Callers (2):** _index_files, test_build_blast_radius_map_keys_every_node
- **Calls:** blast_radius
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+56 more)
### `god_nodes`
- **Callers (5):** _finalise_index_and_skill, test_god_nodes_empty_input, test_god_nodes_n_larger_than_nodes, test_god_nodes_ranks_by_degree, test_god_nodes_respects_n
- **Calls:** append, callees_of, len, set, sort
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+59 more)
### `_adjacency`
- **Callers (1):** pagerank
- **Calls:** append, items, set, sorted
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+70 more)
### `pagerank`
- **Callers (6):** ranked_symbols, test_pagerank_empty_input, test_pagerank_handles_cycles, test_pagerank_is_deterministic, test_pagerank_keys_every_node_and_sums_to_one, test_pagerank_ranks_a_hub_above_leaves
- **Calls:** _adjacency, abs, get, len, range, sum, values
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+69 more)
### `ranked_symbols`
- **Callers (3):** repo_map, test_ranked_symbols_empty, test_ranked_symbols_orders_by_pagerank_desc
- **Calls:** pagerank, sorted
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+63 more)
### `_approx_tokens`
- **Callers (1):** repo_map
- **Calls:** len, max
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+61 more)
### `repo_map`
- **Callers (6):** _finalise_index_and_skill, test_repo_map_empty, test_repo_map_larger_budget_includes_more, test_repo_map_leads_with_highest_ranked, test_repo_map_respects_token_budget, test_repo_map_returns_string
- **Calls:** _approx_tokens, _index_by_id, append, get, join, len, ranked_symbols, set
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+60 more)
### `density_group`
- **Callers (8):** _index_files, test_deep_sparse_merges_upward, test_dense_folder_gets_own_page, test_different_folders_get_separate_groups, test_returns_all_files, test_root_files_count_correctly, test_root_level_files, test_sparse_folders_merge_to_parent
- **Calls:** Path, defaultdict, folder_of, join, len, prefixes, range, resolve_group … (+2 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+62 more)
### `folder_of`
- **Callers (2):** density_group, resolve_group
- **Calls:** Path, str
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+64 more)
### `prefixes`
- **Callers (2):** density_group, resolve_group
- **Calls:** join, len, range, split
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+64 more)
### `resolve_group`
- **Callers (1):** density_group
- **Calls:** folder_of, len, prefixes
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+63 more)
### `_hook_command`
- **Callers (3):** _hook_script_append, _hook_script_fresh, install_hook
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _hook_script_append, _hook_script_fresh, _index_and_persist, _index_files … (+59 more)
### `_hook_script_fresh`
- **Callers (1):** install_hook
- **Calls:** _hook_command
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+57 more)
### `_hook_script_append`
- **Callers (1):** install_hook
- **Calls:** _hook_command
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+57 more)
### `install_hook`
- **Callers (3):** execute, hook_install, init
- **Calls:** _hook_command, _hook_script_append, _hook_script_fresh, chmod, enumerate, exists, join, mkdir … (+5 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+56 more)
### `remove_hook`
- **Callers (1):** hook_remove
- **Calls:** append, exists, join, read_text, splitlines, strip, unlink, write_text
- **Editing this affects:** hook_remove
### `_rel`
- **Callers (2):** parse_file, parse_js_file
- **Calls:** relative_to, str
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+92 more)
### `_get_language`
- **Callers (1):** parse_js_file
- **Calls:** Language, language, language_tsx, language_typescript
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+92 more)
### `_node_text`
- **Callers (9):** _extract_calls, _extract_doc, _extract_imports, _extract_jsdoc, _get_name, _last_identifier, extract_generic, parse_js_file … (+1 more)
- **Calls:** decode
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_doc, _extract_imports, _extract_jsdoc … (+102 more)
### `_extract_jsdoc`
- **Callers (2):** parse_js_file, visit
- **Calls:** _node_text, append, join, lstrip, splitlines, startswith, strip
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_imports, _finalise_index_and_skill, _index_and_persist … (+98 more)
### `_extract_imports`
- **Callers (3):** extract_generic, parse_file, parse_js_file
- **Calls:** _node_text, append, split, visit, walk
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+93 more)
### `_extract_calls`
- **Callers (4):** _emit_method, parse_file, parse_js_file, visit
- **Calls:** _node_text, add, child_by_field_name, list, set, visit
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_imports, _finalise_index_and_skill, _index_and_persist … (+98 more)
### `_get_name`
- **Callers (4):** _emit_method, extract_generic, parse_js_file, visit
- **Calls:** _node_text, child_by_field_name
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_imports, _finalise_index_and_skill, _index_and_persist … (+98 more)
### `parse_js_file`
- **Callers (1):** parse_file
- **Calls:** ASTNode, Parser, _extract_calls, _extract_imports, _extract_jsdoc, _get_language, _get_name, _node_text … (+9 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+91 more)
### `visit`
- **Callers (5):** _extract_calls, _extract_imports, extract_generic, parse_js_file, visit
- **Calls:** _node_text, append, split, visit
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_imports, _finalise_index_and_skill, _index_and_persist … (+98 more)
### `visit`
- **Callers (5):** _extract_calls, _extract_imports, extract_generic, parse_js_file, visit
- **Calls:** _node_text, add, child_by_field_name, visit
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_imports, _finalise_index_and_skill, _index_and_persist … (+98 more)
### `visit`
- **Callers (5):** _extract_calls, _extract_imports, extract_generic, parse_js_file, visit
- **Calls:** ASTNode, _extract_calls, _extract_jsdoc, _get_name, _node_text, append, child_by_field_name, list … (+1 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_imports, _finalise_index_and_skill, _index_and_persist … (+98 more)
### `is_indexable`
- **Callers (5):** _is_indexable, test_is_indexable_accepts_known_suffixes, test_is_indexable_honours_part_glob, test_is_indexable_honours_path_glob, test_is_indexable_rejects_unknown_suffix
- **Calls:** Path, any, fnmatch
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _is_indexable, _run … (+60 more)
### `_is_anthropic`
- **Callers (1):** _complete
- **Calls:** any, startswith
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+55 more)
### `_claude_cli_path`
- **Callers (2):** _claude_cli_completion, _complete
- **Calls:** which
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+55 more)
### `_claude_cli_completion`
- **Callers (3):** _complete, test_claude_cli_completion_invokes_print_mode, test_claude_cli_completion_raises_on_nonzero
- **Calls:** RuntimeError, _claude_cli_path, removeprefix, run, strip
- **Editing this affects:** _bootstrap_repo, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart, all_tracked_files … (+54 more)
### `_complete`
- **Callers (9):** deep_enrich_index, deep_enrich_page, describe_files, describe_nodes, synthesize_commit_message, test_deep_flag_uses_configured_model_cli, test_explicit_api_key_takes_priority_over_cli, test_falls_back_to_cli_when_no_key_and_cli_present … (+1 more)
- **Calls:** RuntimeError, _anthropic_completion, _claude_cli_completion, _claude_cli_path, _is_anthropic, _resolve_api_key, completion
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart, all_tracked_files … (+54 more)
### `_clean_json`
- **Callers (10):** deep_enrich_index, deep_enrich_page, describe_files, describe_nodes, test_clean_json_fenced, test_clean_json_list_payload, test_clean_json_plain, test_clean_json_preamble_then_bare_object … (+2 more)
- **Calls:** append, find, group, len, loads, range, removeprefix, removesuffix … (+3 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+61 more)
### `_resolve_api_key`
- **Callers (1):** _complete
- **Calls:** get, isupper, replace
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+55 more)
### `_anthropic_completion`
- **Callers (1):** _complete
- **Calls:** Anthropic, create, removeprefix
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+55 more)
### `describe_nodes`
- **Callers (2):** _index_files, test_describe_nodes_uses_cli_path_end_to_end
- **Calls:** _clean_json, _complete, dumps, get, isinstance, warn
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+54 more)
### `describe_files`
- **Callers (1):** _index_files
- **Calls:** _clean_json, _complete, dumps, get, isinstance, items, split, warn
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+54 more)
### `deep_enrich_page`
- **Callers (1):** _index_files
- **Calls:** _clean_json, _complete, dumps, get, isinstance, warn
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+54 more)
### `deep_enrich_index`
- **Callers (1):** _finalise_index_and_skill
- **Calls:** _clean_json, _complete, dumps, get, isinstance, warn
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+54 more)
### `synthesize_commit_message`
- **Callers (1):** _index_and_persist
- **Calls:** _complete, dumps, isinstance, strip, warn
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+54 more)
### `FileEntry`
- **Callers (25):** _seed_valid_state, file_entry_for, load_manifest, test_execute_deletes_orphan_pages_and_prunes_manifest, test_fresh_file_not_stale, test_missing_wiki_page_pulls_files_from_manifest, test_pages_missing_deep_excluded_when_skip_deep, test_pages_missing_deep_included_when_deep_active … (+17 more)
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+66 more)
### `Manifest`
- **Callers (25):** _empty_manifest, _make_repo_with_manifest, _seed_valid_state, load_manifest, test_execute_deletes_orphan_pages_and_prunes_manifest, test_execute_runs_reindex_for_files, test_fresh_file_not_stale, test_missing_wiki_page_pulls_files_from_manifest … (+17 more)
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _empty_manifest, _finalise_index_and_skill, _index_and_persist, _index_files, _make_repo_with_manifest … (+70 more)
### `Manifest.stale_files`
- **Callers (0):** none
- **Calls:** append, compute_hash, exists, get
- **Editing this affects:** none
### `compute_hash`
- **Callers (16):** Manifest.stale_files, _index_and_persist, _seed_valid_state, execute, test_compute_hash_stable, test_fresh_file_not_stale, test_scan_deep_page_with_empty_narrative_not_flagged, test_scan_detects_missing_index_and_skill … (+8 more)
- **Calls:** hexdigest, read_bytes, sha256
- **Editing this affects:** Manifest.stale_files, _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run … (+59 more)
### `file_entry_for`
- **Callers (2):** _index_and_persist, execute
- **Calls:** FileEntry, scip_symbol
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+55 more)
### `load_manifest`
- **Callers (7):** run, status, test_empty_manifest_on_missing, test_load_manifest_missing_component_ids, test_save_and_reload, test_smart_fills_fresh_repo_with_no_manifest, test_smart_fills_never_indexed_tracked_file
- **Calls:** FileEntry, Manifest, exists, get, items, loads, read_text
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+58 more)
### `save_manifest`
- **Callers (9):** _index_and_persist, execute, test_save_and_reload, test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero, test_smart_dry_run_does_not_modify_filesystem, test_smart_dry_run_drift_exits_nonzero, test_smart_fills_never_indexed_tracked_file … (+1 more)
- **Calls:** asdict, dumps, items, mkdir, write_text
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+56 more)
### `RepairPlan`
- **Callers (3):** plan, test_execute_deletes_orphan_pages_and_prunes_manifest, test_execute_runs_reindex_for_files
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+62 more)
### `RepairPlan.has_work`
- **Callers (0):** none
- **Calls:** bool
- **Editing this affects:** none
### `plan`
- **Callers (8):** _run_smart, test_clean_report_produces_empty_plan, test_cleanup_ops_carried_through, test_execute_restores_agents_md, test_missing_wiki_page_pulls_files_from_manifest, test_pages_missing_deep_excluded_when_skip_deep, test_pages_missing_deep_included_when_deep_active, test_stale_and_untracked_files_go_to_reindex
- **Calls:** RepairPlan, add, bool, is_clean, items, list, set, sorted … (+1 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+61 more)
### `execute`
- **Callers (4):** _run_smart, test_execute_deletes_orphan_pages_and_prunes_manifest, test_execute_restores_agents_md, test_execute_runs_reindex_for_files
- **Calls:** _ensure_cache_gitignore, _ensure_nav_guidance, _finalise_index_and_skill, _index_entries_from_manifest, _index_files, compute_hash, current_commit, echo … (+13 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+54 more)
### `_index_entries_from_manifest`
- **Callers (1):** execute
- **Calls:** IndexEntry, append, items, join, setdefault, sorted
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+55 more)
### `_split_id`
- **Callers (1):** scip_symbol
- **Calls:** split
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+65 more)
### `scip_symbol`
- **Callers (9):** file_entry_for, test_class, test_is_deterministic, test_malformed_id_without_separator_is_safe, test_method, test_method_with_dotted_class_path_uses_last_segment_as_member, test_root_level_file, test_top_level_function … (+1 more)
- **Calls:** _split_id, getattr, rpartition
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+64 more)
### `_node_text`
- **Callers (9):** _extract_calls, _extract_doc, _extract_imports, _extract_jsdoc, _get_name, _last_identifier, extract_generic, parse_js_file … (+1 more)
- **Calls:** decode
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_doc, _extract_imports, _extract_jsdoc … (+102 more)
### `_get_name`
- **Callers (4):** _emit_method, extract_generic, parse_js_file, visit
- **Calls:** _node_text, child_by_field_name
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_imports, _finalise_index_and_skill, _index_and_persist … (+98 more)
### `_clean_comment`
- **Callers (1):** _extract_doc
- **Calls:** append, endswith, join, len, lstrip, splitlines, startswith, strip
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_doc, _extract_imports, _finalise_index_and_skill … (+99 more)
### `_doc_anchor`
- **Callers (1):** _extract_doc
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_doc, _extract_imports, _finalise_index_and_skill … (+99 more)
### `_extract_doc`
- **Callers (3):** _emit_method, extract_generic, visit
- **Calls:** _clean_comment, _doc_anchor, _node_text, append, join, next, reverse, startswith … (+1 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_imports, _finalise_index_and_skill, _index_and_persist … (+98 more)
### `_extract_imports`
- **Callers (3):** extract_generic, parse_file, parse_js_file
- **Calls:** _node_text, append, split, visit
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+93 more)
### `_last_identifier`
- **Callers (2):** _extract_calls, visit
- **Calls:** _node_text, reversed, split, strip
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_imports, _finalise_index_and_skill, _index_and_persist … (+98 more)
### `_extract_calls`
- **Callers (4):** _emit_method, parse_file, parse_js_file, visit
- **Calls:** _last_identifier, add, child_by_field_name, list, set, visit
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_imports, _finalise_index_and_skill, _index_and_persist … (+98 more)
### `_load_language`
- **Callers (1):** extract_generic
- **Calls:** Language, __import__, add, getattr, lang_fn, warn
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+92 more)
### `_resolve_class_node`
- **Callers (2):** extract_generic, visit
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_imports, _finalise_index_and_skill, _index_and_persist … (+98 more)
### `_emit_method`
- **Callers (3):** extract_generic, find_methods_in_body, visit
- **Calls:** ASTNode, _extract_calls, _extract_doc, _get_name, append, child_by_field_name
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _extract_calls, _extract_imports, _finalise_index_and_skill, _index_and_persist, _index_files … (+97 more)
### `extract_generic`
- **Callers (1):** parse_file
- **Calls:** ASTNode, Parser, _emit_method, _extract_doc, _extract_imports, _get_name, _load_language, _node_text … (+11 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+91 more)
### `visit`
- **Callers (5):** _extract_calls, _extract_imports, extract_generic, parse_js_file, visit
- **Calls:** _node_text, append, split, visit
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_imports, _finalise_index_and_skill, _index_and_persist … (+98 more)
### `visit`
- **Callers (5):** _extract_calls, _extract_imports, extract_generic, parse_js_file, visit
- **Calls:** _last_identifier, add, child_by_field_name, visit
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_imports, _finalise_index_and_skill, _index_and_persist … (+98 more)
### `find_methods_in_body`
- **Callers (2):** extract_generic, visit
- **Calls:** _emit_method, child_by_field_name
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_imports, _finalise_index_and_skill, _index_and_persist … (+97 more)
### `visit`
- **Callers (5):** _extract_calls, _extract_imports, extract_generic, parse_js_file, visit
- **Calls:** ASTNode, _emit_method, _extract_doc, _get_name, _node_text, _resolve_class_node, append, child_by_field_name … (+3 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _extract_calls, _extract_imports, _finalise_index_and_skill, _index_and_persist … (+98 more)
### `_is_indexable`
- **Callers (4):** _run_smart, run, scan, status
- **Calls:** is_indexable
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+55 more)
### `VerifyReport`
- **Callers (13):** scan, test_clean_report_produces_empty_plan, test_cleanup_ops_carried_through, test_empty_report_is_clean, test_execute_restores_agents_md, test_missing_wiki_page_pulls_files_from_manifest, test_pages_missing_deep_excluded_when_skip_deep, test_pages_missing_deep_included_when_deep_active … (+5 more)
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+66 more)
### `VerifyReport.total_issues`
- **Callers (0):** none
- **Calls:** len
- **Editing this affects:** none
### `VerifyReport.is_clean`
- **Callers (0):** none
- **Calls:** total_issues
- **Editing this affects:** none
### `scan`
- **Callers (17):** _run_smart, test_scan_agents_md_present_and_valid_not_flagged, test_scan_deep_page_with_empty_narrative_not_flagged, test_scan_detects_dangling_manifest_entries, test_scan_detects_hook_drift, test_scan_detects_missing_agents_md_snippet, test_scan_detects_missing_claude_md_snippet, test_scan_detects_missing_gitignore_entry … (+9 more)
- **Calls:** VerifyReport, _is_indexable, all_tracked_files, append, exists, glob, is_git_repo, keys … (+5 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+54 more)
### `print_report`
- **Callers (3):** _run_smart, test_print_report_clean, test_print_report_lists_each_drift
- **Calls:** echo, is_clean, len, total_issues
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+57 more)
### `PageContext`
- **Callers (16):** _index_files, test_build_page_contains_called_by, test_build_page_contains_calls, test_build_page_contains_symbol, test_build_page_no_agent_hints, test_page_body_sections_preserved_below_frontmatter, test_page_frontmatter_description_from_narrative_first_sentence, test_page_frontmatter_description_generic_when_no_narrative … (+8 more)
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+70 more)
### `IndexEntry`
- **Callers (5):** _index_entries_from_manifest, _index_files, test_build_index_contains_page, test_index_frontmatter_has_okf_version, test_index_renders_core_abstractions
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_entries_from_manifest, _index_files, _run … (+59 more)
### `_jinja_env`
- **Callers (2):** build_index, build_page
- **Calls:** Environment, FileSystemLoader, str
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+75 more)
### `_first_sentence`
- **Callers (1):** build_page
- **Calls:** endswith, find, strip
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+71 more)
### `_tags_from_path`
- **Callers (1):** build_page
- **Calls:** add, append, set, split, strip
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+71 more)
### `_short`
- **Callers (2):** _symbol_relationships, build_index
- **Calls:** split
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+76 more)
### `_capped`
- **Callers (1):** _symbol_relationships
- **Calls:** len
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+72 more)
### `_symbol_relationships`
- **Callers (1):** build_page
- **Calls:** _capped, _short, append, get, len, set, sorted
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+71 more)
### `build_page`
- **Callers (16):** _index_files, test_build_page_contains_called_by, test_build_page_contains_calls, test_build_page_contains_symbol, test_build_page_no_agent_hints, test_page_body_sections_preserved_below_frontmatter, test_page_frontmatter_description_from_narrative_first_sentence, test_page_frontmatter_description_generic_when_no_narrative … (+8 more)
- **Calls:** _first_sentence, _jinja_env, _symbol_relationships, _tags_from_path, _yaml_frontmatter, get, get_template, join … (+4 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+70 more)
### `_yaml_frontmatter`
- **Callers (2):** build_index, build_page
- **Calls:** rstrip, safe_dump
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+75 more)
### `build_index`
- **Callers (4):** _finalise_index_and_skill, test_build_index_contains_page, test_index_frontmatter_has_okf_version, test_index_renders_core_abstractions
- **Calls:** _jinja_env, _short, _yaml_frontmatter, get_template, render
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+58 more)
### `page_basename`
- **Callers (4):** page_relpath, test_page_basename_nested_group, test_page_basename_root_group, write_page
- **Calls:** replace, strip
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+61 more)
### `page_relpath`
- **Callers (3):** _index_and_persist, execute, test_page_relpath_matches_write_page
- **Calls:** page_basename
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+56 more)
### `write_page`
- **Callers (3):** _index_files, test_page_relpath_matches_write_page, test_write_page_creates_file
- **Calls:** mkdir, page_basename, write_text
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+57 more)
### `write_index`
- **Callers (1):** _finalise_index_and_skill
- **Calls:** mkdir, write_text
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _run, _run_smart … (+55 more)
## Data Flows
- Pre-commit hook triggers → cli.py:run detects staged_files via git.py → _is_indexable filters → _index_files parses with ast_parser/js_parser → grouper assigns density groups → llm writes wiki pages → manifest.py saves artifact → _finalise_index_and_skill writes INDEX.md + codebase.md
- First-time init: cli.py:init → save_config writes .indexer.toml → install_hook registers pre-commit → _ensure_nav_guidance appends navigation block to CLAUDE.md
- Smart run: cli.py:_run_smart → repair.scan detects issues → repair.execute fixes → _index_and_persist runs full pipeline → synthesize_commit_message summarizes changes → save_manifest persists
- Cache hit path: parse_file → compute_hash_short on file bytes → load_cached_nodes returns deserialized ASTNode list, skipping AST walk entirely → nodes fed directly to grouper/wiki stages
## Design Constraints
- Cache keys are the first 16 chars of SHA256 of raw file bytes — two files with identical content share a cache entry, which is intentional but means renaming a file does not invalidate the cache if content is unchanged.
- changed_files_since returns paths relative to repo root as strings, not Path objects; callers in cli.py must convert before passing to is_indexable or open.
- _index_files uses setdefault to bucket symbols by density group, meaning a file whose group changes between runs will appear in the new bucket only after a full re-index — incremental runs do not remove stale group assignments from the manifest.
- _finalise_index_and_skill calls repo_map which reads the manifest, so save_manifest must be called before _finalise or INDEX.md reflects the previous run's state.
- ASTNode.calls is deduplicated at extraction time (_extract_calls uses a set); ordering is non-deterministic across Python versions — do not rely on call order for dependency graphs.
- The navigation guidance block in CLAUDE.md is gated on a marker string via lstrip+in check; if the user edits CLAUDE.md and removes only the marker (not the block), _ensure_nav_guidance will re-append a duplicate block.
## Relationships
- **Calls:** ASTNode, Anthropic, Config, Environment, Exit, FileEntry, FileSystemLoader, IndexEntry, Language, Manifest, PageContext, Parser, Path, RepairPlan, RuntimeError, UsageError, VerifyReport, __import__, _adjacency, _anthropic_completion, _approx_tokens, _bare_name, _capped, _claude_cli_completion, _claude_cli_path, _clean_comment, _clean_json, _complete, _doc_anchor, _emit_method, _ensure_cache_gitignore, _ensure_nav_guidance, _extract_calls, _extract_doc, _extract_imports, _extract_jsdoc, _finalise_index_and_skill, _first_sentence, _get_class_method_ids, _get_language, _get_name, _hook_command, _hook_script_append, _hook_script_fresh, _index_and_persist, _index_by_id, _index_entries_from_manifest, _index_files, _is_anthropic, _is_indexable, _jinja_env, _last_identifier, _load_language, _node_text, _rel, _resolve_api_key, _resolve_class_node, _run, _run_smart, _short, _split_id, _symbol_relationships, _tags_from_path, _yaml_frontmatter, abs, add, all_tracked_files, any, append, asdict, blast_radius, bool, build_blast_radius_map, build_index, build_page, callees_of, changed_files_since, child_by_field_name, chmod, command, completion, compute_hash, compute_hash_short, create, current_commit, cwd, decode, deep_enrich_index, deep_enrich_page, defaultdict, density_group, deque, describe_files, describe_nodes, discard, dump, dumps, echo, endswith, enumerate, execute, exists, extend, extract_generic, file_entry_for, find, find_methods_in_body, fnmatch, folder_of, get, get_docstring, get_template, getattr, glob, god_nodes, group, has_work, hexdigest, id, install_hook, is_clean, is_git_repo, is_indexable, isinstance, isoformat, isupper, items, join, keys, lang_fn, language, language_tsx, language_typescript, len, list, load, load_cached_nodes, load_config, load_manifest, loads, lower, lstrip, max, mkdir, next, now, open, option, page_basename, page_relpath, pagerank, parse, parse_file, parse_js_file, plan, popleft, prefixes, print_report, range, ranked_symbols, read_bytes, read_text, rel, relative_to, remove_hook, removeprefix, removesuffix, render, replace, repo_map, resolve_group, reverse, reversed, rpartition, rstrip, run, safe_dump, save_cached_nodes, save_config, save_manifest, scan, scip_symbol, search, set, setdefault, sha256, sort, sorted, split, splitlines, staged_files, stale_files, startswith, str, strftime, strip, sum, synthesize_commit_message, total_issues, unlink, update, values, visit, walk, warn, which, write_index, write_page, write_text
- **Called by:** indexer/ast_parser.py::load_cached_nodes, indexer/ast_parser.py::parse_file, indexer/cli.py::_finalise_index_and_skill, indexer/cli.py::_index_and_persist, indexer/cli.py::_index_files, indexer/cli.py::_is_indexable, indexer/cli.py::_run_smart, indexer/cli.py::hook_install, indexer/cli.py::hook_remove, indexer/cli.py::init, indexer/cli.py::run, indexer/cli.py::status, indexer/config.py::load_config, indexer/git.py::_run, indexer/git.py::all_tracked_files, indexer/git.py::changed_files_since, indexer/git.py::current_commit, indexer/git.py::is_git_repo, indexer/git.py::staged_files, indexer/graph.py::blast_radius, indexer/graph.py::build_blast_radius_map, indexer/graph.py::callees_of, indexer/graph.py::callers_of, indexer/graph.py::god_nodes, indexer/graph.py::pagerank, indexer/graph.py::ranked_symbols, indexer/graph.py::repo_map, indexer/grouper.py::density_group, indexer/grouper.py::resolve_group, indexer/hooks.py::_hook_script_append, indexer/hooks.py::_hook_script_fresh, indexer/hooks.py::install_hook, indexer/js_parser.py::_extract_calls, indexer/js_parser.py::_extract_imports, indexer/js_parser.py::_extract_jsdoc, indexer/js_parser.py::_get_name, indexer/js_parser.py::parse_js_file, indexer/js_parser.py::visit, indexer/llm.py::_claude_cli_completion, indexer/llm.py::_complete, indexer/llm.py::deep_enrich_index, indexer/llm.py::deep_enrich_page, indexer/llm.py::describe_files, indexer/llm.py::describe_nodes, indexer/llm.py::synthesize_commit_message, indexer/manifest.py::Manifest.stale_files, indexer/manifest.py::file_entry_for, indexer/manifest.py::load_manifest, indexer/repair.py::_index_entries_from_manifest, indexer/repair.py::execute, indexer/repair.py::plan, indexer/scip.py::scip_symbol, indexer/ts_extract.py::_emit_method, indexer/ts_extract.py::_extract_calls, indexer/ts_extract.py::_extract_doc, indexer/ts_extract.py::_extract_imports, indexer/ts_extract.py::_get_name, indexer/ts_extract.py::_last_identifier, indexer/ts_extract.py::extract_generic, indexer/ts_extract.py::find_methods_in_body, indexer/ts_extract.py::visit, indexer/verify.py::_is_indexable, indexer/verify.py::scan, indexer/wiki.py::_symbol_relationships, indexer/wiki.py::build_index, indexer/wiki.py::build_page, indexer/wiki.py::page_relpath, indexer/wiki.py::write_page, tests/test_ast_parser.py::test_cache_roundtrip, tests/test_ast_parser.py::test_calls_extracted, tests/test_ast_parser.py::test_class_node, tests/test_ast_parser.py::test_docstring_extracted, tests/test_ast_parser.py::test_function_node, tests/test_ast_parser.py::test_imports_extracted, tests/test_ast_parser.py::test_method_node, tests/test_ast_parser.py::test_parse_returns_nodes, tests/test_config.py::test_load_defaults, tests/test_config.py::test_partial_toml_uses_defaults, tests/test_config.py::test_save_and_reload, tests/test_graph.py::_node, tests/test_graph.py::test_blast_radius_diamond, tests/test_graph.py::test_blast_radius_excludes_self, tests/test_graph.py::test_blast_radius_handles_cycles, tests/test_graph.py::test_blast_radius_is_transitive_reverse_reachability, tests/test_graph.py::test_blast_radius_leaf_caller_is_empty, tests/test_graph.py::test_blast_radius_unknown_symbol_is_empty, tests/test_graph.py::test_build_blast_radius_map_keys_every_node, tests/test_graph.py::test_callees_of_resolves_bare_names_to_ids, tests/test_graph.py::test_callees_of_skips_unresolvable_external_names, tests/test_graph.py::test_callers_of_empty_when_no_callers, tests/test_graph.py::test_callers_of_returns_caller_ids, tests/test_graph.py::test_god_nodes_empty_input, tests/test_graph.py::test_god_nodes_n_larger_than_nodes, tests/test_graph.py::test_god_nodes_ranks_by_degree, tests/test_graph.py::test_god_nodes_respects_n, tests/test_graph.py::test_pagerank_empty_input, tests/test_graph.py::test_pagerank_handles_cycles, tests/test_graph.py::test_pagerank_is_deterministic, tests/test_graph.py::test_pagerank_keys_every_node_and_sums_to_one, tests/test_graph.py::test_pagerank_ranks_a_hub_above_leaves, tests/test_graph.py::test_ranked_symbols_empty, tests/test_graph.py::test_ranked_symbols_orders_by_pagerank_desc, tests/test_graph.py::test_repo_map_empty, tests/test_graph.py::test_repo_map_larger_budget_includes_more, tests/test_graph.py::test_repo_map_leads_with_highest_ranked, tests/test_graph.py::test_repo_map_respects_token_budget, tests/test_graph.py::test_repo_map_returns_string, tests/test_grouper.py::test_deep_sparse_merges_upward, tests/test_grouper.py::test_dense_folder_gets_own_page, tests/test_grouper.py::test_different_folders_get_separate_groups, tests/test_grouper.py::test_returns_all_files, tests/test_grouper.py::test_root_files_count_correctly, tests/test_grouper.py::test_root_level_files, tests/test_grouper.py::test_sparse_folders_merge_to_parent, tests/test_init.py::_bootstrap_repo, tests/test_langs.py::test_is_indexable_accepts_known_suffixes, tests/test_langs.py::test_is_indexable_honours_part_glob, tests/test_langs.py::test_is_indexable_honours_path_glob, tests/test_langs.py::test_is_indexable_rejects_unknown_suffix, tests/test_llm_dispatch.py::_cfg, tests/test_llm_dispatch.py::test_claude_cli_completion_invokes_print_mode, tests/test_llm_dispatch.py::test_claude_cli_completion_raises_on_nonzero, tests/test_llm_dispatch.py::test_clean_json_fenced, tests/test_llm_dispatch.py::test_clean_json_list_payload, tests/test_llm_dispatch.py::test_clean_json_plain, tests/test_llm_dispatch.py::test_clean_json_preamble_then_bare_object, tests/test_llm_dispatch.py::test_clean_json_preamble_then_fence, tests/test_llm_dispatch.py::test_clean_json_raises_on_garbage, tests/test_llm_dispatch.py::test_deep_flag_uses_configured_model_cli, tests/test_llm_dispatch.py::test_describe_nodes_uses_cli_path_end_to_end, tests/test_llm_dispatch.py::test_explicit_api_key_takes_priority_over_cli, tests/test_llm_dispatch.py::test_falls_back_to_cli_when_no_key_and_cli_present, tests/test_llm_dispatch.py::test_no_key_no_cli_raises_so_callers_fall_back, tests/test_manifest.py::test_compute_hash_stable, tests/test_manifest.py::test_empty_manifest_on_missing, tests/test_manifest.py::test_fresh_file_not_stale, tests/test_manifest.py::test_load_manifest_missing_component_ids, tests/test_manifest.py::test_save_and_reload, tests/test_manifest.py::test_stale_files_detected, tests/test_multilang.py::test_go_calls, tests/test_multilang.py::test_go_docstring, tests/test_multilang.py::test_go_function, tests/test_multilang.py::test_go_imports, tests/test_multilang.py::test_go_method, tests/test_multilang.py::test_go_struct_is_class, tests/test_multilang.py::test_go_yields_nonzero_symbols, tests/test_multilang.py::test_java_calls, tests/test_multilang.py::test_java_class, tests/test_multilang.py::test_java_docstring, tests/test_multilang.py::test_java_imports, tests/test_multilang.py::test_java_method, tests/test_multilang.py::test_java_static_method, tests/test_multilang.py::test_java_yields_nonzero_symbols, tests/test_multilang.py::test_ruby_calls, tests/test_multilang.py::test_ruby_class_and_module, tests/test_multilang.py::test_ruby_docstring, tests/test_multilang.py::test_ruby_method, tests/test_multilang.py::test_ruby_top_level_function, tests/test_multilang.py::test_ruby_yields_nonzero_symbols, tests/test_multilang.py::test_rust_calls, tests/test_multilang.py::test_rust_docstring, tests/test_multilang.py::test_rust_free_function, tests/test_multilang.py::test_rust_impl_method, tests/test_multilang.py::test_rust_struct_and_trait_are_classes, tests/test_multilang.py::test_rust_yields_nonzero_symbols, tests/test_multilang.py::test_unsupported_suffix_returns_empty, tests/test_repair_plan.py::_empty_manifest, tests/test_repair_plan.py::test_clean_report_produces_empty_plan, tests/test_repair_plan.py::test_cleanup_ops_carried_through, tests/test_repair_plan.py::test_execute_deletes_orphan_pages_and_prunes_manifest, tests/test_repair_plan.py::test_execute_restores_agents_md, tests/test_repair_plan.py::test_execute_runs_reindex_for_files, tests/test_repair_plan.py::test_missing_wiki_page_pulls_files_from_manifest, tests/test_repair_plan.py::test_pages_missing_deep_excluded_when_skip_deep, tests/test_repair_plan.py::test_pages_missing_deep_included_when_deep_active, tests/test_repair_plan.py::test_stale_and_untracked_files_go_to_reindex, tests/test_scip.py::_node, tests/test_scip.py::test_class, tests/test_scip.py::test_is_deterministic, tests/test_scip.py::test_malformed_id_without_separator_is_safe, tests/test_scip.py::test_method, tests/test_scip.py::test_method_with_dotted_class_path_uses_last_segment_as_member, tests/test_scip.py::test_root_level_file, tests/test_scip.py::test_top_level_function, tests/test_scip.py::test_unknown_type_falls_back_to_term, tests/test_smart_integration.py::_bootstrap_repo, tests/test_smart_integration.py::test_smart_bails_when_no_indexable_files, tests/test_smart_integration.py::test_smart_clean_state_is_noop, tests/test_smart_integration.py::test_smart_dry_run_clean_repo_exits_zero, tests/test_smart_integration.py::test_smart_dry_run_does_not_modify_filesystem, tests/test_smart_integration.py::test_smart_dry_run_drift_exits_nonzero, tests/test_smart_integration.py::test_smart_dry_run_reports_full_initial_index_without_changes, tests/test_smart_integration.py::test_smart_fills_fresh_repo_with_no_manifest, tests/test_smart_integration.py::test_smart_fills_never_indexed_tracked_file, tests/test_smart_integration.py::test_smart_repairs_missing_wiki_page, tests/test_verify.py::_make_repo_with_manifest, tests/test_verify.py::_seed_valid_state, tests/test_verify.py::test_empty_report_is_clean, tests/test_verify.py::test_print_report_clean, tests/test_verify.py::test_print_report_lists_each_drift, tests/test_verify.py::test_report_counts_all_drift_classes, tests/test_verify.py::test_report_with_stale_files_not_clean, tests/test_verify.py::test_scan_agents_md_present_and_valid_not_flagged, tests/test_verify.py::test_scan_deep_page_with_empty_narrative_not_flagged, tests/test_verify.py::test_scan_detects_dangling_manifest_entries, tests/test_verify.py::test_scan_detects_hook_drift, tests/test_verify.py::test_scan_detects_missing_agents_md_snippet, tests/test_verify.py::test_scan_detects_missing_claude_md_snippet, tests/test_verify.py::test_scan_detects_missing_gitignore_entry, tests/test_verify.py::test_scan_detects_missing_index_and_skill, tests/test_verify.py::test_scan_detects_missing_wiki_page, tests/test_verify.py::test_scan_detects_orphan_wiki_page, tests/test_verify.py::test_scan_detects_pages_missing_deep_sections, tests/test_verify.py::test_scan_detects_stale_files, tests/test_verify.py::test_scan_detects_untracked_source_files, tests/test_verify.py::test_scan_flags_missing_manifest, tests/test_verify.py::test_scan_skips_deep_check_when_skip_deep_true, tests/test_verify.py::test_scan_skips_hook_check_when_check_hook_false, tests/test_wiki.py::_make_node, tests/test_wiki.py::test_build_index_contains_page, tests/test_wiki.py::test_build_page_contains_called_by, tests/test_wiki.py::test_build_page_contains_calls, tests/test_wiki.py::test_build_page_contains_symbol, tests/test_wiki.py::test_build_page_no_agent_hints, tests/test_wiki.py::test_index_frontmatter_has_okf_version, tests/test_wiki.py::test_index_renders_core_abstractions, tests/test_wiki.py::test_page_basename_nested_group, tests/test_wiki.py::test_page_basename_root_group, tests/test_wiki.py::test_page_body_sections_preserved_below_frontmatter, tests/test_wiki.py::test_page_frontmatter_description_from_narrative_first_sentence, tests/test_wiki.py::test_page_frontmatter_description_generic_when_no_narrative, tests/test_wiki.py::test_page_frontmatter_is_valid_yaml_with_required_type, tests/test_wiki.py::test_page_frontmatter_tags_from_path_segments, tests/test_wiki.py::test_page_frontmatter_timestamp_passed_in_not_computed, tests/test_wiki.py::test_page_frontmatter_title_and_resource, tests/test_wiki.py::test_page_relationships_block_caps_long_lists, tests/test_wiki.py::test_page_relpath_matches_write_page, tests/test_wiki.py::test_page_renders_relationships_block_per_symbol, tests/test_wiki.py::test_page_starts_with_frontmatter_delimiter, tests/test_wiki.py::test_write_page_creates_file
- **Imports from:** __future__.annotations, anthropic, ast, click, collections.defaultdict, collections.deque, dataclasses.asdict, dataclasses.dataclass, dataclasses.field, datetime.datetime, datetime.timezone, fnmatch.fnmatch, hashlib, indexer.ast_parser.ASTNode, indexer.ast_parser.compute_hash_short, indexer.ast_parser.load_cached_nodes, indexer.ast_parser.parse_file, indexer.ast_parser.save_cached_nodes, indexer.cli._ensure_cache_gitignore, indexer.cli._ensure_nav_guidance, indexer.cli._finalise_index_and_skill, indexer.cli._index_files, indexer.config.Config, indexer.config.load_config, indexer.config.save_config, indexer.git.all_tracked_files, indexer.git.changed_files_since, indexer.git.current_commit, indexer.git.is_git_repo, indexer.git.staged_files, indexer.graph.build_blast_radius_map, indexer.graph.god_nodes, indexer.graph.repo_map, indexer.grouper.density_group, indexer.hooks.HOOK_MARKER, indexer.hooks.install_hook, indexer.hooks.remove_hook, indexer.js_parser.parse_js_file, indexer.langs.is_indexable, indexer.llm.deep_enrich_index, indexer.llm.deep_enrich_page, indexer.llm.describe_files, indexer.llm.describe_nodes, indexer.llm.synthesize_commit_message, indexer.manifest.Manifest, indexer.manifest.compute_hash, indexer.manifest.file_entry_for, indexer.manifest.load_manifest, indexer.manifest.save_manifest, indexer.repair, indexer.scip.scip_symbol, indexer.ts_extract.LANG_CONFIGS, indexer.ts_extract.extract_generic, indexer.verify, indexer.verify.VerifyReport, indexer.wiki.IndexEntry, indexer.wiki.PageContext, indexer.wiki.TEMPLATES_DIR, indexer.wiki.build_index, indexer.wiki.build_page, indexer.wiki.page_relpath, indexer.wiki.write_index, indexer.wiki.write_page, jinja2.Environment, jinja2.FileSystemLoader, json, litellm, os, pathlib.Path, re, shutil, subprocess, time, tomli_w, tomllib, tree_sitter.Language, tree_sitter.Parser, tree_sitter_javascript, tree_sitter_typescript, typing.Callable, typing.Optional, warnings, yaml
## Entry Points
- `main`
- `init`
- `status`
- `hook`
- `hook_install`
- `hook_remove`
- `LangConfig`
