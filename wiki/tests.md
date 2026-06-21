---
type: Code Group
title: tests
description: The tests group is the quality-gate and behavioral specification for
  kiwiskil's core pipeline.
tags:
- tests
timestamp: '2026-06-21T20:09:33.562703+00:00'
resource: tests
---
# tests/
<!-- kiwiskil:deep -->

## Overview

The tests group is the quality-gate and behavioral specification for kiwiskil's core pipeline. It covers four orthogonal subsystems: (1) ast_parser — verifying that parse_file produces correct ASTNode objects with ids, docstrings, imports, calls, and that a hash-keyed disk cache round-trips losslessly; (2) graph — specifying the pure functional call-graph layer (callers_of, callees_of, blast_radius, god_nodes, pagerank, ranked_symbols, repo_map) over synthetic ASTNode lists with no filesystem or LLM dependency; (3) config — asserting that load_config/save_config round-trip a TOML file and that partial TOML correctly falls back to Config() defaults; (4) additional test files (scip, langs, verify, manifest, smart_integration, multilang, grouper, repair_plan, llm_dispatch, init, wiki) cover the remaining pipeline stages. Tests are the executable contract for every public API in the indexer package.

## Modules
| File | Purpose |
|------|---------|
| tests/test_scip.py | Unit tests for SCIP symbol descriptor generation |
| tests/test_ast_parser.py | Unit tests for Python AST parsing and caching |
| tests/test_langs.py | Unit tests for language detection and suffix validation |
| tests/test_verify.py | Unit tests for drift detection and verification |
| tests/test_manifest.py | Unit tests for manifest file operations and staleness |
| tests/test_smart_integration.py | Integration tests for smart repair workflow |
| tests/test_graph.py | Unit tests for call graph and blast radius algorithms |
| tests/test_repair_plan.py | Unit tests for repair planning and drift correction |
| tests/test_llm_dispatch.py | Unit tests for LLM provider dispatch and CLI integration |
| tests/test_init.py | Unit tests for initialization and CLAUDE.md setup |
| tests/test_config.py | Unit tests for configuration loading and persistence |
| tests/test_wiki.py | Unit tests for wiki page and index generation |
| tests/test_multilang.py | Integration tests for Go, Java, Ruby, Rust parsers |
| tests/test_grouper.py | Unit tests for density-based folder grouping logic |
## Key Symbols
| ID | Type | Description |
|----|------|-------------|
| `tests/test_ast_parser.py::test_parse_returns_nodes` | function | Verify parse_file returns nodes list |
| `tests/test_ast_parser.py::test_function_node` | function | Verify parser extracts function nodes |
| `tests/test_ast_parser.py::test_method_node` | function | Verify parser extracts method nodes |
| `tests/test_ast_parser.py::test_class_node` | function | Verify parser extracts class nodes |
| `tests/test_ast_parser.py::test_docstring_extracted` | function | Verify parser extracts docstrings |
| `tests/test_ast_parser.py::test_imports_extracted` | function | Verify parser extracts import statements |
| `tests/test_ast_parser.py::test_calls_extracted` | function | Verify parser extracts function calls |
| `tests/test_ast_parser.py::test_cache_roundtrip` | function | Verify node cache save and load work |
| `tests/test_config.py::test_load_defaults` | function | Verify Config loads defaults from TOML |
| `tests/test_config.py::test_save_and_reload` | function | Verify Config save and load roundtrip |
| `tests/test_config.py::test_partial_toml_uses_defaults` | function | Verify partial TOML uses default values |
| `tests/test_graph.py::_node` | function | Parse node string to ASTNode object |
| `tests/test_graph.py::_chain_nodes` | function | Build call chain from node list |
| `tests/test_graph.py::test_callers_of_returns_caller_ids` | function | Verify callers_of returns caller IDs |
| `tests/test_graph.py::test_callers_of_empty_when_no_callers` | function | Verify callers_of returns empty when none exist |
| `tests/test_graph.py::test_callees_of_resolves_bare_names_to_ids` | function | Verify callees_of resolves bare names |
| `tests/test_graph.py::test_callees_of_skips_unresolvable_external_names` | function | Verify callees_of skips external names |
| `tests/test_graph.py::test_blast_radius_is_transitive_reverse_reachability` | function | Verify blast_radius computes transitive callers |
| `tests/test_graph.py::test_blast_radius_excludes_self` | function | Verify blast_radius excludes self |
| `tests/test_graph.py::test_blast_radius_leaf_caller_is_empty` | function | Verify blast_radius empty for leaf nodes |
| `tests/test_graph.py::test_blast_radius_handles_cycles` | function | Verify blast_radius handles cyclic graphs |
| `tests/test_graph.py::test_blast_radius_diamond` | function | Verify blast_radius on diamond call graph |
| `tests/test_graph.py::test_blast_radius_unknown_symbol_is_empty` | function | Verify blast_radius empty for unknown symbols |
| `tests/test_graph.py::test_god_nodes_ranks_by_degree` | function | Verify god_nodes ranks by call degree |
| `tests/test_graph.py::test_god_nodes_respects_n` | function | Verify god_nodes respects N limit |
| `tests/test_graph.py::test_god_nodes_empty_input` | function | Verify god_nodes handles empty input |
| `tests/test_graph.py::test_god_nodes_n_larger_than_nodes` | function | Verify god_nodes handles N > node count |
| `tests/test_graph.py::test_build_blast_radius_map_keys_every_node` | function | Verify blast radius map keys all nodes |
| `tests/test_graph.py::test_pagerank_keys_every_node_and_sums_to_one` | function | Verify pagerank scores sum to 1.0 |
| `tests/test_graph.py::test_pagerank_empty_input` | function | Verify pagerank handles empty input |
| `tests/test_graph.py::test_pagerank_ranks_a_hub_above_leaves` | function | Verify pagerank ranks hubs highest |
| `tests/test_graph.py::test_pagerank_is_deterministic` | function | Verify pagerank produces consistent results |
| `tests/test_graph.py::test_pagerank_handles_cycles` | function | Verify pagerank handles cyclic graphs |
| `tests/test_graph.py::test_ranked_symbols_orders_by_pagerank_desc` | function | Verify ranked_symbols sorts by pagerank |
| `tests/test_graph.py::test_ranked_symbols_empty` | function | Verify ranked_symbols handles empty input |
| `tests/test_graph.py::test_repo_map_returns_string` | function | Verify repo_map returns string output |
| `tests/test_graph.py::test_repo_map_respects_token_budget` | function | Verify repo_map respects token limit |
| `tests/test_graph.py::test_repo_map_leads_with_highest_ranked` | function | Verify repo_map prioritizes highest-ranked symbols |
| `tests/test_graph.py::test_repo_map_empty` | function | Verify repo_map handles empty input |
| `tests/test_graph.py::test_repo_map_larger_budget_includes_more` | function | Verify repo_map includes more with larger budget |
| `tests/test_grouper.py::test_sparse_folders_merge_to_parent` | function | Verify sparse folders merge to parent group |
| `tests/test_grouper.py::test_dense_folder_gets_own_page` | function | Verify dense folder gets separate page |
| `tests/test_grouper.py::test_different_folders_get_separate_groups` | function | Verify different folders get separate groups |
| `tests/test_grouper.py::test_deep_sparse_merges_upward` | function | Verify deep sparse paths merge upward |
| `tests/test_grouper.py::test_root_level_files` | function | Verify root-level files are grouped correctly |
| `tests/test_grouper.py::test_returns_all_files` | function | Verify grouper returns all files |
| `tests/test_grouper.py::test_root_files_count_correctly` | function | Verify root files counted in group density |
| `tests/test_init.py::_bootstrap_repo` | function | Bootstrap test repo with git initialization |
| `tests/test_init.py::test_init_creates_agents_md` | function | Verify init creates AGENTS.md file |
| `tests/test_init.py::test_init_creates_claude_md_unchanged_behavior` | function | Verify init creates CLAUDE.md unchanged |
| `tests/test_init.py::test_init_appends_to_existing_agents_md` | function | Verify init appends to existing AGENTS.md |
| `tests/test_init.py::test_init_does_not_duplicate_agents_md_guidance` | function | Verify init avoids duplicate guidance text |
| `tests/test_init.py::test_claude_and_agents_share_guidance_constant` | function | Verify CLAUDE.md and AGENTS.md share guidance |
| `tests/test_langs.py::test_indexable_suffixes_is_union_of_parser_sets` | function | Verify indexable suffixes cover all parsers |
| `tests/test_langs.py::test_other_suffixes_match_ts_extract_lang_configs` | function | Verify non-JS suffixes have tree-sitter configs |
| `tests/test_langs.py::test_js_ts_suffixes_match_dispatch` | function | Verify JS/TS suffixes match parser dispatch |
| `tests/test_langs.py::test_is_indexable_accepts_known_suffixes` | function | Verify is_indexable accepts known suffixes |
| `tests/test_langs.py::test_is_indexable_rejects_unknown_suffix` | function | Verify is_indexable rejects unknown suffix |
| `tests/test_langs.py::test_is_indexable_honours_part_glob` | function | Verify is_indexable respects part glob |
| `tests/test_langs.py::test_is_indexable_honours_path_glob` | function | Verify is_indexable respects path glob |
| `tests/test_llm_dispatch.py::_cfg` | function | Create Config with merged attributes |
| `tests/test_llm_dispatch.py::test_explicit_api_key_takes_priority_over_cli` | function | Verify API key overrides CLI resolution |
| `tests/test_llm_dispatch.py::test_falls_back_to_cli_when_no_key_and_cli_present` | function | Verify CLI fallback when key missing |
| `tests/test_llm_dispatch.py::test_deep_flag_uses_configured_model_cli` | function | Verify deep flag selects heavier model |
| `tests/test_llm_dispatch.py::test_no_key_no_cli_raises_so_callers_fall_back` | function | Verify error when no key and no CLI |
| `tests/test_llm_dispatch.py::test_describe_nodes_uses_cli_path_end_to_end` | function | Verifies describe_nodes returns CLI-sourced descriptions when API key absent |
| `tests/test_llm_dispatch.py::test_claude_cli_completion_invokes_print_mode` | function | Validates _claude_cli_completion invokes claude CLI with print mode, system prompt, model |
| `tests/test_llm_dispatch.py::test_claude_cli_completion_raises_on_nonzero` | function | Confirms _claude_cli_completion raises exception on non-zero exit code |
| `tests/test_llm_dispatch.py::test_clean_json_plain` | function | Tests _clean_json handles plain JSON object input |
| `tests/test_llm_dispatch.py::test_clean_json_fenced` | function | Tests _clean_json strips markdown code fence delimiters |
| `tests/test_llm_dispatch.py::test_clean_json_preamble_then_fence` | function | Tests _clean_json extracts JSON from fenced block with preamble text |
| `tests/test_llm_dispatch.py::test_clean_json_preamble_then_bare_object` | function | Tests _clean_json extracts bare JSON object after preamble text |
| `tests/test_llm_dispatch.py::test_clean_json_list_payload` | function | Tests _clean_json handles JSON array payloads |
| `tests/test_llm_dispatch.py::test_clean_json_raises_on_garbage` | function | Confirms _clean_json raises on unparseable input |
| `tests/test_llm_dispatch.py::fake_sdk` | function | Fixture providing mocked SDK instance for testing |
| `tests/test_llm_dispatch.py::fake_cli` | function | Fixture providing mocked CLI environment for testing |
| `tests/test_llm_dispatch.py::fake_cli` | function | Fixture providing mocked CLI environment for testing |
| `tests/test_llm_dispatch.py::FakeProc` | class | Mock process with configurable stdout, stderr, returncode |
| `tests/test_llm_dispatch.py::fake_run` | function | Fixture providing mocked subprocess.run for CLI testing |
| `tests/test_llm_dispatch.py::FakeProc` | class | Mock process with configurable stdout, stderr, returncode |
| `tests/test_manifest.py::test_compute_hash_stable` | function | Verifies compute_hash returns consistent hash for same file |
| `tests/test_manifest.py::test_empty_manifest_on_missing` | function | Confirms load_manifest returns empty when file absent |
| `tests/test_manifest.py::test_save_and_reload` | function | Tests save_manifest and load_manifest round-trip correctly |
| `tests/test_manifest.py::test_stale_files_detected` | function | Validates stale_files identifies modified tracked files |
| `tests/test_manifest.py::test_fresh_file_not_stale` | function | Confirms stale_files excludes unchanged files |
| `tests/test_manifest.py::test_load_manifest_missing_component_ids` | function | Tests load_manifest handles legacy format without component_ids |
| `tests/test_multilang.py::_grammar_available` | function | Checks if language grammar parser is installed |
| `tests/test_multilang.py::_by_id` | function | Helper returning symbol by ID from parsed file |
| `tests/test_multilang.py::test_go_yields_nonzero_symbols` | function | Regression: verify Go parser extracts non-zero symbols |
| `tests/test_multilang.py::test_go_function` | function | Tests Go function symbol parsing |
| `tests/test_multilang.py::test_go_struct_is_class` | function | Validates Go struct maps to class symbol type |
| `tests/test_multilang.py::test_go_method` | function | Tests Go method symbol extraction |
| `tests/test_multilang.py::test_go_docstring` | function | Validates Go docstring extraction from AST |
| `tests/test_multilang.py::test_go_calls` | function | Tests Go function call detection in symbols |
| `tests/test_multilang.py::test_go_imports` | function | Tests Go import statement parsing |
| `tests/test_multilang.py::test_java_yields_nonzero_symbols` | function | Verifies Java parser extracts symbols |
| `tests/test_multilang.py::test_java_class` | function | Tests Java class symbol parsing |
| `tests/test_multilang.py::test_java_method` | function | Tests Java instance method extraction |
| `tests/test_multilang.py::test_java_static_method` | function | Tests Java static method parsing |
| `tests/test_multilang.py::test_java_docstring` | function | Validates Java Javadoc extraction |
| `tests/test_multilang.py::test_java_calls` | function | Tests Java method call detection |
| `tests/test_multilang.py::test_java_imports` | function | Tests Java import parsing |
| `tests/test_multilang.py::test_ruby_yields_nonzero_symbols` | function | Verifies Ruby parser extracts symbols |
| `tests/test_multilang.py::test_ruby_class_and_module` | function | Tests Ruby class and module symbol parsing |
| `tests/test_multilang.py::test_ruby_method` | function | Tests Ruby method symbol extraction |
| `tests/test_multilang.py::test_ruby_top_level_function` | function | Tests Ruby function-level definition parsing |
| `tests/test_multilang.py::test_ruby_docstring` | function | Validates Ruby docstring extraction |
| `tests/test_multilang.py::test_ruby_calls` | function | Tests Ruby function call detection |
| `tests/test_multilang.py::test_rust_yields_nonzero_symbols` | function | Verifies Rust parser extracts symbols |
| `tests/test_multilang.py::test_rust_struct_and_trait_are_classes` | function | Validates Rust struct/trait map to class type |
| `tests/test_multilang.py::test_rust_free_function` | function | Tests Rust top-level function parsing |
| `tests/test_multilang.py::test_rust_impl_method` | function | Tests Rust impl block method extraction |
| `tests/test_multilang.py::test_rust_docstring` | function | Validates Rust doc comment extraction |
| `tests/test_multilang.py::test_rust_calls` | function | Tests Rust function call detection |
| `tests/test_multilang.py::test_unsupported_suffix_returns_empty` | function | Confirms unsupported file types yield zero symbols |
| `tests/test_repair_plan.py::_empty_manifest` | function | Fixture providing empty Manifest for testing |
| `tests/test_repair_plan.py::test_clean_report_produces_empty_plan` | function | Verifies plan is empty when no issues found |
| `tests/test_repair_plan.py::test_stale_and_untracked_files_go_to_reindex` | function | Confirms stale/untracked files queued for reindex |
| `tests/test_repair_plan.py::test_missing_wiki_page_pulls_files_from_manifest` | function | Validates missing pages collect relevant files |
| `tests/test_repair_plan.py::test_pages_missing_deep_included_when_deep_active` | function | Confirms deep pages included when deep mode enabled |
| `tests/test_repair_plan.py::test_pages_missing_deep_excluded_when_skip_deep` | function | Verifies deep pages excluded when skip_deep set |
| `tests/test_repair_plan.py::test_cleanup_ops_carried_through` | function | Validates cleanup operations preserved in plan |
| `tests/test_repair_plan.py::test_execute_restores_agents_md` | function | Confirms execute restores AGENTS.md on empty plan |
| `tests/test_repair_plan.py::test_execute_deletes_orphan_pages_and_prunes_manifest` | function | Validates execute removes orphan pages, updates manifest |
| `tests/test_repair_plan.py::test_execute_runs_reindex_for_files` | function | Confirms execute invokes reindex for stale files |
| `tests/test_repair_plan.py::fake_index_files` | function | Fixture providing mocked index_files function |
| `tests/test_repair_plan.py::fake_finalise` | function | Fixture providing mocked finalise function |
| `tests/test_scip.py::_node` | function | Helper creating ASTNode from symbol string |
| `tests/test_scip.py::test_top_level_function` | function | Tests SCIP symbol generation for function |
| `tests/test_scip.py::test_class` | function | Tests SCIP symbol generation for class |
| `tests/test_scip.py::test_method` | function | Tests SCIP symbol generation for method |
| `tests/test_scip.py::test_method_with_dotted_class_path_uses_last_segment_as_member` | function | Validates SCIP uses last segment of dotted path |
| `tests/test_scip.py::test_root_level_file` | function | Tests SCIP symbol for root-level file |
| `tests/test_scip.py::test_is_deterministic` | function | Confirms SCIP symbol generation is deterministic |
| `tests/test_scip.py::test_unknown_type_falls_back_to_term` | function | Validates unknown symbol types default to term |
| `tests/test_scip.py::test_malformed_id_without_separator_is_safe` | function | Confirms malformed IDs handled gracefully |
| `tests/test_smart_integration.py::_bootstrap_repo` | function | Fixture initializing git repo with .gitignore |
| `tests/test_smart_integration.py::test_smart_rejects_combo_with_force` | function | Confirms smart rejects --force with other flags |
| `tests/test_smart_integration.py::test_smart_rejects_combo_with_staged` | function | Confirms smart rejects --staged with other flags |
| `tests/test_smart_integration.py::test_smart_bails_when_no_indexable_files` | function | Validates smart exits when no parseable files found |
| `tests/test_smart_integration.py::test_smart_dry_run_does_not_modify_filesystem` | function | Verifies --dry-run makes no persistent changes |
| `tests/test_smart_integration.py::_stub_llm` | function | Fixture mocking LLM to return fixed descriptions |
| `tests/test_smart_integration.py::test_smart_repairs_missing_wiki_page` | function | Confirms smart generates missing wiki page |
| `tests/test_smart_integration.py::test_smart_clean_state_is_noop` | function | Validates smart is no-op when index current |
| `tests/test_smart_integration.py::test_smart_fills_fresh_repo_with_no_manifest` | function | Confirms smart creates manifest and wiki for new repo |
| `tests/test_smart_integration.py::test_smart_dry_run_reports_full_initial_index_without_changes` | function | Validates dry-run reports full initial index |
| `tests/test_smart_integration.py::test_smart_fills_never_indexed_tracked_file` | function | Confirms smart indexes tracked files not in manifest |
| `tests/test_smart_integration.py::test_smart_dry_run_clean_repo_exits_zero` | function | Verifies dry-run exits 0 on clean state |
| `tests/test_smart_integration.py::test_smart_dry_run_drift_exits_nonzero` | function | Validates dry-run exits non-zero on drift |
| `tests/test_verify.py::_make_repo_with_manifest` | function | Helper creating test repo with manifest file |
| `tests/test_verify.py::test_empty_report_is_clean` | function | Confirms empty report has zero issues, is clean |
| `tests/test_verify.py::test_report_with_stale_files_not_clean` | function | Validates stale files cause non-clean status |
| `tests/test_verify.py::test_report_counts_all_drift_classes` | function | Confirms report totals all drift issue types |
| `tests/test_verify.py::test_scan_flags_missing_manifest` | function | Tests scan detects missing manifest file |
| `tests/test_verify.py::test_scan_detects_stale_files` | function | Verifies scan detects source files missing from manifest |
| `tests/test_verify.py::test_scan_detects_dangling_manifest_entries` | function | Verifies scan detects manifest entries referencing non-existent files |
| `tests/test_verify.py::test_scan_detects_untracked_source_files` | function | Verifies scan detects source files not listed in manifest |
| `tests/test_verify.py::test_scan_detects_missing_wiki_page` | function | Verifies scan detects manifest entries without corresponding wiki pages |
| `tests/test_verify.py::test_scan_detects_orphan_wiki_page` | function | Verifies scan detects wiki pages lacking manifest entries |
| `tests/test_verify.py::test_scan_detects_missing_index_and_skill` | function | Verifies scan detects missing wiki index and skill components |
| `tests/test_verify.py::_seed_valid_state` | function | Helper to create fully-valid filesystem and manifest for drift tests |
| `tests/test_verify.py::test_scan_detects_missing_claude_md_snippet` | function | Verifies scan detects missing CLAUDE.md configuration snippet |
| `tests/test_verify.py::test_scan_detects_missing_agents_md_snippet` | function | Verifies scan detects missing AGENTS.md configuration snippet |
| `tests/test_verify.py::test_scan_agents_md_present_and_valid_not_flagged` | function | Verifies scan does not flag valid AGENTS.md as drift |
| `tests/test_verify.py::test_scan_detects_missing_gitignore_entry` | function | Verifies scan detects missing .indexer entry in .gitignore |
| `tests/test_verify.py::test_scan_detects_hook_drift` | function | Verifies scan detects pre-commit hook file drift or absence |
| `tests/test_verify.py::test_scan_detects_pages_missing_deep_sections` | function | Verifies scan detects deep-enriched pages lacking required sections |
| `tests/test_verify.py::test_scan_deep_page_with_empty_narrative_not_flagged` | function | Verifies empty LLM narrative in deep page does not trigger false drift |
| `tests/test_verify.py::test_scan_skips_deep_check_when_skip_deep_true` | function | Verifies scan skips deep-section checks when skip_deep enabled |
| `tests/test_verify.py::test_print_report_clean` | function | Verifies print_report outputs clean state when no drift detected |
| `tests/test_verify.py::test_print_report_lists_each_drift` | function | Verifies print_report lists each detected drift issue |
| `tests/test_verify.py::test_scan_skips_hook_check_when_check_hook_false` | function | Verifies scan skips hook drift check when check_hook disabled |
| `tests/test_wiki.py::_make_node` | function | Helper to construct ASTNode dict with test attributes |
| `tests/test_wiki.py::test_build_page_contains_symbol` | function | Verifies page builder includes symbol definitions |
| `tests/test_wiki.py::test_build_page_contains_calls` | function | Verifies page builder includes function call relationships |
| `tests/test_wiki.py::test_build_page_contains_called_by` | function | Verifies page builder includes caller relationships |
| `tests/test_wiki.py::test_build_page_no_agent_hints` | function | Verifies page builder excludes agent hints from content |
| `tests/test_wiki.py::test_build_index_contains_page` | function | Verifies index builder includes page entries |
| `tests/test_wiki.py::test_write_page_creates_file` | function | Verifies write_page creates wiki markdown file |
| `tests/test_wiki.py::_parse_frontmatter` | function | Extract and YAML-parse leading frontmatter block |
| `tests/test_wiki.py::test_page_starts_with_frontmatter_delimiter` | function | Verifies page starts with YAML frontmatter delimiter |
| `tests/test_wiki.py::test_page_frontmatter_is_valid_yaml_with_required_type` | function | Verifies frontmatter is valid YAML with required type field |
| `tests/test_wiki.py::test_page_frontmatter_title_and_resource` | function | Verifies frontmatter includes title and resource fields |
| `tests/test_wiki.py::test_page_frontmatter_tags_from_path_segments` | function | Verifies frontmatter tags derived from file path segments |
| `tests/test_wiki.py::test_page_frontmatter_timestamp_passed_in_not_computed` | function | Verifies frontmatter timestamp comes from parameter, not computed |
| `tests/test_wiki.py::test_page_frontmatter_description_from_narrative_first_sentence` | function | Verifies frontmatter description extracted from narrative first sentence |
| `tests/test_wiki.py::test_page_frontmatter_description_generic_when_no_narrative` | function | Verifies frontmatter uses generic description when narrative absent |
| `tests/test_wiki.py::test_page_body_sections_preserved_below_frontmatter` | function | Verifies page preserves body sections below frontmatter |
| `tests/test_wiki.py::test_index_frontmatter_has_okf_version` | function | Verifies index frontmatter includes OKF version field |
| `tests/test_wiki.py::test_page_renders_relationships_block_per_symbol` | function | Verifies page renders relationships block for each symbol |
| `tests/test_wiki.py::test_page_relationships_block_caps_long_lists` | function | Verifies page relationships block truncates long reference lists |
| `tests/test_wiki.py::test_index_renders_core_abstractions` | function | Verifies index builder includes core abstractions |
| `tests/test_wiki.py::test_page_basename_root_group` | function | Verifies page_basename generates correct path for root group |
| `tests/test_wiki.py::test_page_basename_nested_group` | function | Verifies page_basename generates correct path for nested group |
| `tests/test_wiki.py::test_page_relpath_matches_write_page` | function | Verifies page_relpath matches actual file path from write_page |
## Symbol Relationships
### `test_parse_returns_nodes`
- **Callers (0):** none
- **Calls:** len, parse_file
- **Editing this affects:** none
### `test_function_node`
- **Callers (0):** none
- **Calls:** any, parse_file
- **Editing this affects:** none
### `test_method_node`
- **Callers (0):** none
- **Calls:** any, parse_file
- **Editing this affects:** none
### `test_class_node`
- **Callers (0):** none
- **Calls:** any, endswith, parse_file
- **Editing this affects:** none
### `test_docstring_extracted`
- **Callers (0):** none
- **Calls:** next, parse_file
- **Editing this affects:** none
### `test_imports_extracted`
- **Callers (0):** none
- **Calls:** isinstance, len, next, parse_file
- **Editing this affects:** none
### `test_calls_extracted`
- **Callers (0):** none
- **Calls:** next, parse_file
- **Editing this affects:** none
### `test_cache_roundtrip`
- **Callers (0):** none
- **Calls:** Path, TemporaryDirectory, len, load_cached_nodes, parse_file, save_cached_nodes
- **Editing this affects:** none
### `test_load_defaults`
- **Callers (0):** none
- **Calls:** Config, Path, TemporaryDirectory, load_config
- **Editing this affects:** none
### `test_save_and_reload`
- **Callers (0):** none
- **Calls:** Config, Path, TemporaryDirectory, load_config, save_config
- **Editing this affects:** none
### `test_partial_toml_uses_defaults`
- **Callers (0):** none
- **Calls:** Config, Path, TemporaryDirectory, load_config, write_bytes
- **Editing this affects:** none
### `_node`
- **Callers (19):** _chain_nodes, test_blast_radius_diamond, test_blast_radius_handles_cycles, test_callees_of_skips_unresolvable_external_names, test_class, test_god_nodes_ranks_by_degree, test_is_deterministic, test_malformed_id_without_separator_is_safe … (+11 more)
- **Calls:** ASTNode, split
- **Editing this affects:** _chain_nodes, test_blast_radius_diamond, test_blast_radius_excludes_self, test_blast_radius_handles_cycles, test_blast_radius_is_transitive_reverse_reachability, test_blast_radius_leaf_caller_is_empty, test_blast_radius_unknown_symbol_is_empty, test_build_blast_radius_map_keys_every_node … (+24 more)
### `_chain_nodes`
- **Callers (13):** test_blast_radius_excludes_self, test_blast_radius_is_transitive_reverse_reachability, test_blast_radius_leaf_caller_is_empty, test_blast_radius_unknown_symbol_is_empty, test_build_blast_radius_map_keys_every_node, test_callees_of_resolves_bare_names_to_ids, test_callers_of_empty_when_no_callers, test_callers_of_returns_caller_ids … (+5 more)
- **Calls:** _node
- **Editing this affects:** test_blast_radius_excludes_self, test_blast_radius_is_transitive_reverse_reachability, test_blast_radius_leaf_caller_is_empty, test_blast_radius_unknown_symbol_is_empty, test_build_blast_radius_map_keys_every_node, test_callees_of_resolves_bare_names_to_ids, test_callers_of_empty_when_no_callers, test_callers_of_returns_caller_ids … (+5 more)
### `test_callers_of_returns_caller_ids`
- **Callers (0):** none
- **Calls:** _chain_nodes, callers_of
- **Editing this affects:** none
### `test_callers_of_empty_when_no_callers`
- **Callers (0):** none
- **Calls:** _chain_nodes, callers_of
- **Editing this affects:** none
### `test_callees_of_resolves_bare_names_to_ids`
- **Callers (0):** none
- **Calls:** _chain_nodes, callees_of
- **Editing this affects:** none
### `test_callees_of_skips_unresolvable_external_names`
- **Callers (0):** none
- **Calls:** _node, callees_of
- **Editing this affects:** none
### `test_blast_radius_is_transitive_reverse_reachability`
- **Callers (0):** none
- **Calls:** _chain_nodes, blast_radius
- **Editing this affects:** none
### `test_blast_radius_excludes_self`
- **Callers (0):** none
- **Calls:** _chain_nodes, blast_radius
- **Editing this affects:** none
### `test_blast_radius_leaf_caller_is_empty`
- **Callers (0):** none
- **Calls:** _chain_nodes, blast_radius, set
- **Editing this affects:** none
### `test_blast_radius_handles_cycles`
- **Callers (0):** none
- **Calls:** _node, blast_radius
- **Editing this affects:** none
### `test_blast_radius_diamond`
- **Callers (0):** none
- **Calls:** _node, blast_radius
- **Editing this affects:** none
### `test_blast_radius_unknown_symbol_is_empty`
- **Callers (0):** none
- **Calls:** _chain_nodes, blast_radius, set
- **Editing this affects:** none
### `test_god_nodes_ranks_by_degree`
- **Callers (0):** none
- **Calls:** _node, god_nodes
- **Editing this affects:** none
### `test_god_nodes_respects_n`
- **Callers (0):** none
- **Calls:** _chain_nodes, god_nodes, len
- **Editing this affects:** none
### `test_god_nodes_empty_input`
- **Callers (0):** none
- **Calls:** god_nodes
- **Editing this affects:** none
### `test_god_nodes_n_larger_than_nodes`
- **Callers (0):** none
- **Calls:** _chain_nodes, god_nodes, len
- **Editing this affects:** none
### `test_build_blast_radius_map_keys_every_node`
- **Callers (0):** none
- **Calls:** _chain_nodes, build_blast_radius_map, keys, set
- **Editing this affects:** none
### `test_pagerank_keys_every_node_and_sums_to_one`
- **Callers (0):** none
- **Calls:** _chain_nodes, abs, keys, pagerank, set, sum, values
- **Editing this affects:** none
### `test_pagerank_empty_input`
- **Callers (0):** none
- **Calls:** pagerank
- **Editing this affects:** none
### `test_pagerank_ranks_a_hub_above_leaves`
- **Callers (0):** none
- **Calls:** _node, pagerank
- **Editing this affects:** none
### `test_pagerank_is_deterministic`
- **Callers (0):** none
- **Calls:** _chain_nodes, pagerank
- **Editing this affects:** none
### `test_pagerank_handles_cycles`
- **Callers (0):** none
- **Calls:** _node, abs, pagerank, sum, values
- **Editing this affects:** none
### `test_ranked_symbols_orders_by_pagerank_desc`
- **Callers (0):** none
- **Calls:** _node, len, ranked_symbols
- **Editing this affects:** none
### `test_ranked_symbols_empty`
- **Callers (0):** none
- **Calls:** ranked_symbols
- **Editing this affects:** none
### `test_repo_map_returns_string`
- **Callers (0):** none
- **Calls:** _chain_nodes, isinstance, repo_map
- **Editing this affects:** none
### `test_repo_map_respects_token_budget`
- **Callers (0):** none
- **Calls:** _node, count, len, range, repo_map
- **Editing this affects:** none
### `test_repo_map_leads_with_highest_ranked`
- **Callers (0):** none
- **Calls:** _node, index, repo_map
- **Editing this affects:** none
### `test_repo_map_empty`
- **Callers (0):** none
- **Calls:** repo_map
- **Editing this affects:** none
### `test_repo_map_larger_budget_includes_more`
- **Callers (0):** none
- **Calls:** _node, len, range, repo_map
- **Editing this affects:** none
### `test_sparse_folders_merge_to_parent`
- **Callers (0):** none
- **Calls:** all, density_group, values
- **Editing this affects:** none
### `test_dense_folder_gets_own_page`
- **Callers (0):** none
- **Calls:** all, density_group, len, range, set, values
- **Editing this affects:** none
### `test_different_folders_get_separate_groups`
- **Callers (0):** none
- **Calls:** density_group
- **Editing this affects:** none
### `test_deep_sparse_merges_upward`
- **Callers (0):** none
- **Calls:** density_group
- **Editing this affects:** none
### `test_root_level_files`
- **Callers (0):** none
- **Calls:** density_group
- **Editing this affects:** none
### `test_returns_all_files`
- **Callers (0):** none
- **Calls:** density_group, keys, set
- **Editing this affects:** none
### `test_root_files_count_correctly`
- **Callers (0):** none
- **Calls:** all, density_group, values
- **Editing this affects:** none
### `_bootstrap_repo`
- **Callers (14):** test_claude_and_agents_share_guidance_constant, test_init_appends_to_existing_agents_md, test_init_creates_agents_md, test_init_creates_claude_md_unchanged_behavior, test_init_does_not_duplicate_agents_md_guidance, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero … (+6 more)
- **Calls:** run
- **Editing this affects:** test_claude_and_agents_share_guidance_constant, test_init_appends_to_existing_agents_md, test_init_creates_agents_md, test_init_creates_claude_md_unchanged_behavior, test_init_does_not_duplicate_agents_md_guidance, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero … (+6 more)
### `test_init_creates_agents_md`
- **Callers (0):** none
- **Calls:** CliRunner, Path, _bootstrap_repo, exists, invoke, isolated_filesystem, read_text
- **Editing this affects:** none
### `test_init_creates_claude_md_unchanged_behavior`
- **Callers (0):** none
- **Calls:** CliRunner, Path, _bootstrap_repo, exists, invoke, isolated_filesystem, read_text
- **Editing this affects:** none
### `test_init_appends_to_existing_agents_md`
- **Callers (0):** none
- **Calls:** CliRunner, Path, _bootstrap_repo, invoke, isolated_filesystem, read_text, write_text
- **Editing this affects:** none
### `test_init_does_not_duplicate_agents_md_guidance`
- **Callers (0):** none
- **Calls:** CliRunner, Path, _bootstrap_repo, count, invoke, isolated_filesystem, read_text
- **Editing this affects:** none
### `test_claude_and_agents_share_guidance_constant`
- **Callers (0):** none
- **Calls:** CliRunner, Path, _bootstrap_repo, invoke, isolated_filesystem, read_text, strip
- **Editing this affects:** none
### `test_other_suffixes_match_ts_extract_lang_configs`
- **Callers (0):** none
- **Calls:** keys, set
- **Editing this affects:** none
### `test_js_ts_suffixes_match_dispatch`
- **Callers (0):** none
- **Calls:** getsource, repr
- **Editing this affects:** none
### `test_is_indexable_accepts_known_suffixes`
- **Callers (0):** none
- **Calls:** is_indexable
- **Editing this affects:** none
### `test_is_indexable_rejects_unknown_suffix`
- **Callers (0):** none
- **Calls:** is_indexable
- **Editing this affects:** none
### `test_is_indexable_honours_part_glob`
- **Callers (0):** none
- **Calls:** is_indexable
- **Editing this affects:** none
### `test_is_indexable_honours_path_glob`
- **Callers (0):** none
- **Calls:** is_indexable
- **Editing this affects:** none
### `_cfg`
- **Callers (5):** test_deep_flag_uses_configured_model_cli, test_describe_nodes_uses_cli_path_end_to_end, test_explicit_api_key_takes_priority_over_cli, test_falls_back_to_cli_when_no_key_and_cli_present, test_no_key_no_cli_raises_so_callers_fall_back
- **Calls:** Config, items, setattr
- **Editing this affects:** test_deep_flag_uses_configured_model_cli, test_describe_nodes_uses_cli_path_end_to_end, test_explicit_api_key_takes_priority_over_cli, test_falls_back_to_cli_when_no_key_and_cli_present, test_no_key_no_cli_raises_so_callers_fall_back
### `test_explicit_api_key_takes_priority_over_cli`
- **Callers (0):** none
- **Calls:** _cfg, _complete, setattr
- **Editing this affects:** none
### `test_falls_back_to_cli_when_no_key_and_cli_present`
- **Callers (0):** none
- **Calls:** _cfg, _complete, setattr
- **Editing this affects:** none
### `test_deep_flag_uses_configured_model_cli`
- **Callers (0):** none
- **Calls:** _cfg, _complete, any, setattr, setdefault
- **Editing this affects:** none
### `test_no_key_no_cli_raises_so_callers_fall_back`
- **Callers (0):** none
- **Calls:** _cfg, _complete, raises, setattr
- **Editing this affects:** none
### `test_describe_nodes_uses_cli_path_end_to_end`
- **Callers (0):** none
- **Calls:** ASTNode, _cfg, describe_nodes, setattr
- **Editing this affects:** none
### `test_claude_cli_completion_invokes_print_mode`
- **Callers (0):** none
- **Calls:** FakeProc, _claude_cli_completion, any, get, setattr, startswith
- **Editing this affects:** none
### `test_claude_cli_completion_raises_on_nonzero`
- **Callers (0):** none
- **Calls:** FakeProc, _claude_cli_completion, raises, setattr
- **Editing this affects:** none
### `test_clean_json_plain`
- **Callers (0):** none
- **Calls:** _clean_json
- **Editing this affects:** none
### `test_clean_json_fenced`
- **Callers (0):** none
- **Calls:** _clean_json
- **Editing this affects:** none
### `test_clean_json_preamble_then_fence`
- **Callers (0):** none
- **Calls:** _clean_json
- **Editing this affects:** none
### `test_clean_json_preamble_then_bare_object`
- **Callers (0):** none
- **Calls:** _clean_json
- **Editing this affects:** none
### `test_clean_json_list_payload`
- **Callers (0):** none
- **Calls:** _clean_json
- **Editing this affects:** none
### `test_clean_json_raises_on_garbage`
- **Callers (0):** none
- **Calls:** _clean_json, raises
- **Editing this affects:** none
### `FakeProc`
- **Callers (3):** fake_run, test_claude_cli_completion_invokes_print_mode, test_claude_cli_completion_raises_on_nonzero
- **Calls:** none
- **Editing this affects:** fake_run, test_claude_cli_completion_invokes_print_mode, test_claude_cli_completion_raises_on_nonzero
### `fake_run`
- **Callers (0):** none
- **Calls:** FakeProc, get
- **Editing this affects:** none
### `FakeProc`
- **Callers (3):** fake_run, test_claude_cli_completion_invokes_print_mode, test_claude_cli_completion_raises_on_nonzero
- **Calls:** none
- **Editing this affects:** fake_run, test_claude_cli_completion_invokes_print_mode, test_claude_cli_completion_raises_on_nonzero
### `test_compute_hash_stable`
- **Callers (0):** none
- **Calls:** NamedTemporaryFile, Path, compute_hash, startswith, write
- **Editing this affects:** none
### `test_empty_manifest_on_missing`
- **Callers (0):** none
- **Calls:** Path, TemporaryDirectory, load_manifest
- **Editing this affects:** none
### `test_save_and_reload`
- **Callers (0):** none
- **Calls:** FileEntry, Manifest, Path, TemporaryDirectory, load_manifest, save_manifest
- **Editing this affects:** none
### `test_stale_files_detected`
- **Callers (0):** none
- **Calls:** FileEntry, Manifest, Path, TemporaryDirectory, stale_files, write_text
- **Editing this affects:** none
### `test_fresh_file_not_stale`
- **Callers (0):** none
- **Calls:** FileEntry, Manifest, Path, TemporaryDirectory, compute_hash, stale_files, write_text
- **Editing this affects:** none
### `test_load_manifest_missing_component_ids`
- **Callers (0):** none
- **Calls:** Path, TemporaryDirectory, dumps, load_manifest, mkdir, write_text
- **Editing this affects:** none
### `_grammar_available`
- **Callers (0):** none
- **Calls:** __import__
- **Editing this affects:** none
### `_by_id`
- **Callers (22):** test_go_calls, test_go_docstring, test_go_function, test_go_imports, test_go_method, test_go_struct_is_class, test_java_calls, test_java_class … (+14 more)
- **Calls:** none
- **Editing this affects:** test_go_calls, test_go_docstring, test_go_function, test_go_imports, test_go_method, test_go_struct_is_class, test_java_calls, test_java_class … (+14 more)
### `test_go_yields_nonzero_symbols`
- **Callers (0):** none
- **Calls:** len, parse_file
- **Editing this affects:** none
### `test_go_function`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_go_struct_is_class`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_go_method`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_go_docstring`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_go_calls`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_go_imports`
- **Callers (0):** none
- **Calls:** _by_id, len, parse_file
- **Editing this affects:** none
### `test_java_yields_nonzero_symbols`
- **Callers (0):** none
- **Calls:** len, parse_file
- **Editing this affects:** none
### `test_java_class`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_java_method`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_java_static_method`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_java_docstring`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_java_calls`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_java_imports`
- **Callers (0):** none
- **Calls:** _by_id, len, parse_file
- **Editing this affects:** none
### `test_ruby_yields_nonzero_symbols`
- **Callers (0):** none
- **Calls:** len, parse_file
- **Editing this affects:** none
### `test_ruby_class_and_module`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_ruby_method`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_ruby_top_level_function`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_ruby_docstring`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_ruby_calls`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_rust_yields_nonzero_symbols`
- **Callers (0):** none
- **Calls:** len, parse_file
- **Editing this affects:** none
### `test_rust_struct_and_trait_are_classes`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_rust_free_function`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_rust_impl_method`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_rust_docstring`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_rust_calls`
- **Callers (0):** none
- **Calls:** _by_id, parse_file
- **Editing this affects:** none
### `test_unsupported_suffix_returns_empty`
- **Callers (0):** none
- **Calls:** parse_file, write_text
- **Editing this affects:** none
### `_empty_manifest`
- **Callers (4):** test_clean_report_produces_empty_plan, test_cleanup_ops_carried_through, test_execute_restores_agents_md, test_stale_and_untracked_files_go_to_reindex
- **Calls:** Manifest
- **Editing this affects:** test_clean_report_produces_empty_plan, test_cleanup_ops_carried_through, test_execute_restores_agents_md, test_stale_and_untracked_files_go_to_reindex
### `test_clean_report_produces_empty_plan`
- **Callers (0):** none
- **Calls:** Config, Path, TemporaryDirectory, VerifyReport, _empty_manifest, plan
- **Editing this affects:** none
### `test_stale_and_untracked_files_go_to_reindex`
- **Callers (0):** none
- **Calls:** Config, Path, TemporaryDirectory, VerifyReport, _empty_manifest, plan, sorted
- **Editing this affects:** none
### `test_missing_wiki_page_pulls_files_from_manifest`
- **Callers (0):** none
- **Calls:** Config, FileEntry, Manifest, Path, TemporaryDirectory, VerifyReport, plan, sorted
- **Editing this affects:** none
### `test_pages_missing_deep_included_when_deep_active`
- **Callers (0):** none
- **Calls:** Config, FileEntry, Manifest, Path, TemporaryDirectory, VerifyReport, plan
- **Editing this affects:** none
### `test_pages_missing_deep_excluded_when_skip_deep`
- **Callers (0):** none
- **Calls:** Config, FileEntry, Manifest, Path, TemporaryDirectory, VerifyReport, plan
- **Editing this affects:** none
### `test_cleanup_ops_carried_through`
- **Callers (0):** none
- **Calls:** Config, Path, TemporaryDirectory, VerifyReport, _empty_manifest, plan
- **Editing this affects:** none
### `test_execute_restores_agents_md`
- **Callers (0):** none
- **Calls:** Config, VerifyReport, _empty_manifest, execute, exists, plan, read_text
- **Editing this affects:** none
### `test_execute_deletes_orphan_pages_and_prunes_manifest`
- **Callers (0):** none
- **Calls:** Config, FileEntry, Manifest, Path, RepairPlan, TemporaryDirectory, execute, exists … (+2 more)
- **Editing this affects:** none
### `test_execute_runs_reindex_for_files`
- **Callers (0):** none
- **Calls:** Config, Manifest, Path, RepairPlan, TemporaryDirectory, execute, setattr
- **Editing this affects:** none
### `_node`
- **Callers (19):** _chain_nodes, test_blast_radius_diamond, test_blast_radius_handles_cycles, test_callees_of_skips_unresolvable_external_names, test_class, test_god_nodes_ranks_by_degree, test_is_deterministic, test_malformed_id_without_separator_is_safe … (+11 more)
- **Calls:** ASTNode, split
- **Editing this affects:** _chain_nodes, test_blast_radius_diamond, test_blast_radius_excludes_self, test_blast_radius_handles_cycles, test_blast_radius_is_transitive_reverse_reachability, test_blast_radius_leaf_caller_is_empty, test_blast_radius_unknown_symbol_is_empty, test_build_blast_radius_map_keys_every_node … (+24 more)
### `test_top_level_function`
- **Callers (0):** none
- **Calls:** _node, scip_symbol
- **Editing this affects:** none
### `test_class`
- **Callers (0):** none
- **Calls:** _node, scip_symbol
- **Editing this affects:** none
### `test_method`
- **Callers (0):** none
- **Calls:** _node, scip_symbol
- **Editing this affects:** none
### `test_method_with_dotted_class_path_uses_last_segment_as_member`
- **Callers (0):** none
- **Calls:** _node, scip_symbol
- **Editing this affects:** none
### `test_root_level_file`
- **Callers (0):** none
- **Calls:** _node, scip_symbol
- **Editing this affects:** none
### `test_is_deterministic`
- **Callers (0):** none
- **Calls:** _node, scip_symbol
- **Editing this affects:** none
### `test_unknown_type_falls_back_to_term`
- **Callers (0):** none
- **Calls:** _node, scip_symbol
- **Editing this affects:** none
### `test_malformed_id_without_separator_is_safe`
- **Callers (0):** none
- **Calls:** _node, scip_symbol
- **Editing this affects:** none
### `_bootstrap_repo`
- **Callers (14):** test_claude_and_agents_share_guidance_constant, test_init_appends_to_existing_agents_md, test_init_creates_agents_md, test_init_creates_claude_md_unchanged_behavior, test_init_does_not_duplicate_agents_md_guidance, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero … (+6 more)
- **Calls:** run
- **Editing this affects:** test_claude_and_agents_share_guidance_constant, test_init_appends_to_existing_agents_md, test_init_creates_agents_md, test_init_creates_claude_md_unchanged_behavior, test_init_does_not_duplicate_agents_md_guidance, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero … (+6 more)
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
- **Callers (6):** test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero, test_smart_dry_run_reports_full_initial_index_without_changes, test_smart_fills_fresh_repo_with_no_manifest, test_smart_fills_never_indexed_tracked_file, test_smart_repairs_missing_wiki_page
- **Calls:** setattr
- **Editing this affects:** test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero, test_smart_dry_run_reports_full_initial_index_without_changes, test_smart_fills_fresh_repo_with_no_manifest, test_smart_fills_never_indexed_tracked_file, test_smart_repairs_missing_wiki_page
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
### `_make_repo_with_manifest`
- **Callers (3):** test_scan_detects_dangling_manifest_entries, test_scan_detects_stale_files, test_scan_detects_untracked_source_files
- **Calls:** Manifest, items, mkdir, write_text
- **Editing this affects:** test_scan_detects_dangling_manifest_entries, test_scan_detects_stale_files, test_scan_detects_untracked_source_files
### `test_empty_report_is_clean`
- **Callers (0):** none
- **Calls:** VerifyReport, is_clean, total_issues
- **Editing this affects:** none
### `test_report_with_stale_files_not_clean`
- **Callers (0):** none
- **Calls:** VerifyReport, is_clean, total_issues
- **Editing this affects:** none
### `test_report_counts_all_drift_classes`
- **Callers (0):** none
- **Calls:** VerifyReport, is_clean, total_issues
- **Editing this affects:** none
### `test_scan_flags_missing_manifest`
- **Callers (0):** none
- **Calls:** Config, Manifest, Path, TemporaryDirectory, scan
- **Editing this affects:** none
### `test_scan_detects_stale_files`
- **Callers (0):** none
- **Calls:** Config, FileEntry, Path, TemporaryDirectory, _make_repo_with_manifest, scan, setattr
- **Editing this affects:** none
### `test_scan_detects_dangling_manifest_entries`
- **Callers (0):** none
- **Calls:** Config, FileEntry, Path, TemporaryDirectory, _make_repo_with_manifest, scan, setattr
- **Editing this affects:** none
### `test_scan_detects_untracked_source_files`
- **Callers (0):** none
- **Calls:** Config, FileEntry, Path, TemporaryDirectory, _make_repo_with_manifest, scan, setattr
- **Editing this affects:** none
### `test_scan_detects_missing_wiki_page`
- **Callers (0):** none
- **Calls:** Config, FileEntry, Manifest, Path, TemporaryDirectory, compute_hash, scan, setattr … (+1 more)
- **Editing this affects:** none
### `test_scan_detects_orphan_wiki_page`
- **Callers (0):** none
- **Calls:** Config, FileEntry, Manifest, Path, TemporaryDirectory, compute_hash, mkdir, scan … (+2 more)
- **Editing this affects:** none
### `test_scan_detects_missing_index_and_skill`
- **Callers (0):** none
- **Calls:** Config, FileEntry, Manifest, Path, TemporaryDirectory, compute_hash, mkdir, scan … (+2 more)
- **Editing this affects:** none
### `_seed_valid_state`
- **Callers (6):** test_scan_agents_md_present_and_valid_not_flagged, test_scan_detects_hook_drift, test_scan_detects_missing_agents_md_snippet, test_scan_detects_missing_claude_md_snippet, test_scan_detects_missing_gitignore_entry, test_scan_skips_hook_check_when_check_hook_false
- **Calls:** FileEntry, Manifest, compute_hash, mkdir, write_text
- **Editing this affects:** test_scan_agents_md_present_and_valid_not_flagged, test_scan_detects_hook_drift, test_scan_detects_missing_agents_md_snippet, test_scan_detects_missing_claude_md_snippet, test_scan_detects_missing_gitignore_entry, test_scan_skips_hook_check_when_check_hook_false
### `test_scan_detects_missing_claude_md_snippet`
- **Callers (0):** none
- **Calls:** Config, Path, TemporaryDirectory, _seed_valid_state, scan, setattr, write_text
- **Editing this affects:** none
### `test_scan_detects_missing_agents_md_snippet`
- **Callers (0):** none
- **Calls:** Config, Path, TemporaryDirectory, _seed_valid_state, scan, setattr, write_text
- **Editing this affects:** none
### `test_scan_agents_md_present_and_valid_not_flagged`
- **Callers (0):** none
- **Calls:** Config, Path, TemporaryDirectory, _seed_valid_state, scan, setattr, write_text
- **Editing this affects:** none
### `test_scan_detects_missing_gitignore_entry`
- **Callers (0):** none
- **Calls:** Config, Path, TemporaryDirectory, _seed_valid_state, scan, setattr, write_text
- **Editing this affects:** none
### `test_scan_detects_hook_drift`
- **Callers (0):** none
- **Calls:** Config, Path, TemporaryDirectory, _seed_valid_state, mkdir, scan, setattr, write_text
- **Editing this affects:** none
### `test_scan_detects_pages_missing_deep_sections`
- **Callers (0):** none
- **Calls:** Config, FileEntry, Manifest, Path, TemporaryDirectory, compute_hash, mkdir, scan … (+2 more)
- **Editing this affects:** none
### `test_scan_deep_page_with_empty_narrative_not_flagged`
- **Callers (0):** none
- **Calls:** Config, FileEntry, Manifest, Path, TemporaryDirectory, compute_hash, mkdir, scan … (+2 more)
- **Editing this affects:** none
### `test_scan_skips_deep_check_when_skip_deep_true`
- **Callers (0):** none
- **Calls:** Config, FileEntry, Manifest, Path, TemporaryDirectory, compute_hash, mkdir, scan … (+2 more)
- **Editing this affects:** none
### `test_print_report_clean`
- **Callers (0):** none
- **Calls:** VerifyReport, print_report, readouterr
- **Editing this affects:** none
### `test_print_report_lists_each_drift`
- **Callers (0):** none
- **Calls:** VerifyReport, lower, print_report, readouterr
- **Editing this affects:** none
### `test_scan_skips_hook_check_when_check_hook_false`
- **Callers (0):** none
- **Calls:** Config, Path, TemporaryDirectory, _seed_valid_state, scan, setattr, write_text
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
## Data Flows
- Fixture file → parse_file(FIXTURE, repo_root) → list[ASTNode] → assertions on .id/.docstring/.imports/.calls fields
- list[ASTNode] → save_cached_nodes(root, hash, nodes) → disk → load_cached_nodes(root, hash) → identical list[ASTNode]
- Synthetic _node() stubs → blast_radius/god_nodes/pagerank/repo_map(nodes, ...) → set/list/dict/str assertions (no I/O)
- TemporaryDirectory → load_config(path) / save_config(path, cfg) → .indexer.toml → reload → assertEqual Config dataclass
## Design Constraints
- blast_radius uses called_by (pre-populated component ids) for reverse traversal, NOT calls; tests confirm it excludes self and terminates on cycles via BFS/DFS with a visited set — callers must ensure called_by is cross-referenced before calling blast_radius
- callees_of resolves bare callee names (from .calls) to full component ids by matching the bare name suffix against known node ids; names that don't match any node id are silently dropped — external stdlib calls like 'print' vanish without error
- god_nodes degree = len(called_by) + len(calls) (raw list lengths, NOT resolved ids); unresolvable external names in .calls still inflate degree counts
- pagerank scores sum to exactly 1.0 (±1e-6) and are deterministic; mutual-cycle nodes receive equal scores; empty input returns {} not an error
- repo_map accepts max_tokens as a hard budget using a ~4 chars/token heuristic; symbols are emitted in descending pagerank order and output is truncated when the budget is reached — the trailing symbols are silently omitted, not indicated with ellipsis
- load_config returns Config() defaults (not raises) when no .indexer.toml exists; partial TOML merges only the specified keys and preserves dataclass defaults for all others — the TOML section key is [llm], not [indexer] or [config]
## Relationships
- **Calls:** ASTNode, CliRunner, Config, FakeProc, FileEntry, IndexEntry, Manifest, NamedTemporaryFile, PageContext, Path, RepairPlan, TemporaryDirectory, VerifyReport, __import__, _bootstrap_repo, _by_id, _cfg, _chain_nodes, _claude_cli_completion, _clean_json, _complete, _empty_manifest, _make_node, _make_repo_with_manifest, _node, _parse_frontmatter, _seed_valid_state, _stub_llm, abs, all, any, blast_radius, build_blast_radius_map, build_index, build_page, callees_of, callers_of, compute_hash, count, density_group, describe_nodes, dict, dumps, endswith, execute, exists, get, getsource, god_nodes, index, invoke, is_clean, is_indexable, isinstance, isolated_filesystem, items, keys, len, load_cached_nodes, load_config, load_manifest, lower, mkdir, next, page_basename, page_relpath, pagerank, parse_file, plan, print_report, raises, range, ranked_symbols, read_text, readouterr, repo_map, repr, run, safe_load, save_cached_nodes, save_config, save_manifest, scan, scip_symbol, set, setattr, setdefault, sorted, split, stale_files, startswith, strip, sum, total_issues, update, values, write, write_bytes, write_page, write_text
- **Called by:** tests/test_graph.py::_chain_nodes, tests/test_graph.py::test_blast_radius_diamond, tests/test_graph.py::test_blast_radius_excludes_self, tests/test_graph.py::test_blast_radius_handles_cycles, tests/test_graph.py::test_blast_radius_is_transitive_reverse_reachability, tests/test_graph.py::test_blast_radius_leaf_caller_is_empty, tests/test_graph.py::test_blast_radius_unknown_symbol_is_empty, tests/test_graph.py::test_build_blast_radius_map_keys_every_node, tests/test_graph.py::test_callees_of_resolves_bare_names_to_ids, tests/test_graph.py::test_callees_of_skips_unresolvable_external_names, tests/test_graph.py::test_callers_of_empty_when_no_callers, tests/test_graph.py::test_callers_of_returns_caller_ids, tests/test_graph.py::test_god_nodes_n_larger_than_nodes, tests/test_graph.py::test_god_nodes_ranks_by_degree, tests/test_graph.py::test_god_nodes_respects_n, tests/test_graph.py::test_pagerank_handles_cycles, tests/test_graph.py::test_pagerank_is_deterministic, tests/test_graph.py::test_pagerank_keys_every_node_and_sums_to_one, tests/test_graph.py::test_pagerank_ranks_a_hub_above_leaves, tests/test_graph.py::test_ranked_symbols_orders_by_pagerank_desc, tests/test_graph.py::test_repo_map_larger_budget_includes_more, tests/test_graph.py::test_repo_map_leads_with_highest_ranked, tests/test_graph.py::test_repo_map_respects_token_budget, tests/test_graph.py::test_repo_map_returns_string, tests/test_init.py::test_claude_and_agents_share_guidance_constant, tests/test_init.py::test_init_appends_to_existing_agents_md, tests/test_init.py::test_init_creates_agents_md, tests/test_init.py::test_init_creates_claude_md_unchanged_behavior, tests/test_init.py::test_init_does_not_duplicate_agents_md_guidance, tests/test_llm_dispatch.py::fake_run, tests/test_llm_dispatch.py::test_claude_cli_completion_invokes_print_mode, tests/test_llm_dispatch.py::test_claude_cli_completion_raises_on_nonzero, tests/test_llm_dispatch.py::test_deep_flag_uses_configured_model_cli, tests/test_llm_dispatch.py::test_describe_nodes_uses_cli_path_end_to_end, tests/test_llm_dispatch.py::test_explicit_api_key_takes_priority_over_cli, tests/test_llm_dispatch.py::test_falls_back_to_cli_when_no_key_and_cli_present, tests/test_llm_dispatch.py::test_no_key_no_cli_raises_so_callers_fall_back, tests/test_multilang.py::test_go_calls, tests/test_multilang.py::test_go_docstring, tests/test_multilang.py::test_go_function, tests/test_multilang.py::test_go_imports, tests/test_multilang.py::test_go_method, tests/test_multilang.py::test_go_struct_is_class, tests/test_multilang.py::test_java_calls, tests/test_multilang.py::test_java_class, tests/test_multilang.py::test_java_docstring, tests/test_multilang.py::test_java_imports, tests/test_multilang.py::test_java_method, tests/test_multilang.py::test_java_static_method, tests/test_multilang.py::test_ruby_calls, tests/test_multilang.py::test_ruby_class_and_module, tests/test_multilang.py::test_ruby_docstring, tests/test_multilang.py::test_ruby_method, tests/test_multilang.py::test_ruby_top_level_function, tests/test_multilang.py::test_rust_calls, tests/test_multilang.py::test_rust_docstring, tests/test_multilang.py::test_rust_free_function, tests/test_multilang.py::test_rust_impl_method, tests/test_multilang.py::test_rust_struct_and_trait_are_classes, tests/test_repair_plan.py::test_clean_report_produces_empty_plan, tests/test_repair_plan.py::test_cleanup_ops_carried_through, tests/test_repair_plan.py::test_execute_restores_agents_md, tests/test_repair_plan.py::test_stale_and_untracked_files_go_to_reindex, tests/test_scip.py::test_class, tests/test_scip.py::test_is_deterministic, tests/test_scip.py::test_malformed_id_without_separator_is_safe, tests/test_scip.py::test_method, tests/test_scip.py::test_method_with_dotted_class_path_uses_last_segment_as_member, tests/test_scip.py::test_root_level_file, tests/test_scip.py::test_top_level_function, tests/test_scip.py::test_unknown_type_falls_back_to_term, tests/test_smart_integration.py::test_smart_bails_when_no_indexable_files, tests/test_smart_integration.py::test_smart_clean_state_is_noop, tests/test_smart_integration.py::test_smart_dry_run_clean_repo_exits_zero, tests/test_smart_integration.py::test_smart_dry_run_does_not_modify_filesystem, tests/test_smart_integration.py::test_smart_dry_run_drift_exits_nonzero, tests/test_smart_integration.py::test_smart_dry_run_reports_full_initial_index_without_changes, tests/test_smart_integration.py::test_smart_fills_fresh_repo_with_no_manifest, tests/test_smart_integration.py::test_smart_fills_never_indexed_tracked_file, tests/test_smart_integration.py::test_smart_repairs_missing_wiki_page, tests/test_verify.py::test_scan_agents_md_present_and_valid_not_flagged, tests/test_verify.py::test_scan_detects_dangling_manifest_entries, tests/test_verify.py::test_scan_detects_hook_drift, tests/test_verify.py::test_scan_detects_missing_agents_md_snippet, tests/test_verify.py::test_scan_detects_missing_claude_md_snippet, tests/test_verify.py::test_scan_detects_missing_gitignore_entry, tests/test_verify.py::test_scan_detects_stale_files, tests/test_verify.py::test_scan_detects_untracked_source_files, tests/test_verify.py::test_scan_skips_hook_check_when_check_hook_false, tests/test_wiki.py::test_build_page_contains_called_by, tests/test_wiki.py::test_build_page_contains_calls, tests/test_wiki.py::test_build_page_contains_symbol, tests/test_wiki.py::test_build_page_no_agent_hints, tests/test_wiki.py::test_page_body_sections_preserved_below_frontmatter, tests/test_wiki.py::test_page_frontmatter_description_from_narrative_first_sentence, tests/test_wiki.py::test_page_frontmatter_description_generic_when_no_narrative, tests/test_wiki.py::test_page_frontmatter_is_valid_yaml_with_required_type, tests/test_wiki.py::test_page_frontmatter_tags_from_path_segments, tests/test_wiki.py::test_page_frontmatter_timestamp_passed_in_not_computed, tests/test_wiki.py::test_page_frontmatter_title_and_resource, tests/test_wiki.py::test_page_relationships_block_caps_long_lists, tests/test_wiki.py::test_page_renders_relationships_block_per_symbol, tests/test_wiki.py::test_page_starts_with_frontmatter_delimiter, tests/test_wiki.py::test_write_page_creates_file
- **Imports from:** click.testing.CliRunner, indexer.ast_parser, indexer.ast_parser.ASTNode, indexer.ast_parser.compute_hash_short, indexer.ast_parser.load_cached_nodes, indexer.ast_parser.parse_file, indexer.ast_parser.save_cached_nodes, indexer.cli.NAV_GUIDANCE, indexer.cli.main, indexer.config.Config, indexer.config.load_config, indexer.config.save_config, indexer.graph.blast_radius, indexer.graph.build_blast_radius_map, indexer.graph.callees_of, indexer.graph.callers_of, indexer.graph.god_nodes, indexer.graph.pagerank, indexer.graph.ranked_symbols, indexer.graph.repo_map, indexer.grouper.density_group, indexer.langs.INDEXABLE_SUFFIXES, indexer.langs.JS_TS_SUFFIXES, indexer.langs.OTHER_SUFFIXES, indexer.langs.PYTHON_SUFFIXES, indexer.langs.is_indexable, indexer.llm, indexer.manifest.FileEntry, indexer.manifest.Manifest, indexer.manifest.compute_hash, indexer.manifest.load_manifest, indexer.manifest.save_manifest, indexer.repair.RepairPlan, indexer.repair.execute, indexer.repair.plan, indexer.scip.scip_symbol, indexer.ts_extract.LANG_CONFIGS, indexer.verify.VerifyReport, indexer.verify.print_report, indexer.verify.scan, indexer.wiki.IndexEntry, indexer.wiki.PageContext, indexer.wiki.build_index, indexer.wiki.build_page, indexer.wiki.page_basename, indexer.wiki.page_relpath, indexer.wiki.write_page, inspect, json, pathlib.Path, pytest, subprocess, tempfile, yaml
## Entry Points
- `test_parse_returns_nodes`
- `test_function_node`
- `test_method_node`
- `test_class_node`
- `test_docstring_extracted`
- `test_imports_extracted`
- `test_calls_extracted`
- `test_cache_roundtrip`
- `test_load_defaults`
- `test_save_and_reload`
- `test_partial_toml_uses_defaults`
- `test_callers_of_returns_caller_ids`
- `test_callers_of_empty_when_no_callers`
- `test_callees_of_resolves_bare_names_to_ids`
- `test_callees_of_skips_unresolvable_external_names`
- `test_blast_radius_is_transitive_reverse_reachability`
- `test_blast_radius_excludes_self`
- `test_blast_radius_leaf_caller_is_empty`
- `test_blast_radius_handles_cycles`
- `test_blast_radius_diamond`
- `test_blast_radius_unknown_symbol_is_empty`
- `test_god_nodes_ranks_by_degree`
- `test_god_nodes_respects_n`
- `test_god_nodes_empty_input`
- `test_god_nodes_n_larger_than_nodes`
- `test_build_blast_radius_map_keys_every_node`
- `test_pagerank_keys_every_node_and_sums_to_one`
- `test_pagerank_empty_input`
- `test_pagerank_ranks_a_hub_above_leaves`
- `test_pagerank_is_deterministic`
- `test_pagerank_handles_cycles`
- `test_ranked_symbols_orders_by_pagerank_desc`
- `test_ranked_symbols_empty`
- `test_repo_map_returns_string`
- `test_repo_map_respects_token_budget`
- `test_repo_map_leads_with_highest_ranked`
- `test_repo_map_empty`
- `test_repo_map_larger_budget_includes_more`
- `test_sparse_folders_merge_to_parent`
- `test_dense_folder_gets_own_page`
- `test_different_folders_get_separate_groups`
- `test_deep_sparse_merges_upward`
- `test_root_level_files`
- `test_returns_all_files`
- `test_root_files_count_correctly`
- `test_init_creates_agents_md`
- `test_init_creates_claude_md_unchanged_behavior`
- `test_init_appends_to_existing_agents_md`
- `test_init_does_not_duplicate_agents_md_guidance`
- `test_claude_and_agents_share_guidance_constant`
- `test_indexable_suffixes_is_union_of_parser_sets`
- `test_other_suffixes_match_ts_extract_lang_configs`
- `test_js_ts_suffixes_match_dispatch`
- `test_is_indexable_accepts_known_suffixes`
- `test_is_indexable_rejects_unknown_suffix`
- `test_is_indexable_honours_part_glob`
- `test_is_indexable_honours_path_glob`
- `test_explicit_api_key_takes_priority_over_cli`
- `test_falls_back_to_cli_when_no_key_and_cli_present`
- `test_deep_flag_uses_configured_model_cli`
- `test_no_key_no_cli_raises_so_callers_fall_back`
- `test_describe_nodes_uses_cli_path_end_to_end`
- `test_claude_cli_completion_invokes_print_mode`
- `test_claude_cli_completion_raises_on_nonzero`
- `test_clean_json_plain`
- `test_clean_json_fenced`
- `test_clean_json_preamble_then_fence`
- `test_clean_json_preamble_then_bare_object`
- `test_clean_json_list_payload`
- `test_clean_json_raises_on_garbage`
- `fake_sdk`
- `fake_cli`
- `fake_cli`
- `fake_run`
- `test_compute_hash_stable`
- `test_empty_manifest_on_missing`
- `test_save_and_reload`
- `test_stale_files_detected`
- `test_fresh_file_not_stale`
- `test_load_manifest_missing_component_ids`
- `test_go_yields_nonzero_symbols`
- `test_go_function`
- `test_go_struct_is_class`
- `test_go_method`
- `test_go_docstring`
- `test_go_calls`
- `test_go_imports`
- `test_java_yields_nonzero_symbols`
- `test_java_class`
- `test_java_method`
- `test_java_static_method`
- `test_java_docstring`
- `test_java_calls`
- `test_java_imports`
- `test_ruby_yields_nonzero_symbols`
- `test_ruby_class_and_module`
- `test_ruby_method`
- `test_ruby_top_level_function`
- `test_ruby_docstring`
- `test_ruby_calls`
- `test_rust_yields_nonzero_symbols`
- `test_rust_struct_and_trait_are_classes`
- `test_rust_free_function`
- `test_rust_impl_method`
- `test_rust_docstring`
- `test_rust_calls`
- `test_unsupported_suffix_returns_empty`
- `test_clean_report_produces_empty_plan`
- `test_stale_and_untracked_files_go_to_reindex`
- `test_missing_wiki_page_pulls_files_from_manifest`
- `test_pages_missing_deep_included_when_deep_active`
- `test_pages_missing_deep_excluded_when_skip_deep`
- `test_cleanup_ops_carried_through`
- `test_execute_restores_agents_md`
- `test_execute_deletes_orphan_pages_and_prunes_manifest`
- `test_execute_runs_reindex_for_files`
- `fake_index_files`
- `fake_finalise`
- `test_top_level_function`
- `test_class`
- `test_method`
- `test_method_with_dotted_class_path_uses_last_segment_as_member`
- `test_root_level_file`
- `test_is_deterministic`
- `test_unknown_type_falls_back_to_term`
- `test_malformed_id_without_separator_is_safe`
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
- `test_empty_report_is_clean`
- `test_report_with_stale_files_not_clean`
- `test_report_counts_all_drift_classes`
- `test_scan_flags_missing_manifest`
- `test_scan_detects_stale_files`
- `test_scan_detects_dangling_manifest_entries`
- `test_scan_detects_untracked_source_files`
- `test_scan_detects_missing_wiki_page`
- `test_scan_detects_orphan_wiki_page`
- `test_scan_detects_missing_index_and_skill`
- `test_scan_detects_missing_claude_md_snippet`
- `test_scan_detects_missing_agents_md_snippet`
- `test_scan_agents_md_present_and_valid_not_flagged`
- `test_scan_detects_missing_gitignore_entry`
- `test_scan_detects_hook_drift`
- `test_scan_detects_pages_missing_deep_sections`
- `test_scan_deep_page_with_empty_narrative_not_flagged`
- `test_scan_skips_deep_check_when_skip_deep_true`
- `test_print_report_clean`
- `test_print_report_lists_each_drift`
- `test_scan_skips_hook_check_when_check_hook_false`
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
