# Shop Drawing PDF Extraction

## Context

Shop drawings from construction/fit-out projects are typically **PostScript → Acrobat Distiller PDFs** (producer: `PScript5.dll Version 5.2.2` + `Acrobat Distiller 20.0`). These are NOT pure image-based PDFs — they have a **partial text layer** that PyMuPDF can extract, even though the visual appearance is that of a scanned/rendered drawing.

## Key Insight

The text layer in Distiller PDFs is often garbled (scrambled characters, encoding artifacts, missing spaces) but still **far more reliable** than tesseract OCR on the same page. The text layer preserves:
- Title block fields (drawing title, number, date, drawn by, reviewed by)
- Dimension numbers
- Section labels
- Material callouts
- Notes and disclaimers

OCR on these same pages produces near-zero useful output because the text is rendered as vector paths, not raster text.

## Workflow

### 1. Quick detection

```bash
pdfinfo "/path/to/shop_drawing.pdf" | grep -i "producer"
# "PScript5.dll Version 5.2.2" + "Acrobat Distiller" → partial text layer
```

### 2. Extract text from ALL pages in one pass

```python
import fitz

doc = fitz.open(pdf_path)
for i in range(doc.page_count):
    page = doc[i]
    text = page.get_text()
    if text.strip():
        print(f"=== PAGE {i+1} ===")
        print(text[:1500])
doc.close()
```

### 3. For pages with no text layer, render + OCR

```python
pix = page.get_pixmap(dpi=300)
img_path = f"/tmp/page_{i+1:02d}.png"
pix.save(img_path)
# Then tesseract on the PNG
```

### 4. Extract embedded images for visual reference

```python
for page_num in range(doc.page_count):
    page = doc[page_num]
    image_list = page.get_images(full=True)
    for img_idx, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        img_bytes = base_image["image"]
        ext = base_image["ext"]
        w, h = base_image["width"], base_image["height"]
        img_path = f"/tmp/p{page_num+1:02d}_img{img_idx}_{w}x{h}.{ext}"
        with open(img_path, "wb") as f:
            f.write(img_bytes)
```

## What to Look For in Shop Drawing Text

### Title block fields (typically on every page)
- **Firm/Company**: e.g. "OutLine Enterprise" (often bilingual AR/EN)
- **Drawn By**: Engineer name
- **Reviewed By**: Reviewer name
- **Date**: Creation and revision dates
- **Page No**: Sheet numbering (e.g. "2/25", "3/3")
- **Drawing Title**: e.g. "SHOE RACK", "BOOK SHELVES", "SKIRTING"
- **Project Name**: Often blank in shop drawings (filled in by contractor)
- **Part Number**: Component numbering
- **Material**: e.g. "MDF with walnut veneer", "ply wood", "solid wood"
- **Qty**: Quantity
- **Scale**: "scale as shown on drawing"
- **Units**: "All dimensions are in millimeters (mm) unless otherwise noted"

### Dimension data (scattered in text layer)
- Overall dimensions: e.g. "2200.0", "2800.0", "3400.0" (widths)
- Section dimensions: e.g. "SECTION A-A", "SECTION B-B", "SECTION C-C"
- Material thicknesses: "18.0", "36.0" (mm)
- Component dimensions: shelf heights "305.0", toe kicks "70.0", "400.0"
- Hidden elements: "HIDDEN LEDLIGHT" with dimensions

### Materials specification pages
- Board materials: "FR-FireResistant-MDF 18MM X 122CM X 244CM"
- Finishes: "FireResistant polyurethane lacquer finish"
- Hardware: "Screw, Zinc Polish, Size: 75 X 5 mm"
- Adhesives: "SILICONE CLEAR"
- Skirting types: Type SK02 (MDF), Type SK03 (solid wood) with reference codes (IWDB-101, IWDB-51)

### Contact/cover pages
- Company name, email, phone, address
- "THANK YOU" closing page

## Common Patterns in Shop Drawing Sets

| Pattern | Example |
|---------|---------|
| Cover sheet | Page 1: collection name, firm name, drawn/reviewed by |
| General notes | Page 2: disclaimer, standard notes |
| Cutting lists / BOM | Pages with part numbers, quantities, materials |
| Section views | A-A, B-B, C-C, D-D with dimension callouts |
| Multiple sizes of same item | SHOE RACK w 2200 / 2800 / 2900 / 3400 mm |
| Materials spec page | Consolidated materials list |
| Skirting/baseboard details | Types, lengths, profiles |
| Wall cladding | Area totals, subframe details |
| Contact sheet | Last page: company info |

## Pitfalls

1. **Text layer is garbled but usable**: Don't discard text just because it has encoding artifacts (e.g. `$//'5$:,1*6$1'&252/6$5(%$6('21 7+(6(1'(' ,0$'*(6` decodes to "ALL DRAWINGS AND COLORS ARE BASED ON THE SENT IMAGES"). The garbled text is still readable when you look past the encoding.
2. **Some pages have no text layer**: Pages that are purely vector graphics (section views, elevations) may have zero extractable text. These need OCR or visual inspection.
3. **Arabic text in text layer**: Arabic text may appear as garbled unicode or RTL artifacts. The text layer preserves it better than OCR, but it may need manual interpretation.
4. **Page numbering is inconsistent**: Some pages have "2/25" (set numbering) while others have "2/3" (sub-set numbering). Don't assume a single numbering scheme.
5. **Project name is often blank**: Shop drawings frequently leave the "Project name" field empty — it's filled in by the contractor when issued.
6. **OCR is nearly useless on Distiller PDFs**: Tesseract produces almost no output on PostScript-rendered vector text. Always prefer the text layer.
