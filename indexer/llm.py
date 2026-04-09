# indexer/llm.py
from __future__ import annotations
import json, os
from indexer.ast_parser import ASTNode
from indexer.config import Config

_ANTHROPIC_MODELS = {"claude", "anthropic"}


def _is_anthropic(cfg: Config) -> bool:
    return any(cfg.provider.startswith(p) for p in _ANTHROPIC_MODELS)


def _resolve_api_key(cfg: Config) -> str | None:
    """
    api_key_env can be either:
    - an env var name (e.g. "GROQ_API_KEY") -> look it up from environment
    - an actual key value (e.g. "gsk_...") -> use it directly
    - empty string "" -> auto-detect from well-known env vars
    """
    value = cfg.api_key_env
    if not value:
        # Auto-detect from common env vars based on provider
        for env_var in ("ANTHROPIC_API_KEY", "GROQ_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY"):
            key = os.environ.get(env_var)
            if key:
                return key
        return None
    # If it looks like an actual key (has lowercase/mixed case), use directly
    if " " not in value and not value.isupper() and not value.replace("_", "").isupper():
        return value
    return os.environ.get(value)


def _anthropic_completion(model: str, system: str, user: str, api_key: str) -> str:
    """Call Anthropic SDK directly with the provided API key."""
    import anthropic

    bare_model = model.removeprefix("anthropic/")
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=bare_model,
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return response.content[0].text


def describe_nodes(nodes: list[ASTNode], cfg: Config) -> dict[str, str]:
    """
    Describe a batch of ASTNodes via LLM.
    Returns dict mapping node.id -> one-line description (max 15 words).
    Falls back to empty strings on any error.

    Uses Anthropic SDK directly (Claude Code session auth) when:
    - provider starts with "anthropic/" or "claude"
    - api_key_env is empty
    """
    api_key = _resolve_api_key(cfg)
    use_sdk = _is_anthropic(cfg) and api_key is None

    prompt_items = [
        {
            "id": n.id,
            "type": n.type,
            "docstring": n.docstring or "",
            "calls": n.calls[:15],
            "line_start": n.line_start,
            "line_end": n.line_end,
        }
        for n in nodes
    ]

    system = (
        "You are a code documentation assistant. "
        "Given a list of code symbols with their type, optional docstring, line range, and list of functions they call, "
        "return a JSON object mapping each symbol ID to a single short description (max 15 words, no period). "
        "Focus on WHAT it does and HOW (e.g. 'Validates Auth0 JWT tokens using JWKS public keys, returns UserClaims'). "
        "For classes, describe the role. For methods, describe the action and key side-effects. "
        "Be specific — avoid generic phrases like 'handles', 'manages', 'initializes'. "
        "Be factual and structural — no opinions, no guidance. "
        "Response must be valid JSON only, no markdown fences."
    )
    user = json.dumps(prompt_items)

    try:
        if use_sdk:
            raw = _anthropic_completion(cfg.provider, system, user, api_key)
        else:
            import litellm
            response = litellm.completion(
                model=cfg.provider,
                api_key=api_key,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            raw = response.choices[0].message.content

        raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        result = json.loads(raw)
        return {n.id: result.get(n.id, "") for n in nodes}
    except Exception as e:
        if isinstance(e, (TypeError, AttributeError, ImportError, NameError)):
            raise
        return {n.id: "" for n in nodes}


def describe_files(file_nodes: dict[str, list[ASTNode]], cfg: Config) -> dict[str, str]:
    """
    Describe each file at the module level.
    file_nodes: dict mapping rel_path -> list of ASTNodes in that file.
    Returns dict mapping rel_path -> one-line purpose string.
    """
    api_key = _resolve_api_key(cfg)
    use_sdk = _is_anthropic(cfg) and api_key is None

    prompt_items = [
        {
            "file": rel_path,
            "top_level_symbols": [
                {"name": n.id.split("::")[-1], "type": n.type, "docstring": n.docstring or ""}
                for n in nodes
                if n.type in ("class", "function")
            ][:12],
        }
        for rel_path, nodes in file_nodes.items()
    ]

    system = (
        "You are a code documentation assistant. "
        "Given a list of source files with their top-level classes and functions, "
        "return a JSON object mapping each file path to a single short description (max 12 words, no period). "
        "Describe the module's responsibility at a system level (e.g. 'Supabase-backed store for agent authentication sessions'). "
        "Be specific — use the symbol names as hints. "
        "Response must be valid JSON only, no markdown fences."
    )
    user = json.dumps(prompt_items)

    try:
        if use_sdk:
            raw = _anthropic_completion(cfg.provider, system, user, api_key)
        else:
            import litellm
            response = litellm.completion(
                model=cfg.provider,
                api_key=api_key,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            raw = response.choices[0].message.content

        raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        result = json.loads(raw)
        return {f: result.get(f, "") for f in file_nodes}
    except Exception as e:
        if isinstance(e, (TypeError, AttributeError, ImportError, NameError)):
            raise
        return {f: "" for f in file_nodes}


def synthesize_commit_message(changed_files: list[str], descriptions: dict[str, str], cfg: Config) -> str:
    """
    Generate a one-line commit message from changed files and symbol descriptions.
    Returns empty string on any error.
    """
    api_key = _resolve_api_key(cfg)
    use_sdk = _is_anthropic(cfg) and api_key is None

    system = (
        "Write a single git commit message (max 72 chars) summarising the code changes. "
        "No conventional commit prefix. No markdown. Just the message text."
    )
    user = json.dumps({"changed_files": changed_files, "symbols": descriptions})

    try:
        if use_sdk:
            raw = _anthropic_completion(cfg.provider, system, user, api_key)
        else:
            import litellm
            response = litellm.completion(
                model=cfg.provider,
                api_key=api_key,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            raw = response.choices[0].message.content

        return raw.strip()[:72]
    except Exception as e:
        if isinstance(e, (TypeError, AttributeError, ImportError, NameError)):
            raise
        return ""
