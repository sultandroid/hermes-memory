# Stale CRS Template Replacement + Manual Merged-Cell Block Shift

## When to Use

A CRS `.xlsx` file is handed to you but its header AND comment rows carry content from a
**different document** (e.g. the header says "Interactive Design Specialist - Scope of Work"
while the actual submittal is "Showcase DD Drawings"). You must replace the stale header +
comments with the real Code C comments from the actual submittal, then fill replies.

This is distinct from `crs-revision-update.md` (same document, just add replies) and
`crs-from-template-cell-map.md` (fresh Code C from a blank template).

## Workflow

### 1. Detect the mismatch

Read the CRS header (rows 4-7) and compare against the actual submittal:
- `D5` CRS NUMBER, `D6` DOCUMENT No., `D7` DOCUMENT TITLE, `K6` DISCIPLINE, `K7` DOCUMENT TYPE.
- If the DOCUMENT No. / TITLE don't match the submittal you're responding to, the file is stale.

### 2. Extract the real Code C comments

The actual comments live on the submittal **cover sheet PDF** (e.g. `MOC-MUS-ASE-1A0-1G-0009.pdf`),
not in the CRS. Extract with `pdftotext -layout` and read the
`SUPERVISION CONSULTANT (CG) COMMENT:` block. Each `-` bullet is one comment. The reviewer
name, date, and `CODE -C` line are at the bottom of that block.

### 3. Replace header fields

```python
ws["D5"] = "CRS_1A0-1G-0009"      # CRS number (match doc ref)
ws["H5"] = "01"                    # Rev
ws["K5"] = "01/09/2026"            # date
ws["D6"] = "MOC-MUS-ASE-1A0-1G-0009"
ws["H6"] = "01"
ws["K6"] = "Architectural"
ws["D7"] = "Architectural Detailed Design Drawings - Showcases - 50% Design Gateway"
ws["K7"] = "Architectural DD Drawings"
```

### 4. Replace comment rows (different count than stale)

If the new comment count differs from the stale count, you must shift the legend/signature
block (rows 16-24 in the MOC template) up or down to make room. **`ws.insert_rows()` does NOT
shift merged ranges** — do it manually.

### 5. Manual merged-cell block shift (the working recipe)

```python
from copy import copy
START, END, SHIFT = 16, 24, 2   # shift legend block down 2 rows

# (a) unmerge every merge in the block
legend_merges = [m for m in ws.merged_cells.ranges if m.min_row >= START]
for m in legend_merges:
    ws.unmerge_cells(str(m))

# (b) snapshot value + style of every cell in the block
cells = {}
for r in range(START, END+1):
    for c in range(1, 18):
        cell = ws.cell(row=r, column=c)
        cells[(r, c)] = (cell.value, copy(cell._style))

# (c) clear the block — reset style via a copy of a blank cell's _style
blank = copy(ws.cell(row=1, column=1)._style)
for r in range(START, END+1):
    for c in range(1, 18):
        cc = ws.cell(row=r, column=c)
        cc.value = None
        cc._style = copy(blank)

# (d) write back shifted
for (r, c), (val, style) in cells.items():
    tgt = ws.cell(row=r+SHIFT, column=c)
    tgt.value = val
    tgt._style = style

# (e) re-merge shifted
for m in legend_merges:
    ws.merge_cells(start_row=m.min_row+SHIFT, start_column=m.min_col,
                   end_row=m.max_row+SHIFT, end_column=m.max_col)
```

### 6. Write new comment rows

For each new comment row, add the three merges first (D:H comment, I:N reply, P:Q status),
then write to the top-left cell of each merge. Copy style attributes individually from a
reference row (`copy(ref.font)`, `copy(ref.alignment)`, `copy(ref.border)`, `copy(ref.fill)`).

## openpyxl Pitfalls (all hit this session)

- **`openpyxl.styles.Style()` does not exist.** To reset a cell's style, copy `_style` from a
  blank cell: `copy(ws.cell(row=1, column=1)._style)`.
- **`MergedCell.value` is read-only.** Write `None`/value only to the top-left cell of a merge.
  Clearing a merged row means writing `None` to the top-left of each merge + each standalone cell.
- **`cell._style` is a `StyleArray`, not a Style object** — it has no `.font`/`.alignment`
  attributes. To change one attribute, build a new `Font(...)`/`Alignment(...)` and assign to
  `cell.font`/`cell.alignment` directly, then copy the rest from a reference cell.
- **`insert_rows` silently leaves merges in place** (verified: `before == after` on merge set).
  Always shift merges manually.

## Reply Voice (contractor, not designer)

Same rules as the main SKILL.md: speak as Samaya, humanize, no AI fingerprints. For a
"DD drawing only" resubmission, fabrication-level items (opening mechanisms, locking, structural
calcs) are deferred to the specialist fabricator's shop drawings / structural scope — do NOT
claim they are "in Rev 01" unless the drawings actually contain them. Flag unverified claims
to the user before finalizing.

## Deferral Reply Pattern (DD-stage drawing comments)

When CG returns Code C on a DD drawing package and the user says the detail items are NOT to be
added to the DD drawings but deferred, the reply pattern is:

> "…will be developed and provided at the next stage in the workshop drawings, coordinated with
> the specialist showcase fabricator Glasbau Hahn."

The user distinguishes THREE deferral targets — do NOT collapse them into one phrase. Match the
target to the comment type:

| Comment type | Deferral target |
|---|---|
| Mechanism / locking / hardware | **shop drawings** (fabrication-level, by the fabricator) — "workshop and fabrication items to be developed by [fabricator] in their shop drawings. The Stage 4 DD drawings establish the spatial envelope and functional arrangement." |
| Access panels / sections / details / electrical & AV outlets | **workshop drawings** (next-stage detail) — "will be developed and provided at the next stage in the workshop drawings." |
| Wall interface / finishing details at intersections | **coordination drawings** — "will be developed and provided in the coordination drawings." |
| Structural design + calculations | **structural scope** — "submitted under the structural scope, coordinated with the structural engineer, at the fabrication stage with the [fabricator] shop drawing submission." |

## Verify Before Claiming "Already Shown"

If the user asks "it's already shown, what do you think?" about a comment (e.g. electrical/AV
outlets), do NOT agree from memory — open the actual Rev 01 PDFs and confirm the item is present
before flipping the reply from "deferred" to "already shown." A false "already shown" claim is the
same credibility trap as a false "revised" claim (see SKILL.md pitfalls 0c/0g).
