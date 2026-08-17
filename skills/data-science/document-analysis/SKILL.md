---
name: document-analysis
description: "Use when extracting structured data from PDFs, scans, or exported Excel registers (BIM/museum project logs) — handles RTL Arabic, mirrored pages, multi-section registers, table continuity, and OneDrive-locked files."
version: 1.0.0
author: hermes
license: MIT
platforms: [macos, linux]
prerequisites:
  commands: [python3, pdfplumber, tesseract]
  env_vars: []
metadata:
  hermes:
    tags: [pdf, document-extraction, rtl, arabic, excel, register]
    examples: ["aseer-register", "pdfplumber"]
---

# Document Analysis

Extract structured data from PDFs and Excel exports for BIM/museum project registers.

## Pick the right route

| Source | Tool | Notes |
|--------|------|-------|
| URL-accessible PDF | `web_extract(urls=[...])` | Handles PDF-to-markdown, zero local deps — try this FIRST for any URL |
| **Large self-contained HTML plan document** | **`search_files` (regex) + `read_file` (offset/limit)** | **PEP, DMP, BEP as single-file HTML with inline CSS. Locate sections via `<!-- PAGE` comment markers + `<h2>` headings. Extract tables, dashboards, flow diagrams, and milestone tracks sector by sector. See `references/html-project-plan-audit.md`.** |
| PDF with real tables | `pdfplumber` | `extract_tables()` + `extract_text()` |
| Simple single-column PDF (quotes) | `pdftotext` (poppler) | beats pdfplumber on irregular layouts |
| macOS text-based PDF (fastest) | `pdftotext -layout -enc UTF-8` | Available on macOS via poppler, handles bilingual AR/EN |
| **Bilingual KSA government contract (AR/EN dual-column)** | **`pdftotext -layout` + Python Unicode split** | **Split each line at first Arabic Unicode char (\u0600-\u06FF) into separate EN and AR files. Always produce TWO files, never merged. See `references/aseer-main-contract-extraction.md` for worked example.** |
| Image-based PDF (no text layer) | PyMuPDF (`fitz`) → render to PNG → `tesseract` OCR | common for Illustrator/InDesign exports, scanned drawings |
| **Scanned photo catalog (low-quality scans, OCR garbles)** | **Vision model reads the pixels directly** — configure `auxiliary.vision` to a vision-capable model (e.g. `qwen3.5:397b` on ollama-cloud) or call the vision API directly per page. Far more reliable than tesseract on photo scans. See `references/vision-api-fallback-grok.md` | museum artifact catalogs, product photos, packing lists |
| **Slide deck PDF (PowerPoint/Keynote export)** | PyMuPDF → PNG → tesseract OCR, **then supplement with web sources** | 39-page slide decks with decorative elements; OCR is incomplete — always find a companion text document (overview PDF, published article) as primary source |
| Scanned PDF (lightweight OCR) | `pytesseract` + Pillow | ~200MB tesseract, no PyTorch needed |
| Complex layouts / equations / forms | `marker-pdf` | Best accuracy, ~3-5GB install |
| Encrypted PDF (128-bit RC4) | `pypdf` → `reader.decrypt('')` → then any tool | Many national-adoption PDFs are encrypted; decrypt first with empty password, then extract with pdftotext/pymupdf |
| Incomplete PDF (partial content) | Compare page count vs TOC; supplement with web sources | National adoptions may only contain front matter + first few clauses; detect by checking if last page ends mid-document |
| OneDrive-locked PDF | hydrate via `open` (Preview), then `pdftotext` | NOT the Excel/AppleScript route |
| `.xlsb` (OneDrive-locked) | Excel → Save As `.xlsx`, then `openpyxl` | only working path; xlsb is binary |
| `.xlsx` | `openpyxl` (`read_only`, `data_only`) | |
| DOCX | `python-docx` | Parses actual structure, far better than OCR |
| **OneDrive-locked DOCX** | **`zipfile.ZipFile` + regex tag-strip** | **When `python-docx` fails with `Resource deadlock avoided` — zipfile's raw byte I/O may bypass the macOS OneDrive lock. Extract `word/document.xml`, strip XML tags with `re.sub(r'<[^>]+>', ' ', xml)`, squeeze whitespace. See [OneDrive-locked DOCX](#onedrive-locked-docx) below.** |
| PPTX | See `powerpoint` skill | Uses `python-pptx` with full slide/notes |

### pymupdf (lightweight, instant)

```bash
pip install pymupdf pymupdf4llm
python3 -c "
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
"
```

For markdown, tables, images, metadata, or specific pages — use the helper scripts from this skill's `scripts/` directory.

### marker-pdf (high-quality OCR)

```bash
pip install marker-pdf
marker_single document.pdf --output_dir ./output
```

**Decision**: Use pymupdf unless you need OCR, equations, forms, or complex layout analysis. marker-pdf downloads ~2.5GB of models on first use.

### Lightweight Scanned-PDF OCR with tesseract

When pymupdf returns empty text (scanned / image-based pages) and marker-pdf is too heavy:

**Route A — PyMuPDF render (multi-page, any PDF):**

```python
import fitz, pytesseract
from PIL import Image

doc = fitz.open("document.pdf")
page = doc[0]
pix = page.get_pixmap(dpi=300)
img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
text = pytesseract.image_to_string(img, lang='eng', config='--psm 12')
```

**Route B — sips render (simpler, macOS-only, single-page or simple PDFs):**

For scanned letter PDFs (not tables, not books — just letter text), `sips` is simpler than PyMuPDF:

```bash
# Convert PDF page 1 to PNG
sips -s format png "/path/to/letter.pdf" --out /tmp/letter.png

# Then OCR with tesseract
tesseract /tmp/letter.png stdout -l eng
```

**Critical: tesseract /tmp path issue on macOS.** Tesseract can fail with `fopenReadStream` errors when the image is in `/tmp` due to sandboxed filesystem isolation. The error looks like:

```
Error in fopenReadStream: failed to open locally with tail letter.png for filename /tmp/letter.png
Leptonica Error in findFileFormat: image file not found: /tmp/letter.png
```

**Workaround — `cd /tmp` first (simplest):**

The root cause is that tesseract resolves relative paths from its own working directory, not the shell's CWD. Changing the working directory to `/tmp` before running tesseract fixes it:

```bash
cd /tmp && tesseract letter.png stdout -l eng
```

**Fallback — copy to CWD:**

```bash
cp /tmp/letter.png ./letter.png && tesseract ./letter.png stdout -l eng
```

Or use Python + pytesseract (avoids the CLI path issue entirely):

```python
from PIL import Image
import pytesseract
img = Image.open('/tmp/letter.png')
text = pytesseract.image_to_string(img, lang='eng')
```

**Route C — pdftoppm (CLI, multi-page, portable):**

For bulk batch conversion of scanned PDFs to page images, `pdftoppm` (from poppler) is the simplest CLI option — no Python needed:

```bash
# Convert all pages to JPEG at 200 DPI
pdftoppm -jpeg -r 200 "document.pdf" page_prefix

# Output: page_prefix-1.jpg, page_prefix-2.jpg, ...

# Convert to PNG at 300 DPI
pdftoppm -png -r 300 "document.pdf" page_prefix

# Single page
pdftoppm -jpeg -r 200 -f 1 -l 1 "document.pdf" page_prefix
```

**Key benefits over PyMuPDF:**
- Pure CLI — works in a one-liner loop, no Python process overhead
- Handles page ranges with `-f` / `-l` flags
- Available from poppler (brew install poppler on macOS)
- Faster for batch conversion of 10+ pages

**Pre-processing with ImageMagick (faster OCR):**

Large images (3000+ px wide at 200 DPI) slow tesseract significantly. Resize before OCR:

```bash
# Resize to 1200px wide, 75% quality JPEG
magick large_page.jpg -resize 1200x -quality 75 small_page.jpg

# Batch resize all page images
mkdir -p small
for f in page_prefix-*.jpg; do
  magick "$f" -resize 1200x -quality 75 "small/$f"
done
```

**When to resize:**
- **200-300 DPI page renders** = 2500-4000px wide → resize to 1200px saves 60-70% size, minimal OCR quality loss
- **Already-small images** (under 1000px) → skip resize
- **Handwritten/faint text** → skip resize, keep maximum resolution
- **Table-heavy documents** → resize gently (1600px) to preserve cell boundaries

**When to use which route:**

| Situation | Route |
|-----------|-------|
| Multi-page PDF, need page-by-page | A (PyMuPDF) |
| Single-page scanned letter, macOS | B (sips) — fewer deps |
| Bulk batch conversion (10+ pages) | C (pdftoppm) — pure CLI, fastest |
| Tables / structured data | A (PyMuPDF) + TSV reconstruction |
| tesseract CLI fails on /tmp | Use Python pytesseract or copy to CWD |

**PSM selection guide**: `3`=default, `4`=single column, `6`=single block, `11`=sparse text, `12`=single block variable orient (best for tables/forms), `13`=raw line.

**Pre-processing for difficult scans:**
```python
from PIL import ImageEnhance
gray = img.convert('L')
enhancer = ImageEnhance.Contrast(gray)
gray_high = enhancer.enhance(2.0)
```

### Multi-Pass OCR Cross-Referencing (Difficult Scans)

When a single OCR pass produces garbled output (common with scanned letters, faxes, or low-quality images), run OCR on **multiple image variants** of the same page and cross-reference the results to reconstruct the correct text:

**Strategy — render the same page at different quality levels and compare:**

```bash
# Pass 1: Original render
tesseract page1.png stdout -l eng > /tmp/pass1.txt

# Pass 2: Enhanced contrast (grayscale, 2-3x contrast)
python3 -c "
from PIL import Image, ImageEnhance
img = Image.open('page1.png').convert('L')
img = ImageEnhance.Contrast(img).enhance(2.0)
img.save('/tmp/page1_enhanced.png')
"
tesseract /tmp/page1_enhanced.png stdout -l eng > /tmp/pass2.txt

# Pass 3: Aggressive binarization
python3 -c "
from PIL import Image
img = Image.open('page1.png').convert('L')
img = img.point(lambda x: 0 if x < 180 else 255, '1')
img.save('/tmp/page1_binary.png')
"
tesseract /tmp/page1_binary.png stdout -l eng > /tmp/pass3.txt
```

**Cross-reference rules:**
- **Consensus text** (same words in 2+ passes) → accept as correct
- **Unique text** (only in one pass) → likely noise or OCR hallucination — flag for manual review
- **Character-level disagreements** (e.g. "GLASBAU bH" vs "GLASBAU HAHN") → the longer/more specific variant is usually correct
- **Known artifacts** (e.g. "§@" from logo graphics, "hare ?" for "Page 2") → recognize and discard

**When to use which variant:**

| Variant | Best for | Trade-off |
|---------|----------|-----------|
| Original render | General purpose, good contrast pages | May miss faint text |
| Enhanced contrast (2-3x) | Faint/light text, low-contrast scans | Can amplify noise |
| Aggressive binarization | Very faint text, pencil marks | Destroys thin strokes |
| Inverted (dark bg) | White-on-dark text, watermarks | Only for specific layouts |

**Pitfall — don't trust a single pass.** OCR on the same image can produce different results depending on contrast, binarization, and PSM mode. Always run at least 2-3 variants and cross-reference. The most reliable text is the intersection of multiple passes.

**Pitfall — run a full-page OCR pass BEFORE narrow-crop hunting.** When a table value (e.g. a fee/amount) is missed, the instinct is to crop tighter and re-OCR — but repeated narrow crops often keep missing it while a single full-page pass catches it. In a scanned 3-page proposal, the amount `175,000.00` was recovered by the FIRST full-page `tesseract` pass (PSM 6) on the page image, while ~10 successive zoomed crops of the same table region returned only headers. Workflow: (1) extract page images with `pdfimages -png doc.pdf /tmp/pg` (or `pdftoppm`), (2) run a full-page OCR pass per page first, (3) only zoom-crop for values the full pass missed. Don't burn cycles re-cropping a region the full pass already read.

### Table Reconstruction from Garbled OCR

Image-based PDFs with tabular data (inspection certificates, test reports, material data sheets) produce garbled OCR output where table cells are jumbled, column headers are scrambled, and values are misaligned. Use this multi-strategy pipeline to recover structured data.

#### Strategy 1: TSV Bounding-Box Line Reconstruction

Use `pytesseract.image_to_data()` with `output_type=pytesseract.Output.DICT` to get per-word bounding boxes, then group by `(block_num, line_num)` and sort by `left` coordinate to reconstruct table rows:

```python
from collections import defaultdict

data = pytesseract.image_to_data(img, lang='eng',
    config='--oem 3 --psm 6', output_type=pytesseract.Output.DICT)

lines = defaultdict(list)
for i in range(len(data['text'])):
    t = data['text'][i].strip()
    if t and data['conf'][i] > 0:  # filter low-confidence noise
        key = (data['block_num'][i], data['line_num'][i])
        lines[key].append((data['left'][i], t))

for key in sorted(lines.keys()):
    items = sorted(lines[key], key=lambda x: x[0])
    print(' | '.join(item[1] for item in items))
```

**Why this works:** Tesseract's TSV output preserves spatial position even when the raw `image_to_string` output is garbled. Grouping by block+line and sorting by x-coordinate reconstructs the original table layout.

**Filtering:** Use `data['conf'][i] > 0` to drop noise. For cleaner output, raise to `> 10` or `> 30` depending on image quality.

#### Strategy 2: Zoomed Crop for Missing Values

When OCR misses specific table cells (e.g., the "Result" column in a test report), crop the exact region, upscale 2-3x with NEAREST, apply high contrast (3-4x), binarize aggressively, and re-OCR:

```python
from PIL import ImageEnhance, ImageFilter

w, h = img.size
# Crop the results area specifically
crop = img.crop((int(w*0.15), int(h*0.45), int(w*0.85), int(h*0.65)))
# Upscale 2-3x with NEAREST to preserve pixel edges
crop = crop.resize((crop.width * 2, crop.height * 2), Image.NEAREST)
crop = crop.convert('L')
enhancer = ImageEnhance.Contrast(crop)
crop = enhancer.enhance(3.0)
# Aggressive binarization
crop = crop.point(lambda x: 0 if x < 120 else 255, '1')

text = pytesseract.image_to_string(crop, lang='eng', config='--oem 3 --psm 6')
```

**Parameter tuning:**
- **Crop region**: Start with `(0.15w, 0.45h, 0.85w, 0.65h)` and adjust based on where the table body sits in the page
- **Upscale factor**: 2x for most cases, 3x for very small text
- **Contrast enhancement**: 2.0-3.0 for moderate, 3.0-4.0 for very faint text
- **Binarization threshold**: 100-140 range; lower = more aggressive (captures faint text but more noise)
- **PSM**: 6 (uniform block) for table cells, 7 (single line) for one-line results

#### Strategy 3: Multiple PSM Mode Cross-Reference

Different PSM modes produce different results on the same image. Run 3-4 modes and cross-reference:

```python
for psm in [3, 6, 7, 11]:
    text = pytesseract.image_to_string(img, lang='eng',
        config=f'--oem 3 --psm {psm}')
    print(f"=== PSM {psm} ===\n{text}")
```

| PSM | Best for | Notes |
|-----|----------|-------|
| 3 | Default — general purpose | Fallback when others fail |
| 6 | Uniform block of text | Best for table bodies, single-column data |
| 7 | Single text line | Best for one-line results, headers |
| 11 | Sparse text | Best when table has many empty cells |
| 12 | Single block variable orient | Best for forms with mixed orientation |

#### Strategy 4: Manual Calculation of Derived Values

When OCR reads the raw data (loads, areas, dimensions) but misses the calculated average/result, compute it manually:

```python
# Example: Internal Bond Strength from load + area
loads = [2760, 2560, 2550]  # OCR'd from table
area = 2500                  # OCR'd from table
avg_bond = sum(loads) / len(loads) / area
print(f"Average: {avg_bond:.3f} N/mm² = {avg_bond*145.038:.1f} psi")
```

**Common derived values in material test reports:**
- **MOR** (Modulus of Rupture): `(3 * max_load * span) / (2 * width * thickness²)`
- **MOE** (Modulus of Elasticity): `(span³ * slope) / (4 * width * thickness³)`
- **Density**: `mass / volume`
- **Internal Bond**: `max_load / bond_area`
- **Moisture Content**: `((wet_mass - dry_mass) / dry_mass) * 100`

#### Strategy 5: Full Pipeline — Multi-Page Image-Based PDF with Tables

Combine all strategies for a complete extraction:

```python
import fitz, pytesseract
from PIL import Image, ImageEnhance
from collections import defaultdict
import io

doc = fitz.open("document.pdf")

for page_num in range(len(doc)):
    # 1. Render at 300 DPI
    pix = doc[page_num].get_pixmap(dpi=300)
    img = Image.open(io.BytesIO(pix.tobytes("png")))

    # 2. Try full-page OCR first
    text = pytesseract.image_to_string(img, lang='eng', config='--oem 3 --psm 6')
    print(f"=== Page {page_num+1} ===\n{text}")

    # 3. If table data is garbled, use TSV reconstruction
    data = pytesseract.image_to_data(img, lang='eng',
        config='--oem 3 --psm 6', output_type=pytesseract.Output.DICT)
    lines = defaultdict(list)
    for i in range(len(data['text'])):
        t = data['text'][i].strip()
        if t and data['conf'][i] > 0:
            key = (data['block_num'][i], data['line_num'][i])
            lines[key].append((data['left'][i], t))
    for key in sorted(lines.keys()):
        items = sorted(lines[key], key=lambda x: x[0])
        print(' | '.join(item[1] for item in items))

    # 4. For specific missing values, zoom crop + re-OCR
    # (see Strategy 2 above)
```

**Pitfalls:**
1. **TSV confidence filtering**: `data['conf'][i] > 0` includes very low-confidence noise. For cleaner output, raise to `> 10` or `> 30`. But be aware that some valid values (especially in scanned documents) have low confidence — cross-reference with the raw `image_to_string` output.
2. **Overlapping Arabic/English text**: When Arabic stamps overlap English table cells (common in Middle East inspection certs), OCR garbles both. The TSV approach helps by isolating spatial positions, but some cells will be unrecoverable. Note these as "partially obscured" in your output.
3. **NEAREST vs LANCZOS for upscaling**: Use `Image.NEAREST` (not LANCZOS/BILINEAR) when upscaling for OCR. Nearest-neighbor preserves hard character boundaries; interpolation blurs them.
4. **Binarization destroys thin text**: If the text is very thin (1-2px strokes), aggressive binarization can erase it entirely. Try a higher threshold (140-160) or skip binarization and rely on contrast enhancement alone.
5. **Page-by-page memory**: For multi-page documents (10+ pages), process one page at a time and save results incrementally. Don't hold all rendered images in memory.
6. **Verify with manual calculation**: When OCR reads raw data but misses the summary value, calculate it yourself. This also serves as a sanity check on the OCR'd values.

### Split, Merge & Search PDFs (pymupdf)

```python
# Split pages 1-5
doc = pymupdf.open("report.pdf")
new = pymupdf.open()
for i in range(5): new.insert_pdf(doc, from_page=i, to_page=i)
new.save("pages_1-5.pdf")

# Merge
result = pymupdf.open()
for path in ["a.pdf", "b.pdf"]: result.insert_pdf(pymupdf.open(path))
result.save("merged.pdf")

# Search text
for i, page in enumerate(doc):
    results = page.search_for("revenue")
    if results: print(f"Page {i+1}: {len(results)} match(es)")
```

### Arxiv Papers

```bash
web_extract(urls=["https://arxiv.org/abs/2402.03300"])    # Abstract
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])     # Full paper
```

## Large structured PDFs (books, standards, manuals)

For PDFs over ~50 pages (standards, textbooks, manuals), extract by **targeted page ranges** rather than the whole document:

```bash
# 1. Get the table of contents first
pdftotext -f 1 -l 20 "/path/to/book.pdf" /tmp/toc.txt

# 2. Read TOC to identify section page numbers
read_file(path="/tmp/toc.txt")

# 3. Extract each section by its page range
pdftotext -f 21 -l 60 "/path/to/book.pdf" /tmp/section1.txt
pdftotext -f 61 -l 130 "/path/to/book.pdf" /tmp/section2.txt

# 4. Find subsection boundaries within extracted text
grep -n "3\.4\|3\.5\|3\.6" /tmp/section1.txt

# 5. Read targeted chunks with offset/limit
read_file(path="/tmp/section1.txt", offset=401, limit=300)
```

**Handling PDF formatting artifacts:**
- `pdftotext` may produce **scrambled lettering in headers** (e.g. `STEWARDSHIP` → `STEWARDSHIP`) due to PDF text-positioning operators — ignore these, the body text is correct
- Form feed characters (`\f`) appear at page boundaries — strip with `sed 's/\f//g'`
- Running headers (book title, chapter name, page number) repeat on every page — filter with `grep -v` or skip known patterns

**PMBOK 7th Edition page map** (worked example in `references/pmbok-7th-ed-extraction.md`):
| Section | Pages |
|---------|-------|
| TOC / Front matter | 1-20 |
| System for Value Delivery | 2-20 |
| 12 Principles | 21-60 |
| 8 Performance Domains | 61-130 |
| Tailoring | 131-152 |
| Models, Methods, Artifacts | 153-196 |

## Setup

```bash
# Core tools
pip3 install pdfplumber openpyxl PyMuPDF   # system python3
brew install poppler tesseract             # pdftotext + OCR engine
brew install tesseract-lang                # Arabic + additional OCR languages

# Or inside a venv
python3 -m pip install pdfplumber openpyxl PyMuPDF
```

## PDF Reading Pattern

### Basic multi-page extraction

```python
import pdfplumber

pdf_path = "/path/to/register.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total Pages: {len(pdf.pages)}")
    for i, page in enumerate(pdf.pages):
        text = page.extract_text() or ""
        tables = page.extract_tables()
        print(f"\n{'='*80}")
        print(f"PAGE {i+1} — {len(tables)} table(s)")
        print(text[:2000])
        for t, table in enumerate(tables):
            for row in table[:5]:
                print(row)
```

### Image-based PDFs (no text layer — or partial text layer)

PDFs from Adobe Illustrator, InDesign, scanned documents, or **slide deck exports** (PowerPoint/Keynote → PDF) may have zero extractable text. **However, many "image-based" PDFs actually have partial text layers** — especially those created via PostScript → Acrobat Distiller (producer: `PScript5.dll Version 5.2.2` + `Acrobat Distiller`). These PDFs look like scanned images but contain hidden text that PyMuPDF can extract.

**Critical workflow: always try `page.get_text()` FIRST before falling back to OCR.** The text layer, even if garbled or incomplete, is often more reliable than tesseract on the same page.

```python
import fitz
doc = fitz.open(path)
for i, page in enumerate(doc):
    text = page.get_text()
    if text.strip():
        print(f"Page {i+1}: {len(text)} chars of text layer found")
        # Use this as primary source — supplement with OCR for missing pages
    else:
        print(f"Page {i+1}: no text layer — need OCR")
```

**Detection of PostScript/Distiller PDFs (partial text layer):**
```bash
pdfinfo "/path/to/file.pdf" | grep -i "producer"
# "PScript5.dll Version 5.2.2" + "Acrobat Distiller" → partial text layer likely
# "macOS" or "LibreOffice" → may have full text layer
# "Image Conversion Plug-in" → slide deck export, no text layer
```

**Workflow for mixed text-layer PDFs (most common in shop drawings):**
1. Extract text from ALL pages with `page.get_text()` in one pass
2. Pages with text → use as primary source (even if garbled)
3. Pages without text → render at 300 DPI + tesseract OCR
4. Cross-reference: OCR may catch things the text layer missed, and vice versa

Detect with PyMuPDF:

**Quick detection via pdfinfo:**
```bash
pdfinfo "/path/to/file.pdf" | grep -i "producer"
# If producer contains "Image Conversion Plug-in" → slide deck export, no text layer
# If producer contains "macOS" or "LibreOffice" → may have text layer
```

**Slide deck PDFs (PowerPoint/Keynote exports):** These are 39-page slide decks with decorative elements, partial text, and fragmented layout. OCR will produce usable but incomplete output — expect missing headers, garbled bullet points, and decorative text artifacts. **Always look for a companion text-based document** (overview PDF, published article, or web source) as the primary source. The slide deck is a visual reference, not a reliable text source.

```python
import fitz
doc = fitz.open(path)
for i, page in enumerate(doc):
    text = page.get_text()
    if not text.strip():
        print(f"Page {i+1}: no text layer — need OCR")
```

**Workflow — render to image + tesseract OCR:**

```python
import fitz
import subprocess

doc = fitz.open(path)
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=300)          # 300 DPI for decent OCR
    png_path = f"/tmp/page_{i}.png"
    pix.save(png_path)

    # OCR with tesseract (supports Arabic + English)
    result = subprocess.run(
        ["tesseract", png_path, "stdout", "-l", "eng+ara"],
        capture_output=True, text=True, timeout=60
    )
    print(f"--- Page {i+1} ---")
    print(result.stdout or "[no text detected]")
```

**Pitfalls:**
- Tesseract may fail to open files saved under `/tmp` due to filesystem isolation in sandboxed environments. Save the rendered PNG in the current working directory instead.
- Adobe Illustrator PDFs often contain only vector graphics, not embedded raster images. `get_pixmap(dpi=300)` renders the vector page to a raster image first — this is the correct approach.
- For large multi-page image PDFs (scanned drawings, specification books), process page-by-page to avoid memory bloat.
- Install tesseract with Arabic language pack: `brew install tesseract tesseract-lang` (macOS) or `apt install tesseract-ocr tesseract-ocr-ara` (Linux).

### Register with mirrored/duplicate pages

Many BIM register PDFs are Excel-to-PDF exports that repeat header rows on every printed page. The result: pages 2–7 may all show the same header, then page 8 starts fresh. When scanning:

1. Read all pages with `pdfplumber`
2. Deduplicate by comparing first N chars of extracted text
3. Keep only the first occurrence of each unique section header block

```python
# Deduplicate mirrored pages
seen_headers = set()
unique_pages = []
for page in pdf.pages:
    text = page.extract_text() or ""
    header = text[:200]  # first 200 chars as signature
    if header not in seen_headers:
        seen_headers.add(header)
        unique_pages.append(page)
```

### RTL Arabic text handling

Arabic text in PDFs comes out mirrored or with RTL glyphs. For register extraction:
- Use `pdfplumber` raw text — it preserves Arabic unicode
- Do NOT try to reverse or flip — just capture as-is
- When displaying to user, note "Arabic text appears as extracted from PDF"
- When searching, use Arabic keywords directly

```python
# Search for Arabic text
arabic_query = "عورشملل"
for page in pdf.pages:
    text = page.extract_text() or ""
    if arabic_query in text:
        print(f"Found on page {page.page_number}")
```

### Multi-section registers (8 log types in one PDF)

Aseer-style registers pack 8 log types into a single PDF, each section starting on a new page. Pattern:

```
Pages 2-7   → Material Submittal Log (with status codes A/B/C/D/E/F/U)
Pages 8-10  → SNA (Start New Activity)
Pages 11+   → Shop Drawings, Method Statements, RFI Log, SI Log, NCR Log, Correspondence
```

Scan for section headers first:

```python
SECTION_KEYWORDS = {
    "Material Submittal": ["MATERIAL SUBMITTAL LOG", "Material Submittal Log"],
    "SNA": ["Start New Activity", "SNA"],
    "RFI": ["REQUEST FOR INFORMATION", "RFI Log"],
    "Site Instruction": ["Site Instruction LOG", "SITE INSTRUCTION LOG"],
    "NCR": ["Non-Conformance Report LOG", "NON-CONFORMANCE REPORT LOG"],
    "Outgoing Correspondence": ["OUTGOING CORRESPONDENCE", "Outgoing Correspondence"],
    "Incoming Correspondence": ["INCOMING CORRESPONDENCE", "Incoming Correspondence"],
}

def classify_page(text):
    for section, keywords in SECTION_KEYWORDS.items():
        if any(kw.upper() in text.upper() for kw in keywords):
            return section
    return "Unknown"
```

## Bulk Directory Processing

When a directory contains **mixed document types** (some text-based PDFs, some scanned images, some already images), process them all with a single script:

### Workflow

1. **Inventory** — list all files, classify by extension and content type
2. **Test for text layer** — try `pdftotext` or `pymupdf` first; if empty, fall back to OCR
3. **Convert scanned PDFs** to images via `pdftoppm`
4. **Resize images** (optional, for speed) via `magick`
5. **OCR** all images with tesseract
6. **Compile** into structured summaries

### Example: Process a directory with mixed file types

```bash
# === STEP 1: Inventory ===
DIR="/path/to/document/folder"
mkdir -p output/text output/ocr output/summaries

for f in "$DIR"/*.pdf; do
  base=$(basename "$f" .pdf)
  echo "=== Processing: $base ==="

  # === STEP 2: Try text extraction first ===
  text=$(pdftotext -layout "$f" - 2>/dev/null | head -c 500)
  if [ -n "${text// }" ]; then
    # Text-based PDF — extract full text
    pdftotext -layout "$f" "output/text/${base}.txt"
    echo "  ✓ Text-based PDF, extracted to output/text/"
  else
    # === STEP 3: Scanned PDF — convert to images ===
    echo "  ⚠ Image-based PDF, converting to pages..."
    pdftoppm -jpeg -r 200 "$f" "output/ocr/${base}_page"

    # === STEP 4: Resize for faster OCR ===
    mkdir -p "output/ocr/${base}_small"
    for page in "output/ocr/${base}_page"*.jpg; do
      p=$(basename "$page")
      magick "$page" -resize 1200x -quality 75 "output/ocr/${base}_small/$p"
    done

    # === STEP 5: OCR each page ===
    for page in "output/ocr/${base}_small/"*.jpg; do
      pname=$(basename "$page" .jpg)
      tesseract "$page" "output/ocr/${pname}" -l ara 2>/dev/null
    done
  fi
done

# === STEP 5b: OCR native images (JPG/JPEG/PNG) ===
for img in "$DIR"/*.{jpg,jpeg,png,JPG,JPEG,PNG}; do
  [ -f "$img" ] || continue
  base=$(basename "$img")
  magick "$img" -resize 1200x -quality 75 "output/ocr/${base}_small.jpg"
  tesseract "output/ocr/${base}_small.jpg" "output/ocr/${base}" -l ara 2>/dev/null
  echo "  ✓ OCR'd image: $base"
done
```

### Python version (more control)

```python
import subprocess, os, glob
from pathlib import Path

DIR = "/path/to/documents"
out = Path("output")
(out / "text").mkdir(parents=True, exist_ok=True)
(out / "ocr").mkdir(parents=True, exist_ok=True)

for pdf_path in glob.glob(f"{DIR}/*.pdf"):
    base = Path(pdf_path).stem
    print(f"=== {base} ===")

    # Try text extraction first
    result = subprocess.run(
        ["pdftotext", "-layout", pdf_path, "-"],
        capture_output=True, text=True, timeout=30
    )
    text = result.stdout.strip()

    if len(text) > 100:  # has real text content
        (out / "text" / f"{base}.txt").write_text(result.stdout)
        print(f"  Text: {len(text)} chars")
    else:
        # Scanned — convert to images via pdftoppm
        subprocess.run(
            ["pdftoppm", "-jpeg", "-r", "200", pdf_path,
             str(out / "ocr" / f"{base}_page")],
            check=True, timeout=60
        )
        print("  Scanned PDF → images")

        # Resize and OCR each page
        for img in sorted(glob.glob(str(out / "ocr" / f"{base}_page*.jpg"))):
            small = img.replace(".jpg", "_small.jpg")
            subprocess.run(
                ["magick", img, "-resize", "1200x", "-quality", "75", small],
                check=True
            )
            txt_out = Path(img).with_suffix("")
            subprocess.run(
                ["tesseract", small, str(txt_out), "-l", "ara"],
                check=True
            )
            print(f"  OCR'd: {Path(img).name}")
```

### Documentation of results

After bulk processing, create a **document inventory table** showing what was processed:

| File | Type | Method | Quality | Extracted Content |
|------|------|--------|---------|-------------------|
| contract.pdf | PDF (scanned) | pdftoppm → tesseract | Fair | Contract terms, parties, clauses |
| statement.pdf | PDF (text) | pdftotext | Excellent | Full table data with amounts |
| receipt.jpg | JPG | tesseract | Fair | Amount and date readable |

Also create a **processing notes section** documenting:
- Methods used per file type
- Quality assessment per document
- Known limitations (poor OCR areas, garbled numbers)
- Any files that failed or had very poor extraction

### Structured Summary Output

After extracting content from all documents, organize the results into **categorized markdown files** rather than one monolithic output. This creates a browsable document library.

#### Categorization pattern

Group documents by functional type, not by file extension:

| Category | Example Sources | Output File |
|----------|----------------|-------------|
| **Contracts** | Signed agreements, SOWs, MOUs | `contract_summary.md` |
| **Financial/BOQ** | Estimates, quotations, budgets | `boq_estimate.md` |
| **Statements** | Bank statements, account histories | `account_statements.md` |
| **Receipts** | Payment proofs, transfer confirmations | `payment_receipts.md` |
| **Contractor Quotes** | Subcontractor bids, material quotes | `contractor_quotations.md` |
| **Correspondence** | Letters, emails, memos | `correspondence.md` |
| **Technical** | Drawings, specs, method statements | `technical_docs.md` |

#### Per-document structure

Each document inside a summary file should have:

```markdown
## [Document Title]

| Field | Details |
|-------|---------|
| **File** | filename.pdf |
| **Size** | 147 KB |
| **Pages** | 1 |
| **Language** | Arabic |

### Content Summary

[Key extracted data in structured format — tables for tabular data,
paragraphs for prose, bullet lists for itemized content]

### Key Values (if financial)

| Item | Amount (EGP) |
|------|:-----------:|
| Total | 366,894 |
| Balance | -4,142 |

### Notes
- OCR quality assessment
- Known limitations
- Cross-references to related documents
```

#### Cross-document synthesis

When financial documents interact (e.g., receipts + account statements), verify consistency:

```markdown
### Cross-Reference Check

| Receipt | Amount | Statement Entry | Match? |
|---------|:------:|:--------------:|:------:|
| دفعة 2A + 2B | 100,000 | Cert 3005: 100,000 (10/04) | ✅ |
| دفعة 3 | 50,000 | Cert 3022: 50,000 (21/05) | ✅ |
```

#### Document inventory master file

Create a `document_inventory.md` that serves as the index, containing:
- Table of all documents with file name, type, size, and category
- Processing methods used per file
- Quality assessment per file
- Storage layout showing directory tree
- Key findings summary (total amounts, date ranges, key parties)

## OneDrive-locked PDFs

BIM registers often live as `.xlsb` files or PDFs on OneDrive. They are **unreadable by any tool** from the terminal because the OneDrive sync engine holds a file lock.

**Tools that ALL fail with `Resource deadlock avoided` on locked OneDrive files:**
- `pdftotext` (poppler) — returns 0 bytes, stderr: `Couldn't find trailer dictionary`
- `pdfminer.high_level.extract_text` — raises `OSError: [Errno 11] Resource deadlock avoided`
- `pdfplumber` — raises `[Errno 11] Resource deadlock avoided`
- `PyMuPDF (fitz)` — raises `Failed to open file`
- `python-docx` — raises `OSError: [Errno 11] Resource deadlock avoided`
- `textutil` (macOS) — returns `The file couldn't be opened`
- `shutil.copy2`, `cp`, `cat`, `head`, `file` — all fail with `Resource deadlock avoided`
- `zipfile.ZipFile` (Python stdlib) — may bypass the lock for DOCX files (lower-level I/O path), but still fails for PDFs

**There is no partial-read workaround for dataless OneDrive placeholders.** The lock is at the macOS VFS layer, not at the application level.

### Fallback: find alternative copies outside OneDrive

When OneDrive files are locked, search for alternative copies in git repos, desktop folders, and email attachment caches:

```bash
# Search for alternative copies outside OneDrive
find /Users/mohamedessa -maxdepth 5 -name "*keyword*" 2>/dev/null | grep -v "CloudStorage" | grep -v "Library"

# Common fallback locations for Aseer Museum project:
# - /Users/mohamedessa/aseer-museum-pm/03_Scope/   (scope documents)
# - /Users/mohamedessa/aseer-museum-pm/00_Contracts/ (contract indices)
# - /Users/mohamedessa/Desktop/Work_Projects/Asher_Regional_Museum_Emails/Attachments/ (email attachments)
```

**Pattern:** The `aseer-museum-pm` git repo often has README.md files, analysis reports, and extracted PDFs that serve as fallback sources when OneDrive originals are locked. Check `03_Scope/<Vendor>/` and `99_Archive/09_Procurement_Management/Contracts/` for alternative copies.

rather than one monolithic output. This creates a browsable document library.

### Categorization pattern

Group documents by functional type, not by file extension:

| Category | Example Sources | Output File |
|----------|----------------|-------------|
| **Contracts** | Signed agreements, SOWs, MOUs | `contract_summary.md` |
| **Financial/BOQ** | Estimates, quotations, budgets | `boq_estimate.md` |
| **Statements** | Bank statements, account histories | `account_statements.md` |
| **Receipts** | Payment proofs, transfer confirmations | `payment_receipts.md` |
| **Contractor Quotes** | Subcontractor bids, material quotes | `contractor_quotations.md` |
| **Correspondence** | Letters, emails, memos | `correspondence.md` |
| **Technical** | Drawings, specs, method statements | `technical_docs.md` |

### Per-document structure

Each document inside a summary file should have:

```markdown
## [Document Title]

| Field | Details |
|-------|---------|
| **File** | filename.pdf |
| **Size** | 147 KB |
| **Pages** | 1 |
| **Language** | Arabic |

### Content Summary

[Key extracted data in structured format — tables for tabular data, 
paragraphs for prose, bullet lists for itemized content]

### Key Values (if financial)

| Item | Amount (EGP) |
|------|:-----------:|
| Total | 366,894 |
| Balance | -4,142 |

### Notes
- OCR quality assessment
- Known limitations
- Cross-references to related documents
```

### Cross-document synthesis

When financial documents interact (e.g., receipts + account statements), verify consistency:

```markdown
### Cross-Reference Check

| Receipt | Amount | Statement Entry | Match? |
|---------|:------:|:--------------:|:------:|
| دفعة 2A + 2B | 100,000 | Cert 3005: 100,000 (10/04) | ✅ |
| دفعة 3 | 50,000 | Cert 3022: 50,000 (21/05) | ✅ |
```

### Document inventory master file

Create a `document_inventory.md` that serves as the index, containing:
- Table of all documents with file name, type, size, and category
- Processing methods used per file
- Quality assessment per file
- Storage layout showing directory tree
- Key findings summary (total amounts, date ranges, key parties)

Same `Resource deadlock avoided` symptom as PDFs, with an extra twist: the `.md` companion files (created by DOCX-to-MD conversion tools) can have `com.apple.provenance` extended attributes making them appear as file-sized-but-empty stubs.

**Detection — check xattr before assuming the file is empty:**

```bash
xattr -l /path/to/file.md
# → com.apple.provenance (binary data) = OneDrive placeholder, not a real empty file
```

A `.md` file showing `file_size > 0` but `read_file` returning 0 lines is NOT necessarily empty — it may be a OneDrive placeholder that hasn't hydrated. The `com.apple.provenance` xattr is the signal.

**Primary workaround — extract from the sibling DOCX via zipfile:**

`python-docx` (which calls `open()` at the OS level) may also fail with `Resource deadlock avoided` on locked OneDrive paths. However, Python's `zipfile.ZipFile` stdlib module uses a lower-level I/O path that **sometimes bypasses the OneDrive lock** on macOS, allowing direct extraction of the DOCX internals.

```python
import zipfile, re

path = '/path/to/locked.docx'
with zipfile.ZipFile(path) as z:
    # Verify the internal structure
    for name in z.namelist():
        if 'document' in name.lower():
            print(f'{name}: {z.getinfo(name).file_size} bytes')

    # Read the main document XML
    xml_content = z.read('word/document.xml').decode('utf-8', errors='replace')

    # Strip XML tags to extract text
    text = re.sub(r'<[^>]+>', ' ', xml_content)
    text = re.sub(r'\s+', ' ', text).strip()

    # Check for key content
    if text:
        print(f'Extracted {len(text)} characters')
        # Use grep-like extraction for specific sections:
        if 'TBD' in text:
            for chunk in text.split('TBD'):
                # Show context around each TBD
                print(f'...TBD context: ...{chunk[-100:]}')
```

**Limitations:**
- This bypass works for DOCX but may fail on other zip-based formats (`.pptx`, `.xlsx`) — the lock affects different file extensions differently
- The extracted text has no table structure (XML tags are stripped uniformly) — for tables, use `python-docx` if the file IS readable, fall back to zipfile only when it isn't
- Still subject to macOS sandboxing: `head`, `cat`, `file` all fail — only `zipfile.open()` via Python may work

**Secondary workaround — hydrate via `open` then extract:**

Same pattern as OneDrive-locked PDFs — trigger OneDrive to download the real file:

```bash
open "/path/to/locked.docx"    # Opens in Word/LibreOffice, triggers hydration
sleep 15                       # Wait for download
ls -laO "/path/to/locked.docx" # Verify dataless flag is gone
# Then use python-docx normally
```

**If both fail — the .docx itself is a stale stub:** Check the `brctl status` diagnostic (see `macos-onedrive-recovery` skill) and fall back to working-copy paths on Micro volume or git repo.

## OneDrive Path-Too-Long Sync Error

OneDrive on macOS has a ~260-character path limit (inherited from Windows NTFS). When a file or folder name is excessively long — common with Alibaba product page downloads, deeply nested folder structures, or auto-generated filenames — OneDrive shows the error:

> "We can't sync this item because the path is too long"

The error dialog shows the truncated path. The file exists locally but OneDrive refuses to sync it.

### Detection

```bash
# Find files/folders with long paths in a OneDrive directory
find ~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/ -maxdepth 8 -type d -name "*Alibaba*" -o -name "*alibaba*" 2>/dev/null
```

The most common cause: downloading an Alibaba product page (HTML + `_files` folder) which generates a filename like:
```
Active Microclimate Generator For Museum Display Cases - Buy Microclimate Generator active Microclimate Generator microclimate Generator For Museum Display Cases Product on Alibaba.com
```

### Fix

Rename both the folder and the HTML file to short names:

```bash
cd ~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/.../target_directory/

# Rename the _files folder
mv "Long Product Name - Buy Product active Product Product For Product on Alibaba.com_files" "ShortName_files"

# Rename the HTML file
mv "Long Product Name - Buy Product active Product Product For Product on Alibaba.com.html" "ShortName.html"
```

### Prevention

- When downloading product pages from Alibaba or similar sites, save to `/tmp/` first, then rename before moving to OneDrive
- Check path length before moving: `echo $PATH | wc -c`
- Keep folder names under 50 characters in deep OneDrive trees

### Pitfalls

1. **The `_files` folder and `.html` file must both be renamed** — OneDrive tracks the pair. Renaming only one leaves a dangling reference.
2. **The folder may contain hundreds of items** (images, CSS, JS) — `mv` on the folder renames the whole tree, no need to touch individual files.
3. **OneDrive may take minutes to notice the rename** — the error dialog may persist briefly. Check OneDrive icon in menu bar for sync status.
4. **Other long paths in the same directory** — after fixing one, check for others with `find ... -maxdepth 1 -type d | awk 'length>80'`

## OneDrive 4-byte stub files

A distinct failure mode from `compressed,dataless`: some OneDrive cloud-only files are **4-byte text files containing `"null"`** — placeholders for files that were never synced locally.

**Symptom**: `file` reports "ASCII text" (not PDF/XLSX). Size is exactly 4 bytes. Contents are literally `null`.

**Cause**: OneDrive creates these stubs when files exist in the cloud but haven't been requested locally. They are not real placeholders — they are essentially empty.

**Workaround**:
1. Trigger sync via Finder: navigate to the file and double-click to open it. OneDrive will download the real file from cloud.
2. Or check the source email that contained the attachment — the attachment may still be in the email server and needs extraction.
3. Or force OneDrive to sync: right-click OneDrive icon in menu bar → "Sync files" → wait for download.
4. Verify with: `ls -laO /path/to/file` — after download, the expected file size appears and the file type matches the extension.

**Detection script:**
```bash
# Find all OneDrive stub files (4-byte null) in a directory
find /path/to/search -size 4c -exec sh -c \
  'test "$(cat "$1")" = "null" && echo "STUB: $1"' _ {} \;
```

## Extracting PDFs from Outlook attachment cache

When quotation PDFs exist as OneDrive stubs (4-byte "null" files) and the source email is in Outlook but the attachment hasn't been downloaded, the `.olk15MsgAttachment` files in Outlook's data directory often contain the actual data.

**Discovery workflow:**

```bash
DB=~/Library/Group\ Containers/UBF8T346G9.Office/Outlook/Outlook\ 15\ Profiles/Main\ Profile/Data/Outlook.sqlite

# 1. Find the email with attachment
sqlite3 "$DB" "SELECT Record_RecordID, Message_TimeSent, Message_NormalizedSubject \
  FROM Mail \
  WHERE Message_NormalizedSubject LIKE '%Faro Focus%' AND Message_HasAttachment=1 \
  ORDER BY Message_TimeSent DESC;"

# 2. Find the attachment blocks (RecordID 35182 example)
sqlite3 "$DB" "SELECT hex(m.BlockID), m.BlockTag, b.PathToDataFile \
  FROM Mail_OwnedBlocks m JOIN Blocks b ON b.BlockID = m.BlockID \
  WHERE m.Record_RecordID=35182 ORDER BY m.BlockTag;"

# 3. PathToDataFile gives the .olk15MsgAttachment path under the Data dir
```

**Extraction pattern:**

`.olk15MsgAttachment` files have this structure:
- **512-byte header** (starts with `d00d000001000000...`, contains MIME metadata like `Content-type: application/pdf; name="..."`)
- **Base64-encoded content** starting at offset ~285+ with `JVBER...` for PDFs

```python
import base64, re

with open('file.olk15MsgAttachment', 'rb') as f:
    data = f.read()

# Find base64 PDF marker
idx = data.find(b'JVBER')
if idx >= 0:
    b64_text = data[idx:].decode('ascii', errors='ignore')
    b64_clean = re.sub(r'[^A-Za-z0-9+/=]', '', b64_text)
    pdf_data = base64.b64decode(b64_clean)
    with open('output.pdf', 'wb') as out:
        out.write(pdf_data)
```

**Identifying attachments:**
- `strings` on the `.olk15MsgAttachment` file reveals the original filename in `name="..."` 
- Each block corresponds to one attachment (PDF, image, etc.)
- RecordID → folder mapping for Message Sources/ and Message Attachments/: `folder = RecordID // 1000`

## Extracting pricing data from quotation PDFs

```python
import subprocess, re
# Extract all text
result = subprocess.run(["pdftotext", "/path/to/quote.pdf", "-"],
    capture_output=True, text=True, timeout=30)
text = result.stdout

# Extract pricing patterns
prices = re.findall(r'\$\s*[\d,]+\.?\d*', text)
# → ['$31,000.00', '$3,300.00', '$800.00', ...]

# Find total
total_match = re.search(r'Total.*?\$\s*([\d,]+\.?\d*)', text)
if total_match:
    total = total_match.group(1)  # '35,000.00'

# Find item descriptions
lines = text.split('\n')
for i, line in enumerate(lines):
    if re.search(r'\$\s*[\d,]+\.?\d*', line):
        desc = lines[i-1] if i > 0 else ''
        price = re.search(r'\$\s*([\d,]+\.?\d*)', line).group(1)
        print(f"{desc.strip()} → ${price}")
```

## OneDrive-locked Excel files (.xlsb)

BIM registers often live as `.xlsb` files on OneDrive. They are **unreadable by any tool** from the terminal because the OneDrive sync engine holds a file lock.

**Symptom**: `Resource deadlock avoided` — every syscall (read, copy, stat) fails.

**Solution — Excel conversion only**:
```python
import subprocess

# Open in Excel via AppleScript, save as .xlsx
script = '''
tell application "Microsoft Excel"
    activate
    open "/path/to/Live Register Log.xlsb"
    delay 5
    save active workbook in "/tmp/Live_Register_Log.xlsx" as Excel workbook
    delay 1
    close active workbook
    quit
end tell
'''
with open("/tmp/convert.scpt", "w") as f:
    f.write(script)
subprocess.run(["osascript", "/tmp/convert.scpt"], timeout=60)
```

Or via `open` CLI:
```bash
open -a "Microsoft Excel" "/path/to/file.xlsb"
# Then user must File → Save As .xlsx manually
```

After conversion, read with openpyxl:
```python
import openpyxl
wb = openpyxl.load_workbook("/tmp/file.xlsx", read_only=True, data_only=True)
ws = wb.active
headers = next(ws.iter_rows(min_row=1, max_row=1, values_only=True))
```

## Project Schedule / Gantt Chart Extraction

Extract structured schedule data from project Gantt chart PDFs (e.g. Moharram Bakhoum, Primavera P6 exports, MS Project printed views). These are common in BIM/construction projects.

### Detection

Schedule PDFs have:
- Columns: Activity ID, Activity Name, Original Duration, Start, Finish, Total Float
- Gantt bar graphics (not real tables — cell-based extraction won't work)
- Bilingual headers (Arabic project name + English activity descriptions)
- Hierarchical WBS grouping (phases → sub-phases → leaf activities)
- Milestones with 0 duration
- Float values that indicate critical path (negative values)

### OCR Pipeline

These PDFs are typically vector-based (exported from P6/MS Project) with no embedded text layer. The working pipeline:

```python
import pymupdf, pytesseract, io, json
from PIL import Image

path = "/path/to/schedule.pdf"
doc = pymupdf.open(path)

all_pages = []
for i in range(len(doc)):
    pix = doc[i].get_pixmap(dpi=200)           # 200 DPI minimum for Gantt bar text
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    text = pytesseract.image_to_string(img, lang='ara+eng')
    all_pages.append({"page": i+1, "text": text})
    print(f"Page {i+1}: {len(text)} chars")

# Save for structured extraction
with open("/tmp/ocr_output.json", "w") as f:
    json.dump(all_pages, f)
```

**Key parameters:**
- `dpi=200` — 150 misses small text in dense Gantt charts; 300 is slower but safer for very small font sizes
- `lang='ara+eng'` — required for bilingual Saudi/Egypt project documents
- Process all pages in one pass, then structure after

### Structured Data Extraction

After OCR, extract activity records from the garbled Gantt output:

**Get all OCR text first:**
```python
for p in all_pages:
    print(f"\n=== Page {p['page']} ===")
    print(p['text'])
```

**Search for specific sections (keywords by discipline):**
```python
for p in all_pages:
    text_lower = p["text"].lower()
    if any(kw in text_lower for kw in ["structural", "architectural", "electrical",
                                        "mechanical", "specialized", "showcase",
                                        "av hardware", "graphic design"]):
        print(f"\nPAGE {p['page']}")
        print(p["text"])
```

### WBS Hierarchy Reconstruction

Schedule PDFs group activities hierarchically. The OCR output is flat — reconstruct the tree using indentation cues and phase headers visible in the Gantt:

**Pattern — phases render as summary bars with children indented:**
```
PHASE 1: PRELIMINARIES (30d: Dec 25 → Jan 26)
  ├─ 1.1 PERMIT
  │   MB1020 │ Issuing a Permit for Renovations
  │   MB1050 │ Issuance of Permits from Municipality
  └─ 1.2 MOBILIZATION
      MB1010 │ Mobilization Plan Drawing
```

**Typical WBS levels in a museum/schedule:**
| Level | Description | Example |
|-------|-------------|---------|
| L1 | Project Phase | Engineering (216d) |
| L2 | Discipline Group | Technical Design (50%) |
| L3 | Work Package | Structural (22d) |
| L4 | Sub-Package | Preparation & Submittal (16d) |
| L5 | Activity | A1480: Prep Structural Design 50% (5d) |

### Float Analysis for Critical Path

Total Float values are critical schedule indicators:

| Float Value | Meaning |
|-------------|---------|
| **Negative (-5 to -35)** | Behind schedule / compressed — these drive the critical path |
| **Zero (0)** | Critical path activities |
| **Positive (3-22)** | Slack available |
| **Very high (83-200)** | Significant slack — often early-start items waiting on later phases |

**Pitfall:** Float values may be computed against a baseline different from the displayed dates. Cross-reference with the project start/finish milestones.

### Relationship / Dependency Inference

From the sequencing of activities and float values, infer these standard relationships:

| Pattern | Relationship |
|----------|-------------|
| Assessment → Approval → Design | Finish-to-Start (sequential stage-gate) |
| 50% Design → 90% Design → 100% IFC | Stage-gate progression |
| Design → BIM Model → Clash Detection | Design-complete before federated model |
| BIM/Design Approval → Fabrication Drawings | Approval gates fabrication |
| Material Submittal Approval → Purchase Order | Approval gates procurement |
| Material Submittal (all disciplines) → same approval date window | Convergent bottleneck |

**Parallel discipline tracks** (run concurrently, need cross-discipline coordination):
```
Dec 25  Jan 26  Feb 26  Mar 26
██████████████████           Structural
██████████████████           Architectural
██████████████████           Electrical
██████████████████           Mechanical
████████████████████████     Specialized Designs
```

### Gantt-to-Schedule Summary Format

When presenting extracted schedule data, use this structure:

```
PHASE: Preliminaries (30d)
  ├─ PERMIT: MB1020, MB1050
  └─ MOBILIZATION: MB1010 → MB1030 → MB1040

PHASE: Engineering (216d)
  ├─ 2.1 Assessment & Survey (51d)
  │   ├─ Site Surveys, BIM Existing, Cloud Survey
  │   ├─ Architectural & Structural Assessment
  │   └─ MEP Assessments (HVAC, BMS, Fire, Elec, Plumb)
  ├─ 2.2 Technical Design 50% (70d)
  │   ├─ Structural | Architectural | Electrical | Mechanical
  │   └─ Specialized: AV, Graphics, Lighting, Showcase
  ├─ 2.3 Technical Design 90% (88d)
  │   ├─ All disciplines + Specialized 90%
  │   └─ BIM 90% + Clash Detection
  └─ 2.4 IFC 100% (27d)
      └─ Final Design Package + Final Federated BIM

PHASE: Procurement
  ├─ Subcontractor Assessments
  ├─ Material Submittals (80+ items across 5 categories)
  └─ PO → Delivery → Construction

PHASE: Construction → T&C → Handover
```

### Timelines Overview

Render a compact timeline showing phase overlap:

```
Dec'25 Jan'26 Feb'26 Mar'26 Apr'26 May'26 Jun'26 Jul'26 Aug'26 Sep'26
 │      │      │      │      │      │      │      │      │      │
PRELIMS  ████████
ASSESS   ████████████
50% DES  ████████████████████
90% DES  ───████████████████████████
100% IFC ───────────────█████████
FAB DRW  ────────────────────███
PROCURE  ◇───MatSub──◇PO────◇Delv
AS-BUILD ─────────────────────────██████████
CONSTR   ──────────────────────────────────██
T&C      ────────────────────────────────────◇
 │      │      │      │      │      │      │      │      │      │
```

## Status Code Reference (Aseer-style)

| Code | Meaning |
|------|---------|
| A | Approved |
| B | Approved With Comments |
| C | Revise and Resubmit |
| D | Rejected |
| E | Not Required |
| F | For Information |
| U | Under Review |

## CAD-Generated Interior Design PDFs (BMA / Boris Micka Associates pattern)

Design PDFs exported from AutoCAD/Vectorworks by scenographers (BMA, Boris Micka Associates) are **not** MEP engineering documents. Extracted text reveals:

- Sheet indexes with drawing codes (e.g., `S.CF.ID.01` = Supporting, Café, Interior Design, Sheet 01)
- Fixture legends (outlet types, diffuser types, detector types)
- Room dimensions and finish schedules
- Construction notes about demolition/finishes

**Critical disclaimer** — always search extracted text for this language pattern BEFORE answering MEP questions from these PDFs:

> "These drawings are for indicative and notional purposes only, showing hypothetical locations of MEP services. Refer to MEP documentation for final locations and routing of all MEP elements shown."
> "This document section only includes remaining MEP elements and modifications proposed to the existing MEP equipment."
> "Refer to Package [Lighting/Audiovisual Hardware/Power supply] for details on [system] power supply."

**Implication for RFI cross-referencing**: Use a 3-tier answer matrix (CONFIRMED / PARTIAL / NOT IN SCOPE) when answering construction RFIs from these documents:

| Tier | Criteria | Example |
|------|----------|---------|
| CONFIRMED | Fixture legend + spec explicitly stated | "13A 2-gang switched socket outlet shown on S.ZZ.CS.11" |
| PARTIAL | Symbol/legend exists but placement is graphical | "DB symbol in legend but actual location is graphical only" |
| NOT IN SCOPE | Building infrastructure, rooms not in interior design set | "No electrical rooms, AHU rooms, or UPS rooms shown" |

**BMA document structure** — drawing codes follow `GROUP.ZONE.PACKAGE.SEQUENCE`:
- Group: S (Supporting) or E (Exhibition)
- Zone: CF (Café), FL (Female Lounge), SM (Studio/Meeting), LB (Library), MJ (Majlis), FY (Foyer), BR (Break), CA (Central), ZZ (General)
- Package: CS (Current State), CR (Construction Requirements), ID (Interior Design), DT (Details), LI (Lighting)

See `references/bma-cad-pdf-extraction.md` for full fixture legend libraries and the 27-question RCRC worked example.

## DOCX to Markdown Conversion (Complex Documents)

For DOCX files with many tables (BEPs, PEPs, plans with 50+ tables), `pandoc -t markdown` mangles table structure. Use `python-docx` with body-element iteration to preserve table placement relative to text:

```python
from docx import Document
from docx.oxml.ns import qn
import re

doc = Document('input.docx')

def get_table_md(table):
    rows = []
    for row in table.rows:
        cells = [cell.text.strip().replace('\n', ' ').replace('|', ' / ') for cell in row.cells]
        rows.append(cells)
    if not rows: return ''
    max_cols = max(len(r) for r in rows)
    for r in rows:
        while len(r) < max_cols: r.append('')
    lines = ['| ' + ' | '.join(rows[0]) + ' |']
    lines.append('|' + '|'.join(['---'] * max_cols) + '|')
    for row in rows[1:]:
        lines.append('| ' + ' | '.join(row) + ' |')
    return '\n'.join(lines)

def para_to_md(para):
    style = para.style.name
    text = para.text.strip()
    if not text: return ''
    formatted = ''
    for run in para.runs:
        rt = run.text
        if not rt: continue
        if run.bold and run.italic: rt = f'***{rt}***'
        elif run.bold: rt = f'**{rt}**'
        elif run.italic: rt = f'*{rt}*'
        formatted += rt
    if not formatted: formatted = text
    if 'Heading 1' in style: return f'\n## {formatted}\n'
    elif 'Heading 2' in style: return f'\n### {formatted}\n'
    elif 'Heading 3' in style: return f'\n#### {formatted}\n'
    elif 'List Paragraph' in style:
        pPr = para._element.find(qn('w:pPr'))
        indent = 0
        if pPr is not None:
            ind = pPr.find(qn('w:ind'))
            if ind is not None:
                left = ind.get(qn('w:left'))
                if left: indent = int(left) // 720
        return '  ' * indent + '- ' + formatted
    return formatted

# Iterate body elements in document order (preserves table placement)
body = doc.element.body
md_parts = []
for element in body:
    if element.tag == qn('w:p'):
        for p in doc.paragraphs:
            if p._element is element:
                md = para_to_md(p)
                if md: md_parts.append(md)
                break
    elif element.tag == qn('w:tbl'):
        for t in doc.tables:
            if t._element is element:
                table_md = get_table_md(t)
                if table_md: md_parts.append('\n' + table_md + '\n')
                break

full_md = '\n'.join(md_parts)
full_md = re.sub(r'\n{4,}', '\n\n\n', full_md).strip() + '\n'
```

**Key:** Iterate `doc.element.body` in document order, not `doc.paragraphs` + `doc.tables` separately — the latter loses relative positioning.

**Pitfall:** `pandoc -t markdown` produces cleaner prose but mangles complex tables (merged cells, multi-row headers). For 50+ table documents, always use `python-docx`.

## Pitfalls

1. **Double extension files**: PDFs exported from Excel often get `.pdf.pdf` extension. Handle gracefully.
1. **`pdftotext scrambled headers`**: PDF text-positioning operators (kerning, letter-spacing) cause `pdftotext` to produce garbled headers like `STEWARDSHIP` → `STEWARDSHIP`. The body text is correct — ignore header artifacts and read the paragraph content.
1. **`search_files` timeouts in large directory trees**: When `search_files` (ripgrep-backed) takes >60s and returns `[Command timed out after 60s]`, the directory tree is too large. Narrow scope: target specific subdirectories (`path` parameter), limit depth with `find -maxdepth` in terminal, or search by date/extension first.
1. **Cross-referencing Outlook DB for missing attachments**: When quotation PDFs are cloud-only stubs with no local copy, check the Outlook SQLite `Mail` table for emails matching the subject (e.g. `Message_NormalizedSubject LIKE '%scanner%'`). Attachments may still be in `Message Attachments/` directory or the email server. Query pattern:...
   ```bash
   sqlite3 ~/Library/Group\ Containers/UBF8T346G9.Office/Outlook/Outlook\ 15\ Profiles/Main\ Profile/Data/Outlook.sqlite \
     "SELECT Message_TimeSent, Message_NormalizedSubject FROM Mail \
      WHERE Message_NormalizedSubject LIKE '%keyword%' AND Message_HasAttachment=1 \
      ORDER BY Message_TimeSent DESC LIMIT 10;"
   ```
1. **Empty pages**: Some pages in multi-section PDFs are blank separators. Skip if `text.strip() == ""` and `len(tables) == 0`.
3. **Table split across pages**: If a table ends mid-page, the continuation will have no header row. Solution: accumulate rows until a new header row is detected.
4. **Column offset in extracted tables**: `pdfplumber` tables sometimes return `None` for empty cells, shifting column alignment. Validate with `row[0]` being the expected first column.
5. **OneDrive lock affects ALL syscalls**: `shutil.copy2`, `open(...,'rb')`, `os.stat` — all fail with `Resource deadlock avoided`. There is no partial-read workaround for dataless placeholders.
6. **OneDrive-locked PDFs differ from .xlsb**: Excel .xlsb files need the Excel conversion workaround. PDFs can be hydrated via `open` (Preview) then read with `pdftotext` — do not try the AppleScript/Excel route for PDFs.
7. **System python3 vs venv**: `pdfplumber` may be installed under `/usr/local/bin/python3` but not under the hermes venv python. Use explicit path or check both.
8. **Tesseract /tmp access**: Tesseract can fail with `fopenReadStream` errors when the image is in `/tmp` on locked-down systems. **Fix: `cd /tmp && tesseract ...`** — changing the working directory to `/tmp` before running tesseract resolves the path resolution issue. Copying to CWD also works.
9. **No text layer detection is not an error**: PyMuPDF `page.get_text()` returning empty string is valid for image-based PDFs. Always check text length first before deciding the route.
10. **Encrypted PDFs may decrypt with empty password**: Many national-adoption PDFs (SIST, DIN, BSI previews) use 128-bit RC4 encryption with no user password. Try `pypdf.PdfReader(path).decrypt('')` before giving up.
11. **Incomplete PDFs (TOC says 42 pages, file has 15)**: National adoptions of European standards often only include the front matter and first few clauses. Always check: (a) page count vs TOC, (b) whether the last page ends mid-sentence or mid-clause. Supplement with web sources (ANSI previews, iTeh standards, academic reviews) for the missing sections.
12. **stdout cap truncates large terminal output (~40KB).** When extracting full contracts or large PDFs, `terminal("cat file")` or piping through `terminal()` silently truncates. For files over ~1000 lines, use Python file I/O directly (`open()` in `execute_code`) instead of terminal piping. The `execute_code` tool is the correct approach for bulk extraction.

16. **Arabic-Indic numerals (٠١٢٣٤٥٦٧٨٩) OCR is unreliable on scanned documents.** Tesseract routinely misreads Arabic-Indic digits, especially when handwritten or in low-quality scans. A 6x error occurred in one session (OCR reported internal plastering BOQ as ~52K EGP when the actual figure was 331K EGP). **Do not trust OCR-extracted financial figures from scanned Arabic documents.** Always:
    - Get a clean digital copy (MD, XLSX, text-based PDF) as primary source
    - Cross-reference OCR figures against expected totals (e.g., contract value vs sum of BOQ items)
    - Flag any OCR-extracted number for human verification before using in reports
    - If only scanned documents are available, note the uncertainty explicitly in all derived analysis

17. **execute_code has a 50 tool call limit.** When doing batch operations (converting multiple DOCX files, scanning many folders for file counts), use a single `terminal()` shell script that loops internally rather than making one `terminal()` call per item. The 50-call limit is hit quickly with per-file operations — a 98-folder scan with 4 tool calls per folder exhausts the budget. Write the loop as a bash script, run it once, then parse the output.

18. **Do not fabricate contract content.** If you have not read a specific article/clause, do not invent its content and cite it as a source. An AI agent previously fabricated "Day+1 PM sends reminder to CG, Day+3 PD escalates to CG Acting PM, Day+5 formal notice" and cited it as "Per Contract 0010003521 Sec 4 escalation protocol" — this text does not exist anywhere in the contract. The user caught it and flagged it as a serious error. Before citing any contract provision: (a) extract the actual text from the PDF, (b) quote it verbatim, (c) cite the exact article number. If the contract does not contain what the user is looking for, say so explicitly.

19. **`com.apple.provenance` xattr means OneDrive placeholder.** A file with size >0 that returns 0 lines from `read_file` is not necessarily empty — check `xattr -l /path/to/file`. The `com.apple.provenance` extended attribute (binary data) indicates a OneDrive "files on demand" placeholder that hasn't hydrated locally. This affects `.md`, `.pdf`, `.docx`, and any other extension. Don't assume the file is actually empty or corrupted — it's just not yet downloaded. Try the `open` hydration workaround or zipfile bypass (see [OneDrive-locked DOCX](#onedrive-locked-docx)).

## Schedule Compression & Restructuring

After extracting schedule data from a Gantt chart PDF, the next step is often **compressing** the design phase to meet a contractual requirement (e.g. "design complete in 3 months per SOW/ER"). This section covers the methodology.

### When to compress

Compression is needed when:
- The original schedule's design phase exceeds the contractual design period (e.g. 216 days -> 90 days)
- The SOW/ER explicitly states a fixed design period
- Activities show negative float from day one (schedule is already compressed/behind baseline)

### Correct phase sequencing

The design phase must follow this **logical dependency order** — getting the sequence wrong is the most common mistake:

1. PRELIMINARY -> Permits, mobilization (parallel with assessment)
2. ASSESSMENT -> Site surveys, existing BIM, MEP assessments
3. PREQUALIFICATION -> Subcontractor/supplier prequalification (BEFORE design)
4. 50% DESIGN -> Concept design all disciplines + specialized
5. MATERIAL SUBMITTALS -> Samples + approvals from prequalified vendors
6. 90% DESIGN -> Detailed design with APPROVED materials in specs
7. IFC 100% -> Final package + BIM federation + approvals

**Critical rule**: Material approvals must complete BEFORE 90% design finalizes. You cannot specify materials at 90% without knowing what's approved.

**Critical rule 2**: Prequalification must complete BEFORE 50% design starts for specialized disciplines (AV, lighting, showcase). Design teams need to know approved vendors to reference real products.

### Realistic durations per design package

For a museum fit-out / renovation project (not new-build), use these baselines:

| Package | Duration (working days) | Scope |
|---------|------------------------|-------|
| Architectural 50% | 12-15d | Plans, elevations, sections, material selection |
| Structural 50% | 8-10d | Calculations, load paths, coordination |
| MEP (Elec + Mech) 50% | 8-10d each | Layouts, sizing, schematics |
| Specialized (AV/Graphics/Lighting/Showcase) 50% | 7-10d each | Design with prequalified vendors |
| Architectural 90% | 10-12d | Detailed plans, specs, joinery |
| Structural 90% | 8d | Detailed reinforcement, connections |
| MEP 90% | 8-10d | Detailed routing, schedules |
| BIM Federation | 10d | All disciplines -> federation + 5d clash |
| IFC 100% Final Package | 12d | All disciplines coordinated |

### Compression methods

1. **Parallel disciplines** — ARC, STR, MEP, Specialized run simultaneously, not sequentially. Cuts 60-70% off serial timelines.
2. **Fast-track approvals** — Reduce from 5d to 2-3d per item. Requires written consultant commitment.
3. **Overlapping stage gates** — Assessment/50% overlap. 50%/90% zero gap. BIM continuous.
4. **Progressive release** — Fabrication info per discipline, not batched.
5. **Early specialized starts** — Museum-specific work starts alongside core disciplines.
6. **Prequalified vendors** — Lock subcontractors before 50% design. No "TBD" in specs.

### Material submittal batching

Batch 100+ items across 5 categories in parallel:

Week 1: Submit AV data sheets (screens, projectors, audio, racks)
Week 2: Submit Structural + Architectural Wave 1 + Electrical + Mechanical
Week 3: Submit Architectural Wave 2 + approvals start rolling
Week 4: All approvals complete

Requires **5 concurrent review streams** (one per discipline).

### Excel schedule structure

| Sheet | Content |
|-------|---------|
| 3-Month Design Schedule | All activities with WBS, ID, name, duration, dates, phase, predecessors, week |
| Timeline Summary | Phase overview + milestones |
| Compression Analysis | Original vs compressed comparison + assumptions |
| Dependency Map | Predecessor/successor relationships |

Color-code phases (navy headers 1F3864, yellow phase separators, distinct phase colors).

### Common pitfalls

1. Material approvals after 90% design — #1 error. Complete 2 weeks before 90% finalization.
2. Prequalification as afterthought — Must happen during prelims/assessment.
3. 5-day design packages — Too short. Use 8-12 days for 50%.
4. Sequential disciplines — ARC then STR then MEP wastes 60% of schedule.
5. Negative float ignored — Address root cause, not symptom.
6. Missing predecessors — Every activity needs explicit predecessor IDs.

### Reference files

- `references/aseer-museum-schedule-2026.md` — Original schedule data
- `references/aseer-schedule-compression-3month.md` — Worked example: 216d->90d compression

## Book & Standard Acquisition (PDF)

When the user asks you to "study" or "train on" a set of books/standards, follow this workflow to find, download, and ingest them.

### Search strategy

| Source | Best for | Notes |
|--------|----------|-------|
| `web_search` with `filetype:pdf` | Free/open PDFs | Try `"exact title" filetype:pdf` and `"exact title" PDF download` |
| `web_search` with `site:edu` | University-hosted copies | `"Manual of Museum Planning" filetype:pdf site:edu` |
| Internet Archive (`archive.org`) | Out-of-print / older editions | Check directory listing for non-restricted files (`.lcpdf`, `.lcp.epub`) |
| iTeh Standards preview | European standards (BS EN, ISO) | `cdn.standards.iteh.ai/samples/...` — often partial (first clauses only) |
| Academia.edu / ResearchGate | Academic PDFs | May require login; try direct PDF links |
| Slideshare / Scribd | Presentation versions | Often redirect to login; check raw file links |
| Publisher previews | Current editions | `api.pageplace.de/preview/...` — partial preview only |

### Download & verify

```bash
# Download with retry
curl -sL -o "filename.pdf" "URL" --max-time 120 --retry 3

# Verify it's a real PDF (not HTML redirect)
file "filename.pdf"
# Expected: "PDF document, version X.Y, N pages"
# Bad: "HTML document text" or "ASCII text" (redirect/login page)

# Check page count
python3 -c "
import PyPDF2
with open('filename.pdf', 'rb') as f:
    r = PyPDF2.PdfReader(f)
    print(f'Pages: {len(r.pages)}')
"
```

### Handling restricted/DRM files

| Symptom | Cause | Action |
|---------|-------|--------|
| HTML redirect (172B) | 401/403 from server | Try different source or accept unavailable |
| "Zip archive data" (`.lcpdf`) | LCP-encrypted PDF | Unzip → check if inner PDF is readable; if encrypted, delete |
| EPUB with 160 chars extracted | LCP-encrypted EPUB | Delete; DRM-locked EPUBs yield no usable text |
| 3-page PDF claiming 462 pages | Fake/scam PDF | Delete immediately |
| Cloudflare challenge | Bot protection | Try browser tool or accept unavailable |
| 15-page PDF with 42-page TOC | National adoption (partial) | Extract what's available; note limitation; supplement with web sources |

### Organize the library

```bash
# Rename to clean, readable filenames
mv "random_hash.pdf" "PMBOK_Guide_7th_Edition.pdf"

# Remove junk
rm -f "fake_book.pdf" "login_page.pdf"
```

### Study via subagent delegation

For each acquired document, dispatch a subagent with a focused extraction goal:

```python
delegate_task(
    context=f"PDF path: {pdf_path}\nThis is a {pages}-page document.",
    goal="Read and study [DOCUMENT]. Extract key knowledge about [TOPIC]. "
         "Focus on [USER'S DOMAIN: construction/museum/fitout]. "
         "Return a structured summary of the most important concepts."
)
```

**Batch pattern** — dispatch 3-6 subagents in parallel, one per document. Each returns its summary independently. Consolidate after all complete.

### Reference files

- `references/book-library-2026-07.md` — Acquired book library for this session: sources, sizes, page counts, and what was unobtainable

When extracting FIDIC contract clauses from PDFs (Red Book, Yellow Book, etc.), use this pattern:

```python
import pdfplumber

pdf = pdfplumber.open("/path/to/fidic.pdf")
full_text = ""
for i, page in enumerate(pdf.pages):
    text = page.extract_text()
    if text:
        full_text += f"\n\n=== PDF PAGE {i+1} ===\n{text}"

# Save to text file for chunked reading
with open("/tmp/fidic_full.txt", "w") as f:
    f.write(full_text)
```

Then use `read_file` with offset/limit to read specific clause sections. Search for clause headers like `"4.1"`, `"8.4"`, `"20.1"` to locate content.

**Key clauses for contractor focus:** 4 (Obligations), 8 (Delays), 11 (Defects), 13 (Variations), 14 (Payment), 15-16 (Termination), 20 (Claims/Disputes).

See `references/fidic-red-book-2005-contractor-guide.md` for the full extracted guide from the MDB Harmonised Edition (115 pages, 320K chars extracted).

```bash
# Test pdfplumber works
python3 -c "import pdfplumber; print('ok')"

# Test a single page
python3 - <<'PYEOF'
import pdfplumber
with pdfplumber.open("/tmp/test.pdf") as pdf:
    print(f"Pages: {len(pdf.pages)}")
    t = pdf.pages[0].extract_text()
    print(t[:500] if t else "[empty]")
PYEOF
```

## Construction Cost Analysis Pipeline

For extracting project financial data from a web app + scanned documents and producing an estimate-vs-actual comparison report, see `references/construction-cost-analysis.md` for the full pipeline: Supabase bulk download, OCR workflow, cross-document reconciliation, categorized MD summaries, and Chart.js HTML report generation.

## Reference files

- `references/contract-key-terms-extraction.md` — Worked example: extracting key terms from 5 Aseer Museum contracts when OneDrive originals are locked. 6-step extraction workflow, 15-field template, cross-reference patterns, OneDrive lock diagnostic, and tool failure table.
- `references/construction-cost-analysis.md` — Worked example: building finishing project cost analysis from web app + Supabase documents: verify factual claims about a document's content against the actual source; locate the correct file when the given path is wrong; search docx paragraphs + tables for naming patterns; build a structured discrepancy report with claim-vs-actual tables
- `references/shop-drawing-extraction.md` — Shop drawing PDFs from PostScript/Acrobat Distiller: partial text layer extraction, title block fields, dimension data, materials specs, and common sheet patterns (worked example: Bohemian Collection furniture shop drawings, 32 pages)
- `references/bma-cad-pdf-extraction.md` — BMA/Boris Micka CAD-generated interior design PDFs: drawing code system, MEP fixture legend libraries, critical disclaimer language, and RFI cross-reference worked example (RCRC Exhibition, 27 questions)
- `references/aseer-file-location-patterns.md` — Aseer Museum project file structure, OneDrive stub detection, Excel comparison sheet extraction, Outlook DB cross-reference, and known vendor quotation locations
- `references/aseer-register-2026-05-28.md` — Aseer-style multi-section register extraction (8 log types in one PDF, RTL Arabic, status code mapping)
- `references/email-archive-pattern-analysis.md` — Email archive analysis for template detection, sender profiling, response time patterns, and AI-generation indicators in correspondence bodies
- `references/fidic-red-book-2005-contractor-guide.md` — FIDIC Red Book 2005 MDB Harmonised Edition: full clause-by-clause extraction of Contractor Obligations (Clause 4), Variations (13), Claims & Disputes (20), Time Extensions (8), Payment (14), Defects Liability (11), Termination (15-16), plus museum-specific risk tables, critical time-bar deadlines, payment timelines, and dispute resolution ladder. Extracted via pdfplumber from the 115-page PDF.
- `references/medical-report-ocr.md` — OCR pipeline for mixed Arabic/English medical lab reports (blood tests, CBC, hormones) with tesseract + pillow, structured data extraction, and HTML/Chart.js dashboard generation
- `references/excel-schedule-extraction.md` — Extract all columns from multi-sheet Excel schedule files, auto-detect header rows, handle deduplication by code prefix, preserve full field sets per schedule type
- `references/standard-pdf-extraction-pattern.md` — Pattern for extracting from European/British standards (BS EN, EN, ISO): encrypted national adoptions, incomplete PDFs (TOC says 42 pages, file has 15), supplementing missing clauses from web sources. Worked example: BS EN 16893:2018 Conservation of Cultural Heritage.
- `references/material-data-sheet-extraction.md` — Worked example: extracting tabular data from image-based material data sheets (SS 304 inspection cert + Verdo FR MDF test report) using TSV bounding-box reconstruction, zoomed crop OCR, and manual calculation of derived values
- `references/riba-plan-of-work-2013-study.md` — RIBA Plan of Work 2013 comprehensive study: all 8 stages (0–7) with full task bar tables, 6 procurement options with museum-specific recommendations, 12 project strategies, contractor's PM perspective, 2007→2013 stage mapping, and information exchange deliverables. Extracted from a 39-page image-based slide deck PDF + UCL overview supplement.
- `references/aseer-main-contract-extraction.md` — KSA MoC Contract 0010003521: file locations, 9-section structure, Section 4 article map (13 articles), extraction pattern for bilingual AR/EN government construction contracts via pdftotext -layout
- `references/html-project-plan-audit.md` — Structured QC audit of large HTML project plan documents (PEP, DMP, BEP). Workflow for locating sections via `<!-- PAGE` comment markers, extracting data tables, management dashboards, flow diagrams, and building a structured finding report with gap analysis. Worked example: Aseer Museum PEP Rev 01 audit of 6 sections in a 17,795-line HTML document.