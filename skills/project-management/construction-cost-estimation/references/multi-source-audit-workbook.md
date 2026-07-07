# Multi-Source Pricing Audit Workbook

## Purpose

Standardised Excel workbook that audits every BoQ item against 3-4 independent market price sources. Color-coded verdict per item enables quick negotiation targeting.

## Workbook Structure

| Sheet | Contents |
|-------|----------|
| AUDIT SUMMARY | Color-coded dashboard — counts per sheet, totals by verdict |
| AV Hardware | Epson, QSC, Crestron, Brightsign, Cisco, Eaton — 3-4 sources each |
| AV Productions | Content creation, media production |
| Lighting EX | Exhibition lighting w/ Italian list prices |
| Lighting SUP | Supporting area lighting |
| AV Graphics | Print graphics, signage |
| LED Walls | LOPU, Muxwave — Alibaba FOB, bulk, factory direct |
| Furniture | Calligaris, B&B Italia, Poltrona Frau — EU list, retailer, contract |
| Exhibition Galleries | Gallery fit-out, finishes — KSA market |
| Supporting Areas | Construction, ceilings, floors, paint — KSA market |
| Showcases & Objects | Display cases, artifacts, models |
| Materials & Finishes | Raw materials |

## Item Columns (22 per row)

| # | Column | Purpose |
|---|--------|---------|
| 1 | Item ID | Unique ref from BoQ |
| 2 | Category | Work package (AV, Lighting, etc.) |
| 3 | Subcategory | Finer grouping |
| 4 | Description | Full item name + spec |
| 5 | Qty | Quantity |
| 6 | Unit | m², pcs, lm, etc. |
| 7 | BoQ Unit Rate ($) | Consultant's price — the target being audited |
| 8-10 | Source 1: Name / Price ($) / Reference | Manufacturer list price |
| 11-13 | Source 2: Name / Price ($) / Reference | Distributor/reseller price |
| 14-16 | Source 3: Name / Price ($) / Reference | Online retail / Alibaba / market |
| 17-19 | Median / Low / High ($) | Range statistics from sources |
| 20 | BoQ vs Median (%) | Variance = (BoQ − median) / median × 100 |
| 21 | Verdict | Color-coded: OVERPRICED / SLIGHTLY HIGH / FAIR / UNDERPRICED / UNVERIFIED |
| 22 | Action / Recommendation | Specific negotiation target or research note |

## Verdict Logic

| Condition | Verdict | Fill | Action |
|-----------|---------|------|--------|
| BoQ > median +30% | OVERPRICED | 🔴 Red | Negotiate down. Get 3 quotes. Target median. |
| BoQ > median +15% | SLIGHTLY HIGH | 🟡 Amber | Target 85% of BoQ. Cross-check spec. |
| BoQ within ±15% of median | FAIR | 🟢 Green | Accept. Within market range. |
| BoQ < median −30% | UNDERPRICED | 🟢 Green | RISK — verify spec/quality. Market is higher. |
| BoQ < median −15% | SLIGHTLY LOW | 🟢 Green | Confirm specification match. |
| No source data | UNVERIFIED | ⬜ Gray | Needs market research. |

## Source Strategy by Import Category

### EU Import (×1.33 landed multiplier)
**Brands:** DGA, FLOS, Calligaris, B&B Italia, Poltrona Frau, Molteni&C, Draenert, NORR11, LAGO, ACERBIS, BK CONTRACT, ARTEMEST, LUXAM, Prolights, Visual Production, Enttec

**Sources:**
1. **Manufacturer list price** — brand website EUR or USD
2. **European design retailer** — design store 15-25% below list
3. **Contract quantity** — 68 chairs = −40%; 26 chairs = −45%

### US Import (×1.25 landed multiplier)
**Brands:** Epson, QSC, Crestron, Brightsign, Cisco, Eaton, Chief, Iiyama

**Sources:**
1. **B&H Photo Video** — current USD retail
2. **Markertek / CDW** — pro AV dealer pricing
3. **Manufacturer MSRP** — official list price

### China Import (×1.20 landed multiplier)
**Brands:** LOPU, Muxwave, Brainsalt

**Sources:**
1. **Alibaba FOB** — per-piece factory price (10 pcs minimum)
2. **Alibaba bulk** — 100+ pcs FOB (cheapest)
3. **Factory direct CNY** — Chinese domestic price (hard to verify remotely)

### Local KSA (×1.00)
**Items:** installation, labour, civil, paint, gypsum, drywall, MDF, stone

**Sources:**
1. **KSA supplier quote** — local distributor
2. **Project benchmark** — previous Samaya project rate
3. **Saudi Building Cost Index** — published KSA rates

## Openpyxl Implementation Pattern

```python
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

# Styles
hdr_font = Font(bold=True, size=9, color='FFFFFF')
hdr_fill = PatternFill('solid', fgColor='1F4E79')
green_fill = PatternFill('solid', fgColor='C6EFCE')
yellow_fill = PatternFill('solid', fgColor='FFEB9C')
red_fill = PatternFill('solid', fgColor='FFC7CE')
gray_fill = PatternFill('solid', fgColor='D9D9D9')
thin_border = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin'))

HEADERS = [
    'Item ID', 'Category', 'Subcategory', 'Description', 'Qty', 'Unit',
    'BoQ Unit Rate ($)',
    'Src 1: Name', 'Src 1: Price ($)', 'Src 1: Reference',
    'Src 2: Name', 'Src 2: Price ($)', 'Src 2: Reference',
    'Src 3: Name', 'Src 3: Price ($)', 'Src 3: Reference',
    'Median Market ($)', 'Low ($)', 'High ($)',
    'BoQ vs Median (%)', 'Verdict', 'Action / Recommendation']

def create_audit_sheet(ws, title, item_list, sources_by_keyword):
    ws.title = title[:31]
    # Header row
    for c, h in enumerate(HEADERS, 1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.font = hdr_font
        cell.fill = hdr_fill
        cell.alignment = Alignment(wrap_text=True, vertical='top')
        cell.border = thin_border
    # ... iterate items, match sources, write rows, apply verdict logic
    
def find_sources(desc, source_dict):
    desc_lower = str(desc).lower() if desc else ''
    for keyword, sources in source_dict.items():
        if keyword in desc_lower:
            return sources
    return []

# Each source is a (price, source_name, reference_note) tuple
SOURCES = {
    'lopu': [(600, 'Alibaba avg LOPU', 'FOB ~$400-800 depending on model'),
             (500, 'Alibaba bulk', '100+ pcs FOB'),
             (650, 'Absen competitor', 'Similar spec Chinese brand')],
    'calligaris': [(1000, 'Calligaris EU list', 'Dining chair €800-1,200'),
                   (750, 'EU design retailer', 'Retail -25%'),
                   (600, 'Contract qty', '68 chairs at -40%')],
    # ... etc per item
}

# Auto-colour the verdict cell
verd_fills = {
    'OVERPRICED': red_fill,
    'SLIGHTLY HIGH': yellow_fill,
    'FAIR': green_fill,
    'UNDERPRICED': green_fill,
    'SLIGHTLY LOW': green_fill,
    'UNVERIFIED': gray_fill,
}
```

## Category-to-Sheet Mapping (Exhibition)

| BoQ Category | Sheet | Source Type |
|-------------|-------|-------------|
| AV Hardware (branded) | AV Hardware | US/EU market prices |
| AV Hardware (LED walls) | LED Walls | Alibaba FOB + bulk |
| AV Productions | AV Productions | KSA market |
| Graphics | AV Graphics | KSA print shops |
| Showcases | Showcases & Objects | KSA fabricators |
| Objects/Models | Showcases & Objects | KSA fabricators |
| EX Lighting (DGA/FLOS/LUXAM) | Lighting EX | Italian EUR list prices |
| SUP Lighting (DGA/FLOS/LUXAM) | Lighting SUP | Italian EUR list prices |
| Exhibition Galleries | Exhibition Galleries | KSA fit-out rates |
| Supporting Areas | Supporting Areas | KSA construction rates |
| Materials | Materials & Finishes | KSA material prices |
| (furniture keywords) | Furniture | EU retailer + contract |

## Summary Dashboard

Auto-generated from reading all sheet verdict columns:

| Sheet | Items | OVERPRICED | SLIGHTLY HIGH | FAIR | UNDERPRICED | SLIGHTLY LOW | UNVERIFIED |
|-------|-------|------------|---------------|------|-------------|--------------|------------|
| AV Hardware | 97 | 23 | 5 | 8 | 1 | 2 | 58 |
| Grand Total | 519 | 91 | 11 | 19 | 1 | 3 | 136 |

Color-coded: red fills for overpriced columns, green for fair/underpriced, gray for unverified.

## Confidence Levels (Item-Level)

Recorded in an EVIDENCE sheet or Notes column:

| Level | Criteria | Color |
|-------|----------|-------|
| HIGH | Known brand + model with searchable market price from 3 sources | Green |
| MEDIUM | Generic description with inferred market range from 2 sources | Amber |
| LOW | Provisional sum, PC sum, or unique item with no comparable | Red |
