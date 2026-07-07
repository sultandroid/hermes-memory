---
name: model-routing
description: "Use when you need to pick the optimal model from ollama-cloud (34 models) based on task type. Auto-detect task from prompt signals and route to the best model."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [models, routing, performance, ollama-cloud]
    related_skills: [hermes-model-provider-troubleshooting, hermes-performance-audits, labor-clis]
    created_by: agent
---

# Model Routing — ollama-cloud (34 models)

## Overview

ollama-cloud at `https://ollama.com/v1` serves 34 models across 8 families. This skill defines routing rules so you always use the best model for the task — not just the default `deepseek-v4-flash`.

## When to Use

- Load when the default model (`deepseek-v4-flash`) isn't optimal for the current task — e.g. heavy analysis, code generation, or structured output.
- Load when you want to pick a model explicitly for a sub-task.
- Re-evaluate when new models appear on ollama-cloud (check with `curl -s https://ollama.com/v1/models`).
- **Don't use for:** trivial queries where flash is fine. The routing overhead isn't worth it.

## Routing Table

### Detection priority: check signals in order, first match wins.

| Signal keywords / tool patterns | Route to | Context | Why |
|---|---|---|---|---|
| `web_search`, `read_file`, `search_files`, quick lookup, "check", "find", "list" | **deepseek-v4-flash** | ~128K | Fastest, lowest latency. Default for 90% of work. |
| `execute_code`, code gen, debug, refactor, "write a script", "implement", "fix bug" | **kimi-k2.7-code** (quick edits, scripts) or **qwen3-coder:480b** (complex multi-file refactors) | ~128K / ~128K | Code-specialized > general models. kimi-k2.7-code for speed, qwen3-coder:480b for depth. |
| "analyze", "review", "audit", "generate doc", "create report", Odoo writes, complex reasoning | **deepseek-v4-pro** | ~128K | Deeper reasoning than flash. Proven for analysis. |
| "contract", "legal", "specification", "complex logic", "deep research", hardest problems | **deepseek-v3.1:671b** or **deepseek-v3.2** or **mistral-large-3:675b** | ~128K / ~128K / ~128K | 671B/675B — best reasoning on the platform. v3.2 is newer than v3.1. |
| JSON output, structured data, classification, format conversion | **ministral-3:3b** or **ministral-3:8b** | ~32K / ~32K | Small, fast, format-reliable. |
| Creative writing, summarization, rewrite, tone adjustment | **gemma4:31b** or **minimax-m3** | ~8K / ~128K | Best creative quality among available. |
| Code review, PR audit, security review | **qwen3.5:397b** | ~128K | Strong analytical reasoning for code quality. |
| Fast alternative when flash is slow | **gemini-3-flash-preview** (Google) | ~1M+ | Google's fast model — try if flash lags. Note: different API characteristics, rate limits, pricing. |

### Full model catalog (ollama-cloud, 34 models)

**DeepSeek family**
| Model | Size | Role |
|---|---|---|
| deepseek-v4-flash | ~236B MoE | ⭐ DEFAULT — fast daily driver |
| deepseek-v4-pro | ~685B MoE | ⭐⭐⭐ Heavy analysis, docs, reasoning |
| deepseek-v3.1:671b | 671B | ⭐⭐⭐ Hardest problems |
| deepseek-v3.2 | ~685B | ⭐⭐⭐ Newer than v3.1. Comparable reasoning. |

**Kimi (Moonshot AI)**
| Model | Size | Role |
|---|---|---|
| kimi-k2.5 | ? | ⭐⭐ General alternative to pro |
| kimi-k2.6 | ? | ⭐⭐ Newer k2.5 |
| kimi-k2.7-code | ? | ⭐⭐⭐ **Code-specialized** |

**GLM (Zhipu AI)**
| Model | Size | Role |
|---|---|---|
| glm-5 | ? | ⭐⭐ Mid-weight all-rounder |
| glm-4.7 | ? | ⭐ Skip — older |
| glm-5.1 | ? | ⭐⭐ Incremental over glm-5 |
| glm-5.2 | ? | ⭐⭐ Latest GLM |

**Gemma (Google)**
| Model | Size | Role |
|---|---|---|
| gemma3:4b | 4B | ⭐ Too small for real work |
| gemma3:12b | 12B | ⭐⭐ Lightweight general |
| gemma3:27b | 27B | ⭐⭐ Mid-weight option |
| gemma4:31b | 31B | ⭐⭐⭐ Newest, best Gemma |

**Qwen (Alibaba)**
| Model | Size | Role |
|---|---|---|
| qwen3-coder:480b | 480B | ⭐⭐⭐ **Best coding model** |
| qwen3-coder-next | ? | ⭐⭐⭐ Newer coder |
| qwen3.5:397b | 397B | ⭐⭐⭐ Strong general reasoning |

**Mistral**
| Model | Size | Role |
|---|---|---|
| ministral-3:3b | 3B | ⭐ Tiny — JSON/classification only |
| ministral-3:8b | 8B | ⭐⭐ Structured output |
| ministral-3:14b | 14B | ⭐⭐ Better reasoning than 8b |
| mistral-large-3:675b | 675B | ⭐⭐⭐ Top-tier reasoning |
| devstral-small-2:24b | 24B | ⭐⭐ Mid-weight |
| devstral-2:123b | 123B | ⭐⭐⭐ Strong reasoning |

**MiniMax**
| Model | Size | Role |
|---|---|---|
| minimax-m2.1 | ? | ⭐⭐ Decent all-rounder |
| minimax-m2.5 | ? | ⭐⭐ Better than m2.1 |
| minimax-m2.7 | ? | ⭐⭐ Latest m2 |
| minimax-m3 | ~456B | ⭐⭐⭐ Newest flagship |

**Nemotron (NVIDIA)**
| Model | Size | Role |
|---|---|---|
| nemotron-3-super | ? | ⭐⭐ Mid-weight |
| nemotron-3-ultra | ? | ⭐⭐⭐ NVIDIA's best |
| nemotron-3-nano:30b | 30B | ⭐⭐ Smallest |

**Google**
| Model | Size | Role |
|---|---|---|
| gemini-3-flash-preview | ? | ⭐⭐⭐ Fast alternative to flash. ~1M+ context. Different API characteristics/rate limits. |

**Others (open-source GPT clones)**

## How to Route (3 strategies)

### Step 0: Check current model/provider
```bash
hermes config | grep -E 'model|provider'
```
Or use the interactive picker: `hermes model`

### Strategy A: One-shot sub-task on a different model (recommended for single tasks)
```bash
hermes -z -m <model> "<task>"
```
Use for isolated sub-tasks that don't need the full conversation context. Does NOT change your session's model.

### Strategy B: New session with a different model
```bash
hermes -m <model>
```
Starts a fresh session with the chosen model. Your config stays unchanged.

### Strategy C: Change default model (persistent)
```bash
hermes config set provider ollama-cloud   # only if on a different provider
hermes config set model <model-name>
```
Then run `/new` to start a fresh session with the new default. This mutates your config — use sparingly.

## Common Pitfalls

1. **Can't change model mid-session.** The model is set at session start. Use Strategy A (`-m` flag) or B (new session) for model switching.
2. **Big models are slow.** deepseek-v3.1:671b, deepseek-v3.2, and mistral-large-3:675b have high latency. Only use for tasks that genuinely need that reasoning depth.
3. **Model availability changes.** ollama-cloud adds/removes models. Refresh the list periodically with `curl -s https://ollama.com/v1/models`.
4. **Code models for non-code tasks.** kimi-k2.7-code and qwen3-coder:480b are specialized — don't use them for general chat or analysis.
5. **Ministral for complex reasoning.** 3B and 8B models lack depth. Don't route analysis or code to them.
6. **Model not found / doesn't exist.** If `hermes -m <model>` fails, the model name may be wrong or temporarily unavailable. Check with `curl -s https://ollama.com/v1/models | python3 -c "import json,sys; [print(m['id']) for m in json.load(sys.stdin)['data']]"`.
7. **Provider mismatch.** If you're on a different provider (e.g. openai-codex), `hermes config set model` won't work without also setting the provider. Use `hermes -m` (auto-resolves) or `hermes config set provider ollama-cloud` first.

## Verification Checklist

- [ ] Task type detected from prompt keywords + tool usage
- [ ] Model selected from routing table (first signal match)
- [ ] If current model != optimal: use `hermes -m <model>` for a new session, or `hermes -z -m <model> "<task>"` for a one-shot
- [ ] Verify model responds: `hermes -z -m <model> "hello"` (quick smoke test)
- [ ] Big models (671B/675B) only used for genuinely hard problems
- [ ] Code models only for code tasks
- [ ] Provider mismatch checked: `hermes config | grep -E 'model|provider'`
