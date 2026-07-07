# Cloud MoA Deployment

## Provider comparison

| Provider | Pros | Cons | Free tier | Best for |
|----------|------|------|-----------|----------|
| **OpenRouter** | One key, all models, OpenAI-compatible | Markup over direct | None (pay-as-you-go from $0.0001/tok) | Fastest start, multi-model access |
| **Groq** | Ultra-fast inference (LPU), generous free | Limited model set, 1-3 req/s | Yes (Llama 3.x, Mixtral) | Free + fast experimentation |
| **OpenAI** | Best-in-class GPT-4o, reliable | Expensive, key-only access | None | When GPT-4o quality needed |
| **Anthropic** | Claude 3.5 Sonnet strong for synthesis | No free tier, key-only | None | Top-quality aggregator |
| **Together** | Open-source models, OpenAI-compatible | Less reliable uptime | $5 credit on signup | Open-weights via API |
| **Google Gemini** | Flash tier cheap, 1M ctx | Region restrictions, free tier limited | Yes (Flash 1.5) | Long-context queries |

## Recommended starter stack (OpenRouter)

| Role | Model | Cost / 1M tok | Notes |
|------|-------|---------------|-------|
| Aggregator | `qwen/qwen-2.5-72b-instruct` | ~$0.30 | Strong synthesis |
| Complex proposer | same as aggregator | ~$0.30 | Quality ceiling |
| Flash #1 | `qwen/qwen-2.5-7b-instruct` | ~$0.02 | Open-weights family |
| Flash #2 | `meta-llama/llama-3.1-8b-instruct` | ~$0.02 | Different family = diversity |
| Flash #3 | `google/gemini-flash-1.5` | ~$0.02 | Third family |
| Router | `google/gemini-flash-1.5` | ~$0.02 | Sub-second |

Estimated per query: $0.01-0.05 (3-4 proposers + aggregator + router).

## Free-tier stack (Groq + Gemini)

| Role | Provider | Model | Limit |
|------|----------|-------|-------|
| Aggregator | Groq | `llama-3.1-70b-versatile` | 30 req/min |
| Complex proposer | Groq | `llama-3.1-70b-versatile` | 30 req/min |
| Flash #1 | Groq | `llama-3.1-8b-instant` | 30 req/min |
| Flash #2 | Groq | `mixtral-8x7b-32768` | 30 req/min |
| Flash #3 | Google | `gemini-1.5-flash` | 15 req/min |
| Router | Groq | `llama-3.1-8b-instant` | 30 req/min |

## Setup

```bash
# OpenRouter (easiest, one key)
export OPENROUTER_API_KEY=sk-or-v1-...
export MOA_BASE_URL=https://openrouter.ai/api/v1
python moa-cloud.py "Your question"

# Groq (free)
export GROQ_API_KEY=gsk_...
python moa-cloud.py --provider groq "Your question"

# Multi-provider — pass --provider per call, or set MOA_BASE_URL to override
```

## API quirks

- **OpenRouter** charges both input and output tokens. Aggregator prompts can
  be long (3 proposer responses × ~500 tokens each = 1500+ input tokens per
  synthesis). Budget $0.05-0.10 per complex query.
- **Groq** enforces token-per-minute limits, not just request rate. A burst of
  large prompts can hit the cap.
- **Gemini** rate limits vary by region and are stricter on the free tier.
  Add exponential backoff (built into `moa-cloud.py`).
- **OpenAI** has tier-based rate limits (free tier = 3 req/min, Tier 1 = 500).
- **All providers** reject prompts > their context window. Cap proposer input
  at 8K tokens to stay safe across providers.

## Pitfalls

- **No fallback to local on cloud failure.** The cloud version errors out if
  the API is down. If you need resilience, add a try/except that calls Ollama
  as fallback (combine `moa.py` and `moa-cloud.py` into one).
- **Cost surprise on long contexts.** Aggregator input = proposer outputs.
  Three 2000-token proposers = 6000+ input tokens per query.
- **Key leakage in logs.** `httpx` doesn't log request bodies by default, but
  custom logging might. Never log the full request.
- **Different prompt formats.** OpenRouter/Groq/OpenAI use OpenAI format.
  Anthropic uses a different format (separate `/v1/messages` endpoint with
  `system` as a top-level field, not a message). `moa-cloud.py` is
  OpenAI-compatible only — add an Anthropic adapter if needed.

## Custom / private providers

A provider name like `ollama-cloud` in Hermes config may be a **custom/private provider**, not a public API. Never assume the base URL or API key. Always ask the user before configuring anything.

**Procedure when encountering an unknown provider name:**
1. Ask: "What is the base URL and API key for this provider?"
2. Do not proceed with guesses or assumptions.
3. If the user says "remove it," do not suggest a replacement — just delete the config.

See `references/custom-provider-pitfalls.md` for the full case study.

## Ollama Cloud specifics

- Provider slug in Hermes: `ollama-cloud`.
- Live model catalog: `https://ollama.com/v1/models`.
- Model IDs change over time; use the live endpoint rather than guessing.
- When editing Hermes native MoA presets for Ollama Cloud, do **not** use
  `hermes config set` for list-valued fields — it stringifies them. Use the
  structured YAML recipe in `references/hermes-moa-presets.md`.