# OpenCode Go Provider Fix

## Issue
The `opencode-go` provider in `~/.hermes/config.yaml` had `base_url: 'https://ollama.com/v1'` which is incorrect. This caused HTTP 401 Unauthorized errors when using models like `deepseek-v4-flash`.

## Root Cause
The config was pointing to Ollama's API endpoint instead of OpenCode's actual endpoint.

## Fix
Update the `model` section in `~/.hermes/config.yaml`:

```yaml
model:
  api_key: ''
  base_url: 'https://opencode.ai/zen/go/v1'  # Corrected
  default: deepseek-v4-flash
  provider: opencode-go
  api_mode: chat_completions
```

## Verification
1. Run `hermes config check` — should show `OPENCODE_GO_API_KEY` as ✓
2. Test with `hermes chat -q "test"` — should connect successfully
3. Session shows: `Model: deepseek-v4-flash via opencode-go`

## Command Applied
```bash
hermes config set model.base_url "https://opencode.ai/zen/go/v1"
```

## Notes
- The `OPENCODE_GO_API_KEY` in `~/.hermes/.env` was already correct
- Only the base_url in config.yaml was wrong
- Requires session restart or `/reload` to take effect