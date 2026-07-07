# Ollama MoA Preset Setup

This is the exact working configuration used to set up an Ollama-only MoA preset.

## Working YAML (correct format)

```yaml
moa:
  default_preset: ollama
  active_preset: ollama
  presets:
    ollama:
      enabled: true
      reference_models:
        - provider: ollama-cloud
          model: minimax-m2.5
        - provider: ollama-cloud
          model: glm-5.2
        - provider: ollama-cloud
          model: qwen3-coder-next
      aggregator:
        provider: ollama-cloud
        model: minimax-m3
      reference_temperature: 0.6
      aggregator_temperature: 0.4
      max_tokens: 4096
```

## Python script to write the config

```python
import yaml

config_path = '/Users/mohamedessa/.hermes/config.yaml'

with open(config_path, 'r') as f:
    cfg = yaml.safe_load(f)

# Ensure moa section exists
if 'moa' not in cfg:
    cfg['moa'] = {'presets': {}}

cfg['moa']['default_preset'] = 'ollama'
cfg['moa']['active_preset'] = 'ollama'
cfg['moa']['presets']['ollama'] = {
    'enabled': True,
    'reference_models': [
        {'provider': 'ollama-cloud', 'model': 'minimax-m2.5'},
        {'provider': 'ollama-cloud', 'model': 'glm-5.2'},
        {'provider': 'ollama-cloud', 'model': 'qwen3-coder-next'}
    ],
    'aggregator': {'provider': 'ollama-cloud', 'model': 'minimax-m3'},
    'reference_temperature': 0.6,
    'aggregator_temperature': 0.4,
    'max_tokens': 4096
}

with open(config_path, 'w') as f:
    yaml.dump(cfg, f, default_flow_style=False, sort_keys=False)

print('Ollama MoA preset configured')
```

## Available Ollama models (from API)

- minimax-m2.5, minimax-m2.7, minimax-m3
- glm-5.2, glm-4.7
- gemma3:12b, gemma3:27b
- qwen3-coder-next, qwen3.5:397b
- kim-k2.5, kimi-k2.6

## Common error: Wrong format stored as string

If you see this in config.yaml, it's broken:

```yaml
    ollama:
      reference_models: '[{"provider": "ollama-cloud", "model": "minimax-m2.5"}, {"provider": 
        "ollama-cloud", "model": "glm-5.2"}, {"provider": "ollama-cloud", "model": 
        "qwen3-coder-next"}]'
      aggregator: '{"provider": "ollama-cloud", "model": "minimax-m3"}'
```

Fix by running the Python script above.