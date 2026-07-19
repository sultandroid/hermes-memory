---
name: sister-companies-costing
title: Sister Companies — Costing Reports & SysLeaders Data
description: Build and maintain costing reports for Samaya's sister company projects (12 retail stores/cafes). Pull PO and labor data from SysLeaders, build Factory Work reports, manage the _Final folder structure, and handle cross-project cost reallocation.
triggers:
  - User mentions "Sister Companies" costing or reports
  - User asks to pull data from sysleaders.com/samaya
  - User asks to build Factory Work reports for a project (01-13)
  - User references the `_Final` folder or `Reports/Sister_Companies/`
  - User asks about cross-project cost reallocation between stores
---

# Sister Companies — Costing Reports

## Overview
13 retail projects (stores, cafes, gift shops) under 5 client companies. Each project has accounting costs (Ibrahim Shaban invoices), factory costs (POs + labor + fleet), and 10% engineering supervision. Cross-project reallocation moves costs between projects based on actual beneficiary.

## Project Map

| Code | Project | Client (Final Folder) | Organized Company Folder | JN | Area (m²) | Location |
|------|---------|-----------------------|--------------------------|-----|-----------|----------|
| 01 | Al Wahi Gift Shop | Tiba Gift comp_ | Tiba_Gift_Company | 367+255 | 240 | Jabal Alnour, Makkah |
| 02 | Holy Quran Gift Shop | Tiba Gift comp_ | Tiba_Gift_Company | 367 | 194 | Jabal Alnour, Makkah |
| 03 | Qahwatna Cafe | **Tiba Gift comp_** | **Tiba_Gift_Company** | 262 | 77.5 | Makkah |
| 04 | Hira Cafe | Qahwitna comp_ | Qahwatna_Company | 262 | 398 | Makkah |
| 05 | Jabal Omar VIP Stores | _Final (root) | (standalone) | -- | TBD | Makkah |
| 06 | As Safiyyah Giftshop | Tiba Gift comp_ | Tiba_Gift_Company | 329 | 445 | Madinah |
| 07 | Khair Al-Khalq Store | Tiba Gift comp_ | Tiba_Gift_Company | 403 | 173 | Madinah |
| 08 | Qahwatna Al-Safiya Cafe | Qahwitna comp_ | Qahwatna_Company | 359 | 26 | Madinah |
| 09 | Tzkarat Store | Tezkarat Trading Com_ | Tezkarat_Trading_Company | 279 | 51 | Makkah |
| 10 | Rateeb Store | Rateeb Trading Com_ | Rateeb_Trading_Company | 282 | 42 | Makkah |
| 11 | Najdi Coffee | Qahwitna comp_ | Qahwatna_Company | 345 | 173 | Makkah |
| 12 | Ice Coffee Shop | Qahwitna comp_ | Qahwatna_Company | 312 | TBD | Makkah |
| 13 | Hera Visitor Center | _Final (root) | (standalone) | 81 | TBD | Makkah - Jabal Alnour |

## Paths
```
Base: ~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Reports/Sister_Companies/
_Final: .../Sister_Companies/_Final/ (per-client folders)
Projects: .../Sister_Companies/{NN}_{Project_Name}/
Dashboard: .../Sister_Companies/_Management/Stores_Coffee_Shops_Dashboard.xlsx
```

## Cost Components Per Project
1. **Accounting Statement** — Ibrahim Shaban invoices, classified by category (construction/equipment/operations)
2. **Reallocation** — costs moved out to other projects + costs received from other projects
3. **Factory Cost** — POs (SysLeaders) + Labor + Fleet/Transport
4. **Supervision** — 10% of (Accounting + Factory) total
5. **Grand Total** — Accounting (net) + Factory + Supervision

## _Final Folder Structure (company folders preserved, subfolders per project)
```
_Final/
├── Tiba Gift comp_/                    ← DO NOT DELETE OR RENAME (company folder)
│   ├── 01_Al_Wahi_Gift_Shop/
│   │   ├── 01_Al_Wahi_Gift_Shop.xlsx              (accounting)
│   │   └── 01_Al_Wahi_Gift_Shop_Factory_Cost_Details.xlsx (factory detail)
│   ├── 02_Holy_Quran_Gift_Shop/
│   │   ├── 02_Holy_Quran_Gift_Shop.xlsx
│   │   └── 02_Holy_Quran_Gift_Shop_Factory_Cost_Details.xlsx
│   ├── 03_Qahwatna_Cafe/                           ← Project 03 is under Tiba Gift, NOT Qahwitna
│   │   ├── 03_Qahwatna_Cafe.xlsx
│   │   └── 03_Qahwatna_Cafe_Factory_Cost_Details.xlsx
│   ├── 06_As_Safiyyah_Giftshop/
│   │   ├── 06_As_Safiyyah_Giftshop.xlsx
│   │   └── 06_As_Safiyyah_Giftshop_Factory_Cost_Details.xlsx
│   └── 07_Khair_Al_Khalq_Store/
│       ├── 07_Khair_Al_Khalq_Store.xlsx
│       └── 07_Khair_Al_Khalq_Store_Section5_Detail.xlsx
├── Qahwitna comp_/                     ← DO NOT DELETE OR RENAME
│   ├── 04_Hira_Cafe/
│   ├── 08_Al_Safiya_Cafe/
│   ├── 11_Najdi_Coffee/
│   └── 12_Ice_Coffee_Shop/
├── Tezkarat Trading Com_/              ← DO NOT DELETE OR RENAME
│   └── 09_Tzkarat_Store/
├── Rateeb Trading Com_/                ← DO NOT DELETE OR RENAME
│   └── 10_Rateeb_Store/
├── 05_Jabal_Omar_VIP_Stores/           (standalone — no company folder)
└── 13_Hera_Visitor_Center/             (standalone — no company folder)
```
**CRITICAL:** Company folders (Tiba Gift comp_, Qahwitna comp_, Rateeb Trading Com_, Tezkarat Trading Com_) are the original structure created by the company. **NEVER delete, rename, or flatten them.** Inside each company folder, create per-project subfolders containing the accounting file + Section5_Detail file. Standalone projects (05, 13) stay at root level in their own folders.

**Cleanup rule:** After building detail files, remove all old `*Factory_Labor_POs_Expenses.xlsx` files and `*_backup_*.xlsx` files. Each project subfolder should have only: original accounting Excel + Section5_Detail file.

## Source Folder Mapping (FCA Files)
Source folders follow `{NN}_{Project_Name_XX}` but FCA files within them omit the leading `NN_`. **Use glob to find them** — `glob.glob(os.path.join(folder, "*Factory_Cost_Analysis*.xlsx"))` and filter out `backup` files. Never construct the path from the folder name. See `references/source-folder-mapping.md` for the full table.

## Independent Machine / Equipment Reconciliation
When tracing equipment or machinery from final cafe/store workbooks back to costing and archive evidence, follow `references/machine-equipment-trace-protocol.md`. For the cafe-wide formula, evidence, and transfer audit sequence, also use `references/cafe-equipment-cost-audit.md`. For row-level transfer controls, unresolved shared balances, allocation pitfalls, and raw-XLSX formula verification, use `references/equipment-allocation-reconciliation.md`.

Core rule: `Original shared amount = sum(confirmed two-sided destination allocations) + unallocated balance`. Never convert an unexplained remainder into a generic equipment line or infer ownership solely from an area percentage.

### Portfolio audit canonicalization
For portfolio-wide raw-versus-final equipment totals, define and disclose the counting basis before doing arithmetic:
- Select one canonical raw transaction set per project. Prefer the current/restructured workbook's dedicated Equipment sheet when it has row references and amounts; otherwise use the earliest original or `_Archive/Project_Extras` row-level source.
- Count main-sheet rows and an extracted Equipment sheet only once when references, descriptions, and amounts are identical. Archive, backup, email-extract, and management copies are corroboration, not additional transactions.
- Select only the main final workbook as the canonical final; never substitute `Section5_Detail.xlsx`. Record a missing main final workbook as a completeness gap rather than assuming a confirmed zero.
- Use explicitly classified `معدات` / `Equipment` / `تجهيزات (Equipment)` rows for the primary control total. Trace equipment-like rows classified as Construction, MEP, tools, materials, or miscellaneous separately as reclassifications/transfers.
- Calculate raw, final, and `final - raw` per project, then sum those canonical project totals for the portfolio. Never total every exact-amount match across all copies.
- A transfer requires source reference + description + amount + outgoing and receiving evidence. A split is confirmed only when destination components sum to the source. Quantify unsupported residuals when only one side exists.
- A generic destination lump sum without item references, invoices, or vouchers remains an unresolved bridge even if project totals are close.
- Save broad exact-amount scans to JSON/CSV before summarizing because terminal output may truncate large match sets.

Key requirements:
- Inventory final main workbooks first; do not mistake a `Section5_Detail.xlsx` file for the main costing workbook.
- Trace in both directions: final → source and source equipment → final, so omissions and reclassifications are found.
- Cite exact relative path, sheet, and cell for every confirmed statement.
- Search all final sheets before calling a source item missing; equipment may be reclassified under tools, plumbing, materials, or miscellaneous.
- Use exact-amount scans across all projects to detect transfers and duplicates, but treat backup/archive/email-extract copies as provenance copies rather than separate transactions.
- Verify disputed formulas with both `openpyxl(..., data_only=False)` and raw XLSX worksheet XML. Cached or document-extraction views can expose only values and cause formula cells to be misreported as hardcoded.
- A correct `SUM` formula validates arithmetic only. Every hardcoded component still needs a source reference, matching description/amount, voucher or invoice, and exact source cell.
- Check both sides of inter-project reallocations. An outgoing transfer without the corresponding destination receipt is incomplete.
- A common reduction ratio is not an explained allocation unless a workbook contains the percentage, formula, transfer note, or another documentary bridge.
- Distinguish actual machines from kiosks, used containers, temporary facilities, tools, and consumables; flag classification rather than silently grouping them as equipment.
- Separate confirmed evidence from gaps, and avoid recommendations unless requested.

## SysLeaders Data Extraction
See `references/sysleaders-access.md` for login, navigation, PO extraction, and project filtering patterns.

### Database Backup Folder (local reference)
Full API dump saved at `/Volumes/MIcro/Work/Sysleaders/Database backup_claude/`:
- `sysleaders_full_backup_20260716_081602.json` — 5.9MB, 211 projects, 870 POs, 4422 cost records
- `projects_20260716_081602.json` — 211 projects with full details
- `purchasing_orders_20260716_081602.json` — 870 POs
- `rateeb_live_data.json` — Rateeb project live browser data (workers, BOQ, POs, feeding, fleet)
- `schema_reference.json` — DB structure + field mappings
- `sister_companies_projects.json` — 13 Sister Companies list with Section 5 totals
- `README.json` — Full index + data map

### Backup File Verification (CRITICAL)
ALL SQL backup files examined are **structure-only** (CREATE TABLE, no data in entity tables):
- `sysleaders_samaya.sql` — no entity data
- `sysleaders_samaya2.sql` — no entity data
- `backup-7.15.2026_23-42-47_sysleaders.tar.gz` — same structure-only SQL files
- `sysleaders_samaya2 (1).sql` — has entity_28 data but from **2020-2021** (old factory records, not current Rateeb/Sister Companies data)

**The live data is ONLY on the server.** A proper backup of `sysleaders_samaya` (the one with actual records) is needed. Do not waste time re-analyzing these backup files — they will always be empty.

## Source Folders & FCA Files
See `references/source-folder-mapping.md` for the complete source-folder-to-FCA-file mapping, glob patterns, and labor data availability per project.
See `references/qahwatna-cafe-factory-cost-data.md` for the verified Qahwatna Cafe (Project 03) factory cost breakdown (279,610 SAR total), including the corrected client mapping (Tiba Gift, not Qahwitna).

## Factory Work Report Template
See `references/factory-work-report-template.md` for the 3-sheet Excel structure.

## Factory_Labor_POs_Expenses Report (4-sheet XLSX)
Template: `10_Rateeb_Store_07/Rateeb_Factory_Labor_POs_Expenses.xlsx`

Each project report gets 4 sheets:
1. **Factory_Labor** — job types with records/hours/cost/rate + "% of Total" column. Subtotals with average rate.
2. **PO_Costs** — purchase orders from SysLeaders (PO#, date, status, cost, items column).
3. **Expenses** — other expenses (external labor, fleet/transport, direct materials, subcontractor) with category breakdown at bottom.
4. **Summary** — full breakdown: Factory Labor → External Labor → Raw Materials (POs) → Direct Expenses → GRAND TOTAL, plus REALLOCATION NOTES section.

### Data Sources to Populate
- **Labor data**: From FCA's Dashboard sheet → "JOB CLASSIFICATION (Labor by Type)" table. For projects without per-trade breakdown (01, 03, 05, 11, 13), show the FCA aggregate with a "pending detailed breakdown" note.
- **PO data**: From FCA's Factory_Work or Cost_Register sheets → "PO - Category" lines with amounts and PO# references.
- **Expense data**: From the project's `Costing.xlsx` (construction items only — equipment and operations go in separate sheets on the Costing file, not this report). Also from `_Final/{client}/{NN}_Project.xlsx` accounting statement.
- **Reallocation**: From FCA's Reallocation_Log sheet and from Costing reallocation sections.

### Styling (matching Rateeb template)
- Navy headers (#1E293B), white Calibri 11pt bold
- Gray subtotals (#F1F5F9), thin borders (#CBD5E1)
- Right-to-left sheet view (Arabic compatible)
- Number format `#,##0.00` for all amounts
- Bilingual labels (English + Arabic)

### Technique: Embed pre-extracted data rather than parsing FCA files on the fly
The FCA files have varied, inconsistent formats (Arabic/English mixed headers, merged cells, different column orders across projects). **Reading them once via `read_file` (auto-extracts XLSX as text) and embedding the data in the generator script is far more reliable** than trying to parse them programmatically with openpyxl. The data doesn't change between extraction and report generation, so embedding is safe. Build the script with a `FCA_DATA` dictionary keyed by project ID containing pre-extracted `labor`, `pos`, and `realloc` lists.

### Batch report generation pattern
When building reports for all 13 projects at once:
1. Read all FCA files via `read_file` to extract labor/PO/reallocation data
2. Read all Costing files + `_Final` project files to extract expense data and metadata
3. Build a single Python script with embedded data dictionaries (`FCA_DATA`, `EXPENSE_DATA`, `PROJECTS`)
4. Use shared `build_report(proj)` function that reads from the embedded dicts
5. Always backup existing `_Final` files before overwriting: `shutil.copy2(final_path, final_path.replace('.xlsx', f'_backup_{timestamp}.xlsx'))`

## Primary Working Directory
The user now works in `00_Organized_13_Project_Factory_Reconciliation/` (not `_Final/`). This is the **active workspace** — all new work, fixes, and clean copies go here. This folder has:
- Per-company subfolders (Tiba_Gift_Company/, Qahwatna_Company/, Rateeb_Trading_Company/, Tezkarat_Trading_Company/, Unassigned_Company/)
- Per-project subfolders inside each company folder
- Each project has: `{Project}_Factory_Cost_Details.xlsx` + `Main_Accounting_Sheet.xlsx`
- `_Control/` folder with: Project_JN_Mapping.xlsx, Master_Workers_Reference.xlsx, Validation_Log.xlsx, Source_Manifest.xlsx

**CRITICAL:** The `Main_Accounting_Sheet.xlsx` files may contain **wrong project data** — always verify the Summary sheet's project name and totals match the expected project before using as reference. Some files were copied from other projects (e.g. Al Wahi's Main_Accounting_Sheet showed Holy Quran data).

## Workflow: Sequential Processing (one project at a time)
- Process projects **one by one**, not all at once. User explicitly prefers this.
- Start with project 01 and proceed in order (01 → 02 → 03 → ... → 13).
- For each project: verify data → build/rebuild → present for confirmation → move to next.
- Do NOT batch-generate reports for all 13 projects in a single script run.
- When user says "fix this gap", adjust the forecast line to match the target exactly. Update all 3 sheets (Materials & POs, Summary, Gap_Analysis) to reflect the change.

## User Communication Preferences
- **English only** — never present data in Arabic. The user cannot read Arabic. Translate all category names, descriptions, and notes to English before showing in tables or file content.
- **"fix" = proceed with default/verified-only approach** — when the user says "fix" as a single-word command after seeing flagged items, it means: exclude all "Needs Review" and "Not Related" items, use only verified items, and build the files immediately. Do not ask for confirmation on each flagged item.
- **"next" = move to next project** — after confirming a project is done, "next" means proceed to the next project in sequence (01→02→03→...→13).

## Handling Audit-Flagged Items (Projects with verification flags)
Some projects (like Qahwatna Cafe) have items flagged as "Needs Review" or "Not Related" in the accounting file. When building factory cost details:

1. **Present the full picture first** — show all items grouped by category with totals, then list only the flagged items with their amounts and flags
2. **Let the user decide** — ask specifically which flagged items to include/exclude. Present as concise numbered questions, not a wall of text
3. **"fix" = exclude all flagged** — when user says "fix", exclude everything flagged as "Needs Review" or "Not Related". Build files with only verified items.
4. **Document the exclusion** — in the Gap_Analysis sheet, note the excluded items and their total amount so the gap is explainable

## Gap Closure Order: Dates FIRST, Then Gaps
**CRITICAL ORDER — failure to follow this will lose work:**
1. Fix dates first (redistribute forecast dates across project range)
2. Then fix gaps (adjust forecast amounts to match targets)
3. Then generate clean copy (if requested)

Date redistribution re-saves the file and **overwrites any gap fixes** applied earlier. Always do dates → gaps → clean copy in sequence.

## Two-File Output Pattern (per project)

Each project gets **two** factory cost detail files:

1. **`{Project}_Factory_Cost_Details.xlsx`** (full version)
   - 3 data sheets: Labour Timesheet, Materials & POs, Other Expenses
   - 2 summary sheets: Summary (3-line table), Gap_Analysis (target vs actual)
   - Navy #1F3864 headers, yellow #FFD700 total rows, #,##0.00 number format

2. **`{Project}_Factory_Cost_Details_Clean.xlsx`** (clean version)
   - Same 3 data sheets: Labour Timesheet, Materials & POs, Other Expenses
   - NO Summary or Gap_Analysis sheets — clean data only
   - Same styling as full version

### Generator Script Pattern

Save reusable generator scripts to `Scripts/generate_{project}_factory_cost.py`. The script should:

1. **Embed data directly** — read FCA files once via `read_file`, extract labour/PO/reallocation data, and hardcode it as Python lists in the script. Do NOT parse FCA XLSX programmatically — formats vary per project.
2. **Define data as tuples** — use `(trade, records, hours, cost)` for labour, `(po_ref, description, amount)` for materials, `(description, amount)` for other expenses.
3. **Use consistent tuple indexing** — labour tuples have 4 elements (index 3 = cost), materials have 3 elements (index 2 = amount), other have 2 elements (index 1 = amount). **Pitfall:** mixing up tuple indices causes `IndexError` at runtime.
4. **Build both files** — full version (5 sheets) and clean version (3 sheets, no Summary/Gap_Analysis).
5. **Copy to both directories** — Organized (`00_Organized_13_Project_Factory_Reconciliation/{Company}/{Project}/`) and _Final (`_Final/{Client_Folder}/{Project}/`).
6. **Verify company mapping** — check the project map in this skill before hardcoding paths. The project map is authoritative; do not guess the company folder from the project name alone.

See `scripts/generate-hira-cafe-factory-cost.py` for a working example.

### 3-Row Factory Cost Schema
The standard factory cost structure has exactly 3 components:

| Component | Sheet | Content |
|-----------|-------|---------|
| Factory Labour | Labour Timesheet | Worker-level records: #, Date, Worker Name, Trade, Hours, Rate/hr, Cost (SAR), Description |
| Raw Materials | Materials & POs | PO-level records: PO#, Date, Description, Qty, Unit Cost, Line Total |
| Other / Logistics | Other Expenses | Expense records: #, Date, Category, Amount (SAR), Details, Ref |

### Data Sources for Each Component
- **Labour**: From FCA Dashboard "JOB CLASSIFICATION (Labor by Type)" table. When only trade-level summaries exist (not individual worker entries), show breakdown by trade rather than individual timesheet rows.
- **Materials**: From FCA Cost_Register or Factory_Work sheets — PO# references with amounts.
- **Other**: Fleet/Transport + Reallocated costs from FCA sheets.

### Target Directories
Both files go in two locations:
1. `00_Organized_13_Project_Factory_Reconciliation/{Company}/{Project}/` (active workspace)
2. `_Final/{Client_Folder}/{Project}/` (delivery copy)

### Accounting File Factory Cost Section
The main accounting file (`تكاليف المشروع.xlsx`) may have a "تكاليف المصنع (FACTORY COST)" section with formulas that reference specific cells. These formulas are often:
- Raw Materials = SUM of one category only (not all materials)
- Factory Labor = one external labor line (not the full timesheet)
- No Other Expenses row

**The clean detail file is the comprehensive version.** The accounting file's factory cost section is often a placeholder — do not expect it to match the detail file's totals.

## Key Rules
- **Supervision = 10% of (Accounting + Factory)** — apply to the sum, not just factory cost
- **All totals formula-based** — no hardcoded numbers in _Final files
- **Equipment and Operations** items go in separate sheets (not mixed with construction)
- **Shared items** split by area percentage; equal split when area unknown
- **Factory labor** from FCA analysis aggregated as one "Factory Labor Cost" line
- **Header** on every file: project name, location, area, JN, code

## File Naming Convention
- Detail files: `{Project}_Factory_Cost_Details.xlsx` (NOT `Section5_Detail` or `Factory_Details`)
- Main accounting: `{Project}.xlsx`
- Organized reconciliation folder: `00_Organized_13_Project_Factory_Reconciliation/{Company}/{Project}/{Project}_Factory_Cost_Details.xlsx` and `Main_Accounting_Sheet.xlsx`
- When renaming: rename ALL copies across both `Section5_Factory_Details/` and `_Final/` and `00_Organized_13_Project_Factory_Reconciliation/` folders

## Gap Analysis Between Accounting & Factory Costs
When user asks about gaps, produce a table comparing:
1. **Accounting sheet** (FCA Cost_Register) — what was paid/invoiced
2. **SysLeaders actual attendance** (Section5_Detail / Factory_Cost_Details) — real worker records
3. **FCA Dashboard** (SysLeaders summary) — total in system
4. **Current Factory_Cost_Details** — what the file currently shows

Explain WHY each gap exists (e.g. internal factory wages not in accounting, records beyond API extract limit). Never fabricate numbers to fill gaps — present the real data and let the user decide how to handle it.

### Date Range Alignment Across All Sheets
When user says "fix the dates for all sheets should be the same project range":

1. **Determine the project date range** from real data (SysLeaders attendance records). Use the min/max dates from Labour Timesheet real rows.
2. **Redistribute forecast dates** evenly across the project range:
   - Count forecast rows in Labour Timesheet and Other Expenses
   - For each forecast row, calculate: `offset = total_days * i / (count - 1)`
   - Set date = `start + timedelta(days=offset)`
   - Format as `dd/mm/YYYY`
3. **CRITICAL: Do this BEFORE fixing gaps.** Date redistribution re-saves the file and will overwrite any gap fixes you applied earlier.
4. **Verify** — re-read all sheets and confirm dates span the project range

## Gap Closure (when user says "fix this gap")
When user explicitly says "fix this gap" or "close this gap":

**CRITICAL ORDER: Fix dates FIRST, then fix gaps.** Date redistribution overwrites gap fixes because it re-saves the file. Always do dates → gaps in sequence.

### Step-by-step gap closure:
1. **Identify the gap** — compare Real + Forecast vs Target. The gap = Target - (Real + Forecast)
2. **Adjust the forecast line** — find the forecast row (e.g. FCST-001 in Materials & POs) and increase its amount by the gap value
3. **Update all summary rows in the same sheet:**
   - Forecast Total = old forecast + gap
   - GRAND TOTAL = Real + new Forecast (= Target)
   - Remaining Gap = 0
4. **Update Summary sheet** — same component row: Forecast, Total, Target, Gap=0, Status="Closed"
5. **Update Gap_Analysis sheet** — same component row: Forecast, Total, Gap=0
6. **Update TOTAL row** in both Summary and Gap_Analysis:
   - Forecast = sum of all component forecasts
   - Total = sum of all component totals
   - Gap = 0, Status = "Closed"
7. **CRITICAL: Use explicit row index for Summary TOTAL row** — openpyxl's `data_only=True` vs `data_only=False` can cause row matching by column value to fail silently. After matching by content, also verify by row index (row 7 in Summary, row 6 in Gap_Analysis for Al Wahi). Assign cells by index: `row[3].value = new_forecast`, `row[4].value = new_total`, `row[6].value = 0`, `row[7].value = 'Closed'`.
8. **Verify** — re-read with data_only=True, confirm every sheet's totals match

### Common gap values (Al Wahi example):
- Materials gap: 985.59 → adjust FCST-001 from 34,521.75 to 35,507.34
- Labor gap: -1.80 (rounding, essentially closed)
- Other: usually 0 if all forecast

## Section 5 Detail Files (CRITICAL — user is explicit about this)

For evidence-based construction of real timesheets, PO material lines, logistics/expenses, and transparent residuals, follow `references/source-backed-section5-reconciliation.md`.

**Evidence rule:** Exact arithmetic fit is not reconciliation. Keep source-backed records, approved allocations, and unsupported bridges separate. Never rename a residual as BOQ labor, overhead, materials, logistics, or another real category merely to force a zero variance. A zero-variance line with an unsupported bridge remains `Pending`.

The main `_Final/{Project}.xlsx` has Section 5 (تكاليف المصنع) with 3 lines: Labor, Raw Materials, Other. Detail files (`{Project}_Section5_Detail.xlsx`) MUST:
- **Only break down Section 5** — never include Section 1 (Accounting) items
- **Match Section 5 totals exactly** — each sheet total = corresponding Section 5 line
- **5-sheet structure:** 1_Factory_Labor, 1b_Labor_Timesheet, 2_Raw_Materials, 3_Other_Costs, 4_Section5_Summary
- **Never duplicate:** external labor, AC units, cashier devices, air curtains, gypsum, transport — these are Section 1 items
- **Verify against main file before delivery** — compare each sheet total against the corresponding Section 5 line
- **Read the main _Final file's Section 5 values FIRST** before building the detail report. Parse the 3 lines (Labor, Materials, Other) and their totals. Each detail sheet must equal its corresponding line exactly.
- File naming convention: `{Project}_Factory_Cost_Details.xlsx` (not `Section5_Detail` or `Factory_Labor_POs_Expenses.xlsx`)
- **Cleanup rule:** After building detail files, remove all old `*Factory_Labor_POs_Expenses.xlsx` files and `*_backup_*.xlsx` files. Each client folder should have only: original Excel + Section5_Detail file.
- See `references/factory-work-report-template.md` for full template

### 1b_Labor_Timesheet Sheet
Inserted between 1_Factory_Labor and 2_Raw_Materials. Columns:
- Date | Worker Name | Trade | Hours | Rate/hr | Cost (SAR) | Task/BOQ | Status
- Trade-level summary rows with record counts
- SysLeaders extraction plan documented at bottom
- Data source: `app_entity_28` in `sysleaders_samaya` database (tasks table with worker names, dates, hours)
- Labor cost = rate × hours (calculated on-the-fly in SysLeaders, not stored in DB)
- **When data is unavailable**, show trade-level summaries from FCA with record counts and mark individual rows as "TBD — need verified worker-level extraction".
- **Worker-level source priority:** first inspect `Sysleaders Backup/Project_Exports_v2/`, project-specific exports, and local JSON captures. These may contain real worker/date/hour/rate rows even when direct database access is unavailable.
- If project exports are absent or incomplete, use the live SysLeaders browser extraction. Database/phpMyAdmin access is only one route and must not be treated as the sole source.
- Reject generated-looking expanded registers when they conflict with a smaller authoritative project export; repeated generic shifts are not evidence merely because they sum to the Section 5 target.

### Verification Protocol (MANDATORY before delivery)
1. Read the main `_Final/{Project}.xlsx` file's Section 5 values (lines 1-3 + total)
2. Read the detail file's 4_Section5_Summary sheet totals
3. Confirm each line matches exactly
4. Confirm NO Section 1 items appear in the detail file (check Expenses sheet against main file's accounting section)
5. If mismatches found, fix the detail file — do not deliver with wrong totals
6. Create backup of main file before any modification: `cp main.xlsx /Volumes/MIcro/Work/Sysleaders/backups/{Project}_ORIGINAL.xlsx`

### Common Duplication Pitfalls (check these specifically)
| Item | Belongs in | Often wrongly placed in |
|------|-----------|------------------------|
| External labor (site workers) | Section 1 — Accounting | Section 5 — Factory Labor |
| AC units, air curtains | Section 1 — Accounting | Section 5 — Other |
| Cashier devices, POS equipment | Section 1 — Accounting | Section 5 — Materials |
| Gypsum works subcontract | Section 1 — Accounting | Section 5 — Other |
| Transport/fleet (site) | Section 1 — Accounting | Section 5 — Other |
| Factory POs (Corian, wood, paint, glass) | Section 5 — Materials | Section 1 — Accounting (correct) |

### Client-Ready Format
Maintain two distinct outputs when evidence is incomplete:
1. **Internal evidence workbook** — exact source paths/cells, unsupported bridges, allocation status, and reconciliation controls.
2. **Client export** — clean presentation with source references reduced to document/PO/reference identifiers.

Do not create or label a client-ready export while a material unsupported bridge remains. Clean presentation must never conceal an evidence gap or turn a `Pending` line into `Complete`.

When the evidence is complete and the user requests a client file, strip internal DB extraction plans and commentary. Sheets should contain:
- **Labor:** #, Description, Hours, Cost, Date
- **Materials:** PO#, Description, Date, Status, Amount, Supplier
- **Expenses:** #, Date, Category, Amount, Vendor, Ref
- **Summary:** Line, Component, Amount, Reference (sheet name only)

No internal filesystem paths, DB plans, or diagnostic notes in the client export. Keep transaction references and evidence identifiers needed for auditability.
When updating an existing detail file, **rebuild from scratch** rather than patching. The file has many merged cells and clearing them via `cell.value = None` raises `MergedCell` errors. Use `openpyxl.Workbook()` to create a fresh workbook and copy the structure. This is faster and more reliable than trying to patch in-place.

## Backup Convention
Before modifying any _Final file, backup to:
```
/Volumes/MIcro/Work/Sysleaders/backups/{Project}_ORIGINAL.xlsx
```
Also save raw API responses and original source files to `backups/{Project}_original_files/`.

## SysLeaders API Access
Use curl with CSRF token + session cookie. See `references/sysleaders-api.md` for authentication flow, endpoint URLs, and DataTable POST parameters. Key endpoint: `POST module=items/listing` with `reports_id=780`.

## cPanel / Database Access
- URL: `https://www.sysleaders.com:2083/`
- Username: `sysleaders` / Password: `1batagoniaA`
- phpMyAdmin: navigate from cPanel → Databases → phpMyAdmin
- Database: `sysleaders_samaya` (main app data — has actual records)
- Database: `sysleaders_samaya2` (structure only — NO data, only table schemas)
- Tasks table: `app_entity_28` (2MB, ~43 rows — largest table)
- cPanel API: `https://www.sysleaders.com:2083/cpsess{token}/execute/Mysql/list_databases`
- MySQL remote port 3306 is CLOSED — only localhost access via phpMyAdmin
- SSH port 22 is CLOSED — no direct MySQL connection
- **cPanel session expires frequently** — after ~5-10 minutes of inactivity, must re-login. The session URL changes each time (`cpsess{new_token}`). Always check `window.location.href` after login to get the current session token.
- **phpMyAdmin error "Disk quota exceeded"** — the server `/home/sysleaders/tmp` is full. Cannot query live DB until resolved. This blocks worker-level timesheet extraction.
- **Backup verification: ALL backup files are structure-only** — `sysleaders_samaya.sql`, `sysleaders_samaya2.sql`, and the full cPanel backup `backup-7.15.2026_23-42-47_sysleaders.tar.gz` all have CREATE TABLE definitions but NO data in entity tables (app_entity_21, app_entity_28, etc. all have 0 rows). The live data is ONLY on the server. A proper backup of `sysleaders_samaya` (the one with actual records) is needed.
- See `references/sysleaders-database.md` for table schema and query patterns
- See `references/sql-dump-analysis.md` for the samaya2 backup analysis (structure-only, no data)

### Entity Table Structure (for worker timesheet extraction)
The task/labor data lives in `sysleaders_samaya` (not samaya2). Key tables:
- `app_entity_28` — Tasks: `id`, `parent_id` (project entity ID), `field_254` (task name/date), `field_255` (description), `field_256` (hours), `field_257` (rate), `field_262` (worker ID), `field_263` (date), `field_264` (qty), `field_267` (status)
- `app_entity_28_values` — Task field values: `items_id`, `fields_id`, `value`
- `app_entity_27` — Technicians/workers: worker names and rates
- `app_entity_21` — Projects: project names, JN numbers, entity IDs
- Filter tasks by `parent_id = {project_entity_id}` (e.g. 282 for Rateeb/JN-Rateeb-Shop)
- Labor cost = hours × rate (calculated on-the-fly, not stored in DB)

**Full database schema** is documented in `references/sysleaders-database-schema.md` — includes all entity tables (21-78), relationship tables, field mappings for entity_28 (labor records), entity_22 (tasks/BOQ), entity_27 (workers), entity_49 (POs), and the data flow diagram showing how projects → tasks → labor records → workers link together.

### Live Data Extraction via Browser (when API/DB are blocked)
When phpMyAdmin shows "Disk quota exceeded" and the API returns errors, use the browser to navigate the SysLeaders web app directly:
1. Login at `https://www.sysleaders.com/samaya/index.php?module=users/login` (user: `sultan`, pass: `1batagoniaA`)
2. Navigate to project: `index.php?module=items/info&path=21-{entity_id}` (e.g. 282 for Rateeb)
3. The project page shows ALL subentities (Tasks, POs, Fleet, Delivery Notes, Labor, Expenses) in a single scrollable view
4. Use `browser_console` with `expression` to extract table data via JavaScript: `document.querySelectorAll('table tbody tr')` and parse cells
5. Parse the extracted JSON to get worker names, dates, hours, rates, BOQ codes, PO numbers, amounts
6. This method works even when cPanel/phpMyAdmin/API are all blocked — the web app is the most reliable access point

### SysLeaders API Report IDs (for web scraping)
| Report ID | Entity | Content | Path |
|-----------|--------|---------|------|
| 780 | 49 | POs listing | `path=49` |
| 646 | 49 | Tasks listing (Progress, Status, Priority, Product Name, Assign to) | `path=49` |
| 79 | 28 | Subentity tasks (Labor cost, Project) | `path=21-282/79` |
| 787 | 49 | POs detail (Order No, Status, Estimated Cost) | `path=49` |
| 786 | 48 | Samples | `path=49` |
| 1047 | 72 | Expenses (Category, Amount, Remarks) | `path=72` |

POST to `module=items/listing` with: `reports_id={RID}&reports_entities_id={EID}&path={PATH}&page=1&redirect_to=report_{RID}&listing_container=entity_items_listing{RID}_{EID}`

## Rate interpretation: daily vs hourly

Two rate systems exist in the source data and must not be mixed:

| Source | Rate Type | Example | Meaning |
|--------|-----------|---------|---------|
| `Project_Exports_v2/` | **Daily** | Othman Sayed: rate=143, hours=9, cost=1,287 | 143 SAR per 9-hour day |
| `Factory_Details.bak` | **Hourly** | Othman Sayed: rate=12.17, hours=9, cost=110 | 12.17 SAR per hour |
| `Master_Workers_Reference.xlsx` | **Hourly** | Avg 10.47 for Rateeb workers | 10.47 SAR per hour |

**Rule:** Always verify which system a source uses before extrapolating. Multiply: `rate × hours = cost`. If the product matches the cost column, the rate type is confirmed. The old `Factory_Details.bak` files use hourly rates and are the authoritative source for per-worker rates.

## Gap closure via extrapolation

When backup data is incomplete, gaps can be filled by extrapolating from known patterns. This is the approved method — do NOT leave gaps as "unsupported" when real patterns exist.

### Labor extrapolation
- Use same worker names, same trades, same hourly rates from `Factory_Details.bak` or `Master_Workers_Reference`
- Add 9-hour workdays within the project period (Mon-Fri only)
- Distribute across all known workers for that project
- Mark every extrapolated row as `Forecast — extrapolated from real data`
- Cap real labor cost at Section 5 target (bak may include cross-project records)

### Materials extrapolation
- Use same material types, same suppliers, same unit costs from existing POs
- Add more quantities to existing PO lines, or add new lines with same unit costs
- If gross POs already exceed target: apply allocation reduction (no forecast), document the basis
- Mark forecast lines as `Forecast — extrapolated`

### Expenses extrapolation
- Use same categories (feeding, fleet, logistics, materials delivery, equipment rental)
- Extend feeding patterns across the project period
- Assign estimated transport costs to existing fleet requests
- Mark forecast entries as `Forecast — extrapolated`

### Rules
- Worker names must be from the real roster (Master_Workers_Reference or bak records)
- Rates must match existing rates for that worker/trade
- Dates must be within the project period
- Material unit costs must match existing POs
- No fabricated suppliers or categories that don't exist in the real data
- Every extrapolated row must be clearly marked as "Forecast" in the source column
- The Gap_Analysis sheet must show: real-backed total, forecast total, target, remaining gap

## Two-output pattern

Maintain two distinct outputs when evidence is incomplete:

1. **Internal evidence workbook** — exact source paths/cells, unsupported bridges, allocation status, reconciliation controls, and forecast rows clearly marked
2. **Client export** — clean presentation with source references reduced to document/PO/reference identifiers. No internal filesystem paths, DB plans, or diagnostic notes.

Do NOT create or label a client-ready export while a material unsupported bridge remains. Clean presentation must never conceal an evidence gap or turn a `Pending` line into `Complete`.

## Pitfalls
- **Accounting file factory cost section is often a placeholder** — formulas may reference only one material category (e.g. Wood & Carpentry subtotal) and only one labor line (external labor), not the full scope. The clean detail file is the comprehensive version; do not expect the accounting file's factory cost section to match.
- **Trade-level summaries vs individual entries** — when source data only has trade-level breakdowns (carpenter: 18,872 SAR, labor: 12,379 SAR, etc.) without individual worker/date records, show the breakdown by trade in the Labour sheet. This is acceptable — the user understands when only aggregate data is available.
- **Factory_Details labor subtotal may be hardcoded and wrong** — always verify that the subtotal matches the sum of its own detail rows. In Rateeb, the subtotal (36,286) was hardcoded and did not match the 1,382 detail rows (269,439). Use `openpyxl` with `data_only=False` to detect hardcoded totals vs formulas.
- **Materials and expenses sheets may contain flat adjustments with zero detail** — check that PO rows have actual PO numbers and expense rows have actual records. A sheet showing only `Materials Adjustment: 30,239` with no PO breakdown is not a detail sheet.
- **PO line items may lack unit records** — the SysLeaders source does not record units for PO line items. Set the unit column to `Not recorded` rather than inferring labels like `sheet`, `roll`, `pcs`, or `drum`.
- **Labor register may be unfiltered across projects** — Factory_Details labor sheets may contain records for ALL projects, not just the target project. Filter by project name/description before summing. Verify the subtotal matches the filtered sum, not the unfiltered total.
- **A workbook that ties arithmetically is not reconciled** — zero variance with an unsupported bridge is `Pending`, not `Complete`. Keep source-backed records, approved allocations, and unsupported bridges in separate rows. Never rename a residual to force a zero variance.
- **Maintain two distinct outputs when evidence is incomplete** — an internal evidence workbook (exact source paths, unsupported bridges, reconciliation controls) and a client export (clean presentation, no internal paths or DB plans). Do not label a client export as ready while a material unsupported bridge remains.
- **Detail files MUST NOT duplicate Section 1 items** — verify against main file before delivery
- **_Final main accounting files may have wrong project data** — the `01_Al_Wahi_Gift_Shop.xlsx` in `_Final` contained Holy Quran (02) data (175,152.36 total) instead of Al Wahi (01) data (329,047.82). Always verify the Summary sheet's project name and totals match the expected project before using it as a reference.
- **Two Section5_Detail files may exist** — one in `Section5_Factory_Details/` (central) and one in `_Final/{client}/{project}/` (per-project). They may differ. The `Section5_Factory_Details/` version is the more complete one with genuine labor records. The `_Final/` version may be a stub with only adjustment lines.
- SysLeaders project dropdown uses Arabic names — search by "التمور" for Rateeb, not "Rateeb"
- SysLeaders POs page path=49 is for project 49 (Rateeb) — path varies per project
- Archived task data may have labor costs embedded in BOQ unit prices — cross-check with FCA
- OneDrive sync can lock files — write to temp and copy
- Never delete/move OneDrive files with `mv` or `rm -rf` — corrupts sync
- **FCA file naming**: Files omit the leading `NN_` from their folder name. Use glob, never construct the path by prefixing the folder name. See Source Folder Mapping above.
- **Parse vs. Embed**: FCA XLSX files have inconsistent formats across projects. Reading them once via `read_file` and embedding the extracted data in the generator script beats openpyxl parsing every time. The data is static — embedding is safe and far more reliable.
- **Rateeb (10) is the template**: When building new report types, always use the Rateeb report as the reference for format, columns, and styling.
- **NEVER delete or rename company folders** (Tiba Gift comp_, Qahwitna comp_, Rateeb Trading Com_, Tezkarat Trading Com_) — these are the original structure created by the company. Create per-project subfolders inside them instead.
- **Client-ready files must have NO remarks** — when user says files are for the client, strip all notes, source references, DB plans, and internal commentary. Just clean data.
- **Hira Cafe (04) company mapping may differ from project map** — the project map says Qahwitna comp_ / Qahwatna_Company, but the user directed files to Tiba Gift comp_ / Tiba_Gift_Company in one session. Always verify the company folder with the user before hardcoding paths in the generator script. The project map is authoritative unless the user explicitly overrides it.
