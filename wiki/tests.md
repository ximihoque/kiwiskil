---
type: Code Group
title: tests
description: The `tests` module serves as the primary verification layer for the agent's
  core engine, specifically validating AST extraction, configuration lifecycle, and
  dependency graph traversal.
tags:
- tests
timestamp: '2026-06-29T09:16:51.445490+00:00'
resource: tests
---
# tests/
<!-- kiwiskil:deep -->

## Overview

The `tests` module serves as the primary verification layer for the agent's core engine, specifically validating AST extraction, configuration lifecycle, and dependency graph traversal. By utilizing internal helpers like `_node` and `_chain_nodes`, the suite ensures the graph algorithms—`blast_radius`, `pagerank`, and `god_nodes`—properly handle structural complexities such as cycles and diamond dependencies. This module guarantees that the AST parser maintains semantic fidelity during file ingestion, providing the bedrock for reliable code analysis and impact reporting within the broader architecture.

## Modules
| File | Purpose |
|------|---------|
| tests/test_repair_plan.py | Unit tests for repair strategy generation and execution orchestration |
| tests/test_smart_integration.py | Integration tests for the smart repair and index refresh workflow |
| tests/test_llm_dispatch.py | Unit tests for LLM provider selection and JSON parsing logic |
| tests/test_manifest.py | Unit tests for manifest persistence and file staleness detection |
| tests/test_grouper.py | Unit tests for directory-to-wiki-group mapping logic |
| tests/test_ast_parser.py | Unit tests for Python AST parsing and caching functionality |
| tests/test_multilang.py | Unit tests for Go and Java language support and symbol extraction |
| tests/test_graph.py | Unit tests for dependency analysis, PageRank, and blast radius calculations |
| tests/test_scip.py | Unit tests for SCIP symbol descriptor generation |
| tests/test_config.py | Unit tests for indexer configuration loading and saving |
| tests/test_verify.py | Unit tests for scanning and reporting codebase index drift |
| tests/test_init.py | Unit tests for repository initialization and guidance file setup |
| tests/test_wiki.py | Unit tests for wiki page construction and frontmatter serialization |
| tests/test_langs.py | Unit tests for language detection and indexability logic |
## Key Symbols
| ID | Type | Description |
|----|------|-------------|
| `tests/test_ast_parser.py::test_parse_returns_nodes` | function | Verifies AST parsing returns expected node counts |
| `tests/test_ast_parser.py::test_function_node` | function | Checks if function definitions are correctly identified in parsed nodes |
| `tests/test_ast_parser.py::test_method_node` | function | Checks if class method definitions are correctly identified in parsed nodes |
| `tests/test_ast_parser.py::test_class_node` | function | Checks if class structures are correctly identified in parsed nodes |
| `tests/test_ast_parser.py::test_docstring_extracted` | function | Confirms docstrings are accurately captured during file parsing |
| `tests/test_ast_parser.py::test_imports_extracted` | function | Verifies that module import statements are parsed and extracted correctly |
| `tests/test_ast_parser.py::test_calls_extracted` | function | Confirms function call relationships are correctly identified within source code |
| `tests/test_ast_parser.py::test_cache_roundtrip` | function | Tests saving and loading parsed node data via cache files |
| `tests/test_config.py::test_load_defaults` | function | Validates that default configurations load correctly when no file exists |
| `tests/test_config.py::test_save_and_reload` | function | Confirms configuration settings persist correctly across save and load cycles |
| `tests/test_config.py::test_partial_toml_uses_defaults` | function | Verifies that incomplete configurations are merged with system defaults |
| `tests/test_graph.py::_node` | function | Helper to create dummy AST nodes for graph algorithm testing |
| `tests/test_graph.py::_chain_nodes` | function | Helper to link dummy nodes into a sequence for dependency testing |
| `tests/test_graph.py::test_callers_of_returns_caller_ids` | function | Validates retrieval of all nodes invoking a specific symbol |
| `tests/test_graph.py::test_callers_of_empty_when_no_callers` | function | Checks that callers_of returns an empty set for isolated nodes |
| `tests/test_graph.py::test_callees_of_resolves_bare_names_to_ids` | function | Ensures bare call strings correctly resolve to unique symbol identifiers |
| `tests/test_graph.py::test_callees_of_skips_unresolvable_external_names` | function | Verifies that non-existent or external calls are ignored in the graph |
| `tests/test_graph.py::test_blast_radius_is_transitive_reverse_reachability` | function | Confirms transitive identification of all impacted symbols in the call graph |
| `tests/test_graph.py::test_blast_radius_excludes_self` | function | Ensures the input node is not included in its own blast radius |
| `tests/test_graph.py::test_blast_radius_leaf_caller_is_empty` | function | Verifies leaf nodes return an empty set for blast radius |
| `tests/test_graph.py::test_blast_radius_handles_cycles` | function | Validates graph traversal algorithm stability in the presence of circular references |
| `tests/test_graph.py::test_blast_radius_diamond` | function | Checks reachability logic through diamond-shaped dependency patterns |
| `tests/test_graph.py::test_blast_radius_unknown_symbol_is_empty` | function | Confirms handling of requests for non-existent graph nodes |
| `tests/test_graph.py::test_god_nodes_ranks_by_degree` | function | Verifies that 'god nodes' are ranked correctly by total connection count |
| `tests/test_graph.py::test_god_nodes_respects_n` | function | Checks that god_nodes limit output correctly based on the N parameter |
| `tests/test_graph.py::test_god_nodes_empty_input` | function | Verifies graceful handling of empty inputs in god_nodes identification |
| `tests/test_graph.py::test_god_nodes_n_larger_than_nodes` | function | Checks behavior when requested limit exceeds total node count |
| `tests/test_graph.py::test_build_blast_radius_map_keys_every_node` | function | Confirms the map contains an entry for every node in the graph |
| `tests/test_graph.py::test_pagerank_keys_every_node_and_sums_to_one` | function | Verifies PageRank probability distribution properties |
| `tests/test_graph.py::test_pagerank_empty_input` | function | Checks that pagerank returns an empty dict for no inputs |
| `tests/test_graph.py::test_pagerank_ranks_a_hub_above_leaves` | function | Ensures central nodes receive higher importance scores than leaf nodes |
| `tests/test_graph.py::test_pagerank_is_deterministic` | function | Validates that PageRank returns consistent scores for identical input graphs |
| `tests/test_graph.py::test_pagerank_handles_cycles` | function | Confirms PageRank stability within cyclic dependency structures |
| `tests/test_graph.py::test_ranked_symbols_orders_by_pagerank_desc` | function | Verifies ranking outputs are sorted by importance score descending |
| `tests/test_graph.py::test_ranked_symbols_empty` | function | Checks behavior of ranking empty node sets |
| `tests/test_graph.py::test_repo_map_returns_string` | function | Confirms repository map output is a valid formatted string |
| `tests/test_graph.py::test_repo_map_respects_token_budget` | function | Validates that repo map generation respects maximum token constraints |
| `tests/test_graph.py::test_repo_map_leads_with_highest_ranked` | function | Ensures the highest importance symbols appear first in the map |
| `tests/test_graph.py::test_repo_map_empty` | function | Checks behavior of generating a map for empty input |
| `tests/test_graph.py::test_repo_map_larger_budget_includes_more` | function | Verifies that increasing the token budget expands the repo map content |
| `tests/test_grouper.py::test_sparse_folders_merge_to_parent` | function | Validates that folders with few items consolidate into parent wiki pages |
| `tests/test_grouper.py::test_dense_folder_gets_own_page` | function | Confirms that high-density folders generate their own dedicated wiki page |
| `tests/test_grouper.py::test_different_folders_get_separate_groups` | function | Ensures distinct directories maintain separate wiki grouping boundaries |
| `tests/test_grouper.py::test_deep_sparse_merges_upward` | function | Validates hierarchical merging of sparse subdirectories |
| `tests/test_grouper.py::test_root_level_files` | function | Checks grouping behavior for files located in the repository root |
| `tests/test_grouper.py::test_returns_all_files` | function | Ensures no source files are missed during the grouping process |
| `tests/test_grouper.py::test_root_files_count_correctly` | function | Validates accurate counting logic for root-level file grouping |
| `tests/test_init.py::_bootstrap_repo` | function | Helper function to initialize a mock repository environment |
| `tests/test_init.py::test_init_creates_agents_md` | function | Checks if init command generates the standard agents.md file |
| `tests/test_init.py::test_init_creates_claude_md_unchanged_behavior` | function | Validates backward compatibility for claude.md creation |
| `tests/test_init.py::test_init_appends_to_existing_agents_md` | function | Confirms existing agents files are safely appended to rather than overwritten |
| `tests/test_init.py::test_init_does_not_duplicate_agents_md_guidance` | function | Ensures initialization logic prevents duplicate content insertion |
| `tests/test_init.py::test_claude_and_agents_share_guidance_constant` | function | Validates consistency of guidance text across config files |
| `tests/test_langs.py::test_indexable_suffixes_is_union_of_parser_sets` | function | Confirms all supported file extensions are correctly registered for indexing |
| `tests/test_langs.py::test_other_suffixes_match_ts_extract_lang_configs` | function | Ensures language configurations align with supported file extensions |
| `tests/test_langs.py::test_js_ts_suffixes_match_dispatch` | function | Validates JavaScript/TypeScript suffix routing to correct parsers |
| `tests/test_langs.py::test_is_indexable_accepts_known_suffixes` | function | Verifies that known supported suffixes return true for indexability |
| `tests/test_langs.py::test_is_indexable_rejects_unknown_suffix` | function | Confirms that unsupported file types are correctly rejected |
| `tests/test_langs.py::test_is_indexable_honours_part_glob` | function | Tests file globbing patterns for indexing eligibility |
| `tests/test_langs.py::test_is_indexable_honours_path_glob` | function | Tests directory-level globbing patterns for indexing eligibility |
| `tests/test_llm_dispatch.py::_cfg` | function | Creates a test configuration object with specified attributes |
| `tests/test_llm_dispatch.py::test_explicit_api_key_takes_priority_over_cli` | function | Ensures explicit API keys override CLI-provided authentication methods |
| `tests/test_llm_dispatch.py::test_falls_back_to_cli_when_no_key_and_cli_present` | function | Verifies fallback to Claude CLI when no API key is detected |
| `tests/test_llm_dispatch.py::test_deep_flag_uses_configured_model_cli` | function | Checks if deep flag correctly selects heavier models via the CLI |
| `tests/test_llm_dispatch.py::test_no_key_no_cli_raises_so_callers_fall_back` | function | Confirms error handling when both API key and CLI are missing |
| `tests/test_llm_dispatch.py::test_describe_nodes_uses_cli_path_end_to_end` | function | Integration test for sourcing node descriptions from the CLI |
| `tests/test_llm_dispatch.py::test_claude_cli_completion_invokes_print_mode` | function | Validates CLI invocation parameters and stdout capture during completion |
| `tests/test_llm_dispatch.py::test_claude_cli_completion_raises_on_nonzero` | function | Ensures completion fails when the CLI process returns a non-zero exit code |
| `tests/test_llm_dispatch.py::test_clean_json_plain` | function | Verifies extraction of plain JSON strings |
| `tests/test_llm_dispatch.py::test_clean_json_fenced` | function | Tests extraction of JSON code blocks with markdown fences |
| `tests/test_llm_dispatch.py::test_clean_json_preamble_then_fence` | function | Tests JSON extraction when preceded by arbitrary text and fences |
| `tests/test_llm_dispatch.py::test_clean_json_preamble_then_bare_object` | function | Tests JSON extraction when preceded by text without fences |
| `tests/test_llm_dispatch.py::test_clean_json_list_payload` | function | Validates parsing of list-formatted JSON payloads |
| `tests/test_llm_dispatch.py::test_clean_json_raises_on_garbage` | function | Ensures error is raised when input contains invalid JSON data |
| `tests/test_llm_dispatch.py::fake_sdk` | function | Provides a mock SDK interface for testing |
| `tests/test_llm_dispatch.py::fake_cli` | function | Simulates a CLI environment for dispatch testing |
| `tests/test_llm_dispatch.py::fake_cli` | function | Simulates a CLI environment for dispatch testing |
| `tests/test_llm_dispatch.py::FakeProc` | class | Mock process class for simulating CLI execution outcomes |
| `tests/test_llm_dispatch.py::fake_run` | function | Simulates running external commands for completion testing |
| `tests/test_llm_dispatch.py::FakeProc` | class | Mock process class for simulating CLI execution outcomes |
| `tests/test_manifest.py::test_compute_hash_stable` | function | Ensures file hashing remains consistent across identical content |
| `tests/test_manifest.py::test_empty_manifest_on_missing` | function | Verifies loading an empty manifest when file is absent |
| `tests/test_manifest.py::test_save_and_reload` | function | Tests manifest persistence and recovery from disk |
| `tests/test_manifest.py::test_stale_files_detected` | function | Checks if stale files are correctly identified against manifest metadata |
| `tests/test_manifest.py::test_fresh_file_not_stale` | function | Confirms up-to-date files are not flagged as stale |
| `tests/test_manifest.py::test_load_manifest_missing_component_ids` | function | Validates robust loading when manifest file lacks specific component identifiers |
| `tests/test_multilang.py::_grammar_available` | function | Checks if language grammar for parsing exists |
| `tests/test_multilang.py::_by_id` | function | Helper to retrieve parsed symbols by identifier |
| `tests/test_multilang.py::test_go_yields_nonzero_symbols` | function | Regression test verifying symbol extraction from Go source files |
| `tests/test_multilang.py::test_go_function` | function | Tests parsing of top-level Go functions |
| `tests/test_multilang.py::test_go_struct_is_class` | function | Verifies Go structs are identified as classes |
| `tests/test_multilang.py::test_go_method` | function | Tests parsing of Go struct methods |
| `tests/test_multilang.py::test_go_docstring` | function | Verifies correct extraction of Go function docstrings |
| `tests/test_multilang.py::test_go_calls` | function | Tests extraction of function call references in Go |
| `tests/test_multilang.py::test_go_imports` | function | Verifies identification of Go package imports |
| `tests/test_multilang.py::test_java_yields_nonzero_symbols` | function | Verifies symbol extraction from Java source files |
| `tests/test_multilang.py::test_java_class` | function | Tests parsing of Java classes |
| `tests/test_multilang.py::test_java_method` | function | Tests parsing of Java instance methods |
| `tests/test_multilang.py::test_java_static_method` | function | Tests parsing of Java static methods |
| `tests/test_multilang.py::test_java_docstring` | function | Verifies extraction of Java doc comments |
| `tests/test_multilang.py::test_java_calls` | function | Tests extraction of method calls in Java |
| `tests/test_multilang.py::test_java_imports` | function | Verifies identification of Java package imports |
| `tests/test_multilang.py::test_ruby_yields_nonzero_symbols` | function | Verifies symbol extraction from Ruby source files |
| `tests/test_multilang.py::test_ruby_class_and_module` | function | Tests parsing of Ruby classes and modules |
| `tests/test_multilang.py::test_ruby_method` | function |  |
| `tests/test_multilang.py::test_ruby_top_level_function` | function |  |
| `tests/test_multilang.py::test_ruby_docstring` | function |  |
| `tests/test_multilang.py::test_ruby_calls` | function |  |
| `tests/test_multilang.py::test_rust_yields_nonzero_symbols` | function |  |
| `tests/test_multilang.py::test_rust_struct_and_trait_are_classes` | function |  |
| `tests/test_multilang.py::test_rust_free_function` | function |  |
| `tests/test_multilang.py::test_rust_impl_method` | function |  |
| `tests/test_multilang.py::test_rust_docstring` | function |  |
| `tests/test_multilang.py::test_rust_calls` | function |  |
| `tests/test_multilang.py::test_unsupported_suffix_returns_empty` | function |  |
| `tests/test_repair_plan.py::_empty_manifest` | function | Returns an unpopulated Manifest instance |
| `tests/test_repair_plan.py::test_clean_report_produces_empty_plan` | function | Confirms no repairs are planned for clean repository states |
| `tests/test_repair_plan.py::test_stale_and_untracked_files_go_to_reindex` | function | Verifies reindexing trigger for stale or new files |
| `tests/test_repair_plan.py::test_missing_wiki_page_pulls_files_from_manifest` | function | Checks if missing documentation triggers file re-indexing |
| `tests/test_repair_plan.py::test_pages_missing_deep_included_when_deep_active` | function | Tests inclusion of deep-index files when deep mode is enabled |
| `tests/test_repair_plan.py::test_pages_missing_deep_excluded_when_skip_deep` | function | Tests exclusion of deep-index files when deep mode is disabled |
| `tests/test_repair_plan.py::test_cleanup_ops_carried_through` | function | Verifies propagation of cleanup operations in the repair plan |
| `tests/test_repair_plan.py::test_execute_restores_agents_md` | function | Tests restoration of core documentation files during execution |
| `tests/test_repair_plan.py::test_execute_deletes_orphan_pages_and_prunes_manifest` | function | Verifies removal of orphans and manifest cleanup during execution |
| `tests/test_repair_plan.py::test_execute_runs_reindex_for_files` | function | Ensures file re-indexing logic triggers during plan execution |
| `tests/test_repair_plan.py::fake_index_files` | function | Mocks file indexing operations |
| `tests/test_repair_plan.py::fake_finalise` | function | Mocks finalization of the repair process |
| `tests/test_scip.py::_node` | function | Creates an ASTNode for symbol testing |
| `tests/test_scip.py::test_top_level_function` | function | Tests SCIP symbol generation for top-level functions |
| `tests/test_scip.py::test_class` | function | Tests SCIP symbol generation for classes |
| `tests/test_scip.py::test_method` | function | Tests SCIP symbol generation for methods |
| `tests/test_scip.py::test_method_with_dotted_class_path_uses_last_segment_as_member` | function | Validates mapping of nested paths to SCIP class members |
| `tests/test_scip.py::test_root_level_file` | function | Tests SCIP symbol generation for file-level scope |
| `tests/test_scip.py::test_is_deterministic` | function | Verifies SCIP symbol output consistency |
| `tests/test_scip.py::test_unknown_type_falls_back_to_term` | function | Ensures unknown types default to term representation |
| `tests/test_scip.py::test_malformed_id_without_separator_is_safe` | function | Confirms error resistance for malformed IDs |
| `tests/test_smart_integration.py::_bootstrap_repo` | function | Sets up a minimal repository for integration testing |
| `tests/test_smart_integration.py::test_smart_rejects_combo_with_force` | function | Validates CLI rejection of conflicting flags |
| `tests/test_smart_integration.py::test_smart_rejects_combo_with_staged` | function | Validates CLI rejection of incompatible staged flags |
| `tests/test_smart_integration.py::test_smart_bails_when_no_indexable_files` | function | Tests clean exit when no relevant files are found |
| `tests/test_smart_integration.py::test_smart_dry_run_does_not_modify_filesystem` | function | Verifies dry-run operations avoid side effects |
| `tests/test_smart_integration.py::_stub_llm` | function | Mocks the LLM interface for integration tests |
| `tests/test_smart_integration.py::test_smart_repairs_missing_wiki_page` | function | Tests automatic restoration of missing wiki documentation |
| `tests/test_smart_integration.py::test_smart_clean_state_is_noop` | function | Confirms no action is taken on correctly indexed repositories |
| `tests/test_smart_integration.py::test_smart_fills_fresh_repo_with_no_manifest` | function | Tests initial indexing for new repositories |
| `tests/test_smart_integration.py::test_smart_dry_run_reports_full_initial_index_without_changes` | function | Verifies dry-run reporting for unindexed content |
| `tests/test_smart_integration.py::test_smart_fills_never_indexed_tracked_file` | function | Verifies indexing for previously untracked files |
| `tests/test_smart_integration.py::test_smart_dry_run_clean_repo_exits_zero` | function | Confirms successful dry-run exit for clean repositories |
| `tests/test_smart_integration.py::test_smart_dry_run_drift_exits_nonzero` | function | Checks for non-zero exit code when drift is detected |
| `tests/test_smart_integration.py::test_run_deletes_orphan_page_when_source_deleted` | function | Verifies that running indexer removes wiki pages when the last source file is deleted |
| `tests/test_smart_integration.py::test_staged_subset_does_not_regroup_whole_wiki` | function | Ensures staged runs update only target files without re-bucketing or deleting existing wiki pages |
| `tests/test_smart_integration.py::test_staged_run_does_not_delete_pages_for_unstaged_files` | function | Validates that staged indexer runs do not erroneously delete pages for unreferenced source files |
| `tests/test_smart_integration.py::test_smart_does_not_delete_pages_for_untouched_groups` | function | Checks that smart repair operations preserve wiki pages for tracked but unmanifested source groups |
| `tests/test_verify.py::_make_repo_with_manifest` | function | Initializes a temporary directory with a boilerplate manifest and mock repository structure |
| `tests/test_verify.py::test_empty_report_is_clean` | function | Confirms a verification report with no issues returns clean status |
| `tests/test_verify.py::test_report_with_stale_files_not_clean` | function | Confirms a verification report containing stale file issues returns unclean status |
| `tests/test_verify.py::test_report_counts_all_drift_classes` | function | Validates that drift report accurately aggregates all identified code and manifest discrepancies |
| `tests/test_verify.py::test_scan_flags_missing_manifest` | function | Verifies that the scanner identifies and reports a missing .indexer.toml manifest file |
| `tests/test_verify.py::test_scan_detects_stale_files` | function | Confirms scanner identifies files present in manifest but modified or removed from disk |
| `tests/test_verify.py::test_scan_detects_dangling_manifest_entries` | function | Checks that scanner identifies manifest references to non-existent source files |
| `tests/test_verify.py::test_scan_detects_untracked_source_files` | function | Verifies scanner flags source files present on disk but missing from the manifest |
| `tests/test_verify.py::test_scan_detects_missing_wiki_page` | function | Validates scanner identifies missing wiki pages required by the current manifest |
| `tests/test_verify.py::test_scan_detects_orphan_wiki_page` | function | Confirms scanner identifies wiki pages on disk that are not referenced in the manifest |
| `tests/test_verify.py::test_scan_detects_missing_index_and_skill` | function | Checks that scanner flags missing index files or required skill implementation artifacts |
| `tests/test_verify.py::_seed_valid_state` | function | Creates a valid baseline filesystem and manifest state to support drift detection tests |
| `tests/test_verify.py::test_scan_detects_missing_claude_md_snippet` | function | Verifies scanner detects the absence of required Claude markdown configuration snippets |
| `tests/test_verify.py::test_scan_detects_missing_agents_md_snippet` | function | Verifies scanner detects the absence of required agents markdown configuration snippets |
| `tests/test_verify.py::test_scan_agents_md_present_and_valid_not_flagged` | function | Ensures correctly configured agents markdown files pass verification without triggering drift flags |
| `tests/test_verify.py::test_scan_detects_missing_gitignore_entry` | function | Confirms scanner identifies missing or improperly configured entries in the gitignore file |
| `tests/test_verify.py::test_scan_detects_hook_drift` | function | Validates scanner detects missing or mismatched git pre-commit hooks |
| `tests/test_verify.py::test_scan_detects_pages_missing_deep_sections` | function | Checks that scanner identifies wiki pages lacking required deep enrichment markers |
| `tests/test_verify.py::test_scan_deep_page_with_empty_narrative_not_flagged` | function | Ensures pages with empty LLM narratives are not falsely flagged as missing deep sections |
| `tests/test_verify.py::test_scan_skips_deep_check_when_skip_deep_true` | function | Confirms that deep enrichment verification is bypassed when skip_deep flag is enabled |
| `tests/test_verify.py::test_print_report_clean` | function | Checks clean report output format when no drift is detected |
| `tests/test_verify.py::test_print_report_lists_each_drift` | function | Verifies that all detected drift instances are accurately listed in the printed report |
| `tests/test_verify.py::test_scan_skips_hook_check_when_check_hook_false` | function | Verifies that hook drift detection is correctly disabled via the check_hook flag |
| `tests/test_wiki.py::_make_node` | function | Creates a synthetic AST node for wiki page generation testing |
| `tests/test_wiki.py::test_build_page_contains_symbol` | function | Validates that generated wiki pages correctly include documentation for specified source symbols |
| `tests/test_wiki.py::test_build_page_contains_calls` | function | Confirms generated wiki pages correctly map and list internal symbol dependencies |
| `tests/test_wiki.py::test_build_page_contains_called_by` | function | Confirms generated wiki pages correctly map and list reverse-dependency call references |
| `tests/test_wiki.py::test_build_page_no_agent_hints` | function | Ensures generated wiki pages exclude agent-specific hints when not required |
| `tests/test_wiki.py::test_build_index_contains_page` | function | Verifies that the index builder correctly aggregates individual wiki pages into the map |
| `tests/test_wiki.py::test_write_page_creates_file` | function | Confirms that page writing logic correctly persists wiki content to the filesystem |
| `tests/test_wiki.py::_parse_frontmatter` | function | Extracts and validates YAML metadata from the leading block of a wiki page |
| `tests/test_wiki.py::test_page_starts_with_frontmatter_delimiter` | function | Checks that wiki pages begin with the required YAML frontmatter delimiter |
| `tests/test_wiki.py::test_page_frontmatter_is_valid_yaml_with_required_type` | function | Validates frontmatter structure and type consistency for generated wiki pages |
| `tests/test_wiki.py::test_page_frontmatter_title_and_resource` | function | Confirms frontmatter accurately reflects page title and associated resource metadata |
| `tests/test_wiki.py::test_page_frontmatter_tags_from_path_segments` | function | Validates that frontmatter tags are correctly derived from file path directory segments |
| `tests/test_wiki.py::test_page_frontmatter_timestamp_passed_in_not_computed` | function | Ensures page frontmatter preserves provided timestamps rather than generating new ones |
| `tests/test_wiki.py::test_page_frontmatter_description_from_narrative_first_sentence` | function | Checks that page descriptions are correctly extracted from the first sentence of narrative content |
| `tests/test_wiki.py::test_page_frontmatter_description_generic_when_no_narrative` | function | Verifies that a default description is applied when page narrative is absent |
| `tests/test_wiki.py::test_page_body_sections_preserved_below_frontmatter` | function | Ensures wiki content body remains intact and correctly formatted beneath the frontmatter block |
| `tests/test_wiki.py::test_index_frontmatter_has_okf_version` | function | Validates index page frontmatter contains the correct framework version identifier |
| `tests/test_wiki.py::test_page_renders_relationships_block_per_symbol` | function | Confirms accurate rendering of dependency relationship tables for documented symbols |
| `tests/test_wiki.py::test_page_relationships_block_caps_long_lists` | function | Checks that relationship lists are correctly truncated or capped at configured limits |
| `tests/test_wiki.py::test_index_renders_core_abstractions` | function | Verifies that core system abstractions are correctly listed in the index page |
| `tests/test_wiki.py::test_page_basename_root_group` | function | Validates basename derivation logic for wiki pages located in the root directory |
| `tests/test_wiki.py::test_page_basename_nested_group` | function | Validates basename derivation logic for wiki pages within nested source groups |
| `tests/test_wiki.py::test_page_relpath_matches_write_page` | function | Confirms that manifest path resolution matches the actual filesystem location of written pages |
| `tests/test_wiki.py::test_delete_orphan_pages_removes_unreferenced` | function | Tests that orphan page cleanup logic successfully removes unlinked wiki files |
| `tests/test_wiki.py::test_delete_orphan_pages_noop_when_all_referenced` | function | Ensures no pages are deleted when all wiki files are correctly referenced |
| `tests/test_wiki.py::test_delete_orphan_pages_missing_wiki_dir` | function | Handles cases where the target wiki directory is missing during orphan cleanup |
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
- **Callers (18):** test_claude_and_agents_share_guidance_constant, test_init_appends_to_existing_agents_md, test_init_creates_agents_md, test_init_creates_claude_md_unchanged_behavior, test_init_does_not_duplicate_agents_md_guidance, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop … (+10 more)
- **Calls:** run
- **Editing this affects:** test_claude_and_agents_share_guidance_constant, test_init_appends_to_existing_agents_md, test_init_creates_agents_md, test_init_creates_claude_md_unchanged_behavior, test_init_does_not_duplicate_agents_md_guidance, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop … (+10 more)
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
- **Callers (18):** test_claude_and_agents_share_guidance_constant, test_init_appends_to_existing_agents_md, test_init_creates_agents_md, test_init_creates_claude_md_unchanged_behavior, test_init_does_not_duplicate_agents_md_guidance, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop … (+10 more)
- **Calls:** run
- **Editing this affects:** test_claude_and_agents_share_guidance_constant, test_init_appends_to_existing_agents_md, test_init_creates_agents_md, test_init_creates_claude_md_unchanged_behavior, test_init_does_not_duplicate_agents_md_guidance, test_run_deletes_orphan_page_when_source_deleted, test_smart_bails_when_no_indexable_files, test_smart_clean_state_is_noop … (+10 more)
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
- **Callers (10):** test_run_deletes_orphan_page_when_source_deleted, test_smart_clean_state_is_noop, test_smart_does_not_delete_pages_for_untouched_groups, test_smart_dry_run_clean_repo_exits_zero, test_smart_dry_run_reports_full_initial_index_without_changes, test_smart_fills_fresh_repo_with_no_manifest, test_smart_fills_never_indexed_tracked_file, test_smart_repairs_missing_wiki_page … (+2 more)
- **Calls:** setattr
- **Editing this affects:** test_run_deletes_orphan_page_when_source_deleted, test_smart_clean_state_is_noop, test_smart_does_not_delete_pages_for_untouched_groups, test_smart_dry_run_clean_repo_exits_zero, test_smart_dry_run_reports_full_initial_index_without_changes, test_smart_fills_fresh_repo_with_no_manifest, test_smart_fills_never_indexed_tracked_file, test_smart_repairs_missing_wiki_page … (+2 more)
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
### `test_smart_does_not_delete_pages_for_untouched_groups`
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
- Test runner calls parse_file -> AST output is validated against expected node counts and docstring capture.
- Graph test builds dummy nodes -> calls blast_radius -> verifies transitive reverse reachability metrics.
- Config test writes partial TOML -> load_config merges with defaults -> verified against expected state.
## Design Constraints
- Blast radius operations exclude the input node by definition; a node is never part of its own downstream impact set.
- The `god_nodes` function returns results sorted by degree, but its output size is clamped by the input N parameter, even if total nodes are fewer.
- PageRank implementations expect all node keys to be present in the returned dictionary, with values guaranteed to sum to approximately 1.0.
- AST cache files must be treated as transient; the test suite uses `TemporaryDirectory` to ensure filesystem isolation during roundtrip verification.
- Callers/Callees logic filters out unresolvable external names, meaning the graph only contains internal code references.
## Relationships
- **Calls:** ASTNode, CliRunner, Config, FakeProc, FileEntry, IndexEntry, Manifest, NamedTemporaryFile, PageContext, Path, RepairPlan, TemporaryDirectory, VerifyReport, __import__, _bootstrap_repo, _by_id, _cfg, _chain_nodes, _claude_cli_completion, _clean_json, _complete, _empty_manifest, _make_node, _make_repo_with_manifest, _node, _parse_frontmatter, _seed_valid_state, _stub_llm, abs, all, any, blast_radius, build_blast_radius_map, build_index, build_page, callees_of, callers_of, compute_hash, count, delete_orphan_pages, density_group, describe_nodes, dict, dumps, endswith, execute, exists, get, getsource, glob, god_nodes, index, invoke, is_clean, is_indexable, isinstance, isolated_filesystem, items, keys, len, load_cached_nodes, load_config, load_manifest, lower, mkdir, next, page_basename, page_relpath, pagerank, parse_file, plan, print_report, raises, range, ranked_symbols, read_text, readouterr, repo_map, repr, run, safe_load, save_cached_nodes, save_config, save_manifest, scan, scip_symbol, set, setattr, setdefault, sorted, split, stale_files, startswith, strip, sum, total_issues, unlink, update, values, write, write_bytes, write_page, write_text
- **Called by:** tests/test_graph.py::_chain_nodes, tests/test_graph.py::test_blast_radius_diamond, tests/test_graph.py::test_blast_radius_excludes_self, tests/test_graph.py::test_blast_radius_handles_cycles, tests/test_graph.py::test_blast_radius_is_transitive_reverse_reachability, tests/test_graph.py::test_blast_radius_leaf_caller_is_empty, tests/test_graph.py::test_blast_radius_unknown_symbol_is_empty, tests/test_graph.py::test_build_blast_radius_map_keys_every_node, tests/test_graph.py::test_callees_of_resolves_bare_names_to_ids, tests/test_graph.py::test_callees_of_skips_unresolvable_external_names, tests/test_graph.py::test_callers_of_empty_when_no_callers, tests/test_graph.py::test_callers_of_returns_caller_ids, tests/test_graph.py::test_god_nodes_n_larger_than_nodes, tests/test_graph.py::test_god_nodes_ranks_by_degree, tests/test_graph.py::test_god_nodes_respects_n, tests/test_graph.py::test_pagerank_handles_cycles, tests/test_graph.py::test_pagerank_is_deterministic, tests/test_graph.py::test_pagerank_keys_every_node_and_sums_to_one, tests/test_graph.py::test_pagerank_ranks_a_hub_above_leaves, tests/test_graph.py::test_ranked_symbols_orders_by_pagerank_desc, tests/test_graph.py::test_repo_map_larger_budget_includes_more, tests/test_graph.py::test_repo_map_leads_with_highest_ranked, tests/test_graph.py::test_repo_map_respects_token_budget, tests/test_graph.py::test_repo_map_returns_string, tests/test_init.py::test_claude_and_agents_share_guidance_constant, tests/test_init.py::test_init_appends_to_existing_agents_md, tests/test_init.py::test_init_creates_agents_md, tests/test_init.py::test_init_creates_claude_md_unchanged_behavior, tests/test_init.py::test_init_does_not_duplicate_agents_md_guidance, tests/test_llm_dispatch.py::fake_run, tests/test_llm_dispatch.py::test_claude_cli_completion_invokes_print_mode, tests/test_llm_dispatch.py::test_claude_cli_completion_raises_on_nonzero, tests/test_llm_dispatch.py::test_deep_flag_uses_configured_model_cli, tests/test_llm_dispatch.py::test_describe_nodes_uses_cli_path_end_to_end, tests/test_llm_dispatch.py::test_explicit_api_key_takes_priority_over_cli, tests/test_llm_dispatch.py::test_falls_back_to_cli_when_no_key_and_cli_present, tests/test_llm_dispatch.py::test_no_key_no_cli_raises_so_callers_fall_back, tests/test_multilang.py::test_go_calls, tests/test_multilang.py::test_go_docstring, tests/test_multilang.py::test_go_function, tests/test_multilang.py::test_go_imports, tests/test_multilang.py::test_go_method, tests/test_multilang.py::test_go_struct_is_class, tests/test_multilang.py::test_java_calls, tests/test_multilang.py::test_java_class, tests/test_multilang.py::test_java_docstring, tests/test_multilang.py::test_java_imports, tests/test_multilang.py::test_java_method, tests/test_multilang.py::test_java_static_method, tests/test_multilang.py::test_ruby_calls, tests/test_multilang.py::test_ruby_class_and_module, tests/test_multilang.py::test_ruby_docstring, tests/test_multilang.py::test_ruby_method, tests/test_multilang.py::test_ruby_top_level_function, tests/test_multilang.py::test_rust_calls, tests/test_multilang.py::test_rust_docstring, tests/test_multilang.py::test_rust_free_function, tests/test_multilang.py::test_rust_impl_method, tests/test_multilang.py::test_rust_struct_and_trait_are_classes, tests/test_repair_plan.py::test_clean_report_produces_empty_plan, tests/test_repair_plan.py::test_cleanup_ops_carried_through, tests/test_repair_plan.py::test_execute_restores_agents_md, tests/test_repair_plan.py::test_stale_and_untracked_files_go_to_reindex, tests/test_scip.py::test_class, tests/test_scip.py::test_is_deterministic, tests/test_scip.py::test_malformed_id_without_separator_is_safe, tests/test_scip.py::test_method, tests/test_scip.py::test_method_with_dotted_class_path_uses_last_segment_as_member, tests/test_scip.py::test_root_level_file, tests/test_scip.py::test_top_level_function, tests/test_scip.py::test_unknown_type_falls_back_to_term, tests/test_smart_integration.py::test_run_deletes_orphan_page_when_source_deleted, tests/test_smart_integration.py::test_smart_bails_when_no_indexable_files, tests/test_smart_integration.py::test_smart_clean_state_is_noop, tests/test_smart_integration.py::test_smart_does_not_delete_pages_for_untouched_groups, tests/test_smart_integration.py::test_smart_dry_run_clean_repo_exits_zero, tests/test_smart_integration.py::test_smart_dry_run_does_not_modify_filesystem, tests/test_smart_integration.py::test_smart_dry_run_drift_exits_nonzero, tests/test_smart_integration.py::test_smart_dry_run_reports_full_initial_index_without_changes, tests/test_smart_integration.py::test_smart_fills_fresh_repo_with_no_manifest, tests/test_smart_integration.py::test_smart_fills_never_indexed_tracked_file, tests/test_smart_integration.py::test_smart_repairs_missing_wiki_page, tests/test_smart_integration.py::test_staged_run_does_not_delete_pages_for_unstaged_files, tests/test_smart_integration.py::test_staged_subset_does_not_regroup_whole_wiki, tests/test_verify.py::test_scan_agents_md_present_and_valid_not_flagged, tests/test_verify.py::test_scan_detects_dangling_manifest_entries, tests/test_verify.py::test_scan_detects_hook_drift, tests/test_verify.py::test_scan_detects_missing_agents_md_snippet, tests/test_verify.py::test_scan_detects_missing_claude_md_snippet, tests/test_verify.py::test_scan_detects_missing_gitignore_entry, tests/test_verify.py::test_scan_detects_stale_files, tests/test_verify.py::test_scan_detects_untracked_source_files, tests/test_verify.py::test_scan_skips_hook_check_when_check_hook_false, tests/test_wiki.py::test_build_page_contains_called_by, tests/test_wiki.py::test_build_page_contains_calls, tests/test_wiki.py::test_build_page_contains_symbol, tests/test_wiki.py::test_build_page_no_agent_hints, tests/test_wiki.py::test_page_body_sections_preserved_below_frontmatter, tests/test_wiki.py::test_page_frontmatter_description_from_narrative_first_sentence, tests/test_wiki.py::test_page_frontmatter_description_generic_when_no_narrative, tests/test_wiki.py::test_page_frontmatter_is_valid_yaml_with_required_type, tests/test_wiki.py::test_page_frontmatter_tags_from_path_segments, tests/test_wiki.py::test_page_frontmatter_timestamp_passed_in_not_computed, tests/test_wiki.py::test_page_frontmatter_title_and_resource, tests/test_wiki.py::test_page_relationships_block_caps_long_lists, tests/test_wiki.py::test_page_renders_relationships_block_per_symbol, tests/test_wiki.py::test_page_starts_with_frontmatter_delimiter, tests/test_wiki.py::test_write_page_creates_file
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
- `test_smart_does_not_delete_pages_for_untouched_groups`
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
