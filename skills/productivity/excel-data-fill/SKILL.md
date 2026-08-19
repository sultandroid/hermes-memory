---
name: excel-data-fill
description: Fill data into existing Excel files — data only, never touch formatting, preserve existing values, leave blanks for unknowns.
tags:
  - excel
  - openpyxl
  - data-entry
  - formatting-preservation
---

# Excel Data Fill — Preserve Formatting, Fill Only Blanks

## Cardinal Rules

1. **DATA ONLY — NEVER TOUCH FORMATTING.** When filling an existing Excel file, write cell VALUES only. Do NOT change fonts, colors, fills, borders, column widths, merged cells, or any styling. The original formatting is the user's design — preserve it exactly.

2. **PRESERVE EXISTING DATA.** Before writing any cell, check if it already has a value. If the original file has data in a cell, do NOT overwrite it unless the repo has a clearly better value. Merge: fill blanks, correct only what's wrong.

3. **Leave blank for unknowns.** If a company or person is genuinely unknown, leave the cell empty. Do NOT write "TBC", "TBD", "--", or any placeholder text. Empty cells signal "not yet known" better than filler text. Exception: "TBC (System Integrator)" is acceptable when it describes the role type, not a placeholder.

4. **Column header changes only on user request.** Do not rename columns unless the user explicitly asks. If they suggest it (e.g., "replace Person to Specialist"), confirm before doing it.

## Workflow

### Step 1: Backup the original
```python
import shutil
shutil.copy2(original_path, '/tmp/backup.xlsx')
```

### Step 2: Read the original to see what exists
```python
import openpyxl
wb = openpyxl.load_workbook(original_path)
ws = wb.active
for r in range(1, ws.max_row + 1):
    vals = [ws.cell(r, c).value for c in range(1, ws.max_column + 1)]
    # Check what's already filled
```

### Step 3: Build a merge dict — only fill empty cells
```python
# For each row, only specify cells that are EMPTY in the original
# or where the original value is clearly wrong
overrides = {
    row_num: {
        'C': 'New Company',  # only if original cell C is empty
        'D': 'New Person',
    }
}

for row_num, cols in overrides.items():
    for col_letter, value in cols.items():
        col_idx = ord(col_letter) - ord('A') + 1
        existing = ws.cell(row=row_num, column=col_idx).value
        if existing is None or str(existing).strip() == '':
            ws.cell(row=row_num, column=col_idx).value = value
        # If existing has a value, skip — do NOT overwrite
```

### Step 4: Save in-place
```python
wb.save(original_path)
```

## Advanced Patterns

### Split Combined Disciplines into Separate Rows

When a single row combines two disciplines (e.g., "AV and interactive designer & supplier"), split into separate rows:

```python
ws.insert_rows(position)  # insert a new row
# Fill row N (original) with first discipline
# Fill row N+1 (new) with second discipline
# Renumber all subsequent NO values
```

### Overwrite Demonstrably Wrong Data

If the original file has clearly wrong data in a cell (e.g., "E" as a company name, " sustainibility Manager" as a company), overwrite it with the correct repo value. Use judgment — a typo in a name is not "wrong data" (preserve it), but a company name that is actually a misspelled role title is wrong.

### WhatsApp-Origin File Paths

WhatsApp files live at:
```
~/Library/Containers/net.whatsapp.WhatsApp/Data/tmp/documents/<UUID>/<filename>.xlsx
```

These files have original formatting that must be preserved. Always:
1. `cp` to a backup first
2. Work on the original path (not a copy in /tmp)
3. Only set `.value` — no formatting calls
4. Verify by re-reading after save

### Split Combined Disciplines into Separate Rows

When a single row combines two disciplines (e.g., "AV and interactive designer & supplier"), split into separate rows:

```python
ws.insert_rows(position)  # insert a new row
# Fill row N (original) with first discipline
# Fill row N+1 (new) with second discipline
# Renumber all subsequent NO values
```

### Overwrite Demonstrably Wrong Data

If the original file has clearly wrong data in a cell (e.g., "E" as a company name, " sustainibility Manager" as a company), overwrite it with the correct repo value. Use judgment — a typo in a name is not "wrong data" (preserve it), but a company name that is actually a misspelled role title is wrong.

### WhatsApp-Origin File Paths

WhatsApp files live at:
```
~/Library/Containers/net.whatsapp.WhatsApp/Data/tmp/documents/<UUID>/<filename>.xlsx
```

These files have original formatting that must be preserved. Always:
1. `cp` to a backup first
2. Work on the original path (not a copy in /tmp)
3. Only set `.value` — no formatting calls
4. Verify by re-reading after save

## Pitfalls

- **Overwriting original data is the #1 mistake.** Always read the original file first and check every cell before writing. The user will notice and correct you.
- **Formatting changes are the #2 mistake.** openpyxl preserves formatting by default when you only set `.value`. But if you call `PatternFill`, `Font`, `Alignment`, `Border`, or `ColumnDimension` methods, you overwrite the original styling. Don't call any of these.
- **Column header rename** — only do this if the user explicitly asks. If they suggest it as a question ("what do you think?"), ask for confirmation before proceeding.
- **"TBC" in company column** — the user explicitly said: if no company/person, leave blank. Do not write "TBC", "TBD", or any placeholder. Exception: "TBC (System Integrator)" is acceptable when it describes the role type.
- **OneDrive files** — copy to /tmp first, work on the copy, then copy back. Direct writes to OneDrive paths can corrupt sync.
- **Verify after write** — re-read the file and print a summary to confirm data landed correctly.
- **User repeating instruction = go to source** — If the user says the same thing 2+ times (e.g., "fill the names from your repo"), you're getting it wrong. STOP trying to reconstruct from memory. Read the ACTUAL source file to see what's already there, then fill only what's missing.
- **WhatsApp origin files have original formatting** — WhatsApp temp files under `~/Library/Containers/net.whatsapp.WhatsApp/Data/tmp/documents/` have user-designed formatting. Never apply styles to these files. Only set `.value`.

## Merged-Cell Pitfall (openpyxl `MergedCell.value` is read-only)

When a template uses **merged cells** (e.g. Samaya CRS / Comments Resolution Sheets, submittal registers with merged column groups), `ws.cell(r,c).value = x` raises `AttributeError: 'MergedCell' object attribute 'value' is read-only` for any cell inside a merge except the top-left anchor.

**Rules for merged templates:**
1. **Build a set of merged coordinates first**, then write only to unmerged cells or the top-left anchor of each merge:
   ```python
   merged = set()
   for mc in ws.merged_cells.ranges:
       for row in ws[mc.coord]:
           for cell in row:
               merged.add((cell.row, cell.column))
   def safe_set(r, c, v):
       if (r, c) in merged:
           for mc in ws.merged_cells.ranges:
               if mc.min_row <= r <= mc.max_row and mc.min_col <= c <= mc.max_col:
                   ws.cell(mc.min_row, mc.min_col).value = v  # top-left anchor only
                   return
       else:
           ws.cell(r, c).value = v
   ```
2. **To CLEAR stale template rows that live inside merges**, you cannot `= None` individual merged cells. Clear the merge's top-left anchor (and any unmerged cells). Iterate `list(ws.merged_cells.ranges)` (snapshot — the live list mutates during clearing) and set the anchor's value to None.
3. **Merged header/label cells** (e.g. `A5:C5` "CRS NUMBER") must be written through the anchor only; `ws['D5'] = ...` fails when D5 is a merge child.
4. **CRS-fill pattern** (Samaya Comments Resolution Sheet): the comment table uses merged column groups — E:I = Reviewer Comment, J:O = Originator Reply, Q:R = Reply Status, C:D = Sheet. Fill via the top-left of each group (E, J, Q, C) and the merge carries the value. Start at header+1 (usually row 11), and clear leftover template rows below your data (the old plan's comments).
5. Verify by re-reading with a compact print of the affected columns — confirm your rows landed and no stale template text remains in trailing rows.

## CRITICAL: Preserving a Merged Template's Footer & Layout

**This is the #1 failure mode when filling a merged template (CRS, submittal register, etc.): destroying the footer/legend/signature block or breaking the layout by unmerging.**

Hard rules learned the hard way:

1. **NEVER unmerge a template's data region to "fix" it.** Unmerging cells breaks the layout irreversibly. The user will say "FORMAT BROKEN" — do not go down this path. The merges ARE the format.

2. **NEVER rebuild the template from scratch** (fresh `openpyxl.Workbook()`). You lose the footer (A/B/C/D/F legend, SC/PMCM/MOC/Originator signature block, approval note) and its exact styling (bold headers, `FFCC9900` fills, medium borders). Always work on a copy of the pristine file and preserve those rows.

3. **`openpyxl.insert_rows()` does NOT shift merged cells** (verified 3.1.2). It moves cell *values* but leaves the merge definitions at their old rows — producing a broken file where merges and data are out of sync. Do not use it on merged templates.

4. **To shift the footer down (to make room for more data rows) while preserving its EXACT format: do XML-level row insertion.** Rewrite the sheet XML inside the .xlsx zip: for every `<row r="N">` with N >= footer_top, increment N (and each cell's `r="A{N}"`) by the shift amount; do the same for every `<mergeCell ref="A27:B28">` whose min row >= footer_top. This copies the footer byte-for-byte (values, merges, styles) to the new position. See `references/crs-merged-template-fill.md` for the full working recipe and a fill script.

5. **Keep the pristine backup as your base.** Before any destructive edit, save a known-good copy (e.g. to Downloads). When you need to redo, rebuild from that backup — never from a partially-destroyed working file.

6. **Fill via merge anchors only, never unmerge.** Write to the top-left cell of each merge group (`setv(r,c,v)` helper that walks `ws.merged_cells.ranges` and writes the anchor). Add extra data rows by *recreating* the same merge pattern (C:D, E:I, J:O, Q:R) for the new rows — copy the pattern from a known data row.

7. **Only the target document's comments.** When refilling a CRS for a new submittal, the template may carry a previous plan's rows (e.g. old Subcontract Management Plan comments). Clear ONLY the data region and fill with the new document's comments — never leave unrelated template content. Pull the full comment set from the actual CG submittal cover page (18 comments for 1st submittal + 5 for 2nd), not just the partial Audit Response sheet.

8. **If the user made manual edits, read and honor them** (e.g. "I made manual modification, keep it"). Compare the current file against the pristine backup to see exactly what changed, and preserve those changes when you refill.

Full working recipe + code for the XML footer-shift and merge-anchor fill: `references/crs-merged-template-fill.md`.
