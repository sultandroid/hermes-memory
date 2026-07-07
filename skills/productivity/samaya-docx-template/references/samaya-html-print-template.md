# Samaya HTML Print-Ready Document Template

Design system and workflow for creating A4 print-ready HTML documents following the Samaya project template format (used for SMP, BEP, Risk Plan, MOS, and all formal submittals).

## When to use HTML vs DOCX

| Format | Use case | Output |
|--------|----------|--------|
| **HTML** (this pattern) | Plans, submittals, formal documents needing professional A4 print layout with logos, photos, cover page, and tables | `.html` -> browser preview -> Ctrl+P -> `.pdf` |
| **DOCX** (samaya_doc_template.py) | SOWs, letters, transmittals, meeting minutes -- documents primarily edited in Word | `.docx` for formal issue |

**Rule:** If the document needs a cover page, stakeholder logos, embedded photos, or will be printed/submitted as a bound A4 document -> use HTML format.

## Design System

### CSS Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `--primary` | `#0F172A` | Dark navy -- headings, table headers, cover bg |
| `--secondary` | `#0284C7` | Blue -- accent bars, icons |
| `--accent` | `#16A34A` | Green -- status badges, cover accents |
| `--fail` | `#B91C1C` | Red -- critical risk badges |
| `--text-main` | `#1E293B` | Body text |
| `--text-muted` | `#64748B` | Secondary text, captions |
| `--border` | `#E2E8F0` | Table/section borders |
| `--font-heading` | `'Montserrat', sans-serif` | Heading font |
| `--font-body` | `'Inter', sans-serif` | Body font |

### Cover Page Pattern

Dark navy cover with Samaya logo (inverted white), 5 stakeholder logos at bottom, green accent lines. See the SMP or MOS RevA HTML for exact markup -- it is always the same structure with project-specific title text swapped in.

### Page Shell Pattern

Each content page follows:
- `.page-header`: left=project info + doc ref, right=Samaya logo
- `.h2-row`: blue bar + section H2 + disposition chip (PMBOK ref)
- Content: tables (`.eng-table`), info strips (`.spec-strip`), photos (`.photo-frame`)
- `.pg-footer`: 3-column grid -- doc ref / short description / page number

### Key CSS Classes

`.page` = A4 page 210x297mm, `.page-cover` = dark cover, `.eng-table` = navy-header alternating-row table, `.snapshot-grid` = TOC cards, `.spec-strip` = left-border info box, `.photo-frame` = bordered image, `.wf-node` = workflow step, `.badge`/`.badge-pass`/`.badge-high`/`.badge-low` = status pills, `.compact`/`.tight` = spacing modifiers.

### Logos

All logos in `assets/` copied from `02.13_Stakeholder_Plan/01_Source_Files/01_HTML/assets/`. Five entities: MoC, PMC, CG, NRS, Samaya. Cover page logos use `filter: brightness(0) invert(1)` for white rendering on dark bg.

## Project Folder Template

When creating a new document type under `02_Plans_and_Procedures/`:

```
02.XX_Document_Type/
├── 00_Master_Index/README.md      # File register + PMBOK mapping
├── 01_Source_Files/
│   ├── 01_HTML/assets/            # Logos + photographs
│   ├── 02_PDFs/                   # Generated PDFs
│   ├── 03_Word/                   # DOCX backup
│   └── 04_Assets/                 # Raw source photos
├── 02_CG_Responses/
├── 03_Supplementary/
├── 04_Registers/
├── 05_Compliance_Audit/
├── 06_Legacy_Files/
├── 07_Guidelines/
└── README.md
```

## Design Variant: Monochrome CV-Pack Template

For some deliverables, the user explicitly prefers the **monochrome black/white template** used in `ASR-SAM-KP-CV-PACK-BIM-001.html` (found under `Docs/09_Registers/13_Key_Personnel_Register/CVs/_archive/HTML/`).

**When to use:** The user will say "use same template" and point to a CV pack HTML. Use this for Method of Statements, technical reports, and other submittals where the navy/blue colored template is not requested.

**Key CSS differences from colored template:**
- `:root` colors: `--ink: #000000`, `--rule: #000000`, `--paper: #FFFFFF` — pure monochrome
- No `--primary` navy, no `--secondary` blue, no `--accent` green
- `font-family: 'Calibri','Carlito','Arial','Helvetica',sans-serif` at 9.75pt body
- `h1`: 22pt uppercase bold, black
- `h2`: 10pt uppercase bold, bottom border 0.6pt black
- Logo strip: 4-column CSS grid (`grid-template-columns: repeat(4, 1fr)`) with entity logos + labels
- `meta-grid`: 3-column grid for project metadata
- `dc-block` / `qc-block`: black-background header bars (`background: #000; color: #FFF`), bordered content blocks
- `summary-table`: full-width bordered table, black header row borders 0.8pt
- Sheet: `210mm × 297mm`, padding `14mm 18mm`, shadow `0 1px 6px rgba(0,0,0,0.08)`
- Logos rendered at `height: 10mm; object-fit: contain` inside logo cells

**Regeneration workflow when user asks "use same template":**
1. Read the referenced CV pack HTML to extract the `<style>` block and full CSS
2. Adapt the existing MOS/plan content into the monochrome sheet structure
3. Keep the same doc-strip, logo-strip, meta-grid, dc-block, qc-block patterns
4. Embed images as base64 (see Photo Sourcing below)
5. Verify with: `document.querySelectorAll('img').forEach(i => console.log(i.naturalWidth))` in browser console

## Photo Sourcing

### Priority Order
1. **Project's own files first** — Check project folders for real product images, brochure PDFs, and previous similar documents.
2. **Extract from brochure PDFs** (PyMuPDF, preferred over pdftoppm):
   ```python
   import fitz
   doc = fitz.open("brochure.pdf")
   page = doc[0]
   pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))  # 3x for print quality
   pix.save("output.jpg")  # yields 1800-2400px JPEG
   ```
   Then base64-encode and embed in HTML. This avoids web download failures.
3. **Web-sourced (CC-licensed)** — Wikimedia Commons is the most reliable source:
   - Navigate to `https://commons.wikimedia.org/w/index.php?search=KEYWORD&title=Special:MediaSearch&type=image`
   - Click results, look for full-resolution versions
   - Download via `curl -sL -o "filename.jpg" "URL" -H "User-Agent: Mozilla/5.0"`
4. **Avoid:** Unsplash/Pexels (blocked by corporate firewall/bot detection).

### Image Verification (CRITICAL)
After downloading ANY image, run:
```bash
file /path/to/image.jpg
```
**Must report "JPEG image data"**, NOT "HTML document text" or "ASCII text". If it says HTML, the download returned a redirect/error page — re-download with proper User-Agent or try a different source.

Then embed as base64:
```python
import base64
with open("image.jpg", "rb") as f:
    b64 = base64.b64encode(f.read()).decode("ascii")
src = f"data:image/jpeg;base64,{b64}"
```

**Verify in browser:**
```javascript
Array.from(document.querySelectorAll('img')).map((img,i) =>
  `${i+1}: ${img.naturalWidth}x${img.naturalHeight} ${img.complete?'OK':'FAIL'}`)
```
Every image must show non-zero dimensions. If any shows 0x0, the base64 data is corrupt — re-encode from the source file.

### Size Constraints
- Base64 expands binary by ~33%. A 150KB JPEG → 200KB base64 string.
- Total HTML size with 5-7 embedded images: ~4-7 MB. This is acceptable for local/OneDrive distribution but too large for email. For email, attach the HTML separately.
- Minimum image resolution: 800px wide; 1024px+ preferred for A4 print.

### Notes
- Never use generic placeholder stock photos. User will reject them.
- Photos stored in `assets/` (HTML-adjacent) + `04_Assets/` (reusable source).

## PDF Generation

```bash
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib weasyprint \
  "input.html" "output.pdf"
```

Cosmetic warnings (box-shadow, filter, color-adjust) are safe to ignore.

## Surge Deployment (only if user requests)

```bash
cd "01_Source_Files/01_HTML"
surge --domain project-doc-ref.surge.sh .
```

## Personnel Verification Protocol

Before inserting any person's name into an HTML or DOCX document, cross-reference:
1. SMP Rev03 HTML -- extract from the `<td>` cells (QC-01 to QC-04 for management, T1-01 to T1-08 for key personnel)
2. `~/Stakeholder_Register_Update_Findings.md` -- latest email-derived changes
3. `~/hermes-memory/unified/UNIFIED_MEMORY.md` -- condensed verified roles

Extraction: `grep for T1-0[1-8]` in the SMP Rev03 HTML and read the adjacent `<td>` cells for names.
