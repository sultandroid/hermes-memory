# Codex OAuth gpt-5.5 context cap

Session date: 2026-06-24

## What was verified

User switched Hermes default to:

```yaml
model:
  default: gpt-5.5
  provider: openai-codex
```

Runtime/source checks showed:

```text
get_model_context_length('gpt-5.5', provider='openai-codex') -> 272000
get_model_context_length('gpt-5.5', provider='openrouter')    -> 1050000
get_model_context_length('gpt-5.5', provider='openai')        -> 1050000
```

Hermes source comments also state that provider-aware context resolution is intentional because Codex OAuth, Copilot, and other provider routes can enforce caps that differ from raw model metadata.

Relevant source areas found in the local Hermes repo:

- `cli.py`: display comments note `gpt-5.5 is 1.05M on openai but 272K on Codex OAuth`.
- `hermes_cli/config.py`: `compression.codex_gpt55_autoraise` comment says Codex hard-caps gpt-5.5 at a 272K window.
- `agent/model_metadata.py`: base fallback lists `gpt-5.5: 1050000`, while `_CODEX_OAUTH_CONTEXT_FALLBACK` lists `gpt-5.5: 272_000`.

## Interpretation

The 272K value is an effective cap of the ChatGPT/Codex OAuth provider path, not proof that the underlying gpt-5.5 model has only 272K context everywhere.

Likely reasons include product entitlement, subscription-style cost control, latency/reliability of interactive Codex sessions, abuse/rate-limit protection, and backend-routing differences. Avoid presenting these as confirmed vendor policy unless verified from official docs.

## How to answer future users

Say:

> For your current route, `openai-codex + gpt-5.5`, Hermes resolves 272K tokens. The same slug can resolve around 1.05M through other provider routes such as direct OpenAI/OpenRouter, so the cap is provider-route-specific.

Avoid:

> gpt-5.5 is only 272K.

## Verification snippet

From the Hermes repo:

```bash
cd ~/.hermes/hermes-agent
python3 - <<'PY'
from agent.model_metadata import get_model_context_length
for provider in ['openai-codex','openrouter','openai']:
    print(provider, get_model_context_length('gpt-5.5', provider=provider, base_url='', api_key=''))
PY
```
