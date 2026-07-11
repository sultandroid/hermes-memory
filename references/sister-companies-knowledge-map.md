# Sister Companies Knowledge Map — Comprehensive Index

> **Generated:** 2026-07-11  
> **Auditor:** Hermes Agent  
> **Purpose:** Single-entry index linking all Sister Companies project documentation, specs, reports, and canonical knowledge.  
> **Location:** `Reports/Sister_Companies/` (OneDrive — Windows)  
> **Agent repo:** `~/hermes-memory/references/sister-companies-knowledge-map.md`

---

## 1. Project Overview

**13 sister company projects** (stores, coffee shops, visitor center) under Samaya Investment. Full cost reallocation and restructuring using accounting invoices (Ibrahim Shaban) + factory cost records (FCA files).

| Code | Project | Area m² | Location | Status |
|:----:|:--------|:-------:|:---------|:-------|
| 01 | Al Wahi Gift Shop | 240 | Makkah — Jabal Alnoor | ✅ Complete |
| 02 | Holy Quran Gift Shop | 194 | Makkah | 🔴 Needs .xls→.xlsx restructure |
| 03 | Qahwatna Cafe (Hira) | 77.5 | Makkah | ✅ Complete |
| 04 | Hira Cafe (Cave) | 398 | Makkah | 🔴 Needs .xls→.xlsx restructure |
| 05 | Jabal Omar VIP Stores | 67 | Makkah | ⚠️ Needs item type + sections |
| 06 | As Safiyyah Giftshop | 445 | Madinah | 🔴 Needs data entry from PDFs |
| 07 | Khair Al-Khalq Museum Store | 173 | Makkah | ✅ Complete |
| 08 | Qahwatna Al-Safiya Cafe | 26 | Madinah | ⚠️ Needs item type column |
| 09 | Tzkarat Store | 51 | Makkah | ✅ Complete (dual file cleanup needed) |
| 10 | Rateeb Store | 42 | Makkah | ⚠️ Needs item type column |
| 11 | Najdi Coffee | 173 | Makkah | ⚠️ Needs item type column |
| 12 | Ice Coffee Shop | — | Makkah | ⚠️ Needs item type column |
| 13 | Hera Visitor Center | — | Makkah | ⚠️ Needs item type + formulas |

### Key Data Sources
- **Source A (Accounting):** Ibrahim Shaban email files (`من ايميل ابراهيم` in filenames)
- **Source B (Factory):** `*_Factory_Cost_Analysis.xlsx` files — labour hours + POs
- **Source C (System):** Rukovoditel PMS (Sysleaders/Factory ERP System) REST API data

---

## 2. File Inventory — All MD Files

### 2.1 Root Level

| File | Type | Key Content | Last Status |
|------|------|-------------|-------------|
| `Sister_Companies_Project_Plan.md` | **Executive Plan** | Completed cross-project reallocation (10 transfers), file restructure (9 files), item type classification. Remaining: 5 priority groups across 25 tasks. | Current |

### 2.2 _Management (Active MD Files)

| File | Type | Key Content | Last Status |
|------|------|-------------|-------------|
| `_Management/Audit_and_Task_Plan.md` | **Operational Audit** | Per-store audit (8 criteria), 25 delegation tasks across 5 phases, technical notes, priority map. References old macOS paths. | Current |
| `_Management/Factory_Labour_Topup_Memory.md` | **🔒 Internal Only** | Budget top-up calculation (factory labour folded into construction). DO NOT SHOW in deliverables. Shows 1.24M SAR total top-up across projects. | Current |
| `_Management/Invoice_Classification_Report.md` | **Classification Data** | Per-store invoice line item breakdown by work type (General, Labor, Wood, etc.). Shows ~102 lines across stores. | Current |
| `_Management/Factory_Scope_Analysis.md` | **System Data** | Rukovoditel PMS data: 2,030 labour records, 16,084h, 180,692 SAR labour cost, 627,666 SAR POs, 39,550 SAR fleet cost. 12 projects analyzed. Generated 2026-06-10. | Current |

### 2.3 _Management/specs/financial-cost-analysis-reporting/

| # | File | Purpose |
|:-:|------|---------|
| 00 | `00-brief.md` | **Project brief** — business need, deliverables, non-negotiable controls. References old macOS OneDrive paths. |
| 01 | `01-data-sources.md` | **Data source definitions** — accounting, factory, labor, supervision, management Excel files. |
| 02 | `02-workflow.md` | **8-stage workflow** — inventory → invoice review → classification → summary → factory analysis → budget vs actual → reconciliation → final report. |
| 03 | `03-classification-rules.md` | **Classification taxonomy** — 14 work categories, raw material detection, building material logic, confidence levels, review statuses. |
| 04 | `04-analysis-reconciliation.md` | **Reconciliation rules** — cost build-up layers, installation labor estimation, supervision cost, 9 reconciliation checks, tolerance rules. |
| 05 | `05-report-output.md` | **Report output spec** — 12-section report, 10-sheet workbook structure, Store_Costs template (preferred), minimum columns per sheet. |
| 06 | `06-acceptance-checklist.md` | **QA checklist** — 55 checks across source data, invoices, classification, labor, factory, supervision, reconciliation, final report. |
| 07 | `07-tasks.md` | **Implementation tasks** — 7 phases (Setup → Data Import → Classification → Factory → Budget → Reconciliation → Reporting). |
| 08 | `08-governance-and-controls.md` | **Governance** — roles, segregation of duties, version control, access control, exception escalation. |
| 09 | `09-excel-style-guide.md` | **Style guide** — Format A (Store_Costs, preferred) & Format B (Full Report), colors, status fills, controls per sheet. |
| 10 | `10-store-costs-template.md` | **Store_Costs template** — 2-sheet workbook (cost register + work analysis), column layout, standard categories, PO tracking. |

### 2.4 _Management/Financial_Cost_Analysis_Reports/

| File | Type | Key Content |
|------|------|-------------|
| `Draft_Work_Type_Classification_Report.md` | **First-Pass Analysis** | 1535 rows classified across 14 projects. 32 workbooks scanned. 438 unclassified (refined later). Generated 2026-06-10 04:42. |
| `Refined_Classification_Report.md` | **Second-Pass Refinement** | Reduced unclassified from 438→219. Per-project category breakdown with safe amounts. |
| `Factory_Analysis_Report.md` | **Factory Cost Analysis** | Factory breakdown per project, double-counting check (no material duplicates), budget vs actual comparison, verified values for classification. |

---

## 3. Relationship Map

```
Sister_Companies_Project_Plan.md          ← Executive overview (what's done, what's left)
         │
         ├──► Audit_and_Task_Plan.md      ← Operational breakdown of remaining work (25 tasks)
         │         │
         │         └──► 7 Tasks MDs (specs/)  ← Methodology executed by each task
         │
         ├──► Factory_Scope_Analysis.md   ← Raw system data from Rukovoditel
         │
         ├──► Invoice_Classification_Report.md  ← Raw classification view
         │
         ├──► Factory_Analysis_Report.md  ← Factory cost verdict + double-counting check
         │
         ├──► Draft_Classification.md → Refined_Classification.md  ← Classification pipeline
         │
         ├──► Factory_Labour_Topup_Memory.md  ← 🔒 Budget reconciliation (internal only)
         │
         └──► specs/
              ├── 00-brief.md              ─┐
              ├── 01-data-sources.md        │
              ├── 02-workflow.md            │
              ├── 03-classification-rules.md│── Methodology framework
              ├── 04-analysis-reconciliation.md│  (how to analyze)
              ├── 05-report-output.md       │
              ├── 06-acceptance-checklist.md│
              ├── 07-tasks.md               │
              ├── 08-governance-and-controls.md│
              ├── 09-excel-style-guide.md   ─┘
              └── 10-store-costs-template.md  ← Preferred output format
```

### Hermes-Memory Cross-References

The agent repo (`~/hermes-memory/`) already contains:

| Reference | Location | Relationship |
|-----------|----------|--------------|
| `sister-companies-project-folders.md` | `skills/productivity/bulk-file-organization/references/` | Folder setup workflow (step-by-step) |
| `sister-companies-costing-methodology.md` | `skills/productivity/samaya-technical-office/references/` | Costing methodology (12 projects, 6-step process) |
| `project-cost-reconciliation/` | `skills/project-management/` | Full reconciliation skill (5 rules, file structure, pitfalls) |
| `ibrahim-shaaban-extraction-2026-06.md` | `skills/email/outlook-email/references/` | Ibrahim's email invoice extraction workflow |

---

## 4. Duplicate / Outdated Content

### 4.1 _Archive Folder

| Archive File | Current Equivalent | Verdict |
|-------------|-------------------|---------|
| `_Archive/specs/financial-cost-analysis-reporting/*.md` (9 files) | `_Management/specs/financial-cost-analysis-reporting/*.md` (11 files) | 🟡 **OUTDATED** — Archive lacks Store_Costs template additions (00-brief, 05-report-output, 06-checklist, 09-style-guide were updated). Missing `10-store-costs-template.md` which only exists in _Management. |
| `_Archive/_Management/Financial_Cost_Analysis_Reports/Draft_Work_Type_Classification_Report.md` | Identical to `_Management/Financial_Cost_Analysis_Reports/Draft_Work_Type_Classification_Report.md` | 🔴 **EXACT DUPLICATE** — Same content (same timestamp 2026-06-10 04:42). Safe to remove. |

**Recommendation:** 
- Delete `_Archive/_Management/Financial_Cost_Analysis_Reports/Draft_Work_Type_Classification_Report.md` (exact duplicate)
- Keep `_Archive/specs/` as is or tag as `DEPRECATED — see _Management/specs/`

### 4.2 Outdated Paths

| File | Issue | Fix Needed |
|------|-------|------------|
| `_Management/Audit_and_Task_Plan.md` | Line 64: `BASE = /Users/mohamedessa/...` | Should be `BASE = /c/Users/user/...` |
| `_Management/specs/00-brief.md` | Lines 23-24: `/Users/mohamedessa/Library/CloudStorage/...` | Should be `C:\Users\user\OneDrive - SAMAYA INVESTMENT\...` |

### 4.3 Stale Notes

| File | Note | Status |
|------|------|--------|
| `Factory_Labour_Topup_Memory.md` | Line 38: "Overhead is still to be added." | 🟡 May now be resolved — needs verification |
| `Factory_Analysis_Report.md` | Line 177: "Cost_Classification_By_Work_Type.xlsx needs update with actual values" | 🟡 May have been done since report generated |

---

## 5. Key Data Summary

### 5.1 Total Project Costs (from Labour Top-Up Memory)

| # | Project | Direct Construction | Factory Top-Up | Works Shown | Budget | Grand Total |
|:-:|:--------|-------------------:|:--------------:|------------:|------:|-----------:|
| 01 | Al Wahi | 252,124 | 201,244 | 453,368 | 478,580 | 478,580 |
| 02 | Holy Quran | 95,763 | 114,129 | 209,892 | 219,468 | 219,468 |
| 03 | Qahwatna | 170,211 | 0 | 170,211 | 170,773 | 187,232 |
| 04 | Hira Cafe | 1,138,584 | 200,322 | 1,338,906 | 1,452,764 | 1,452,764 |
| 05 | Jabal Omar | 144,432 | 447,247 | 591,679 | 606,122 | 606,122 |
| 06 | As-Safiyyah | 350,772 | 0 | 350,772 | 334,157 | 385,849 |
| 07 | Khair Al-Khalq | 96,281 | 0 | 96,281 | 13,369 | 105,909 |
| 08 | Qahwatna Al-Safiya | 73,118 | 321 | 73,439 | 80,751 | 80,751 |
| 09 | Tzkarat | 101,917 | 31,058 | 132,975 | 143,167 | 143,167 |
| 10 | Rateeb | 55,097 | 197,933 | 253,030 | 258,540 | 258,540 |
| 11 | Najdi Coffee | 233,662 | 52,556 | 286,218 | 309,584 | 309,584 |
| 12 | Ice Coffee | 13,751 | 0 | 13,751 | — | 15,126 |
| | **TOTAL** | **2,725,712** | **1,244,810** | **3,970,522** | **4,067,275** | **4,243,092** |

### 5.2 Factory System Data (from Rukovoditel)

| Project | JN | Labour Records | Labour Hours | Labour Cost | PO Cost | Fleet Cost | Factory Total |
|---------|:--:|:-------------:|:-----------:|-----------:|-------:|:---------:|:------------:|
| Tzkarat | JN-64 | 43 | 374h | 4,250 | 16,982 | 0 | 21,232 |
| Rateeb | JN-67 | 22 | 196h | 2,481 | 39,970 | 0 | 42,450 |
| Jabal Alnoor Gift | JN-40 | 195 | 1,713h | 20,287 | 74,821 | 5,150 | 100,258 |
| Hera Cafe | JN-47 | 224 | 1,909h | 23,897 | 72,514 | 1,400 | 97,811 |
| ICE Coffee | JN-97 | 1 | 10h | 148 | 2,240 | 0 | 2,388 |
| As Safiyyah | JN-114 | 379 | 2,711h | 30,890 | 260,940 | 19,100 | 310,930 |
| Qahwatna Mecca | JN-129 | 0 | 0h | 0 | 8,500 | 0 | 8,500 |
| Najdi Coffee | JN-130 | 0 | 0h | 0 | 42,383 | 0 | 42,383 |
| Qahwatna Al-Safiya | JN-144 | 330 | 2,774h | 31,064 | 43,494 | 2,900 | 77,458 |
| Holy Quran | JN-152 | 658 | 4,922h | 51,856 | 59,412 | 11,000 | 122,268 |
| Khair Al-Khalq | JN-187 | 176 | 1,469h | 14,492 | 200 | 0 | 14,692 |
| Qahwatuna Jabal Omer | JN-213 | 2 | 6h | 119 | 0 | 0 | 119 |
| **TOTAL** | | **2,030** | **16,084h** | **180,692** | **627,666** | **39,550** | **847,908** |

### 5.3 Classification Pipeline Results

| Pass | Date | Lines | Unclassified | Improvement |
|------|------|:----:|:-----------:|:-----------|
| Draft (1st) | 2026-06-10 | 1,535 | 438 (28.5%) | Baseline |
| Refined (2nd) | 2026-06-10 | 1,535 | 219 (14.3%) | -219 reclassified |

### 5.4 Cross-Project Reallocations (Completed)

| From | To | Amount SAR | Rule |
|------|----|:---------:|------|
| Al Wahi (01) | Tzkarat (09) + Rateeb (10) | 82,437.50 | MEP 50%, area split 51:42 |
| Al Wahi (01) | Rateeb (10) + Hera VC (13) | 36,468.00 | MEP 30%, equal 50:50 |
| Al Wahi (01) | Tzkarat (09) + Rateeb (10) | 29,563.00 | Signage lettering, equal |
| Al Wahi (01) | Tzkarat (09) (partial) | 646.89 | Fire protection, area split |
| Hira Cafe (04) | Ice Coffee (12) | 29,549.00 | Billboard, full transfer |
| Jabal Omar (05) | Khair Al-Khalq (07) | 20,826.00 | Full transfer |
| Jabal Omar (05) | Al Wahi (01) | 1,583.00 | Full transfer |
| Jabal Omar (05) | Holy Quran (02) | 429.00 | Full transfer |
| Rateeb (10) | Tzkarat (09) | 9,824.79 | Cashier devices, equal split |
| Rateeb (10) | Hera VC (13) | 11,398.00 | Gypsum, Maska merged |

---

## 6. Remaining Work Status

### Phase 1 — Item Type Column (5 stores)
- [ ] 08 Qahwatna Al-Safiya 
- [ ] 10 Rateeb (has non-standard "Work Type" column to convert)
- [ ] 11 Najdi Coffee
- [ ] 12 Ice Coffee
- [ ] 13 Hera VC

### Phase 2 — Full Restructure (4 stores)
- [ ] 02 Holy Quran (.xls → .xlsx conversion needed)
- [ ] 04 Hira Cafe (.xls → .xlsx conversion needed)
- [ ] 05 Jabal Omar (complete partial: item types, factory cost, supervision)
- [ ] 06 As Safiyyah (data entry from PDFs)

### Phase 3 — Formula Conversion
- [ ] 09 Tzkarat (clean up dual-file issue — delete legacy English file)
- [ ] 13 Hera VC (convert hardcoded values to formulas)

### Phase 4 — Equipment/Operations Separation (13 stores)
- [ ] Extract Equipment → separate sheet per store
- [ ] Extract Operations → separate sheet per store

### Phase 5 — Master Summary Dashboard
- [ ] Build comprehensive dashboard across all 13 projects

---

## 7. Tasks & Status

This knowledge map was generated by scanning all 18 MD files in the project folder (root + _Management + specs + reports) plus 3 related skill files in hermes-memory. Total files analyzed: 21.

| Action | Status | Detail |
|--------|--------|--------|
| Scan MD files | ✅ | 18 files found and read |
| Evaluate content | ✅ | All categorized into 5 groups |
| Detect duplicates | ✅ | Archive/Draft_Report = exact duplicate; Archive/specs = older version |
| Find outdated info | ✅ | macOS paths in 2 files; stale overhead note |
| Extract new info | ✅ | Full data consolidation above |
| Create index | ✅ | This file |
| Update references | ⏳ | Next step |

---

## 8. Terminology & Conventions

| Term | Convention |
|------|-----------|
| "Sysleaders System" | Always → "Factory ERP System" in deliverables |
| Item types | Construction (إنشاءات) / Equipment (معدات) / Operations (تشغيلية) |
| Work categories | 14 standard (Woodwork, Decoration, Civil, MEP, Finishing, Metal, Glass, Signage, Furniture, Subcontractors, Logistics, Labor, General, Unclassified) |
| Supervision | 10% of (Accounting Total + Factory Cost) |
| Number format | `#,##0.00` |
| Header style | Navy `#1E293B`, white bold Calibri |
| Naming | `{Code}_{EnglishName}.xlsx` for main file |
| Report outputs | `_Management/Financial_Cost_Analysis_Reports/` |
