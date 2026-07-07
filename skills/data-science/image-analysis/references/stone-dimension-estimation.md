# Stone Dimension Estimation — Worked Example

## Context

Task: Analyze a stone image from a video frame to estimate dimensions and determine if it matches OB218 (1500×600mm) or is a different larger stone.

## Image Details

- **Source**: `/tmp/stone.jpg` — 848×478px, 123KB JPEG
- **Content**: Close-up of a stone surface with warm earthy brown/tan tones
- **No scale reference objects visible** — no people, doors, vehicles, equipment, or standard objects

## Analysis Pipeline

### Step 1: Basic Image Info

```python
from PIL import Image
import numpy as np

img = Image.open('/tmp/stone.jpg')
pixels = np.array(img)
h, w, _ = pixels.shape
print(f"Image: {w}x{h}px")
```

### Step 2: Color Profiling

```python
r, g, b = pixels[:,:,0].astype(float), pixels[:,:,1].astype(float), pixels[:,:,2].astype(float)
print(f"Avg: RGB({r.mean():.0f},{g.mean():.0f},{b.mean():.0f})")
print(f"Warmth (R-B): {(r-b).mean():.1f}")
```

**Result**: Overall RGB(145,136,120), warmth +25.6 — warm earthy tones consistent with natural stone.

### Step 3: Scale Reference Search

Searched for: bright objects, dark objects, red/orange, blue (sky), green (vegetation), yellow, skin tone, metal.

**Result**: 0% blue, 0% green, 0% red/orange, 0% yellow. Only 2.4% bright white pixels. **No scale references found.**

### Step 4: Region Segmentation

```python
from scipy import ndimage

stone_mask = (r > 80) & (r < 200) & (g > 60) & (g < 180) & (b > 40) & (b < 150) & (r > g) & (g > b)
labeled, n_features = ndimage.label(stone_mask)
```

**Result**: Largest stone region = 116,845px, bbox=(172,70)-(847,345), 675w × 275h, aspect=2.45, RGB(119,104,81).

### Step 5: Edge Analysis

```python
gray = np.mean(pixels, axis=2).astype(float)
gy, gx = np.gradient(gray)
edge_mag = np.sqrt(gx**2 + gy**2)
strong = edge_mag > 30
h_edge, v_edge = np.abs(gx), np.abs(gy)
hv_ratio = h_edge[strong].mean() / max(v_edge[strong].mean(), 0.01)
```

**Result**: H/V ratio = 0.78 — mixed edge directions (natural stone texture, not manufactured slab).

### Step 6: Texture/Feature Analysis

```python
from PIL import ImageFilter
highpass = img.filter(ImageFilter.Kernel((3,3), [-1,-1,-1,-1,8,-1,-1,-1,-1], scale=1))
hp_array = np.array(highpass)
```

**Result**: 12.7% strong features (>80). Feature clustering analysis showed 44 cells with >15% features, distributed across the stone surface — consistent with natural stone grain, not organized text/carvings.

### Step 7: Brightness Transition (Left Edge)

Analyzed x=140-200 to check if the darker left region was a shadow or separate object.

**Result**: Gradual brightness change from 107→148 over 50px — consistent with shadow/lighting gradient, not a sharp object boundary.

### Step 8: Scene Layout

- **Top 70px**: RGB(170,176,184) — slightly blue/cool, possible sky reflection or wall
- **Bottom 78px**: RGB(201,193,173) — lighter, possible concrete ground
- **Left (x=0-170)**: Darker (brightness 108 vs 141 main) — shadow or background
- **Center/Right**: Main stone surface

## Conclusion

| Feature | OB218 | This Stone | Match? |
|---------|-------|------------|--------|
| Aspect ratio | 2.5:1 (1500/600) | ~2.45:1 | **YES** |
| Orientation | Landscape/flat | Landscape/flat | **YES** |
| Color | Not specified | Warm earthy brown | Plausible |
| Absolute dimensions | 1500×600mm | Unknown | **Cannot confirm** |

**Final verdict**: The aspect ratio is consistent with OB218, but without any scale reference object in the frame, absolute dimensions cannot be determined. The image is a close-up — the stone could be 500mm or 5000mm wide. A new photo with a person, door, or vehicle for scale is needed to confirm or refute the claim that this is a larger stone.

## Key Lesson

When vision models are unavailable, a complete pixel-level analysis pipeline can extract:
- Color profiles and material classification
- Aspect ratios and orientation
- Edge direction bias (manufactured vs natural)
- Texture analysis (smooth vs grainy vs carved)
- Scale reference detection (presence/absence of known objects)

But **absolute dimensions require a scale reference** — this is a hard limitation that no amount of pixel analysis can overcome.
