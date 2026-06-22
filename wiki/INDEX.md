---
type: Code Index
okf_version: '0.1'
title: Codebase Index
---
# Codebase Index

## System Overview

kiwiskil is a codebase indexer that transforms source repos into a checked-in, LLM-navigable knowledge artifact (wiki pages + manifest + skill file) with no running server. The pipeline is orchestrated by `cli.py` (`run`/`run --smart`/`run --staged`/`status`/`init`/`hook`): `langs.py` filters indexable files; `ast_parser.py`, `js_parser.py`, and `ts_extract.py` parse symbols and call graphs per language; `grouper.py` clusters files into wiki pages by density threshold; `llm.py` calls Anthropic SDK or falls back to the `claude` CLI subprocess to generate LLM descriptions; `wiki.py` renders Jinja2-templated markdown with OKF YAML frontmatter; and `manifest.py` persists file→component-ID hash mappings. `graph.py` computes PageRank and blast-radius over the call graph; `verify.py` detects drift between filesystem, manifest, and wiki; `repair.py` computes and executes a minimal `RepairPlan`; and `hooks.py` manages the pre-commit hook for incremental re-indexing.
## Key Flows
- Full index: cli.run → git.all_tracked_files → langs.is_indexable → cli._index_and_persist → ast_parser.parse_file / js_parser.parse_js_file / ts_extract.extract_generic → grouper.density_group → llm.describe_nodes / deep_enrich_page → graph.build_blast_radius_map → wiki.build_page / write_page → cli._finalise_index_and_skill [graph.repo_map + llm.deep_enrich_index → wiki.build_index] → manifest.save_manifest
- Incremental staged (pre-commit hook): hooks.py triggers cli.run --staged → git.staged_files → langs.is_indexable → manifest.Manifest.stale_files (hash check) → cli._index_and_persist (changed files only) → same _index_files/_finalise pipeline → manifest.save_manifest → llm.synthesize_commit_message
- Smart repair: cli.run --smart → cli._run_smart → verify.scan [manifest vs filesystem vs wiki drift detection → VerifyReport] → repair.plan [VerifyReport → RepairPlan: dirty re-index, orphan page delete, dangling entry prune] → repair.execute [cli._index_files + cli._finalise_index_and_skill + manifest.save_manifest + cli._ensure_nav_guidance]
- LLM dispatch: llm._complete → llm._resolve_api_key (env var priority) → Anthropic SDK path (llm._anthropic_completion) OR claude CLI subprocess fallback (llm._claude_cli_completion) → llm._clean_json strips fences/preamble → structured dict returned to describe_nodes / deep_enrich_page / deep_enrich_index
- Blast radius tracing: graph.blast_radius(symbol) → BFS over reverse call edges via graph._index_by_id → transitive set of impacted component IDs → precomputed for all nodes by graph.build_blast_radius_map during _index_files → rendered per symbol in wiki.py._symbol_relationships as 'Editing this affects' lists

## Structure
| Wiki Page | Covers | Entry Points |
|-----------|--------|--------------|
| wiki/indexer.md | indexer/__init__.py, indexer/ast_parser.py, indexer/cli.py, indexer/config.py, indexer/git.py, indexer/graph.py, indexer/grouper.py, indexer/hooks.py, indexer/js_parser.py, indexer/langs.py, indexer/llm.py, indexer/manifest.py, indexer/repair.py, indexer/scip.py, indexer/ts_extract.py, indexer/verify.py, indexer/wiki.py |  |
| wiki/tests.md | tests/__init__.py, tests/test_ast_parser.py, tests/test_config.py, tests/test_graph.py, tests/test_grouper.py, tests/test_init.py, tests/test_langs.py, tests/test_llm_dispatch.py, tests/test_manifest.py, tests/test_multilang.py, tests/test_repair_plan.py, tests/test_scip.py, tests/test_smart_integration.py, tests/test_verify.py, tests/test_wiki.py |  |
| wiki/tests_fixtures.md | tests/fixtures/sample_go/server.go, tests/fixtures/sample_java/Widget.java, tests/fixtures/sample_py/auth.py, tests/fixtures/sample_ruby/widget.rb, tests/fixtures/sample_rust/widget.rs |  |
## Last Indexed
Commit: 8a10bfcbb107480b1347b31d82199d22383ca1b0 — 2026-06-22