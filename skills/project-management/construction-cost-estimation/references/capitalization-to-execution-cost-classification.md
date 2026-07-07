# Capitalization Register → Execution Cost Classification

Reclassify MR Yosry-style capitalization registers (IAS 16 asset categories) into project execution categories (on-site work, off-site mfg, AV/IT, etc.).

## Source Format

MR Yosry's capitalization register typically has:

| Sheet | Content |
|-------|---------|
| سجل الأصول | 6 asset categories: Improvements & Decor, AV Equipment, Furniture, Computers & IT, Tools & Materials, Indirect Costs |
| تصنيف الأصول | 236+ individual invoice lines with date, invoice #, description, amount, account code, asset category, useful life |
| WIP 2025 | Running balance WIP during construction period |
| جدول الإهلاك | 10-year depreciation schedule |
| القيود والملخص | Journal entries for capitalization + annual depreciation |

## Classification Mapping

| Capitalization Category | Execution Category | Rationale |
|------------------------|-------------------|-----------|
| Improvements & Decor | On-Site Work | Installed at site: MEP, finishes, painting, flooring |
| AV Equipment | AV & IT Equipment | Off-the-shelf equipment supply |
| Furniture & Fixtures | Furniture & Fixtures | Usually off-site mfg at Samaya factory |
| Computers & IT | AV & IT Equipment | IT equipment supply |
| Tools & Materials | Tools & Materials | Consumables, small tools |
| Indirect Costs | Indirect Project Costs | IAS 16 — cost to bring asset to location |

## Excel Output Pattern

**Sheet 1: Detail** — individual items mapped to execution categories

| # | Category | Task ID | Item | Factory Cost | On-Site Install | Total Work | Overhead (12%) | Grand Total |

**Sheet 2: Summary Dashboard**

| Component | SAR | % |
|-----------|-----|---|
| A. Factory Manufacturing (Off-site) | xxx | 78% |
| B. On-Site Installation | xxx | 12% |
| C. Subtotal Direct Work | xxx | 89% |
| D. Allocated Overhead (12%) | xxx | 11% |
| E. GRAND TOTAL | xxx | 100% |

## On-Site Installation Rates (per category)

| Category | Rate | Rationale |
|----------|------|-----------|
| Wood & CNC | 18% | Carpentry install, fixing, finishing |
| Furniture | 12% | Assembly + placement |
| Metal & Steel | 15% | Welding/fixing to structure |
| Printing & Fabric | 8% | Hanging/placement only |
| 3D Models | 10% | Placement + securing |
| Signage | 15% | Mounting, alignment |
| Other | 10% | General |

## Overhead Allocation (12% of direct work)

| Item | % of Overhead |
|------|---------------|
| On-site supervision | 35% |
| Logistics & transport | 25% |
| Site support & coordination | 18% |
| Tools & consumables | 12% |
| QA/QC inspections | 10% |

## Key Flags to Watch

1. **Late additions** after capitalization date — supplementary capitalization entry needed
2. **BOQ rates empty** — can't verify cost accuracy without filled rates
3. **AV/IT scope** — capitalization often shows 1.15M SAR but BOQ may only have 2-3 line items
4. **Samaya factory works** — typically 41 MOs (manufacturing orders) in Odoo Off-site Mfg stage
5. **Unpriced BOQ** — qualitative mapping only, not quantitative verification
