# Hermes built-in MoA presets

Hermes has a native `/moa` slash command and named presets under the
`moa:` section of `~/.hermes/config.yaml`. These notes cover how to edit them
without corrupting the YAML.

## Listing presets

```bash
hermes moa list
```

## Two-preset strategy for speed vs strength

When the user needs both fast responses and strong reasoning, create **two
presets** so they can switch via model picker:

### `ollama-fast` (speed-optimized)

All models ≤ Gemini Flash latency. Total turn time ~3-8s.

```yaml
reference_models:
  - {provider: ollama-cloud, model: deepseek-v4-flash}
  - {provider: ollama-cloud, model: gemini-3-flash-preview}
  - {provider: ollama-cloud, model: ministral-3:8b}
  - {provider: ollama-cloud, model: gemma3:12b}
aggregator:
  provider: ollama-cloud
  model: deepseek-v4-flash
```

### `ollama-strong` (quality-optimized)

Strong models for heavy reasoning. Total turn time ~20-40s.

```yaml
reference_models:
  - {provider: ollama-cloud, model: deepseek-v4-pro}
  - {provider: ollama-cloud, model: gemma4:31b}
  - {provider: ollama-cloud, model: qwen3.5:397b}
aggregator:
  provider: ollama-cloud
  model: deepseek-v4-pro
```

### Switching presets

- Via model picker: `hermes model` → select the preset name
- Via config: `hermes config set moa.active_preset ollama-strong`
- Via slash command: `/moa --preset ollama-strong <prompt>`

## Known fast model IDs (Ollama Cloud, verified)

Fast (≤ Gemini Flash latency):
- `deepseek-v4-flash`
- `gemini-3-flash-preview`
- `ministral-3:8b`
- `gemma3:12b`
- `kimi-k2.7-code`
- `glm-5.2`

Strong but slower:
- `deepseek-v4-pro`
- `gemma4:31b`
- `qwen3.5:397b`

## Pitfall: `hermes config set` stringifies lists

`hermes config set` does **not** parse JSON/YAML list syntax. Passing a JSON
array writes the literal string into `config.yaml`, which then fails to load
as a list of reference models.

Bad — leaves a quoted string:

```bash
hermes config set moa.presets.ollama.reference_models '[{"provider":"ollama-cloud","model":"deepseek-v4-pro"},...]'
```

Resulting YAML:

```yaml
reference_models: '[{"provider":"ollama-cloud",...}]'
```

## Fix: edit the YAML as structured data

Use a short Python script with PyYAML (already a Hermes dependency):

```python
import yaml
from pathlib import Path

cfg_path = Path.home() / ".hermes" / "config.yaml"
with open(cfg_path, "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

preset = cfg.setdefault("moa", {}).setdefault("presets", {}).setdefault("ollama", {})
preset["reference_models"] = [
    {"provider": "ollama-cloud", "model": "deepseek-v4-flash"},
    {"provider": "ollama-cloud", "model": "kimi-k2.7-code"},
    {"provider": "ollama-cloud", "model": "qwen3.5:397b"},
    {"provider": "ollama-cloud", "model": "glm-5.2"},
    {"provider": "ollama-cloud", "model": "gemini-3-flash-preview"},
]
preset["aggregator"] = {
    "provider": "ollama-cloud",
    "model": "deepseek-v4-pro",
}
preset["enabled"] = True

with open(cfg_path, "w", encoding="utf-8") as f:
    yaml.safe_dump(cfg, f, default_flow_style=False, sort_keys=False)
```

Then verify:

```bash
hermes moa list
```

## Discovering Ollama Cloud models

Ollama Cloud exposes a standard `/v1/models` endpoint. Query it to see the
exact model IDs available to your key:

```bash
curl -s https://ollama.com/v1/models | python3 -c "import json,sys; data=json.load(sys.stdin); print('\n'.join(m['id'] for m in data['data']))"
```

Use the returned IDs verbatim in `model:` fields. Provider stays
`ollama-cloud`.
