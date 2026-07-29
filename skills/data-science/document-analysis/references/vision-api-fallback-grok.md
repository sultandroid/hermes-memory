# Vision API Fallback — Grok-4.5 via OpenCode Provider

When `vision_analyze` fails (current model lacks vision support), fall back to calling Grok-4.5 directly via the OpenCode API.

## Why

The current Hermes provider (opencode-go / deepseek-v4-flash) does not support vision/image analysis. `vision_analyze` returns "Error from provider (Console Go): Upstream request failed" for any image input. The models list from this provider includes Grok-4.5, which DOES support vision.

## Available vision-capable models

From `https://opencode.ai/zen/go/v1/models`:
- `grok-4.5` — confirmed working for image analysis
- `minimax-m3` — may support vision
- `kimi-k3` — may support vision
- `qwen3.7-max` — may support vision

## Usage

```python
import base64, os, requests

with open('/path/to/image.png', 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

api_key = os.environ.get('OPENCODE_API_KEY', '')
url = 'https://opencode.ai/zen/go/v1/chat/completions'

payload = {
    'model': 'grok-4.5',
    'messages': [{
        'role': 'user',
        'content': [
            {'type': 'text', 'text': 'Describe this image in detail.'},
            {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{img_b64}'}}
        ]
    }],
    'max_tokens': 1000
}

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

resp = requests.post(url, json=payload, headers=headers, timeout=60)
if resp.status_code == 200:
    print(resp.json()['choices'][0]['message']['content'])
```

## Limitations

- The API key is stored in environment variable `OPENCODE_API_KEY` (not in config.yaml directly — config shows `api_key: ''` but the actual key lives in env)
- `MAX_TOKENS` may need adjustment for larger images
- The model name must be exact: `grok-4.5` (not `grok-4`, not `grok4.5`)
- Some models (deepseek-v4-pro, mimo-v2-omni) failed with 400/500 errors when given images
