---
type: Code Index
okf_version: '0.1'
title: Codebase Index
---
# Codebase Index

## System Overview

kiwiskil is a codebase indexer that transforms source repositories into a checked-in, LLM-navigable knowledge artifact — wiki pages, a manifest, and a skill file — without requiring a running server or cloud service. The pipeline flows: `langs.py` filters indexable files → `ast_parser.py`/`js_parser.py`/`ts_extract.py` parse symbols and call graphs → `grouper.py` clusters files into pages by density threshold → `llm.py` enriches with LLM-generated descriptions and narratives (via Anthropic SDK, claude CLI, or LiteLLM) → `wiki.py` renders Jinja2-templated markdown pages with OKF YAML frontmatter → `manifest.py` persists file→component-ID mappings. `graph.py` precomputes PageRank and blast radius over the call graph for every symbol. `verify.py` detects drift between filesystem, manifest, and wiki; `repair.py` computes a minimal `RepairPlan` and executes it. `cli.py` orchestrates all modes (`run`, `run --smart`, `run --staged`, `status`, `init`, `hook`) and `hooks.py` manages the pre-commit hook that triggers incremental re-indexing on every commit.
## Key Flows
- Full index run: cli.run → git.all_tracked_files → langs.is_indexable → cli._index_and_persist → cli._index_files [parse_file/parse_js_file/extract_generic → grouper.density_group → llm.describe_nodes/describe_files/deep_enrich_page → graph.build_blast_radius_map → wiki.build_page/write_page] → cli._finalise_index_and_skill [graph.repo_map + llm.deep_enrich_index → wiki.build_index/write_index] → manifest.save_manifest
- Incremental staged index (pre-commit hook): cli.run --staged → git.staged_files → langs.is_indexable → cli._index_and_persist (only changed files, hash-checked via manifest.Manifest.stale_files) → same _index_files/_finalise_index_and_skill pipeline → manifest.save_manifest → llm.synthesize_commit_message
- Smart repair flow: cli.run --smart → cli._run_smart → verify.scan [checks manifest vs filesystem vs wiki pages for drift] → repair.plan [VerifyReport → RepairPlan: re-index dirty files, delete orphan pages, prune dangling entries] → repair.execute [cli._index_files + cli._finalise_index_and_skill + manifest.save_manifest + cli._ensure_nav_guidance]
- LLM dispatch: llm._complete → llm._resolve_api_key (env var priority) → if Anthropic key: llm._anthropic_completion (Anthropic SDK); else if claude CLI on PATH: llm._claude_cli_completion (subprocess); else raise → llm._clean_json strips fences/preamble → caller (describe_nodes/deep_enrich_page/deep_enrich_index) extracts structured dict
- Blast radius tracing: graph.blast_radius(symbol, all_nodes) → BFS over reverse call edges via _index_by_id → returns transitive set of all component IDs whose behavior could change → precomputed for all nodes by build_blast_radius_map in _index_files → rendered inline per symbol in wiki.py._symbol_relationships → exposed in wiki page 'Editing this affects' lists

## Core abstractions
The highest-connectivity symbols (most callers + callees) — likely the load-bearing parts of the system:
- `indexer/ast_parser.py::parse_file` — degree 48
- `indexer/config.py::Config` — degree 30
- `indexer/cli.py::run` — degree 27
- `indexer/manifest.py::FileEntry` — degree 25
- `indexer/manifest.py::Manifest` — degree 25
- `indexer/verify.py::scan` — degree 23
- `tests/test_multilang.py::_by_id` — degree 22
- `indexer/wiki.py::build_page` — degree 21

## Repo Map
Symbols ranked by importance (PageRank over the call graph), most load-bearing first. Read these to orient before diving into any page:
- indexer/ast_parser.py::ASTNode  (callers: 11)
- indexer/cli.py::run  (callers: 15)
- indexer/ast_parser.py::parse_file  (callers: 36)
- indexer/js_parser.py::_node_text  (callers: 12)
- indexer/ts_extract.py::_node_text  (callers: 12)
- indexer/config.py::Config  (callers: 30)
- indexer/langs.py::is_indexable  (callers: 6)
- indexer/git.py::_run  (callers: 4)
- indexer/manifest.py::Manifest  (callers: 25)
- tests/test_multilang.py::_by_id  (callers: 22)
- indexer/graph.py::_index_by_id  (callers: 4)
- indexer/js_parser.py::visit  (callers: 8)
- indexer/ts_extract.py::visit  (callers: 8)
- tests/test_graph.py::_node  (callers: 19)
- tests/test_scip.py::_node  (callers: 19)
- indexer/manifest.py::FileEntry  (callers: 25)
- indexer/llm.py::_clean_json  (callers: 10)
- indexer/grouper.py::density_group  (callers: 8)
- indexer/verify.py::VerifyReport  (callers: 13)
- tests/test_graph.py::_chain_nodes  (callers: 13)
- indexer/js_parser.py::_get_name  (callers: 5)
- indexer/ts_extract.py::_get_name  (callers: 5)
- indexer/graph.py::_adjacency  (callers: 1)
- indexer/graph.py::pagerank  (callers: 6)
- indexer/llm.py::_complete  (callers: 9)
- indexer/ts_extract.py::_emit_method  (callers: 3)
- indexer/wiki.py::page_basename  (callers: 4)
- indexer/manifest.py::compute_hash  (callers: 16)
- indexer/ast_parser.py::_extract_calls  (callers: 4)
- indexer/js_parser.py::_extract_calls  (callers: 4)
- indexer/ts_extract.py::_extract_calls  (callers: 4)
- indexer/manifest.py::load_manifest  (callers: 7)
- indexer/verify.py::scan  (callers: 17)
- indexer/wiki.py::PageContext  (callers: 16)
- indexer/wiki.py::build_page  (callers: 16)
- tests/test_wiki.py::_make_node  (callers: 15)
- indexer/config.py::load_config  (callers: 7)
- indexer/graph.py::blast_radius  (callers: 7)
- indexer/ts_extract.py::_last_identifier  (callers: 2)
- tests/test_init.py::_bootstrap_repo  (callers: 14)
- tests/test_smart_integration.py::_bootstrap_repo  (callers: 14)
- indexer/graph.py::callees_of  (callers: 3)
- indexer/git.py::all_tracked_files  (callers: 5)
- indexer/git.py::is_git_repo  (callers: 6)
- indexer/scip.py::_split_id  (callers: 1)
- indexer/grouper.py::folder_of  (callers: 2)
- indexer/grouper.py::prefixes  (callers: 2)
- indexer/cli.py::_is_indexable  (callers: 4)
- indexer/verify.py::_is_indexable  (callers: 4)
- indexer/hooks.py::_hook_command  (callers: 3)
- indexer/scip.py::scip_symbol  (callers: 9)
- indexer/ts_extract.py::_extract_doc  (callers: 3)
- indexer/repair.py::RepairPlan  (callers: 3)
- indexer/cli.py::_ensure_cache_gitignore  (callers: 4)
- indexer/wiki.py::IndexEntry  (callers: 5)
- indexer/graph.py::repo_map  (callers: 6)
- indexer/js_parser.py::_extract_jsdoc  (callers: 2)
- indexer/llm.py::_claude_cli_path  (callers: 2)
- indexer/graph.py::god_nodes  (callers: 5)
- indexer/cli.py::_index_and_persist  (callers: 2)
- indexer/ts_extract.py::_resolve_class_node  (callers: 2)
- indexer/ts_extract.py::find_methods_in_body  (callers: 2)
- indexer/graph.py::ranked_symbols  (callers: 3)
- indexer/grouper.py::resolve_group  (callers: 1)
- tests/test_llm_dispatch.py::_cfg  (callers: 5)
- indexer/cli.py::_run_smart  (callers: 1)
- indexer/git.py::changed_files_since  (callers: 1)
- indexer/git.py::staged_files  (callers: 1)
- indexer/graph.py::_bare_name  (callers: 1)
- indexer/llm.py::_claude_cli_completion  (callers: 3)
- indexer/ast_parser.py::_extract_imports  (callers: 3)
- indexer/js_parser.py::_extract_imports  (callers: 3)
- indexer/ts_extract.py::_extract_imports  (callers: 3)
- tests/test_llm_dispatch.py::FakeProc  (callers: 3)
- tests/test_verify.py::_seed_valid_state  (callers: 6)
- indexer/ast_parser.py::_rel  (callers: 2)
- indexer/js_parser.py::_rel  (callers: 2)
- indexer/repair.py::plan  (callers: 8)
- indexer/wiki.py::_jinja_env  (callers: 2)
- indexer/wiki.py::_yaml_frontmatter  (callers: 2)
- indexer/ast_parser.py::_get_class_method_ids  (callers: 1)
- indexer/js_parser.py::parse_js_file  (callers: 1)
- indexer/ts_extract.py::extract_generic  (callers: 1)
- indexer/wiki.py::_short  (callers: 2)
- indexer/wiki.py::build_index  (callers: 4)
- indexer/manifest.py::save_manifest  (callers: 9)

## Structure
| Wiki Page | Covers | Entry Points |
|-----------|--------|--------------|
| wiki/indexer.md | indexer/ast_parser.py, indexer/cli.py, indexer/config.py, indexer/git.py, indexer/graph.py, indexer/grouper.py, indexer/hooks.py, indexer/js_parser.py, indexer/langs.py, indexer/llm.py, indexer/manifest.py, indexer/repair.py, indexer/scip.py, indexer/ts_extract.py, indexer/verify.py, indexer/wiki.py | main, init, status, hook, hook_install, hook_remove, Manifest.stale_files, RepairPlan.has_work, LangConfig, VerifyReport.total_issues, VerifyReport.is_clean |
| wiki/tests_fixtures.md | tests/fixtures/sample_go/server.go, tests/fixtures/sample_java/Widget.java, tests/fixtures/sample_py/auth.py, tests/fixtures/sample_ruby/widget.rb, tests/fixtures/sample_rust/widget.rs | Server, Start, Widget, Widget.bump, Widget.helper, TokenValidator, TokenValidator.refresh, require_auth, wrapper, Greeter, Greeter.hello, Widget, Widget.bump, top_level, Widget, Widget.bump, greet, Speak, speak |
| wiki/tests.md | tests/test_ast_parser.py, tests/test_config.py, tests/test_graph.py, tests/test_grouper.py, tests/test_init.py, tests/test_langs.py, tests/test_llm_dispatch.py, tests/test_manifest.py, tests/test_multilang.py, tests/test_repair_plan.py, tests/test_scip.py, tests/test_smart_integration.py, tests/test_verify.py, tests/test_wiki.py | test_parse_returns_nodes, test_function_node, test_method_node, test_class_node, test_docstring_extracted, test_imports_extracted, test_calls_extracted, test_cache_roundtrip, test_load_defaults, test_save_and_reload, test_partial_toml_uses_defaults, test_callers_of_returns_caller_ids, test_callers_of_empty_when_no_callers, test_callees_of_resolves_bare_names_to_ids, test_callees_of_skips_unresolvable_external_names, test_blast_radius_is_transitive_reverse_reachability, test_blast_radius_excludes_self, test_blast_radius_leaf_caller_is_empty, test_blast_radius_handles_cycles, test_blast_radius_diamond, test_blast_radius_unknown_symbol_is_empty, test_god_nodes_ranks_by_degree, test_god_nodes_respects_n, test_god_nodes_empty_input, test_god_nodes_n_larger_than_nodes, test_build_blast_radius_map_keys_every_node, test_pagerank_keys_every_node_and_sums_to_one, test_pagerank_empty_input, test_pagerank_ranks_a_hub_above_leaves, test_pagerank_is_deterministic, test_pagerank_handles_cycles, test_ranked_symbols_orders_by_pagerank_desc, test_ranked_symbols_empty, test_repo_map_returns_string, test_repo_map_respects_token_budget, test_repo_map_leads_with_highest_ranked, test_repo_map_empty, test_repo_map_larger_budget_includes_more, test_sparse_folders_merge_to_parent, test_dense_folder_gets_own_page, test_different_folders_get_separate_groups, test_deep_sparse_merges_upward, test_root_level_files, test_returns_all_files, test_root_files_count_correctly, test_init_creates_agents_md, test_init_creates_claude_md_unchanged_behavior, test_init_appends_to_existing_agents_md, test_init_does_not_duplicate_agents_md_guidance, test_claude_and_agents_share_guidance_constant, test_indexable_suffixes_is_union_of_parser_sets, test_other_suffixes_match_ts_extract_lang_configs, test_js_ts_suffixes_match_dispatch, test_is_indexable_accepts_known_suffixes, test_is_indexable_rejects_unknown_suffix, test_is_indexable_honours_part_glob, test_is_indexable_honours_path_glob, test_explicit_api_key_takes_priority_over_cli, test_falls_back_to_cli_when_no_key_and_cli_present, test_deep_flag_uses_configured_model_cli, test_no_key_no_cli_raises_so_callers_fall_back, test_describe_nodes_uses_cli_path_end_to_end, test_claude_cli_completion_invokes_print_mode, test_claude_cli_completion_raises_on_nonzero, test_clean_json_plain, test_clean_json_fenced, test_clean_json_preamble_then_fence, test_clean_json_preamble_then_bare_object, test_clean_json_list_payload, test_clean_json_raises_on_garbage, fake_sdk, fake_cli, fake_cli, fake_run, test_compute_hash_stable, test_empty_manifest_on_missing, test_save_and_reload, test_stale_files_detected, test_fresh_file_not_stale, test_load_manifest_missing_component_ids, _grammar_available, test_go_yields_nonzero_symbols, test_go_function, test_go_struct_is_class, test_go_method, test_go_docstring, test_go_calls, test_go_imports, test_java_yields_nonzero_symbols, test_java_class, test_java_method, test_java_static_method, test_java_docstring, test_java_calls, test_java_imports, test_ruby_yields_nonzero_symbols, test_ruby_class_and_module, test_ruby_method, test_ruby_top_level_function, test_ruby_docstring, test_ruby_calls, test_rust_yields_nonzero_symbols, test_rust_struct_and_trait_are_classes, test_rust_free_function, test_rust_impl_method, test_rust_docstring, test_rust_calls, test_unsupported_suffix_returns_empty, test_clean_report_produces_empty_plan, test_stale_and_untracked_files_go_to_reindex, test_missing_wiki_page_pulls_files_from_manifest, test_pages_missing_deep_included_when_deep_active, test_pages_missing_deep_excluded_when_skip_deep, test_cleanup_ops_carried_through, test_execute_restores_agents_md, test_execute_deletes_orphan_pages_and_prunes_manifest, test_execute_runs_reindex_for_files, fake_index_files, fake_finalise, test_top_level_function, test_class, test_method, test_method_with_dotted_class_path_uses_last_segment_as_member, test_root_level_file, test_is_deterministic, test_unknown_type_falls_back_to_term, test_malformed_id_without_separator_is_safe, test_smart_rejects_combo_with_force, test_smart_rejects_combo_with_staged, test_smart_bails_when_no_indexable_files, test_smart_dry_run_does_not_modify_filesystem, test_smart_repairs_missing_wiki_page, test_smart_clean_state_is_noop, test_smart_fills_fresh_repo_with_no_manifest, test_smart_dry_run_reports_full_initial_index_without_changes, test_smart_fills_never_indexed_tracked_file, test_smart_dry_run_clean_repo_exits_zero, test_smart_dry_run_drift_exits_nonzero, test_empty_report_is_clean, test_report_with_stale_files_not_clean, test_report_counts_all_drift_classes, test_scan_flags_missing_manifest, test_scan_detects_stale_files, test_scan_detects_dangling_manifest_entries, test_scan_detects_untracked_source_files, test_scan_detects_missing_wiki_page, test_scan_detects_orphan_wiki_page, test_scan_detects_missing_index_and_skill, test_scan_detects_missing_claude_md_snippet, test_scan_detects_missing_agents_md_snippet, test_scan_agents_md_present_and_valid_not_flagged, test_scan_detects_missing_gitignore_entry, test_scan_detects_hook_drift, test_scan_detects_pages_missing_deep_sections, test_scan_deep_page_with_empty_narrative_not_flagged, test_scan_skips_deep_check_when_skip_deep_true, test_print_report_clean, test_print_report_lists_each_drift, test_scan_skips_hook_check_when_check_hook_false, test_build_page_contains_symbol, test_build_page_contains_calls, test_build_page_contains_called_by, test_build_page_no_agent_hints, test_build_index_contains_page, test_write_page_creates_file, test_page_starts_with_frontmatter_delimiter, test_page_frontmatter_is_valid_yaml_with_required_type, test_page_frontmatter_title_and_resource, test_page_frontmatter_tags_from_path_segments, test_page_frontmatter_timestamp_passed_in_not_computed, test_page_frontmatter_description_from_narrative_first_sentence, test_page_frontmatter_description_generic_when_no_narrative, test_page_body_sections_preserved_below_frontmatter, test_index_frontmatter_has_okf_version, test_page_renders_relationships_block_per_symbol, test_page_relationships_block_caps_long_lists, test_index_renders_core_abstractions, test_page_basename_root_group, test_page_basename_nested_group, test_page_relpath_matches_write_page |
## Last Indexed
Commit: b950860bb04e52f69692358bb14dd59055cf805c — 2026-06-21