# Vision Delegation Pattern — When Model Lacks Vision

## Trigger

Active model does not support `image_url` content type. Error example:
```
Error code: 400 - unknown variant `image_url`, expected `text`
```
This happens with text-only models (deepseek-v4-flash, gpt-4, etc.). `browser_vision` also fails because the auxiliary fallback routes through the same provider.

## Solution: Delegate to a Vision-Capable Subagent

```python
from hermes_tools import delegate_task, terminal

# Step 1: Copy image to /tmp
terminal("cp '/path/to/image.jpg' /tmp/viz.jpg")

# Step 2: Start local HTTP server
terminal("cd /tmp && python3 -m http.server 8900", background=true)

# Step 3: Delegate vision analysis to subagent
delegate_task(
    goal="Describe this image in complete detail for [your purpose].",
    context=f"Image at http://localhost:8900/viz.jpg\nPath: /path/to/image.jpg\n\nI need [specific details] from this image.",
    toolsets=["browser", "terminal", "file"]
)
```

The subagent:
1. `browser_navigate("http://localhost:8900/viz.jpg")`
2. `browser_vision(question="Describe in full detail...")`
3. Returns structured text description

## Preferred Subagent

**Kimi** — user preference ("let kimi read for you"). Kimi's browser_vision works reliably.

If Kimi is unavailable, spawn via `delegate_task` (which creates a Hermes subagent with any available provider).

## Fallback: Pixel-Level Analysis (No Vision)

When delegation isn't possible, use PIL to extract structural data:

```python
from PIL import Image
img = Image.open("image.jpg")

# Bounding box of object
gray = img.convert('L')
mask = gray.point(lambda x: 0 if x > 200 else 255)
bbox = mask.getbbox()  # (left, top, right, bottom)
print(f"Aspect: {(bbox[2]-bbox[0])/(bbox[3]-bbox[1]):.2f}")

# Horizontal edge density → detect shelves/countertops
edges = gray.filter(ImageFilter.FIND_EDGES)
for y in range(0, h, 10):
    strip = edges.crop((0, y, w, min(y+10, h)))
    density = sum(1 for px in strip.getdata() if px > 128) / (w*10) * 100
    if density > 10:  # strong horizontal feature
        print(f"  y={y}: {density:.1f}% — possible shelf/counter")

# Dominant colors → wood type inference
colors = img.getcolors(w*h)
obj = [(c, color) for c, color in colors if sum(color[:3]) < 700]
# Dark near-black (RGB ~10-20) = dark wood/walnut/wenge or black paint
# Medium brown (RGB 80-150, G>R>B) = oak, teak, stained wood
# Warm (R>G>B) = mahogany, cherry
# Green pixels ~RBG(60,125,55) = plant decoration nearby
```

## Known Limitations

- Subagent timeout: large/complex images may time out. Break into multiple focused questions.
- Local HTTP server: must be running before subagent navigates to it.
- Server port conflicts: use distinct ports per session (8899, 8900, 8901, etc.).
- Screenshot-only access: `browser_vision` works with the rendered browser view, not the raw image. Resolution depends on viewport size.
- No image editing support: subagent can only read/describe, not modify images.
