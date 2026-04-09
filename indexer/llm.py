# indexer/llm.py
from __future__ import annotations
import json, os
from indexer.ast_parser import ASTNode
from indexer.config import Config


def _resolve_api_key(cfg: Config) -> str | None:
    """
    api_key_env can be either:
    - an env var name (e.g. "GROQ_API_KEY") -> look it up from environment
    - an actual key value (e.g. "gsk_...") -> use it directly
    """
    value = cfg.api_key_env
    # If it contains lowercase letters or special chars typical of keys, treat as direct key
    if " " not in value and not value.isupper() and not value.replace("_", "").isupper():
        return value
    return os.environ.get(value)


def describe_nodes(nodes: list[ASTNode], cfg: Config) -> dict[str, str]:
    """
    Send a batch of ASTNodes to LiteLLM.
    Returns dict mapping node.id -> one-line description string (max 12 words).
    Returns empty descriptions (node.id -> "") on any API error.
    """
    import litellm

    api_key = _resolve_api_key(cfg)

    prompt_items = [
        {
            "id": n.id,
            "type": n.type,
            "docstring": n.docstring or "",
            "calls": n.calls[:10],  # cap to avoid token bloat
        }
        for n in nodes
    ]

    system = (
        "You are a code documentation assistant. "
        "Given a list of code symbols with their type, optional docstring, and list of functions they call, "
        "return a JSON object mapping each symbol ID to a single short description (max 12 words, no period). "
        "Be factual and structural — no opinions, no guidance. "
        "Response must be valid JSON only, no markdown fences."
    )

    try:
        response = litellm.completion(
            model=cfg.provider,
            api_key=api_key,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": json.dumps(prompt_items)},
            ],
        )
        raw = response.choices[0].message.content
        # Strip markdown fences if model wrapped the JSON
        raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        result = json.loads(raw)
        # Ensure all node IDs are present in result (fill missing with "")
        return {n.id: result.get(n.id, "") for n in nodes}
    except Exception as e:
        if isinstance(e, (TypeError, AttributeError, ImportError, NameError)):
            raise
        return {n.id: "" for n in nodes}


def synthesize_commit_message(changed_files: list[str], descriptions: dict[str, str], cfg: Config) -> str:
    """
    Given changed files and their symbol descriptions, return a one-line commit message (max 72 chars).
    Returns empty string on any API error.
    """
    import litellm

    api_key = _resolve_api_key(cfg)

    summary = {
        "changed_files": changed_files,
        "symbols": descriptions,
    }

    try:
        response = litellm.completion(
            model=cfg.provider,
            api_key=api_key,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Write a single git commit message (max 72 chars) summarising the code changes. "
                        "No conventional commit prefix. No markdown. Just the message text."
                    ),
                },
                {"role": "user", "content": json.dumps(summary)},
            ],
        )
        return response.choices[0].message.content.strip()[:72]
    except Exception as e:
        if isinstance(e, (TypeError, AttributeError, ImportError, NameError)):
            raise
        return ""
