# Cross-Project Cost Reallocation Pattern

**Use when:** Multiple project folders contain cost data with misallocated, shared, or cross-project invoice lines that need to be re-assigned to the correct project.

## Workflow Overview

```
1. INVENTORY → 2. IDENTIFY CROSS-PROJECT LINES → 3. DEFINE REALLOCATION RULES → 
4. UPDATE SOURCE FILES → 5. UPDATE TARGET FILES → 6. ADD AUDIT TRAIL → 7. VERIFY
```

## Step 1: Inventory All Project Folders

Scan every project folder for costing files. Identify:
- `*_Factory_Cost_Analysis.xlsx` — the canonical analysis workbook
- Raw source files (accounting statements, bank statements from vendors/Ibrahim)
- Empty template files (can be deleted after data extraction)

## Step 2: Identify Cross-Project Cost Lines

Use parallel `delegate_task` to scan subsets of projects simultaneously. Each subagent reads ALL xlsx/xls files and flags:

- Lines mentioning **other stores by name** (e.g., "متجر التمور وتذكارات" mentioning both store names)
- Lines with **shared costs** (e.g., "مكافحة الحريق تذكارات + هدايا طيبة")
- Lines with **unclear project references** (e.g., "اجور عمالة خارجية لمشاريع مكة")
- Lines with **عهدة** (advance/custody) entries — often lack clear project reference

**Return format:** Structured report with:
- Store name, file name, sheet, row
- Description, Amount (SAR)
- Flag type (Cross-Store / Shared Cost / Unclear / عهدة)
- Which other projects are mentioned

## Step 3: Define Reallocation Rules

| Rule | Logic | Example |
|------|-------|---------|
| **Area Split** | Cost shared proportional to store area (m²) | Fire protection shared Al Wahi (240m²) + Tzkarat (51m²) |
| **Equal Split** | Cost divided equally among involved stores | Signage lettering shared between 2 stores |
| **Full Transfer** | Cost clearly belongs to another project | Billboard coded to Hira Cafe but for Ice Coffee |
| **Remain in Source** | Cost with unclear reference stays in current project | عهدة entries with no project mention |

**Yield items that need user confirmation** — some splits are judgment calls (which 2 stores for a max-2-shops item, etc.).

## Step 4: Update Source Files (Outgoing)

For each project losing cost lines:
1. **Remove the item** from the Cost_Register
2. **Renumber remaining items** sequentially
3. **Recalculate subtotals** in Factory_Work sheet
4. **Update Dashboard** total
5. **Merge labor rows** into one "Factory Labor Cost" line (per user preference)
6. **Keep only Engineering Supervision 10%** (remove PM 5%)

## Step 5: Update Target Files (Incoming)

For each project gaining cost lines:
1. **Add new items** to the Cost_Register with appropriate category (typically "Reallocated Costs")
2. **Recalculate totals**
3. Same labor merge and supervision adjustments as source files

## Step 6: Add Reallocation_Log Sheet (Audit Trail)

Add a `Reallocation_Log` sheet to **every** Factory_Cost_Analysis.xlsx that was affected:

**Source files** (items moved OUT): Columns: #, Description, Amount (SAR), Moved To, Split Method
**Target files** (items moved IN): Columns: #, Description, Amount (SAR), Source Project, Split Method

Format:
- Navy header (#1E293B, white bold font)
- Number formatting #,##0.00 on amounts
- Include a note on the Dashboard sheet referencing the Reallocation_Log

## Step 7: Verify

Use a Python script to read all Cost_Register sheets and compare summed amounts against declared totals. Flag any mismatch.

## Parallel Delegation Structure for This Workflow

The work splits naturally into independent streams:

| Phase | Parallel Tasks | Each Handles |
|-------|---------------|--------------|
| **Inventory** | 3 subagents | ~4-5 stores each, scan all files |
| **Update source files** | 1-3 subagents | Rebuild FCAs for stores losing costs |
| **Update target files** | 1-3 subagents | Rebuild FCAs for stores gaining costs |
| **Add audit logs** | 2-3 subagents | Add Reallocation_Log to source + target files |

**Key:** Subagents modify different files — no concurrency conflicts.

## Common Pitfalls

- **Renumbering errors** — after removing items, the remaining items must be renumbered sequentially. A gap breaks the register flow.
- **Formula references** — some FCAs use SUMIF formulas that don't cache values in data_only mode. The file must be opened in Excel to calculate. Add a note.
- **Labor merge + supervision cleanup** — these are user preferences that must be applied consistently across ALL files. Don't forget any file.
- **Reallocation_Log in both directions** — the user corrected: source file must say WHERE it went, target file must say WHERE it came from. Both sides are required.
- **Arabic description preservation** — keep original Arabic descriptions in the Reallocation_Log, don't translate to English-only.
