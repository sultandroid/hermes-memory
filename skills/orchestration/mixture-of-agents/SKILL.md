---
name: mixture-of-agents
description: "Design Mixture-of-Agents (MoA) LLM pipelines — model selection, tiered routing, local vs cloud deployment. Load when user mentions MoA, multi-model orchestration, or building an LLM pipeline with proposer/aggregator roles."
---

# Mixture-of-Agents (MoA) Pipeline Design

Class-level skill for designing, configuring, and deploying MoA pipelines —
multiple LLM "proposers" generate responses in parallel and an "aggregator"
synthesizes them into one final answer.

## ⚠️ FIRST STEP: Clarify deployment target

Before installing anything, pulling models, or writing orchestrator code, ask the user:

> "Do you want this running **locally** (Ollama/llama.cpp/LM Studio) or via **cloud APIs** (OpenRouter, Groq, OpenAI, Anthropic, Gemini)? Do you have API keys already, or do you want to set those up?"

**Why this matters:** A full local setup (Ollama install, multi-GB model pulls, Python orchestrator) can consume 10+ minutes and several GB of disk before the user clarifies they wanted cloud APIs. The user already corrected this — never repeat the wasted setup.

**Do not assume from keywords.** "Cheap" and "fast" do NOT imply local. Cloud flash models (Gemini Flash, Groq-hosted Llama) are often cheaper and faster than local inference on modest hardware. Clarify regardless.

**User preference: remove, don't replace** — When the user says "remove provider X" or "I didn't use anymore," do NOT suggest a replacement. Ask: "Disable the feature, delete the config, or switch to something else?" Do not force a migration path. This user has corrected this twice — they want removal, not migration.

**Custom provider names are not standard** — A provider name like `ollama-cloud` in Hermes config may be a custom/private provider, not the public ollama.com API. Never assume the base URL or API key. Always ask: "What is the base URL and API key for this provider?" before configuring anything against it.

## Core architecture

```
User Query
    │
    ▼
[Heuristic gate] ── short-circuit obvious simple prompts (≤4 words, factual lookups)
    │  (skips LLM router when confident)
    ▼
[Router] ── classifies: simple | complex
    │  (fires in parallel with first batch of proposers — see Speed below)
    │
    ├── simple ──► 4x flash proposers (parallel) ──► [Aggregator] ──► Final answer
    │
    └── complex ─► 6x proposers: 1x strong + 2x mid + 2x flash + 1x specialist ──► [Aggregator] ──► Final answer
```

### Key principles

1. **Aggregator = quality ceiling.** Never put a weak model at the aggregator
   role. The aggregator must comprehend, filter, and synthesize — a 2B model
   here drags the entire pipeline down regardless of proposer strength.
2. **Proposer diversity > proposer strength.** Three identical strong models
   converge on the same answer. Better to have 3 different model families at
   smaller sizes than 3 copies of one large model. Diversity catches blind spots.
   **Default to 4-6 proposers spanning at least 3 model families.** The user
   has explicitly pushed back on 3-proposer configs — they want 4-6 for
   cross-family coverage (e.g. Qwen + Llama + Gemini + DeepSeek).
3. **Tiered routing saves cost.** Simple queries (greetings, definitions,
   lookups) don't need the strong model. Route to flash-only proposers. Complex
   queries (code, analysis, ambiguity) get one strong proposer + mid-tier + flash + specialist.
4. **DeepSeek is part of the standard stack.** Include `deepseek-chat` as a
   general-purpose proposer and `deepseek-coder` for code-heavy tasks. They
   bring different reasoning patterns than Qwen/Llama/Gemini.
5. **Flash models hallucinate.** The aggregator must filter, not blindly merge.
   Instruct it to prefer the most specific/factual response and drop
   unsubstantiated claims.

## Speed optimizations (the user notices latency)

The user is latency-sensitive. A naive sequential router → proposers →
aggregator pipeline takes 20+ seconds. The optimizations below cut that to
under 10s on complex queries and under 3s on simple.

1. **Heuristic gate.** Before calling the LLM router, run a regex-based check
   for obvious simple prompts (≤4 words, "what is X", "define X", "hi/hello").
   Skip the router entirely when confident. Adds 0ms.
2. **Speculative kickoff.** Fire the first 3 fast proposers in parallel with
   the LLM router. When the router returns, conditionally fire the remaining
   slow/strong proposers (e.g. qwen-72b, deepseek-coder). Saves 2-3s on
   complex queries. Cost: 3 extra flash calls on simple queries (negligible).
3. **Streaming aggregator.** Stream the aggregator's response token-by-token
   to stdout so the user sees the first token within 0.3-1s, not the full
   response. **Implementation gotcha:** with httpx, streaming requires
   `client.stream("POST", url, ...)` as a context manager, not `client.post()`.
   The latter buffers the entire response and defeats the purpose.
4. **Per-tier `max_tokens`.** Cap at 1024 for simple, 2048 for complex, 4096
   for aggregator. A blanket 4096 wastes latency on short responses.
5. **Pre-warm.** On first call, hit each model with a trivial prompt to load
   it. Subsequent calls have no cold-start. Add a `--warmup` flag.

## Latency-Constrained MoA Design

When the user specifies a maximum acceptable latency (e.g. "no refs slower than
Gemini Flash"), follow these rules:

- **The slowest proposer determines total latency.** MoA fires all references
  in parallel and waits for every one to finish before the aggregator runs.
  Total turn latency = `max(proposer_latencies) + aggregator_latency`. A
  single slow model (e.g. 397B) in an otherwise flash set still makes the
  whole pipeline slow.
- **Reference models must all be ≤ the user's latency ceiling.** If the user
  says "slowest acceptable ref is Gemini Flash", every reference model must
  have latency ≤ Gemini Flash. No exceptions — a strong model in the
  reference phase is a bottleneck.
- **Aggregator must be faster than the slowest ref.** Otherwise the
  aggregator becomes the bottleneck. Use a flash model as aggregator when
  speed is the priority.
- **Do not mix latency tiers in one preset.** A preset with `deepseek-v4-pro`
  (slow, strong) and `gemini-3-flash-preview` (fast) provides the quality of
  a mixture but the latency of the slowest member. Instead, create separate
  presets:
  - `ollama-fast`: all flash refs + flash aggregator (for speed)
  - `ollama-strong`: strong refs + strong aggregator (for heavy tasks)
  - Let the user switch via model picker or `/moa` preset name.
- **User-specific: DeepSeek required.** This user requires at least one
  DeepSeek model in the pipeline. Include `deepseek-v4-flash` or
  `deepseek-v4-pro` in references or aggregator.
- **User-specific: 4-6 proposers.** This user has pushed back on 3-proposer
  configs. Default to 4-6 references spanning 3+ model families.

### Known fast model IDs (Ollama Cloud, verified)

These models all have latency ≤ Gemini Flash and are safe to use together in a
speed-optimized preset:

- `deepseek-v4-flash`
- `gemini-3-flash-preview`
- `ministral-3:8b`
- `gemma3:12b`
- `kimi-k2.7-code`
- `glm-5.2`

Stronger but slower models (use in a separate `ollama-strong` preset):
- `deepseek-v4-pro`
- `gemma4:31b`
- `qwen3.5:397b`

### Pitfall: mixing strong and flash in one preset

> If you include a strong model (e.g. `deepseek-v4-pro`) in references but use
> a fast aggregator (e.g. `deepseek-v4-flash`), the MoA pipeline still waits
> for the slowest ref to finish. This violates the user's latency constraint.
> The only way to have both speed and strength is two separate presets the
> user switches between.

## Deployment paths

After the user confirms target, follow the matching path:

### Cloud (default recommendation — simpler, faster start)

See `references/cloud-deployment.md` for full details.

| Role | OpenRouter model | Cost / 1M tok | Notes |
|------|------------------|---------------|-------|
| Aggregator | `qwen/qwen-2.5-72b-instruct` | ~$0.30 | Strong synthesis, 32K ctx |
| Complex proposer (strong) | `qwen/qwen-2.5-72b-instruct` | ~$0.30 | Quality ceiling |
| Mid-tier proposers (x2) | `qwen/qwen-2.5-7b-instruct`, `deepseek/deepseek-chat` | ~$0.02-0.10 | Reasoning + alt angle |
| Flash proposers (x2) | `google/gemini-2.0-flash-exp:free`, `meta-llama/llama-3.1-8b-instruct` | ~$0.02-0.10 | Speed + diversity |
| Code specialist | `deepseek/deepseek-coder` | ~$0.10 | Code-heavy tasks |
| Router | `google/gemini-2.0-flash-exp:free` | free | Sub-second classification |

Per-query cost: simple ~$0.001-0.005, complex ~$0.05-0.10.

One API key, one base URL (`https://openrouter.ai/api/v1`), all providers. Use `templates/moa-cloud.py` + `templates/config-cloud.yaml`.

Free-tier alternative: Groq (Llama 3.x) + Google Gemini free. $0 cost, rate-limited, slower throughput.

### Local (Ollama)

See `references/local-deployment.md` for full details.

| Role | Model | RAM |
|------|-------|-----|
| Aggregator + complex proposer | `qwen2.5:7b` or `llama3.1:8b` | ~5-6 GB |
| Flash proposers | `qwen2.5:3b`, `llama3.2:3b`, `gemma2:2b` | ~2-3 GB each |
| Router | any flash (e.g. `gemma2:2b`) | ~1.5 GB |

Total ~15-18 GB RAM if all loaded simultaneously. 48GB M-series: trivial. 8GB machines: stick to 2-3 models, expect swap.

Use `templates/moa.py` + `templates/config.yaml`.

## Templates

- `templates/moa.py` — Python async orchestrator over Ollama HTTP API (local)
- `templates/config.yaml` — Tiered config for local MoA
- `templates/moa-cloud.py` — Python async orchestrator for OpenRouter/Groq/Gemini (cloud)
- `templates/config-cloud.yaml` — Tiered config for cloud MoA
- `templates/bench.py` — Smoke test + latency benchmark

## Pitfalls

- **Assuming local when user wants cloud** — Always ask first. The full install+pull cycle in the originating session was wasted.
- **Weak aggregator** — Never put a 2B model at aggregator. It cannot synthesize.
- **Too few proposers** — 3 models with same family = 1 model with extra steps. Default 4-6 across 3+ families (Qwen + Llama + Gemini + DeepSeek is the standard spread).
- **No diversity** — same model repeated = convergence on one answer. Use different families.
- **Sequential pipeline** — router → wait → proposers → wait → aggregator wastes 3-6s. Use heuristic gate + speculative kickoff + streaming aggregator. See "Speed optimizations" above.
- **Blind merging** — Aggregator must be instructed to filter and resolve conflicts, not concatenate.
- **Backup deletion before verification** — Never delete the backup of a working config until the new setup is confirmed operational. In the originating session, `config.yaml.bak` was deleted before the ollama-cloud provider was verified, leaving no rollback path.
- **Cloud API key leakage** — Never hardcode keys. Use env vars (`OPENROUTER_API_KEY`, `GROQ_API_KEY`, `GEMINI_API_KEY`).
- **Cloud rate limits** — Free tiers (Groq, Gemini) cap at 1-3 req/sec. Add exponential backoff.
- **Context truncation** — Cloud models have lower ctx than local. Cap proposer input or chunk long queries.
- **Ollama perf flags** — If running local, set `OLLAMA_FLASH_ATTENTION=1 OLLAMA_KV_CACHE_TYPE=q8_0` for Apple Silicon throughput.

## See also

- `references/cloud-deployment.md` — provider comparison, API quirks, rate limits, Ollama Cloud specifics
- `references/local-deployment.md` — Ollama install, model pulls, hardware sizing
- `references/hermes-moa-presets.md` — editing Hermes native MoA presets without stringifying YAML lists