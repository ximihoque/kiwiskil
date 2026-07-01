# tests/test_llm_dispatch.py
"""The LLM provider dispatcher: API key > claude CLI > graceful skip.

These tests mock the boundaries (env, shutil.which, subprocess, the anthropic
SDK, litellm) so no real network/CLI call happens.
"""
import indexer.llm as llm
from indexer.config import Config


def _cfg(**kw):
    c = Config()
    for k, v in kw.items():
        setattr(c, k, v)
    return c


# ── provider selection ────────────────────────────────────────────────────────

def test_explicit_api_key_takes_priority_over_cli(monkeypatch):
    """When an API key is resolvable, never shell out to the CLI."""
    monkeypatch.setattr(llm, "_resolve_api_key", lambda cfg: "sk-real")
    monkeypatch.setattr(llm, "_claude_cli_path", lambda: "/usr/bin/claude")  # CLI also present
    called = {}

    def fake_sdk(model, s, u, k):
        called["sdk"] = (model, k)
        return "OK"

    def fake_cli(model, s, u):
        called["cli"] = True
        return "NO"

    monkeypatch.setattr(llm, "_anthropic_completion", fake_sdk)
    monkeypatch.setattr(llm, "_claude_cli_completion", fake_cli)
    out = llm._complete("sys", "usr", _cfg(provider="anthropic/claude-sonnet-4-6"))
    assert out == "OK"
    assert "sdk" in called and "cli" not in called


def test_litellm_receives_base_url_when_configured(monkeypatch):
    """OpenAI-compatible provider + base_url -> base_url is passed to litellm."""
    monkeypatch.setattr(llm, "_resolve_api_key", lambda cfg: "sk-real")
    seen = {}

    class FakeMsg:
        content = "OK"

    class FakeChoice:
        message = FakeMsg()

    class FakeResp:
        choices = [FakeChoice()]

    import sys, types
    fake_litellm = types.ModuleType("litellm")
    fake_litellm.completion = lambda **kw: seen.update(kw) or FakeResp()
    monkeypatch.setitem(sys.modules, "litellm", fake_litellm)

    out = llm._complete(
        "sys", "usr",
        _cfg(provider="openai/minimax-m2.7", base_url="https://opencode.ai/zen/v1"),
    )
    assert out == "OK"
    assert seen["base_url"] == "https://opencode.ai/zen/v1"
    assert seen["model"] == "openai/minimax-m2.7"
    assert seen["api_key"] == "sk-real"


def test_litellm_base_url_none_when_unset(monkeypatch):
    """No base_url configured -> pass base_url=None so litellm uses its default."""
    monkeypatch.setattr(llm, "_resolve_api_key", lambda cfg: "sk-real")
    seen = {}

    class FakeMsg:
        content = "OK"

    class FakeChoice:
        message = FakeMsg()

    class FakeResp:
        choices = [FakeChoice()]

    import sys, types
    fake_litellm = types.ModuleType("litellm")
    fake_litellm.completion = lambda **kw: seen.update(kw) or FakeResp()
    monkeypatch.setitem(sys.modules, "litellm", fake_litellm)

    llm._complete("sys", "usr", _cfg(provider="openai/gpt-4o"))  # no base_url
    assert seen["base_url"] is None


def test_base_url_routes_anthropic_provider_through_litellm(monkeypatch):
    """A base_url set on an anthropic/claude provider must route through litellm
    (honoring base_url) rather than the Anthropic SDK (which hardcodes the
    api.anthropic.com endpoint and would silently drop base_url)."""
    monkeypatch.setattr(llm, "_resolve_api_key", lambda cfg: "sk-real")
    seen = {}
    sdk_called = {}

    def fake_sdk(model, s, u, k):
        sdk_called["hit"] = True
        return "SDK"

    monkeypatch.setattr(llm, "_anthropic_completion", fake_sdk)

    class FakeMsg:
        content = "LITELLM"

    class FakeChoice:
        message = FakeMsg()

    class FakeResp:
        choices = [FakeChoice()]

    import sys, types
    fake_litellm = types.ModuleType("litellm")
    fake_litellm.completion = lambda **kw: seen.update(kw) or FakeResp()
    monkeypatch.setitem(sys.modules, "litellm", fake_litellm)

    out = llm._complete(
        "sys", "usr",
        _cfg(provider="anthropic/claude-sonnet-4-6", base_url="https://proxy.example/v1"),
    )
    assert out == "LITELLM"
    assert "hit" not in sdk_called  # Anthropic SDK NOT used
    assert seen["base_url"] == "https://proxy.example/v1"
    assert seen["model"] == "anthropic/claude-sonnet-4-6"


def test_anthropic_provider_without_base_url_uses_sdk(monkeypatch):
    """Regression guard: an anthropic provider with NO base_url still uses the
    Anthropic SDK path (the free/default route), not litellm."""
    monkeypatch.setattr(llm, "_resolve_api_key", lambda cfg: "sk-real")
    used = {}

    def fake_sdk(model, s, u, k):
        used["sdk"] = True
        return "SDK"

    def fake_litellm_completion(**kw):
        used["litellm"] = True
        return None

    monkeypatch.setattr(llm, "_anthropic_completion", fake_sdk)

    import sys, types
    fake_litellm = types.ModuleType("litellm")
    fake_litellm.completion = fake_litellm_completion
    monkeypatch.setitem(sys.modules, "litellm", fake_litellm)

    out = llm._complete("sys", "usr", _cfg(provider="anthropic/claude-sonnet-4-6"))
    assert out == "SDK"
    assert used == {"sdk": True}  # litellm never touched


def test_falls_back_to_cli_when_no_key_and_cli_present(monkeypatch):
    """Anthropic provider + no API key + claude CLI on PATH -> use the CLI."""
    monkeypatch.setattr(llm, "_resolve_api_key", lambda cfg: None)
    monkeypatch.setattr(llm, "_claude_cli_path", lambda: "/usr/bin/claude")
    seen = {}

    def fake_cli(model, s, u):
        seen["cli"] = model
        return "CLI_OUT"

    monkeypatch.setattr(llm, "_claude_cli_completion", fake_cli)
    out = llm._complete("sys", "usr", _cfg(provider="anthropic/claude-sonnet-4-6"))
    assert out == "CLI_OUT"
    assert "cli" in seen


def test_deep_flag_uses_configured_model_cli(monkeypatch):
    """deep=True -> CLI uses the configured (heavier) model; deep=False -> haiku."""
    monkeypatch.setattr(llm, "_resolve_api_key", lambda cfg: None)
    monkeypatch.setattr(llm, "_claude_cli_path", lambda: "/usr/bin/claude")
    models = {}
    monkeypatch.setattr(llm, "_claude_cli_completion", lambda model, s, u: models.setdefault(model, True) or "x")
    cfg = _cfg(provider="anthropic/claude-sonnet-4-6")
    llm._complete("s", "u", cfg, deep=False)
    llm._complete("s", "u", cfg, deep=True)
    assert any("haiku" in m for m in models)      # cheap model for high-volume calls
    assert any("sonnet" in m for m in models)     # configured model for deep prose


def test_no_key_no_cli_raises_so_callers_fall_back(monkeypatch):
    """No key and no CLI -> _complete raises; the public functions catch it and
    return empty (structural-only wiki)."""
    monkeypatch.setattr(llm, "_resolve_api_key", lambda cfg: None)
    monkeypatch.setattr(llm, "_claude_cli_path", lambda: None)
    import pytest
    with pytest.raises(Exception):
        llm._complete("s", "u", _cfg(provider="anthropic/claude-sonnet-4-6"))


def test_describe_nodes_uses_cli_path_end_to_end(monkeypatch):
    """Integration: with no key but CLI present, describe_nodes returns
    descriptions sourced from the CLI."""
    from indexer.ast_parser import ASTNode
    monkeypatch.setattr(llm, "_resolve_api_key", lambda cfg: None)
    monkeypatch.setattr(llm, "_claude_cli_path", lambda: "/usr/bin/claude")
    monkeypatch.setattr(llm, "_claude_cli_completion",
                        lambda model, s, u: '{"a.py::f": "adds two numbers"}')
    n = ASTNode(id="a.py::f", type="function", file="a.py", line_start=1, line_end=2, docstring=None)
    out = llm.describe_nodes([n], _cfg(provider="anthropic/claude-sonnet-4-6"))
    assert out["a.py::f"] == "adds two numbers"


# ── CLI invocation mechanics ──────────────────────────────────────────────────

def test_claude_cli_completion_invokes_print_mode(monkeypatch):
    """_claude_cli_completion calls `claude -p --system-prompt ... --model ...`
    with the user text on stdin, and returns stdout."""
    calls = {}

    class FakeProc:
        returncode = 0
        stdout = "RESULT"
        stderr = ""

    def fake_run(cmd, **kw):
        calls["cmd"] = cmd
        calls["input"] = kw.get("input")
        return FakeProc()

    monkeypatch.setattr(llm, "_claude_cli_path", lambda: "/usr/bin/claude")
    monkeypatch.setattr(llm.subprocess, "run", fake_run)
    out = llm._claude_cli_completion("claude-haiku-4-5", "SYS", "USR")
    assert out == "RESULT"
    assert "/usr/bin/claude" in calls["cmd"]
    assert "-p" in calls["cmd"]
    # system prompt is passed (with a terse-output instruction appended)
    assert any(arg.startswith("SYS") for arg in calls["cmd"])
    assert "claude-haiku-4-5" in calls["cmd"]
    assert calls["input"] == "USR"          # user text on stdin


def test_claude_cli_completion_raises_on_nonzero(monkeypatch):
    class FakeProc:
        returncode = 1
        stdout = ""
        stderr = "boom"
    monkeypatch.setattr(llm, "_claude_cli_path", lambda: "/usr/bin/claude")
    monkeypatch.setattr(llm.subprocess, "run", lambda cmd, **kw: FakeProc())
    import pytest
    with pytest.raises(Exception):
        llm._claude_cli_completion("m", "s", "u")


# ── _clean_json robustness (CLI returns preamble + fences) ────────────────────

def test_clean_json_plain():
    assert llm._clean_json('{"a": 1}') == {"a": 1}


def test_clean_json_fenced():
    assert llm._clean_json('```json\n{"a": 1}\n```') == {"a": 1}


def test_clean_json_preamble_then_fence():
    raw = 'Here is the requested JSON:\n\n```json\n{"overview": "x", "flows": []}\n```'
    assert llm._clean_json(raw) == {"overview": "x", "flows": []}


def test_clean_json_preamble_then_bare_object():
    raw = "The path doesn't exist but here you go: {\"k\": [1, 2]} thanks!"
    assert llm._clean_json(raw) == {"k": [1, 2]}


def test_clean_json_list_payload():
    raw = "ok:\n[{\"id\": \"a\"}]"
    assert llm._clean_json(raw) == [{"id": "a"}]


def test_clean_json_raises_on_garbage():
    import pytest
    with pytest.raises(Exception):
        llm._clean_json("no json here at all")
