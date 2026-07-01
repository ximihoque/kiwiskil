---
type: Code Group
title: tests
description: 'The tests group is the correctness harness for kiwiskil''s four core
  subsystems: AST parsing (test_ast_parser.py), call-graph analytics (test_graph.py),
  project configuration (test_config.py), and the remaining indexer pipeline stages
  covered by the other files.'
tags:
- tests
timestamp: '2026-07-01T15:33:21.751987+00:00'
resource: tests
---
# tests/
<!-- kiwiskil:deep -->

## Overview

The tests group is the correctness harness for kiwiskil's four core subsystems: AST parsing (test_ast_parser.py), call-graph analytics (test_graph.py), project configuration (test_config.py), and the remaining indexer pipeline stages covered by the other files. It exists to give fast, LLM-free verification of the pure-function layer so that CI can catch regressions in graph traversal, cache serialization, and config parsing without touching the filesystem or making API calls. test_graph.py is the most structurally complex: it constructs synthetic ASTNode chains in-memory and exercises callers_of, callees_of, blast_radius, god_nodes, pagerank, ranked_symbols, and repo_map. test_ast_parser.py uses a real fixture file (tests/fixtures/sample_py/auth.py) to verify that parse_file correctly extracts function, method, class, docstring, import, and call data, and that the cache roundtrip is lossless. test_config.py validates that load_config merges partial TOML with dataclass defaults and that save_config/load_config roundtrips are bijective.

## Modules
| File | Purpose |
|------|---------|
| tests/test_config.py | Tests for configuration loading and saving. |
| tests/test_llm_dispatch.py | Tests for LLM provider routing and CLI fallback. |
| tests/test_manifest.py | Tests for manifest persistence and staleness. |
| tests/test_grouper.py | Tests for folder density grouping logic. |
| tests/test_scip.py | Tests for SCIP descriptor generation. |
| tests/test_smart_integration.py | Integration tests for smart repair mode. |
| tests/test_multilang.py | Tests for Go, Java, and other language parsing. |
| tests/test_ast_parser.py | Tests for Python AST parsing and caching. |
| tests/test_verify.py | Tests for drift detection and verification. |
| tests/test_langs.py | Tests for language detection and suffix matching. |
| tests/test_wiki.py | Tests for wiki page and INDEX generation. |
| tests/test_repair_plan.py | Tests for repair plan generation and execution. |
| tests/test_init.py | Tests for repository initialization. |
| tests/test_graph.py | Tests for call graph analysis functions. |
## Key Symbols
| ID | Type | Description |
|----|------|-------------|
| `tests/test_ast_parser.py::test_parse_returns_nodes` | function | Verify parse_file returns ASTNode list. |
| `tests/test_ast_parser.py::test_function_node` | function | Verify parse_file extracts function nodes correctly. |
| `tests/test_ast_parser.py::test_method_node` | function | Verify parse_file extracts method nodes correctly. |
| `tests/test_ast_parser.py::test_class_node` | function | Verify parse_file extracts class nodes correctly. |
| `tests/test_ast_parser.py::test_docstring_extracted` | function | Verify first parsed node has docstring populated. |
| `tests/test_ast_parser.py::test_imports_extracted` | function | Verify parsed nodes include import statements. |
| `tests/test_ast_parser.py::test_calls_extracted` | function | Verify parsed nodes include function calls. |
| `tests/test_ast_parser.py::test_cache_roundtrip` | function | Verify parse_file cache save and load produce identical results. |
| `tests/test_config.py::test_load_defaults` | function | Verify load_config applies default Config values. |
| `tests/test_config.py::test_save_and_reload` | function | Verify save_config and load_config roundtrip preserves values. |
| `tests/test_config.py::test_partial_toml_uses_defaults` | function | Verify partial TOML file fills missing keys with defaults. |
| `tests/test_config.py::test_base_url_defaults_empty` | function | Verify Config.base_url defaults to empty string. |
| `tests/test_config.py::test_base_url_loads_from_toml` | function | Verify load_config reads base_url from TOML. |
| `tests/test_config.py::test_base_url_roundtrips_through_save` | function | Verify base_url survives save_config + load_config cycle. |
| `tests/test_graph.py::_node` | function | Parse component ID string to ASTNode for test setup. |
| `tests/test_graph.py::_chain_nodes` | function | Create chain of connected ASTNode objects for test graphs. |
| `tests/test_graph.py::test_callers_of_returns_caller_ids` | function | Verify callers_of returns correct caller IDs. |
| `tests/test_graph.py::test_callers_of_empty_when_no_callers` | function | Verify callers_of returns empty set for uncalled symbols. |
| `tests/test_graph.py::test_callees_of_resolves_bare_names_to_ids` | function | Verify callees_of resolves bare names to full component IDs. |
| `tests/test_graph.py::test_callees_of_skips_unresolvable_external_names` | function | Verify callees_of ignores unresolvable external calls. |
| `tests/test_graph.py::test_blast_radius_is_transitive_reverse_reachability` | function | Verify blast_radius computes transitive reverse-reachable set. |
| `tests/test_graph.py::test_blast_radius_excludes_self` | function | Verify blast_radius doesn't include the queried symbol. |
| `tests/test_graph.py::test_blast_radius_leaf_caller_is_empty` | function | Verify blast_radius returns empty set for leaf nodes. |
| `tests/test_graph.py::test_blast_radius_handles_cycles` | function | Verify blast_radius handles cyclic call graphs correctly. |
| `tests/test_graph.py::test_blast_radius_diamond` | function | Verify blast_radius handles diamond-shaped call graphs. |
| `tests/test_graph.py::test_blast_radius_unknown_symbol_is_empty` | function | Verify blast_radius returns empty for unknown symbols. |
| `tests/test_graph.py::test_god_nodes_ranks_by_degree` | function | Verify god_nodes ranks symbols by in-degree descending. |
| `tests/test_graph.py::test_god_nodes_respects_n` | function | Verify god_nodes respects max result count parameter. |
| `tests/test_graph.py::test_god_nodes_empty_input` | function | Verify god_nodes returns empty for empty graph. |
| `tests/test_graph.py::test_god_nodes_n_larger_than_nodes` | function | Verify god_nodes handles N larger than node count. |
| `tests/test_graph.py::test_build_blast_radius_map_keys_every_node` | function | Verify build_blast_radius_map includes all nodes as keys. |
| `tests/test_graph.py::test_pagerank_keys_every_node_and_sums_to_one` | function | Verify pagerank includes all nodes, scores sum to one. |
| `tests/test_graph.py::test_pagerank_empty_input` | function | Verify pagerank handles empty graph. |
| `tests/test_graph.py::test_pagerank_ranks_a_hub_above_leaves` | function | Verify pagerank ranks central hubs higher than leaves. |
| `tests/test_graph.py::test_pagerank_is_deterministic` | function | Verify pagerank produces identical results on repeated runs. |
| `tests/test_graph.py::test_pagerank_handles_cycles` | function | Verify pagerank handles cyclic graphs, scores sum to one. |
| `tests/test_graph.py::test_ranked_symbols_orders_by_pagerank_desc` | function | Verify ranked_symbols orders symbols by pagerank descending. |
| `tests/test_graph.py::test_ranked_symbols_empty` | function | Verify ranked_symbols returns empty for empty graph. |
| `tests/test_graph.py::test_repo_map_returns_string` | function | Verify repo_map returns string output. |
| `tests/test_graph.py::test_repo_map_respects_token_budget` | function | Verify repo_map truncates output to token budget. |
| `tests/test_graph.py::test_repo_map_leads_with_highest_ranked` | function | Verify repo_map prioritizes high-pagerank symbols first. |
| `tests/test_graph.py::test_repo_map_empty` | function | Verify repo_map handles empty graph. |
| `tests/test_graph.py::test_repo_map_larger_budget_includes_more` | function | Verify repo_map includes more symbols with larger budget. |
| `tests/test_grouper.py::test_sparse_folders_merge_to_parent` | function | Verify sparse folders merge into parent group. |
| `tests/test_grouper.py::test_dense_folder_gets_own_page` | function | Verify folder with many files gets own wiki page. |
| `tests/test_grouper.py::test_different_folders_get_separate_groups` | function | Verify different folders produce separate groups. |
| `tests/test_grouper.py::test_deep_sparse_merges_upward` | function | Verify deeply nested sparse folders merge to root. |
| `tests/test_grouper.py::test_root_level_files` | function | Verify root-level files grouped correctly. |
| `tests/test_grouper.py::test_returns_all_files` | function | Verify density_group returns all input files. |
| `tests/test_grouper.py::test_root_files_count_correctly` | function | Verify root group includes root-level files in file count. |
| `tests/test_init.py::_bootstrap_repo` | function | Set up test repo with git init and indexer config. |
| `tests/test_init.py::test_init_creates_agents_md` | function | Verify init command creates AGENTS.md in test repo. |
| `tests/test_init.py::test_init_creates_claude_md_unchanged_behavior` | function | Verify init command creates CLAUDE.md unchanged. |
| `tests/test_init.py::test_init_appends_to_existing_agents_md` | function | Verify init command appends to existing AGENTS.md. |
| `tests/test_init.py::test_init_does_not_duplicate_agents_md_guidance` | function | Verifies init command creates single AGENTS.md without duplicating guidance text |
| `tests/test_init.py::test_claude_and_agents_share_guidance_constant` | function | Confirms CLAUDE.md and AGENTS.md use same guidance constant, avoiding text divergence |
| `tests/test_langs.py::test_indexable_suffixes_is_union_of_parser_sets` | function | Validates indexable file extensions equal union of all language parser suffix sets |
| `tests/test_langs.py::test_other_suffixes_match_ts_extract_lang_configs` | function | Ensures non-JS/TS/Python suffixes have tree-sitter LANG_CONFIG entries |
| `tests/test_langs.py::test_js_ts_suffixes_match_dispatch` | function | Confirms JS_TS_SUFFIXES matches ast_parser's routing to JavaScript parser |
| `tests/test_langs.py::test_is_indexable_accepts_known_suffixes` | function | Validates is_indexable returns true for recognized file extensions |
| `tests/test_langs.py::test_is_indexable_rejects_unknown_suffix` | function | Ensures is_indexable rejects unrecognized file extensions |
| `tests/test_langs.py::test_is_indexable_honours_part_glob` | function | Verifies is_indexable respects exclude glob patterns on file parts |
| `tests/test_langs.py::test_is_indexable_honours_path_glob` | function | Verifies is_indexable respects exclude glob patterns on full paths |
| `tests/test_llm_dispatch.py::_cfg` | function | Test fixture: configures Config object from test settings dict |
| `tests/test_llm_dispatch.py::test_explicit_api_key_takes_priority_over_cli` | function | Confirms API key in config bypasses CLI lookup entirely |
| `tests/test_llm_dispatch.py::test_litellm_receives_base_url_when_configured` | function | Validates base_url is passed to litellm for OpenAI-compatible providers |
| `tests/test_llm_dispatch.py::test_litellm_base_url_none_when_unset` | function | Ensures base_url=None is passed when unconfigured, using litellm defaults |
| `tests/test_llm_dispatch.py::test_base_url_routes_anthropic_provider_through_litellm` | function | Confirms Anthropic providers with base_url route through litellm, not SDK |
| `tests/test_llm_dispatch.py::test_anthropic_provider_without_base_url_uses_sdk` | function | Regression: Anthropic without base_url uses SDK, not litellm |
| `tests/test_llm_dispatch.py::test_falls_back_to_cli_when_no_key_and_cli_present` | function | Anthropic provider without key falls back to claude CLI if available |
| `tests/test_llm_dispatch.py::test_deep_flag_uses_configured_model_cli` | function | Deep flag selects configured heavier model; disabled uses haiku |
| `tests/test_llm_dispatch.py::test_no_key_no_cli_raises_so_callers_fall_back` | function | No key and no CLI raises; callers catch and return structural-only wiki |
| `tests/test_llm_dispatch.py::test_describe_nodes_uses_cli_path_end_to_end` | function | Integration test: describe_nodes fetches descriptions via CLI when available |
| `tests/test_llm_dispatch.py::test_claude_cli_completion_invokes_print_mode` | function | Claude CLI completion runs claude -p with system prompt and model flags |
| `tests/test_llm_dispatch.py::test_claude_cli_completion_raises_on_nonzero` | function | CLI completion raises when claude subprocess returns nonzero exit code |
| `tests/test_llm_dispatch.py::test_clean_json_plain` | function | Extracts JSON from plain text response without fences |
| `tests/test_llm_dispatch.py::test_clean_json_fenced` | function | Extracts JSON from markdown-fenced code blocks |
| `tests/test_llm_dispatch.py::test_clean_json_preamble_then_fence` | function | Strips preamble, extracts JSON from fenced block |
| `tests/test_llm_dispatch.py::test_clean_json_preamble_then_bare_object` | function | Strips preamble, extracts JSON object without fences |
| `tests/test_llm_dispatch.py::test_clean_json_list_payload` | function | Extracts JSON array from response |
| `tests/test_llm_dispatch.py::test_clean_json_raises_on_garbage` | function | Raises ValueError when response contains no valid JSON |
| `tests/test_llm_dispatch.py::fake_sdk` | function | Test fixture: mocks Anthropic SDK module |
| `tests/test_llm_dispatch.py::fake_cli` | function | Test fixture: mocks claude CLI as available |
| `tests/test_llm_dispatch.py::FakeMsg` | class | Test mock: minimal message object with content field |
| `tests/test_llm_dispatch.py::FakeChoice` | class | Test mock: minimal choice object wrapping FakeMsg |
| `tests/test_llm_dispatch.py::FakeResp` | class | Test mock: minimal response object with choices list |
| `tests/test_llm_dispatch.py::FakeMsg` | class | Test mock: minimal message object with content field |
| `tests/test_llm_dispatch.py::FakeChoice` | class | Test mock: minimal choice object wrapping FakeMsg |
| `tests/test_llm_dispatch.py::FakeResp` | class | Test mock: minimal response object with choices list |
| `tests/test_llm_dispatch.py::fake_sdk` | function | Test fixture: mocks Anthropic SDK module |
| `tests/test_llm_dispatch.py::FakeMsg` | class | Test mock: minimal message object with content field |
| `tests/test_llm_dispatch.py::FakeChoice` | class | Test mock: minimal choice object wrapping FakeMsg |
| `tests/test_llm_dispatch.py::FakeResp` | class | Test mock: minimal response object with choices list |
| `tests/test_llm_dispatch.py::fake_sdk` | function | Test fixture: mocks Anthropic SDK module |
| `tests/test_llm_dispatch.py::fake_litellm_completion` | function |  |
| `tests/test_llm_dispatch.py::fake_cli` | function | Test fixture: mocks claude CLI as available |
| `tests/test_llm_dispatch.py::FakeProc` | class |  |
| `tests/test_llm_dispatch.py::fake_run` | function |  |
| `tests/test_llm_dispatch.py::FakeProc` | class |  |
| `tests/test_manifest.py::test_compute_hash_stable` | function | Validates compute_hash returns consistent sha256 hex for identical file content |
| `tests/test_manifest.py::test_empty_manifest_on_missing` | function | load_manifest returns empty Manifest when file missing |
| `tests/test_manifest.py::test_save_and_reload` | function | Manifest save and load roundtrip preserves file entries and component IDs |
| `tests/test_manifest.py::test_stale_files_detected` | function | stale_files identifies FileEntry with mismatched hash |
| `tests/test_manifest.py::test_fresh_file_not_stale` | function | File with matching hash is not marked stale |
| `tests/test_manifest.py::test_load_manifest_missing_component_ids` | function | load_manifest gracefully handles legacy manifests missing component_ids field |
| `tests/test_multilang.py::_grammar_available` | function | Test helper: checks if tree-sitter grammar module is importable |
| `tests/test_multilang.py::_by_id` | function | Test helper: returns symbol from parse output by component ID |
| `tests/test_multilang.py::test_go_yields_nonzero_symbols` | function | Regression: Go files extract at least one symbol |
| `tests/test_multilang.py::test_go_function` | function | Go free functions parse as function type |
| `tests/test_multilang.py::test_go_struct_is_class` | function | Go structs parse as class type |
| `tests/test_multilang.py::test_go_method` | function | Go receiver methods parse with receiver info in calls |
| `tests/test_multilang.py::test_go_docstring` | function | Go symbols extract preceding doc comments as docstring |
| `tests/test_multilang.py::test_go_calls` | function | Go symbols list function calls in call graph |
| `tests/test_multilang.py::test_go_imports` | function | Go files extract import statements |
| `tests/test_multilang.py::test_java_yields_nonzero_symbols` | function | Java files parse and extract symbols |
| `tests/test_multilang.py::test_java_class` | function | Java classes parse as class type |
| `tests/test_multilang.py::test_java_method` | function | Java methods parse with parent class and modifiers |
| `tests/test_multilang.py::test_java_static_method` | function | Java static methods include static modifier |
| `tests/test_multilang.py::test_java_docstring` | function | Java symbols extract preceding Javadoc comments |
| `tests/test_multilang.py::test_java_calls` | function | Java methods list method invocations in call graph |
| `tests/test_multilang.py::test_java_imports` | function | Java files extract import statements |
| `tests/test_multilang.py::test_ruby_yields_nonzero_symbols` | function | Ruby files parse and extract symbols |
| `tests/test_multilang.py::test_ruby_class_and_module` | function | Ruby classes and modules parse as class type |
| `tests/test_multilang.py::test_ruby_method` | function | Ruby methods parse with parent class context |
| `tests/test_multilang.py::test_ruby_top_level_function` | function | Ruby top-level functions parse as function type |
| `tests/test_multilang.py::test_ruby_docstring` | function | Ruby symbols extract preceding comments as docstring |
| `tests/test_multilang.py::test_ruby_calls` | function | Ruby methods list function/method calls |
| `tests/test_multilang.py::test_rust_yields_nonzero_symbols` | function | Rust files extract multiple symbols |
| `tests/test_multilang.py::test_rust_struct_and_trait_are_classes` | function | Rust structs and traits parse as class type |
| `tests/test_multilang.py::test_rust_free_function` | function | Rust free functions parse as function type |
| `tests/test_multilang.py::test_rust_impl_method` | function | Rust impl block methods parse with impl context |
| `tests/test_multilang.py::test_rust_docstring` | function | Rust symbols extract doc comments as docstring |
| `tests/test_multilang.py::test_rust_calls` | function | Rust functions list called function identifiers |
| `tests/test_multilang.py::test_unsupported_suffix_returns_empty` | function | Unsupported file types return empty symbol list |
| `tests/test_repair_plan.py::_empty_manifest` | function | Test fixture: returns empty Manifest with no files |
| `tests/test_repair_plan.py::test_clean_report_produces_empty_plan` | function | Clean verify report yields empty repair plan |
| `tests/test_repair_plan.py::test_stale_and_untracked_files_go_to_reindex` | function | Plan schedules stale and untracked files for reindexing |
| `tests/test_repair_plan.py::test_missing_wiki_page_pulls_files_from_manifest` | function | Missing wiki page triggers reindex of all manifest files for that page |
| `tests/test_repair_plan.py::test_pages_missing_deep_included_when_deep_active` | function | Deep descriptions missing includes deep pages when deep mode enabled |
| `tests/test_repair_plan.py::test_pages_missing_deep_excluded_when_skip_deep` | function | Deep descriptions missing excluded when skip_deep flag set |
| `tests/test_repair_plan.py::test_cleanup_ops_carried_through` | function | Cleanup operations from verify report propagate to repair plan |
| `tests/test_repair_plan.py::test_execute_restores_agents_md` | function | Plan execute recreates AGENTS.md from template when deleted |
| `tests/test_repair_plan.py::test_execute_deletes_orphan_pages_and_prunes_manifest` | function | Verifies orphan wiki pages and stale manifest entries are deleted during repair |
| `tests/test_repair_plan.py::test_execute_runs_reindex_for_files` | function | Verifies repair execution re-indexes modified files via reindex callback |
| `tests/test_repair_plan.py::fake_index_files` | function | Stub callback that marks files as indexed without actual processing |
| `tests/test_repair_plan.py::fake_finalise` | function | Stub callback for repair finalization phase |
| `tests/test_scip.py::_node` | function | Converts symbol path string to ASTNode for SCIP testing |
| `tests/test_scip.py::test_top_level_function` | function | Verifies SCIP symbol generation for top-level functions |
| `tests/test_scip.py::test_class` | function | Verifies SCIP symbol generation for class definitions |
| `tests/test_scip.py::test_method` | function | Verifies SCIP symbol generation for class methods |
| `tests/test_scip.py::test_method_with_dotted_class_path_uses_last_segment_as_member` | function | Verifies SCIP uses final segment for method member names |
| `tests/test_scip.py::test_root_level_file` | function | Verifies SCIP symbol generation for file-level symbols |
| `tests/test_scip.py::test_is_deterministic` | function | Verifies SCIP symbol generation produces consistent output |
| `tests/test_scip.py::test_unknown_type_falls_back_to_term` | function | Verifies SCIP defaults to Term for unrecognized symbol types |
| `tests/test_scip.py::test_malformed_id_without_separator_is_safe` | function | Verifies SCIP handles malformed IDs without crashing |
| `tests/test_smart_integration.py::_bootstrap_repo` | function | Initializes git repository with source files for integration tests |
| `tests/test_smart_integration.py::test_smart_rejects_combo_with_force` | function | Verifies --smart rejects incompatible --force flag |
| `tests/test_smart_integration.py::test_smart_rejects_combo_with_staged` | function | Verifies --smart rejects incompatible --staged flag |
| `tests/test_smart_integration.py::test_smart_bails_when_no_indexable_files` | function | Verifies --smart exits early when no indexable files exist |
| `tests/test_smart_integration.py::test_smart_dry_run_does_not_modify_filesystem` | function | Verifies --smart --dry-run reports changes without modifying files |
| `tests/test_smart_integration.py::_stub_llm` | function | Mocks LLM for testing without external API calls |
| `tests/test_smart_integration.py::test_smart_repairs_missing_wiki_page` | function | Verifies --smart creates missing wiki pages via LLM generation |
| `tests/test_smart_integration.py::test_smart_clean_state_is_noop` | function | Verifies --smart is no-op when repo and manifest are in sync |
| `tests/test_smart_integration.py::test_smart_fills_fresh_repo_with_no_manifest` | function | Verifies --smart generates full manifest and wiki for fresh repo |
| `tests/test_smart_integration.py::test_smart_dry_run_reports_full_initial_index_without_changes` | function | Verifies --smart --dry-run on fresh repo reports full scope |
| `tests/test_smart_integration.py::test_smart_fills_never_indexed_tracked_file` | function | Verifies --smart indexes previously-untracked files |
| `tests/test_smart_integration.py::test_smart_dry_run_clean_repo_exits_zero` | function | Verifies --smart --dry-run exits 0 when state is clean |
| `tests/test_smart_integration.py::test_smart_dry_run_drift_exits_nonzero` | function | Verifies --smart --dry-run exits non-zero when drift detected |
| `tests/test_smart_integration.py::test_run_deletes_orphan_page_when_source_deleted` | function | Verifies deleted source file triggers wiki page removal on reindex |
| `tests/test_smart_integration.py::test_staged_subset_does_not_regroup_whole_wiki` | function | Verifies --staged run respects existing page layout, no destructive re-bucketing |
| `tests/test_smart_integration.py::test_staged_run_does_not_delete_pages_for_unstaged_files` | function | Verifies --staged doesn't delete wiki pages for files outside staged set |
| `tests/test_smart_integration.py::test_smart_does_not_delete_pages_for_untouched_groups` | function | Verifies repair doesn't orphan-prune pages for stale-manifest-missing source files |
| `tests/test_verify.py::_make_repo_with_manifest` | function | Creates temporary repo with manifest entries for drift testing |
| `tests/test_verify.py::test_empty_report_is_clean` | function | Verifies zero-issue report marked as clean state |
| `tests/test_verify.py::test_report_with_stale_files_not_clean` | function | Verifies report with stale files marked as dirty |
| `tests/test_verify.py::test_report_counts_all_drift_classes` | function | Verifies report tallies all drift categories correctly |
| `tests/test_verify.py::test_scan_flags_missing_manifest` | function | Verifies scan detects absence of manifest file |
| `tests/test_verify.py::test_scan_detects_stale_files` | function | Verifies scan flags tracked files modified after last index |
| `tests/test_verify.py::test_scan_detects_dangling_manifest_entries` | function | Verifies scan detects manifest entries for deleted files |
| `tests/test_verify.py::test_scan_detects_untracked_source_files` | function | Verifies scan flags source files not in manifest |
| `tests/test_verify.py::test_scan_detects_missing_wiki_page` | function | Verifies scan flags manifest entries without corresponding wiki page |
| `tests/test_verify.py::test_scan_detects_orphan_wiki_page` | function | Verifies scan flags wiki pages with no backing manifest entries |
| `tests/test_verify.py::test_scan_detects_missing_index_and_skill` | function | Verifies scan flags missing .indexer directory or codebase.md skill |
| `tests/test_verify.py::_seed_valid_state` | function | Creates valid filesystem and manifest for regression drift tests |
| `tests/test_verify.py::test_scan_detects_missing_claude_md_snippet` | function | Verifies scan flags missing CLAUDE.md boilerplate snippet |
| `tests/test_verify.py::test_scan_detects_missing_agents_md_snippet` | function | Verifies scan flags missing AGENTS.md reference when needed |
| `tests/test_verify.py::test_scan_agents_md_present_and_valid_not_flagged` | function | Verifies valid AGENTS.md snippet passes scan check |
| `tests/test_verify.py::test_scan_detects_missing_gitignore_entry` | function | Verifies scan flags missing .indexer/ in .gitignore |
| `tests/test_verify.py::test_scan_detects_hook_drift` | function | Verifies scan detects pre-commit hook mismatch or absence |
| `tests/test_verify.py::test_scan_detects_pages_missing_deep_sections` | function | Verifies scan flags deep-marked pages missing Overview section |
| `tests/test_verify.py::test_scan_deep_page_with_empty_narrative_not_flagged` | function | Verifies deep page with empty LLM narrative not falsely flagged |
| `tests/test_verify.py::test_scan_skips_deep_check_when_skip_deep_true` | function | Verifies skip_deep=True suppresses deep-section validation |
| `tests/test_verify.py::test_print_report_clean` | function | Verifies report printer outputs clean state message |
| `tests/test_verify.py::test_print_report_lists_each_drift` | function | Verifies report printer lists all detected drift issues |
| `tests/test_verify.py::test_scan_skips_hook_check_when_check_hook_false` | function | Verifies check_hook=False suppresses hook drift detection |
| `tests/test_wiki.py::_make_node` | function | Creates ASTNode dict with optional docstring and metadata |
| `tests/test_wiki.py::test_build_page_contains_symbol` | function | Verifies page renders symbol in output |
| `tests/test_wiki.py::test_build_page_contains_calls` | function | Verifies page includes symbol's outbound function calls |
| `tests/test_wiki.py::test_build_page_contains_called_by` | function | Verifies page includes functions that call symbol |
| `tests/test_wiki.py::test_build_page_no_agent_hints` | function | Verifies page excludes agent hints when not present |
| `tests/test_wiki.py::test_build_index_contains_page` | function | Verifies index lists pages from build output |
| `tests/test_wiki.py::test_write_page_creates_file` | function | Verifies write_page creates wiki file at expected path |
| `tests/test_wiki.py::_parse_frontmatter` | function | Extracts and YAML-parses leading frontmatter block |
| `tests/test_wiki.py::test_page_starts_with_frontmatter_delimiter` | function | Verifies page begins with frontmatter delimiter |
| `tests/test_wiki.py::test_page_frontmatter_is_valid_yaml_with_required_type` | function | Verifies frontmatter is valid YAML with type field |
| `tests/test_wiki.py::test_page_frontmatter_title_and_resource` | function | Verifies frontmatter contains title and resource |
| `tests/test_wiki.py::test_page_frontmatter_tags_from_path_segments` | function | Verifies frontmatter derives tags from path |
| `tests/test_wiki.py::test_page_frontmatter_timestamp_passed_in_not_computed` | function | Verifies frontmatter uses provided timestamp |
| `tests/test_wiki.py::test_page_frontmatter_description_from_narrative_first_sentence` | function | Verifies frontmatter extracts description from narrative |
| `tests/test_wiki.py::test_page_frontmatter_description_generic_when_no_narrative` | function | Verifies frontmatter uses generic description when narrative absent |
| `tests/test_wiki.py::test_page_body_sections_preserved_below_frontmatter` | function | Verifies page preserves body sections below frontmatter |
| `tests/test_wiki.py::test_index_frontmatter_has_okf_version` | function | Verifies index frontmatter includes OKF version |
| `tests/test_wiki.py::test_page_renders_relationships_block_per_symbol` | function | Verifies page renders relationships blocks for each symbol |
| `tests/test_wiki.py::test_page_relationships_block_caps_long_lists` | function | Verifies page truncates long relationship lists |
| `tests/test_wiki.py::test_index_renders_core_abstractions` | function | Verifies index renders core abstractions |
| `tests/test_wiki.py::test_page_basename_root_group` | function | Verifies page_basename generates correct root group filename |
| `tests/test_wiki.py::test_page_basename_nested_group` | function | Verifies page_basename generates correct nested group filename |
| `tests/test_wiki.py::test_page_relpath_matches_write_page` | function | Verifies page_relpath matches write_page destination file |
| `tests/test_wiki.py::test_delete_orphan_pages_removes_unreferenced` | function | Verifies delete_orphan_pages removes unreferenced wiki files |
| `tests/test_wiki.py::test_delete_orphan_pages_noop_when_all_referenced` | function | Verifies delete_orphan_pages skips referenced wiki files |
| `tests/test_wiki.py::test_delete_orphan_pages_missing_wiki_dir` | function | Verifies delete_orphan_pages handles missing wiki directory |
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
### `test_base_url_defaults_empty`
- **Callers (0):** none
- **Calls:** Config
- **Editing this affects:** none
### `test_base_url_loads_from_toml`
- **Callers (0):** none
- **Calls:** Path, TemporaryDirectory, load_config, write_bytes
- **Editing this affects:** none
### `test_base_url_roundtrips_through_save`
- **Callers (0):** none
- **Calls:** Config, Path, TemporaryDirectory, load_config, save_config
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
- **Callers (9):** test_anthropic_provider_without_base_url_uses_sdk, test_base_url_routes_anthropic_provider_through_litellm, test_deep_flag_uses_configured_model_cli, test_describe_nodes_uses_cli_path_end_to_end, test_explicit_api_key_takes_priority_over_cli, test_falls_back_to_cli_when_no_key_and_cli_present, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured … (+1 more)
- **Calls:** Config, items, setattr
- **Editing this affects:** test_anthropic_provider_without_base_url_uses_sdk, test_base_url_routes_anthropic_provider_through_litellm, test_deep_flag_uses_configured_model_cli, test_describe_nodes_uses_cli_path_end_to_end, test_explicit_api_key_takes_priority_over_cli, test_falls_back_to_cli_when_no_key_and_cli_present, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured … (+1 more)
### `test_explicit_api_key_takes_priority_over_cli`
- **Callers (0):** none
- **Calls:** _cfg, _complete, setattr
- **Editing this affects:** none
### `test_litellm_receives_base_url_when_configured`
- **Callers (0):** none
- **Calls:** FakeChoice, FakeMsg, FakeResp, ModuleType, _cfg, _complete, setattr, setitem … (+1 more)
- **Editing this affects:** none
### `test_litellm_base_url_none_when_unset`
- **Callers (0):** none
- **Calls:** FakeChoice, FakeMsg, FakeResp, ModuleType, _cfg, _complete, setattr, setitem … (+1 more)
- **Editing this affects:** none
### `test_base_url_routes_anthropic_provider_through_litellm`
- **Callers (0):** none
- **Calls:** FakeChoice, FakeMsg, FakeResp, ModuleType, _cfg, _complete, setattr, setitem … (+1 more)
- **Editing this affects:** none
### `test_anthropic_provider_without_base_url_uses_sdk`
- **Callers (0):** none
- **Calls:** ModuleType, _cfg, _complete, setattr, setitem
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
### `FakeMsg`
- **Callers (3):** test_base_url_routes_anthropic_provider_through_litellm, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured
- **Calls:** none
- **Editing this affects:** test_base_url_routes_anthropic_provider_through_litellm, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured
### `FakeChoice`
- **Callers (3):** test_base_url_routes_anthropic_provider_through_litellm, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured
- **Calls:** none
- **Editing this affects:** test_base_url_routes_anthropic_provider_through_litellm, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured
### `FakeResp`
- **Callers (3):** test_base_url_routes_anthropic_provider_through_litellm, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured
- **Calls:** none
- **Editing this affects:** test_base_url_routes_anthropic_provider_through_litellm, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured
### `FakeMsg`
- **Callers (3):** test_base_url_routes_anthropic_provider_through_litellm, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured
- **Calls:** none
- **Editing this affects:** test_base_url_routes_anthropic_provider_through_litellm, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured
### `FakeChoice`
- **Callers (3):** test_base_url_routes_anthropic_provider_through_litellm, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured
- **Calls:** none
- **Editing this affects:** test_base_url_routes_anthropic_provider_through_litellm, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured
### `FakeResp`
- **Callers (3):** test_base_url_routes_anthropic_provider_through_litellm, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured
- **Calls:** none
- **Editing this affects:** test_base_url_routes_anthropic_provider_through_litellm, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured
### `FakeMsg`
- **Callers (3):** test_base_url_routes_anthropic_provider_through_litellm, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured
- **Calls:** none
- **Editing this affects:** test_base_url_routes_anthropic_provider_through_litellm, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured
### `FakeChoice`
- **Callers (3):** test_base_url_routes_anthropic_provider_through_litellm, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured
- **Calls:** none
- **Editing this affects:** test_base_url_routes_anthropic_provider_through_litellm, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured
### `FakeResp`
- **Callers (3):** test_base_url_routes_anthropic_provider_through_litellm, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured
- **Calls:** none
- **Editing this affects:** test_base_url_routes_anthropic_provider_through_litellm, test_litellm_base_url_none_when_unset, test_litellm_receives_base_url_when_configured
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
- test_ast_parser: parse_file(fixture) → ASTNode list → save_cached_nodes(tmp_dir, hash, nodes) → load_cached_nodes(tmp_dir, hash) → assert length and id equality
- test_graph: _chain_nodes() constructs synthetic ASTNodes with pre-populated called_by lists → callers_of/callees_of/blast_radius/god_nodes/pagerank/ranked_symbols/repo_map operate on that list → assertions on returned sets, lists, or strings
- test_config: write partial/full TOML bytes to tmp .indexer.toml → load_config(Path) returns Config dataclass → save_config(Path, cfg) → load_config(Path) asserts field equality
## Design Constraints
- blast_radius uses called_by (pre-resolved component IDs), not calls (bare names); callers_of reads called_by directly while callees_of performs bare-name resolution against the node list — mixing the two fields incorrectly will silently return wrong results
- callees_of drops any bare name that cannot be resolved to a known node ID; external stdlib calls (e.g. 'print') are silently discarded, not errored
- blast_radius excludes the queried symbol itself from its result set and must terminate on cycles — tests confirm both; any implementation that includes self or loops infinitely fails
- god_nodes degree is sum of len(called_by) + len(calls) per node (both directions), not just in-degree; the test fixture confirms hub with 3 callers + 2 callees scores 5
- pagerank must sum to 1.0 within 1e-6 tolerance and be deterministic across repeated calls on the same input; symmetric mutual-call pairs must yield equal rank
- load_config merges a partial TOML file with Config() defaults field-by-field — missing TOML keys fall back to the dataclass default, not to None; base_url defaults to empty string '', not None
## Relationships
- **Calls:** ASTNode, CliRunner, Config, FakeChoice, FakeMsg, FakeProc, FakeResp, FileEntry, IndexEntry, Manifest, ModuleType, NamedTemporaryFile, PageContext, Path, RepairPlan, TemporaryDirectory, VerifyReport, __import__, _bootstrap_repo, _by_id, _cfg, _chain_nodes, _claude_cli_completion, _clean_json, _complete, _empty_manifest, _make_node, _make_repo_with_manifest, _node, _parse_frontmatter, _seed_valid_state, _stub_llm, abs, all, any, blast_radius, build_blast_radius_map, build_index, build_page, callees_of, callers_of, compute_hash, count, delete_orphan_pages, density_group, describe_nodes, dict, dumps, endswith, execute, exists, get, getsource, glob, god_nodes, index, invoke, is_clean, is_indexable, isinstance, isolated_filesystem, items, keys, len, load_cached_nodes, load_config, load_manifest, lower, mkdir, next, page_basename, page_relpath, pagerank, parse_file, plan, print_report, raises, range, ranked_symbols, read_text, readouterr, repo_map, repr, run, safe_load, save_cached_nodes, save_config, save_manifest, scan, scip_symbol, set, setattr, setdefault, setitem, sorted, split, stale_files, startswith, strip, sum, total_issues, unlink, update, values, write, write_bytes, write_page, write_text
- **Called by:** tests/test_graph.py::_chain_nodes, tests/test_graph.py::test_blast_radius_diamond, tests/test_graph.py::test_blast_radius_excludes_self, tests/test_graph.py::test_blast_radius_handles_cycles, tests/test_graph.py::test_blast_radius_is_transitive_reverse_reachability, tests/test_graph.py::test_blast_radius_leaf_caller_is_empty, tests/test_graph.py::test_blast_radius_unknown_symbol_is_empty, tests/test_graph.py::test_build_blast_radius_map_keys_every_node, tests/test_graph.py::test_callees_of_resolves_bare_names_to_ids, tests/test_graph.py::test_callees_of_skips_unresolvable_external_names, tests/test_graph.py::test_callers_of_empty_when_no_callers, tests/test_graph.py::test_callers_of_returns_caller_ids, tests/test_graph.py::test_god_nodes_n_larger_than_nodes, tests/test_graph.py::test_god_nodes_ranks_by_degree, tests/test_graph.py::test_god_nodes_respects_n, tests/test_graph.py::test_pagerank_handles_cycles, tests/test_graph.py::test_pagerank_is_deterministic, tests/test_graph.py::test_pagerank_keys_every_node_and_sums_to_one, tests/test_graph.py::test_pagerank_ranks_a_hub_above_leaves, tests/test_graph.py::test_ranked_symbols_orders_by_pagerank_desc, tests/test_graph.py::test_repo_map_larger_budget_includes_more, tests/test_graph.py::test_repo_map_leads_with_highest_ranked, tests/test_graph.py::test_repo_map_respects_token_budget, tests/test_graph.py::test_repo_map_returns_string, tests/test_init.py::test_claude_and_agents_share_guidance_constant, tests/test_init.py::test_init_appends_to_existing_agents_md, tests/test_init.py::test_init_creates_agents_md, tests/test_init.py::test_init_creates_claude_md_unchanged_behavior, tests/test_init.py::test_init_does_not_duplicate_agents_md_guidance, tests/test_llm_dispatch.py::fake_run, tests/test_llm_dispatch.py::test_anthropic_provider_without_base_url_uses_sdk, tests/test_llm_dispatch.py::test_base_url_routes_anthropic_provider_through_litellm, tests/test_llm_dispatch.py::test_claude_cli_completion_invokes_print_mode, tests/test_llm_dispatch.py::test_claude_cli_completion_raises_on_nonzero, tests/test_llm_dispatch.py::test_deep_flag_uses_configured_model_cli, tests/test_llm_dispatch.py::test_describe_nodes_uses_cli_path_end_to_end, tests/test_llm_dispatch.py::test_explicit_api_key_takes_priority_over_cli, tests/test_llm_dispatch.py::test_falls_back_to_cli_when_no_key_and_cli_present, tests/test_llm_dispatch.py::test_litellm_base_url_none_when_unset, tests/test_llm_dispatch.py::test_litellm_receives_base_url_when_configured, tests/test_llm_dispatch.py::test_no_key_no_cli_raises_so_callers_fall_back, tests/test_multilang.py::test_go_calls, tests/test_multilang.py::test_go_docstring, tests/test_multilang.py::test_go_function, tests/test_multilang.py::test_go_imports, tests/test_multilang.py::test_go_method, tests/test_multilang.py::test_go_struct_is_class, tests/test_multilang.py::test_java_calls, tests/test_multilang.py::test_java_class, tests/test_multilang.py::test_java_docstring, tests/test_multilang.py::test_java_imports, tests/test_multilang.py::test_java_method, tests/test_multilang.py::test_java_static_method, tests/test_multilang.py::test_ruby_calls, tests/test_multilang.py::test_ruby_class_and_module, tests/test_multilang.py::test_ruby_docstring, tests/test_multilang.py::test_ruby_method, tests/test_multilang.py::test_ruby_top_level_function, tests/test_multilang.py::test_rust_calls, tests/test_multilang.py::test_rust_docstring, tests/test_multilang.py::test_rust_free_function, tests/test_multilang.py::test_rust_impl_method, tests/test_multilang.py::test_rust_struct_and_trait_are_classes, tests/test_repair_plan.py::test_clean_report_produces_empty_plan, tests/test_repair_plan.py::test_cleanup_ops_carried_through, tests/test_repair_plan.py::test_execute_restores_agents_md, tests/test_repair_plan.py::test_stale_and_untracked_files_go_to_reindex, tests/test_scip.py::test_class, tests/test_scip.py::test_is_deterministic, tests/test_scip.py::test_malformed_id_without_separator_is_safe, tests/test_scip.py::test_method, tests/test_scip.py::test_method_with_dotted_class_path_uses_last_segment_as_member, tests/test_scip.py::test_root_level_file, tests/test_scip.py::test_top_level_function, tests/test_scip.py::test_unknown_type_falls_back_to_term, tests/test_smart_integration.py::test_run_deletes_orphan_page_when_source_deleted, tests/test_smart_integration.py::test_smart_bails_when_no_indexable_files, tests/test_smart_integration.py::test_smart_clean_state_is_noop, tests/test_smart_integration.py::test_smart_does_not_delete_pages_for_untouched_groups, tests/test_smart_integration.py::test_smart_dry_run_clean_repo_exits_zero, tests/test_smart_integration.py::test_smart_dry_run_does_not_modify_filesystem, tests/test_smart_integration.py::test_smart_dry_run_drift_exits_nonzero, tests/test_smart_integration.py::test_smart_dry_run_reports_full_initial_index_without_changes, tests/test_smart_integration.py::test_smart_fills_fresh_repo_with_no_manifest, tests/test_smart_integration.py::test_smart_fills_never_indexed_tracked_file, tests/test_smart_integration.py::test_smart_repairs_missing_wiki_page, tests/test_smart_integration.py::test_staged_run_does_not_delete_pages_for_unstaged_files, tests/test_smart_integration.py::test_staged_subset_does_not_regroup_whole_wiki, tests/test_verify.py::test_scan_agents_md_present_and_valid_not_flagged, tests/test_verify.py::test_scan_detects_dangling_manifest_entries, tests/test_verify.py::test_scan_detects_hook_drift, tests/test_verify.py::test_scan_detects_missing_agents_md_snippet, tests/test_verify.py::test_scan_detects_missing_claude_md_snippet, tests/test_verify.py::test_scan_detects_missing_gitignore_entry, tests/test_verify.py::test_scan_detects_stale_files, tests/test_verify.py::test_scan_detects_untracked_source_files, tests/test_verify.py::test_scan_skips_hook_check_when_check_hook_false, tests/test_wiki.py::test_build_page_contains_called_by, tests/test_wiki.py::test_build_page_contains_calls, tests/test_wiki.py::test_build_page_contains_symbol, tests/test_wiki.py::test_build_page_no_agent_hints, tests/test_wiki.py::test_page_body_sections_preserved_below_frontmatter, tests/test_wiki.py::test_page_frontmatter_description_from_narrative_first_sentence, tests/test_wiki.py::test_page_frontmatter_description_generic_when_no_narrative, tests/test_wiki.py::test_page_frontmatter_is_valid_yaml_with_required_type, tests/test_wiki.py::test_page_frontmatter_tags_from_path_segments, tests/test_wiki.py::test_page_frontmatter_timestamp_passed_in_not_computed, tests/test_wiki.py::test_page_frontmatter_title_and_resource, tests/test_wiki.py::test_page_relationships_block_caps_long_lists, tests/test_wiki.py::test_page_renders_relationships_block_per_symbol, tests/test_wiki.py::test_page_starts_with_frontmatter_delimiter, tests/test_wiki.py::test_write_page_creates_file
- **Imports from:** click.testing.CliRunner, indexer.ast_parser, indexer.ast_parser.ASTNode, indexer.ast_parser.compute_hash_short, indexer.ast_parser.load_cached_nodes, indexer.ast_parser.parse_file, indexer.ast_parser.save_cached_nodes, indexer.cli.NAV_GUIDANCE, indexer.cli.main, indexer.config.Config, indexer.config.load_config, indexer.config.save_config, indexer.graph.blast_radius, indexer.graph.build_blast_radius_map, indexer.graph.callees_of, indexer.graph.callers_of, indexer.graph.god_nodes, indexer.graph.pagerank, indexer.graph.ranked_symbols, indexer.graph.repo_map, indexer.grouper.density_group, indexer.langs.INDEXABLE_SUFFIXES, indexer.langs.JS_TS_SUFFIXES, indexer.langs.OTHER_SUFFIXES, indexer.langs.PYTHON_SUFFIXES, indexer.langs.is_indexable, indexer.llm, indexer.manifest.FileEntry, indexer.manifest.Manifest, indexer.manifest.compute_hash, indexer.manifest.load_manifest, indexer.manifest.save_manifest, indexer.repair.RepairPlan, indexer.repair.execute, indexer.repair.plan, indexer.scip.scip_symbol, indexer.ts_extract.LANG_CONFIGS, indexer.verify.VerifyReport, indexer.verify.print_report, indexer.verify.scan, indexer.wiki.IndexEntry, indexer.wiki.PageContext, indexer.wiki.build_index, indexer.wiki.build_page, indexer.wiki.delete_orphan_pages, indexer.wiki.page_basename, indexer.wiki.page_relpath, indexer.wiki.write_page, inspect, json, pathlib.Path, pytest, subprocess, sys, tempfile, types, yaml
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
- `test_base_url_defaults_empty`
- `test_base_url_loads_from_toml`
- `test_base_url_roundtrips_through_save`
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
- `test_litellm_receives_base_url_when_configured`
- `test_litellm_base_url_none_when_unset`
- `test_base_url_routes_anthropic_provider_through_litellm`
- `test_anthropic_provider_without_base_url_uses_sdk`
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
- `fake_sdk`
- `fake_sdk`
- `fake_litellm_completion`
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
