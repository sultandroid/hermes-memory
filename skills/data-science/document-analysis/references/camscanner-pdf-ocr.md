# CamScanner / iOS Quartz PDF OCR Workflow

CamScanner-generated PDFs (producer: `iOS Version ... Quartz PDFContext`) are image-based scans with **very large page dimensions** (1892×2740 pts = ~7884×11417 px at 300 DPI). These trigger PIL `DecompressionBombWarning` and require specific handling.

## Detection

```bash
pdfinfo document.pdf | grep -E "Producer|Page size|Pages"
# Producer: iOS Version 16.7.16 (Build 20H392) Quartz PDFContext
# Page size: 1892 x 2740 pts  ← very large for a phone scan
# Pages: 3
```

## Pipeline

### 1. Render pages to PNG with PyMuPDF

```python
import fitz
doc = fitz.open("document.pdf")
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=300)
    pix.save(f"/tmp/page_{i}.png")
    print(f"Page {i}: {pix.width}x{pix.height}")
```

### 2. Handle PIL DecompressionBombWarning

Images over 89M pixels trigger PIL's safety limit. **Fix before opening:**

```python
from PIL import Image
Image.MAX_IMAGE_PIXELS = None  # Disable the bomb detection
```

### 3. Resize for faster OCR

300 DPI renders produce 7000-12000px tall images. Resize to 2000px wide:

```python
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

img = Image.open(f"/tmp/page_{i}.png")
w, h = img.size
ratio = 2000 / w
new_size = (2000, int(h * ratio))
img_resized = img.resize(new_size, Image.LANCZOS)
img_resized.convert("RGB").save(f"/tmp/small_{i}.jpg", "JPEG", quality=85)
```

### 4. OCR with tesseract (Arabic + English)

**Must `cd /tmp` first** — tesseract on macOS fails with `fopenReadStream` errors when the image is in `/tmp` due to sandboxed filesystem isolation:

```bash
cd /tmp && tesseract small_0.jpg out_0 -l ara+eng
```

Or use Python pytesseract to avoid the CLI path issue:

```python
import pytesseract
from PIL import Image
img = Image.open("/tmp/small_0.jpg")
text = pytesseract.image_to_string(img, lang="ara+eng")
```

### 5. Read output

```bash
cat /tmp/out_0.txt
```

## Full script

```python
import fitz, pytesseract
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

doc = fitz.open("document.pdf")
for i in range(len(doc)):
    # Render
    pix = doc[i].get_pixmap(dpi=300)
    pix.save(f"/tmp/page_{i}.png")

    # Resize
    img = Image.open(f"/tmp/page_{i}.png")
    w, h = img.size
    ratio = 2000 / w
    img_resized = img.resize((2000, int(h * ratio)), Image.LANCZOS)
    img_resized.convert("RGB").save(f"/tmp/small_{i}.jpg", "JPEG", quality=85)

    # OCR
    text = pytesseract.image_to_string(img_resized, lang="ara+eng")
    print(f"--- Page {i+1} ---")
    print(text)
```

## Common CamScanner artifacts

| Artifact | Example | Handling |
|----------|---------|----------|
| Stamped text over content | "CamScanner" watermark | OCR reads through it; ignore |
| Skewed pages | Slight rotation | Tesseract handles up to ~5° |
| Mixed AR/EN on same line | "قيمة العقد : 74,926,813.83 ريال" | `lang='ara+eng'` handles both |
| Very large page dimensions | 7884×11417 px | Must resize before OCR or PIL crashes |
| Low contrast | Faint text on white bg | Enhance contrast 2-3x before OCR |
