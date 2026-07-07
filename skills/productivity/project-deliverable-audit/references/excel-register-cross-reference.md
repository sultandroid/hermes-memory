# Excel Register Cross-Reference Technique

Verify document references in a plan/HTML against an Excel Register Log.

## When to Use

A plan cites document numbers (e.g. `MOC-ASEER-GN-DS-006`, `MOC-ASEER-SIC-1K0-PL-0010`). You need to confirm they match the actual approved document numbers on the project's CDE/Register Log.

## Workflow

### 1. Find the right sheet in the Register Log

Register Logs (`.xlsx`) often have separate tabs for different submission types. List all sheets:

```python
import openpyxl
wb = openpyxl.load_workbook('Register Log.xlsx', data_only=True)
for s in wb.sheetnames:
    print(s)
```

Look for: `Document Submittals`, `Material Submittal`, `Starting New Activity`, `Inspection Request (IR)`, `Shop Drawings`.

Plan/procedure document numbers are typically in **Document Submittals** tab.

### 2. Read rows from the target sheet

```python
ws = wb[' Document Submittals']  # note leading space in tab name
for row in ws.iter_rows(min_row=1, max_row=80, max_col=6, values_only=False):
    vals = [str(c.value) if c.value is not None else '' for c in row]
    line = '\t'.join(vals)
    if any(v.strip() for v in vals):
        print(line)
```

Key columns: Sl. No. | Document Number | Discipline | Description (Arabic) | TYPE | Description (English)

### 3. Extract all document numbers for cross-reference

```python
import re
content = ...  # from step 2
mocs = set(re.findall(r'MOC-[A-Za-z0-9-]+', content))
for m in sorted(mocs):
    print(m)
```

### 4. Compare against plan references

Extract all `MOC-...` references from the HTML plan:
```bash
grep -o 'MOC-[A-Z0-9-]*' plan.html | sort -u
```

Cross-reference each plan reference against the Register Log. Flag mismatches.

## Common Pitfalls

- **Tab names with leading/trailing spaces**: The Excel tab may be `' Document Submittals'` not `'Document Submittals'`. Include the space in the sheet name.
- **Excel warnings about headers/footers**: `openpyxl` may print `UserWarning: Cannot parse header or footer` — harmless, suppress with `2>/dev/null`.
- **Mixed naming conventions**: Older entries may use `MOC-Asser-SIC-...` (lowercase 'Asser') while newer entries use `MOC-MUS-ASE-...`. Both are valid — the convention shifted mid-project.
- **Plan references vs register references may differ**: A plan may reference a document by a different number than the Register Log if the log uses a different series. Check with the Document Controller.
- **Permissions on server-deployed files**: After scp/ssh upload, files are `-rw-------` (600). Web server returns 403. Fix with `chmod -R 755` on the remote directory.
