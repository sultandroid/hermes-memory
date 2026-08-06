# External File → Repo Markdown Conversion

## When to Use

A file arrives from an external source (Zoho download link, email attachment, Aconex, shared link) and needs to be converted to structured markdown in the repo. The original is a binary (Excel, PDF, ZIP) that can't live in the repo per the no-binaries rule.

## Typical Flow

1. **Download** — `curl -L -o /tmp/file.zip --max-time 600 "<url>"`
   - Large files (>100 MB): use `background=true, notify_on_complete=true` with 600s timeout
   - Zoho links are single-use — download succeeds once, then the link expires
   - Check `file` output after download to confirm it's a real ZIP/Excel

2. **Extract** — `unzip -o /tmp/file.zip -d /tmp/extract_dir/`
   - List contents first with `unzip -l` to understand structure
   - Zoho folders often contain: Excel schedule + reference PDFs + reference images

3. **Read Excel** — openpyxl with `read_only=True, data_only=True`
   - Multi-sheet workbooks: each sheet is a separate gallery/zone
   - Headers are typically on row 8 (not row 1) — scan rows 1-8 to find the header row
   - Column positions vary per sheet — build a dynamic column map from header text
   - Use a helper function: `def get_val(vals, key): idx = col_map.get(key); return vals[idx] if idx is not None and idx < len(vals) else ''`

4. **Analyze** — extract key insights before writing the full dump
   - Count AV-relevant objects (screen/projector/interactive)
   - Count TBC fields (unknown weight, unknown display method)
   - Identify scope gaps and risks
   - Summarize per-gallery statistics

5. **Generate Markdown** — write a Python script that produces the .md file
   - Frontmatter: title, doc_ref, source, last_updated, status
   - Summary table (key metrics)
   - AV-relevant section first (user priority)
   - Gallery-by-gallery breakdown with full object tables
   - Risk analysis section
   - Save to `01_Registers/<name>.md`

## Column Mapping Strategy

Headers vary between sheets in the same workbook. Common column names to detect:

| Key | Header patterns |
|-----|----------------|
| id | `Object ID` |
| exhibit | `Exhibit Name` |
| name | `Object/artwork name`, `artwork name` |
| artist | `Artist` |
| display | `Display Method` |
| showcase | `Showcase needed` (not `Showcase ID`) |
| medium | `Medium` |
| subtheme | `Sub-theme`, `Sub theme` |
| height | `Height`, `Height (cm)` |
| weight | `Weight` |
| desc | `Description` |
| materials | `Materials` |

Build the map with case-insensitive matching:
```python
for i, h in enumerate(headers):
    hl = h.lower()
    if 'object id' in hl: col_map['id'] = i
    elif 'display method' in hl: col_map['display'] = i
    elif 'showcase needed' in hl or ('showcase' in hl and 'id' not in hl): col_map['showcase'] = i
```

## Pitfalls

- **OneDrive "Resource deadlock avoided"** — files on OneDrive cannot be read or copied while OneDrive is running. Kill OneDrive first: `osascript -e 'tell app "Microsoft OneDrive" to quit'`. If that doesn't work, the file is a "files-on-demand" placeholder and must be downloaded via the web UI first.
- **Zoho links are single-use** — if the download times out, the link may be dead. Re-request from the sender.
- **Large Excel files** — use `read_only=True` in openpyxl. Never load the full workbook into memory for 100+ MB files.
- **Row 8 header assumption** — some sheets have headers on row 8, others on row 7 or 9. Always scan rows 1-10 to find the actual header row by looking for known column names.
- **Empty rows** — skip rows where Object ID is empty or equals "Object ID" (repeated header rows in multi-page sheets).
- **Arabic filenames in ZIP** — Zoho ZIPs may contain Arabic-named files. These extract fine on macOS but the names may not display correctly in terminal output.
