---
type: Code Index
okf_version: '0.1'
title: Codebase Index
---
# Codebase Index

## System Overview

kiwiskil is a codebase indexer that transforms source repos into a checked-in, LLM-navigable knowledge artifact (wiki pages + manifest + skill file) with no running server. The pipeline entry point is `cli.py` (`run`/`run --smart`/`run --staged`/`status`/`init`/`hook`): language filtering via `langs.py`, multi-language symbol/call-graph extraction via `ast_parser.py`, `js_parser.py`, and `ts_extract.py`, file clustering via `grouper.py` (density threshold), and markdown wiki generation via `wiki.py` (Jinja2 + OKF YAML frontmatter). `llm.py` drives all LLM calls (Anthropic SDK or `claude` CLI subprocess fallback) for node descriptions and page enrichment; `graph.py` computes PageRank and blast-radius over the call graph; `manifest.py` persists file→component-ID hash mappings; and `verify.py`/`repair.py` detect and resolve drift between filesystem, manifest, and wiki. `hooks.py` wires the pre-commit hook for incremental re-indexing.
## Key Flows
- Full index: cli.run → git.all_tracked_files → langs.is_indexable → cli._index_and_persist → ast_parser.parse_file / js_parser.parse_js_file / ts_extract.extract_generic → grouper.density_group → llm.describe_nodes / deep_enrich_page → graph.build_blast_radius_map → wiki.build_page / write_page → cli._finalise_index_and_skill [graph.repo_map + llm.deep_enrich_index → wiki.build_index] → manifest.save_manifest
- Incremental staged (pre-commit hook): hooks.py triggers cli.run --staged → git.staged_files → langs.is_indexable → manifest.Manifest.stale_files (hash check) → cli._index_and_persist (changed files only) → same _index_files/_finalise pipeline → manifest.save_manifest → llm.synthesize_commit_message
- Smart repair: cli.run --smart → cli._run_smart → verify.scan [manifest vs filesystem vs wiki drift → VerifyReport] → repair.plan [VerifyReport → RepairPlan] → repair.execute [cli._index_files + cli._finalise_index_and_skill + manifest.save_manifest + cli._ensure_nav_guidance]
- LLM dispatch: llm._complete → llm._resolve_api_key → Anthropic SDK (llm._anthropic_completion) OR claude CLI subprocess fallback (llm._claude_cli_completion) → llm._clean_json strips fences/preamble → structured dict returned to describe_nodes / deep_enrich_page / deep_enrich_index
- Blast radius tracing: graph.blast_radius(symbol) → BFS over reverse call edges via graph._index_by_id → transitive impacted component IDs → precomputed by graph.build_blast_radius_map during _index_files → rendered per symbol in wiki.py._symbol_relationships as 'Editing this affects' lists

## Structure
| Wiki Page | Covers | Entry Points |
|-----------|--------|--------------|
| wiki/indexer.md | indexer/__init__.py, indexer/ast_parser.py, indexer/cli.py, indexer/config.py, indexer/git.py, indexer/graph.py, indexer/grouper.py, indexer/hooks.py, indexer/js_parser.py, indexer/langs.py, indexer/llm.py, indexer/manifest.py, indexer/repair.py, indexer/scip.py, indexer/ts_extract.py, indexer/verify.py, indexer/wiki.py |  |
| wiki/tests.md | tests/__init__.py, tests/test_ast_parser.py, tests/test_config.py, tests/test_graph.py, tests/test_grouper.py, tests/test_init.py, tests/test_langs.py, tests/test_llm_dispatch.py, tests/test_manifest.py, tests/test_multilang.py, tests/test_repair_plan.py, tests/test_scip.py, tests/test_smart_integration.py, tests/test_verify.py, tests/test_wiki.py |  |
| wiki/tests_fixtures.md | tests/fixtures/sample_go/server.go, tests/fixtures/sample_java/Widget.java, tests/fixtures/sample_py/auth.py, tests/fixtures/sample_ruby/widget.rb, tests/fixtures/sample_rust/widget.rs |  |
## Last Indexed
Commit: 2f65edbca068bce4230f8080bee9da28f9bebcca — 2026-06-22