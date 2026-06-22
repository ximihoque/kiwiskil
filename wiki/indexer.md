---
type: Code Group
title: indexer
description: 'This module pair forms the output layer of the kiwiskil indexing pipeline:
  cli.py orchestrates the full index lifecycle (init, incremental run, smart repair,
  pre-commit hook management) while wiki.py owns all rendering logic — converting
  AST nodes and LLM-generated metadata into OKF-compliant markdown wiki pages.'
tags:
- indexer
timestamp: '2026-06-22T09:08:18.826446+00:00'
resource: indexer
---
# indexer/
<!-- kiwiskil:deep -->

## Overview

This module pair forms the output layer of the kiwiskil indexing pipeline: cli.py orchestrates the full index lifecycle (init, incremental run, smart repair, pre-commit hook management) while wiki.py owns all rendering logic — converting AST nodes and LLM-generated metadata into OKF-compliant markdown wiki pages. cli.py is the single consumer of every other indexer subsystem (ast_parser, grouper, graph, llm, manifest, git, hooks) and sequences them through a 5-phase pipeline (parse → cross-reference → LLM describe → file-level describe → group→page). wiki.py is stateless and template-driven (Jinja2), receiving fully-prepared PageContext/IndexEntry data objects from cli.py and emitting markdown strings; it has no LLM dependency. The split means rendering logic can be tested independently from orchestration, and templates (in indexer/templates/) are the single change point for output format.

## Modules
| File | Purpose |
|------|---------|
| indexer/wiki.py | Build wiki pages and INDEX from AST nodes, symbol relationships |
| indexer/cli.py | CLI commands to index codebase, generate wiki pages, manage hooks |
## Key Symbols
| ID | Type | Description |
|----|------|-------------|
| `indexer/cli.py::_ensure_nav_guidance` | function | Append NAV_GUIDANCE marker to target file if absent, idempotent. |
| `indexer/cli.py::main` | function | Click group entry point for CLI commands. |
| `indexer/cli.py::init` | function | Create .indexer.toml config, install pre-commit hook, update CLAUDE.md. |
| `indexer/cli.py::run` | function | Index codebase, generate wiki pages, persist manifest and skill. |
| `indexer/cli.py::status` | function | Display last indexed commit, stale files, manifest statistics. |
| `indexer/cli.py::hook` | function | Click group for pre-commit hook subcommands. |
| `indexer/cli.py::hook_install` | function | Install pre-commit hook in current git repository. |
| `indexer/cli.py::hook_remove` | function | Remove pre-commit hook from current repository. |
| `indexer/cli.py::_ensure_cache_gitignore` | function | Add .indexer/cache/ to root .gitignore, create if missing. |
| `indexer/cli.py::_is_indexable` | function | Check if file is indexable per configuration. |
| `indexer/cli.py::_index_files` | function | Run phases 1-5 indexing pipeline, write wiki pages and cache. |
| `indexer/cli.py::_finalise_index_and_skill` | function | Build wiki/INDEX.md and codebase.md skill with god nodes. |
| `indexer/cli.py::_prune_deleted` | function | Remove manifest entries and orphan wiki pages for deleted files. |
| `indexer/cli.py::_index_and_persist` | function | Index candidates, persist wiki pages, INDEX, skill, manifest. |
| `indexer/cli.py::_run_smart` | function | Scan for issues and diffs, plan repairs, execute with report. |
| `indexer/wiki.py::PageContext` | class | Container for group-level context during wiki page building. |
| `indexer/wiki.py::IndexEntry` | class | Container for index entry metadata. |
| `indexer/wiki.py::_jinja_env` | function | Create Jinja2 environment with filesystem template loader. |
| `indexer/wiki.py::_first_sentence` | function | Extract first sentence from text (up to first period). |
| `indexer/wiki.py::_tags_from_path` | function | Derive YAML frontmatter tags from group path segments. |
| `indexer/wiki.py::_short` | function | Convert component ID to page-local symbol label. |
| `indexer/wiki.py::_capped` | function | Return tuple of first N items and count of remaining. |
| `indexer/wiki.py::_symbol_relationships` | function | Build per-symbol inline relationships (callers, calls, blast radius). |
| `indexer/wiki.py::build_page` | function | Render wiki page markdown from group nodes and metadata. |
| `indexer/wiki.py::_yaml_frontmatter` | function | Serialize dict to YAML frontmatter string with proper escaping. |
| `indexer/wiki.py::build_index` | function | Render wiki/INDEX.md from repository map and index entries. |
| `indexer/wiki.py::page_basename` | function | Sanitize group label to filename stem (/→_, root→root). |
| `indexer/wiki.py::page_relpath` | function | Return repo-relative path for wiki page of a group. |
| `indexer/wiki.py::write_page` | function | Write rendered markdown to wiki page file. |
| `indexer/wiki.py::delete_orphan_pages` | function | Remove wiki/*.md files no longer referenced in manifest. |
| `indexer/wiki.py::write_index` | function | Write INDEX.md to wiki directory. |
## Symbol Relationships
### `_ensure_nav_guidance`
- **Callers (1):** init
- **Calls:** echo, exists, lstrip, read_text, write_text
- **Editing this affects:** init
### `main`
- **Callers (0):** none
- **Calls:** group
- **Editing this affects:** none
### `init`
- **Callers (0):** none
- **Calls:** _ensure_cache_gitignore, _ensure_nav_guidance, command, cwd, echo, install_hook, is_git_repo, load_config … (+1 more)
- **Editing this affects:** none
### `run`
- **Callers (12):** _bootstrap_repo, _index_and_persist, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero, test_smart_dry_run_does_not_modify_filesystem, test_smart_dry_run_drift_exits_nonzero … (+4 more)
- **Calls:** UsageError, _ensure_cache_gitignore, _finalise_index_and_skill, _index_and_persist, _index_entries_from_manifest, _is_indexable, _prune_deleted, _run_smart … (+20 more)
- **Editing this affects:** _bootstrap_repo, _index_and_persist, _run_smart, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero, test_smart_dry_run_does_not_modify_filesystem … (+5 more)
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
- **Callers (3):** _run_smart, init, run
- **Calls:** echo, exists, read_text, rstrip, write_text
- **Editing this affects:** _bootstrap_repo, _index_and_persist, _run_smart, init, run, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop … (+7 more)
### `_is_indexable`
- **Callers (3):** _run_smart, run, status
- **Calls:** is_indexable
- **Editing this affects:** _bootstrap_repo, _index_and_persist, _run_smart, run, status, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop … (+7 more)
### `_index_files`
- **Callers (1):** _index_and_persist
- **Calls:** IndexEntry, PageContext, append, build_blast_radius_map, build_page, compute_hash_short, deep_enrich_page, density_group … (+25 more)
- **Editing this affects:** _bootstrap_repo, _index_and_persist, _run_smart, run, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero … (+6 more)
### `_finalise_index_and_skill`
- **Callers (2):** _index_and_persist, run
- **Calls:** Environment, FileSystemLoader, build_index, current_commit, deep_enrich_index, echo, get, get_template … (+12 more)
- **Editing this affects:** _bootstrap_repo, _index_and_persist, _run_smart, run, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero … (+6 more)
### `_prune_deleted`
- **Callers (1):** run
- **Calls:** all_tracked_files, bool, delete_orphan_pages, echo, is_git_repo, set, values
- **Editing this affects:** _bootstrap_repo, _index_and_persist, _run_smart, run, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero … (+6 more)
### `_index_and_persist`
- **Callers (2):** _run_smart, run
- **Calls:** _finalise_index_and_skill, _index_files, all_tracked_files, compute_hash, current_commit, delete_orphan_pages, echo, exists … (+12 more)
- **Editing this affects:** _bootstrap_repo, _run_smart, run, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero, test_smart_dry_run_does_not_modify_filesystem … (+5 more)
### `_run_smart`
- **Callers (1):** run
- **Calls:** Exit, _ensure_cache_gitignore, _index_and_persist, _is_indexable, all_tracked_files, echo, execute, has_work … (+6 more)
- **Editing this affects:** _bootstrap_repo, _index_and_persist, run, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero, test_smart_dry_run_does_not_modify_filesystem … (+5 more)
### `PageContext`
- **Callers (16):** _index_files, test_build_page_contains_called_by, test_build_page_contains_calls, test_build_page_contains_symbol, test_build_page_no_agent_hints, test_page_body_sections_preserved_below_frontmatter, test_page_frontmatter_description_from_narrative_first_sentence, test_page_frontmatter_description_generic_when_no_narrative … (+8 more)
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _index_and_persist, _index_files, _run_smart, run, test_build_page_contains_called_by, test_build_page_contains_calls, test_build_page_contains_symbol … (+22 more)
### `IndexEntry`
- **Callers (4):** _index_files, test_build_index_contains_page, test_index_frontmatter_has_okf_version, test_index_renders_core_abstractions
- **Calls:** none
- **Editing this affects:** _bootstrap_repo, _index_and_persist, _index_files, _run_smart, run, test_build_index_contains_page, test_index_frontmatter_has_okf_version, test_index_renders_core_abstractions … (+10 more)
### `_jinja_env`
- **Callers (2):** build_index, build_page
- **Calls:** Environment, FileSystemLoader, str
- **Editing this affects:** _bootstrap_repo, _finalise_index_and_skill, _index_and_persist, _index_files, _run_smart, build_index, build_page, run … (+28 more)
### `_first_sentence`
- **Callers (1):** build_page
- **Calls:** endswith, find, strip
- **Editing this affects:** _bootstrap_repo, _index_and_persist, _index_files, _run_smart, build_page, run, test_build_page_contains_called_by, test_build_page_contains_calls … (+23 more)
### `_tags_from_path`
- **Callers (1):** build_page
- **Calls:** add, append, set, split, strip
- **Editing this affects:** _bootstrap_repo, _index_and_persist, _index_files, _run_smart, build_page, run, test_build_page_contains_called_by, test_build_page_contains_calls … (+23 more)
### `_short`
- **Callers (2):** _symbol_relationships, build_index
- **Calls:** split
- **Editing this affects:** _bootstrap_repo, _finalise_index_and_skill, _index_and_persist, _index_files, _run_smart, _symbol_relationships, build_index, build_page … (+29 more)
### `_capped`
- **Callers (1):** _symbol_relationships
- **Calls:** len
- **Editing this affects:** _bootstrap_repo, _index_and_persist, _index_files, _run_smart, _symbol_relationships, build_page, run, test_build_page_contains_called_by … (+24 more)
### `_symbol_relationships`
- **Callers (1):** build_page
- **Calls:** _capped, _short, append, get, len, set, sorted
- **Editing this affects:** _bootstrap_repo, _index_and_persist, _index_files, _run_smart, build_page, run, test_build_page_contains_called_by, test_build_page_contains_calls … (+23 more)
### `build_page`
- **Callers (16):** _index_files, test_build_page_contains_called_by, test_build_page_contains_calls, test_build_page_contains_symbol, test_build_page_no_agent_hints, test_page_body_sections_preserved_below_frontmatter, test_page_frontmatter_description_from_narrative_first_sentence, test_page_frontmatter_description_generic_when_no_narrative … (+8 more)
- **Calls:** _first_sentence, _jinja_env, _symbol_relationships, _tags_from_path, _yaml_frontmatter, get, get_template, join … (+4 more)
- **Editing this affects:** _bootstrap_repo, _index_and_persist, _index_files, _run_smart, run, test_build_page_contains_called_by, test_build_page_contains_calls, test_build_page_contains_symbol … (+22 more)
### `_yaml_frontmatter`
- **Callers (2):** build_index, build_page
- **Calls:** rstrip, safe_dump
- **Editing this affects:** _bootstrap_repo, _finalise_index_and_skill, _index_and_persist, _index_files, _run_smart, build_index, build_page, run … (+28 more)
### `build_index`
- **Callers (4):** _finalise_index_and_skill, test_build_index_contains_page, test_index_frontmatter_has_okf_version, test_index_renders_core_abstractions
- **Calls:** _jinja_env, _short, _yaml_frontmatter, get_template, render
- **Editing this affects:** _bootstrap_repo, _finalise_index_and_skill, _index_and_persist, _run_smart, run, test_build_index_contains_page, test_index_frontmatter_has_okf_version, test_index_renders_core_abstractions … (+10 more)
### `page_basename`
- **Callers (4):** page_relpath, test_page_basename_nested_group, test_page_basename_root_group, write_page
- **Calls:** replace, strip
- **Editing this affects:** _bootstrap_repo, _index_and_persist, _index_files, _run_smart, page_relpath, run, test_page_basename_nested_group, test_page_basename_root_group … (+13 more)
### `page_relpath`
- **Callers (2):** _index_and_persist, test_page_relpath_matches_write_page
- **Calls:** page_basename
- **Editing this affects:** _bootstrap_repo, _index_and_persist, _run_smart, run, test_page_relpath_matches_write_page, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop … (+7 more)
### `write_page`
- **Callers (3):** _index_files, test_page_relpath_matches_write_page, test_write_page_creates_file
- **Calls:** mkdir, page_basename, write_text
- **Editing this affects:** _bootstrap_repo, _index_and_persist, _index_files, _run_smart, run, test_page_relpath_matches_write_page, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files … (+9 more)
### `delete_orphan_pages`
- **Callers (5):** _index_and_persist, _prune_deleted, test_delete_orphan_pages_missing_wiki_dir, test_delete_orphan_pages_noop_when_all_referenced, test_delete_orphan_pages_removes_unreferenced
- **Calls:** exists, glob, sorted, unlink
- **Editing this affects:** _bootstrap_repo, _index_and_persist, _prune_deleted, _run_smart, run, test_delete_orphan_pages_missing_wiki_dir, test_delete_orphan_pages_noop_when_all_referenced, test_delete_orphan_pages_removes_unreferenced … (+10 more)
### `write_index`
- **Callers (1):** _finalise_index_and_skill
- **Calls:** mkdir, write_text
- **Editing this affects:** _bootstrap_repo, _finalise_index_and_skill, _index_and_persist, _run_smart, run, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop … (+7 more)
## Data Flows
- pre-commit hook trigger → run --staged → staged_files() → _index_and_persist() → _index_files() phases 1-5 → write_page() + _finalise_index_and_skill() → git add wiki/ manifest skill → commit message synthesis
- kiwiskil run (incremental) → load_manifest → changed_files_since + stale_files → filter by _is_indexable → _index_and_persist → _index_files → build_page(PageContext) → write_page → save_manifest
- kiwiskil run --smart → verify.scan() → if clean return; if manifest_missing full fill via _index_and_persist; else repair.plan + repair.execute → _finalise_index_and_skill rebuilds INDEX + skill
- deletion-only commit → candidates empty → _prune_deleted removes manifest entries + delete_orphan_pages unlinks wiki/*.md → _finalise_index_and_skill rebuilds INDEX/skill from surviving manifest entries
## Design Constraints
- page_basename() is the single source of truth for wiki filename derivation — manifest's wiki_page field MUST use page_relpath() (which calls page_basename()), never the raw group label; divergence causes --smart to see phantom missing-page + orphan-page for the same group
- _index_files() writes wiki pages as a side effect but does NOT touch INDEX.md, the skill file, manifest, .gitignore, hooks, or CLAUDE.md — callers must call _finalise_index_and_skill() and save_manifest() separately or those artifacts will be stale
- PageContext.timestamp and blast_radius_map are computed in cli.py (_index_files), never inside wiki.py or templates — Date.now()-equivalent calls are banned inside rendering to preserve determinism and resume safety
- delete_orphan_pages() excludes INDEX.md by name check (p.name != 'INDEX.md') — all other wiki/*.md files not in the manifest's referenced_pages set are deleted unconditionally, including any hand-authored pages
- _ensure_nav_guidance() uses the string 'Codebase Navigation' as the idempotency marker, not a comment or sentinel line — editing that heading in CLAUDE.md/AGENTS.md causes the block to be appended again on next init or run
- --smart and --force/--staged are mutually exclusive at the CLI level (UsageError); --dry-run and --no-hook-check are only valid with --smart; these constraints are enforced before any I/O
## Relationships
- **Calls:** Environment, Exit, FileSystemLoader, IndexEntry, PageContext, UsageError, _capped, _ensure_cache_gitignore, _ensure_nav_guidance, _finalise_index_and_skill, _first_sentence, _index_and_persist, _index_entries_from_manifest, _index_files, _is_indexable, _jinja_env, _prune_deleted, _run_smart, _short, _symbol_relationships, _tags_from_path, _yaml_frontmatter, add, all_tracked_files, append, bool, build_blast_radius_map, build_index, build_page, changed_files_since, command, compute_hash, compute_hash_short, current_commit, cwd, deep_enrich_index, deep_enrich_page, delete_orphan_pages, density_group, describe_files, describe_nodes, echo, endswith, enumerate, execute, exists, extend, file_entry_for, find, get, get_template, glob, god_nodes, group, has_work, install_hook, is_clean, is_git_repo, is_indexable, isoformat, items, join, len, list, load_cached_nodes, load_config, load_manifest, lstrip, mkdir, now, option, page_basename, page_relpath, parse_file, plan, print_report, read_text, relative_to, remove_hook, render, replace, repo_map, rstrip, run, safe_dump, save_cached_nodes, save_config, save_manifest, scan, set, setdefault, sorted, split, staged_files, stale_files, startswith, str, strftime, strip, sum, synthesize_commit_message, total_issues, unlink, update, values, write_index, write_page, write_text
- **Called by:** indexer/cli.py::_finalise_index_and_skill, indexer/cli.py::_index_and_persist, indexer/cli.py::_index_files, indexer/cli.py::_prune_deleted, indexer/cli.py::_run_smart, indexer/cli.py::init, indexer/cli.py::run, indexer/cli.py::status, indexer/wiki.py::_symbol_relationships, indexer/wiki.py::build_index, indexer/wiki.py::build_page, indexer/wiki.py::page_relpath, indexer/wiki.py::write_page, tests/test_smart_integration.py::_bootstrap_repo, tests/test_smart_integration.py::test_run_deletes_orphan_page_when_source_deleted, tests/test_smart_integration.py::test_smart_bails_when_no_indexable_files, tests/test_smart_integration.py::test_smart_clean_state_is_noop, tests/test_smart_integration.py::test_smart_dry_run_clean_repo_exits_zero, tests/test_smart_integration.py::test_smart_dry_run_does_not_modify_filesystem, tests/test_smart_integration.py::test_smart_dry_run_drift_exits_nonzero, tests/test_smart_integration.py::test_smart_dry_run_reports_full_initial_index_without_changes, tests/test_smart_integration.py::test_smart_fills_fresh_repo_with_no_manifest, tests/test_smart_integration.py::test_smart_fills_never_indexed_tracked_file, tests/test_smart_integration.py::test_smart_repairs_missing_wiki_page, tests/test_wiki.py::test_build_index_contains_page, tests/test_wiki.py::test_build_page_contains_called_by, tests/test_wiki.py::test_build_page_contains_calls, tests/test_wiki.py::test_build_page_contains_symbol, tests/test_wiki.py::test_build_page_no_agent_hints, tests/test_wiki.py::test_delete_orphan_pages_missing_wiki_dir, tests/test_wiki.py::test_delete_orphan_pages_noop_when_all_referenced, tests/test_wiki.py::test_delete_orphan_pages_removes_unreferenced, tests/test_wiki.py::test_index_frontmatter_has_okf_version, tests/test_wiki.py::test_index_renders_core_abstractions, tests/test_wiki.py::test_page_basename_nested_group, tests/test_wiki.py::test_page_basename_root_group, tests/test_wiki.py::test_page_body_sections_preserved_below_frontmatter, tests/test_wiki.py::test_page_frontmatter_description_from_narrative_first_sentence, tests/test_wiki.py::test_page_frontmatter_description_generic_when_no_narrative, tests/test_wiki.py::test_page_frontmatter_is_valid_yaml_with_required_type, tests/test_wiki.py::test_page_frontmatter_tags_from_path_segments, tests/test_wiki.py::test_page_frontmatter_timestamp_passed_in_not_computed, tests/test_wiki.py::test_page_frontmatter_title_and_resource, tests/test_wiki.py::test_page_relationships_block_caps_long_lists, tests/test_wiki.py::test_page_relpath_matches_write_page, tests/test_wiki.py::test_page_renders_relationships_block_per_symbol, tests/test_wiki.py::test_page_starts_with_frontmatter_delimiter, tests/test_wiki.py::test_write_page_creates_file
- **Imports from:** __future__.annotations, click, dataclasses.dataclass, dataclasses.field, datetime.datetime, datetime.timezone, indexer.ast_parser.compute_hash_short, indexer.ast_parser.load_cached_nodes, indexer.ast_parser.parse_file, indexer.ast_parser.save_cached_nodes, indexer.config.Config, indexer.config.load_config, indexer.config.save_config, indexer.git.all_tracked_files, indexer.git.changed_files_since, indexer.git.current_commit, indexer.git.is_git_repo, indexer.git.staged_files, indexer.graph.build_blast_radius_map, indexer.graph.god_nodes, indexer.graph.repo_map, indexer.grouper.density_group, indexer.hooks.install_hook, indexer.hooks.remove_hook, indexer.langs.is_indexable, indexer.llm.deep_enrich_index, indexer.llm.deep_enrich_page, indexer.llm.describe_files, indexer.llm.describe_nodes, indexer.llm.synthesize_commit_message, indexer.manifest.compute_hash, indexer.manifest.file_entry_for, indexer.manifest.load_manifest, indexer.manifest.save_manifest, indexer.repair, indexer.repair._index_entries_from_manifest, indexer.verify, indexer.wiki.IndexEntry, indexer.wiki.PageContext, indexer.wiki.TEMPLATES_DIR, indexer.wiki.build_index, indexer.wiki.build_page, indexer.wiki.delete_orphan_pages, indexer.wiki.page_relpath, indexer.wiki.write_index, indexer.wiki.write_page, jinja2.Environment, jinja2.FileSystemLoader, pathlib.Path, subprocess, yaml
## Entry Points
- `main`
- `init`
- `status`
- `hook`
- `hook_install`
- `hook_remove`
