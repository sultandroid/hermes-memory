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
| PDF with real tables | `pdfplumber` | `extract_tables()` + `extract_text()` |
| Simple single-column PDF (quotes) | `pdftotext` (poppler) | beats pdfplumber on irregular layouts |
| macOS text-based PDF (fastest) | `pdftotext -layout -enc UTF-8` | Available on macOS via poppler, handles bilingual AR/EN |
| Image-based PDF (no text layer) | PyMuPDF (`fitz`) → render to PNG → `tesseract` OCR | common for Illustrator/InDesign exports, scanned drawings |
| **Slide deck PDF (PowerPoint/Keynote export)** | PyMuPDF → PNG → tesseract OCR, **then supplement with web sources** | 39-page slide decks with decorative elements; OCR is incomplete — always find a companion text document (overview PDF, published article) as primary source |
| Scanned PDF (lightweight OCR) | `pytesseract` + Pillow | ~200MB tesseract, no PyTorch needed |
| Complex layouts / equations / forms | `marker-pdf` | Best accuracy, ~3-5GB install |
| Encrypted PDF (128-bit RC4) | `pypdf` → `reader.decrypt('')` → then any tool | Many national-adoption PDFs are encrypted; decrypt first with empty password, then extract with pdftotext/pymupdf |
| Incomplete PDF (partial content) | Compare page count vs TOC; supplement with web sources | National adoptions may only contain front matter + first few clauses; detect by checking if last page ends mid-document |
| OneDrive-locked PDF | hydrate via `open` (Preview), then `pdftotext` | NOT the Excel/AppleScript route |
| `.xlsb` (OneDrive-locked) | Excel → Save As `.xlsx`, then `openpyxl` | only working path; xlsb is binary |
| `.xlsx` | `openpyxl` (`read_only`, `data_only`) | |
| DOCX | `python-docx` | Parses actual structure, far better than OCR |
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

**When to use which route:**

| Situation | Route |
|-----------|-------|
| Multi-page PDF, need page-by-page | A (PyMuPDF) |
| Single-page scanned letter, macOS | B (sips) — fewer deps |
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

## OneDrive-locked PDFs

BIM registers often live as `.xlsb` files or PDFs on OneDrive. They are **unreadable by any tool** from the terminal because the OneDrive sync engine holds a file lock.

**Symptom**: `Resource deadlock avoided` — every syscall (read, copy, stat) fails. Files show `compressed,dataless` flag in `ls -laO`.

**Workaround — hydrate via `open` then extract:**

OneDrive PDFs can be hydrated (downloaded from cloud) by opening them in their native app (Preview for PDFs). Once hydrated, they become regular files readable by extraction tools.

```bash
# Step 1: Trigger hydration by opening in Preview
open "/path/to/OneDrive-locked-file.pdf"
# Step 2: Wait a few seconds for download
sleep 8
# Step 3: Verify dataless flag is gone
ls -laO "/path/to/file.pdf"
# → compressed,dataless should no longer appear
# Step 4: Extract text with pdftotext (from poppler)
pdftotext "/path/to/file.pdf" - 2>/dev/null
```

The `open` command triggers macOS LaunchServices → Preview → OneDrive hydrates the file. The dataless flag disappears and the file becomes a regular file.

Do NOT use non-native apps (e.g. `open -a TextEdit file.pdf`) — they open blank for dataless files.

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

## Reference files

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