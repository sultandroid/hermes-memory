# LM Studio local provider — working config (M4 Pro, 48 GB)

Session-derived setup that succeeded on this machine (2026-09-04).

## Environment
- MacBook Pro, Apple M4 Pro, 48 GB unified RAM, macOS 26.5.2
- Internal disk nearly full (~18 GB free); external drive `MIcro` (`/Volumes/MIcro`) has ~105 GB free
- LM Studio running, exposing OpenAI-compatible server on `http://localhost:1234/v1`

## Models loaded in LM Studio (exact IDs)
- `qwen/qwen3.6-35b-a3b` (35B — best quality, default)
- `qwen/qwen3.8-27b` (27B — faster)
- `text-embedding-nomic-embed-text-v1.5` (embedding, not chat)

## Config written to ~/.hermes/config.yaml
```yaml
providers:
  openai-codex: {}
  lmstudio:
    base_url: http://localhost:1234/v1
    api_key: lmstudio
    api_mode: chat_completions
    default_model: qwen/qwen3.6-35b-a3b
    models:
      - qwen/qwen3.8-27b
      - qwen/qwen3.6-35b-a3b
```

## Commands that worked
```bash
hermes config set providers.lmstudio.base_url "http://localhost:1234/v1"
hermes config set providers.lmstudio.api_key "lmstudio"
hermes config set providers.lmstudio.api_mode "chat_completions"
hermes config set providers.lmstudio.default_model "qwen/qwen3.6-35b-a3b"
# verify
hermes config get providers.lmstudio --json
hermes chat -q "Reply with exactly: LM Studio connected OK" --provider lmstudio
```

## Key facts
- `hermes config set` handles FLAT provider fields cleanly (unlike nested MoA dicts).
- LM Studio model IDs are prefixed (`qwen/...`) — use the exact `id` from `/v1/models`.
- Local server ignores the api_key value; any non-empty string works.
- Model must be loaded in LM Studio before Hermes can call it; server must be running.
- 35B Q4 ≈ 20 GB RAM while loaded; 70B ≈ 40 GB (too tight on 48 GB — causes swap).
- External USB drive solves storage only, not RAM.
