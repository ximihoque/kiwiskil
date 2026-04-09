from __future__ import annotations
from collections import defaultdict
from pathlib import Path


def density_group(files: list[str], merge_threshold: int = 6) -> dict[str, str]:
    """
    Maps each file path to a wiki page label (a folder path string).

    Algorithm:
    1. Count files reachable under each folder prefix.
    2. Walk from the deepest folder upward. If a folder has fewer than
       merge_threshold files reachable under it, merge it into its parent.
    3. The resolved group for each file is the shallowest folder whose
       subtree count >= merge_threshold, or the top-level folder if none qualify.

    Returns: dict mapping file_path -> wiki_page_label (a folder string)
    """
    if not files:
        return {}

    def folder_of(f: str) -> str:
        parent = str(Path(f).parent)
        return "." if parent == "." else parent

    def prefixes(folder: str) -> list[str]:
        """All ancestor folder prefixes from deepest to shallowest."""
        if folder == ".":
            return ["."]
        parts = folder.split("/")
        return ["/".join(parts[:i]) for i in range(len(parts), 0, -1)]

    # Count how many files fall under each prefix
    prefix_count: dict[str, int] = defaultdict(int)
    for f in files:
        folder = folder_of(f)
        for prefix in prefixes(folder):
            prefix_count[prefix] += 1
        if folder == ".":
            prefix_count["."] += 1

    def resolve_group(f: str) -> str:
        folder = folder_of(f)
        all_prefixes = prefixes(folder)

        # Walk from deepest to shallowest, find first prefix that meets threshold
        for prefix in all_prefixes:
            if prefix_count[prefix] >= merge_threshold:
                return prefix

        # None met threshold — use the shallowest non-root prefix, or "." for root
        # For files at depth, merge to immediate parent folder
        if len(all_prefixes) > 1:
            return all_prefixes[-2]  # parent of deepest
        return "."  # root level

    return {f: resolve_group(f) for f in files}
