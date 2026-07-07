# Capitalization Register → Project Cost Classification

Pattern for reclassifying an IAS 16 capital asset register into operational execution categories (On-Site Work, Off-Site Manufacturing, AV/IT Equipment, Furniture, Indirect Costs) and cross-mapping to BOQ divisions.

## When To Use

The Finance department (e.g. MR Yosry) sends a cost capitalization register (رسملة تكلفة المشروع) containing all capitalized project costs per IAS 16. You need to reclassify these into categories that match how the project was actually executed — for review, comparison against BOQ, or reporting back to Finance.

## Source Data Shape

The capitalization register typically has 3-6 sheets:
1. **Asset Summary** (سجل الأصول) — 6-8 categories with total costs, useful lives, depreciation
2. **Depreciation Schedule** (جدول الإهلاك) — annual depreciation across 5-10 years
3. **Journal Entries** (القيود والملخص) — accounting entries for capitalization + first-year depreciation
4. **Asset Classification** (تصنيف الأصول) — DETAILED list of every invoice/item sorted by category, with date, document number, description, amount, and account code
5. **WIP 2025** — work-in-progress costs incurred before the capitalization date (typically in 2025) that rolled up into the January 2026 capitalization

## Reclassification Methodology

### Step 1: Analyze the Asset Classification sheet

The detail sheet has columns: Date, Document #, Description, Amount, Account Code, Asset Category, Useful Life.

Extract every line item and classify it into an EXECUTION category:

| Execution Category | What Goes Here | Typical Capitalization Categories |
|---|---|---|
| **On-Site Work** | Work executed at the museum location — MEP, civil works, finishes, painting, flooring, lighting, external works | Improvements & Decor (تحسينات وديكورات) |
| **Off-Site Manufacturing** | Items fabricated at workshops/factories then delivered — CNC panels, display models, metal fabrication | Improvements & Decor (fabrication items) |
| **AV & IT Equipment** | Equipment supply — projectors, screens, cameras, computers, network, media servers | Display & AV Equipment + Computers & IT |
| **Furniture & Fixtures** | Counters, seating, tables, carpets, cushions, decorative items | Furniture & Fixtures |
| **Tools, Materials & Consumables** | Small tools, hardware, building supplies, consumables | Tools & Materials (عدد وأدوات ومواد) |
| **Indirect Project Costs** | External labor, travel, accommodation, transport, meals, equipment rental | Indirect Project Costs |

### Step 2: Item-Level Classification Rules

Use Arabic keyword matching to classify each line item from the detail sheet:

| Keyword (Arabic) | Execution Category | Notes |
|---|---|---|
| كهرباء, ميكانيكا, لياسة, بورسلان, رخام, حجر, دهان, بويه, شبوك, حديد (تشكيل/تطعيج) | On-Site Work | Site installation work |
| خشب, اخشاب (supply only), فايبر, مجسم, نجارة (fabrication), ستيل (fabrication) | Off-Site Manufacturing | Items fabricated off-site |
| بروجكتر, شاشة, ميديا سيرفر, صوتيات, اضاءات (projection/AV type), كاميرا, هولوجرام | AV & IT Equipment | Equipment supply |
| كنب, موكيت, اثاث, طاولة, كاونتر, خيمة, اسقف (suspended), عشب | Furniture & Fixtures |
| عدد وادوات, مواد (consumables), مسامير, براغي | Tools & Materials |
| عمالة, أجور, سفر, تذكرة, سكن, نقل, شحن, مواصلات, اعاشة, ايجار معدات, مصاريف متنوعة | Indirect Costs |

### Step 3: Aggregate and Verify

Sum all items in each execution category, then verify against the original capitalization total:

```python
execution_total = sum(on_site + off_site + av_it + furniture + tools + indirect)
# Must equal the capitalization register's grand total
assert abs(execution_total - capitalization_total) < 1, "Totals don't match!"
```

### Step 4: Cross-Map to BOQ Divisions

The BOQ (Bill of Quantities) uses MasterFormat divisions. Map each BOQ division to the corresponding execution category:

| BOQ Division | Execution Category | Match |
|---|---|---|
| Div 6 — Wood & Plastics | On-Site Work (installation) + Off-Site Mfg (fabrication) | Split by nature |
| Div 8 — Openings | On-Site Work | ✅ |
| Div 9 — Finishes | On-Site Work | ✅ |
| Div 10 — Specialties | On-Site Work | ✅ |
| Div 11 — AV Equipment | AV & IT Equipment | ✅ |
| Div 12 — Furnishings | Furniture & Fixtures | ✅ |
| Div 13 — Special Construction | On-Site Work | ✅ |
| Div 26 — Electrical | On-Site Work | ✅ |
| Div 27 — Communications | AV & IT Equipment | ✅ |

**Note:** If the BOQ is unpriced (zero rates), the mapping is qualitative only — cannot verify cost amounts.

### Step 5: Handle Late Additions

If the capitalization register includes items after the capitalization date (e.g. POs dated after 01-Jan-2026):
- Flag these separately — they need a supplementary capitalization entry
- They are NOT in the original depreciation schedule
- Estimate their additional annual depreciation: `amount / useful_life`

## Excel Output Structure

Generate a 6-sheet workbook:

| Sheet | Content |
|---|---|
| Cost Classification Summary | 7 categories with amounts, %, notes |
| 1-On-Site Work | 10 sub-categories with item breakdown |
| 2-AV-IT-Equipment | 10 line items with descriptions |
| 3-Indirect-Costs | 8 categories with descriptions |
| 4-BOQ-Mapping | BOQ divisions mapped to capitalization |
| 5-Depreciation | Original depreciation schedule |

Format: Navy headers (#1E293B), alternating rows (#F1F5F9), #,##0 number format, 11pt Calibri.

## Key Verifications to Flag

Always check these when reviewing a capitalization register:

1. **BOQ rates vs actual costs** — if BOQ is unpriced, note that cost accuracy cannot be verified
2. **Late additions** — items after the capitalization date may need separate treatment
3. **AV Equipment scope gap** — compare capitalized AV costs vs BOQ line items (BOQ may be missing detail)
4. **Indirect costs ratio** — 6-8% is typical for IAS 16 capitalization; higher may need justification
5. **Useful lives** — verify they match IAS 16 guidelines (buildings 10-30yrs, equipment 5yrs, IT 3-5yrs, furniture 7yrs)
