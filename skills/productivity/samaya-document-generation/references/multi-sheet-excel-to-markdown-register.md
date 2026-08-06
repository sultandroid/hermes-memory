# Multi-Sheet Excel to Markdown Register — Data Extraction Pattern

Use when the user provides a multi-sheet Excel (e.g. object schedule, BOQ, material register) and asks you to study it, extract key items, and produce a markdown register.

## Steps

1. **Download the file** — if from a Zoho/cloud link, use `curl -L -o /tmp/file.zip <url>` with `--max-time 600` for large files. Background the download with `notify_on_complete=true` if >50MB.

2. **Extract** — `unzip -o /tmp/file.zip -d /tmp/outdir/`

3. **Read the Excel** — use openpyxl in read_only mode:
   ```python
   wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
   print("Sheets:", wb.sheetnames)
   ```

4. **Map columns** — each sheet may have different column positions. Build a dynamic column map from the header row (typically row 8):
   ```python
   col_map = {}
   for i, h in enumerate(headers):
       hl = h.lower()
       if 'object id' in hl: col_map['id'] = i
       elif 'display method' in hl: col_map['display'] = i
   ```

5. **Filter for target items** — e.g. AV-relevant objects by keyword matching on display method column.

6. **Generate markdown** — write a script that produces a structured .md file with summary stats, gallery breakdown, and full object tables.

## Common Pitfalls

- **OneDrive EDEADLK** — files on OneDrive may be permanently locked. Copy to `/tmp/` first, or use the Zoho download link from the email.
- **Large files** — 188MB+ Excel files take minutes to download. Use background curl with notify.
- **Column positions vary per sheet** — always build a dynamic column map, never hardcode column indices.
- **Header row varies** — some sheets have merged header rows (rows 1-7), data starts at row 8 or 9. Check each sheet.
- **TBC values** — many cells contain "TBC by client" or "n/a". Track these for risk analysis.
