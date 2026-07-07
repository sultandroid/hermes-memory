# CG Data Package — Extract, Compare, Forward

When CG sends a data file (Excel/PDF) with object schedules, material lists, or other structured project data, the workflow is:

## 1. Download & Stage

- Files may arrive via email attachment, cloud link (Zoho/WeTransfer/SharePoint), or user downloads manually
- If cloud link: flag to user for manual download (not auto-downloadable from sandbox)
- Stage to a temp location, then copy to project subfolder

## 2. Extract Structured Data

- For Excel: use `openpyxl` via system Python (`terminal(python3 -c "...")`) — NOT `execute_code` sandbox
- For PDF: use `pdftotext` or `pymupdf`
- Identify header rows by scanning for known column names (e.g., "Showcase ID", "Object ID", "Showcase needed")
- Map columns by header text, not position — sheets may have different column layouts

```python
# Pattern: find header row and column positions
for r in range(1, min(ws.max_row+1, 10)):
    for c in range(1, ws.max_column+1):
        v = ws.cell(r, c).value
        if v and 'Showcase ID' in str(v):
            showcase_id_col = c
            header_row = r
```

## 3. Compare Against Previous Version

- Check if a previous version exists in the project (old package, earlier schedule)
- Compare: total object counts, per-showcase counts, new/removed showcases
- Report delta in a compact table

| Dimension | Old | New | Delta |
|-----------|:---:|:---:|:-----:|
| Total objects | 53 | 80 | +27 |
| Showcases | 23 | 24 | +1 |

## 4. Create Mapping Deliverable

- Build a structured mapping (object → showcase) from the extracted data
- Two formats: **Markdown** (for reference) and **Excel** (for forwarding)
- Excel should have 3 sheets:
  - **Sheet 1 — Object to Showcase Mapping**: one row per object, with Gallery, Showcase ID, Object ID, Exhibit ID, Object Name, Status, Notes
  - **Sheet 2 — Summary**: gallery-level totals
  - **Sheet 3 — CG Study Requests**: any specific design/study requests from CG, with action items for each recipient

### Excel Formatting (Formal)

- Dark blue title header (`1F3864`) with white bold text
- Medium blue column headers (`2F5496`)
- Gallery section dividers in light blue (`D6E4F0`)
- Alternating row shading (`F2F2F2`)
- Color-coded status: green (`548235`) for Available, amber (`BF8F00`) for TBC/Needs Sourcing
- Red (`C00000`) or orange (`ED7D31`) for CG study request notes
- Frozen panes below header, auto-filter enabled
- Landscape print layout, fit to width

## 5. Determine Forwarding

After extracting and mapping, answer: **who needs what?**

| Recipient | What They Need | Why |
|-----------|---------------|-----|
| **Design lead** (NRS) | Full object schedule + plans + study requests | They design the showcases around the objects |
| **Manufacturer** (Glasbau Hahn) | Object schedule + rock study request | They need object weights/dimensions for structural design |
| **CG** | Nothing — they sent it | They expect responses to study requests |

### Drafting the Forwarding Email

- State clearly: "CG sent the Ministry-approved [document type]"
- List what's included (bullet points)
- Quote CG's key instructions verbatim
- List any study requests with clear "what we need from you" per item
- Provide the file path or attach the mapping deliverable

## 6. File to Project

- Create a dated subfolder: `04_Submittals/Showcase/YYYY-MM-DD_CG_Description/`
- Copy all source files + the mapping deliverable
- Update the project's OBJECT_TO_SHOWCASE_MAPPING.md if one exists

## Pitfalls

- **Excel column positions vary** — always scan for header text, don't hardcode column indices
- **Merged cells in source Excel** — openpyxl reads merged cells as None in non-anchor cells. Use `data_only=True` and scan row-by-row
- **Cloud stubs on OneDrive** — if the target folder is on OneDrive, verify the file is a real ZIP before openpyxl operations
- **CG study requests are often embedded in the email body, not the attachment** — always read the full email text (AppleScript) to catch them
- **Object names may be in Arabic** — translate for English output, keep original in the Excel for reference
