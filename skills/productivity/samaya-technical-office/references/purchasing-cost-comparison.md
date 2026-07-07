# Purchasing Cost Comparison — Vendor Quote Analysis

## When to use

A vendor/subcontractor quote arrives (or multiple quotes for the same item). You need to:

- Compare prices, specs, and terms across vendors
- Update an existing cost-comparison spreadsheet with actual quoted prices
- Simplify an overly verbose cost-comparison document
- Produce a clean side-by-side summary for procurement decision

## Workflow

### Step 1: Read existing spreadsheet structure

Always understand the source file before modifying:

```python
import openpyxl
wb = openpyxl.load_workbook(path)
print("Sheets:", wb.sheetnames)
for s in wb.sheetnames:
    ws = wb[s]
    print(f"  {s}: {ws.max_row}r x {ws.max_column}c, merged={list(ws.merged_cells.ranges)}")
```

Note: **openpyxl is NOT available in `execute_code` sandbox**. Use terminal with the system python3:

```bash
python3 -c "
import openpyxl
wb = openpyxl.load_workbook('/tmp/file.xlsx')
print(wb.sheetnames)
"
```

### Step 2: Extract PDF quote data

Use `pdftotext` to pull text from quotation PDFs:

```bash
pdftotext "/path/to/quotation.pdf" - | head -200   # skim intro
pdftotext "/path/to/quotation.pdf" - | tail -200   # get pricing
```

Key fields to extract from every quote:
- **Vendor name** & contact info (phone, email, address)
- **Quote reference number** and date
- **Model name/number** quoted (may differ from what was assumed!)
- **Unit price** and **total price** (note currency: SAR vs USD)
- **Discounts** applied
- **VAT** — included or quoted separately
- **Delivery / lead time**
- **Warranty** and included accessories
- **Payment terms** (advance, milestone, etc.)
- **Validity period**

### Step 3: Identify model discrepancies

Compare what the spreadsheet *assumes* is being quoted against what the vendor *actually* quoted. Common mismatches:

| Assumed in spreadsheet | Actually quoted | Action |
|---|---|---|
| EinScan HX2 | FreeScan COMBO+ | Different model by same manufacturer — note and request alternative quote if needed |
| HandySCAN 307 | Go!SCAN SPARK | Different Creaform product line — update model name and ask for HandySCAN quote separately |
| Space Spider (Gen 1) | Space Spider II | Model revision — update specs and pricing |

Document these explicitly in the output — the user needs to know.

### Step 4: Simplify spreadsheet structure

From → To guide:

| Over-verbose pattern | Simplified replacement |
|---|---|
| Separate "Project Requirements" sheet (scope info) | Omit — not a cost comparison concern |
| "Scanner Selection" with ratings/stars | Merge into Summary table — hard data only |
| "Distributors" with 4 priority levels | Trim to key vendors with active quotes |
| Separate "Action Plan" + "Contacts" | Merge into single sheet |
| Two cost options (A/B) with formulas | Replace with actual vendor prices |

Aim for **3 sheets max**:
1. **Summary** — side-by-side comparison table (vendor, model, price, accuracy, key features, delivery)
2. **Quotes Detail** — line-by-line breakdown from each vendor's actual quotation
3. **Contacts & Action** — key vendor contacts + numbered procurement actions with status

### Step 5: Apply Samaya document styling

| Property | Value |
|---|---|
| Font | Calibri (body 10pt, headers 11pt bold) |
| Header fill | `#1E293B` (navy) with white text |
| Sub-headers | `#B01E2F` (Samaya red), bold 10pt |
| Body alignment | Left wrap for text, center for numbers/currency |
| Table border | Thin `#D0D0D0` |
| Notes | 9pt italic, `#666666` |
| Page setup | Landscape, fit to width |

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

hdr_font = Font(name='Calibri', bold=True, size=11, color='FFFFFF')
hdr_fill = PatternFill(start_color='1E293B', end_color='1E293B', fill_type='solid')
sub_font = Font(name='Calibri', bold=True, size=10, color='B01E2F')
body_font = Font(name='Calibri', size=10)
note_font = Font(name='Calibri', size=9, italic=True, color='666666')
thin_border = Border(
    left=Side(style='thin', color='D0D0D0'),
    right=Side(style='thin', color='D0D0D0'),
    top=Side(style='thin', color='D0D0D0'),
    bottom=Side(style='thin', color='D0D0D0')
)
```

### Step 6: Notes section

Always add a Notes section under the summary with:
- Each vendor's price calculation (base → discount → VAT → total)
- Any model name discrepancies (assumed vs quoted)
- Currency and delivery terms (ex-works, DDP, etc.)
- VAT applicability (15% KSA VAT for local purchases)

## Output format

### Summary sheet columns
`# | Vendor | Model | Price (with VAT) | Accuracy | Key Features | Delivery`

### Notes below summary
```
1. MAPTEC quote (Ref: X, Jun 2): SAR 75,000 - SAR 3,000 = SAR 72,000 + 15% VAT = SAR 82,800
2. GDS quote (Ref: Y, Jun 2): SAR 119,920 - SAR 11,992 discount + 15% VAT = SAR 124,117.20
3. 3DME quote (Ref: Z, May 25): $35,000 USD ex-works Dubai (customs by buyer)
4. IMPORTANT: [list any model name discrepancies found]
```

### Action items
| # | Action | Vendor | Target | Status |
|---|---|---|---|---|
| 1 | Request formal PO-ready proforma | Vendor A | This week | PENDING |
| 2 | Request alternative model quote | Vendor B | This week | PENDING |
...

## Pitfalls

- **openpyxl not in sandbox** — use `terminal(python3 -c "...")` not `execute_code`. The system python3 has openpyxl installed.
- **Quoted model ≠ assumed model** — always verify the exact model name from the PDF against what the spreadsheet says. Document the discrepancy.
- **Currency mismatch** — local KSA quotes in SAR, international quotes in USD. Show both. Use 3.75 conversion rate.
- **VAT handling** — SAR quotes typically include 15% VAT; USD quotes are ex-works/EXW. Note: "Add 15% Saudi VAT for local purchases" on EXW quotes.
- **Merged cells in source** — original spreadsheets have many merged cell ranges. Copying structure blindly preserves bloat — simplify instead.
- **pdftotext output quality** — some PDFs have poor text extraction (Arabic mixed in, missing tables). Always verify extracted prices against the visual PDF. Use `-layout` flag if needed.
- **File naming** — avoid "(1)" suffixes in filenames. Clean it when replacing.
