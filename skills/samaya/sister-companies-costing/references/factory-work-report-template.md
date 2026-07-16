# Factory Work Detail Template (Section 5 Breakdown)

Each project gets a detail file in its `_Final` client folder that breaks down ONLY Section 5 (تكاليف المصنع) from the main project file. The detail file MUST NOT duplicate items from Section 1 (Accounting).

## Path
```
_Final/{Client_Folder}/{Project}_Factory_Labor_POs_Expenses.xlsx
```
Example: `_Final/Rateeb Trading Com_/Rateeb_Factory_Labor_POs_Expenses.xlsx`

## CRITICAL RULE: No Duplication
The main `_Final` file has 6 sections:
- Section 1: Accounting (Ibrahim invoices) — items belong HERE
- Section 2-3: Reallocation (outgoing/incoming)
- Section 4: Summary by type
- **Section 5: Factory Cost (تكاليف المصنع)** — THIS is what the detail file covers
- Section 6: Grand Total with 10% supervision

**The detail file breaks down Section 5 ONLY.** Items in Section 1 (AC units, cashier devices, external labor, air curtains, gypsum, etc.) are NOT factory costs — they are accounting items and must stay in the main file, not repeated in the detail file.

### Common Duplication Pitfalls (check these specifically)
| Item | Belongs in | Often wrongly placed in |
|------|-----------|------------------------|
| External labor (site workers) | Section 1 — Accounting | Section 5 — Factory Labor |
| AC units, air curtains | Section 1 — Accounting | Section 5 — Other |
| Cashier devices, POS equipment | Section 1 — Accounting | Section 5 — Materials |
| Gypsum works subcontract | Section 1 — Accounting | Section 5 — Other |
| Transport/fleet (site) | Section 1 — Accounting | Section 5 — Other |
| Factory POs (Corian, wood, paint, glass) | Section 5 — Materials | Section 1 — Accounting (correct) |

## Verification Protocol (MANDATORY before delivery)
1. Read the main `_Final/{Project}.xlsx` file's Section 5 values (lines 1-3 + total)
2. Read the detail file's 4_Section5_Summary sheet totals
3. Confirm each line matches exactly
4. Confirm NO Section 1 items appear in the detail file (check Expenses sheet against main file's accounting section)
5. If mismatches found, fix the detail file — do not deliver with wrong totals
6. Create backup of main file before any modification: `cp main.xlsx /Volumes/MIcro/Work/Sysleaders/backups/{Project}_ORIGINAL.xlsx`

## Sheet Structure (5 sheets, one per Section 5 line + timesheet)

### Sheet 1: 1_Factory_Labor — تفصيل عمالة المصنع
Maps to Section 5, Line 1 (Factory Labor). Must equal that amount exactly.
- Table: #, Job Type, Workers, Hours, Rate/hr, Cost, Source
- 3 FCA trades (carpenter/fiber/welder) as separate rows
- Remaining balance as "SysLeaders BOQ Labor" row
- BOQ task detail section below: BOQ, Task, Qty, Unit, Labor/Unit, Total, Status
- Note: SysLeaders labor = rate × hours, calculated on-the-fly

### Sheet 1b: 1b_Labor_Timesheet — سجل ساعات العمل
Inserted between 1_Factory_Labor and 2_Raw_Materials. Worker-level records.
- Columns: #, Date / التاريخ, Worker Name / العامل, Trade / التخصص, Hours, Rate/hr, Cost (SAR), Task/BOQ, Status
- Trade-level summary rows with record counts (e.g., "Carpenter: 9 records, 78.5 hrs, 962 SAR")
- SysLeaders BOQ Labor row for calculated-on-the-fly tasks
- Total row matching Section 5 Line 1
- SysLeaders extraction plan documented at bottom
- Data source: `app_entity_28` in `sysleaders_samaya` database
- Labor cost = hours × rate (calculated on-the-fly, not stored in DB)

### Sheet 2: 2_Raw_Materials — تفصيل مواد خام المصنع
Maps to Section 5, Line 2 (Raw Materials). Must equal that amount exactly.
- PO line items from SysLeaders with qty/unit cost/total
- SysLeaders POs subtotal
- "Less: Shared/Factory overhead allocation" line to reconcile difference
- POs may total MORE than Section 5 — the difference is shared factory costs

### Sheet 3: 3_Other_Costs — تفصيل أخرى
Maps to Section 5, Line 3 (Other — logistics/transport/subcontract). Must equal that amount exactly.
- Transport/fleet items
- Subcontract items (e.g., gypsum retained portion)
- Balance row for TBD items needing SysLeaders data

### Sheet 4: 4_Section5_Summary — ملخص القسم 5
- 3-line table matching Section 5 exactly: Line 1 (Labor), Line 2 (Materials), Line 3 (Other)
- TOTAL SECTION 5 row
- Reference section listing what IS and IS NOT in this file
- Status column (Partial/Complete) per line

## Style Conventions
- Navy fill: `#1E293B` with white bold Calibri 10-11pt
- Gray subtotals: `#E2E8F0`
- Section headers: Calibri 12pt bold, `#1E293B`
- Data cells: Calibri 10pt, thin border `#D1D5DB`
- Notes: Calibri 9pt italic, `#999999`
- All amounts: `#,##0.00` number format
- RTL sheet view: `ws.sheet_view.rightToLeft = True`
- Partial status: yellow `#FEF3C7` fill

## Data Sources
| Component | Source |
|-----------|--------|
| Section 5 totals | Read from existing `_Final/{Project}.xlsx` |
| FCA labor | `{NN}_{Project}/_{Project}_Factory_Cost_Analysis.xlsx` |
| SysLeaders POs | Live API (curl) or archived `Pruchasing-Orders_{Project}.xlsx` |
| SysLeaders BOQ tasks | `tasks_{Project}.xlsx` or live API listing |
| Fleet/transport | Raw cost data files |

## Verification Checklist
- [ ] Read Section 5 values from main _Final file FIRST (3 lines: Labor, Materials, Other)
- [ ] All 4 sheets populated
- [ ] Each sheet total matches its Section 5 line exactly
- [ ] No items from Section 1 (Accounting) appear anywhere
- [ ] No external labor, AC, cashier, air curtain, or gypsum items
- [ ] Reference section clearly states what is NOT in this file
- [ ] Backup created before modifying
- [ ] 1b_Labor_Timesheet has trade-level summaries (even if individual records are TBD)
