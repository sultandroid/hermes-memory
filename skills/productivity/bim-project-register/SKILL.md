---
name: bim-project-register
description: "Create or update all 14 project registers for a BIM Unit project from file scan. Always update ALL registers, not just Drawing and Submittal."
version: 1.0.0
author: Hermes Agent
platforms: [macos]
metadata:
  hermes:
    tags: [BIM, Project-Management, Registers, Excel, Samaya]
---

# BIM Project Register — Creation & Update from File Scan

When tasked to create or update a project register in the Samaya BIM Unit, follow this workflow exactly.

## 🔴 CRITICAL RULE: Date Logic for O&M/Handover Items

**O&M, handover, close-out, as-built, commissioning, training, spare parts, and warranty items MUST only have dates in the IFC/AFC column.** Never place these dates in 50%, 90%, or 100% columns — these deliverables are produced at project handover, not during design stages.

**Exception:** Existing-building surveys (pre-design condition records) may appear in the 50% column, but their description must say "Existing Building Survey" or "Existing Condition" — not "As-Built" — to avoid confusion with project handover as-builts.

**Always run the date logic audit script** from `submittal-register-management` skill (`scripts/audit_register_dates.py`) before finalizing any register.

## 🔴 CRITICAL RULE: NEVER Create New Files

**Only append rows to existing Excel files.** Never create new register files from scratch. If a register file doesn't exist, ask the user before creating one. Always scan the project for existing `.xlsx` files first in all subdirectories.

Existing files have these sheet names per register type:
- RFI_Register.xlsx → Data sheet: "RFI"
- SI_Register.xlsx → "SI"
- NCR_Register.xlsx → "NCR"
- Change_Order_Register.xlsx → "Change Order" or "ChangeOrder"
- Material_Register.xlsx → "Material"
- Invoice_Register.xlsx → "Invoice"
- Meeting_Minutes_Register.xlsx → "Meeting Minutes" or "MeetingMinutes"
- Transmittal_Register.xlsx → "Transmittal"
- Contract_Register.xlsx → "Contract"
**Risk_Register.xlsx → "Risk"**
- Simple register for tracking identified risks during project execution.
- **For comprehensive risk registers** (20+ risks, 24-column structure, P×I matrix, RBS taxonomy, heat map, executive dashboard with KPI cards and charts) → use `project-risk-register` skill instead.
- HSE_Register.xlsx → "HSE"
- Submittal_Register.xlsx → "Submittal"
- Drawing_Register.xlsx → "Drawing"

**Always verify after saving:** Re-open and check headers are present, data rows correct.

## The 14 Registers

Every project has these registers in `Docs/09_Registers/`:
1. **Drawing_Register.xlsx** — all drawing files (CAD, PDF)
2. **Submittal_Register.xlsx** — all submittal packages
3. **RFI_Register.xlsx** — Request for Information
4. **SI_Register.xlsx** — Site Instruction
5. **NCR_Register.xlsx** — Non-Conformance Report
6. **Change_Order_Register.xlsx** — change orders
7. **Material_Register.xlsx** — material approvals
8. **Invoice_Register.xlsx** — invoices
9. **Meeting_Minutes_Register.xlsx** — meeting minutes
10. **Transmittal_Register.xlsx** — transmittals
11. **Contract_Register.xlsx** — contracts
12. **Risk_Register.xlsx** — risks
13. **Subcontractor_Register.xlsx** — subcontractors
14. **HSE_Register.xlsx** — health, safety, environment

## Step-by-Step Workflow

### 1. Always Show Todo List First
Before starting, display the full todo list to the user so they know exactly what will be done.

### 2. Scan Project Files
Use Python `os.walk` to scan all files in the project folder (skip `Library/Caches`). Categorize by:
- Drawing files (`.dwg`, `.dxf`, `.pdf` in Design Files / Submittals folders)
- Submittal files (`.pdf` in Submittals folder)
- Contract files (in Contracts folder)
- BOQ files (in B.O.Q folder)
- Other register-relevant files

### 3. Create/Ensure Folder Structure
Ensure `Docs/09_Registers/` exists. If not, create it.

### 4. Create Register Excel Files

Each register has 2 sheets:
- **Cover** — project info, revision history
- **[Name]** — data rows with headers

Use openpyxl. Always include:
- Project name and Arabic name
- Contractor: Samaya Investment
- Revision history entry
- Auto-filter on data sheet

### 5. Always Show Todo List at Start
When the user assigns a register update task, always display the todo list first.

## Register Structure Template

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from datetime import datetime
import os

def make_cover(ws, title, subtitle, project, project_ar, contractor):
    ws.merge_cells('B2:E2')
    ws['B2'] = 'PROJECT REGISTER'
    ws['B2'].font = Font(bold=True, size=14)
    ws.merge_cells('B4:E4')
    ws['B4'] = title
    ws['B4'].font = Font(bold=True, size=18)
    ws['B7'] = 'Project:'; ws['C7'] = project
    ws['B8'] = 'Project (AR):'; ws['C8'] = project_ar
    ws['B9'] = 'Contractor:'; ws['C10'] = contractor
    ws['B13'] = 'REVISION HISTORY'
    ws['B13'].font = Font(bold=True)
    # ... revision headers ...
    ws['C14'] = '00'
    ws['D14'] = datetime.now().strftime('%Y-%m-%d')
    ws['E14'] = 'Initial Register Creation'
    ws['F14'] = 'Hermes AI'
```

## Drawing Register Columns
Date, Drawing #, Title, Discipline, Scale, Sheet Size, Rev, Status, File Path

## Submittal Register Columns
Date, Submittal #, Title, Type, From, To, Status, Due Date, File Path, Remarks

## Watchdog (Automatic Register Updates)

A watchdog script monitors Submittal's and Design Files folders across all 17 BIM projects and auto-updates registers.

**Script:** `~/.hermes/scripts/bim_watchdog.py`
- `--scan` : One-shot scan (used by cron every 2 minutes)
- `--daemon` : Continuous FSEvents mode (macOS native)

**Cron:** Job `048f24e5d9dd` — runs `bim_watchdog.py --scan` every 2 minutes

**State file:** `~/.hermes/scripts/.watchdog_state.json` (file hashes, 12,868 entries)
**Log:** `~/.hermes/scripts/bim_watchdog.log`
**Notify script:** `~/.hermes/scripts/hermes_notify.sh`

**What it does:**
- On new/modified files in `Submittal's/` or `Design Files/` → auto-adds rows to Drawing_Register and Submittal_Register
- Uses `is_valid_register()` to detect OneDrive cloud-stub register files (~6.5 KB placeholders) before calling `openpyxl.load_workbook()` — skips with WARNING instead of ERROR
- Sends Telegram notification with file name and updated register info
- Skips: `.bak`, `.tmp`, `Cache`, `Archive`, `.DS_Store`, `~` prefixed files

**Projects watched (17):** Aseer-Museum, El-Ghamama (4 projects), Zamzam Museum, Zamzam Visitor Center, El-Haramain, Hera' Ghar, Masjid Alnoor, Khair El-Khalq, Jabal Al-Noor Dispatch, Prime Business Resort, Jabal Omar retail shops (3)

**To pause:** `cronjob remove 048f24e5d9dd`
**To force scan now:** `python3 ~/.hermes/scripts/bim_watchdog.py --scan`

## Tips
- Use proper drawing IDs: DWG-001, PDF-001, etc.
- Use proper submittal IDs: SUB-001, SUB-002, etc.
- Check for duplicates before adding new rows
- Always normalize file paths to relative paths from project root
- Save the Excel with auto-filter on the data sheet

---

## Pitfalls & Lessons Learned

### ⚠️ `execute_code` Does NOT Have openpyxl
The sandbox for `execute_code` does NOT have openpyxl installed. **Use the `terminal` tool with `/usr/bin/python3` for ALL register operations.** Commands like:
```bash
cd /path/to/Registers && /usr/bin/python3 -c "import openpyxl; ..."
```
or write to a `.py` file and run: `/usr/bin/python3 /path/to/script.py`

### ⚠️ `ws.append()` Fails on Empty/Headerless Sheets
If a data sheet has 0 rows OR only a blank merged-cell row, `ws.append()` places data into **row 1** (overwriting where a header should go) because openpyxl's `max_row` is 0 or 1.

**Fix — always use explicit row assignment:**
```python
wb = openpyxl.load_workbook(path)
ws = wb[data_sheet_name]

# Clear ALL cells first to remove merged-cell artifacts
for row in ws.iter_rows():
    for cell in row:
        cell.value = None

# Write header at row 1 (openpyxl is 1-indexed)
for col_idx, header in enumerate(HEADERS, start=1):
    ws.cell(row=1, column=col_idx, value=header)

# Write data starting at row 2
for col_idx, val in enumerate(row_data, start=1):
    ws.cell(row=2, column=col_idx, value=val)

wb.save(path)
```

### ⚠️ Cover Sheet "Last Updated" Uses Merged Cells
The Cover sheet's "Last Updated" label often lives in a merged cell region. When iterating rows with `iter_rows()`, merged cells return `None` for `cell.value` on all but the anchor cell. The search `cell.value and "Last Updated" in str(cell.value)` silently skips merged cells.

**Fix:**
```python
wc = wb["Cover"]
for row in wc.iter_rows():
    for cell in row:
        try:
            if cell.value and "Last Updated" in str(cell.value):
                cell.value = f"Last Updated: {TODAY}"
                break
        except AttributeError:
            continue  # merged cell — skip
```

### ⚠️ Register Data Sheet Names Differ
Each register's data sheet has a specific name. Always look up by name, not by index:
```python
DATA_SHEET = {
    "RFI_Register.xlsx":          "RFI",
    "SI_Register.xlsx":           "SI",
    "NCR_Register.xlsx":          "NCR",
    "Change_Order_Register.xlsx":  "ChangeOrder",
    "Material_Register.xlsx":     "Material",
    "Invoice_Register.xlsx":       "Invoice",
    "Meeting_Minutes_Register.xlsx": "MeetingMinutes",
    "Transmittal_Register.xlsx":  "Transmittal",
    "Contract_Register.xlsx":     "Contract",
    "Risk_Register.xlsx":         "Risk",
    "Subcontractor_Register.xlsx": "Subcontractor",
    "HSE_Register.xlsx":          "HSE",
}
```

### ✅ Always Verify After Saving
After any register write, re-open the file and check:
- Header row is present and non-None
- Data row count is correct
- Cover "Last Updated" was actually updated

### 📁 Reusable Scripts
See `scripts/add_rows_to_registers.py` — copy it to a project folder and edit
`ROWS_TO_ADD` to append rows to any register non-destructively.

---

## Reference: Standard Column Headers Per Register

| Register | Data Sheet | Columns |
|---|---|---|
| RFI | RFI | Date, RFI #, Subject, From, To, Status, Priority, Response, File Path, Remarks |
| SI | SI | Date, SI #, Subject, From, To, Status, File Path, Remarks |
| NCR | NCR | Date, NCR #, Description, Discipline, From, To, Status, File Path, Remarks |
| Change Order | ChangeOrder | Date, CO #, Description, From, To, Status, File Path, Remarks |
| Material | Material | Date, Material #, Description, Type, Status, File Path, Remarks |
| Invoice | Invoice | Date, Invoice #, Description, Contractor, Amount, Status, File Path, Remarks |
| Meeting Minutes | MeetingMinutes | Date, MM #, Subject, Location, Time, Status, File Path, Remarks |
| Transmittal | Transmittal | Date, Transmittal #, Subject, From, To, Status, File Path, Remarks |
| Contract | Contract | Date, Contract #, Description, Contractor, Status, File Path, Remarks |
| Risk | Risk | Date, Risk #, Description, Impact, Probability, Mitigation, Status, File Path, Remarks |
| Subcontractor | Subcontractor | Date, SC #, Name, Scope, Status, File Path, Remarks |
| HSE | HSE | Date, HSE #, Description, Type, Status, File Path, Remarks |