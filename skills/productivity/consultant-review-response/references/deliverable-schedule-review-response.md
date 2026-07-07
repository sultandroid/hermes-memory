# Deliverable Submission Schedule — Review Comment Response

When Samaya Tech Office (or CG/PMC) returns review comments on a Deliverable Submission Schedule (Excel), produce a revised schedule that addresses every comment.

## Trigger Phrases

- "deliverables submission schedule comments"
- "review comments on the schedule"
- "revised schedule reflecting comments"
- "response to comments on submission schedule"

## Workflow

### Step 1: Extract Comments from PDF

```bash
pdftotext "path/to/comments.pdf" -
```

Read the output. Identify each distinct review item. Classify by type:

| Type | Example | Action |
|------|---------|--------|
| **Symbol/Format** | "Avoid § symbol" | Replace throughout schedule |
| **Period Error** | "14 WD ≠ 14 CD" | Fix review period column |
| **Missing Scope** | "Missing: Demolition Plans" | Add new items or flag as outside scope |
| **Detail Insufficient** | "3H+3V sections needed" | Update description/notes |
| **Restructure** | "MEP DD separated by discipline" | Split existing items |
| **New Content** | "Structural survey, geotech, core tests" | Add entirely new section |

### Step 2: Map Each Comment to Schedule Changes

Build a mapping:

| Comment | Schedule Action | Items Affected |
|---------|----------------|----------------|
| Replace "§" with "Section" | Replace all "§" references | All cells |
| 14 WD ≠ 14 CD | Change Review Period column | All rows |
| Missing Demolition Plans, Master Plan, General Layout | Add ARCH-nnn items with producer note | New section |
| Add 3 horizontal + 3 vertical sections | Update DD-06 notes | DD-06 |
| Separate MEP DD by discipline | Split DD-24 → DD-24A/B/C | 3 new items |
| Add MEP calculations date | New DD-24D item | 1 new item |
| Separate MEP material submittals | Split MS-03 → MS-03A/B/C | 3 new items |
| Separate IFC by discipline | Split IFC-01 → IFC-01A/B/C | 3 new items |
| Add structural items | New DD-35–42 + IFC-02–05 | 12 new items |

### Step 3: Produce Revised Excel (Python + openpyxl)

Key patterns to follow:

**Add a response header row (Row 3)**
```python
ws.merge_cells('A3:J3')
c = ws['A3']
c.value = 'REVISED PER TECH OFFICE COMMENTS (DATE): "Section" replaces "§" | Review Period = WD only | MEP/IFC/MS split | Structural items added'
c.font = Font(name='Calibri', size=8, bold=True, color='C00000')
```

**Color conventions for changes:**
- **Yellow fill** (`FFF2CC`) — NEW items (split from existing or added per comments)
- **Orange fill** (`FCE4D6`) — Architectural items outside current scope (for coordination with other parties)
- **Blue section headers** (`D6E4F0` + `1F4E79` text) — Section grouping rows
- **White with alt row shading** (`F2F7FB`) — Existing items unchanged

**When splitting an item** (e.g., DD-24 → DD-24A/B/C/D):
- Assign new ref codes with letter suffix (A, B, C, D)
- Keep original submit date and IFC target
- Update producer and SOW ref for each split
- Mark IS_NEW for yellow highlighting
- Retain the original item number in its section (don't renumber existing items)

**When adding a new section** (e.g., structural items):
- Create a blue section header row
- Assign sequential ref codes (DD-35, DD-36, etc.)
- Mark as IS_NEW
- Add IFC follow-on items if needed (IFC-02, IFC-03, etc.)

### Step 4: Prohibited Character Replacement

Replace all instances of `§` with `Section` or `Clause` in every cell — not just visible cells but also the SOW Reference column, Notes column, section headers, and data in merged cells. This is a bulk text replacement, not a find-and-replace on a single column.

### Step 5: Review Period Correction

Change all instances of `14 CD` or `14 CD / 14 WD` to `14 WD` in the Review Period column. If some items genuinely have different periods (e.g., PMC review is 14 calendar days), note that explicitly in Notes.

## Python / openpyxl Patterns

### Column Setup
```python
col_widths = {'A': 5, 'B': 10, 'C': 46, 'D': 18, 'E': 22, 'F': 12, 'G': 12, 'H': 12, 'I': 12, 'J': 42}
for col, w in col_widths.items():
    ws.column_dimensions[col].width = w
```

### Row Writer Helper
```python
row = 6
def write_item(ref, desc, producer, sow_ref, submit, review='14 WD', resubmit='TBD', ifc_target='TBD', notes='', is_section=False, is_arch=False, is_new=False):
    global row
    if is_section:
        ws.merge_cells(f'A{row}:J{row}')
        c = ws.cell(row=row, column=1, value=desc)
        c.font = section_font; c.fill = section_fill; c.alignment = Alignment(vertical='center'); c.border = thin_border
        row += 1; return
    vals = [row-5, ref, desc, producer, sow_ref, submit, review, resubmit, ifc_target, notes]
    for i, v in enumerate(vals, 1):
        c = ws.cell(row=row, column=i, value=v)
        c.font = normal_font; c.alignment = center_wrap if i in (1,6,7,8,9) else wrap; c.border = thin_border
        if is_new:
            c.fill = yellow_fill
            if i == 1: c.font = Font(name='Calibri', size=9, bold=True, color='C00000')
        elif is_arch:
            c.fill = arch_fill
        elif row % 2 == 0:
            c.fill = alt_fill
    ws.row_dimensions[row].height = 34
    row += 1
```

### Print Setup
```python
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0
ws.page_setup.orientation = 'landscape'
ws.page_setup.paperSize = ws.PAPERSIZE_A3
ws.freeze_panes = 'A6'
```

## Pitfalls

- **Don't renumber existing items** — only assign numbers to new items. Renumbering breaks the established reference system.
- **Don't remove original items** — they may have been delivered (Done) or have accepted dates. Only add, split, or update notes.
- **Don't embed "§" in replacement text** — the comment explicitly prohibits this. Use "Section" or "Clause."
- **Architectural drawings (Demolition, Master Plan, General Layout)** — these are typically outside the exhibition fit-out scope (NRS). Add them as ARCH-nnn items in a separate section with the producer "Architect of Record" and note "coordinate with AOR."
- **Review period correction** is not just changing "CD" to "WD" — the Samaya comment says 14 WD ≠ 14 CD, so all dates should be recalculated. If you don't have the KSA holiday calendar, flag dates as TBD and note the recalculation requirement.
- **Section headers need merged cells across all 10 columns** — `ws.merge_cells(f'A{row}:J{row}')`. Without this, the section header only occupies column A.
