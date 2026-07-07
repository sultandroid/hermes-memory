# iOS HEIC Photo Processing for Sample Labels

## Source

- iPhone 16 Pro Max, iOS 26.5
- HEIC format, 5712×4284px, Display P3 color space
- File naming: `IMG_XXXX.HEIC` from Camera

## macOS Conversion (sips — System Image Processing Service)

```bash
# Convert HEIC → JPG, resize to 1200px wide
sips -Z 1200 -s format jpeg IMG_2374.HEIC --out photo-CODE.jpg

# Get metadata only (no conversion)
sips -g all IMG_2374.HEIC
```

`-Z` = constrain to max dimension while preserving aspect ratio (1200px = 1200×900 for 4:3 iPhone photos).

## Why not PIL/Pillow?

```python
from PIL import Image
Image.open("IMG_2374.HEIC")  # UnidentifiedImageError
```

macOS's `PIL` (via Homebrew) does not include HEIC support. Options:
- Install `pillow-heif` (`pip install pillow-heif`) and register with PIL
- Use `pyheif` library (separate dependency)
- **Simplest:** use `sips` (built into macOS, no deps needed)

## Result

1200×900 JPG, ~100KB, sRGB. Readable by everything (PIL, browser, Word, CAD).

## Lifecycle

1. User sends HEIC via message/attachment → saved to `~/Downloads/`
2. Agent converts with `sips` → drops into sample folder as `photo-CODE.jpg`
3. Original HEIC stays in Downloads (user can delete later)
