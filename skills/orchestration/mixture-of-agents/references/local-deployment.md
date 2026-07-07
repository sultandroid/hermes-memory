# Local MoA Deployment (Ollama)

## Why local

- **No API costs** — unlimited queries after the one-time model download
- **Privacy** — prompts never leave the machine
- **Offline** — works without internet

## Why not local

- **Hardware required** — at least 16GB RAM for a 4-model MoA
- **Slower than cloud** for small flash models on Apple Silicon M-series
- **Model quality ceiling** — best open-weights still trails Claude/GPT-4o
- **Setup time** — install + download 10+ GB of models

## Recommended stack

| Role | Model | RAM | Notes |
|------|-------|-----|-------|
| Aggregator + complex | `qwen2.5:7b` | ~5 GB | Strong synthesis, 32K ctx |
| Flash #1 | `qwen2.5:3b` | ~2.5 GB | Qwen family |
| Flash #2 | `llama3.2:3b` | ~2.5 GB | Meta family = diversity |
| Flash #3 | `gemma2:2b` | ~1.5 GB | Google family = more diversity |
| Router | `gemma2:2b` | ~1.5 GB | Smallest, sub-second |

Total loaded: ~15 GB. 48GB M-series = comfortable. 16GB = tight, expect swap. 8GB = drop to 2 models.

## Setup

```bash
# macOS
brew install ollama
brew services start ollama

# Apple Silicon perf flags (set in env before starting)
export OLLAMA_FLASH_ATTENTION=1
export OLLAMA_KV_CACHE_TYPE=q8_0
brew services start ollama

# Pull models (can be parallelized in separate terminals)
ollama pull qwen2.5:7b       # 4.7 GB
ollama pull qwen2.5:3b       # 1.9 GB
ollama pull llama3.2:3b      # 2.0 GB
ollama pull gemma2:2b        # 1.6 GB

# Run
cd ~/moa
python moa.py "What is the capital of France?"
```

## Ollama quirks

- **First model load is slow.** Subsequent calls reuse the loaded model in
  memory. Cold-start of a 7B model = 5-10s.
- **Concurrent requests to same model** = serialized inference. MoA's
  parallel proposer pattern works because each proposer uses a DIFFERENT model.
  If two proposers use the same model, they queue.
- **`num_ctx` matters.** Default 2048 truncates long context. Set to 8192+
  for aggregator input that concatenates 3 proposer responses.
- **Apple Silicon Metal** is auto-detected. CUDA requires manual setup on Linux.
- **Model storage** at `~/.ollama/models/` (~10 GB for the recommended stack).

## Hardware sizing

| Machine | Recommended stack | Notes |
|---------|-------------------|-------|
| M4 Pro / M3 Pro 48GB | Full 4-model MoA | All models loaded simultaneously |
| M2 / M3 16GB | Drop one flash, use 3 models | 7B aggregator + 2 flash |
| M1 8GB | 2 models only, expect swap | 7B aggregator + 1 flash, slow |
| Linux + RTX 4090 24GB | Full 4-model + larger | 13B/70B aggregator possible |
| Linux + RTX 3060 12GB | 3 models | 7B + 2 flash, no 70B |
| CPU-only | Not recommended | Multi-second per token, MoA will be very slow |

## Pitfalls

- **Pulling models takes 5-10 min for 7B.** Plan accordingly. Pull in parallel
  terminals to save wall time.
- **Disk space.** Each model = 2-5 GB. Full stack = ~10 GB.
- **Ollama holds models in RAM, not VRAM.** Even on Apple Silicon with unified
  memory, the model is "claimed" until you stop the server or unload it.
- **No built-in batching.** 3 parallel proposers = 3 separate inference
  passes, not one batched call. Latency stacks, not amortizes.
- **Stop the service when not in use** to free RAM:
  `brew services stop ollama`
