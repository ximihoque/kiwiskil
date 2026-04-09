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
    - empty string "" -> no key (use Claude Code session auth)
    """
    value = cfg.api_key_env
    if not value:
        return None
    # If it looks like an actual key (has lowercase/mixed case), use directly
    if " " not in value and not value.isupper() and not value.replace("_", "").isupper():
        return value
    return os.environ.get(value)


def _anthropic_completion(model: str, system: str, user: str) -> str:
    """
    Call Anthropic SDK directly — picks up Claude Code session auth automatically.
    No API key needed when running inside Claude Code.
    """
    import anthropic

    # Strip "anthropic/" prefix if present — SDK uses bare model names
    bare_model = model.removeprefix("anthropic/")

    client = anthropic.Anthropic()
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
    Returns dict mapping node.id -> one-line description (max 12 words).
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
            "calls": n.calls[:10],
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
    user = json.dumps(prompt_items)

    try:
        if use_sdk:
            raw = _anthropic_completion(cfg.provider, system, user)
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
            raw = _anthropic_completion(cfg.provider, system, user)
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
