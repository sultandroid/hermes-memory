# Sister Companies Costing Methodology (Samaya) — Updated

## Overview
Comprehensive cost reconciliation methodology for Samaya's sister company projects (stores, coffee shops, visitor center). Applied across 12 projects. Excludes museums/exhibitions — stores and cafes only.

## Project Scope (12 projects)
| Code | Project | Area (m²) | Location |
|:----:|:--------|:--------:|:--------:|
| 01 | Al Wahi Gift Shop | 240 | Makkah |
| 02 | Holy Quran Gift Shop | 194 | Makkah |
| 03 | Qahwatna Cafe | 77.5 | Makkah |
| 04 | Hira Cafe | 398 | Makkah |
| 05 | Jabal Omar VIP Stores | 67 | Makkah |
| 06 | As Safiyyah Giftshop | 445 | Madinah |
| 08 | Qahwatna Al-Safiya Cafe | 26 | Madinah |
| 09 | Tzkarat Store | 51 | Makkah |
| 10 | Rateeb Store | 42 | Makkah |
| 11 | Najdi Coffee | 173 | Makkah |
| 12 | Ice Coffee Shop | — | Makkah |
| 13 | Hera Visitor Center | — | Makkah |

> **📖 See also:** `~/hermes-memory/references/sister-companies-knowledge-map.md` — comprehensive index of all project MD files, classifications, factory data, reallocations, and remaining work.

## Cost Sources
1. **Accounting (Source A)** — Ibrahim Shaban email files (`من ايميل ابراهيم`). Raw invoice line items from bank statements or accounting system. May contain combined-project entries.
2. **Factory Cost (Source B)** — Internal workshop costs from `*_Factory_Cost_Analysis.xlsx` files: labor hours + purchase orders (POs).

## Methodology Steps (Project by Project)

### Step 1: Copy Original to Final Folder
- Use the pristine `- Original.xlsx` backup (NOT previously-modified versions)
- Place in `_Final/` folder with standardized name: `{Code}_{Project_Name}.xlsx`

### Step 2: Classify Every Line
- Add **Category** column (التصنيف): Transport, Fixtures, Wood & Carpentry, Metal Works, Paint, Glass, Electrical, Signage, Subcontract, Labor, Fire, IT, Stone, General
- Add **Item Type** column (نوع البند): Construction (إنشاءات) / Equipment (معدات) / Operations (تشغيلية)
- Classification rules:
  - **Equipment**: شاشة, كيبل, ليد, جهاز, ماكينة, كمبيوتر, كاميرا — movable assets
  - **Operations**: سفر, تذكرة, فندق, نقل, اكل, قرطاسية, بنك, رسوم, مصروفات — operational expenses
  - **Construction**: everything else — building materials, labor, installation

### Step 3: Group by Category
- Reorganize items grouped by category with subtotals per category
- Keep original item number in a reference column
- Show grand total at bottom

### Step 4: Reallocation Sections
Add two documented sections after the grouped items. **ALWAYS include the full original Arabic description and invoice/document number** when moving items — never use summaries or translations.

**Moved Out (تم تحويله إلى مشاريع أخرى):**
Columns: الرقم الأصلي | البيان (Description) | رقم الفاتورة/المستند | المبلغ | تم التحويل إلى | طريقة التقسيم | المبلغ المتبقي
- Original item number (e.g., #39)
- Full original Arabic description from the accounting statement
- Invoice/document reference number
- Original amount
- Destination project(s) with exact amounts
- Split method (مساحة/تساوي/تحويل كامل)
- Amount retained (if partial transfer, e.g., fire protection kept 82.5%)

**Received From (تم استلامه من مشاريع أخرى):**
Columns: # | البيان | المستند | المبلغ | المصدر | سبب التحويل
- Sequential number in received-from section
- Description of what was received (include location context, e.g., "بند يذكر منطقة جبل النور")
- Source document reference
- Amount
- Source project with code
- Reason: why it belongs to this project (e.g., "البند يخص منطقة جبل النور حيث يقع متجر الوحي")

### Step 5: Reallocation Rules
When one project's line clearly belongs to another:
- **Area-based split**: Compute percentage = store_area / total_area of involved stores
- **Equal split**: Used when item is not area-dependent (e.g., signage lettering, cashier devices)
- **Full transfer**: Item clearly belongs entirely to another project
- **Shared cost**: Split between the projects named in the description
- **Unclear reference**: Stay in original project (don't move)
- If a referenced project can't be found (e.g., Maska), merge its share with nearest project

### Step 6: Factory Cost Section
- Add factory costs:
  2. **Factory Labor**: single merged line (all job types: carpenter, painter, welder, CNC, etc.)
  3. **Factory Raw Materials**: purchase orders + wood/carpentry supplies (single line, details in remarks)
  4. **Factory Others** (أخرى): logistics, outsourcing, equipment rental, consumables — **always include this line, even if zero** — it is part of the standard template factory section.

  ### Shared Accounting Statements
  When ONE accounting statement covers multiple projects (e.g., Qahwatna (03) + Hira (04) share a single Ibrahim statement), split by **area percentage**:
  - Calculate each project's share: `project_area / total_area_of_all_involved_projects`
  - Note the percentage in both the section header and each item's remarks
  - Re-run the target value calculation with the adjusted accounting after split

  ### Target Value / Budget Fitting
  User provides a goal value (budget/target) per project. Distribute factory costs to reach it:
  1. Compute: `factory_needed = (target / 1.1) - accounting_after_reallocation`
  2. Fill gap across the three factory lines (Labor + Materials + Others) logically
  3. Verify: `(accounting + factory) * 1.1 = target` exactly
  4. Adjust the last decimal on `Others` to hit exact target if rounding causes drift

  ## Naming Conventions
- **Dates store = Rateeb Store (متجر رطيب)** — same project, Arabic/English naming difference. Also called Rateeb Store (10).
- **Jabal Al Noor (جبل النور)** ≠ **Jabal Omar (جبل عمر)** — different locations. Al Wahi Gift Shop is at Jabal Al Noor. Project 05 is Jabal Omar VIP Stores.
- **Tzkarat Store (09)** is a dates/souvenirs store.
- **Maska (مسكا)** — unidentified project; when splitting shared costs involving Maska, merge with nearest project (e.g., redistributing Maska's share of gypsum between Rateeb and Hera VC equally).
