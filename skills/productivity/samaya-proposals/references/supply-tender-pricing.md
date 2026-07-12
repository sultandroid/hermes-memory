# Supply Tender Costing Pattern (Non-Construction)

For **general supply tenders (توريد عام)** on Etimad or similar government platforms where the deliverable is a manufactured product rather than construction work.

## When to Use This Pattern

- User says "prepare a costing" or "price this tender" for a **manufactured/supplied product**
- The BOQ has a single line item or a few product items (not construction sections)
- The cost structure is: Materials + Hardware + Labor + Logistics + OH&P
- Examples: 400 wooden boxes, furniture pieces, equipment supply, uniforms

## How the Cost Model Differs from Construction BOQ

| Aspect | Construction BOQ (existing skill) | Supply Tender Costing |
|--------|----------------------------------|----------------------|
| Cost categories | Steel, civil, cladding, electrical, gates | Materials, hardware, labor, logistics |
| Item count | 10-12 items across 7-8 sections | 1-5 items, single section |
| Unit rates | Per m², per m, per pc | Per unit of product |
| OH&P loading | 1.30× on subtotal | 1.30× on direct cost |
| Excel sheets | BOQ + Loaded + Notes | Cost Estimate + Pricing Summary + Tender Info |
| Pricing per unit | Rarely needed | Critical (unit price drives bid) |

## Cost Structure Template

Build Excel with **4 direct-cost categories** + OH&P loading:

### A. Raw Materials
Calculate material quantities from product dimensions:
- Surface area from 3D dimensions (m² → multiply by material thickness for volume)
- Per-unit consumption (e.g., m² of wood per box, L of paint per unit)
- Waste factor (typically 5-10% for wood, accounted in qty)

| # | Item | Unit | Qty/Unit | Rate (SAR) |
|---|------|------|----------|-----------|
| 1 | High-quality material (e.g., wood) | m² | 3.5 | 180 |
| 2 | Treatment/preservative | L | 0.3 | 45 |
| 3 | Finish (paint/varnish) | L | 0.5 | 35 |
| 4 | Fixings (screws, nails, adhesives) | set | 1 | 15 |

### B. Hardware & Fittings
All mechanical components per product unit:
- Hinges, locks, handles, brackets, wheels, fasteners

### C. Labor & Manufacturing
Estimate hours per production step × labor rate:
- Cutting/assembly, finishing/painting, hardware installation, packaging
- Use KSA general labor rates (~25-35 SAR/hr)

### D. Logistics & Delivery
- Transport from factory to delivery city (per-unit share)
- Loading/unloading
- Site delivery

### E. OH&P Loading
Standard Samaya loading: 8% supervision + 10% overhead + 12% profit = **1.30× factor**

## Excel Workbook Structure (3 Sheets)

### Sheet 1: Cost Estimate
Full itemised breakdown with formulas:
```
# | Item | Unit | Qty/Box | Rate | Total/Box | Total 400
--|------|------|---------|------|-----------|----------
1 | Wood | m²   | 3.5     | 180  | =D*E      | =F*400
...
   Subtotal A | =SUM(F...)
   Subtotal B | =SUM(F...)
TOTAL DIRECT COST
OH&P 8% / 10% / 12%
LOADED UNIT PRICE
VAT 15%
GRAND TOTAL
```

### Sheet 2: Pricing Summary (Formal Submission)
Single-line BOQ matching the tender format:
- Item description (bilingual AR/EN verbatim from tender)
- Unit, Qty, Unit Price (loaded), Total
- Grand Total excl. VAT, VAT, Total incl. VAT
- Notes section: OH&P explanation, validity, warranty, payment terms

### Sheet 3: Tender Info
Reference sheet with all tender metadata:
- Client, contact, platform, tender URL
- Key dates (Hijri/Gregorian)
- Product specifications
- Delivery location
- Penalty clauses

## Key Pitfalls

1. **Etimad PDFs are standard templates with repetitive headers.** The actual BOQ data is embedded within 42+ pages of repeated header/footer blocks. Search for specific sections:
   - Section 7 (Sections 64-68): Scope of Work + BOQ
   - Section 8 (Sections 69-74): Technical Specifications
   - Section 68: جدول الكميات والأسعار (BOQ table)
   - Look for the product description near the only cell containing the quantity (e.g., "400")

2. **Hijri dates → convert to Gregorian** for timeline planning. Common 1448 dates:
   - 01/02/1448 ≈ 16 Jul 2026
   - 08/02/1448 ≈ 23 Jul 2026
   - 04/03/1448 ≈ 17 Aug 2026
   - 07/03/1448 ≈ 20 Aug 2026

3. **Single BOQ line required** — the tender BOQ has ONE line for the entire supply. Your formal price schedule should also be a single line item with unit price × quantity, not a breakdown. The cost breakdown stays in the Cost Estimate sheet.

4. **No bid bond** — some government tenders specify 0% bid bond. Check Section 41 (الضمان الابتدائي) before assuming a bond is required.

5. **Free tender documents** — check Section 3 (تكاليف وثائق المنافسة) for document costs before accounting for them in pricing.

6. **Penalty cap** — typically 20% of contract value for government tenders. Note in the Tender Info sheet.

7. **`pdftotext` works well for Arabic Etimad PDFs** — the text is embedded (not scanned), so pdftotext extracts clean Arabic text. Look past the repetitive template to find the actual specs.

## Formula Pattern in openpyxl

Use relative cell references in formulas so they auto-update when rows shift:

```python
cell(ws, row, 6, f'=D{row}*E{row}', num_fmt='#,##0.00')  # Total/box
cell(ws, row, 7, f'=F{row}*400', num_fmt='#,##0.00')     # Total 400 units
cell(ws, row, 6, f'=SUM(F{start}:F{end})', bold, num_fmt='#,##0.00')  # Subtotal
cell(ws, row, 6, f'=F{td_row}*1.3', bold, num_fmt='#,##0.00')  # Loaded price
cell(ws, row, 6, f'=F{loaded_row}*0.15', num_fmt='#,##0.00')   # VAT
cell(ws, row, 6, f'=F{loaded_row}+F{vat_row}', bold, num_fmt='#,##0.00')  # Grand total
```

## When to Use vs Not

**Use this pattern when:** The tender has a defined SPEC of a manufactured product — dimensions, materials, hardware — and the deliverable is "supply of X units to location Y."

**Do NOT use this pattern when:** The tender involves construction/installation at site, engineering design, or service contracts — those need the construction BOQ pattern in `BOQ-structure.md`.
