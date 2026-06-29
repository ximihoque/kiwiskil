---
type: Code Group
title: indexer
description: The `indexer` module provides an automated observability layer for large
  codebases by transforming raw source code into structured AST-based wiki documentation.
tags:
- indexer
timestamp: '2026-06-29T09:16:51.445490+00:00'
resource: indexer
---
# indexer/
<!-- kiwiskil:deep -->

## Overview

The `indexer` module provides an automated observability layer for large codebases by transforming raw source code into structured AST-based wiki documentation. It solves the context-window limitations of LLMs by generating persistent, searchable knowledge artifacts that track project-level dependencies and logic clusters. The `ASTNode` data class serves as the atomic unit of representation, while the `cli` orchestration layer coordinates git-aware incremental updates to keep documentation synchronized with repository state.

## Modules
| File | Purpose |
|------|---------|
| indexer/js_parser.py | Tree-sitter based AST parsing for JavaScript and TypeScript source files |
| indexer/scip.py | Generation of SCIP descriptors for AST nodes in the codebase |
| indexer/langs.py | Language-specific indexing eligibility and file filtering logic |
| indexer/ts_extract.py | Common tree-sitter extraction utilities for multi-language AST parsing |
| indexer/cli.py | Main entry point for codebase indexing, project initialization, and orchestration |
| indexer/ast_parser.py | AST parsing for Python source code with file-level caching support |
| indexer/graph.py | Graph-based dependency analysis, symbol ranking, and codebase mapping |
| indexer/manifest.py | Persistence layer for tracking code abstractions and source file states |
| indexer/hooks.py | Management of pre-commit hooks to automate codebase index maintenance |
| indexer/git.py | Git repository interaction utilities for identifying file changes |
| indexer/verify.py | Validation logic to check consistency between manifest and filesystem |
| indexer/wiki.py | Wiki page generation with YAML frontmatter and symbol relationship rendering |
| indexer/llm.py | LLM dispatcher for structural code description and indexing enrichments |
| indexer/repair.py | Correction logic for verifying and repairing codebase index drift |
| indexer/config.py | Configuration management for the indexing system via TOML files |
| indexer/grouper.py | Density-based grouping of source files into hierarchical wiki page structures |
## Key Symbols
| ID | Type | Description |
|----|------|-------------|
| `indexer/ast_parser.py::ASTNode` | class | Data class representing a parsed Python symbol with location and structural metadata |
| `indexer/ast_parser.py::_rel` | function | Returns a file path relative to the current working directory as a string |
| `indexer/ast_parser.py::_extract_imports` | function | Parses Python AST to extract all import statements within a source file |
| `indexer/ast_parser.py::_extract_calls` | function | Parses Python AST to collect unique function call names into a list |
| `indexer/ast_parser.py::_get_class_method_ids` | function | Identifies AST node IDs for all functions defined directly within class bodies |
| `indexer/ast_parser.py::parse_file` | function | Analyzes a Python file into ASTNodes, returning empty list on syntax errors |
| `indexer/ast_parser.py::compute_hash_short` | function | Generates a 16-character SHA256 hex digest for caching source file states |
| `indexer/ast_parser.py::load_cached_nodes` | function | Deserializes cached AST nodes from a JSON file into ASTNode objects |
| `indexer/ast_parser.py::save_cached_nodes` | function | Serializes a list of ASTNode objects to a JSON cache file |
| `indexer/cli.py::_ensure_nav_guidance` | function | Idempotently appends navigation guidance markers to a target file |
| `indexer/cli.py::main` | function | Entry point for the CLI command group |
| `indexer/cli.py::init` | function | Configures indexer files, pre-commit hooks, and CLAUDE.md in the current repo |
| `indexer/cli.py::run` | function | Executes indexing pipeline and generates wiki pages for tracked codebase files |
| `indexer/cli.py::status` | function | Reports indexing state, stale files, and current manifest statistics |
| `indexer/cli.py::hook` | function | Group command for managing pre-commit hooks |
| `indexer/cli.py::hook_install` | function | Installs the indexer pre-commit hook into the current repository |
| `indexer/cli.py::hook_remove` | function | Removes the indexer pre-commit hook from the current repository |
| `indexer/cli.py::_ensure_cache_gitignore` | function | Adds indexer cache directory to the root .gitignore file |
| `indexer/cli.py::_is_indexable` | function | Checks if a file satisfies the requirements to be processed by the indexer |
| `indexer/cli.py::_index_files` | function | Runs full indexing pipeline and persists AST cache and wiki pages |
| `indexer/cli.py::_finalise_index_and_skill` | function | Constructs the master index and codebase skill documentation files |
| `indexer/cli.py::_prune_deleted` | function | Removes manifest entries and wiki pages for files no longer in git |
| `indexer/cli.py::_expand_candidates_to_groups` | function | Expands file list to include all members of affected wiki group clusters |
| `indexer/cli.py::_index_and_persist` | function | Orchestrates full indexing pipeline with state management for full or incremental updates |
| `indexer/cli.py::_run_smart` | function | Executes a smart indexing cycle by analyzing git status and pending work |
| `indexer/config.py::Config` | class | Configuration schema for indexer settings |
| `indexer/config.py::load_config` | function | Loads and validates configuration from the project indexer file |
| `indexer/config.py::save_config` | function | Saves indexer configuration to a local YAML file |
| `indexer/git.py::_run` | function | Executes shell commands via git and returns output as a string |
| `indexer/git.py::current_commit` | function | Retrieves the current git commit hash |
| `indexer/git.py::staged_files` | function | Lists all files currently staged in the git index |
| `indexer/git.py::changed_files_since` | function | Retrieves list of modified files since a specific git commit |
| `indexer/git.py::all_tracked_files` | function | Lists every file tracked by git in the repository |
| `indexer/git.py::is_git_repo` | function | Verifies if the current directory is a valid git repository |
| `indexer/graph.py::_index_by_id` | function | Creates a mapping of symbol IDs to their corresponding ASTNode objects |
| `indexer/graph.py::_bare_name` | function | Extracts the base callable name from a fully qualified component ID |
| `indexer/graph.py::callers_of` | function | Retrieves a sorted list of component IDs that call a specific symbol |
| `indexer/graph.py::callees_of` | function | Resolves and sorts all unique component IDs called by a specific symbol |
| `indexer/graph.py::blast_radius` | function | Calculates transitive reverse-reachability for a symbol to identify dependent components |
| `indexer/graph.py::build_blast_radius_map` | function | Precomputes blast radius sets for every node to optimize recurring lookups |
| `indexer/graph.py::god_nodes` | function | Identifies symbols with highest total connectivity degree from caller and callee counts |
| `indexer/graph.py::_adjacency` | function | Constructs a directed caller-to-callee adjacency list for internal component symbols |
| `indexer/graph.py::pagerank` | function | Computes relative node importance using power iteration on the component graph |
| `indexer/graph.py::ranked_symbols` | function | Returns a list of component symbols ordered by PageRank score descending |
| `indexer/graph.py::_approx_tokens` | function | Estimates token count for a string using a character-based heuristic |
| `indexer/graph.py::repo_map` | function | Renders an importance-ranked, token-budgeted overview of the codebase structure |
| `indexer/grouper.py::density_group` | function | Groups file paths into folder-based labels using a density-based merge threshold |
| `indexer/grouper.py::folder_of` | function | Returns the directory path string for a given file system path |
| `indexer/grouper.py::prefixes` | function | Generates a list of ancestor directory prefixes sorted deepest to shallowest |
| `indexer/grouper.py::resolve_group` | function | Determines the appropriate folder group for a file based on subtree density |
| `indexer/hooks.py::_hook_command` | function | Returns the shell command string for the pre-commit hook execution |
| `indexer/hooks.py::_hook_script_fresh` | function | Returns a full shell script block for a new pre-commit hook |
| `indexer/hooks.py::_hook_script_append` | function | Returns a shell command snippet to append to an existing hook file |
| `indexer/hooks.py::install_hook` | function | Installs or updates the pre-commit hook script within the local repository |
| `indexer/hooks.py::remove_hook` | function | Deletes the managed portion of the pre-commit hook file |
| `indexer/js_parser.py::_rel` | function | Returns the path of a file relative to the project root |
| `indexer/js_parser.py::_get_language` | function | Retrieves the appropriate tree-sitter language configuration based on file extension |
| `indexer/js_parser.py::_node_text` | function | Decodes and returns the source code text for a tree-sitter node |
| `indexer/js_parser.py::_extract_jsdoc` | function | Captures JSDoc comment blocks immediately preceding a code node |
| `indexer/js_parser.py::_extract_imports` | function | Parses and collects import declarations within a JavaScript or TypeScript file |
| `indexer/js_parser.py::_extract_calls` | function | Recursively traverses an AST node to collect all function call identifiers |
| `indexer/js_parser.py::_get_name` | function | Extracts the identifier name from a function, class, or method node |
| `indexer/js_parser.py::parse_js_file` | function | Parses a JS/TS file into a list of documented AST nodes |
| `indexer/js_parser.py::visit` | function | Generic recursive walker that identifies and processes specific node types within ASTs |
| `indexer/js_parser.py::visit` | function | Generic recursive walker that identifies and processes specific node types within ASTs |
| `indexer/js_parser.py::visit` | function | Generic recursive walker that identifies and processes specific node types within ASTs |
| `indexer/langs.py::is_indexable` | function | Determines if a file path is indexable based on extensions and ignore patterns |
| `indexer/llm.py::_is_anthropic` | function | Checks if the configured model belongs to the Anthropic provider family |
| `indexer/llm.py::_claude_cli_path` | function | Locates the authenticated local Claude CLI binary if present on system PATH |
| `indexer/llm.py::_claude_cli_completion` | function | Executes a prompt using the local Claude CLI for API-key-free completion |
| `indexer/llm.py::_complete` | function | Dispatches LLM calls to the appropriate provider or local CLI based on availability |
| `indexer/llm.py::_clean_json` | function | Extracts and parses JSON from model responses containing prose or code fences |
| `indexer/llm.py::_resolve_api_key` | function | Resolves API credentials from environment variables or direct provided values |
| `indexer/llm.py::_anthropic_completion` | function | Executes direct Anthropic SDK API calls using provided credentials and returns completion text |
| `indexer/llm.py::describe_nodes` | function | Generates one-line descriptions for AST nodes using LLM-based inference or Anthropic SDK |
| `indexer/llm.py::describe_files` | function | Creates short purpose summaries for source code files using LLM text generation |
| `indexer/llm.py::deep_enrich_page` | function | Produces narrative summaries, data flow lists, and constraints for wiki module documentation |
| `indexer/llm.py::deep_enrich_index` | function | Creates system-wide overview paragraphs and cross-cutting flow documentation for repository index files |
| `indexer/llm.py::synthesize_commit_message` | function | Constructs concise commit messages based on file changes and associated symbol descriptions |
| `indexer/manifest.py::FileEntry` | class | Represents the structural index metadata for a single source code file |
| `indexer/manifest.py::Manifest` | class | Stores and persists the state of indexed files and their structural hashes |
| `indexer/manifest.py::Manifest.stale_files` | method | Identifies source files with outdated hashes compared to current disk versions |
| `indexer/manifest.py::compute_hash` | function | Calculates the SHA-256 hash of a file's content for change tracking |
| `indexer/manifest.py::file_entry_for` | function | Constructs a FileEntry object by extracting AST nodes and SCIP symbols for files |
| `indexer/manifest.py::load_manifest` | function | Deserializes and restores the repository manifest from a JSON storage file |
| `indexer/manifest.py::save_manifest` | function | Serializes and writes the current manifest state to the filesystem |
| `indexer/repair.py::RepairPlan` | class | Defines the scope and nature of required repository indexing or structural repairs |
| `indexer/repair.py::RepairPlan.has_work` | method | Checks whether any pending repair tasks exist in the current plan |
| `indexer/repair.py::plan` | function | Computes minimal repair operations by identifying discrepancies between manifest and filesystem |
| `indexer/repair.py::execute` | function | Applies repair operations to synchronize the filesystem, manifest, and generated documentation |
| `indexer/repair.py::_index_entries_from_manifest` | function | Rebuilds index entry references from existing manifest data for partial index reconstruction |
| `indexer/scip.py::_split_id` | function | Parses a symbol identifier into its relative path and specific symbol component parts |
| `indexer/scip.py::scip_symbol` | function | Generates a standardized SCIP descriptor string for a given AST node |
| `indexer/ts_extract.py::LangConfig` | class | Defines language-specific extraction rules and grammar configurations for code parsing |
| `indexer/ts_extract.py::_node_text` | function | Extracts raw text content from a specific tree-sitter node |
| `indexer/ts_extract.py::_get_name` | function | Retrieves the identifier name associated with a tree-sitter AST node |
| `indexer/ts_extract.py::_clean_comment` | function | Normalizes documentation comments by removing markers and joining contiguous lines |
| `indexer/ts_extract.py::_doc_anchor` | function | Locates the appropriate declaration node associated with preceding documentation comments |
| `indexer/ts_extract.py::_extract_doc` | function | Collects and cleans contiguous comment blocks positioned above source code nodes |
| `indexer/ts_extract.py::_extract_imports` | function | Parses and records import statements within a source code file |
| `indexer/ts_extract.py::_last_identifier` | function | Returns the terminal method or function name from a complex callee expression |
| `indexer/ts_extract.py::_extract_calls` | function | Identifies and extracts function calls made within an AST code scope |
| `indexer/ts_extract.py::_load_language` | function | Loads and configures tree-sitter language grammars for AST analysis |
| `indexer/ts_extract.py::_resolve_class_node` | function | Unwraps nested class or type declarations to reach core specification nodes |
| `indexer/ts_extract.py::_emit_method` | function | Extracts documentation, metadata, and call sites for an individual class method |
| `indexer/ts_extract.py::extract_generic` | function | Parses source files into AST nodes by applying language-specific extraction strategies |
| `indexer/ts_extract.py::visit` | function | Recursively traverses the AST to extract symbols, method definitions, and function call references |
| `indexer/ts_extract.py::visit` | function | Recursively traverses the AST to extract symbols, method definitions, and function call references |
| `indexer/ts_extract.py::find_methods_in_body` | function | Locates and processes all methods defined within a class or module body |
| `indexer/ts_extract.py::visit` | function | Recursively traverses the AST to extract symbols, method definitions, and function call references |
| `indexer/verify.py::_is_indexable` | function | Filters files to determine if they are valid candidates for indexing |
| `indexer/verify.py::VerifyReport` | class | Aggregates issues and state discrepancies discovered during repository verification |
| `indexer/verify.py::VerifyReport.total_issues` | method | Returns the count of all identified drift or validation issues |
| `indexer/verify.py::VerifyReport.is_clean` | method | Determines if the repository state matches the manifest without any discrepancies |
| `indexer/verify.py::scan` | function | Audits the repository for drift by comparing the filesystem against manifest records |
| `indexer/verify.py::print_report` | function | Displays the summary of verification findings to the user console |
| `indexer/wiki.py::PageContext` | class | Maintains contextual information for rendering and managing wiki page generation |
| `indexer/wiki.py::IndexEntry` | class | Data structure representing a single indexed code symbol or documentation entry |
| `indexer/wiki.py::_jinja_env` | function | Configures and returns a Jinja2 environment for rendering wiki documentation templates |
| `indexer/wiki.py::_first_sentence` | function | Extracts the initial sentence of text up to the first period |
| `indexer/wiki.py::_tags_from_path` | function | Parses a group path string into a list of normalized frontmatter tags |
| `indexer/wiki.py::_short` | function | Converts a full component identifier into a concise page-local label |
| `indexer/wiki.py::_capped` | function | Returns a tuple containing the first N items and the remaining item count |
| `indexer/wiki.py::_symbol_relationships` | function | Generates formatted link blocks describing call graphs and symbol influence for pages |
| `indexer/wiki.py::build_page` | function | Generates documentation content for a specific group of code symbols |
| `indexer/wiki.py::_yaml_frontmatter` | function | Serializes a dictionary into a YAML formatted string for document headers |
| `indexer/wiki.py::build_index` | function | Creates the primary wiki index page content using templates |
| `indexer/wiki.py::page_basename` | function | Computes a filesystem-safe filename stem from a given wiki group label |
| `indexer/wiki.py::page_relpath` | function | Determines the repository-relative file path for a generated wiki page |
| `indexer/wiki.py::write_page` | function | Writes a generated markdown page to the project wiki directory |
| `indexer/wiki.py::delete_orphan_pages` | function | Removes wiki files no longer referenced by the current project manifest |
| `indexer/wiki.py::write_index` | function | Writes the main project wiki index file to the disk |
## Symbol Relationships
### `ASTNode`
- **Callers (9):** _emit_method, _make_node, _node, extract_generic, load_cached_nodes, parse_file, parse_js_file, test_describe_nodes_uses_cli_path_end_to_end … (+1 more)
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _chain_nodes, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_imports … (+154 more)
### `_rel`
- **Callers (2):** parse_file, parse_js_file
- **Calls:** relative_to, str
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+98 more)
### `_extract_imports`
- **Callers (3):** extract_generic, parse_file, parse_js_file
- **Calls:** append, isinstance, walk
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+99 more)
### `_extract_calls`
- **Callers (4):** _emit_method, parse_file, parse_js_file, visit
- **Calls:** append, isinstance, list, set, walk
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_imports, _finalise_index_and_skill … (+104 more)
### `_get_class_method_ids`
- **Callers (1):** parse_file
- **Calls:** add, id, isinstance, set, walk
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+97 more)
### `parse_file`
- **Callers (36):** _index_files, test_cache_roundtrip, test_calls_extracted, test_class_node, test_docstring_extracted, test_function_node, test_go_calls, test_go_docstring … (+28 more)
- **Calls:** ASTNode, _extract_calls, _extract_imports, _get_class_method_ids, _rel, append, extract_generic, get … (+9 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+96 more)
### `compute_hash_short`
- **Callers (1):** _index_files
- **Calls:** hexdigest, read_bytes, sha256
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+61 more)
### `load_cached_nodes`
- **Callers (2):** _index_files, test_cache_roundtrip
- **Calls:** ASTNode, exists, loads, read_text
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+62 more)
### `save_cached_nodes`
- **Callers (2):** _index_files, test_cache_roundtrip
- **Calls:** asdict, dumps, mkdir, write_text
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+62 more)
### `_ensure_nav_guidance`
- **Callers (2):** execute, init
- **Calls:** echo, exists, lstrip, read_text, write_text
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+61 more)
### `main`
- **Callers (0):** none
- **Calls:** group
- **Editing this affects:** none
### `init`
- **Callers (0):** none
- **Calls:** _ensure_cache_gitignore, _ensure_nav_guidance, command, cwd, echo, install_hook, is_git_repo, load_config … (+1 more)
- **Editing this affects:** none
### `run`
- **Callers (18):** _bootstrap_repo, _claude_cli_completion, _index_and_persist, _run, is_git_repo, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop … (+10 more)
- **Calls:** UsageError, _ensure_cache_gitignore, _finalise_index_and_skill, _index_and_persist, _index_entries_from_manifest, _is_indexable, _prune_deleted, _run_smart … (+20 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+60 more)
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
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+61 more)
### `_is_indexable`
- **Callers (6):** _expand_candidates_to_groups, _index_files, _run_smart, run, scan, status
- **Calls:** is_indexable
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+61 more)
### `_index_files`
- **Callers (2):** _index_and_persist, execute
- **Calls:** IndexEntry, PageContext, _is_indexable, all_tracked_files, append, build_blast_radius_map, build_page, compute_hash_short … (+28 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _prune_deleted, _run … (+60 more)
### `_finalise_index_and_skill`
- **Callers (3):** _index_and_persist, execute, run
- **Calls:** Environment, FileSystemLoader, build_index, current_commit, deep_enrich_index, echo, get, get_template … (+12 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _index_and_persist, _index_files, _prune_deleted, _run … (+60 more)
### `_prune_deleted`
- **Callers (1):** run
- **Calls:** all_tracked_files, bool, delete_orphan_pages, echo, is_git_repo, set, values
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _run … (+60 more)
### `_expand_candidates_to_groups`
- **Callers (2):** _index_and_persist, execute
- **Calls:** _is_indexable, all_tracked_files, density_group, get, is_git_repo, set, sorted, update
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted, _run … (+60 more)
### `_index_and_persist`
- **Callers (2):** _run_smart, run
- **Calls:** _expand_candidates_to_groups, _finalise_index_and_skill, _index_files, all_tracked_files, compute_hash, current_commit, delete_orphan_pages, echo … (+13 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_files, _prune_deleted, _run … (+60 more)
### `_run_smart`
- **Callers (1):** run
- **Calls:** Exit, _ensure_cache_gitignore, _index_and_persist, _is_indexable, all_tracked_files, echo, execute, has_work … (+6 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+60 more)
### `Config`
- **Callers (30):** _cfg, load_config, test_clean_report_produces_empty_plan, test_cleanup_ops_carried_through, test_execute_deletes_orphan_pages_and_prunes_manifest, test_execute_restores_agents_md, test_execute_runs_reindex_for_files, test_load_defaults … (+22 more)
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _cfg, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files … (+73 more)
### `load_config`
- **Callers (7):** hook_install, init, run, status, test_load_defaults, test_partial_toml_uses_defaults, test_save_and_reload
- **Calls:** Config, exists, get, list, load, open
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+65 more)
### `save_config`
- **Callers (2):** init, test_save_and_reload
- **Calls:** dump, open
- **Editing this affects:** init, test_save_and_reload
### `_run`
- **Callers (4):** all_tracked_files, changed_files_since, current_commit, staged_files
- **Calls:** run, strip
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+60 more)
### `current_commit`
- **Callers (4):** _finalise_index_and_skill, _index_and_persist, execute, run
- **Calls:** _run
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+60 more)
### `staged_files`
- **Callers (1):** run
- **Calls:** _run, splitlines
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+60 more)
### `changed_files_since`
- **Callers (1):** run
- **Calls:** _run, splitlines
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+60 more)
### `all_tracked_files`
- **Callers (8):** _expand_candidates_to_groups, _index_and_persist, _index_files, _prune_deleted, _run_smart, run, scan, status
- **Calls:** _run, splitlines
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+60 more)
### `is_git_repo`
- **Callers (9):** _expand_candidates_to_groups, _index_and_persist, _index_files, _prune_deleted, execute, init, run, scan … (+1 more)
- **Calls:** run
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+60 more)
### `_index_by_id`
- **Callers (4):** blast_radius, callees_of, callers_of, repo_map
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+87 more)
### `_bare_name`
- **Callers (1):** callees_of
- **Calls:** split
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+69 more)
### `callers_of`
- **Callers (2):** test_callers_of_empty_when_no_callers, test_callers_of_returns_caller_ids
- **Calls:** _index_by_id, get, set, sorted
- **Editing this affects:** test_callers_of_empty_when_no_callers, test_callers_of_returns_caller_ids
### `callees_of`
- **Callers (3):** god_nodes, test_callees_of_resolves_bare_names_to_ids, test_callees_of_skips_unresolvable_external_names
- **Calls:** _bare_name, _index_by_id, add, append, get, set, setdefault, sorted
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+68 more)
### `blast_radius`
- **Callers (7):** build_blast_radius_map, test_blast_radius_diamond, test_blast_radius_excludes_self, test_blast_radius_handles_cycles, test_blast_radius_is_transitive_reverse_reachability, test_blast_radius_leaf_caller_is_empty, test_blast_radius_unknown_symbol_is_empty
- **Calls:** _index_by_id, add, append, deque, discard, get, popleft, set
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+69 more)
### `build_blast_radius_map`
- **Callers (2):** _index_files, test_build_blast_radius_map_keys_every_node
- **Calls:** blast_radius
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+62 more)
### `god_nodes`
- **Callers (5):** _finalise_index_and_skill, test_god_nodes_empty_input, test_god_nodes_n_larger_than_nodes, test_god_nodes_ranks_by_degree, test_god_nodes_respects_n
- **Calls:** append, callees_of, len, set, sort
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+65 more)
### `_adjacency`
- **Callers (1):** pagerank
- **Calls:** append, items, set, sorted
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+76 more)
### `pagerank`
- **Callers (6):** ranked_symbols, test_pagerank_empty_input, test_pagerank_handles_cycles, test_pagerank_is_deterministic, test_pagerank_keys_every_node_and_sums_to_one, test_pagerank_ranks_a_hub_above_leaves
- **Calls:** _adjacency, abs, get, len, range, sum, values
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+75 more)
### `ranked_symbols`
- **Callers (3):** repo_map, test_ranked_symbols_empty, test_ranked_symbols_orders_by_pagerank_desc
- **Calls:** pagerank, sorted
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+69 more)
### `_approx_tokens`
- **Callers (1):** repo_map
- **Calls:** len, max
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+67 more)
### `repo_map`
- **Callers (6):** _finalise_index_and_skill, test_repo_map_empty, test_repo_map_larger_budget_includes_more, test_repo_map_leads_with_highest_ranked, test_repo_map_respects_token_budget, test_repo_map_returns_string
- **Calls:** _approx_tokens, _index_by_id, append, get, join, len, ranked_symbols, set
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+66 more)
### `density_group`
- **Callers (10):** _expand_candidates_to_groups, _index_files, scan, test_deep_sparse_merges_upward, test_dense_folder_gets_own_page, test_different_folders_get_separate_groups, test_returns_all_files, test_root_files_count_correctly … (+2 more)
- **Calls:** Path, defaultdict, folder_of, join, len, prefixes, range, resolve_group … (+2 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+68 more)
### `folder_of`
- **Callers (2):** density_group, resolve_group
- **Calls:** Path, str
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+70 more)
### `prefixes`
- **Callers (2):** density_group, resolve_group
- **Calls:** join, len, range, split
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+70 more)
### `resolve_group`
- **Callers (1):** density_group
- **Calls:** folder_of, len, prefixes
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+69 more)
### `_hook_command`
- **Callers (3):** _hook_script_append, _hook_script_fresh, install_hook
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _hook_script_append, _hook_script_fresh, _index_and_persist … (+65 more)
### `_hook_script_fresh`
- **Callers (1):** install_hook
- **Calls:** _hook_command
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+63 more)
### `_hook_script_append`
- **Callers (1):** install_hook
- **Calls:** _hook_command
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+63 more)
### `install_hook`
- **Callers (3):** execute, hook_install, init
- **Calls:** _hook_command, _hook_script_append, _hook_script_fresh, chmod, enumerate, exists, join, mkdir … (+5 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+62 more)
### `remove_hook`
- **Callers (1):** hook_remove
- **Calls:** append, exists, join, read_text, splitlines, strip, unlink, write_text
- **Editing this affects:** hook_remove
### `_rel`
- **Callers (2):** parse_file, parse_js_file
- **Calls:** relative_to, str
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+98 more)
### `_get_language`
- **Callers (1):** parse_js_file
- **Calls:** Language, language, language_tsx, language_typescript
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+98 more)
### `_node_text`
- **Callers (9):** _extract_calls, _extract_doc, _extract_imports, _extract_jsdoc, _get_name, _last_identifier, extract_generic, parse_js_file … (+1 more)
- **Calls:** decode
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_doc, _extract_imports … (+108 more)
### `_extract_jsdoc`
- **Callers (2):** parse_js_file, visit
- **Calls:** _node_text, append, join, lstrip, splitlines, startswith, strip
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_imports, _finalise_index_and_skill … (+104 more)
### `_extract_imports`
- **Callers (3):** extract_generic, parse_file, parse_js_file
- **Calls:** _node_text, append, split, visit, walk
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+99 more)
### `_extract_calls`
- **Callers (4):** _emit_method, parse_file, parse_js_file, visit
- **Calls:** _node_text, add, child_by_field_name, list, set, visit
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_imports, _finalise_index_and_skill … (+104 more)
### `_get_name`
- **Callers (4):** _emit_method, extract_generic, parse_js_file, visit
- **Calls:** _node_text, child_by_field_name
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_imports, _finalise_index_and_skill … (+104 more)
### `parse_js_file`
- **Callers (1):** parse_file
- **Calls:** ASTNode, Parser, _extract_calls, _extract_imports, _extract_jsdoc, _get_language, _get_name, _node_text … (+9 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+97 more)
### `visit`
- **Callers (5):** _extract_calls, _extract_imports, extract_generic, parse_js_file, visit
- **Calls:** _node_text, append, split, visit
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_imports, _finalise_index_and_skill … (+104 more)
### `visit`
- **Callers (5):** _extract_calls, _extract_imports, extract_generic, parse_js_file, visit
- **Calls:** _node_text, add, child_by_field_name, visit
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_imports, _finalise_index_and_skill … (+104 more)
### `visit`
- **Callers (5):** _extract_calls, _extract_imports, extract_generic, parse_js_file, visit
- **Calls:** ASTNode, _extract_calls, _extract_jsdoc, _get_name, _node_text, append, child_by_field_name, list … (+1 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_imports, _finalise_index_and_skill … (+104 more)
### `is_indexable`
- **Callers (5):** _is_indexable, test_is_indexable_accepts_known_suffixes, test_is_indexable_honours_part_glob, test_is_indexable_honours_path_glob, test_is_indexable_rejects_unknown_suffix
- **Calls:** Path, any, fnmatch
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _is_indexable … (+66 more)
### `_is_anthropic`
- **Callers (1):** _complete
- **Calls:** any, startswith
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+61 more)
### `_claude_cli_path`
- **Callers (2):** _claude_cli_completion, _complete
- **Calls:** which
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+61 more)
### `_claude_cli_completion`
- **Callers (3):** _complete, test_claude_cli_completion_invokes_print_mode, test_claude_cli_completion_raises_on_nonzero
- **Calls:** RuntimeError, _claude_cli_path, removeprefix, run, strip
- **Editing this affects:** _bootstrap_repo, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted, _run … (+60 more)
### `_complete`
- **Callers (9):** deep_enrich_index, deep_enrich_page, describe_files, describe_nodes, synthesize_commit_message, test_deep_flag_uses_configured_model_cli, test_explicit_api_key_takes_priority_over_cli, test_falls_back_to_cli_when_no_key_and_cli_present … (+1 more)
- **Calls:** RuntimeError, _anthropic_completion, _claude_cli_completion, _claude_cli_path, _is_anthropic, _resolve_api_key, completion
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted, _run … (+60 more)
### `_clean_json`
- **Callers (10):** deep_enrich_index, deep_enrich_page, describe_files, describe_nodes, test_clean_json_fenced, test_clean_json_list_payload, test_clean_json_plain, test_clean_json_preamble_then_bare_object … (+2 more)
- **Calls:** append, find, group, len, loads, range, removeprefix, removesuffix … (+3 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+67 more)
### `_resolve_api_key`
- **Callers (1):** _complete
- **Calls:** get, isupper, replace
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+61 more)
### `_anthropic_completion`
- **Callers (1):** _complete
- **Calls:** Anthropic, create, removeprefix
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+61 more)
### `describe_nodes`
- **Callers (2):** _index_files, test_describe_nodes_uses_cli_path_end_to_end
- **Calls:** _clean_json, _complete, dumps, get, isinstance, warn
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+60 more)
### `describe_files`
- **Callers (1):** _index_files
- **Calls:** _clean_json, _complete, dumps, get, isinstance, items, split, warn
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+60 more)
### `deep_enrich_page`
- **Callers (1):** _index_files
- **Calls:** _clean_json, _complete, dumps, get, isinstance, warn
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+60 more)
### `deep_enrich_index`
- **Callers (1):** _finalise_index_and_skill
- **Calls:** _clean_json, _complete, dumps, get, isinstance, warn
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+60 more)
### `synthesize_commit_message`
- **Callers (1):** _index_and_persist
- **Calls:** _complete, dumps, isinstance, strip, warn
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+60 more)
### `FileEntry`
- **Callers (27):** _seed_valid_state, file_entry_for, load_manifest, test_execute_deletes_orphan_pages_and_prunes_manifest, test_fresh_file_not_stale, test_missing_wiki_page_pulls_files_from_manifest, test_pages_missing_deep_excluded_when_skip_deep, test_pages_missing_deep_included_when_deep_active … (+19 more)
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+72 more)
### `Manifest`
- **Callers (27):** _empty_manifest, _make_repo_with_manifest, _seed_valid_state, load_manifest, test_execute_deletes_orphan_pages_and_prunes_manifest, test_execute_runs_reindex_for_files, test_fresh_file_not_stale, test_missing_wiki_page_pulls_files_from_manifest … (+19 more)
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _empty_manifest, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files … (+76 more)
### `Manifest.stale_files`
- **Callers (0):** none
- **Calls:** append, compute_hash, exists, get
- **Editing this affects:** none
### `compute_hash`
- **Callers (18):** Manifest.stale_files, _index_and_persist, _seed_valid_state, execute, test_compute_hash_stable, test_fresh_file_not_stale, test_scan_deep_page_with_empty_narrative_not_flagged, test_scan_detects_missing_index_and_skill … (+10 more)
- **Calls:** hexdigest, read_bytes, sha256
- **Editing this affects:** Manifest.stale_files, _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files … (+65 more)
### `file_entry_for`
- **Callers (2):** _index_and_persist, execute
- **Calls:** FileEntry, scip_symbol
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+61 more)
### `load_manifest`
- **Callers (8):** run, status, test_empty_manifest_on_missing, test_load_manifest_missing_component_ids, test_run_deletes_orphan_page_when_source_deleted, test_save_and_reload, test_smart_fills_fresh_repo_with_no_manifest, test_smart_fills_never_indexed_tracked_file
- **Calls:** FileEntry, Manifest, exists, get, items, loads, read_text
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+64 more)
### `save_manifest`
- **Callers (12):** _index_and_persist, execute, run, test_save_and_reload, test_smart_clean_state_is_noop, test_smart_does_not_delete_pages_for_untouched_groups, test_smart_dry_run_clean_repo_exits_zero, test_smart_dry_run_does_not_modify_filesystem … (+4 more)
- **Calls:** asdict, dumps, items, mkdir, write_text
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+62 more)
### `RepairPlan`
- **Callers (3):** plan, test_execute_deletes_orphan_pages_and_prunes_manifest, test_execute_runs_reindex_for_files
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+68 more)
### `RepairPlan.has_work`
- **Callers (0):** none
- **Calls:** bool
- **Editing this affects:** none
### `plan`
- **Callers (8):** _run_smart, test_clean_report_produces_empty_plan, test_cleanup_ops_carried_through, test_execute_restores_agents_md, test_missing_wiki_page_pulls_files_from_manifest, test_pages_missing_deep_excluded_when_skip_deep, test_pages_missing_deep_included_when_deep_active, test_stale_and_untracked_files_go_to_reindex
- **Calls:** RepairPlan, add, bool, is_clean, items, list, set, sorted … (+1 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+67 more)
### `execute`
- **Callers (4):** _run_smart, test_execute_deletes_orphan_pages_and_prunes_manifest, test_execute_restores_agents_md, test_execute_runs_reindex_for_files
- **Calls:** _ensure_cache_gitignore, _ensure_nav_guidance, _expand_candidates_to_groups, _finalise_index_and_skill, _index_entries_from_manifest, _index_files, compute_hash, current_commit … (+14 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+60 more)
### `_index_entries_from_manifest`
- **Callers (2):** execute, run
- **Calls:** IndexEntry, append, items, join, setdefault, sorted
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+61 more)
### `_split_id`
- **Callers (1):** scip_symbol
- **Calls:** split
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+71 more)
### `scip_symbol`
- **Callers (9):** file_entry_for, test_class, test_is_deterministic, test_malformed_id_without_separator_is_safe, test_method, test_method_with_dotted_class_path_uses_last_segment_as_member, test_root_level_file, test_top_level_function … (+1 more)
- **Calls:** _split_id, getattr, rpartition
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+70 more)
### `_node_text`
- **Callers (9):** _extract_calls, _extract_doc, _extract_imports, _extract_jsdoc, _get_name, _last_identifier, extract_generic, parse_js_file … (+1 more)
- **Calls:** decode
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_doc, _extract_imports … (+108 more)
### `_get_name`
- **Callers (4):** _emit_method, extract_generic, parse_js_file, visit
- **Calls:** _node_text, child_by_field_name
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_imports, _finalise_index_and_skill … (+104 more)
### `_clean_comment`
- **Callers (1):** _extract_doc
- **Calls:** append, endswith, join, len, lstrip, splitlines, startswith, strip
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_doc, _extract_imports … (+105 more)
### `_doc_anchor`
- **Callers (1):** _extract_doc
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_doc, _extract_imports … (+105 more)
### `_extract_doc`
- **Callers (3):** _emit_method, extract_generic, visit
- **Calls:** _clean_comment, _doc_anchor, _node_text, append, join, next, reverse, startswith … (+1 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_imports, _finalise_index_and_skill … (+104 more)
### `_extract_imports`
- **Callers (3):** extract_generic, parse_file, parse_js_file
- **Calls:** _node_text, append, split, visit
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+99 more)
### `_last_identifier`
- **Callers (2):** _extract_calls, visit
- **Calls:** _node_text, reversed, split, strip
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_imports, _finalise_index_and_skill … (+104 more)
### `_extract_calls`
- **Callers (4):** _emit_method, parse_file, parse_js_file, visit
- **Calls:** _last_identifier, add, child_by_field_name, list, set, visit
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_imports, _finalise_index_and_skill … (+104 more)
### `_load_language`
- **Callers (1):** extract_generic
- **Calls:** Language, __import__, add, getattr, lang_fn, warn
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+98 more)
### `_resolve_class_node`
- **Callers (2):** extract_generic, visit
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_imports, _finalise_index_and_skill … (+104 more)
### `_emit_method`
- **Callers (3):** extract_generic, find_methods_in_body, visit
- **Calls:** ASTNode, _extract_calls, _extract_doc, _get_name, append, child_by_field_name
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _extract_calls, _extract_imports, _finalise_index_and_skill, _index_and_persist … (+103 more)
### `extract_generic`
- **Callers (1):** parse_file
- **Calls:** ASTNode, Parser, _emit_method, _extract_doc, _extract_imports, _get_name, _load_language, _node_text … (+11 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+97 more)
### `visit`
- **Callers (5):** _extract_calls, _extract_imports, extract_generic, parse_js_file, visit
- **Calls:** _node_text, append, split, visit
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_imports, _finalise_index_and_skill … (+104 more)
### `visit`
- **Callers (5):** _extract_calls, _extract_imports, extract_generic, parse_js_file, visit
- **Calls:** _last_identifier, add, child_by_field_name, visit
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_imports, _finalise_index_and_skill … (+104 more)
### `find_methods_in_body`
- **Callers (2):** extract_generic, visit
- **Calls:** _emit_method, child_by_field_name
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_imports, _finalise_index_and_skill … (+103 more)
### `visit`
- **Callers (5):** _extract_calls, _extract_imports, extract_generic, parse_js_file, visit
- **Calls:** ASTNode, _emit_method, _extract_doc, _get_name, _node_text, _resolve_class_node, append, child_by_field_name … (+3 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _emit_method, _expand_candidates_to_groups, _extract_calls, _extract_imports, _finalise_index_and_skill … (+104 more)
### `_is_indexable`
- **Callers (6):** _expand_candidates_to_groups, _index_files, _run_smart, run, scan, status
- **Calls:** is_indexable
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+61 more)
### `VerifyReport`
- **Callers (13):** scan, test_clean_report_produces_empty_plan, test_cleanup_ops_carried_through, test_empty_report_is_clean, test_execute_restores_agents_md, test_missing_wiki_page_pulls_files_from_manifest, test_pages_missing_deep_excluded_when_skip_deep, test_pages_missing_deep_included_when_deep_active … (+5 more)
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+72 more)
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
- **Calls:** VerifyReport, _is_indexable, all_tracked_files, append, density_group, exists, glob, is_git_repo … (+7 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+60 more)
### `print_report`
- **Callers (3):** _run_smart, test_print_report_clean, test_print_report_lists_each_drift
- **Calls:** echo, is_clean, len, total_issues
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+63 more)
### `PageContext`
- **Callers (16):** _index_files, test_build_page_contains_called_by, test_build_page_contains_calls, test_build_page_contains_symbol, test_build_page_no_agent_hints, test_page_body_sections_preserved_below_frontmatter, test_page_frontmatter_description_from_narrative_first_sentence, test_page_frontmatter_description_generic_when_no_narrative … (+8 more)
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+76 more)
### `IndexEntry`
- **Callers (5):** _index_entries_from_manifest, _index_files, test_build_index_contains_page, test_index_frontmatter_has_okf_version, test_index_renders_core_abstractions
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_entries_from_manifest, _index_files … (+65 more)
### `_jinja_env`
- **Callers (2):** build_index, build_page
- **Calls:** Environment, FileSystemLoader, str
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+81 more)
### `_first_sentence`
- **Callers (1):** build_page
- **Calls:** endswith, find, strip
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+77 more)
### `_tags_from_path`
- **Callers (1):** build_page
- **Calls:** add, append, set, split, strip
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+77 more)
### `_short`
- **Callers (2):** _symbol_relationships, build_index
- **Calls:** split
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+82 more)
### `_capped`
- **Callers (1):** _symbol_relationships
- **Calls:** len
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+78 more)
### `_symbol_relationships`
- **Callers (1):** build_page
- **Calls:** _capped, _short, append, get, len, set, sorted
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+77 more)
### `build_page`
- **Callers (16):** _index_files, test_build_page_contains_called_by, test_build_page_contains_calls, test_build_page_contains_symbol, test_build_page_no_agent_hints, test_page_body_sections_preserved_below_frontmatter, test_page_frontmatter_description_from_narrative_first_sentence, test_page_frontmatter_description_generic_when_no_narrative … (+8 more)
- **Calls:** _first_sentence, _jinja_env, _symbol_relationships, _tags_from_path, _yaml_frontmatter, get, get_template, join … (+4 more)
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+76 more)
### `_yaml_frontmatter`
- **Callers (2):** build_index, build_page
- **Calls:** rstrip, safe_dump
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+81 more)
### `build_index`
- **Callers (4):** _finalise_index_and_skill, test_build_index_contains_page, test_index_frontmatter_has_okf_version, test_index_renders_core_abstractions
- **Calls:** _jinja_env, _short, _yaml_frontmatter, get_template, render
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+64 more)
### `page_basename`
- **Callers (4):** page_relpath, test_page_basename_nested_group, test_page_basename_root_group, write_page
- **Calls:** replace, strip
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+67 more)
### `page_relpath`
- **Callers (4):** _index_and_persist, execute, scan, test_page_relpath_matches_write_page
- **Calls:** page_basename
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+62 more)
### `write_page`
- **Callers (3):** _index_files, test_page_relpath_matches_write_page, test_write_page_creates_file
- **Calls:** mkdir, page_basename, write_text
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+63 more)
### `delete_orphan_pages`
- **Callers (5):** _index_and_persist, _prune_deleted, test_delete_orphan_pages_missing_wiki_dir, test_delete_orphan_pages_noop_when_all_referenced, test_delete_orphan_pages_removes_unreferenced
- **Calls:** exists, glob, sorted, unlink
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+64 more)
### `write_index`
- **Callers (1):** _finalise_index_and_skill
- **Calls:** mkdir, write_text
- **Editing this affects:** _bootstrap_repo, _claude_cli_completion, _complete, _expand_candidates_to_groups, _finalise_index_and_skill, _index_and_persist, _index_files, _prune_deleted … (+61 more)
## Data Flows
- CLI command execution → `ast_parser` extracts nodes → `cli` persists AST cache and wiki pages.
- Git change detection → `_expand_candidates_to_groups` identifies impact clusters → `_index_files` regenerates only affected pages.
- Config load → `git` checks status → `_prune_deleted` removes orphaned documentation files.
## Design Constraints
- The `parse_file` function returns an empty list upon encountering any syntax error, rather than raising an exception.
- Cached AST nodes are stored as JSON files; manual modification of these files may result in deserialization errors or corrupted index states.
- The `_ensure_nav_guidance` method is idempotent and should be called whenever initializing a repo to ensure CLAUDE.md integrity.
- File tracking is strictly dependent on the existence of a `.git` repository; operations requiring `is_git_repo` will fail in detached environments.
- The system performs grouping based on logic density; file membership in a group is determined by `density_group` and cannot be manually overridden.
## Relationships
- **Calls:** ASTNode, Anthropic, Config, Environment, Exit, FileEntry, FileSystemLoader, IndexEntry, Language, Manifest, PageContext, Parser, Path, RepairPlan, RuntimeError, UsageError, VerifyReport, __import__, _adjacency, _anthropic_completion, _approx_tokens, _bare_name, _capped, _claude_cli_completion, _claude_cli_path, _clean_comment, _clean_json, _complete, _doc_anchor, _emit_method, _ensure_cache_gitignore, _ensure_nav_guidance, _expand_candidates_to_groups, _extract_calls, _extract_doc, _extract_imports, _extract_jsdoc, _finalise_index_and_skill, _first_sentence, _get_class_method_ids, _get_language, _get_name, _hook_command, _hook_script_append, _hook_script_fresh, _index_and_persist, _index_by_id, _index_entries_from_manifest, _index_files, _is_anthropic, _is_indexable, _jinja_env, _last_identifier, _load_language, _node_text, _prune_deleted, _rel, _resolve_api_key, _resolve_class_node, _run, _run_smart, _short, _split_id, _symbol_relationships, _tags_from_path, _yaml_frontmatter, abs, add, all_tracked_files, any, append, asdict, blast_radius, bool, build_blast_radius_map, build_index, build_page, callees_of, changed_files_since, child_by_field_name, chmod, command, completion, compute_hash, compute_hash_short, create, current_commit, cwd, decode, deep_enrich_index, deep_enrich_page, defaultdict, delete_orphan_pages, density_group, deque, describe_files, describe_nodes, discard, dump, dumps, echo, endswith, enumerate, execute, exists, extend, extract_generic, file_entry_for, find, find_methods_in_body, fnmatch, folder_of, get, get_docstring, get_template, getattr, glob, god_nodes, group, has_work, hexdigest, id, install_hook, is_clean, is_git_repo, is_indexable, isinstance, isoformat, isupper, items, join, keys, lang_fn, language, language_tsx, language_typescript, len, list, load, load_cached_nodes, load_config, load_manifest, loads, lower, lstrip, max, mkdir, next, now, open, option, page_basename, page_relpath, pagerank, parse, parse_file, parse_js_file, plan, popleft, prefixes, print_report, range, ranked_symbols, read_bytes, read_text, rel, relative_to, remove_hook, removeprefix, removesuffix, render, replace, repo_map, resolve_group, reverse, reversed, rpartition, rstrip, run, safe_dump, save_cached_nodes, save_config, save_manifest, scan, scip_symbol, search, set, setdefault, sha256, sort, sorted, split, splitlines, staged_files, stale_files, startswith, str, strftime, strip, sum, synthesize_commit_message, total_issues, unlink, update, values, visit, walk, warn, which, write_index, write_page, write_text
- **Called by:** indexer/ast_parser.py::load_cached_nodes, indexer/ast_parser.py::parse_file, indexer/cli.py::_expand_candidates_to_groups, indexer/cli.py::_finalise_index_and_skill, indexer/cli.py::_index_and_persist, indexer/cli.py::_index_files, indexer/cli.py::_is_indexable, indexer/cli.py::_prune_deleted, indexer/cli.py::_run_smart, indexer/cli.py::hook_install, indexer/cli.py::hook_remove, indexer/cli.py::init, indexer/cli.py::run, indexer/cli.py::status, indexer/config.py::load_config, indexer/git.py::_run, indexer/git.py::all_tracked_files, indexer/git.py::changed_files_since, indexer/git.py::current_commit, indexer/git.py::is_git_repo, indexer/git.py::staged_files, indexer/graph.py::blast_radius, indexer/graph.py::build_blast_radius_map, indexer/graph.py::callees_of, indexer/graph.py::callers_of, indexer/graph.py::god_nodes, indexer/graph.py::pagerank, indexer/graph.py::ranked_symbols, indexer/graph.py::repo_map, indexer/grouper.py::density_group, indexer/grouper.py::resolve_group, indexer/hooks.py::_hook_script_append, indexer/hooks.py::_hook_script_fresh, indexer/hooks.py::install_hook, indexer/js_parser.py::_extract_calls, indexer/js_parser.py::_extract_imports, indexer/js_parser.py::_extract_jsdoc, indexer/js_parser.py::_get_name, indexer/js_parser.py::parse_js_file, indexer/js_parser.py::visit, indexer/llm.py::_claude_cli_completion, indexer/llm.py::_complete, indexer/llm.py::deep_enrich_index, indexer/llm.py::deep_enrich_page, indexer/llm.py::describe_files, indexer/llm.py::describe_nodes, indexer/llm.py::synthesize_commit_message, indexer/manifest.py::Manifest.stale_files, indexer/manifest.py::file_entry_for, indexer/manifest.py::load_manifest, indexer/repair.py::_index_entries_from_manifest, indexer/repair.py::execute, indexer/repair.py::plan, indexer/scip.py::scip_symbol, indexer/ts_extract.py::_emit_method, indexer/ts_extract.py::_extract_calls, indexer/ts_extract.py::_extract_doc, indexer/ts_extract.py::_extract_imports, indexer/ts_extract.py::_get_name, indexer/ts_extract.py::_last_identifier, indexer/ts_extract.py::extract_generic, indexer/ts_extract.py::find_methods_in_body, indexer/ts_extract.py::visit, indexer/verify.py::_is_indexable, indexer/verify.py::scan, indexer/wiki.py::_symbol_relationships, indexer/wiki.py::build_index, indexer/wiki.py::build_page, indexer/wiki.py::page_relpath, indexer/wiki.py::write_page, tests/test_ast_parser.py::test_cache_roundtrip, tests/test_ast_parser.py::test_calls_extracted, tests/test_ast_parser.py::test_class_node, tests/test_ast_parser.py::test_docstring_extracted, tests/test_ast_parser.py::test_function_node, tests/test_ast_parser.py::test_imports_extracted, tests/test_ast_parser.py::test_method_node, tests/test_ast_parser.py::test_parse_returns_nodes, tests/test_config.py::test_load_defaults, tests/test_config.py::test_partial_toml_uses_defaults, tests/test_config.py::test_save_and_reload, tests/test_graph.py::_node, tests/test_graph.py::test_blast_radius_diamond, tests/test_graph.py::test_blast_radius_excludes_self, tests/test_graph.py::test_blast_radius_handles_cycles, tests/test_graph.py::test_blast_radius_is_transitive_reverse_reachability, tests/test_graph.py::test_blast_radius_leaf_caller_is_empty, tests/test_graph.py::test_blast_radius_unknown_symbol_is_empty, tests/test_graph.py::test_build_blast_radius_map_keys_every_node, tests/test_graph.py::test_callees_of_resolves_bare_names_to_ids, tests/test_graph.py::test_callees_of_skips_unresolvable_external_names, tests/test_graph.py::test_callers_of_empty_when_no_callers, tests/test_graph.py::test_callers_of_returns_caller_ids, tests/test_graph.py::test_god_nodes_empty_input, tests/test_graph.py::test_god_nodes_n_larger_than_nodes, tests/test_graph.py::test_god_nodes_ranks_by_degree, tests/test_graph.py::test_god_nodes_respects_n, tests/test_graph.py::test_pagerank_empty_input, tests/test_graph.py::test_pagerank_handles_cycles, tests/test_graph.py::test_pagerank_is_deterministic, tests/test_graph.py::test_pagerank_keys_every_node_and_sums_to_one, tests/test_graph.py::test_pagerank_ranks_a_hub_above_leaves, tests/test_graph.py::test_ranked_symbols_empty, tests/test_graph.py::test_ranked_symbols_orders_by_pagerank_desc, tests/test_graph.py::test_repo_map_empty, tests/test_graph.py::test_repo_map_larger_budget_includes_more, tests/test_graph.py::test_repo_map_leads_with_highest_ranked, tests/test_graph.py::test_repo_map_respects_token_budget, tests/test_graph.py::test_repo_map_returns_string, tests/test_grouper.py::test_deep_sparse_merges_upward, tests/test_grouper.py::test_dense_folder_gets_own_page, tests/test_grouper.py::test_different_folders_get_separate_groups, tests/test_grouper.py::test_returns_all_files, tests/test_grouper.py::test_root_files_count_correctly, tests/test_grouper.py::test_root_level_files, tests/test_grouper.py::test_sparse_folders_merge_to_parent, tests/test_init.py::_bootstrap_repo, tests/test_langs.py::test_is_indexable_accepts_known_suffixes, tests/test_langs.py::test_is_indexable_honours_part_glob, tests/test_langs.py::test_is_indexable_honours_path_glob, tests/test_langs.py::test_is_indexable_rejects_unknown_suffix, tests/test_llm_dispatch.py::_cfg, tests/test_llm_dispatch.py::test_claude_cli_completion_invokes_print_mode, tests/test_llm_dispatch.py::test_claude_cli_completion_raises_on_nonzero, tests/test_llm_dispatch.py::test_clean_json_fenced, tests/test_llm_dispatch.py::test_clean_json_list_payload, tests/test_llm_dispatch.py::test_clean_json_plain, tests/test_llm_dispatch.py::test_clean_json_preamble_then_bare_object, tests/test_llm_dispatch.py::test_clean_json_preamble_then_fence, tests/test_llm_dispatch.py::test_clean_json_raises_on_garbage, tests/test_llm_dispatch.py::test_deep_flag_uses_configured_model_cli, tests/test_llm_dispatch.py::test_describe_nodes_uses_cli_path_end_to_end, tests/test_llm_dispatch.py::test_explicit_api_key_takes_priority_over_cli, tests/test_llm_dispatch.py::test_falls_back_to_cli_when_no_key_and_cli_present, tests/test_llm_dispatch.py::test_no_key_no_cli_raises_so_callers_fall_back, tests/test_manifest.py::test_compute_hash_stable, tests/test_manifest.py::test_empty_manifest_on_missing, tests/test_manifest.py::test_fresh_file_not_stale, tests/test_manifest.py::test_load_manifest_missing_component_ids, tests/test_manifest.py::test_save_and_reload, tests/test_manifest.py::test_stale_files_detected, tests/test_multilang.py::test_go_calls, tests/test_multilang.py::test_go_docstring, tests/test_multilang.py::test_go_function, tests/test_multilang.py::test_go_imports, tests/test_multilang.py::test_go_method, tests/test_multilang.py::test_go_struct_is_class, tests/test_multilang.py::test_go_yields_nonzero_symbols, tests/test_multilang.py::test_java_calls, tests/test_multilang.py::test_java_class, tests/test_multilang.py::test_java_docstring, tests/test_multilang.py::test_java_imports, tests/test_multilang.py::test_java_method, tests/test_multilang.py::test_java_static_method, tests/test_multilang.py::test_java_yields_nonzero_symbols, tests/test_multilang.py::test_ruby_calls, tests/test_multilang.py::test_ruby_class_and_module, tests/test_multilang.py::test_ruby_docstring, tests/test_multilang.py::test_ruby_method, tests/test_multilang.py::test_ruby_top_level_function, tests/test_multilang.py::test_ruby_yields_nonzero_symbols, tests/test_multilang.py::test_rust_calls, tests/test_multilang.py::test_rust_docstring, tests/test_multilang.py::test_rust_free_function, tests/test_multilang.py::test_rust_impl_method, tests/test_multilang.py::test_rust_struct_and_trait_are_classes, tests/test_multilang.py::test_rust_yields_nonzero_symbols, tests/test_multilang.py::test_unsupported_suffix_returns_empty, tests/test_repair_plan.py::_empty_manifest, tests/test_repair_plan.py::test_clean_report_produces_empty_plan, tests/test_repair_plan.py::test_cleanup_ops_carried_through, tests/test_repair_plan.py::test_execute_deletes_orphan_pages_and_prunes_manifest, tests/test_repair_plan.py::test_execute_restores_agents_md, tests/test_repair_plan.py::test_execute_runs_reindex_for_files, tests/test_repair_plan.py::test_missing_wiki_page_pulls_files_from_manifest, tests/test_repair_plan.py::test_pages_missing_deep_excluded_when_skip_deep, tests/test_repair_plan.py::test_pages_missing_deep_included_when_deep_active, tests/test_repair_plan.py::test_stale_and_untracked_files_go_to_reindex, tests/test_scip.py::_node, tests/test_scip.py::test_class, tests/test_scip.py::test_is_deterministic, tests/test_scip.py::test_malformed_id_without_separator_is_safe, tests/test_scip.py::test_method, tests/test_scip.py::test_method_with_dotted_class_path_uses_last_segment_as_member, tests/test_scip.py::test_root_level_file, tests/test_scip.py::test_top_level_function, tests/test_scip.py::test_unknown_type_falls_back_to_term, tests/test_smart_integration.py::_bootstrap_repo, tests/test_smart_integration.py::test_run_deletes_orphan_page_when_source_deleted, tests/test_smart_integration.py::test_smart_bails_when_no_indexable_files, tests/test_smart_integration.py::test_smart_clean_state_is_noop, tests/test_smart_integration.py::test_smart_does_not_delete_pages_for_untouched_groups, tests/test_smart_integration.py::test_smart_dry_run_clean_repo_exits_zero, tests/test_smart_integration.py::test_smart_dry_run_does_not_modify_filesystem, tests/test_smart_integration.py::test_smart_dry_run_drift_exits_nonzero, tests/test_smart_integration.py::test_smart_dry_run_reports_full_initial_index_without_changes, tests/test_smart_integration.py::test_smart_fills_fresh_repo_with_no_manifest, tests/test_smart_integration.py::test_smart_fills_never_indexed_tracked_file, tests/test_smart_integration.py::test_smart_repairs_missing_wiki_page, tests/test_smart_integration.py::test_staged_run_does_not_delete_pages_for_unstaged_files, tests/test_smart_integration.py::test_staged_subset_does_not_regroup_whole_wiki, tests/test_verify.py::_make_repo_with_manifest, tests/test_verify.py::_seed_valid_state, tests/test_verify.py::test_empty_report_is_clean, tests/test_verify.py::test_print_report_clean, tests/test_verify.py::test_print_report_lists_each_drift, tests/test_verify.py::test_report_counts_all_drift_classes, tests/test_verify.py::test_report_with_stale_files_not_clean, tests/test_verify.py::test_scan_agents_md_present_and_valid_not_flagged, tests/test_verify.py::test_scan_deep_page_with_empty_narrative_not_flagged, tests/test_verify.py::test_scan_detects_dangling_manifest_entries, tests/test_verify.py::test_scan_detects_hook_drift, tests/test_verify.py::test_scan_detects_missing_agents_md_snippet, tests/test_verify.py::test_scan_detects_missing_claude_md_snippet, tests/test_verify.py::test_scan_detects_missing_gitignore_entry, tests/test_verify.py::test_scan_detects_missing_index_and_skill, tests/test_verify.py::test_scan_detects_missing_wiki_page, tests/test_verify.py::test_scan_detects_orphan_wiki_page, tests/test_verify.py::test_scan_detects_pages_missing_deep_sections, tests/test_verify.py::test_scan_detects_stale_files, tests/test_verify.py::test_scan_detects_untracked_source_files, tests/test_verify.py::test_scan_flags_missing_manifest, tests/test_verify.py::test_scan_skips_deep_check_when_skip_deep_true, tests/test_verify.py::test_scan_skips_hook_check_when_check_hook_false, tests/test_wiki.py::_make_node, tests/test_wiki.py::test_build_index_contains_page, tests/test_wiki.py::test_build_page_contains_called_by, tests/test_wiki.py::test_build_page_contains_calls, tests/test_wiki.py::test_build_page_contains_symbol, tests/test_wiki.py::test_build_page_no_agent_hints, tests/test_wiki.py::test_delete_orphan_pages_missing_wiki_dir, tests/test_wiki.py::test_delete_orphan_pages_noop_when_all_referenced, tests/test_wiki.py::test_delete_orphan_pages_removes_unreferenced, tests/test_wiki.py::test_index_frontmatter_has_okf_version, tests/test_wiki.py::test_index_renders_core_abstractions, tests/test_wiki.py::test_page_basename_nested_group, tests/test_wiki.py::test_page_basename_root_group, tests/test_wiki.py::test_page_body_sections_preserved_below_frontmatter, tests/test_wiki.py::test_page_frontmatter_description_from_narrative_first_sentence, tests/test_wiki.py::test_page_frontmatter_description_generic_when_no_narrative, tests/test_wiki.py::test_page_frontmatter_is_valid_yaml_with_required_type, tests/test_wiki.py::test_page_frontmatter_tags_from_path_segments, tests/test_wiki.py::test_page_frontmatter_timestamp_passed_in_not_computed, tests/test_wiki.py::test_page_frontmatter_title_and_resource, tests/test_wiki.py::test_page_relationships_block_caps_long_lists, tests/test_wiki.py::test_page_relpath_matches_write_page, tests/test_wiki.py::test_page_renders_relationships_block_per_symbol, tests/test_wiki.py::test_page_starts_with_frontmatter_delimiter, tests/test_wiki.py::test_write_page_creates_file
- **Imports from:** __future__.annotations, anthropic, ast, click, collections.defaultdict, collections.deque, dataclasses.asdict, dataclasses.dataclass, dataclasses.field, datetime.datetime, datetime.timezone, fnmatch.fnmatch, hashlib, indexer.ast_parser.ASTNode, indexer.ast_parser.compute_hash_short, indexer.ast_parser.load_cached_nodes, indexer.ast_parser.parse_file, indexer.ast_parser.save_cached_nodes, indexer.cli._ensure_cache_gitignore, indexer.cli._ensure_nav_guidance, indexer.cli._expand_candidates_to_groups, indexer.cli._finalise_index_and_skill, indexer.cli._index_files, indexer.config.Config, indexer.config.load_config, indexer.config.save_config, indexer.git.all_tracked_files, indexer.git.changed_files_since, indexer.git.current_commit, indexer.git.is_git_repo, indexer.git.staged_files, indexer.graph.build_blast_radius_map, indexer.graph.god_nodes, indexer.graph.repo_map, indexer.grouper.density_group, indexer.hooks.HOOK_MARKER, indexer.hooks.install_hook, indexer.hooks.remove_hook, indexer.js_parser.parse_js_file, indexer.langs.is_indexable, indexer.llm.deep_enrich_index, indexer.llm.deep_enrich_page, indexer.llm.describe_files, indexer.llm.describe_nodes, indexer.llm.synthesize_commit_message, indexer.manifest.Manifest, indexer.manifest.compute_hash, indexer.manifest.file_entry_for, indexer.manifest.load_manifest, indexer.manifest.save_manifest, indexer.repair, indexer.repair._index_entries_from_manifest, indexer.scip.scip_symbol, indexer.ts_extract.LANG_CONFIGS, indexer.ts_extract.extract_generic, indexer.verify, indexer.verify.VerifyReport, indexer.wiki.IndexEntry, indexer.wiki.PageContext, indexer.wiki.TEMPLATES_DIR, indexer.wiki.build_index, indexer.wiki.build_page, indexer.wiki.delete_orphan_pages, indexer.wiki.page_relpath, indexer.wiki.write_index, indexer.wiki.write_page, jinja2.Environment, jinja2.FileSystemLoader, json, litellm, os, pathlib.Path, re, shutil, subprocess, time, tomli_w, tomllib, tree_sitter.Language, tree_sitter.Parser, tree_sitter_javascript, tree_sitter_typescript, typing.Callable, typing.Optional, warnings, yaml
## Entry Points
- `main`
- `init`
- `status`
- `hook`
- `hook_install`
- `hook_remove`
- `LangConfig`
