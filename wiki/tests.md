---
type: Code Group
title: tests
description: 'The test suite validates kiwiskil''s three core subsystems: AST parsing,
  call-graph analysis, and configuration.'
tags:
- tests
timestamp: '2026-06-22T13:11:57.286208+00:00'
resource: tests
---
# tests/
<!-- kiwiskil:deep -->

## Overview

The test suite validates kiwiskil's three core subsystems: AST parsing, call-graph analysis, and configuration. `test_ast_parser.py` exercises `parse_file` against a real fixture (`tests/fixtures/sample_py/auth.py`) to confirm that `ASTNode` objects carry correct IDs (path::symbol format), docstrings, file-level imports propagated to every node, and extracted callee bare names. `test_graph.py` covers the pure graph functions (`callers_of`, `callees_of`, `blast_radius`, `god_nodes`, `pagerank`, `ranked_symbols`, `repo_map`) entirely with synthetic `ASTNode` instances—no filesystem or LLM. `test_config.py` verifies that `load_config`/`save_config` round-trip `.indexer.toml` and that missing fields fall back to `Config()` defaults. Together these tests enforce the data contracts that the indexer pipeline depends on before any wiki generation or LLM dispatch.

## Modules
| File | Purpose |
|------|---------|
| tests/test_wiki.py | Unit tests for wiki page and INDEX.md rendering |
| tests/test_multilang.py | Integration tests for Go, Java, and multi-language parsing |
| tests/test_langs.py | Unit tests for language detection and suffix matching |
| tests/test_grouper.py | Unit tests for density-based page grouping algorithm |
| tests/test_llm_dispatch.py | Unit tests for LLM provider routing and JSON parsing |
| tests/test_repair_plan.py | Unit tests for drift repair planning and execution |
| tests/test_graph.py | Unit tests for call graph traversal and blast radius |
| tests/test_manifest.py | Unit tests for manifest loading, saving, and staleness detection |
| tests/test_smart_integration.py | Integration tests for incremental smart-mode indexing |
| tests/test_init.py | Integration tests for repository initialization |
| tests/test_scip.py | Unit tests for SCIP symbol descriptor generation |
| tests/test_ast_parser.py | Unit tests for Python AST parsing and node extraction |
| tests/test_config.py | Unit tests for config loading and persistence |
| tests/test_verify.py | Unit tests for drift verification across all artifact types |
## Key Symbols
| ID | Type | Description |
|----|------|-------------|
| `tests/test_ast_parser.py::test_parse_returns_nodes` | function | Verify parse_file returns nodes |
| `tests/test_ast_parser.py::test_function_node` | function | Verify parse_file extracts function nodes |
| `tests/test_ast_parser.py::test_method_node` | function | Verify parse_file extracts method nodes |
| `tests/test_ast_parser.py::test_class_node` | function | Verify parse_file extracts class nodes |
| `tests/test_ast_parser.py::test_docstring_extracted` | function | Verify docstrings extracted from parsed nodes |
| `tests/test_ast_parser.py::test_imports_extracted` | function | Verify import statements extracted from parsed nodes |
| `tests/test_ast_parser.py::test_calls_extracted` | function | Verify function calls extracted from parsed nodes |
| `tests/test_ast_parser.py::test_cache_roundtrip` | function | Verify nodes survive save/load cache roundtrip |
| `tests/test_config.py::test_load_defaults` | function | Verify load_config uses defaults for missing file |
| `tests/test_config.py::test_save_and_reload` | function | Verify save_config and load_config roundtrip |
| `tests/test_config.py::test_partial_toml_uses_defaults` | function | Verify partial TOML filled with Config defaults |
| `tests/test_graph.py::_node` | function | Parse symbol ID into ASTNode |
| `tests/test_graph.py::_chain_nodes` | function | Build chain of nodes from list of symbol IDs |
| `tests/test_graph.py::test_callers_of_returns_caller_ids` | function | Verify callers_of returns IDs of callers |
| `tests/test_graph.py::test_callers_of_empty_when_no_callers` | function | Verify callers_of returns empty set for leaf |
| `tests/test_graph.py::test_callees_of_resolves_bare_names_to_ids` | function | Verify callees_of resolves bare names to IDs |
| `tests/test_graph.py::test_callees_of_skips_unresolvable_external_names` | function | Verify callees_of skips unresolvable external names |
| `tests/test_graph.py::test_blast_radius_is_transitive_reverse_reachability` | function | Verify blast_radius returns transitive reverse reachability |
| `tests/test_graph.py::test_blast_radius_excludes_self` | function | Verify blast_radius excludes node itself |
| `tests/test_graph.py::test_blast_radius_leaf_caller_is_empty` | function | Verify blast_radius returns empty for leaf caller |
| `tests/test_graph.py::test_blast_radius_handles_cycles` | function | Verify blast_radius handles cyclic call graphs |
| `tests/test_graph.py::test_blast_radius_diamond` | function | Verify blast_radius correctly counts diamond graph |
| `tests/test_graph.py::test_blast_radius_unknown_symbol_is_empty` | function | Verify blast_radius returns empty for unknown symbol |
| `tests/test_graph.py::test_god_nodes_ranks_by_degree` | function | Verify god_nodes ranks nodes by call degree |
| `tests/test_graph.py::test_god_nodes_respects_n` | function | Verify god_nodes respects N limit |
| `tests/test_graph.py::test_god_nodes_empty_input` | function | Verify god_nodes handles empty input |
| `tests/test_graph.py::test_god_nodes_n_larger_than_nodes` | function | Verify god_nodes handles N larger than node count |
| `tests/test_graph.py::test_build_blast_radius_map_keys_every_node` | function | Verify build_blast_radius_map keys every node |
| `tests/test_graph.py::test_pagerank_keys_every_node_and_sums_to_one` | function | Verify pagerank covers all nodes and sums to one |
| `tests/test_graph.py::test_pagerank_empty_input` | function | Verify pagerank handles empty input |
| `tests/test_graph.py::test_pagerank_ranks_a_hub_above_leaves` | function | Verify pagerank ranks hub higher than leaves |
| `tests/test_graph.py::test_pagerank_is_deterministic` | function | Verify pagerank produces consistent results |
| `tests/test_graph.py::test_pagerank_handles_cycles` | function | Verify pagerank converges on cyclic graphs |
| `tests/test_graph.py::test_ranked_symbols_orders_by_pagerank_desc` | function | Verify ranked_symbols orders by pagerank descending |
| `tests/test_graph.py::test_ranked_symbols_empty` | function | Verify ranked_symbols handles empty input |
| `tests/test_graph.py::test_repo_map_returns_string` | function | Verify repo_map returns string |
| `tests/test_graph.py::test_repo_map_respects_token_budget` | function | Verify repo_map respects token budget |
| `tests/test_graph.py::test_repo_map_leads_with_highest_ranked` | function | Verify repo_map prioritizes highest-ranked symbols |
| `tests/test_graph.py::test_repo_map_empty` | function | Verify repo_map handles empty input |
| `tests/test_graph.py::test_repo_map_larger_budget_includes_more` | function | Verify larger token budget includes more symbols |
| `tests/test_grouper.py::test_sparse_folders_merge_to_parent` | function | Verify sparse folders merge to parent group |
| `tests/test_grouper.py::test_dense_folder_gets_own_page` | function | Verify dense folders get own page |
| `tests/test_grouper.py::test_different_folders_get_separate_groups` | function | Verify different folders get separate groups |
| `tests/test_grouper.py::test_deep_sparse_merges_upward` | function | Verify deep sparse paths merge upward |
| `tests/test_grouper.py::test_root_level_files` | function | Verify root-level files grouped correctly |
| `tests/test_grouper.py::test_returns_all_files` | function | Verify density_group returns all input files |
| `tests/test_grouper.py::test_root_files_count_correctly` | function | Verify root files counted in density calculation |
| `tests/test_init.py::_bootstrap_repo` | function | Initialize test repo with git setup |
| `tests/test_init.py::test_init_creates_agents_md` | function | Verify init creates AGENTS.md file |
| `tests/test_init.py::test_init_creates_claude_md_unchanged_behavior` | function | Verify init preserves existing CLAUDE.md |
| `tests/test_init.py::test_init_appends_to_existing_agents_md` | function | Verify init appends guidance to existing AGENTS.md |
| `tests/test_init.py::test_init_does_not_duplicate_agents_md_guidance` | function | Verify init guidance not duplicated |
| `tests/test_init.py::test_claude_and_agents_share_guidance_constant` | function | Verify CLAUDE.md and AGENTS.md use same guidance |
| `tests/test_langs.py::test_indexable_suffixes_is_union_of_parser_sets` | function | Verify indexable suffixes match parser coverage |
| `tests/test_langs.py::test_other_suffixes_match_ts_extract_lang_configs` | function | Verify non-JS suffixes have tree-sitter configs |
| `tests/test_langs.py::test_js_ts_suffixes_match_dispatch` | function | Verify JS_TS_SUFFIXES matches parser dispatch |
| `tests/test_langs.py::test_is_indexable_accepts_known_suffixes` | function | Verify is_indexable accepts known file types |
| `tests/test_langs.py::test_is_indexable_rejects_unknown_suffix` | function | Verify is_indexable rejects unknown suffixes |
| `tests/test_langs.py::test_is_indexable_honours_part_glob` | function | Verify is_indexable respects part glob patterns |
| `tests/test_langs.py::test_is_indexable_honours_path_glob` | function | Verify is_indexable respects path glob patterns |
| `tests/test_llm_dispatch.py::_cfg` | function | Create Config with attributes set from dict |
| `tests/test_llm_dispatch.py::test_explicit_api_key_takes_priority_over_cli` | function | Verify explicit API key bypasses CLI lookup |
| `tests/test_llm_dispatch.py::test_falls_back_to_cli_when_no_key_and_cli_present` | function | Falls back to claude CLI when no API key set but CLI present on PATH |
| `tests/test_llm_dispatch.py::test_deep_flag_uses_configured_model_cli` | function | Verifies deep=True uses configured heavy model, deep=False uses haiku |
| `tests/test_llm_dispatch.py::test_no_key_no_cli_raises_so_callers_fall_back` | function | Confirms _complete raises when no key and no CLI, callers return empty |
| `tests/test_llm_dispatch.py::test_describe_nodes_uses_cli_path_end_to_end` | function | Integration test: describe_nodes with CLI returns CLI-sourced descriptions |
| `tests/test_llm_dispatch.py::test_claude_cli_completion_invokes_print_mode` | function | _claude_cli_completion calls claude -p with system prompt and model |
| `tests/test_llm_dispatch.py::test_claude_cli_completion_raises_on_nonzero` | function | _claude_cli_completion raises exception on nonzero exit code |
| `tests/test_llm_dispatch.py::test_clean_json_plain` | function | Validates _clean_json handles plain JSON object |
| `tests/test_llm_dispatch.py::test_clean_json_fenced` | function | Validates _clean_json extracts JSON from markdown code fence |
| `tests/test_llm_dispatch.py::test_clean_json_preamble_then_fence` | function | Validates _clean_json strips preamble before fenced JSON |
| `tests/test_llm_dispatch.py::test_clean_json_preamble_then_bare_object` | function | Validates _clean_json handles preamble followed by bare object |
| `tests/test_llm_dispatch.py::test_clean_json_list_payload` | function | Validates _clean_json handles JSON array payload |
| `tests/test_llm_dispatch.py::test_clean_json_raises_on_garbage` | function | Validates _clean_json raises on unparseable garbage input |
| `tests/test_llm_dispatch.py::fake_sdk` | function | Fixture: creates mock SDK with no API key |
| `tests/test_llm_dispatch.py::fake_cli` | function | Fixture: creates mock CLI present on PATH |
| `tests/test_llm_dispatch.py::fake_cli` | function | Fixture: creates mock CLI present on PATH |
| `tests/test_llm_dispatch.py::FakeProc` | class | Mock subprocess.Popen return value with stdout, stderr, returncode |
| `tests/test_llm_dispatch.py::fake_run` | function | Fixture: returns mock Popen instance for subprocess.run |
| `tests/test_llm_dispatch.py::FakeProc` | class | Mock subprocess.Popen return value with stdout, stderr, returncode |
| `tests/test_manifest.py::test_compute_hash_stable` | function | Verifies compute_hash produces stable output across multiple calls |
| `tests/test_manifest.py::test_empty_manifest_on_missing` | function | Confirms load_manifest returns empty manifest when file missing |
| `tests/test_manifest.py::test_save_and_reload` | function | Verifies save_manifest and load_manifest round-trip correctly |
| `tests/test_manifest.py::test_stale_files_detected` | function | Confirms stale_files detects files with mismatched content hash |
| `tests/test_manifest.py::test_fresh_file_not_stale` | function | Confirms stale_files excludes files with matching content hash |
| `tests/test_manifest.py::test_load_manifest_missing_component_ids` | function | Verifies load_manifest handles manifests missing component_ids field |
| `tests/test_multilang.py::_grammar_available` | function | Helper: checks if tree-sitter grammar for language is installed |
| `tests/test_multilang.py::_by_id` | function | Helper: maps parsed symbols by full component ID |
| `tests/test_multilang.py::test_go_yields_nonzero_symbols` | function | Regression: confirms .go files extract nonzero symbols |
| `tests/test_multilang.py::test_go_function` | function | Verifies Go function parsed with correct type and docstring |
| `tests/test_multilang.py::test_go_struct_is_class` | function | Confirms Go struct extracted as class-type symbol |
| `tests/test_multilang.py::test_go_method` | function | Verifies Go receiver method parsed with correct hierarchy |
| `tests/test_multilang.py::test_go_docstring` | function | Confirms Go docstring extracted from preceding comment block |
| `tests/test_multilang.py::test_go_calls` | function | Verifies Go function extracts called functions |
| `tests/test_multilang.py::test_go_imports` | function | Confirms Go imports listed in symbol metadata |
| `tests/test_multilang.py::test_java_yields_nonzero_symbols` | function | Confirms .java files extract nonzero symbols |
| `tests/test_multilang.py::test_java_class` | function | Verifies Java class parsed with correct type |
| `tests/test_multilang.py::test_java_method` | function | Confirms Java instance method parsed correctly |
| `tests/test_multilang.py::test_java_static_method` | function | Confirms Java static method parsed as function-type |
| `tests/test_multilang.py::test_java_docstring` | function | Verifies Java Javadoc extracted from preceding comment |
| `tests/test_multilang.py::test_java_calls` | function | Confirms Java method extracts called methods |
| `tests/test_multilang.py::test_java_imports` | function | Verifies Java imports listed in symbol metadata |
| `tests/test_multilang.py::test_ruby_yields_nonzero_symbols` | function | Confirms .rb files extract nonzero symbols |
| `tests/test_multilang.py::test_ruby_class_and_module` | function | Verifies Ruby class and module parsed as class-type |
| `tests/test_multilang.py::test_ruby_method` | function | Confirms Ruby instance method parsed with correct hierarchy |
| `tests/test_multilang.py::test_ruby_top_level_function` | function | Verifies Ruby top-level function parsed as function |
| `tests/test_multilang.py::test_ruby_docstring` | function | Confirms Ruby docstring extracted from preceding comment |
| `tests/test_multilang.py::test_ruby_calls` | function | Verifies Ruby method extracts called methods |
| `tests/test_multilang.py::test_rust_yields_nonzero_symbols` | function |  |
| `tests/test_multilang.py::test_rust_struct_and_trait_are_classes` | function | Verifies Rust struct and trait parsed as class-type |
| `tests/test_multilang.py::test_rust_free_function` | function | Confirms Rust free function parsed as function-type |
| `tests/test_multilang.py::test_rust_impl_method` | function | Verifies Rust impl block method parsed with correct hierarchy |
| `tests/test_multilang.py::test_rust_docstring` | function | Confirms Rust doc comment extracted |
| `tests/test_multilang.py::test_rust_calls` | function | Verifies Rust function extracts called functions |
| `tests/test_multilang.py::test_unsupported_suffix_returns_empty` | function | Confirms unsupported file extension returns zero symbols |
| `tests/test_repair_plan.py::_empty_manifest` | function | Fixture: creates empty Manifest |
| `tests/test_repair_plan.py::test_clean_report_produces_empty_plan` | function | Confirms clean VerifyReport produces empty RepairPlan |
| `tests/test_repair_plan.py::test_stale_and_untracked_files_go_to_reindex` | function | Verifies stale/untracked files included in reindex operations |
| `tests/test_repair_plan.py::test_missing_wiki_page_pulls_files_from_manifest` | function | Confirms missing wiki page triggers reindex for associated files |
| `tests/test_repair_plan.py::test_pages_missing_deep_included_when_deep_active` | function | Verifies missing deep pages included when deep flag active |
| `tests/test_repair_plan.py::test_pages_missing_deep_excluded_when_skip_deep` | function | Confirms missing deep pages excluded when skip_deep flag set |
| `tests/test_repair_plan.py::test_cleanup_ops_carried_through` | function | Verifies cleanup operations preserved in repair plan |
| `tests/test_repair_plan.py::test_execute_restores_agents_md` | function | Confirms execute() restores agents.md from backup |
| `tests/test_repair_plan.py::test_execute_deletes_orphan_pages_and_prunes_manifest` | function | Verifies execute() deletes orphan wiki pages and removes from manifest |
| `tests/test_repair_plan.py::test_execute_runs_reindex_for_files` | function | Confirms execute() invokes index_files for reindex operations |
| `tests/test_repair_plan.py::fake_index_files` | function | Fixture: mock function replacing index_files |
| `tests/test_repair_plan.py::fake_finalise` | function | Fixture: mock function replacing finalise |
| `tests/test_scip.py::_node` | function | Helper: creates ASTNode from component ID string |
| `tests/test_scip.py::test_top_level_function` | function | Verifies top-level function generates correct SCIP symbol |
| `tests/test_scip.py::test_class` | function | Confirms class generates correct SCIP symbol |
| `tests/test_scip.py::test_method` | function | Verifies method generates correct SCIP symbol hierarchy |
| `tests/test_scip.py::test_method_with_dotted_class_path_uses_last_segment_as_member` | function | Confirms dotted class path uses last segment as member |
| `tests/test_scip.py::test_root_level_file` | function | Verifies root-level file generates file-only SCIP symbol |
| `tests/test_scip.py::test_is_deterministic` | function | Confirms scip_symbol output is deterministic |
| `tests/test_scip.py::test_unknown_type_falls_back_to_term` | function | Verifies unknown symbol type falls back to term |
| `tests/test_scip.py::test_malformed_id_without_separator_is_safe` | function | Confirms malformed ID without separator handled safely |
| `tests/test_smart_integration.py::_bootstrap_repo` | function | Helper: initializes git repo with basic config |
| `tests/test_smart_integration.py::test_smart_rejects_combo_with_force` | function | Confirms smart command rejects --force flag combination |
| `tests/test_smart_integration.py::test_smart_rejects_combo_with_staged` | function | Confirms smart command rejects --staged flag combination |
| `tests/test_smart_integration.py::test_smart_bails_when_no_indexable_files` | function | Verifies smart command exits when no indexable files found |
| `tests/test_smart_integration.py::test_smart_dry_run_does_not_modify_filesystem` | function | Confirms dry-run mode makes no filesystem changes |
| `tests/test_smart_integration.py::_stub_llm` | function | Fixture: mocks LLM completion to return predefined descriptions |
| `tests/test_smart_integration.py::test_smart_repairs_missing_wiki_page` | function | Verifies smart creates wiki page for unindexed file |
| `tests/test_smart_integration.py::test_smart_clean_state_is_noop` | function | Confirms smart is noop when manifest and files in sync |
| `tests/test_smart_integration.py::test_smart_fills_fresh_repo_with_no_manifest` | function | Verifies smart indexes fresh repo with no prior manifest |
| `tests/test_smart_integration.py::test_smart_dry_run_reports_full_initial_index_without_changes` | function | Confirms dry-run reports initial index scope without modifications |
| `tests/test_smart_integration.py::test_smart_fills_never_indexed_tracked_file` | function | Verifies smart indexes tracked file never previously indexed |
| `tests/test_smart_integration.py::test_smart_dry_run_clean_repo_exits_zero` | function | Confirms dry-run exits zero for clean synchronized repo |
| `tests/test_smart_integration.py::test_smart_dry_run_drift_exits_nonzero` | function | Confirms dry-run exits nonzero when manifest drifted from files |
| `tests/test_smart_integration.py::test_run_deletes_orphan_page_when_source_deleted` | function | Verifies orphan wiki pages are deleted when last source file removed |
| `tests/test_smart_integration.py::test_staged_subset_does_not_regroup_whole_wiki` | function | Ensures --staged run on 2-file subset preserves untouched wiki pages |
| `tests/test_smart_integration.py::test_staged_run_does_not_delete_pages_for_unstaged_files` | function | Prevents --staged runs from deleting wiki pages for non-staged files |
| `tests/test_verify.py::_make_repo_with_manifest` | function | Creates temporary repo with manifest fixture for testing |
| `tests/test_verify.py::test_empty_report_is_clean` | function | Verifies empty VerifyReport marked as clean |
| `tests/test_verify.py::test_report_with_stale_files_not_clean` | function | Confirms stale files cause report to fail clean check |
| `tests/test_verify.py::test_report_counts_all_drift_classes` | function | Validates VerifyReport totals all drift issue types |
| `tests/test_verify.py::test_scan_flags_missing_manifest` | function | Ensures scan detects missing manifest file |
| `tests/test_verify.py::test_scan_detects_stale_files` | function | Identifies source files missing from manifest |
| `tests/test_verify.py::test_scan_detects_dangling_manifest_entries` | function | Flags manifest entries without corresponding source files |
| `tests/test_verify.py::test_scan_detects_untracked_source_files` | function | Detects source files not listed in manifest |
| `tests/test_verify.py::test_scan_detects_missing_wiki_page` | function | Identifies manifest entries without wiki pages |
| `tests/test_verify.py::test_scan_detects_orphan_wiki_page` | function | Flags wiki pages unreferenced by manifest |
| `tests/test_verify.py::test_scan_detects_missing_index_and_skill` | function | Detects missing INDEX.md and skill files |
| `tests/test_verify.py::_seed_valid_state` | function | Creates fully-valid filesystem and manifest state fixture |
| `tests/test_verify.py::test_scan_detects_missing_claude_md_snippet` | function | Ensures scan flags missing CLAUDE.md content snippet |
| `tests/test_verify.py::test_scan_detects_missing_agents_md_snippet` | function | Verifies missing AGENTS.md snippet detected by scan |
| `tests/test_verify.py::test_scan_agents_md_present_and_valid_not_flagged` | function | Confirms valid AGENTS.md content passes scan |
| `tests/test_verify.py::test_scan_detects_missing_gitignore_entry` | function | Identifies missing .gitignore entries via scan |
| `tests/test_verify.py::test_scan_detects_hook_drift` | function | Detects pre-commit hook mismatches in filesystem |
| `tests/test_verify.py::test_scan_detects_pages_missing_deep_sections` | function | Flags pages missing required deep-enrichment sections |
| `tests/test_verify.py::test_scan_deep_page_with_empty_narrative_not_flagged` | function | Prevents false-positive deep-section drift for empty narratives |
| `tests/test_verify.py::test_scan_skips_deep_check_when_skip_deep_true` | function | Respects skip_deep=True to bypass deep-section validation |
| `tests/test_verify.py::test_print_report_clean` | function | Outputs clean status when no drift detected |
| `tests/test_verify.py::test_print_report_lists_each_drift` | function | Renders all detected drift issues in report output |
| `tests/test_verify.py::test_scan_skips_hook_check_when_check_hook_false` | function | Bypasses hook validation when check_hook=False |
| `tests/test_wiki.py::_make_node` | function | Creates ASTNode test fixture with custom attributes |
| `tests/test_wiki.py::test_build_page_contains_symbol` | function | Verifies build_page renders symbol in output |
| `tests/test_wiki.py::test_build_page_contains_calls` | function | Confirms built page includes symbol calls |
| `tests/test_wiki.py::test_build_page_contains_called_by` | function | Ensures built page lists symbols calling this one |
| `tests/test_wiki.py::test_build_page_no_agent_hints` | function | Validates agent hints excluded from page output |
| `tests/test_wiki.py::test_build_index_contains_page` | function | Checks index includes built page entry |
| `tests/test_wiki.py::test_write_page_creates_file` | function | Verifies write_page creates file with correct content |
| `tests/test_wiki.py::_parse_frontmatter` | function | Extracts and YAML-parses frontmatter from page text |
| `tests/test_wiki.py::test_page_starts_with_frontmatter_delimiter` | function | Confirms page begins with --- delimiter |
| `tests/test_wiki.py::test_page_frontmatter_is_valid_yaml_with_required_type` | function | Validates frontmatter YAML contains type field |
| `tests/test_wiki.py::test_page_frontmatter_title_and_resource` | function | Verifies frontmatter includes title and resource |
| `tests/test_wiki.py::test_page_frontmatter_tags_from_path_segments` | function | Generates tags from wiki page path segments |
| `tests/test_wiki.py::test_page_frontmatter_timestamp_passed_in_not_computed` | function | Uses provided timestamp instead of generating one |
| `tests/test_wiki.py::test_page_frontmatter_description_from_narrative_first_sentence` | function | Extracts description from narrative first sentence |
| `tests/test_wiki.py::test_page_frontmatter_description_generic_when_no_narrative` | function | Falls back to generic description without narrative |
| `tests/test_wiki.py::test_page_body_sections_preserved_below_frontmatter` | function | Maintains body sections after frontmatter block |
| `tests/test_wiki.py::test_index_frontmatter_has_okf_version` | function | Includes OKF version in index frontmatter |
| `tests/test_wiki.py::test_page_renders_relationships_block_per_symbol` | function | Builds relationships (calls, called_by) per symbol |
| `tests/test_wiki.py::test_page_relationships_block_caps_long_lists` | function | Truncates relationship lists exceeding length limit |
| `tests/test_wiki.py::test_index_renders_core_abstractions` | function | Renders core abstract classes in index |
| `tests/test_wiki.py::test_page_basename_root_group` | function | Generates correct basename for root group pages |
| `tests/test_wiki.py::test_page_basename_nested_group` | function | Generates correct basename for nested group pages |
| `tests/test_wiki.py::test_page_relpath_matches_write_page` | function | Ensures page_relpath output path matches write_page file |
| `tests/test_wiki.py::test_delete_orphan_pages_removes_unreferenced` | function | Deletes wiki pages not in manifest |
| `tests/test_wiki.py::test_delete_orphan_pages_noop_when_all_referenced` | function | Skips deletion when all pages referenced |
| `tests/test_wiki.py::test_delete_orphan_pages_missing_wiki_dir` | function | Handles gracefully when wiki directory absent |
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
- **Callers (17):** test_claude_and_agents_share_guidance_constant, test_init_appends_to_existing_agents_md, test_init_creates_agents_md, test_init_creates_claude_md_unchanged_behavior, test_init_does_not_duplicate_agents_md_guidance, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop … (+9 more)
- **Calls:** run
- **Editing this affects:** test_claude_and_agents_share_guidance_constant, test_init_appends_to_existing_agents_md, test_init_creates_agents_md, test_init_creates_claude_md_unchanged_behavior, test_init_does_not_duplicate_agents_md_guidance, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop … (+9 more)
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
- **Callers (17):** test_claude_and_agents_share_guidance_constant, test_init_appends_to_existing_agents_md, test_init_creates_agents_md, test_init_creates_claude_md_unchanged_behavior, test_init_does_not_duplicate_agents_md_guidance, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop … (+9 more)
- **Calls:** run
- **Editing this affects:** test_claude_and_agents_share_guidance_constant, test_init_appends_to_existing_agents_md, test_init_creates_agents_md, test_init_creates_claude_md_unchanged_behavior, test_init_does_not_duplicate_agents_md_guidance, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop … (+9 more)
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
- **Callers (9):** test_run_deletes_orphan_page_when_source_deleted, test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero, test_smart_dry_run_reports_full_initial_index_without_changes, test_smart_fills_fresh_repo_with_no_manifest, test_smart_fills_never_indexed_tracked_file, test_smart_repairs_missing_wiki_page, test_staged_run_does_not_delete_pages_for_unstaged_files … (+1 more)
- **Calls:** setattr
- **Editing this affects:** test_run_deletes_orphan_page_when_source_deleted, test_smart_clean_state_is_noop, test_smart_dry_run_clean_repo_exits_zero, test_smart_dry_run_reports_full_initial_index_without_changes, test_smart_fills_fresh_repo_with_no_manifest, test_smart_fills_never_indexed_tracked_file, test_smart_repairs_missing_wiki_page, test_staged_run_does_not_delete_pages_for_unstaged_files … (+1 more)
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
### `test_staged_subset_does_not_regroup_whole_wiki`
- **Callers (0):** none
- **Calls:** CliRunner, Path, _bootstrap_repo, _stub_llm, glob, invoke, isolated_filesystem, mkdir … (+3 more)
- **Editing this affects:** none
### `test_staged_run_does_not_delete_pages_for_unstaged_files`
- **Callers (0):** none
- **Calls:** CliRunner, FileEntry, Manifest, Path, _bootstrap_repo, _stub_llm, compute_hash, exists … (+6 more)
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
- parse_file(fixture_path, repo_root) → list[ASTNode] with id/docstring/imports/calls populated → save_cached_nodes(cache_dir, hash, nodes) → load_cached_nodes(cache_dir, hash) → identical list
- Synthetic ASTNode list with calls/called_by fields → blast_radius(nodes, symbol_id) → set of transitive upstream callers (excludes self)
- Synthetic ASTNode list → pagerank(nodes) → dict[id, float] summing to 1.0 → ranked_symbols() returns ids desc → repo_map(nodes, max_tokens) emits token-budgeted string leading with highest-ranked
- Path(dir) with partial/missing .indexer.toml → load_config(dir) → Config dataclass with missing fields filled from Config() defaults → save_config(dir, cfg) → identical Config on reload
## Design Constraints
- imports on ASTNode are file-level; every node from a given file carries the full import list, not just the imports visible in that node's scope
- callees_of resolves bare callee names (the strings in node.calls) against known node IDs by suffix match; unresolvable names (builtins, third-party) are silently dropped—callers must not assume completeness
- blast_radius uses called_by (pre-resolved component IDs) for traversal, NOT calls; the cross-ref pass in cli.py::_index_files must populate called_by before graph functions are meaningful
- blast_radius returns empty set for an unknown symbol ID rather than raising—callers cannot distinguish 'no upstream callers' from 'symbol not in graph'
- god_nodes degree = len(called_by) + len(calls) on the raw node fields; it does NOT resolve bare names, so external calls that appear in calls inflate degree artificially
- repo_map token budget is approximate (not exact tokenization); the test uses ~4 chars/token with a 6× slack factor, meaning output can exceed max_tokens in characters if symbol names are short
## Relationships
- **Calls:** ASTNode, CliRunner, Config, FakeProc, FileEntry, IndexEntry, Manifest, NamedTemporaryFile, PageContext, Path, RepairPlan, TemporaryDirectory, VerifyReport, __import__, _bootstrap_repo, _by_id, _cfg, _chain_nodes, _claude_cli_completion, _clean_json, _complete, _empty_manifest, _make_node, _make_repo_with_manifest, _node, _parse_frontmatter, _seed_valid_state, _stub_llm, abs, all, any, blast_radius, build_blast_radius_map, build_index, build_page, callees_of, callers_of, compute_hash, count, delete_orphan_pages, density_group, describe_nodes, dict, dumps, endswith, execute, exists, get, getsource, glob, god_nodes, index, invoke, is_clean, is_indexable, isinstance, isolated_filesystem, items, keys, len, load_cached_nodes, load_config, load_manifest, lower, mkdir, next, page_basename, page_relpath, pagerank, parse_file, plan, print_report, raises, range, ranked_symbols, read_text, readouterr, repo_map, repr, run, safe_load, save_cached_nodes, save_config, save_manifest, scan, scip_symbol, set, setattr, setdefault, sorted, split, stale_files, startswith, strip, sum, total_issues, unlink, update, values, write, write_bytes, write_page, write_text
- **Called by:** tests/test_graph.py::_chain_nodes, tests/test_graph.py::test_blast_radius_diamond, tests/test_graph.py::test_blast_radius_excludes_self, tests/test_graph.py::test_blast_radius_handles_cycles, tests/test_graph.py::test_blast_radius_is_transitive_reverse_reachability, tests/test_graph.py::test_blast_radius_leaf_caller_is_empty, tests/test_graph.py::test_blast_radius_unknown_symbol_is_empty, tests/test_graph.py::test_build_blast_radius_map_keys_every_node, tests/test_graph.py::test_callees_of_resolves_bare_names_to_ids, tests/test_graph.py::test_callees_of_skips_unresolvable_external_names, tests/test_graph.py::test_callers_of_empty_when_no_callers, tests/test_graph.py::test_callers_of_returns_caller_ids, tests/test_graph.py::test_god_nodes_n_larger_than_nodes, tests/test_graph.py::test_god_nodes_ranks_by_degree, tests/test_graph.py::test_god_nodes_respects_n, tests/test_graph.py::test_pagerank_handles_cycles, tests/test_graph.py::test_pagerank_is_deterministic, tests/test_graph.py::test_pagerank_keys_every_node_and_sums_to_one, tests/test_graph.py::test_pagerank_ranks_a_hub_above_leaves, tests/test_graph.py::test_ranked_symbols_orders_by_pagerank_desc, tests/test_graph.py::test_repo_map_larger_budget_includes_more, tests/test_graph.py::test_repo_map_leads_with_highest_ranked, tests/test_graph.py::test_repo_map_respects_token_budget, tests/test_graph.py::test_repo_map_returns_string, tests/test_init.py::test_claude_and_agents_share_guidance_constant, tests/test_init.py::test_init_appends_to_existing_agents_md, tests/test_init.py::test_init_creates_agents_md, tests/test_init.py::test_init_creates_claude_md_unchanged_behavior, tests/test_init.py::test_init_does_not_duplicate_agents_md_guidance, tests/test_llm_dispatch.py::fake_run, tests/test_llm_dispatch.py::test_claude_cli_completion_invokes_print_mode, tests/test_llm_dispatch.py::test_claude_cli_completion_raises_on_nonzero, tests/test_llm_dispatch.py::test_deep_flag_uses_configured_model_cli, tests/test_llm_dispatch.py::test_describe_nodes_uses_cli_path_end_to_end, tests/test_llm_dispatch.py::test_explicit_api_key_takes_priority_over_cli, tests/test_llm_dispatch.py::test_falls_back_to_cli_when_no_key_and_cli_present, tests/test_llm_dispatch.py::test_no_key_no_cli_raises_so_callers_fall_back, tests/test_multilang.py::test_go_calls, tests/test_multilang.py::test_go_docstring, tests/test_multilang.py::test_go_function, tests/test_multilang.py::test_go_imports, tests/test_multilang.py::test_go_method, tests/test_multilang.py::test_go_struct_is_class, tests/test_multilang.py::test_java_calls, tests/test_multilang.py::test_java_class, tests/test_multilang.py::test_java_docstring, tests/test_multilang.py::test_java_imports, tests/test_multilang.py::test_java_method, tests/test_multilang.py::test_java_static_method, tests/test_multilang.py::test_ruby_calls, tests/test_multilang.py::test_ruby_class_and_module, tests/test_multilang.py::test_ruby_docstring, tests/test_multilang.py::test_ruby_method, tests/test_multilang.py::test_ruby_top_level_function, tests/test_multilang.py::test_rust_calls, tests/test_multilang.py::test_rust_docstring, tests/test_multilang.py::test_rust_free_function, tests/test_multilang.py::test_rust_impl_method, tests/test_multilang.py::test_rust_struct_and_trait_are_classes, tests/test_repair_plan.py::test_clean_report_produces_empty_plan, tests/test_repair_plan.py::test_cleanup_ops_carried_through, tests/test_repair_plan.py::test_execute_restores_agents_md, tests/test_repair_plan.py::test_stale_and_untracked_files_go_to_reindex, tests/test_scip.py::test_class, tests/test_scip.py::test_is_deterministic, tests/test_scip.py::test_malformed_id_without_separator_is_safe, tests/test_scip.py::test_method, tests/test_scip.py::test_method_with_dotted_class_path_uses_last_segment_as_member, tests/test_scip.py::test_root_level_file, tests/test_scip.py::test_top_level_function, tests/test_scip.py::test_unknown_type_falls_back_to_term, tests/test_smart_integration.py::test_run_deletes_orphan_page_when_source_deleted, tests/test_smart_integration.py::test_smart_bails_when_no_indexable_files, tests/test_smart_integration.py::test_smart_clean_state_is_noop, tests/test_smart_integration.py::test_smart_dry_run_clean_repo_exits_zero, tests/test_smart_integration.py::test_smart_dry_run_does_not_modify_filesystem, tests/test_smart_integration.py::test_smart_dry_run_drift_exits_nonzero, tests/test_smart_integration.py::test_smart_dry_run_reports_full_initial_index_without_changes, tests/test_smart_integration.py::test_smart_fills_fresh_repo_with_no_manifest, tests/test_smart_integration.py::test_smart_fills_never_indexed_tracked_file, tests/test_smart_integration.py::test_smart_repairs_missing_wiki_page, tests/test_smart_integration.py::test_staged_run_does_not_delete_pages_for_unstaged_files, tests/test_smart_integration.py::test_staged_subset_does_not_regroup_whole_wiki, tests/test_verify.py::test_scan_agents_md_present_and_valid_not_flagged, tests/test_verify.py::test_scan_detects_dangling_manifest_entries, tests/test_verify.py::test_scan_detects_hook_drift, tests/test_verify.py::test_scan_detects_missing_agents_md_snippet, tests/test_verify.py::test_scan_detects_missing_claude_md_snippet, tests/test_verify.py::test_scan_detects_missing_gitignore_entry, tests/test_verify.py::test_scan_detects_stale_files, tests/test_verify.py::test_scan_detects_untracked_source_files, tests/test_verify.py::test_scan_skips_hook_check_when_check_hook_false, tests/test_wiki.py::test_build_page_contains_called_by, tests/test_wiki.py::test_build_page_contains_calls, tests/test_wiki.py::test_build_page_contains_symbol, tests/test_wiki.py::test_build_page_no_agent_hints, tests/test_wiki.py::test_page_body_sections_preserved_below_frontmatter, tests/test_wiki.py::test_page_frontmatter_description_from_narrative_first_sentence, tests/test_wiki.py::test_page_frontmatter_description_generic_when_no_narrative, tests/test_wiki.py::test_page_frontmatter_is_valid_yaml_with_required_type, tests/test_wiki.py::test_page_frontmatter_tags_from_path_segments, tests/test_wiki.py::test_page_frontmatter_timestamp_passed_in_not_computed, tests/test_wiki.py::test_page_frontmatter_title_and_resource, tests/test_wiki.py::test_page_relationships_block_caps_long_lists, tests/test_wiki.py::test_page_renders_relationships_block_per_symbol, tests/test_wiki.py::test_page_starts_with_frontmatter_delimiter, tests/test_wiki.py::test_write_page_creates_file
- **Imports from:** click.testing.CliRunner, indexer.ast_parser, indexer.ast_parser.ASTNode, indexer.ast_parser.compute_hash_short, indexer.ast_parser.load_cached_nodes, indexer.ast_parser.parse_file, indexer.ast_parser.save_cached_nodes, indexer.cli.NAV_GUIDANCE, indexer.cli.main, indexer.config.Config, indexer.config.load_config, indexer.config.save_config, indexer.graph.blast_radius, indexer.graph.build_blast_radius_map, indexer.graph.callees_of, indexer.graph.callers_of, indexer.graph.god_nodes, indexer.graph.pagerank, indexer.graph.ranked_symbols, indexer.graph.repo_map, indexer.grouper.density_group, indexer.langs.INDEXABLE_SUFFIXES, indexer.langs.JS_TS_SUFFIXES, indexer.langs.OTHER_SUFFIXES, indexer.langs.PYTHON_SUFFIXES, indexer.langs.is_indexable, indexer.llm, indexer.manifest.FileEntry, indexer.manifest.Manifest, indexer.manifest.compute_hash, indexer.manifest.load_manifest, indexer.manifest.save_manifest, indexer.repair.RepairPlan, indexer.repair.execute, indexer.repair.plan, indexer.scip.scip_symbol, indexer.ts_extract.LANG_CONFIGS, indexer.verify.VerifyReport, indexer.verify.print_report, indexer.verify.scan, indexer.wiki.IndexEntry, indexer.wiki.PageContext, indexer.wiki.build_index, indexer.wiki.build_page, indexer.wiki.delete_orphan_pages, indexer.wiki.page_basename, indexer.wiki.page_relpath, indexer.wiki.write_page, inspect, json, pathlib.Path, pytest, subprocess, tempfile, yaml
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
- `test_run_deletes_orphan_page_when_source_deleted`
- `test_staged_subset_does_not_regroup_whole_wiki`
- `test_staged_run_does_not_delete_pages_for_unstaged_files`
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
- `test_delete_orphan_pages_removes_unreferenced`
- `test_delete_orphan_pages_noop_when_all_referenced`
- `test_delete_orphan_pages_missing_wiki_dir`
