## Codebase Navigation

This repo is indexed with kiwiskil. Before reading any source file or answering any code question:

1. Load `.indexer/skills/codebase.md` as a skill — it contains the full navigation workflow.
2. Read `wiki/INDEX.md` for the system overview and module map.
3. Match the question to a wiki page, look up symbols there, and only read source when you know the exact file and line range.

Do not read source files speculatively. The wiki gives you structure and relationships in a fraction of the tokens.

- Wiki pages: `wiki/` — grouped by logical density, not directory structure
- Manifest: `.indexer/manifest.json` — maps every file to its wiki page and component IDs
- Component IDs: `relative/path.py::ClassName.method_name`
