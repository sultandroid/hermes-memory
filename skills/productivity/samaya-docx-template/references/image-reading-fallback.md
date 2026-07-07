# Reading Images When Active Model Lacks Vision

When the user sends a screenshot/image but the active model doesn't support vision, try these fallbacks in order:

## 1. tesseract OCR (fast, no API cost)

```bash
tesseract "/path/to/image.png" stdout 2>/dev/null
```

Works well on text-heavy screenshots at 300+ DPI. For small/low-res images (468x40 px), enlarge first via PIL NEAREST to preserve pixel edges:

```python
from PIL import Image
img = Image.open(path)
img_big = img.resize((w*8, h*8), Image.NEAREST)
img_big.save("/tmp/enhanced.png")
# Then OCR
```

**Limitations:** Fails on handwriting, rotated text, non-Latin scripts without language pack, and very small text (<10px effective height).

## 2. delegate_task with a vision-capable subagent (second resort)

When OCR fails and the image needs genuine visual analysis:

```python
delegate_task(
    goal="Read the content of this PNG image and report exactly what it shows.",
    context=f"Image path: {path}",
)
```

The subagent inherits the parent's model provider — if the parent model lacks vision, the subagent also lacks it. To use a different provider for the subagent, configure `delegation.provider` / `delegation.model` in config.yaml, or let the subagent try alternative approaches like downloading and inspecting image metadata.

## 3. browser-based vision (heavy, last resort)

If the image is hosted at a URL, navigate to it via browser tool and use browser_vision. This works only when the image is publicly accessible at a URL.

## 4. metadata / exif inspection

For screenshots with no visible text, check image metadata:
```python
from PIL import Image
img = Image.open(path)
print(img.size, img.mode, img.info)
```
