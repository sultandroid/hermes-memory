# Subcontractor Folder Creation Workflow

Full procedure for standing up a new subcontractor folder under `Subcontractors/`.

## Step-by-step

### 1. Create folder + standard structure

```bash
SUBS="/Users/.../Aseer-Museum/Subcontractors"
mkdir -p "$SUBS/NN_Name/"{01_Schedule_and_BOQ,02_Reference_Drawings,03_Specifications_and_Standards,04_Reference_Imagery,05_Returned_Submittals,06_RFIs,07_Approvals,Email_Data_Extraction,_MANAGER_DASHBOARD}
```

### 2. Write SCOPE_REQUEST.md → `_MANAGER_DASHBOARD/`

The .md is the **editable source** — goes in `_MANAGER_DASHBOARD/`, NOT at sub root.

Mandatory header fields:
- Project name, Issuer, Issued to, Issue date, Reply by, Discipline
- Contract ref: `0010003521`
- KPR Register ID (e.g., "Tier 3 — CITC-Registered Telecom Engineer (R26)")
- Subcontractor Register ID (e.g., "F-03 CITC Telecom Engineer")
- Privity note

Standard sections: 1. Purpose, 2. Programme, 3. Scope, 4. Submission Requirements, 5. Reference Documents, 6. Workflow, 7. Sign-offs, 8. Action

### 3. Generate SCOPE_REQUEST.docx at sub root

Use the `SamayaDoc` template with `set_table_widths()` post-processing (see `docx-generation-example.md`).

- **Read** .md from `_MANAGER_DASHBOARD/`
- **Save** .docx at sub root (same level as `_MANAGER_DASHBOARD/`)
- **Doc ref:** `MOC-ASEER-SIC-1K0-SC-NNN` incrementing per sub
- **NEVER** pass `col_widths_cm` to `add_table()` — use `set_table_widths()` after

### 4. Create SITUATION_REPORT.md → `_MANAGER_DASHBOARD/`

Auto-fill status fields:
- Status: Not appointed (unless known)
- KPR Status: Pending submission
- Prequal Register Status: Not Started
- Key requirements (from ER/SoW/SOW)
- Action checklist

### 5. Create email draft → `_MANAGER_DASHBOARD/`

Short email to Project Team asking them to source candidates. Include scope summary and SOW path.

### 6. Copy reference files → `03_Specifications_and_Standards/`

Standard set: ER Document R02, Division 00, Division 01, Applicable Codes (from 10_Oddy_Testing_Lab).

For related disciplines, copy additional specs from the relevant existing sub (e.g., FLS specs for Fire-Proofing).

### 7. Verify generated docx

Table width should be 16.0cm. Check with:
```python
from docx import Document; from docx.oxml.ns import qn
t = Document(path).tables[0]
cm = int(t._tbl.find(qn('w:tblPr')).find(qn('w:tblW')).get(qn('w:w')))/567
assert abs(cm - 16.0) < 0.1
```

## Numbering conventions

| Pattern | Example | Notes |
|---------|---------|-------|
| `NN_TradeName` | `10_Oddy_Testing_Lab` | Main sequence |
| `NNa_TradeName` | `14a_MEP_Contractor` | Inserted between existing numbers |
| `NNb_TradeName` | `10b_Purchasing_Patinated_Brass` | Material vendors (not trade subs) |

## File placement rules (CRITICAL)

| File type | Location | Rationale |
|-----------|----------|-----------|
| SCOPE_REQUEST.md | `_MANAGER_DASHBOARD/` | Management copy — editable source |
| SCOPE_REQUEST.docx | Sub root | Formal deliverable for issue |
| SITUATION_REPORT.md | `_MANAGER_DASHBOARD/` | Status tracking for PM |
| Email drafts | `_MANAGER_DASHBOARD/` | Team communication |
| Research notes / contract status | `_MANAGER_DASHBOARD/` | Any .md management file |
| Technical PDFs, xlsx, dwg | `01_` through `07_` subdirs | Per discipline |
