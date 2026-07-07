---
name: procurement-info-pack
description: Create purchasing information packs for Samaya Procurement Department. Standardized DOCX per Samaya style guide with material specs, quantities, and action checklists. Supports bilingual (EN/AR) format.
version: 1.1
tags: [samaya, procurement, purchasing, docx, bilingual]
---

# Procurement Information Pack Creation

Create a purchasing info pack when the Technical Office needs to brief the Procurement Department on materials to source. Each pack lives in a `10_Purchasing/` folder under the relevant subcontractor directory.

## Trigger

Create one when:
- A new subcontractor is engaged and material purchasing is needed
- IFC drawings depend on specific product data from suppliers
- A design direction (from NRS/CG) requires new materials not yet sourced
- The user says "prepare a folder for Purchasing Department"

## Standard Structure

```
10_Purchasing/
├── Door_Hardware_Purchasing_Info.docx   # Main purchasing doc
├── 01_NRS_Specs/                         # Spec PDFs (if available)
├── 02_Datasheets/                        # Manufacturer datasheets
└── 03_Drawings/                          # Referenced drawings
```

## DOCX Template (Sections)

| Section | Content |
|---------|---------|
| Title | ITEM — PURCHASING INFORMATION |
| Subtitle | Prepared for Purchasing Dept | Source: spec refs | Rev X |
| 1. Summary | Quick table: brand specified?, finish, standards, source, fire rating, qty |
| 2. Specification Reference | Table of governing docs (NRS spec, ER, SOW, DMP, Div) |
| 3. Materials | Material-by-material with spec, qty, application per material |
| 4. Quantities | Summary table of estimated quantities |
| 5. Actions | Checklist of what Purchasing needs to do |

## Style Rules

- **Font:** Calibri throughout
- **Title:** 16pt Bold, Navy #1E293B, bottom border
- **H2:** 12pt Bold, Navy, uppercase, bottom border
- **Tables:** Navy header (#1E293B) with white text, alternating white/light gray rows (#F1F5F9), compact padding (1pt), 8pt font
- **Note box:** Left red border (#B01E2F), muted bg (#F8FAFC)
- **Bullets:** Dash prefix, 9pt
- **Checklist:** Square checkbox + muted bg items
- **Footer:** Doc ref, Page X of Y, Samaya Investment Company
- **No AI footprints:** No emoji/icons, no first-person, no conversational language
- **Print-friendly:** Light shading only, black text, borders for structure

## Bilingual Mode (English lead)

When the user requests bilingual (AR/EN):
- English paragraph first, Arabic paragraph below (RTL, right-aligned)
- Table headers: `'ITEM / البند'`, `'QTY / الكمية'`
- Note labels: `'NOTE / ملاحظة'`
- Use `bilingual(doc, en_text, ar_text)` for paired content
- Use `body_ar(doc, text)` for standalone Arabic
- Font: Calibri works for both scripts

## python-docx Implementation

Use the Samaya doc engine from the style guide (functions: setup, header, footer, title, h2, h3, body, tbl, note, bullet, actions). Located in the build script pattern.

Key function signatures:
```python
setup(doc)
header(doc, project_name, doc_ref, date)
footer(doc, doc_number)
title(doc, text)
h2(doc, text)
body(doc, text, size=10)
body_ar(doc, text, size=10)          # Arabic RTL
bilingual(doc, en_text, ar_text)      # English + Arabic pair
tbl(doc, headers, data, widths=None)  # Column widths in cm
note(doc, text, label='NOTE')
bullet(doc, text)
actions(doc, items)                   # Checklist with checkboxes
```

## Material Spec Reference Pattern

Each material table has 3 columns:
| Parameter | Specification | Reference |

References should cite: NRS design intent, ER (Employer Requirements), SOW (Scope of Work), DMP (Document Management Plan), Division spec, SBC chapter.

## Folder Location Convention

```
Subcontractors/{NN}_{Trade}_Contractor/10_Purchasing/
```

For items not tied to a single subcontractor:
```
Subcontractors/10_Purchasing_{Item_Name}/
```

## Examples from Aseer Museum

| Pack | Location | Contents |
|------|----------|---------|
| Door hardware | `17_Doors_Metal_Contractors/10_Purchasing/` | NRS L20A, P21 specs, Schlage/ASSA datasheets, door schedule 1960, ironmongery 1961 |
| Setworks materials | `06_Setworks_Joinery_Contractor/10_Purchasing/` | Bilingual EN/AR, 12 materials with specs |
| Replica & model | `01_Replica_Model_Contractor/10_Purchasing/` | Model-making, sculpting, casting materials |
| Graphics & signage | `08_Graphics_Contractor/10_Purchasing/` | Acrylic, vinyl, OLED backlit, mounting |
| Patinated brass | `10_Purchasing_Patinated_Brass/` | CG-mandated solid brass, NRS supplier ref |

## Vendor Quotation Comparison (pre-purchasing evaluation)

When evaluating multiple vendors for the same equipment/service class, create a structured comparison before issuing a purchasing info pack.

### Workflow

1. **Collect quotations** — save all vendor PDFs from Outlook attachments or emails into a staging folder
2. **Organize by product** — each product model gets its own folder containing:
   - `Quotation_<Product>.pdf` — the vendor's price offer
   - `Brochure_<Product>.pdf` — product spec sheet / brochure (if available)
3. **Extract pricing from PDFs** — scanned-image PDFs need pdftotext; text PDFs can use pdfminer. Key data: hardware price, discount, VAT, total with VAT, delivery terms, training, payment terms
4. **Build Excel comparison** — side-by-side table with columns: Vendor, Contact, Scanner Type, Range, Accuracy, Speed, Weight, Price (excl. VAT), VAT, Total, Training, Delivery, Payment Terms, Quotation Ref
5. **Add software/optional extras** as a separate sheet if vendors offer modular add-ons
6. **Key Contacts sheet** — company, contact person, email/phone, product

### Excel template pattern

| Sheet | Content |
|-------|---------|
| Comparison | Side-by-side spec + price table |
| Software Options | Optional add-ons per vendor |
| Contacts | Vendor contact info |

### Pricing extraction tips

- **Scanned PDFs**: Use `pdftotext -layout` which handles table extraction better than pdfminer. For table-heavy pages, extract between section headers (e.g., between "PACKAGE INVESTMENT" and next section) with `sed -n '/Section/,/NextSection/p'`
- **SAR pricing**: Always note whether prices include or exclude VAT (15% KSA). Check for discounts applied
- **Mark TBC** for fields not available in the quotation rather than leaving blank — user will fill them in unprompted

### Outlook attachment extraction technique

When quotation PDFs are attached to Outlook emails but not saved to disk:

1. Find the email's RecordID from Outlook SQLite:
   ```sql
   sqlite3 ~/Library/Group\ Containers/UBF8T346G9.Office/Outlook/Outlook\ 15\ Profiles/Main\ Profile/Data/Outlook.sqlite \
     "SELECT Record_RecordID, Message_NormalizedSubject FROM Mail WHERE Message_NormalizedSubject LIKE '%keyword%';"
   ```

2. Look up the attachment BlockIDs:
   ```sql
   sqlite3 ... "SELECT hex(BlockID), BlockTag FROM Mail_OwnedBlocks WHERE Record_RecordID=<ID> ORDER BY BlockTag;"
   ```

3. Find the actual file paths:
   ```sql
   sqlite3 ... "SELECT hex(b.BlockID), b.PathToDataFile FROM Blocks b JOIN Mail_OwnedBlocks m ON m.BlockID=b.BlockID WHERE m.Record_RecordID=<ID> ORDER BY m.BlockTag;"
   ```

4. Extract the PDF (the `.olk15MsgAttachment` file is a binary header + base64 PDF):
   ```python
   import base64, re
   with open('file.olk15MsgAttachment', 'rb') as f:
       data = f.read()
   idx = data.find(b'JVBER')  # base64-encoded PDF start
   b64 = re.sub(r'[^A-Za-z0-9+/=]', '', data[idx:].decode('ascii', errors='ignore'))
   pdf = base64.b64decode(b64)
   with open('output.pdf', 'wb') as out:
       out.write(pdf)
   ```

### Excel comparison sheet styling

When building the Excel workbook with `openpyxl`, use this style pattern for procurement comparison sheets:

| Element | Style |
|---------|-------|
| Title row | Dark navy fill (`#1F3864`), white 14pt bold, centered |
| Subtitle | 9pt italic gray, centered |
| Column headers | Dark blue fill (`#1F4E79`), white 11pt bold, centered |
| Spec label column | Bold navy 10pt, light gray fill (`#F2F2F2`) |
| Data cells | 10pt Calibri, centered, alternating rows (`#E9EFF7`) |
| Total rows | Yellow fill (`#FFF2CC`), bold navy 11pt, medium navy borders |
| Section dividers | 6pt blank rows, or gray "——— PRICING ———" row |
| Borders | Thin `#B4C6E7` for regular, medium `#1F3864` for total rows |
| Freeze panes | `ws.freeze_panes = 'B5'` (column label + row header) |
| Orientation | Landscape, fit to page |
| Row heights | 22-28pt for data, 30-36pt for totals/title, 55pt for contact rows |

For detailed guidance on number formatting (values not text), formulas for calculated totals, balanced vendor tabs, and recommendation sheet style, see the **supplier-procurement-lifecycle** skill's Phase 2 "Excel Comparison Sheet Standards" section.

Multi-sheet pattern:
- **Sheet 1** "Comparison" — side-by-side spec + price table
- **Sheet 2** "Software Options" (or "{Category} Options") — optional add-ons
- **Sheet 3** "Contacts" — vendor contact info with company, person, email/phone, product

### Spec Verification Against Official Brochures

When a vendor quotation claims specs that seem inconsistent (e.g., model name says "200m" but overview says "400m"), cross-reference against the manufacturer's official brochure PDF:

1. **Extract brochure text** — use `pdftotext -layout` on the official manufacturer brochure PDF
2. **Find the spec table** — section usually titled "Performance Specifications" or "Technical Data". Look for a table comparing multiple model variants side by side.
3. **Cross-reference three levels of claims:**
   - **Quotation title** — what the vendor calls the product
   - **Quotation overview text** — marketing language (often copy-pasted from a more expensive model)
   - **Quotation spec table** — the technical rows (range, accuracy, weight)
4. **Identify model variant** — official brochures often list multiple models (e.g., Focus Core 100m, Focus Premium 200m, Focus Premium Max 400m). Map the quotation's spec table values against the brochure's model columns.
5. **Prefer the spec table** — the quotation's spec table (range, weight, accuracy) is more reliable than the overview text. The overview is marketing copy-paste.

**Common red flags:**
- Overview mentions specs from a higher-tier model (e.g., "400m range") but spec table shows lower values (e.g., "200m")
- Title says one model variant but price matches a different tier
- Weight differs between quotation and brochure (indicates spec sheet copy-paste from wrong variant)
- Vendor renames the manufacturer's model (e.g., "Faro Premium 200m" instead of "Faro Focus Premium")

### Excel Column Reordering with openpyxl

When reordering columns in an existing comparison sheet (e.g., sorting products by range ascending):

1. **Buffer all data first** — read every cell's value + formatting (font, alignment, fill, border, number_format) into a dict keyed by column letter
2. **Skip merged cell sub-cells** — rows covered by merge ranges (e.g., A1:F1) cannot be written to individually. Their data is already in the anchor cell (A1). Check `ws.merged_cells.ranges` before writing.
3. **Write in new order** — iterate the new column sequence, set values + copy all stored formatting attributes
4. **Copy column widths** — `ws.column_dimensions[new_col].width = ws.column_dimensions[old_col].width`

```python
# Pattern
buf = {}
for old_col in ['B','C','D','E','F']:
    buf[old_col] = {}
    for r in range(1, ws.max_row + 1):
        cell = ws[f'{old_col}{r}']
        buf[old_col][r] = {
            'value': cell.value,
            'font': copy(cell.font),
            'alignment': copy(cell.alignment),
            'fill': copy(cell.fill),
            'border': copy(cell.border),
            'number_format': cell.number_format,
        }

# Write new order
for new_col, old_col in [('B','E'), ('C','F'), ('D','C'), ('E','D'), ('F','B')]:
    for r in range(1, ws.max_row + 1):
        if r in merged_rows:  # skip merged cell sub-cells
            continue
        data = buf[old_col][r]
        ws[f'{new_col}{r}'].value = data['value']
        # ... copy formatting ...
```

**Pitfall:** `copy(cell.fill)` on merged cell sub-cells raises `AttributeError` because `MergedCell` objects are read-only. Check merged ranges before accessing sub-cells.

### Folder convention

```
Lidar_Scanning_Services/
├── README.md
├── Product_Name_A/
│   └── Quotation_Product_A.pdf
├── Product_Name_B/
│   ├── Quotation_Product_B.pdf
│   └── Brochure_Product_B.pdf
└── Product_Name_C/
    └── Proposal_Product_C.pdf
```

Each product folder is self-contained with its quotation and brochure. Use a top-level README as the index.

## Pitfalls

- Do NOT specify a brand unless the spec mandates it (NRS spec P21 §122: "Single approved manufacturer or system supplier — to be confirmed")
- Always note if CG has rejected a material substitution (e.g., patinated brass vs powder coat)
- Quantities are estimates from BOQ — note "Verify against latest schedule before ordering"
- Fire certification must be confirmed per SBC Chapter 7
- For bilingual docs: ensure Arabic text is properly RTL-set, not just right-aligned
- When the user says "subcontractor will handle" — do NOT create a purchasing pack for that item
