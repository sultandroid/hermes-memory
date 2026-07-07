# Title Generation Fix — "model not found" 404

## Error
```
⚠ Auxiliary title generation failed: HTTP 404: model "ollama" not found
```

## Root Causes (two variants)

### Variant A: Empty model field
`display.title_generation` has `provider: auto` and `model: ''`. When model is empty, Hermes uses the provider name (`"ollama"`) as the model string, causing a 404.

### Variant B: Invalid provider name
`display.title_generation` has `provider: ollama-cloud` (or any non-existent provider). Hermes can't resolve the provider, falls back to trying a local Ollama model named `"ollama"` — same 404.

## Detection
```bash
grep -n 'title_generation:' ~/.hermes/config.yaml
```
Expected: exactly **one** occurrence at the correct indent (2 spaces, under `display:`).

Read context around each occurrence to identify the variant:
```bash
sed -n 'N,Mp' ~/.hermes/config.yaml   # replace N,M with actual line numbers
```

## Fix

### Step 1: Backup
```bash
cp ~/.hermes/config.yaml ~/.hermes/config.yaml.bak
```

### Step 2: Determine the right provider
**User preference**: prefer reusing an existing working provider (e.g., OpenRouter) over installing new local infrastructure (Ollama). Check what providers are already configured:
```bash
python3 -c "import yaml; cfg=yaml.safe_load(open('/Users/mohamedessa/.hermes/config.yaml')); print('Providers:', list(cfg.get('providers', {}).keys()))"
```

### Step 3: Replace the broken block and delete duplicates
**WARNING**: The `sed` approach below uses hardcoded line numbers that WILL be wrong on a different config file. Always verify line numbers with `grep -n` first and adjust.

```bash
# Replace the first (broken) block — adjust line numbers from grep output
sed -i '' 'START,ENDc\
  title_generation:\
    provider: openrouter\
    model: deepseek/deepseek-chat\
    base_url: '\'''\''\
    api_key: '\'''\''\
    timeout: 30\
    language: '\'''\''' ~/.hermes/config.yaml

# Delete any duplicate blocks — adjust line numbers from grep output
sed -i '' 'DUPLICATE_LINE_START,DUPLICATE_LINE_ENDd' ~/.hermes/config.yaml
```

**Alternative (safer)**: Use Python yaml load/dump to avoid brittle line numbers:
```python
python3 -c "
import yaml
with open('/Users/mohamedessa/.hermes/config.yaml') as f:
    cfg = yaml.safe_load(f)
cfg['display']['title_generation'] = {
    'provider': 'openrouter',
    'model': 'deepseek/deepseek-chat',
    'base_url': '',
    'api_key': '',
    'timeout': 30,
    'language': '',
}
with open('/Users/mohamedessa/.hermes/config.yaml', 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
"
```

## Verification
```bash
grep -n 'title_generation:' ~/.hermes/config.yaml
# Should show exactly one line, e.g. "223:  title_generation:"
```

Also verify the block content:
```bash
grep -A6 'title_generation:' ~/.hermes/config.yaml
```

## Why This Happens
- `hermes config set display.title_generation.provider <value>` **appends** a root-level block instead of updating the existing nested block
- The original block stays broken; the correct values end up in a duplicate block that Hermes ignores
- An invalid provider name (`ollama-cloud`) causes the same 404 as an empty model field

## Prevention
- Always check for duplicates after using `hermes config set` on nested keys
- Prefer Python yaml load/dump over `sed` with hardcoded line numbers
- Set both `provider` and `model` explicitly — never leave model empty
- Use a real provider name (e.g., `openrouter`, `anthropic`) — not a made-up name
- User prefers reusing existing working providers over installing new local infrastructure
