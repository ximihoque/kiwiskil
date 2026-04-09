# indexer/hooks.py
from __future__ import annotations
from pathlib import Path

HOOK_MARKER = "# managed by codeindexer"
HOOK_CONTENT = "indexer run --staged"
HOOK_SCRIPT = f"""\
#!/bin/sh
{HOOK_MARKER}
{HOOK_CONTENT}
"""


def install_hook(repo_root: Path) -> None:
    """Install the pre-commit hook in repo_root/.git/hooks/pre-commit.

    If a pre-commit hook already exists and is not managed by codeindexer,
    append our script to it rather than overwriting.
    If already installed, do nothing.
    """
    hook_path = repo_root / ".git" / "hooks" / "pre-commit"

    if hook_path.exists():
        existing = hook_path.read_text()
        if HOOK_MARKER in existing:
            return  # already installed, nothing to do
        # Append to existing hook
        updated = existing.rstrip() + "\n\n" + HOOK_SCRIPT
        hook_path.write_text(updated)
    else:
        hook_path.parent.mkdir(parents=True, exist_ok=True)
        hook_path.write_text(HOOK_SCRIPT)

    hook_path.chmod(0o755)


def remove_hook(repo_root: Path) -> None:
    """Remove the codeindexer-managed portion of the pre-commit hook.

    If the hook consists entirely of our script, delete the file.
    If our script was appended to an existing hook, remove only our lines.
    If not installed, do nothing.
    """
    hook_path = repo_root / ".git" / "hooks" / "pre-commit"

    if not hook_path.exists():
        return

    content = hook_path.read_text()
    if HOOK_MARKER not in content:
        return  # not managed by us

    # Remove lines added by codeindexer
    lines = content.splitlines()
    cleaned = [
        line for line in lines
        if HOOK_MARKER not in line and HOOK_CONTENT not in line
    ]
    result = "\n".join(cleaned).strip()

    if result and result != "#!/bin/sh":
        hook_path.write_text(result + "\n")
    else:
        hook_path.unlink()
