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
