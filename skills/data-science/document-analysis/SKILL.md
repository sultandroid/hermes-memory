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

```python
import fitz, pytesseract
from PIL import Image

doc = fitz.open("document.pdf")
page = doc[0]
pix = page.get_pixmap(dpi=300)
img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
text = pytesseract.image_to_string(img, lang='eng', config='--psm 12')
```

**PSM selection guide**: `3`=default, `4`=single column, `6`=single block, `11`=sparse text, `12`=single block variable orient (best for tables/forms), `13`=raw line.

**Pre-processing for difficult scans:**
```python
from PIL import ImageEnhance
gray = img.convert('L')
enhancer = ImageEnhance.Contrast(gray)
gray_high = enhancer.enhance(2.0)
```

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

### Image-based PDFs (no text layer)

PDFs from Adobe Illustrator, InDesign, scanned documents, or **slide deck exports** (PowerPoint/Keynote → PDF) may have zero extractable text. Detect with PyMuPDF:

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
8. **Tesseract /tmp access**: Tesseract can fail with `fopenReadStream` errors when the image is in `/tmp` on locked-down systems. Save rendered PNGs to the current working directory instead.
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

- `references/bma-cad-pdf-extraction.md` — BMA/Boris Micka CAD-generated interior design PDFs: drawing code system, MEP fixture legend libraries, critical disclaimer language, and RFI cross-reference worked example (RCRC Exhibition, 27 questions)
- `references/aseer-file-location-patterns.md` — Aseer Museum project file structure, OneDrive stub detection, Excel comparison sheet extraction, Outlook DB cross-reference, and known vendor quotation locations
- `references/aseer-register-2026-05-28.md` — Aseer-style multi-section register extraction (8 log types in one PDF, RTL Arabic, status code mapping)
- `references/email-archive-pattern-analysis.md` — Email archive analysis for template detection, sender profiling, response time patterns, and AI-generation indicators in correspondence bodies
- `references/fidic-red-book-2005-contractor-guide.md` — FIDIC Red Book 2005 MDB Harmonised Edition: full clause-by-clause extraction of Contractor Obligations (Clause 4), Variations (13), Claims & Disputes (20), Time Extensions (8), Payment (14), Defects Liability (11), Termination (15-16), plus museum-specific risk tables, critical time-bar deadlines, payment timelines, and dispute resolution ladder. Extracted via pdfplumber from the 115-page PDF.
- `references/medical-report-ocr.md` — OCR pipeline for mixed Arabic/English medical lab reports (blood tests, CBC, hormones) with tesseract + pillow, structured data extraction, and HTML/Chart.js dashboard generation
- `references/excel-schedule-extraction.md` — Extract all columns from multi-sheet Excel schedule files, auto-detect header rows, handle deduplication by code prefix, preserve full field sets per schedule type
- `references/standard-pdf-extraction-pattern.md` — Pattern for extracting from European/British standards (BS EN, EN, ISO): encrypted national adoptions, incomplete PDFs (TOC says 42 pages, file has 15), supplementing missing clauses from web sources. Worked example: BS EN 16893:2018 Conservation of Cultural Heritage.
- `references/riba-plan-of-work-2013-study.md` — RIBA Plan of Work 2013 comprehensive study: all 8 stages (0–7) with full task bar tables, 6 procurement options with museum-specific recommendations, 12 project strategies, contractor's PM perspective, 2007→2013 stage mapping, and information exchange deliverables. Extracted from a 39-page image-based slide deck PDF + UCL overview supplement.