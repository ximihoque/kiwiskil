---
name: codebase
description: >
  Navigate this codebase. Activates when the user asks about code structure,
  where a function or class lives, how a module works, who calls a method,
  what a file does, how a request flows end-to-end, what changed, or where
  to make an edit. Trigger phrases include: "where is", "how does X work",
  "what does X do", "find the code for", "which file", "who calls", "trace
  the flow", "show me how", "explain the architecture", "what module",
  "read the source", "navigate the repo", "look at the codebase",
  "understand the code". Do NOT activate for general programming questions
  unrelated to this specific repo, writing new code from scratch, or tasks
  that require no codebase knowledge.
---

# Codebase Navigation

This repo is indexed. **Check the wiki before reading any source file.**
The wiki captures structure, relationships, and constraints in a fraction of the tokens.

## Stats

- **354 symbols** across **37 files** — indexed 2026-06-29 @ `354cb313`
- Wiki: `wiki/` — 3 page(s)
- Manifest: `.indexer/manifest.json` — maps every file to its wiki page and component IDs

## System Overview

The indexer is a polyglot codebase analysis engine that translates source code into a structured SCIP graph for downstream LLM consumption. It coordinates multi-language parsing via `ast_parser.py` and `ts_extract.py`, which feed a central `graph.py` structure managed by `grouper.py` and `manifest.py`. The `llm.py` and `repair.py` modules integrate AI-driven analysis to validate and fix index inconsistencies, orchestrated by a CLI interface that leverages `config.py` for environment-specific execution.
## Key Request Flows
- Source code discovery → git.py/manifest.py detection → ast_parser.py/ts_extract.py parsing → scip.py graph generation
- SCIP graph initialization → grouper.py entity clustering → llm.py analysis hook → repair.py consistency patching
- CLI configuration load → indexer core processing → verify.py integrity check → wiki.py documentation generation

## Wiki Pages

| Page | Covers | Key Entry Points |
|------|--------|-----------------|
| [indexer](../wiki/indexer.md) | indexer/__init__.py, indexer/ast_parser.py, indexer/cli.py, indexer/config.py, indexer/git.py, indexer/graph.py, indexer/grouper.py, indexer/hooks.py, indexer/js_parser.py, indexer/langs.py, indexer/llm.py, indexer/manifest.py, indexer/repair.py, indexer/scip.py, indexer/ts_extract.py, indexer/verify.py, indexer/wiki.py |  |
| [tests](../wiki/tests.md) | tests/__init__.py, tests/test_ast_parser.py, tests/test_config.py, tests/test_graph.py, tests/test_grouper.py, tests/test_init.py, tests/test_langs.py, tests/test_llm_dispatch.py, tests/test_manifest.py, tests/test_multilang.py, tests/test_repair_plan.py, tests/test_scip.py, tests/test_smart_integration.py, tests/test_verify.py, tests/test_wiki.py |  |
| [tests_fixtures](../wiki/tests_fixtures.md) | tests/fixtures/sample_go/server.go, tests/fixtures/sample_java/Widget.java, tests/fixtures/sample_py/auth.py, tests/fixtures/sample_ruby/widget.rb, tests/fixtures/sample_rust/widget.rs |  |
## Critical Constraints (read before editing)
**indexer**
- The `parse_file` function returns an empty list upon encountering any syntax error, rather than raising an exception.
- Cached AST nodes are stored as JSON files; manual modification of these files may result in deserialization errors or corrupted index states.
- The `_ensure_nav_guidance` method is idempotent and should be called whenever initializing a repo to ensure CLAUDE.md integrity.
- File tracking is strictly dependent on the existence of a `.git` repository; operations requiring `is_git_repo` will fail in detached environments.
- The system performs grouping based on logic density; file membership in a group is determined by `density_group` and cannot be manually overridden.
**tests**
- Blast radius operations exclude the input node by definition; a node is never part of its own downstream impact set.
- The `god_nodes` function returns results sorted by degree, but its output size is clamped by the input N parameter, even if total nodes are fewer.
- PageRank implementations expect all node keys to be present in the returned dictionary, with values guaranteed to sum to approximately 1.0.
- AST cache files must be treated as transient; the test suite uses `TemporaryDirectory` to ensure filesystem isolation during roundtrip verification.
- Callers/Callees logic filters out unresolvable external names, meaning the graph only contains internal code references.

## Workflow — How to Answer Questions About This Codebase

Follow these steps in order. Do not skip ahead to reading source files.

1. **Orient** — Read `wiki/INDEX.md` first. It has the system overview, module map, and cross-cutting flows.

2. **Locate the module** — Match the question to a wiki page from the table above. Read that page only; do not read unrelated pages.

3. **Look up symbols** — Component IDs follow `relative/path.py::ClassName.method_name`. Find the relevant ID in the wiki page's Key Symbols table and read its description there.

4. **Trace calls without reading source** — Use the `## Relationships → Called by` section on the wiki page to trace callers. Use `## Relationships → Calls` to trace callees.

5. **Read source only when necessary** — Once you know the exact file and line range from the manifest or wiki, read only that range. Do not read whole files speculatively.

6. **Answer with specifics** — Include the component ID, file path, and line range (if known) in your answer so the user can navigate directly.

## Output Format

- Always name the specific file and component ID when identifying where code lives.
- For call traces, show the chain: `A → B → C`, one line per hop.
- For architecture questions, describe the flow in prose then list the files involved.
- Keep answers concise. Do not dump raw wiki content — summarise what is relevant.
- If a question requires reading source, state which file and lines you are about to read before reading them.

## When to Use Wiki vs Source

| Question type | Use |
|--------------|-----|
| What does X do? | Wiki — Key Symbols table |
| Who calls X? | Wiki — Relationships → Called by |
| What does this module own? | Wiki — Modules table |
| How does a request flow end-to-end? | Wiki — Data Flows section (if --deep indexed) |
| What are the gotchas or invariants? | Wiki — Design Constraints section (if --deep indexed) |
| What is the exact implementation? | Source — use line_start/line_end from manifest |
| Is X tested? | Source — check test files directly |

## Component ID Format

```
relative/path.py::ClassName.method_name   ← method
relative/path.py::ClassName               ← class
relative/path.py::function_name           ← top-level function
```

## Manifest Lookup

To find which wiki page covers a file:
```
.indexer/manifest.json → files["path/to/file.py"] → wiki_page
```

To find all symbols in a file:
```
.indexer/manifest.json → files["path/to/file.py"] → component_ids
```

## Edge Cases

- **Symbol not in wiki** — The index covers files tracked at index time. If a symbol is missing, it was added after the last `kiwiskil run`. Tell the user and read the source file directly.
- **Wiki page missing** — If a wiki page linked from the index does not exist, fall back to the manifest and source. Note the gap to the user.
- **Ambiguous name** — If multiple symbols share a name, list all matching component IDs and ask the user which they mean before proceeding.
- **Question spans multiple modules** — Read each relevant wiki page in turn. Do not conflate descriptions from different pages.