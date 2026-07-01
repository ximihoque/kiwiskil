---
type: Code Index
okf_version: '0.1'
title: Codebase Index
---
# Codebase Index

## System Overview

kiwiskil is a polyglot codebase indexing engine that transforms a git repository into a structured, LLM-navigable wiki. The pipeline runs through five sequential phases orchestrated by `cli.py` (`_index_files` → `_finalise_index_and_skill`): source files are discovered via `git.py`, parsed into `ASTNode` records by `ast_parser.py` (Python stdlib AST), `js_parser.py` (tree-sitter JS/TS), and `ts_extract.py` (tree-sitter Go/Java/Ruby/Rust), then described by `llm.py` (Anthropic SDK / claude CLI / LiteLLM). `grouper.py` clusters files into wiki pages by density-based folder merging; `wiki.py` renders Jinja2 templates into `wiki/*.md` and `wiki/INDEX.md`; `manifest.py` persists file hashes and SCIP component IDs for incremental re-indexing. `graph.py` computes PageRank, blast radius, and god-node rankings over the call graph to drive `repo_map` and per-symbol relationship sections. `verify.py` detects drift (stale files, missing pages, orphaned entries), and `repair.py` translates a `VerifyReport` into a `RepairPlan` that `_run_smart` executes without a full re-index.
## Key Flows
- Full index run: `cli.run` → `git.all_tracked_files` → `_index_and_persist` → `_index_files` (parse → `llm.describe_nodes`/`describe_files`/`deep_enrich_page` → `build_blast_radius_map` → `wiki.build_page`/`write_page`) → `_finalise_index_and_skill` (`graph.repo_map`/`god_nodes` → `llm.deep_enrich_index` → `wiki.build_index`/`write_index`) → `manifest.save_manifest`
- Smart incremental repair: `cli.run --smart` → `_run_smart` → `verify.scan` (VerifyReport) → `repair.plan` (RepairPlan) → `repair.execute` → `_index_files` (stale files only) → `_finalise_index_and_skill` → `save_manifest`
- LLM dispatch: `llm.describe_nodes`/`deep_enrich_page`/`deep_enrich_index` → `_complete` → `_is_anthropic` branch: `_anthropic_completion` (Anthropic SDK) | `_claude_cli_completion` (subprocess claude CLI) | `completion` (LiteLLM) → `_clean_json` (parse fenced/bare JSON response)
- Source parsing: `_index_files` → `ast_parser.parse_file` → Python: stdlib `ast.walk` | JS/TS: `js_parser.parse_js_file` (tree-sitter) | Go/Java/Ruby/Rust: `ts_extract.extract_generic` (tree-sitter LangConfig) → `ASTNode` list → `scip.scip_symbol` → `manifest.file_entry_for` → `Manifest`
- Pre-commit hook flow: `hooks.install_hook` (writes `.git/hooks/pre-commit` via `_hook_script_fresh`/`_hook_script_append`) → git commit triggers hook → `cli.run --staged` → `git.staged_files` → `_index_and_persist` (staged files expanded to groups via `_expand_candidates_to_groups`) → `manifest.save_manifest` → `synthesize_commit_message`

## Structure
| Wiki Page | Covers | Entry Points |
|-----------|--------|--------------|
| wiki/indexer.md | indexer/__init__.py, indexer/ast_parser.py, indexer/cli.py, indexer/config.py, indexer/git.py, indexer/graph.py, indexer/grouper.py, indexer/hooks.py, indexer/js_parser.py, indexer/langs.py, indexer/llm.py, indexer/manifest.py, indexer/repair.py, indexer/scip.py, indexer/ts_extract.py, indexer/verify.py, indexer/wiki.py |  |
| wiki/tests.md | tests/__init__.py, tests/test_ast_parser.py, tests/test_config.py, tests/test_graph.py, tests/test_grouper.py, tests/test_init.py, tests/test_langs.py, tests/test_llm_dispatch.py, tests/test_manifest.py, tests/test_multilang.py, tests/test_repair_plan.py, tests/test_scip.py, tests/test_smart_integration.py, tests/test_verify.py, tests/test_wiki.py |  |
| wiki/tests_fixtures.md | tests/fixtures/sample_go/server.go, tests/fixtures/sample_java/Widget.java, tests/fixtures/sample_py/auth.py, tests/fixtures/sample_ruby/widget.rb, tests/fixtures/sample_rust/widget.rs |  |
## Last Indexed
Commit: 76002e95a8e800f565b122b68a775c9245d75ff1 — 2026-07-01