# Vision API Fallback — when the main model can't read images

Two paths to get vision when `vision_analyze` fails with "this model does not support image input" (the active model lacks vision).

## Path 1 (PREFERRED): Configure `auxiliary.vision` to a vision-capable model

The `auxiliary.vision` block in `~/.hermes/config.yaml` defaults to `provider: auto` with no model pinned. When `auto` resolves to the same non-vision model as the main provider, `vision_analyze` fails. Fix it by pinning a vision-capable model on the same provider.

For ollama-cloud (the default provider here), vision-capable models include `qwen3.5:397b`, `glm-5.2`, `gemma4:31b`, `kimi-k3`. `qwen3.5:397b` is confirmed working.

```bash
hermes config set auxiliary.vision.provider "custom:ollama-cloud"
hermes config set auxiliary.vision.model "qwen3.5:397b"
hermes config set auxiliary.vision.base_url "https://ollama.com/v1"
hermes config set auxiliary.vision.api_key "$OLLAMA_API_KEY"
```

The API key is NOT in the shell env — it lives in `~/.hermes/.env`. Source it before using:
```bash
export OLLAMA_API_KEY=$(grep -E "^OLLAMA_API_KEY=" ~/.hermes/.env | cut -d= -f2-)
```

**Direct test** (bypasses vision_analyze, useful for batch page scans):
```python
import os, base64, json, urllib.request, ssl
key = os.environ['OLLAMA_API_KEY']
ctx = ssl._create_unverified_context()   # SSL cert verify fails on macOS python3.13 — must use unverified ctx
img = base64.b64encode(open('page.png','rb').read()).decode()
payload = {
  'model': 'qwen3.5:397b',
  'messages': [{'role':'user','content':[
     {'type':'text','text':'Describe this image.'},
     {'type':'image_url','image_url':{'url':'data:image/png;base64,'+img}}
  ]}]
}
req = urllib.request.Request('https://ollama.com/v1/chat/completions',
    data=json.dumps(payload).encode(),
    headers={'Content-Type':'application/json','Authorization':'Bearer '+key})
r = urllib.request.urlopen(req, timeout=120, context=ctx)
print(json.loads(r.read())['choices'][0]['message']['content'])
```

## Path 2: Manual API call to a vision model on another provider

When the main provider has no vision model at all, call a vision-capable model directly. See the Grok-4.5 via OpenCode example below (worked previously).

## Batch page classification (scanned PDF → "is this a table or a single artifact?")

For a scanned multi-page PDF, convert pages to PNG then loop a vision call per page asking a yes/no classification question. This is far more reliable than tesseract on low-quality scans.

```bash
pdftoppm -png -r 150 "doc.pdf" /tmp/pg   # → pg-01.png ... pg-33.png
```

Then loop the direct API call (Path 1) per page with a question like:
"Is this page a TABLE/LIST/INVENTORY (multiple rows/columns, a packing list of boxes), or a single artifact label/photo? Answer in one short line."

## Pitfalls

- **SSL cert verify fails** on macOS python3.13 direct urllib calls → always pass `context=ssl._create_unverified_context()`.
- **`auxiliary.vision` config changes need a fresh session** to take effect for `vision_analyze`; the direct API call works immediately without restart.
- **Subagents inherit the parent's non-vision model** — delegating the image task to a subagent does NOT fix it. Configure the vision auxiliary or use the direct API call yourself.
- **Don't trust tesseract on low-quality photo scans** — museum artifact catalogs, product photos, etc. OCR produces garbled fragments. A vision model reading the actual pixels is the reliable route.
- **One artifact per page ≠ a count of boxes.** A catalog of N pages is N artifacts, not N boxes. If the user asks "how many boxes" and the doc is a catalog (not a packing list), say so explicitly rather than guessing.
