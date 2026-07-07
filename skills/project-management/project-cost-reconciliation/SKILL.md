---
name: project-cost-reconciliation
description: "Reconcile costs across related projects (sister companies, multi-store chains). Classify raw accounting lines, identify cross-project misallocations, split shared costs, restructure source files with audit trail."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [costing, reconciliation, reallocation, accounting, cross-project, factory-costing]
    related_skills: [codex, project-costing, construction-cost-estimation]
---

# Project Cost Reconciliation

Reconcile costs across related projects (sister companies, multi-store chains, multiple branches). This handles the full workflow: reading raw accounting files → classifying line items → identifying cross-project misallocations → applying split rules → updating Factory_Cost_Analysis files → adding audit trail → restructuring source files with old→new totals.

## When To Use

You have multiple related projects (e.g. 12+ sister company stores, multi-branch cafes, factory projects) with:
- Accounting invoices that may be recorded under the wrong project
- Shared costs that need splitting (MEP, signage, fire protection, equipment)
- "Custody" entries (عهدة) with unclear project references
- Raw accounting source files (from Ibrahim or similar) that need classification and restructuring
- Factory_Cost_Analysis.xlsx files that need updating with reallocations

## Core Methodology — 5 Reallocation Rules

Apply these rules in order when reconciling costs:

### Rule 1: Cross-Project Mapping
Lines recorded under Project A that describe costs for Project B → **re-map to Project B**. Keywords to look for: other store names, other project codes, specific locations.

### Rule 2: Shared Costs
Items covering multiple stores/projects → split:
- **Area-based split** if the item is area-applicable (MEP, fire protection, flooring, gypsum)
- **Equal split** if not area-dependent (signage lettering, cashier devices, IT equipment)
- Area data comes from the Management Reference sheet or user directly

### Rule 3: Unclear Project References
Lines with no clear project reference → **stay in current project**. Don't move them. "عهدة" (custody) entries with no project name → stay.

### Rule 4: Merge Labor
All individual labor job-type rows (carpenter, painter, welder, etc.) → merge into **one "Factory Labor Cost"** line.

### Supervision
Keep only **Engineering Supervision 10%**. Remove Project Management 5%.

### Capitalization Register Reclassification (IAS 16)
See `references/capitalization-register-reclassification.md` — for when Finance sends a capital asset register (رسملة) and you need to reclassify it into project execution categories (On-Site Work, Off-Site Manufacturing, AV/IT, Furniture, Indirect Costs) and cross-map against BOQ divisions. Produces a 6-sheet Excel output.

## Workflow

### Phase 1: Discover Cross-Project Issues

1. **List all project folders** — each has raw accounting files and a Factory_Cost_Analysis.xlsx
2. **Scan EVERY .xlsx file** in each folder (not starting with `._`)
3. **For each line item**, check if the description mentions:
   - Another store name (e.g. تذكارات, رطيب, هدايا طيبة, مركز الزوار)
   - Shared costs (covering multiple projects)
   - Unclear references (just "عهدة" with no project)
4. **Build a cross-project matrix** — list every item that needs reallocation
5. **Get user confirmation** on split methods for each flagged item
6. **Document areas** — store areas (m²) from Management Reference for area-based splits

### Phase 2: Update Factory_Cost_Analysis.xlsx Files

For each affected project's Factory_Cost_Analysis.xlsx:

1. **Cost_Register sheet**: Remove outgoing items, adjust partial items, add incoming items with clear descriptions referencing source project
2. **Dashboard sheet**: Recalculate totals, merge labor rows, update to 10% Supervision only
3. **Factory_Work sheet**: Update category subtotals
4. **Supervision sheet**: Keep only Engineering Supervision 10%
5. **Reallocation_Log sheet**: Add documenting ALL outgoing and incoming items with:
   - Description, Amount, Source/Target Project, Split Method
   - Both OUTGOING (from this project) and INCOMING (to this project) sections

### Phase 3: Restructure Raw Source Files

For each raw accounting file (especially files from Ibrahim Shaban with "من ايميل ابراهيم" in name):

1. **Add Project Header** at the top with:
   - المشروع: [Project Name (Arabic/English)]
   - الموقع: [Location]
   - المساحة: [Area m²]
   - كود المشروع: [NN]
   - JN: [Job Number]

2. **Add Category column** (التصنيف) — classify each item by Arabic keywords:
   - خشب, نجارة → Wood & Carpentry
   - دهان, بويه → Paint
   - كهرباء, لمبة, كيبل → Electrical
   - حديد, ستيل → Metal Works
   - زجاج, اكريليك → Glass & Acrylic
   - عمال, اجور → Labor
   - نقل, شحن, مواصلات → Transport
   - ميكانيكا, تكييف → MEP/Mechanical
   - If none match → General / Miscellaneous

3. **Add Item Type column** (نوع البند) — classify each item as one of:
   - **Construction** (إنشاءات) — construction/contracting work, materials, installation, labor
   - **Equipment** (معدات) — machinery, devices, electronics, screens, cables, LED lights
   - **Operations** (تشغيلية) — travel, accommodation, meals, stationery, bank fees, rent, utilities, permits
   
   Keywords by type:
   - **Equipment**: شاشة, كيبل, ليد, لمبة, جهاز, ماكينة, كمبيوتر, طابعة, كاميرا, راوتر, بروجكتر, مكيف, ثلاجة, خلاط
   - **Operations**: سفر, تذكرة, فندق, سكن, نقل, شحن, مواصلات, اكل, عشاء, طعام, قرطاسية, طباعة, بنك, تأمين, رسوم, صيانة, ايجار, هاتف, ماء, مصروفات, تراخيص, دعاية, اعلان, دومين

4. **Group items by category** with bold subtitle rows
5. **Add subtotal row** per category using **SUM formulas** (=SUM(range)), never hardcoded numbers
6. **Show OLD total** (SUM of all category subtotals)
7. **Add Reallocation Notes section** documenting:
   - Which items were moved out and where (with amounts and split methods)
   - Which items came in from where
8. **Show NEW total** after reallocation using **cell-reference formulas** (not hardcoded)
9. **Add Factory Cost section**:
   - Raw Materials (POs): [amount]
   - Factory Labor: [amount]
   - Subtotal Factory: =SUM(factory rows)
   - Source values from Factory_Cost_Analysis.xlsx Factory_Work sheet

10. **Add Grand Total Summary** (all using cell-reference formulas):
    - Accounting + Reallocations: =cell_ref_to_new_total
    - Factory Cost: =cell_ref_to_factory_subtotal
    - Subtotal: =SUM(accounting + factory)
    - Supervision (10%): =Subtotal * 0.1 (APPLY ON FULL TOTAL, not just factory)
    - **GRAND TOTAL**: =SUM(subtotal + supervision)

11. **Verify formulas** work by checking that data_only=False shows =SUM(...) and =cell*0.1 patterns, not hardcoded numbers

12. **Backup original** as `- Original.ext` before overwriting

## File Structure Pattern

After reconciliation, each project folder should have:

```
NN_Project_Name/
├── Project_Name_Factory_Cost_Analysis.xlsx   ← Main workbook with 5+ sheets
├── تكاليف المشروع (من ايميل ابراهيم 2026-XX).xlsx  ← Restructured raw source (classified + grouped + old→new total)
├── تكاليف المشروع (من ايميل ابراهيم 2026-XX) - Original.xlsx  ← Backup of unmodified original
└── _Docs/ (optional)
```

The Factory_Cost_Analysis.xlsx always has these sheets:
- `Cost_Register` — all line items with descriptions, categories, amounts
- `Dashboard` — project info, cost summary, merged labor, supervision
- `Factory_Work` — category breakdown with subtotals
- `Supervision` — 10% Engineering Supervision only
- `Reallocation_Log` — full audit trail of all cross-project transfers

## Final Reference File Template

Every project gets ONE master reference file in `_Final/NN_Project_Name.xlsx` with this exact structure:

### Sheet Structure
1. **Main sheet** — 6 sections, compact (no big merged banners), RTL, formula-based
2. **معدات (Equipment)** tab — items classified as equipment, source from Ibrahim's files
3. **تشغيلية (Operations)** tab — items classified as operations, source from Ibrahim's files

### Main Sheet 6-Section Layout (compact — 1 row per header, no scattered columns)

```
Row 1: Project Name (merged A1:G1) | Arabic Name
Row 2: Location, Area, Code, JN, Source Notes (merged A2:G2)
Row 3: SAR/m² header — clean row: [label]=[formula] consecutively, NOT scattered across columns
  C2: محاسبي/m²  C3: =E{acct_row}/area
  C4: مصنع/m²   C5: =D{fc_row}/area  
  C6: النهائي/m² C7: =D{ft_row}/area (bold, large)

Section 1 — Accounting Statement (row ~5)
  Row: "1 — كشف الحساب المحاسبي | المصدر: [source]"
  Row: column headers on ONE row
  Items grouped by category with ▸ headers and SUM subtotals
  Grand total row: "الإجمالي الكلي المحاسبي"

Section 2 — Moved Out
  Row: "2 — بنود محولة إلى مشاريع أخرى"
  Items with: original #, document ref, amount, destination, split method, full Arabic description
  Total: =SUM(D{start}:D{end})

Section 3 — Received From
  Row: "3 — بنود مستلمة من مشاريع أخرى"
  Items with: #, document ref, amount, source, reason, description
  Total: =SUM(D{start}:D{end})

Accounting Total After Reallocation: =E{grand_total} - D{out_total} + D{in_total}
  Navy background, white bold font

Section 4 — Item Type Summary
  SUMIF formulas: إنشاءات, معدات, تشغيلية

Section 5 — Factory Cost
  Row: "5 — تكاليف المصنع"
  Items: 1=عمالة, 2=مواد خام, 3=أخرى (لوجستيك/تعهيد/نقل)
  Total: =SUM(D{start}:D{end})

Section 6 — Final Total
  Row: "6 — الإجمالي النهائي"
  1=Accounting, 2=Factory, 3=Subtotal (bold), 4=Supervision 10%, GT=D{subtotal}+D{supervision}
  Final row: merged navy, white bold
```

### Formula Construction Rules
- ALL values are formulas (=SUM, =E{r}+D{r}, =D{r}*0.1, =SUMIF), NEVER hardcoded
- Subtotal formula: =SUM(E{first_row}:E{last_row}) — computed per category
- Grand total: derived from category subtotal rows =E{r1}+E{r2}+...
- Category subtotals tracked in a list, then joined with "+"
- After row insertions/deletions, ALL formula references must be rechecked

### Cost Calculation Order
The correct sequence for hitting a target:
1. List ALL construction items (no equipment/operations)
2. Apply cross-project transfers (move out, receive in)
3. Calculate net accounting = construction_items + incoming - outgoing
4. Factory_needed = (TARGET / 1.1) - net_accounting
5. Distribute factory: Labor + Materials + Others = factory_needed
6. Equipment/Operations go to SEPARATE tabs (NOT in accounting total)

### Equipment/Operations Rules
- Equipment: machinery, devices, electronics, cables, screens, LED lights
- Operations: travel, accommodation, meals, permits, stationery, bank fees, rent
- These go to separate TABS (sheets), not sections in the main sheet
- NEVER duplicate equipment items across projects (#8,#9 in BOTH = wrong)
- If an equipment item appears in multiple projects, it MUST be at proportional area shares
- Always check source Ibrahim files for equipment data, not derived/restructured files
- Use Arabic terms: "محول من [project]" (transferred from), NOT "مهمل" (neglected)

### Format Rules (Non-Negotiable)
- Section headers: bold text on ONE row, NOT big merged banners. Use Font(bold=True, size=12) on a single cell
- Column headers: ALL columns on ONE row with `ws.cell(row=r, column=ci, value=h)` — the r+=1 goes AFTER the loop, not inside it
- No scattered columns: section column headers must not spread across multiple rows
- RTL: always set `ws.sheet_view.rightToLeft = True`
- SAR/m²: labels and values in consecutive columns, not stepped (B,D,F → B,C,D)
- Compact: minimize blank rows. `r += 1` not `r += 2` between sections. max ~30 rows total
- Arabic labels: use proper business Arabic, not slang. "محول من" not "مهمل". "إجمالي" not "توتال"
- All numbers: #,##0.00 format
- Navy color: 1E293B for headers and totals

### Bug Patterns to Avoid
1. **Column headers splitting across rows**: `for ci, h in enumerate(...): ws.cell(r=r, c=ci, h); r+=1` — the r+=1 is INSIDE the loop, creating one row per column. FIX: remove r+=1 from inside the loop
2. **insert_rows breaks formulas**: inserting rows shifts all references. Avoid insert_rows in files with formula chains. Instead, rebuild from scratch
3. **delete_rows corrupts formulas**: same as above — formulas referencing deleted areas become #REF!. Rebuild instead
4. **MergedCell write error**: unmerge all cells in the target range before writing new data
5. **openpyxl data_only=True shows blanks for formulas**: programmatically-created files have no cached formula values. Verify with data_only=False, read the actual =SUM() strings
6. **Modifying workbook while open**: always `load → modify → save → close`. Never keep a workbook open across multiple operations

## Reference File Template (6-Section Format — absorbed from `sister-companies-costing`, `sister-company-costing`, and `sister-companies-cost-classification`)

Every project gets ONE master reference file in `_Final/NN_Project_Name.xlsx`. These three absorbed skills all converged on this same template. The canonical version is below, consolidating all their rules.

### Sheet Structure

1. **Main sheet** — 6 sections, compact (no big merged banners), RTL, formula-based
2. **معدات (Equipment)** tab — items classified as equipment
3. **تشغيلية (Operations)** tab — items classified as operations

### Main Sheet 6-Section Layout

```
Row 1: Project Name (merged A1:G1) | Arabic Name
Row 2: Location, Area, Code, JN, Source Notes (merged A2:G2)
Row 3: SAR/m² header — clean row: [label]=[formula] consecutively
  C2: محاسبي/m²  C3: =E{acct_row}/area
  C4: مصنع/m²   C5: =D{fc_row}/area  
  C6: النهائي/m² C7: =D{ft_row}/area (bold, large)

Section 1 — Accounting Statement (row ~5)
  "1 — كشف الحساب المحاسبي | المصدر: [source]"
  Items grouped by category with ▸ headers and SUM subtotals

Section 2 — Moved Out: "2 — بنود محولة إلى مشاريع أخرى"
Section 3 — Received From: "3 — بنود مستلمة من مشاريع أخرى"
Section 4 — Item Type Summary (SUMIF: Construction/Equipment/Operations)
Section 5 — Factory Cost (Labor + Materials + Others)
Section 6 — Final Total (Accounting → Factory → Subtotal → Supervision 10% → Grand Total)
```

**Formula construction rules (mandatory):**
- ALL values are formulas (=SUM, =cell*0.1, =SUMIF), NEVER hardcoded
- Category subtotals: `=SUM(E{first_row}:E{last_row})`
- Grand total: derived from category subtotal rows
- Supervision: `=Subtotal * 0.1` (on FULL total, not just factory)
- SAR/m²: `=Total/Area`
- NEVER use `insert_rows()` or `delete_rows()` after formulas are set

**Python build helper — `hdr()` function:**
```python
def hdr(ws, r, cols):
    for ci, h in enumerate(cols, 1):
        c = ws.cell(row=r, column=ci, value=h)
        c.font = wf; c.fill = n; c.alignment = Alignment(horizontal="center", wrap_text=True)
# Call: hdr(ws, r, ["col1","col2",...]); r += 1  ← r+=1 OUTSIDE
```

**CRITICAL**: `r += 1` goes AFTER the `hdr()` call, NEVER inside the for-loop. This was the #1 user frustration in production builds.

### Cost Calculation Order
The correct sequence for hitting a target:
1. List ALL construction items (no equipment/operations)
2. Apply cross-project transfers (move out, receive in)
3. Calculate net accounting = construction_items + incoming - outgoing
4. Factory_needed = (TARGET / 1.1) - net_accounting
5. Distribute factory: Labor + Materials + Others = factory_needed
6. Equipment/Operations go to SEPARATE tabs (NOT in accounting total)

### Project Registry (Consolidated from `sister-companies-cost-classification`)

| Code | Project | Arabic | Area m² |
|:----:|:--------|:-------|:-------:|
| 01 | Al Wahi Gift Shop | متجر الوحي للهدايا | 240 |
| 02 | Holy Quran Gift Shop | متجر القرآن الكريم | 194 |
| 03 | Qahwatna Cafe | مقهى قهوتنا | 77.5 |
| 04 | Hira Cafe | مقهى حراء | 398 |
| 05 | Jabal Omar VIP Stores | متاجر جبل عمر | 67 |
| 06 | As Safiyyah Giftshop | متجر الصفية للهدايا | 445 |
| 08 | Qahwatna Al-Safiya Cafe | مقهى قهوتنا الصافية | 26 |
| 09 | Tzkarat Store | متجر تذكارات | 51 |
| 10 | Rateeb Store | متجر رطيب (التمور) | 42 |
| 11 | Najdi Coffee | مقهى القهوة السعودية | 173 |
| 12 | Ice Coffee Shop | متجر الآيس كوفي | — |
| 13 | Hera Visitor Center | مركز الزوار | — |

### Terminology Mapping (Arabic ↔ English)

| Arabic | English | Notes |
|--------|---------|-------|
| متجر رطيب | Rateeb Store | Also "Dates Store" (متجر التمور) |
| متجر تذكارات | Tzkarat Store | — |
| متجر الوحي | Al Wahi Gift Shop | — |
| مركز الزوار | Visitor Center | Jabal Alnour / Hera |
| كبار الزوار | Jabal Omar VIP Store (05) | NOT the Visitor Center |
| مسكا | Maska | New project, not in ref |
| قهوتنا | Qahwatna brand | Multiple branches (03, 08) |

### Area-Based Split Formula
```
per_project_share = shared_amount × (project_area / sum_of_all_involved_areas)
```

### Factory Cost Analysis Workbook Structure
Each project's `Factory_Cost_Analysis.xlsx` has these sheets:
- `Cost_Register` — all line items with descriptions, categories, amounts
- `Dashboard` — project info, cost summary, merged labor, supervision
- `Factory_Work` — category breakdown with subtotals
- `Supervision` — 10% Engineering Supervision only
- `Reallocation_Log` — full audit trail of all cross-project transfers

### Complete Scan Workflow (for reallocation across ALL projects)
1. List all folders under `Sister_Companies/` — look for `NN_Name_XX` pattern
2. For each folder, read ALL .xlsx and .xls files
3. For each accounting statement, extract every line item and check for:
   - Mentions of other stores by name (Arabic or English)
   - Mentions of multiple stores/locations
   - Vague descriptions (عهدة entries)
   - Shared cost indicators (e.g., "للمحلات" = for shops, plural)
4. Cross-reference against the Management Reference for areas, budgets, status
5. Build a consolidated reallocation table
6. Present to the user for confirmation before executing
7. Update all affected Factory_Cost_Analysis.xlsx files

## Common Pitfalls

### Arabic Keyword Classification
When classifying Arabic descriptions, use broad keyword matching. A single item might match multiple categories — pick the best fit. Common categories: Transport, Wood/Carpentry, Electrical, Paint, Metal Works, Glass/Acrylic, Labor, Materials, Equipment, MEP, Signage, Fire Protection, IT.

### Area Data Location
Store areas (m²) live in the Management Reference file:
`_Management/Sister_Companies_Management_Reference.xlsx` → `Project_Summary` sheet

### Zero-Template Projects
Some projects have `Factory_Cost_Analysis.xlsx` with headers but no data (empty template). For these, the reallocation work happens in the raw source files only — the FCA remains empty until data is entered.

### .xls vs .xlsx
Raw files in `.xls` format (old Excel) are typically bank account statements (كشف حساب), not costing sheets. They can be read with `xlrd` but restructuring them the same way as costing sheets may not be appropriate. Skip these unless the user specifically asks.

### Reallocation_Log: Both Sides
Every transfer MUST be documented in BOTH the source project's AND the target project's Reallocation_Log sheet. This creates a complete audit trail. The FCA files track what left (source) and what arrived (target).

### Total Verification
After all updates, verify totals by reading the Cost_Register raw values (not formula results, which may be empty in data_only mode for programmatically-created files). Manually sum column D amounts and compare against the declared total.

### Small-Task Preference
When the scope is large (10+ files, 800+ items), the user prefers **small sequential tasks** rather than large batch delegations. Present the work as a checklist of discrete steps and execute one at a time, getting user confirmation between each. Batch delegation of 3+ parallel subagents is acceptable for independent file operations, but stop and report between batches.
