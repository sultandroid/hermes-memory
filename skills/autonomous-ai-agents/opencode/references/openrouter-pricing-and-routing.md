# OpenRouter Pricing & Routing Reference

> Verified from OpenRouter API (`/api/v1/models`) — June 2026

## DeepSeek V4 Flash — Official Pricing

| Component | Per Token | Per 1M Tokens |
|-----------|:---------:|:-------------:|
| **Input (prompt)** | $0.00000009 | **$0.09** |
| **Output (completion)** | $0.00000018 | **$0.18** |
| **Input Cache Read** | $0.00000002 | **$0.02** |
| Context window | — | 1,048,576 (1M) |
| Max output | — | 65,536 |

## Other Relevant Models on OpenRouter

| Model | Input/1M | Output/1M | Cache/1M |
|-------|:--------:|:---------:|:--------:|
| DeepSeek V4 Pro | $0.44 | $0.87 | $0.?? |
| Qwen 3.7 Plus | $0.32 | $1.28 | yes |
| Qwen 3.7 Max | $1.25 | $3.75 | yes |
| Claude Sonnet 4 | $3.00 | $15.00 | yes |
| Claude Haiku 4.5 | $1.00 | $5.00 | yes |
| Gemini 3.5 Flash | $1.50 | $9.00 | yes |
| GPT-5.5 | $5.00 | $30.00 | yes |

## Auto-Routing Features & Cost Impact

| Feature | Default? | Cost Impact |
|---------|:--------:|:-----------:|
| **Price-Based Load Balancing** | ✅ Yes | **Saves 5-10%** — routes to cheapest provider for same model |
| **Model Fallbacks** (`models` param) | ❌ Manual config | **Saves only if primary is unavailable** — pays for fallback model used |
| **Auto Exacto** (tool-calling) | ✅ Yes | **May increase cost** — prioritizes quality over price for tool-calling. Disable via `provider.sort = "price"` |

### Price-Based Load Balancing (Default — saves money automatically)

When a model is served by multiple providers, OpenRouter's default strategy distributes requests with a strong preference for the lowest-cost provider. No configuration needed.

### Model Fallbacks (Manual — saves on failover)

Pass `models: ['primary', 'fallback1', 'fallback2']` in the API body. If the primary fails (rate-limit, downtime, mod refusal), OpenRouter tries the next. You're charged only for the model that actually responded.

### Auto Exacto (Tool-calling optimization — disable for savings)

Automatically active for ALL requests that include `tools`. Reorders providers by throughput + tool-calling success rate instead of price. To restore price-based ordering:

```python
extra_body = {
    "provider": {"sort": "price"}
}
```

## How to Verify Pricing Programmatically

```bash
# Get pricing for a specific model
curl -s https://openrouter.ai/api/v1/models | python3 -c "
import json, sys
data = json.load(sys.stdin)
for m in data['data']:
    if 'deepseek' in m['id'] and 'flash' in m['id']:
        p = m['pricing']
        print(f\"Input:  {float(p.get('prompt',0))*1e6:.4f}/1M\")
        print(f\"Output: {float(p.get('completion',0))*1e6:.4f}/1M\")
        print(f\"Cache:  {float(p.get('input_cache_read',0))*1e6:.4f}/1M\")
        break
"
```

## Cost Comparison Methodology

When comparing OpenCode Go (subscription) vs OpenRouter (PAYG):

1. **Get actual usage** from `opencode stats` (input, output, cache tokens over N days)
2. **Project OpenRouter cost**:
   - Input × 0.09/1M + Output × 0.18/1M + Cache Read × 0.02/1M
   - Add 5% platform fee (after free tier)
   - Multiply to monthly equivalent
3. **Compare vs OpenCode Go**:
   - $10/month subscription + overages (look at actual total / days × 30)
   - If actual cost > projected OpenRouter cost by 30%+, switching saves

**Key insight:** Cache-heavy workloads (typical for coding agents with large system prompts) benefit disproportionately from OpenRouter's $0.02/1M cache rate versus OpenCode Go's bundled pricing. When cache reads dominate token volume, PAUG almost always wins.

## OpenRouter Plans at a Glance

| | Free | PAYG | Enterprise |
|---|:----:|:----:|:----------:|
| Min spend | $0 | $10 prepaid | Custom |
| Rate limits | 50 req/day, 20 RPM | No limits (≥$10 credits) | Custom |
| Free requests/mo | — | 1M | 5M |
| Platform fee | — | 5% (after free tier) | Custom |
