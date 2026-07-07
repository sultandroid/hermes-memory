# CV-Pack HTML Template — Monochrome Print-Ready Documents

## Overview

A self-contained A4 print-ready HTML template used for formal Samaya project documents (MOS, SOW, CV packs, procedures). Uses monochrome (black/white) styling — no navy, no red, no color. Matches the design system of `ASR-SAM-KP-CV-PACK-BIM-001.html`.

## When to use

- Formal project plans submitted to CG (Method of Statement, Risk Plan, etc.)
- Documents where the CV-pack style was explicitly requested
- Documents with embedded photos/images (base64)
- Any document that needs to look clean in print without color

## Key reference file

`ASR-SAM-KP-CV-PACK-BIM-001.html` at:
```
.../Aseer-Museum/Docs/09_Registers/13_Key_Personnel_Register/CVs/_archive/HTML/ASR-SAM-KP-CV-PACK-BIM-001.html
```

Read this file first to extract the latest CSS. It changes as the design evolves.

## Core CSS structure

| Class | Purpose |
|-------|---------|
| `.sheet` | A4 page wrapper: 210mm × 297mm, 14mm/18mm padding, shadow on screen |
| `.doc-strip` | Document reference line at top of every page — 8.5pt, bottom border |
| `.logo-strip` | 4-column grid (MoC/ACE/CG/Samaya logos) on cover page |
| `h1` | 22pt uppercase bold — cover page title |
| `h2` | 10pt uppercase with bottom border — section headings |
| `.meta-grid` | 3-column grid for project metadata (key-value pairs) |
| `.dc-block` | Bordered document control block with black header bar and white text |
| `.qc-block` | Sign-off block (Prepared/Reviewed/Approved) with signature lines |
| `.summary-table` | Full-width bordered table with header row and alternating shading |

## Base colors

```css
:root {
  --ink: #000000;
  --rule: #000000;
  --paper: #FFFFFF;
}
```

No other colors. Pure black on white.

## Font

```css
font-family: 'Calibri','Carlito','Arial','Helvetica',sans-serif;
font-size: 9.75pt;
line-height: 1.32;
```

## Print CSS

```css
@page { size: A4 portrait; margin: 0; }
.sheet { width: 210mm; min-height: 297mm; padding: 14mm 18mm; }
@media print {
  .sheet {
    margin: 0 !important; box-shadow: none !important;
    width: 210mm !important; height: 297mm !important;
    overflow: hidden !important; page-break-after: always;
  }
}
```

## Image embedding

- All images must be base64-embedded (`data:image/jpeg;base64,...`)
- Use `<img style="max-width:100%;height:auto;">` for responsive sizing
- Wrap in `<div class="figure">` with caption text below

### Embedding workflow

1. Verify image files are real JPEGs: `file image.jpg` → must say "JPEG image data"
2. Encode in Python:
   ```python
   import base64
   with open(fpath, 'rb') as f:
       b64 = base64.b64encode(f.read()).decode('ascii')
   src = f'data:image/jpeg;base64,{b64}'
   ```
3. Verify the base64 decodes to JPEG magic bytes `\xff\xd8`:
   ```python
   decoded = base64.b64decode(b64)
   assert decoded[:2] == b'\xff\xd8', "NOT a JPEG!"
   ```
4. Replace in HTML: use `re.subn()` with alt-text-based pattern matching for reliability (src may appear before or after alt attribute)

### Image embedding pitfalls

- **Subagents often download HTML error pages instead of real images.** Always verify with `file` command after download.
- **PDF brochure extraction is more reliable than web downloads** for product images. Use PyMuPDF (fitz):
  ```python
  import fitz
  doc = fitz.open(brochure.pdf)
  page = doc[page_num]
  pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))
  pix.save("output.jpg")
  ```
- **Base64 of an HTML page still decodes without error** — must check magic bytes, not just valid base64
- **Regex replacement of img src attributes** in Python: use two patterns (alt-before-src, src-before-alt) since HTML may have either order
- **Large images (brochure pages):** brochure page extracts at 3× resolution produce ~1.3 MB JPEGs → ~1.8 MB base64. Total HTML can reach 7+ MB — still fine for browsers but slow in text editors

## Page structure template

```
.sheet (cover page)
  ├── .doc-strip (ref + page number)
  ├── .logo-strip (4-column: MoC / ACE / CG / Samaya)
  ├── h1 (title)
  ├── subtitle
  ├── .meta-grid (project data)
  ├── .dc-block (document control)
  └── .qc-block (sign-off)

.sheet (TOC + section content)
  ├── .doc-strip
  ├── h2 (section title)
  ├── p / ul / table
  └── .figure (embedded image)

.sheet (appendix)
  ├── .doc-strip
  └── .figure (brochure pages)
```

## Document reference pattern

```
MOC-ASEER-SIC-1K0-XXX-NNN
```

Where XXX = document type (MOS, SOW, RPT, PLAN) and NNN = sequential number.

## Typical workflow

1. Read the CV pack HTML to extract latest CSS/classes
2. Build new HTML from scratch using same class names (sheet, doc-strip, etc.)
3. Embed all images as base64 from verified JPEG files
4. Test in browser with print preview (Ctrl+P)
5. Print to PDF for submission (not WeasyPrint — browser print is more reliable for complex layouts)
