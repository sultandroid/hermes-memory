---
name: risk-register-cleanup
description: Clean up a project risk-register folder per its governing Risk Management Plan (RMP), extract one clean standalone workbook per register, archive superseded files, fix README codes, with zero data loss. Triggered by "add the final PRR/DRR/AVRR/HSE register and clean up", or any time a `04_Registers/` (or equivalent) folder has accumulated drift.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [bim, risk, registers, excel, document-control, cleanup, onedrive]
    related_skills: [project-register-manager, samaya-technical-office, project-risk-register]
---

# Risk Register Folder Cleanup (Class-Level)

## When to Use

The user asks to "add the final PRR/DRR/AVRR/HSE register and clean up" a risk register folder, OR the folder shows any of these symptoms:

- Multiple competing workbooks (`C09.xlsx`, `REV00.xlsx`, etc.) with no clear "live" file
- README inside the folder uses codes that don't match the governing RMP
- Loose `.xlsx` files sitting at the folder root (no subfolder)
- Empty placeholder subfolders (`02_Design_Risk_Register/`, `03_HSE_Risk_Register/`, `04_AV_Risk_Register/`)
- Old `*_register.md` skeletons that reference snapshots which no longer exist
- The RMP source is a sibling `.md`/PDF that has authoritative terminology

## Cardinal Rules (Never Violate)

1. **Cross-check register codes against the RMP source first.** Local READMEs drift. The governing plan is authoritative. Example: local README said "DDR" but RMP source and CG documents use "DRR" (Designer Risk Register). Always grep the RMP before emitting anything.
2. **No data loss.** Every previous file must be preserved in a labelled `00_Legacy_Archive/` (or equivalent) subfolder. Never `rm` an original until the archive copy is verified.
3. **Stage in /tmp first.** Write all emitted xlsx to `/tmp/<project>_cleanup/`, verify, then `cp` to OneDrive. Never `openpyxl.save()` directly to a OneDrive path (corruption + sync-lock races).
4. **One register per file.** The final output is one clean standalone workbook per register in its matching subfolder, not one giant consolidated workbook. The consolidated workbook is the working file; the per-register files are the distribution deliverables.
5. **Verify row counts after extraction.** Header + N data rows in the emitted file must equal the source. A mismatch = data loss.
6. **Always create the destination folder before the cp.** `cp src dst_folder/` fails with "Not a directory" if the folder doesn't exist. `mkdir -p` first.
7. **Always update the root README** to match the new layout, using codes from the RMP, not from any old local README.

## Workflow

### Step 1: Inventory and Reconcile

1. List every file and folder under the target folder (e.g. `04_Registers/`)
2. Open the RMP source file and grep for register codes:
   ```
   grep -n -i -E "register|prr|drr|dgr|avrr|hse|design risk|av risk" <rmp-source>.md
   ```
3. Compare folder names + README codes against the RMP. Note discrepancies.
4. Open every `.xlsx` in the folder with openpyxl. Dump sheet names + row counts per sheet. Identify:
   - The most recent consolidated workbook (source of truth for splitting)
   - Older snapshot workbooks (to archive)
   - Loose root files (to file in the right subfolder or archive)
5. Confirm with the user before any destructive action if there's ambiguity.

### Step 2: Identify the Source of Truth

Pick the consolidated workbook with:
- The most recent modification date
- All four register sheets (PRR/DRR/HSE/AV) present
- Consistent scoring scales matching the RMP (P×S 1-4 for PRR/DRR/AV; C×L 1-5 for HSE)
- Row counts that match the RMP-stated counts (e.g. RMP §9 says "33 PRR + 37 DRR + 41 HSE + ~30 AV" — emitted counts must be in this ballpark)

Note any count discrepancies between the source and the RMP — they are signals that the source needs reconciliation against the plan before distribution.

### Step 3: Stage in /tmp

```
/tmp/<project>_risk_cleanup/
├── README.md
├── 00_Legacy_Archive/
│   ├── _ARCHIVE_INDEX.md
│   └── <copies of every file being archived>
├── 01_Master_Risk_Register/
│   └── Aseer_Museum_PRR_Final_Rev01.xlsx
├── 02_Design_Risk_Register/
│   └── Aseer_Museum_DRR_Final_Rev01.xlsx
├── 03_HSE_Risk_Register/
│   └── Aseer_Museum_HSE_Risk_Register_Final_Rev01.xlsx
└── 04_AV_Risk_Register/
    └── Aseer_Museum_AVRR_Final_Rev01.xlsx
```

### Step 4: Extract One Workbook Per Register

For each register sheet in the source, build a clean standalone workbook with three sheets:

| Sheet | Content |
|-------|---------|
| **Cover** | Title, plan reference, source workbook, issue date, issuer, status |
| **Register** | Header + data rows. Frozen top row. Auto-filter on full data range. |
| **Scoring (P×S 1-4)** | Probability / severity / score / bands reference. **Omit for HSE** (uses C×L 1-5 per RMP §6.5). |

Cell-style preservation pattern:

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

wb_src = openpyxl.load_workbook(SRC, data_only=True)
ws_src = wb_src["<sheet name>"]

wb_out = openpyxl.Workbook()
wb_out.remove(wb_out.active)
# ... build Cover ...
new_ws = wb_out.create_sheet("Register")

for row in ws_src.iter_rows(values_only=False):
    for cell in row:
        new_cell = new_ws.cell(row=cell.row, column=cell.column, value=cell.value)
        if cell.has_style:
            new_cell.font = Font(name=cell.font.name, size=cell.font.size,
                                 bold=cell.font.bold, italic=cell.font.italic,
                                 color=cell.font.color)
            if cell.fill.fill_type:
                new_cell.fill = PatternFill(fill_type=cell.fill.fill_type,
                                            fgColor=cell.fill.fgColor,
                                            bgColor=cell.fill.bgColor)
            new_cell.alignment = Alignment(horizontal=cell.alignment.horizontal,
                                           vertical=cell.alignment.vertical,
                                           wrap_text=cell.alignment.wrap_text)

for col_letter, col_dim in ws_src.column_dimensions.items():
    if col_dim.width:
        new_ws.column_dimensions[col_letter].width = col_dim.width

new_ws.freeze_panes = "A2"
new_ws.auto_filter.ref = new_ws.dimensions
wb_out.save(out_path)
```

### Step 5: Verify Row Counts

```python
for s in wb.sheetnames:
    ws = wb[s]
    n = sum(1 for row in ws.iter_rows(values_only=True)
            if row and any(c not in (None, "") for c in row))
    print(f"  [{s}] non-empty rows = {n}")
```

Expected (Aseer Museum Rev00 source): PRR=50, DRR=80, HSE=42, AV=45 (header + data). Adjust per the actual project.

### Step 6: Copy from /tmp to OneDrive

```bash
mkdir -p "<OneDrive>/04_Registers/00_Legacy_Archive"

cp /tmp/<project>_risk_cleanup/README.md "<OneDrive>/04_Registers/"
cp /tmp/<project>_risk_cleanup/00_Legacy_Archive/* "<OneDrive>/04_Registers/00_Legacy_Archive/"
cp /tmp/<project>_risk_cleanup/01_Master_Risk_Register/* "<OneDrive>/04_Registers/01_Master_Risk_Register/"
cp /tmp/<project>_risk_cleanup/02_Design_Risk_Register/* "<OneDrive>/04_Registers/02_Design_Risk_Register/"
cp /tmp/<project>_risk_cleanup/03_HSE_Risk_Register/* "<OneDrive>/04_Registers/03_HSE_Risk_Register/"
cp /tmp/<project>_risk_cleanup/04_AV_Risk_Register/* "<OneDrive>/04_Registers/04_AV_Risk_Register/"
```

### Step 7: Archive-Before-Remove Check (CRITICAL)

```bash
ls -la "<OneDrive>/04_Registers/00_Legacy_Archive/"
```

**Only proceed with `rm` if every file you intend to remove is present in the archive listing.** If the listing is short, stop and figure out why.

### Step 8: Remove Originals

Remove the now-redundant files from their previous locations:

- The old consolidated workbook from the master subfolder
- Older snapshot workbooks
- Loose root `.xlsx` files (move to archive OR file in the appropriate subfolder)
- Old `*_register.md` skeletons that reference non-existent snapshots

### Step 9: Final Tree Verification

```bash
for d in 00_Legacy_Archive 01_Master_Risk_Register 02_Design_Risk_Register \
         03_HSE_Risk_Register 04_AV_Risk_Register; do
  echo "--- $d/ ---"
  ls -la "<OneDrive>/04_Registers/$d/"
done
```

### Step 10: Rewrite the Root README

Use register codes from the **RMP source**, not from any old local README. Document:
- Register table (code, folder, scoring scale, final workbook filename)
- Folder tree
- Discrepancies fixed (e.g. "prior local README used 'DDR' in error; RMP uses 'DRR'")
- Review cadence and scoring thresholds from the RMP
- Reference the legacy archive as read-only

## Final Folder Layout

```
04_Registers/
├── README.md                      (rewritten — accurate codes + folder map)
├── 00_Legacy_Archive/             (read-only reference for superseded files)
│   ├── _ARCHIVE_INDEX.md
│   ├── <old consolidated xlsx>
│   ├── <older snapshot xlsx>
│   └── <loose root files>
├── 01_Master_Risk_Register/
│   └── Aseer_Museum_PRR_Final_Rev01.xlsx
├── 02_Design_Risk_Register/
│   └── Aseer_Museum_DRR_Final_Rev01.xlsx
├── 03_HSE_Risk_Register/
│   └── Aseer_Museum_HSE_Risk_Register_Final_Rev01.xlsx
└── 04_AV_Risk_Register/
    └── Aseer_Museum_AVRR_Final_Rev01.xlsx
```

## Archive Index Template (`_ARCHIVE_INDEX.md`)

```markdown
# Legacy Archive — Risk Registers

> **Archive Date:** YYYY-MM-DD
> **Archived By:** Samaya Technical Office
> **Reason:** Files superseded by the Final Rev01 register workbooks in folders 01-04.

The files in this folder are retained for historical reference only. They are NOT the source of truth.

| File | Why Archived | Superseded By |
|------|--------------|---------------|
| `Aseer_Museum_Consolidated_Risk_Register_C09.xlsx` | Earlier Consolidated Risk Register (snapshot C09). Superseded by REV00 master workbook. | `01_Master_Risk_Register/Aseer_Museum_PRR_Final_Rev01.xlsx` |
| `Aseer_Museum_Comprehensive_Risk_Register_REV00.xlsx` | Source workbook for the Rev01 split. Retained for traceability. | 01-04 final Rev01 workbooks |
| `ASR-SAM-RRG-001_Design_Phase_Risk_Register.xlsx` | Earlier 24-row Design Phase Risk Register. Replaced by full DRR. | `02_Design_Risk_Register/Aseer_Museum_DRR_Final_Rev01.xlsx` |
| `MOC-MUS-ASE-1K0-ZD-0093_CRS_RMP_Rev01.xlsx` | Comments Resolution Sheet for the RMP (CG review cycle). Belongs to RMP review trail, not the live register. | Plan folder `02_CG_Responses/` (see Plan) |

Do not delete. Refer to the Final Rev01 workbooks in folders 01-04 for any active risk data.
```

## Pitfalls

- **Creating the target archive folder before the cp** — `cp src dst_folder/` fails with "Not a directory" if the folder doesn't exist. Always `mkdir -p` first. This bit me on the Aseer cleanup (2026-07-25).
- **Skipping the archive-before-remove check** — if you `rm` the originals before confirming the archive copy exists, you've lost data. Memory rule: never delete user files without explicit confirmation. Archiving into a labelled folder satisfies the "preserve but relocate" intent and is auditable.
- **Trusting the local README over the RMP source** — local READMEs drift. The governing plan document is authoritative. Cross-check codes before emitting any file.
- **Forgetting to update the root README** — the README inside the parent folder is what the team actually reads. If it lists wrong codes or points to deleted files, the cleanup looks incomplete even when it isn't.
- **Mismatched count between source and emitted file** — if the extracted Register sheet has fewer rows than the source, you lost data. Verify row counts after every extraction. Example: source PRR has 49 data rows, emitted file must show 50 non-empty rows (1 header + 49 data).
- **Writing final xlsx directly to OneDrive** — openpyxl writes can race with OneDrive sync and produce corrupt placeholder files. Always stage in /tmp first, verify, then `cp`.
- **Inferring codes from folder names alone** — the folder `02_Design_Risk_Register/` does not tell you the register code. Open the RMP source and confirm. The folder name might be `Design Risk Register` while the code is `DRR` (Designer Risk Register) — not "Design Risk Register".
- **HSE register gets a P×S scoring sheet** — HSE uses C×L 1-5 per RMP §6.5 (industry HSE practice). The other three (PRR, DRR, AV) use P×S 1-4. The Scoring sheet must be omitted from the HSE workbook to avoid contradicting the source data.
- **Skipping the .DS_Store and other hidden files** — leave `.DS_Store` alone. It's harmless and the user creates it automatically. Don't touch it.

### Step 11: Update the Governing RMP Document

After the registers are cleaned up and the folder is organized, the RMP (.docx) itself needs to reflect the new counts, version references, and appendix filenames. This is a common follow-up step.

**What to update in the RMP .docx:**

| Location | Update |
|----------|--------|
| **Section 2.1** (paragraph with register version) | Bump version (e.g. C11 → C12) and date |
| **Risk summary table** (Total/Critical/High/Medium/Low) | Re-count from the latest register |
| **Register structure table** (PRR/DDR/HSE/AV counts) | Match actual data rows |
| **Register status summary table** | Update status strings, version refs, counts |
| **Appendices section** (Appendix A–D paragraphs) | Add actual file reference names (e.g. `EXP-RISK-PRR-2026-040_RevC12`) |

**python-docx technique for updating existing documents:**

```python
from docx import Document

doc = Document('path/to/document.docx')

# ── Paragraph text update (preserves formatting) ──
# WRONG: loses all run formatting (font, size, bold, color)
# paragraph.text = "New text"

# CORRECT: iterate runs and replace in-place
for run in paragraph.runs:
    if 'C11 (19-Jul-2026)' in run.text:
        run.text = run.text.replace('C11 (19-Jul-2026)', 'C12 (24-Jul-2026)')
        break

# ── Table cell update ──
# Setting .text loses multi-run formatting but is fine for simple cells
table = doc.tables[5]      # by index (0-based, documents may have many tables)
row = table.rows[1]
row.cells[0].text = '48'   # update count

# ── Finding the right paragraph ──
# Search by index (iterate document.paragraphs with debug output first)
# OR search by content substring
target_p = None
for p in doc.paragraphs:
    if 'As of live Project Risk Register' in p.text:
        target_p = p
        break

# ── Finding the right table ──
# Tables don't have IDs. Find by examining cell content in the first row:
for idx, t in enumerate(doc.tables):
    first_row_text = '|'.join(c.text for c in t.rows[0].cells)
    if 'Register' in first_row_text and 'Scoring Scale' in first_row_text:
        # This is the register status summary table
        target_table = t
        break
```

**Register xlsx column structure (Aseer Risk Register template):**

```
R0-R4: Title/info rows (merged cells)
R5:    Header — ID(1), CATEGORY(2), RISK(3), CAUSE(4), EVENT(5),
       CONSEQUENCE(6), P(7), S(8), SCORE(9), RATING(10), STATUS(11),
       OWNER(12), TARGET CLOSE(13), RESPONSE/MITIGATION(14), EVIDENCE(15)
R6+:   Data rows
```

**Counting risks by rating:**

```python
import openpyxl

wb = openpyxl.load_workbook('register.xlsx', data_only=True)
ws = wb['Risk Register']

# Find header row (look for 'ID' in column 1)
header_row = None
col_rating = None
for ri in range(1, ws.max_row + 1):
    if str(ws.cell(ri, 1).value).strip() == 'ID':
        header_row = ri
        for ci in range(1, ws.max_column + 1):
            if str(ws.cell(ri, ci).value).strip() == 'RATING':
                col_rating = ci  # typically column 10
        break

# Count data
count = 0
ratings = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
for ri in range(header_row + 1, ws.max_row + 1):
    first = str(ws.cell(ri, 1).value or '').strip()
    if not first or first.startswith('Total'):
        continue
    count += 1
    rating_val = str(ws.cell(ri, col_rating).value or '').strip()
    if rating_val in ratings:
        ratings[rating_val] += 1
```

**Pitfalls when updating .docx:**

- **Setting `paragraph.text =` destroys all run formatting** — font, size, bold, italic, color all reset to the style default. Always update within runs when the original formatting matters.
- **Table cells can have nested paragraphs** — `cell.text = new_value` replaces all content, which is fine for simple cells but destroys multi-run cells with mixed formatting.
- **TOC fields won't auto-update** — if you change section headings or page breaks, the Table of Contents in the document will be stale. The user must right-click → "Update Field" in Word.
- **Index-based paragraph access is brittle** — inserting a paragraph anywhere shifts all indices. Prefer content-matching when the text is unique enough.
- **Always save to a copy first** when testing changes to avoid corrupting the original.
- **Sync the updated .docx to both OneDrive and Micro volume** if the project uses both storage locations.

**After updating the .docx, also update:**
- The repo markdown copy (if one exists at `aseer-museum-pm/03_Plans/08_Risk/risk_management_plan.md`)
- The CRS if it references specific counts that changed

## Reporting Completion

After the cleanup, report:
- Final folder tree (one line per folder, file count + total size)
- What was archived and why (the `_ARCHIVE_INDEX.md` content as a table)
- Issues found and fixed (e.g. "README used DDR, RMP uses DRR — corrected")
- Row-count verification per emitted register (proof of no data loss)
- Explicit statement: "No data was deleted — every previous file is preserved in `00_Legacy_Archive/`."

Per the cardinal communication rule: never say "ok done". State what changed, what was moved, what was archived, and any issues found.

## Related Skills

- `project-register-manager` — broader register management umbrella (human-authored, references exist for risk-register construction)
- `samaya-technical-office` — project context, folder structure, document conventions
- `project-risk-register` — the live risk register maintenance workflow (different scope: this skill is about the *folder*, that one is about the *data*)
