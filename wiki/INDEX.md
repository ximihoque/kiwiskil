---
type: Code Index
okf_version: '0.1'
title: Codebase Index
---
# Codebase Index

## System Overview

The indexer is a polyglot codebase analysis engine that translates source code into a structured SCIP graph for downstream LLM consumption. It coordinates multi-language parsing via `ast_parser.py` and `ts_extract.py`, which feed a central `graph.py` structure managed by `grouper.py` and `manifest.py`. The `llm.py` and `repair.py` modules integrate AI-driven analysis to validate and fix index inconsistencies, orchestrated by a CLI interface that leverages `config.py` for environment-specific execution.
## Key Flows
- Source code discovery → git.py/manifest.py detection → ast_parser.py/ts_extract.py parsing → scip.py graph generation
- SCIP graph initialization → grouper.py entity clustering → llm.py analysis hook → repair.py consistency patching
- CLI configuration load → indexer core processing → verify.py integrity check → wiki.py documentation generation

## Structure
| Wiki Page | Covers | Entry Points |
|-----------|--------|--------------|
| wiki/indexer.md | indexer/__init__.py, indexer/ast_parser.py, indexer/cli.py, indexer/config.py, indexer/git.py, indexer/graph.py, indexer/grouper.py, indexer/hooks.py, indexer/js_parser.py, indexer/langs.py, indexer/llm.py, indexer/manifest.py, indexer/repair.py, indexer/scip.py, indexer/ts_extract.py, indexer/verify.py, indexer/wiki.py |  |
| wiki/tests.md | tests/__init__.py, tests/test_ast_parser.py, tests/test_config.py, tests/test_graph.py, tests/test_grouper.py, tests/test_init.py, tests/test_langs.py, tests/test_llm_dispatch.py, tests/test_manifest.py, tests/test_multilang.py, tests/test_repair_plan.py, tests/test_scip.py, tests/test_smart_integration.py, tests/test_verify.py, tests/test_wiki.py |  |
| wiki/tests_fixtures.md | tests/fixtures/sample_go/server.go, tests/fixtures/sample_java/Widget.java, tests/fixtures/sample_py/auth.py, tests/fixtures/sample_ruby/widget.rb, tests/fixtures/sample_rust/widget.rs |  |
## Last Indexed
Commit: 354cb313b1ed28da45f5d9e1f31e4b8267b26e1c — 2026-06-29