# User Photo Replacement Workflow

When the user provides a local file to replace a specific gallery/hero photo, use this pattern.

## Trigger

User says: `GALLERY_NAME /path/to/file.ext`

Example: `DIRECTORIES /Users/mohamedessa/Downloads/_ (3).jpeg`

## Step 1 — Identify the Gallery Target

The gallery name maps to an image filename in `assets/img/09-wayfinding/` or similar section folder:

| User Says | Current Photo | Folder |
|-----------|--------------|--------|
| DIRECTORIES | `wayfinding-photo-06.jpg` | `09-wayfinding/` |
| PLAQUES | `wayfinding-photo-04.jpg` | `09-wayfinding/` |
| TOTEMS | `wayfinding-photo-05.jpg` | `09-wayfinding/` |
| BRAILLE / TACTILE | `wayfinding-photo-08.jpg` | `09-wayfinding/` |
| FLOOR NUMBERS | `wayfinding-photo-07.jpg` | `09-wayfinding/` |
| ROOM SIGNS | `wayfinding-photo-02.jpg` | `09-wayfinding/` |
| HERO | `wayfinding-photo-01.jpg` | `09-wayfinding/` |

For other sections, the mapping varies — grep the HTML for the gallery label text to find the current image path.

## Step 2 — Copy the File

Copy directly to the destination, overwriting the existing placeholder:

```bash
cp "/Users/mohamedessa/Downloads/Totem.jpeg" \
  "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/samaya-profile/assets/img/09-wayfinding/wayfinding-photo-05.jpg"
```

## Step 3 — WebP Conversion (if needed)

If the source file is `.webp`, convert to JPEG for print compatibility. `sips` handles JPEG conversion natively on macOS (but does NOT read webp natively on all versions):

```bash
# sips may fail on webp files — test first
sips -s format jpeg "/path/to/source.webp" --out "/tmp/converted.jpg" 2>/dev/null
if [ $? -eq 0 ]; then
  cp /tmp/converted.jpg "/path/to/assets/destination.jpg"
else
  # Fallback: copy as-is (browsers support webp, but print may not)
  cp "/path/to/source.webp" "/path/to/assets/destination.jpg"
fi
```

If sips can't handle the webp, copy directly (modern browsers support webp for screen viewing, though print quality may vary).

## Step 4 — Verify HTML Reference

The HTML should already point to the destination path from the placeholder setup. If not, update with patch().

## Step 5 — Confirm

Report back: `Done. destination-file.jpg (GALLERY_NAME) replaced.`

No CHANGELOG entry needed for single photo swaps unless the user asks.
