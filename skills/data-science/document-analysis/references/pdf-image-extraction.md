# PDF Image Extraction Workflow

## Overview
Extract all embedded images from a PDF and organize them with descriptive names. Useful for concept design documents, architectural drawings, and renders.

## Two-Stage Approach

### Stage 1: Bulk Extract All Images

Use `pdfimages` (from poppler-utils) for fastest bulk extraction:

```bash
pdfimages -all "/path/to/document.pdf" "/output/dir/img_"
```

- `-all`: Extract JPEG as JPEG, PNG as PNG (preserves quality)
- Output: `img_-000.png`, `img_-001.jpg`, etc.
- Count includes small icons, logos, and tile fragments — typically 150+ files from a 28-page design PDF

### Stage 2: Identify and Rename Renders

Use PyMuPDF to identify which images are the main renders/diagrams by page:

```python
import fitz

doc = fitz.open("/path/to/document.pdf")
for page_num in range(doc.page_count):
    page = doc[page_num]
    images = page.get_images(full=True)
    for img in images:
        xref = img[0]
        base = doc.extract_image(xref)
        w, h = base["width"], base["height"]
        size_kb = len(base["image"]) / 1024
        ext = base["ext"]
        # Only print substantial images
        if w > 100 or h > 100:
            print(f"Page {page_num+1}: xref={xref} {w}x{h} {size_kb:.0f}KB .{ext}")
```

### Stage 3: Extract Named Renders

For known render pages, extract and name descriptively:

```python
import fitz

doc = fitz.open("/path/to/document.pdf")

renders = {
    20: "RENDER_South_Elevation_View.jpg",
    21: "RENDER_Aerial_View.jpg",
    # ... map page numbers to descriptive names
}

for page_num, fname in renders.items():
    page = doc[page_num - 1]  # 0-indexed
    images = page.get_images(full=True)
    if images:
        # Take the first/largest image on the page
        for img in images:
            xref = img[0]
            base = doc.extract_image(xref)
            with open(f"/output/{fname}", 'wb') as f:
                f.write(base["image"])
            break

doc.close()
```

### Stage 4: Export Full Pages

Export every page as a full-resolution PNG for reference:

```python
for page_num in range(1, doc.page_count + 1):
    page = doc[page_num - 1]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x = 200 DPI
    pix.save(f"/output/full_pages/page_{page_num:02d}.png")
```

## Naming Convention for Design Renders

Format: `TYPE_Subject_Description.jpg`

| Type Prefix | When to Use |
|-------------|-------------|
| `RENDER_` | Photorealistic renderings (Option 3 views, lounge, exhibition) |
| `DIAGRAM_` | Concept diagrams, typology matrices, massing studies |
| `PLAN_` | Floor plans, site plans, roof plans |
| `SECTION_` | Cross-sections, elevations |
| `DETAIL_` | Construction details, material callouts |

## Tips

- **Renders are usually large JPGs** (150-750KB) at 958-1200px wide — the truly small files (<50KB) are logos, icons, or tile fragments
- **Concept diagrams are often the largest images** (500-750KB, 3000+px wide) — massing studies and typology matrices
- **Duplicates happen** — some embedded images (logos, headers) repeat on multiple pages. The `pdfimages` output will have multiple identical files from different xrefs
- **Clean up** — after extracting named renders and diagrams, you can remove the raw `img_*` files to keep only organized output
- **Full page exports** are essential for pages where text is vector-based (not embedded images) — these show the complete layout with all labels and annotations
