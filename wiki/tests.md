---
type: Code Group
title: tests
description: 'This test group validates two orthogonal subsystems: the `--smart` incremental-indexing
  CLI mode (test_smart_integration.py) and the wiki page/index rendering pipeline
  (test_wiki.py).'
tags:
- tests
timestamp: '2026-06-22T09:08:18.826446+00:00'
resource: tests
---
# tests/
<!-- kiwiskil:deep -->

## Overview

This test group validates two orthogonal subsystems: the `--smart` incremental-indexing CLI mode (test_smart_integration.py) and the wiki page/index rendering pipeline (test_wiki.py). The smart integration tests exist because `--smart` has complex state-machine behavior — it must distinguish no-manifest (full index), clean-state (noop), drift (repair), and orphan-deletion scenarios, each with different exit codes and filesystem effects. The wiki tests exist because `build_page`/`build_index`/`write_page` are the primary artifact generators; correctness of their OKF frontmatter, symbol sections, call-graph rendering, and path sanitization is critical for downstream agent navigation. `_stub_llm` is a shared monkeypatch helper that replaces all four LLM call-sites (`describe_nodes`, `describe_files`, `deep_enrich_page`, `deep_enrich_index`) in `indexer.cli` to make integration tests hermetic. `_bootstrap_repo` creates a minimal git repo because `--smart` inspects tracked files via git, not the raw filesystem.

## Modules
| File | Purpose |
|------|---------|
| tests/test_smart_integration.py | Integration tests for smart repair mode with LLM |
| tests/test_wiki.py | Unit tests for wiki page generation and frontmatter |
## Key Symbols
| ID | Type | Description |
|----|------|-------------|
| `tests/test_smart_integration.py::_bootstrap_repo` | function | Initialize test git repository with indexer config. |
| `tests/test_smart_integration.py::test_smart_rejects_combo_with_force` | function | Verify --smart rejects --force flag combination. |
| `tests/test_smart_integration.py::test_smart_rejects_combo_with_staged` | function | Verify --smart rejects --staged flag combination. |
| `tests/test_smart_integration.py::test_smart_bails_when_no_indexable_files` | function | Verify --smart exits cleanly when no indexable files found. |
| `tests/test_smart_integration.py::test_smart_dry_run_does_not_modify_filesystem` | function | Verify --smart --dry-run doesn't write files. |
| `tests/test_smart_integration.py::_stub_llm` | function | Mock LLM description generation for testing. |
| `tests/test_smart_integration.py::test_smart_repairs_missing_wiki_page` | function | Verify --smart rebuilds missing wiki page from manifest. |
| `tests/test_smart_integration.py::test_smart_clean_state_is_noop` | function | Verifies that re-indexing clean repo with manifest produces no changes |
| `tests/test_smart_integration.py::test_smart_fills_fresh_repo_with_no_manifest` | function | Verifies indexing populates fresh repo without prior manifest |
| `tests/test_smart_integration.py::test_smart_dry_run_reports_full_initial_index_without_changes` | function | Verifies dry-run on unindexed repo reports full index without writing |
| `tests/test_smart_integration.py::test_smart_fills_never_indexed_tracked_file` | function | Verifies indexing adds previously unindexed tracked file to manifest |
| `tests/test_smart_integration.py::test_smart_dry_run_clean_repo_exits_zero` | function | Verifies dry-run exits zero on clean indexed repo |
| `tests/test_smart_integration.py::test_smart_dry_run_drift_exits_nonzero` | function | Verifies dry-run exits nonzero when repo drifts from manifest |
| `tests/test_smart_integration.py::test_run_deletes_orphan_page_when_source_deleted` | function | Verifies deleting last source in group removes its wiki page |
| `tests/test_wiki.py::_make_node` | function | Creates test AST node with overridable attributes |
| `tests/test_wiki.py::test_build_page_contains_symbol` | function | Verifies page includes symbol definition |
| `tests/test_wiki.py::test_build_page_contains_calls` | function | Verifies page documents symbol's function calls |
| `tests/test_wiki.py::test_build_page_contains_called_by` | function | Verifies page documents symbol's call sites |
| `tests/test_wiki.py::test_build_page_no_agent_hints` | function | Verifies page excludes agent hints from plain symbols |
| `tests/test_wiki.py::test_build_index_contains_page` | function | Verifies index includes page entry |
| `tests/test_wiki.py::test_write_page_creates_file` | function | Verifies write_page creates wiki file with content |
| `tests/test_wiki.py::_parse_frontmatter` | function | Extracts and YAML-parses leading frontmatter block |
| `tests/test_wiki.py::test_page_starts_with_frontmatter_delimiter` | function | Verifies page starts with frontmatter delimiter |
| `tests/test_wiki.py::test_page_frontmatter_is_valid_yaml_with_required_type` | function | Verifies frontmatter is valid YAML with type field |
| `tests/test_wiki.py::test_page_frontmatter_title_and_resource` | function | Verifies frontmatter contains title and resource fields |
| `tests/test_wiki.py::test_page_frontmatter_tags_from_path_segments` | function | Verifies frontmatter tags extracted from wiki path |
| `tests/test_wiki.py::test_page_frontmatter_timestamp_passed_in_not_computed` | function | Verifies frontmatter uses provided timestamp |
| `tests/test_wiki.py::test_page_frontmatter_description_from_narrative_first_sentence` | function | Verifies frontmatter description pulled from narrative |
| `tests/test_wiki.py::test_page_frontmatter_description_generic_when_no_narrative` | function | Verifies frontmatter uses generic description when no narrative |
| `tests/test_wiki.py::test_page_body_sections_preserved_below_frontmatter` | function | Verifies page body sections preserved after frontmatter |
| `tests/test_wiki.py::test_index_frontmatter_has_okf_version` | function | Verifies index frontmatter contains OKF version |
| `tests/test_wiki.py::test_page_renders_relationships_block_per_symbol` | function | Verifies page renders relationships section per symbol |
| `tests/test_wiki.py::test_page_relationships_block_caps_long_lists` | function | Verifies relationships section caps long call lists |
| `tests/test_wiki.py::test_index_renders_core_abstractions` | function | Verifies index renders core abstractions section |
| `tests/test_wiki.py::test_page_basename_root_group` | function | Verifies page filename for root-level component group |
| `tests/test_wiki.py::test_page_basename_nested_group` | function | Verifies page filename for nested component group |
| `tests/test_wiki.py::test_page_relpath_matches_write_page` | function | Verifies manifest wiki_page path matches write_page output |
| `tests/test_wiki.py::test_delete_orphan_pages_removes_unreferenced` | function | Verifies orphan pages removed when source files deleted |
| `tests/test_wiki.py::test_delete_orphan_pages_noop_when_all_referenced` | function | Verifies orphan deletion skips pages still referenced |
| `tests/test_wiki.py::test_delete_orphan_pages_missing_wiki_dir` | function | Verifies orphan deletion handles missing wiki directory |
## Symbol Relationships
### `_bootstrap_repo`
- **Callers (10):** test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero, test_smart_dry_run_does_not_modify_filesystem, test_smart_dry_run_drift_exits_nonzero, test_smart_dry_run_reports_full_initial_index_without_changes, test_smart_fills_fresh_repo_with_no_manifest … (+2 more)
- **Calls:** run
- **Editing this affects:** test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero, test_smart_dry_run_does_not_modify_filesystem, test_smart_dry_run_drift_exits_nonzero, test_smart_dry_run_reports_full_initial_index_without_changes, test_smart_fills_fresh_repo_with_no_manifest … (+2 more)
### `test_smart_rejects_combo_with_force`
- **Callers (0):** none
- **Calls:** CliRunner, invoke, isolated_filesystem, lower
- **Editing this affects:** none
### `test_smart_rejects_combo_with_staged`
- **Callers (0):** none
- **Calls:** CliRunner, invoke, isolated_filesystem
- **Editing this affects:** none
### `test_smart_bails_when_no_indexable_files`
- **Callers (0):** none
- **Calls:** CliRunner, Path, _bootstrap_repo, invoke, isolated_filesystem, lower, run, write_text
- **Editing this affects:** none
### `test_smart_dry_run_does_not_modify_filesystem`
- **Callers (0):** none
- **Calls:** CliRunner, FileEntry, Manifest, Path, _bootstrap_repo, invoke, isolated_filesystem, lower … (+4 more)
- **Editing this affects:** none
### `_stub_llm`
- **Callers (7):** test_run_deletes_orphan_page_when_source_deleted, test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero, test_smart_dry_run_reports_full_initial_index_without_changes, test_smart_fills_fresh_repo_with_no_manifest, test_smart_fills_never_indexed_tracked_file, test_smart_repairs_missing_wiki_page
- **Calls:** setattr
- **Editing this affects:** test_run_deletes_orphan_page_when_source_deleted, test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero, test_smart_dry_run_reports_full_initial_index_without_changes, test_smart_fills_fresh_repo_with_no_manifest, test_smart_fills_never_indexed_tracked_file, test_smart_repairs_missing_wiki_page
### `test_smart_repairs_missing_wiki_page`
- **Callers (0):** none
- **Calls:** CliRunner, FileEntry, Manifest, Path, _bootstrap_repo, _stub_llm, compute_hash, exists … (+5 more)
- **Editing this affects:** none
### `test_smart_clean_state_is_noop`
- **Callers (0):** none
- **Calls:** CliRunner, FileEntry, Manifest, Path, _bootstrap_repo, _stub_llm, compute_hash, invoke … (+6 more)
- **Editing this affects:** none
### `test_smart_fills_fresh_repo_with_no_manifest`
- **Callers (0):** none
- **Calls:** CliRunner, Path, _bootstrap_repo, _stub_llm, exists, invoke, isolated_filesystem, load_manifest … (+2 more)
- **Editing this affects:** none
### `test_smart_dry_run_reports_full_initial_index_without_changes`
- **Callers (0):** none
- **Calls:** CliRunner, Path, _bootstrap_repo, _stub_llm, exists, invoke, isolated_filesystem, lower … (+2 more)
- **Editing this affects:** none
### `test_smart_fills_never_indexed_tracked_file`
- **Callers (0):** none
- **Calls:** CliRunner, FileEntry, Manifest, Path, _bootstrap_repo, _stub_llm, compute_hash, invoke … (+6 more)
- **Editing this affects:** none
### `test_smart_dry_run_clean_repo_exits_zero`
- **Callers (0):** none
- **Calls:** CliRunner, FileEntry, Manifest, Path, _bootstrap_repo, _stub_llm, compute_hash, invoke … (+5 more)
- **Editing this affects:** none
### `test_smart_dry_run_drift_exits_nonzero`
- **Callers (0):** none
- **Calls:** CliRunner, FileEntry, Manifest, Path, _bootstrap_repo, invoke, isolated_filesystem, run … (+2 more)
- **Editing this affects:** none
### `test_run_deletes_orphan_page_when_source_deleted`
- **Callers (0):** none
- **Calls:** CliRunner, Path, _bootstrap_repo, _stub_llm, glob, invoke, isolated_filesystem, load_manifest … (+4 more)
- **Editing this affects:** none
### `_make_node`
- **Callers (15):** test_build_page_contains_called_by, test_build_page_contains_calls, test_build_page_contains_symbol, test_build_page_no_agent_hints, test_page_body_sections_preserved_below_frontmatter, test_page_frontmatter_description_from_narrative_first_sentence, test_page_frontmatter_description_generic_when_no_narrative, test_page_frontmatter_is_valid_yaml_with_required_type … (+7 more)
- **Calls:** ASTNode, dict, update
- **Editing this affects:** test_build_page_contains_called_by, test_build_page_contains_calls, test_build_page_contains_symbol, test_build_page_no_agent_hints, test_page_body_sections_preserved_below_frontmatter, test_page_frontmatter_description_from_narrative_first_sentence, test_page_frontmatter_description_generic_when_no_narrative, test_page_frontmatter_is_valid_yaml_with_required_type … (+7 more)
### `test_build_page_contains_symbol`
- **Callers (0):** none
- **Calls:** PageContext, _make_node, build_page
- **Editing this affects:** none
### `test_build_page_contains_calls`
- **Callers (0):** none
- **Calls:** PageContext, _make_node, build_page
- **Editing this affects:** none
### `test_build_page_contains_called_by`
- **Callers (0):** none
- **Calls:** PageContext, _make_node, build_page
- **Editing this affects:** none
### `test_build_page_no_agent_hints`
- **Callers (0):** none
- **Calls:** PageContext, _make_node, build_page, lower
- **Editing this affects:** none
### `test_build_index_contains_page`
- **Callers (0):** none
- **Calls:** IndexEntry, build_index
- **Editing this affects:** none
### `test_write_page_creates_file`
- **Callers (0):** none
- **Calls:** PageContext, Path, TemporaryDirectory, _make_node, build_page, exists, read_text, write_page
- **Editing this affects:** none
### `_parse_frontmatter`
- **Callers (6):** test_page_frontmatter_description_from_narrative_first_sentence, test_page_frontmatter_description_generic_when_no_narrative, test_page_frontmatter_is_valid_yaml_with_required_type, test_page_frontmatter_tags_from_path_segments, test_page_frontmatter_timestamp_passed_in_not_computed, test_page_frontmatter_title_and_resource
- **Calls:** safe_load, split, startswith
- **Editing this affects:** test_page_frontmatter_description_from_narrative_first_sentence, test_page_frontmatter_description_generic_when_no_narrative, test_page_frontmatter_is_valid_yaml_with_required_type, test_page_frontmatter_tags_from_path_segments, test_page_frontmatter_timestamp_passed_in_not_computed, test_page_frontmatter_title_and_resource
### `test_page_starts_with_frontmatter_delimiter`
- **Callers (0):** none
- **Calls:** PageContext, _make_node, build_page, count, startswith
- **Editing this affects:** none
### `test_page_frontmatter_is_valid_yaml_with_required_type`
- **Callers (0):** none
- **Calls:** PageContext, _make_node, _parse_frontmatter, build_page
- **Editing this affects:** none
### `test_page_frontmatter_title_and_resource`
- **Callers (0):** none
- **Calls:** PageContext, _make_node, _parse_frontmatter, build_page
- **Editing this affects:** none
### `test_page_frontmatter_tags_from_path_segments`
- **Callers (0):** none
- **Calls:** PageContext, _make_node, _parse_frontmatter, build_page, isinstance
- **Editing this affects:** none
### `test_page_frontmatter_timestamp_passed_in_not_computed`
- **Callers (0):** none
- **Calls:** PageContext, _make_node, _parse_frontmatter, build_page
- **Editing this affects:** none
### `test_page_frontmatter_description_from_narrative_first_sentence`
- **Callers (0):** none
- **Calls:** PageContext, _make_node, _parse_frontmatter, build_page
- **Editing this affects:** none
### `test_page_frontmatter_description_generic_when_no_narrative`
- **Callers (0):** none
- **Calls:** PageContext, _make_node, _parse_frontmatter, build_page
- **Editing this affects:** none
### `test_page_body_sections_preserved_below_frontmatter`
- **Callers (0):** none
- **Calls:** PageContext, _make_node, build_page, split
- **Editing this affects:** none
### `test_index_frontmatter_has_okf_version`
- **Callers (0):** none
- **Calls:** IndexEntry, build_index, safe_load, split, startswith
- **Editing this affects:** none
### `test_page_renders_relationships_block_per_symbol`
- **Callers (0):** none
- **Calls:** PageContext, _make_node, build_page, set
- **Editing this affects:** none
### `test_page_relationships_block_caps_long_lists`
- **Callers (0):** none
- **Calls:** PageContext, _make_node, build_page, range, set
- **Editing this affects:** none
### `test_index_renders_core_abstractions`
- **Callers (0):** none
- **Calls:** IndexEntry, build_index
- **Editing this affects:** none
### `test_page_basename_root_group`
- **Callers (0):** none
- **Calls:** page_basename
- **Editing this affects:** none
### `test_page_basename_nested_group`
- **Callers (0):** none
- **Calls:** page_basename
- **Editing this affects:** none
### `test_page_relpath_matches_write_page`
- **Callers (0):** none
- **Calls:** page_relpath, write_page
- **Editing this affects:** none
### `test_delete_orphan_pages_removes_unreferenced`
- **Callers (0):** none
- **Calls:** delete_orphan_pages, exists, mkdir, write_text
- **Editing this affects:** none
### `test_delete_orphan_pages_noop_when_all_referenced`
- **Callers (0):** none
- **Calls:** delete_orphan_pages, exists, mkdir, write_text
- **Editing this affects:** none
### `test_delete_orphan_pages_missing_wiki_dir`
- **Callers (0):** none
- **Calls:** delete_orphan_pages, set
- **Editing this affects:** none
## Data Flows
- CLI `run --smart` invoked → smart mode checks manifest existence → if absent+indexable files: full index (writes manifest+wiki+INDEX+skill); if manifest present+hash match+wiki exists: noop exit-0; if hash mismatch or missing wiki page: repair only affected groups
- CLI `run --smart --dry-run` → detects drift or no-manifest → prints description of pending work + exits nonzero; clean state → exits zero; in both cases no files are written
- CLI `run` (plain, non-smart) → full or incremental index → after writing new pages, `delete_orphan_pages` scans wiki dir, compares against manifest's referenced pages set, deletes unreferenced `.md` files (excludes INDEX.md)
- `build_page(PageContext)` → renders OKF frontmatter (---YAML---) + body sections (## Modules, ## Key Symbols, relationships block) → `write_page(wiki_dir, group_label, content)` → file at `wiki/{page_basename(group_label)}.md`; `page_relpath` must return the same relative path the file lands at
## Design Constraints
- Exit code is the CI gate signal: `--dry-run` exits nonzero on ANY drift (stale hash, missing wiki page, no manifest with indexable files) and exits zero only on fully clean state — callers must not treat nonzero as error in repair flows, only in CI checks.
- `--smart` is mutually exclusive with both `--force` and `--staged`; passing either combination fails before touching the filesystem.
- A repo with no indexable tracked files (e.g. only README.md) causes `--smart` to exit nonzero with a 'nothing to index' message — it does NOT silently succeed.
- `_stub_llm` must patch all four symbols in `indexer.cli` (not `indexer.llm` or module-local); tests that call LLM code paths without this stub will make real API calls or crash on missing keys.
- `page_basename('.')` returns `'root'` and nested paths use `_` as separator (`a/b/c` → `a_b_c`); the manifest's `wiki_page` field must be computed via `page_relpath` not by manual string construction — the two must stay in sync or orphan detection breaks.
- Blast-radius lists longer than ~10 entries are truncated with a `… (+k more)` marker in page output; tests assert on `'more)'` substring, so this truncation threshold is a tested invariant, not an implementation detail.
## Relationships
- **Calls:** ASTNode, CliRunner, FileEntry, IndexEntry, Manifest, PageContext, Path, TemporaryDirectory, _bootstrap_repo, _make_node, _parse_frontmatter, _stub_llm, build_index, build_page, compute_hash, count, delete_orphan_pages, dict, exists, glob, invoke, isinstance, isolated_filesystem, load_manifest, lower, mkdir, page_basename, page_relpath, range, read_text, run, safe_load, save_manifest, set, setattr, split, startswith, unlink, update, write_page, write_text
- **Called by:** tests/test_smart_integration.py::test_run_deletes_orphan_page_when_source_deleted, tests/test_smart_integration.py::test_smart_bails_when_no_indexable_files, tests/test_smart_integration.py::test_smart_clean_state_is_noop, tests/test_smart_integration.py::test_smart_dry_run_clean_repo_exits_zero, tests/test_smart_integration.py::test_smart_dry_run_does_not_modify_filesystem, tests/test_smart_integration.py::test_smart_dry_run_drift_exits_nonzero, tests/test_smart_integration.py::test_smart_dry_run_reports_full_initial_index_without_changes, tests/test_smart_integration.py::test_smart_fills_fresh_repo_with_no_manifest, tests/test_smart_integration.py::test_smart_fills_never_indexed_tracked_file, tests/test_smart_integration.py::test_smart_repairs_missing_wiki_page, tests/test_wiki.py::test_build_page_contains_called_by, tests/test_wiki.py::test_build_page_contains_calls, tests/test_wiki.py::test_build_page_contains_symbol, tests/test_wiki.py::test_build_page_no_agent_hints, tests/test_wiki.py::test_page_body_sections_preserved_below_frontmatter, tests/test_wiki.py::test_page_frontmatter_description_from_narrative_first_sentence, tests/test_wiki.py::test_page_frontmatter_description_generic_when_no_narrative, tests/test_wiki.py::test_page_frontmatter_is_valid_yaml_with_required_type, tests/test_wiki.py::test_page_frontmatter_tags_from_path_segments, tests/test_wiki.py::test_page_frontmatter_timestamp_passed_in_not_computed, tests/test_wiki.py::test_page_frontmatter_title_and_resource, tests/test_wiki.py::test_page_relationships_block_caps_long_lists, tests/test_wiki.py::test_page_renders_relationships_block_per_symbol, tests/test_wiki.py::test_page_starts_with_frontmatter_delimiter, tests/test_wiki.py::test_write_page_creates_file
- **Imports from:** click.testing.CliRunner, indexer.ast_parser.ASTNode, indexer.cli.main, indexer.manifest.FileEntry, indexer.manifest.Manifest, indexer.manifest.compute_hash, indexer.manifest.load_manifest, indexer.manifest.save_manifest, indexer.wiki.IndexEntry, indexer.wiki.PageContext, indexer.wiki.build_index, indexer.wiki.build_page, indexer.wiki.delete_orphan_pages, indexer.wiki.page_basename, indexer.wiki.page_relpath, indexer.wiki.write_page, pathlib.Path, subprocess, tempfile, yaml
## Entry Points
- `test_smart_rejects_combo_with_force`
- `test_smart_rejects_combo_with_staged`
- `test_smart_bails_when_no_indexable_files`
- `test_smart_dry_run_does_not_modify_filesystem`
- `test_smart_repairs_missing_wiki_page`
- `test_smart_clean_state_is_noop`
- `test_smart_fills_fresh_repo_with_no_manifest`
- `test_smart_dry_run_reports_full_initial_index_without_changes`
- `test_smart_fills_never_indexed_tracked_file`
- `test_smart_dry_run_clean_repo_exits_zero`
- `test_smart_dry_run_drift_exits_nonzero`
- `test_run_deletes_orphan_page_when_source_deleted`
- `test_build_page_contains_symbol`
- `test_build_page_contains_calls`
- `test_build_page_contains_called_by`
- `test_build_page_no_agent_hints`
- `test_build_index_contains_page`
- `test_write_page_creates_file`
- `test_page_starts_with_frontmatter_delimiter`
- `test_page_frontmatter_is_valid_yaml_with_required_type`
- `test_page_frontmatter_title_and_resource`
- `test_page_frontmatter_tags_from_path_segments`
- `test_page_frontmatter_timestamp_passed_in_not_computed`
- `test_page_frontmatter_description_from_narrative_first_sentence`
- `test_page_frontmatter_description_generic_when_no_narrative`
- `test_page_body_sections_preserved_below_frontmatter`
- `test_index_frontmatter_has_okf_version`
- `test_page_renders_relationships_block_per_symbol`
- `test_page_relationships_block_caps_long_lists`
- `test_index_renders_core_abstractions`
- `test_page_basename_root_group`
- `test_page_basename_nested_group`
- `test_page_relpath_matches_write_page`
- `test_delete_orphan_pages_removes_unreferenced`
- `test_delete_orphan_pages_noop_when_all_referenced`
- `test_delete_orphan_pages_missing_wiki_dir`
