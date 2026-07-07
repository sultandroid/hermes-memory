---
name: image-analysis
description: "Programmatic image analysis when vision models are unavailable — pixel-level analysis using Python/PIL/NumPy/SciPy for color profiling, edge detection, region segmentation, texture analysis, aspect ratio estimation, and scale-reference search. Use when vision_analyze or browser_vision fails (model doesn't support image input) or when you need quantitative pixel data."
version: 1.0.0
author: hermes
license: MIT
platforms: [macos, linux]
prerequisites:
  commands: [python3]
  packages: [Pillow, numpy, scipy]
  env_vars: []
metadata:
  hermes:
    tags: [image-analysis, vision-fallback, pixel-analysis, computer-vision, python, ocr, text-extraction, tiny-image]
    examples: ["stone-dimension-estimation", "object-scale-analysis", "tiny-image-text-extraction"]
---

# Image Analysis (Vision Fallback)

Programmatic image analysis pipeline for when vision-capable models are unavailable. Uses Python/PIL/NumPy/SciPy to extract quantitative data from images — color profiles, edge maps, region segmentation, texture analysis, and scale reference detection.

## When to Use

Use this skill when:
- `vision_analyze()` returns "model does not support image input"
- `browser_vision()` fails with the same error
- You need **quantitative** pixel data (not just a description)
- You need to estimate dimensions, aspect ratios, or detect objects without a vision model

## Quick Start

```python
from PIL import Image
import numpy as np

img = Image.open('/path/to/image.jpg')
pixels = np.array(img)
h, w, _ = pixels.shape
print(f"Image: {w}x{h}px, {img.mode}")
```

## Analysis Modules

### 1. Color Profiling

```python
r, g, b = pixels[:,:,0].astype(float), pixels[:,:,1].astype(float), pixels[:,:,2].astype(float)

# Overall stats
print(f"Avg: RGB({r.mean():.0f},{g.mean():.0f},{b.mean():.0f})")
print(f"Std: RGB({r.std():.0f},{g.std():.0f},{b.std():.0f})")

# Warmth index (positive = warm tones like stone/earth)
warmth = r - b
print(f"Warmth (R-B): {warmth.mean():.1f}")

# Saturation proxy
sat = np.abs(r - g) + np.abs(g - b) + np.abs(b - r)
print(f"Saturation: {sat.mean():.1f}")
```

**Color classification heuristics:**

| Pattern | Likely Content |
|---------|---------------|
| R > G > B, moderate brightness (80-200) | Earth/stone (warm brown) |
| B > R, B > G, B > 100 | Sky |
| R > 200, G > 200, B > 200 | Bright/white surface |
| R > 150, G > 150, B > 140, low std | Concrete/gray |
| G > R, G > B, G > 80 | Vegetation |
| R > 150, G < 100, B < 100 | Red/orange object |
| R > 180, G > 180, B < 100 | Yellow object |
| R > 100, G > 60, B > 40, R > G, abs(R-G) < 50 | Skin tone |

### 2. Grid Region Analysis

Divide the image into a 3×3 grid to understand scene layout:

```python
rows = [0, h//3, 2*h//3, h]
cols = [0, w//3, 2*w//3, w]

for ri in range(3):
    for ci in range(3):
        region = pixels[rows[ri]:rows[ri+1], cols[ci]:cols[ci+1], :]
        avg = region.mean(axis=(0,1))
        std = region.std(axis=(0,1))
        print(f"Cell ({ri},{ci}): RGB({avg[0]:.0f},{avg[1]:.0f},{avg[2]:.0f}) std=({std[0]:.0f},{std[1]:.0f},{std[2]:.0f})")
```

**Interpretation:**
- Top row cooler/brighter → sky or wall
- Bottom row lighter → ground/concrete
- Center row warm/brown → main subject (stone, earth)
- Left/right differences → shadow, second object, or background

### 3. Scale Reference Search

Search for known objects that provide scale:

```python
# Bright white (people, equipment, markers)
bright = (r > 200) & (g > 200) & (b > 200)
print(f"Bright objects: {bright.mean()*100:.1f}%")

# Dark (shadows, tires, dark clothing)
dark = (r < 50) & (g < 50) & (b < 50)
print(f"Dark objects: {dark.mean()*100:.1f}%")

# Red/orange (safety vests, equipment)
red = (r > 150) & (g < 100) & (b < 100)
print(f"Red objects: {red.mean()*100:.1f}%")

# Blue (sky, clothing, tarps)
blue = (b > 150) & (r < 120) & (g < 120)
print(f"Blue objects: {blue.mean()*100:.1f}%")

# Green (vegetation, safety vests)
green = (g > 120) & (r < 100) & (b < 100)
print(f"Green objects: {green.mean()*100:.1f}%")

# Yellow (construction equipment)
yellow = (r > 180) & (g > 180) & (b < 100)
print(f"Yellow objects: {yellow.mean()*100:.1f}%")

# Skin tone
skin = (r > 100) & (r < 200) & (g > 60) & (g < 150) & (b > 40) & (b < 120) & (r > g) & (abs(r-g) < 50)
print(f"Skin tone: {skin.mean()*100:.1f}%")

# Metal/reflective (high brightness, low saturation)
metal = (r > 180) & (g > 180) & (b > 180) & (abs(r-g) < 15) & (abs(g-b) < 15)
print(f"Metal: {metal.mean()*100:.1f}%")
```

**If all are <1%**: The image is a close-up with no standard-scale objects — absolute dimensions cannot be determined.

### 4. Region Segmentation (Connected Components)

Find the largest contiguous regions of a specific color class:

```python
from scipy import ndimage

# Create mask for target material (e.g., stone: warm earthy tones)
mask = (r > 80) & (r < 200) & (g > 60) & (g < 180) & (b > 40) & (b < 150) & (r > g) & (g > b)

labeled, n_features = ndimage.label(mask)
sizes = [(labeled == i).sum() for i in range(1, n_features + 1)]

for rank, (idx, size) in enumerate(sorted(enumerate(sizes), key=lambda x: x[1], reverse=True)[:5]):
    label = idx + 1
    coords = np.where(labeled == label)
    y_min, y_max = int(coords[0].min()), int(coords[0].max())
    x_min, x_max = int(coords[1].min()), int(coords[1].max())
    width = x_max - x_min
    height = y_max - y_min
    aspect = width / max(height, 1)
    region_pixels = pixels[coords[0], coords[1], :]
    avg_color = region_pixels.mean(axis=0)
    print(f"Region {rank+1}: {size}px, bbox=({x_min},{y_min})-({x_max},{y_max}), "
          f"{width}w x {height}h, aspect={aspect:.2f}, RGB({avg_color[0]:.0f},{avg_color[1]:.0f},{avg_color[2]:.0f})")
```

### 5. Edge Detection & Direction Analysis

Determine edge strength and dominant orientation:

```python
gray = np.mean(pixels, axis=2).astype(float)
gy, gx = np.gradient(gray)
edge_mag = np.sqrt(gx**2 + gy**2)

# Edge strength
strong = edge_mag > 30
print(f"Strong edges: {strong.mean()*100:.1f}%")

# Edge direction bias
h_edge = np.abs(gx)
v_edge = np.abs(gy)
hv_ratio = h_edge[strong].mean() / max(v_edge[strong].mean(), 0.01)
print(f"H/V edge ratio: {hv_ratio:.2f}")

if hv_ratio > 1.3:
    print("-> DOMINANT HORIZONTAL edges (object likely laid flat)")
elif hv_ratio < 0.7:
    print("-> DOMINANT VERTICAL edges (object likely standing vertical)")
else:
    print("-> Mixed edge directions (natural surface texture)")
```

### 6. Texture & Feature Analysis

Detect high-frequency content (potential text, carvings, or surface grain):

```python
from PIL import ImageFilter

img_pil = Image.fromarray(pixels)
highpass = img_pil.filter(ImageFilter.Kernel((3,3), [-1,-1,-1,-1,8,-1,-1,-1,-1], scale=1))
hp_array = np.array(highpass)
hp_gray = np.mean(hp_array, axis=2).astype(float)

# Overall high-frequency content
hp_strong = hp_gray > 80
print(f"Strong features (>80): {hp_strong.mean()*100:.1f}%")

# Feature clustering (text would have regular spacing)
cell_size = 20
feature_density = []
for y in range(0, h - cell_size, cell_size):
    for x in range(0, w - cell_size, cell_size):
        cell = hp_gray[y:y+cell_size, x:x+cell_size]
        feature_density.append((cell > 80).mean())

fd = np.array(feature_density)
print(f"Feature density: mean={fd.mean()*100:.1f}%, std={fd.std()*100:.1f}%")
print(f"Cells with >5% features: {(fd > 0.05).mean()*100:.1f}%")
print(f"Cells with >20% features: {(fd > 0.20).mean()*100:.1f}%")
```

**Interpretation:**
- <5% strong features → smooth surface
- 5-15% strong features → natural texture (stone grain, wood)
- >15% strong features with clustering → potential text/carvings/artifacts
- Uniformly distributed features → natural texture
- Clustered features with regular spacing → potential text

### 7. Brightness Transition Analysis

Detect object boundaries by analyzing brightness across a transition zone:

```python
# Analyze brightness profile across x=140-200 (example transition zone)
for x in range(140, 200):
    strip = pixels[:, x:min(x+1, w), :]
    brightness = strip.mean()
    bar = "#" * int(brightness / 3)
    print(f"x={x}: brightness={brightness:.0f} {bar}")
```

**Interpretation:**
- Gradual brightness change → shadow or lighting gradient
- Sharp brightness jump (10+ units in 1-2px) → object boundary/edge
- No significant change → same surface/object

### 8. Horizontal & Vertical Profile

Understand scene composition:

```python
# Horizontal profile (avg per column band)
for x_start in range(0, w, 50):
    x_end = min(x_start + 50, w)
    strip = pixels[:, x_start:x_end, :]
    avg = strip.mean(axis=(0,1))
    print(f"x={x_start}-{x_end}: RGB({avg[0]:.0f},{avg[1]:.0f},{avg[2]:.0f})")

# Vertical profile (avg per row band)
for y_start in range(0, h, 30):
    y_end = min(y_start + 30, h)
    strip = pixels[y_start:y_end, :, :]
    avg = strip.mean(axis=(0,1))
    print(f"y={y_start}-{y_end}: RGB({avg[0]:.0f},{avg[1]:.0f},{avg[2]:.0f})")
```

### 9. Anomaly Detection

Find pixels that deviate significantly from the dominant palette:

```python
earth_mean = np.array([145, 136, 120])  # adjust per image
earth_std = np.array([63, 65, 67])      # adjust per image
diff = np.abs(pixels.astype(float) - earth_mean)
anomalous = (diff[:,:,0] > 2*earth_std[0]) | (diff[:,:,1] > 2*earth_std[1]) | (diff[:,:,2] > 2*earth_std[2])
print(f"Anomalous pixels: {anomalous.mean()*100:.1f}%")

# Where are they?
coords = np.where(anomalous)
if len(coords[0]) > 0:
    print(f"Range: x=[{coords[1].min()}-{coords[1].max()}], y=[{coords[0].min()}-{coords[0].max()}]")
    for i in range(min(5, len(coords[0]))):
        y, x = coords[0][i], coords[1][i]
        print(f"  Anomaly at ({x},{y}): RGB({pixels[y,x,0]},{pixels[y,x,1]},{pixels[y,x,2]})")
```

## Dimension Estimation Workflow

When asked to estimate dimensions from an image:

1. **Check for scale references** (Section 3) — people, doors, vehicles, standard objects
2. **If scale references exist**: Use known object dimensions as pixel-to-mm ratio
3. **If no scale references**: Report aspect ratio only, state that absolute dimensions cannot be determined
4. **Report orientation**: Landscape (wider than tall) or portrait (taller than wide)
5. **Compare aspect ratio** to known reference dimensions

```python
# Example: Compare to known object dimensions
known_width_mm = 1500  # e.g., OB218 stone
known_height_mm = 600
known_aspect = known_width_mm / known_height_mm  # 2.5

stone_width_px = 675
stone_height_px = 275
stone_aspect = stone_width_px / stone_height_px  # ~2.45

print(f"Known aspect: {known_aspect:.2f}")
print(f"Measured aspect: {stone_aspect:.2f}")
print(f"Match: {'YES' if abs(stone_aspect - known_aspect) < 0.2 else 'NO'}")
```

## 10. Text Extraction via ASCII Pixel Rendering (Tiny Text Images)

When `vision_analyze()` fails and the image is small (<500px wide, <50px tall) with text content, traditional OCR often garbles the output. Use pixel-level ASCII rendering combined with pytesseract and cross-character comparison.

### Strategy: Three-Pronged Verification

For each character in doubt, cross-reference three sources:

1. **OCR** (pytesseract with multiple PSM modes)
2. **ASCII pixel rendering** (direct character-shape visualization)
3. **Cross-character comparison** (compare pixel patterns between known and unknown characters)

### Step 1: Image Intel

```bash
file /path/to/image.png
```

Take note of dimensions. If under ~500×60, special handling is needed.

### Step 2: Pixel Value Mapping

```python
from PIL import Image

img = Image.open('/path/to/image.png')
gray = img.convert('L')
pixels = list(gray.getdata())
w, h = gray.size

# Understand the pixel range — critical for binarization
all_unique = sorted(set(pixels))
print(f"Unique pixel values: {all_unique}")
print(f"Min: {all_unique[0]}, Max: {all_unique[-1]}")
```

Look for images with 2-5 unique pixel values — these are likely screenshots/graphics with text on uniform background.

### Step 3: Determine Polarity

```python
# Count bright vs dark pixels
bright = sum(1 for p in pixels if p > 128)
dark = sum(1 for p in pixels if p < 128)
print(f"Bright: {bright}, Dark: {dark}")

# If max value < 128, the image is dark with brighter text
# Choose threshold accordingly
threshold = max(pixels) - 20  # for dark-bg-light-text
# or
threshold = min(pixels) + 20  # for light-bg-dark-text
```

### Step 4: ASCII Pixel Rendering

```python
print("=== FULL ASCII ART ===")
for y in range(h):
    row = ''
    for x in range(w):
        p = pixels[y*w + x]
        row += '#' if p > threshold else ' '
    print(f'{y:2d}|{row}|')
```

**Why this works:** For very small text images, the ASCII rendering lets YOU interpret the characters — your model's pattern recognition on 1D character-shaped pixel blobs is often more reliable than OCR on the raw 2D image.

### Step 5: Zoom on Ambiguous Areas

When OCR produces nonsense or has character confusion (e.g., `O` vs `0`, `5` vs `3`, `l` vs `1`):

```python
# Zoom on a specific x-range
def zoom_ascii(pixels, w, h, x_start, x_end, threshold):
    for y in range(h):
        row = ''
        for x in range(x_start, min(x_end, w)):
            p = pixels[y*w + x]
            row += '#' if p > threshold else ' '
        if '#' in row:
            print(f'y={y:2d}: |{row}|')
```

### Step 6: Cross-Character Comparison

When OCR says "SHC-O5" but context suggests "SHC-05":

- Locate the '0' in known contexts (e.g., SHC-01, SHC-02, SHC-04)
- Render the contested '0/O' area at the same x-scale
- Compare shape patterns side by side

```python
# Compare same character across different positions
print("=== '0' from SHC-01 ===")
zoom_ascii(pixels, w, h, 127, 143, threshold)
print("=== '0' from SHC-02 ===")
zoom_ascii(pixels, w, h, 173, 189, threshold)
print("=== Challenged '0/O' from contested code ===")
zoom_ascii(pixels, w, h, 264, 280, threshold)
```

**Rule of thumb:** If the contested character's shape matches the known '0' (closed rounded shape, same width, same baseline penetration) across multiple instances, it's '0' not 'O'.

### Step 7: OCR Binarization & Upscaling

Once you understand the pixel range from Step 2, create a clean binary image:

```python
# Map: text pixels to black (0), background to white (255)
new_pixels = []
for p in pixels:
    if p > threshold:
        new_pixels.append(0)   # text
    else:
        new_pixels.append(255) # background

binary = Image.new('L', (w, h))
binary.putdata(new_pixels)

# Upscale 4-8x with NEAREST to preserve pixel edges
big = binary.resize((w*8, h*8), Image.NEAREST)
big.save('/tmp/ocr_clean.png')
```

Then OCR the upscaled binary:

```python
import pytesseract
for psm in [6, 7, 3]:
    t = pytesseract.image_to_string(big, config=f'--psm {psm} --oem 3')
    print(f'psm={psm}: {repr(t.strip())}')
```

PSM 7 (single text line) is best for one-line images. PSM 6 (uniform block) and PSM 3 (default) as cross-checks.

### Step 8: Use `file` Command for Format Intel

```bash
file /path/to/image.png
```

Outputs exact dimensions, bit depth, color mode. A PNG with `16-bit/color RGBA, non-interlaced` and small dimensions strongly suggests a screenshot snippet.

## Pitfalls

1. **No scale reference = no absolute dimensions**: The most common mistake is claiming dimensions without a known object for scale. Always check for people, doors, vehicles, or standard objects first.
2. **Close-up vs distant shot**: Without context, a 100px-wide object could be 10mm (macro) or 10m (distant). The image composition (close-up vs wide shot) must be inferred from color distribution and edge content.
3. **Color-based segmentation is approximate**: Natural materials (stone, wood) have wide color variation. Tune thresholds per image.
4. **JPEG compression artifacts**: Low-quality JPEGs create false edges. Use a higher edge threshold (>30) to filter noise.
5. **SciPy not always available**: `scipy.ndimage.label` is used for connected components. Fall back to simple bounding box if scipy is missing.
6. **Large images**: Resize before analysis if the image is >2000px on any side. Use `img.resize((w//4, h//4))` for speed.
7. **Screenshots include browser chrome**: When analyzing browser screenshots, crop to the actual image content first by finding where earthy/meaningful pixel content begins.
8. **The model cannot see the image**: You are working blind — every analysis step must be verified by printing intermediate results. Save edge maps and highpass images to disk for optional human review.
9. **OCR from very small images (<500×50) will garble**: Upscaling with NEAREST (not BILINEAR/LANCZOS) preserves pixel edges best for OCR. Nearest-neighbor keeps hard character boundaries intact.
10. **Don't trust a single PSM mode**: PSM 6, 7, and 3 often give different results on the same tiny image. Cross-reference all three. When they disagree, the ASCII pixel rendering (Steps 4-6) is the tiebreaker.
11. **Character whitelists can mislead**: `-c tessedit_char_whitelist=...` can force wrong readings. First run without whitelist, use it only after you know the context to resolve specific character ambiguity.
12. **'5' vs '3' confusion**: These digits share similar top curves. Use the bottom stroke — '5' has a flat bottom curve extending left, '3' has a rounded bottom that curves back up. ASCII zoom at the character's lower half resolves this.
13. **'0' vs 'O' confusion**: OCR routinely misreads narrow '0' as 'O'. Compare width — '0' is full-width (same as other digits), 'O' (letter) is narrower. In sequential codes (SHC-01, SHC-02, etc.), zero is guaranteed by context.
14. **pytesseract installed but no tesseract binary**: `pip install pytesseract` alone won't work. The macOS homebrew tesseract package is `brew install tesseract`. Verify with `which tesseract`.

## Reference Files

- `references/stone-dimension-estimation.md` — Worked example: estimating stone dimensions from a close-up photo with no scale reference, comparing to OB218 (1500×600mm)
- `references/tiny-image-text-extraction.md` — Worked example: reading text from a 468×40 screenshot caption with OCR + ASCII pixel rendering + cross-character comparison

## Verification

```bash
python3 -c "
from PIL import Image
import numpy as np
img = Image.open('/tmp/test.jpg')
pixels = np.array(img)
print(f'{img.size[0]}x{img.size[1]}px, RGB({pixels.mean(axis=(0,1))[0]:.0f},{pixels.mean(axis=(0,1))[1]:.0f},{pixels.mean(axis=(0,1))[2]:.0f})')
"
```
