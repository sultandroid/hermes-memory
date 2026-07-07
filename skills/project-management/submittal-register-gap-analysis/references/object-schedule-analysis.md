# Object Schedule Analysis — Museum Exhibition Projects

## Trigger
CG/Ministry sends an updated object schedule (Excel) with objects mapped to showcases. User needs to:
- Extract the object-to-showcase mapping
- Compare against previous schedule
- Identify gaps (objects without showcase assignments)
- Build a formal deliverable for NRS, GBH, and structural engineer

## Workflow

### Phase 1: Extract Object-to-Showcase Mapping

The CG schedule is a multi-sheet Excel. Each sheet = one gallery. Headers vary by sheet.

**Find header columns:**
```python
for r in range(1, min(ws.max_row+1, 10)):
    for c in range(1, ws.max_column+1):
        v = ws.cell(r, c).value
        if v:
            vs = str(v).strip()
            if 'Object ID' in vs: obj_id_col = c
            if 'Exhibit ID' in vs: exhibit_id_col = c
            if 'Object/artwork name' in vs: obj_name_col = c
            if 'Showcase needed' in vs: showcase_needed_col = c
            if 'Showcase ID' in vs: showcase_id_col = c
            if 'Object Status' in vs: status_col = c
```

**Extract only rows with showcase assignments:**
```python
for r in range(header_row+1, ws.max_row+1):
    sc_id = ws.cell(r, showcase_id_col).value
    sc_needed = ws.cell(r, showcase_needed_col).value
    if sc_id or (sc_needed and str(sc_needed).strip() == 'Yes'):
        # This object has a showcase assignment
```

### Phase 2: Compare Old vs New Schedule

**Extract object IDs from old PDF schedule:**
```python
import subprocess, re
result = subprocess.run(['pdftotext', '-layout', old_pdf, '-'], capture_output=True, text=True, timeout=60)
old_objects = set(re.findall(r'\bOB\d+(?:_\d+)?\b', result.stdout))
```

**Extract from new Excel:**
```python
new_objects = set()
for name in wb.sheetnames:
    ws = wb[name]
    # find Object ID column
    for r in range(1, min(ws.max_row+1, 10)):
        for c in range(1, ws.max_column+1):
            if ws.cell(r, c).value and 'Object ID' in str(ws.cell(r, c).value):
                obj_id_col = c
    for r in range(header_row+1, ws.max_row+1):
        oid = ws.cell(r, obj_id_col).value
        if oid and str(oid).strip():
            new_objects.add(str(oid).strip())
```

**Key comparisons:**
- Objects in old but NOT in new → removed from collection
- Objects in new but NOT assigned to any showcase → gap (flag to CG)
- Objects per showcase count change → design impact (e.g., 12.06_SC_01: 3→20 objects)

### Phase 3: Build Formal Mapping Deliverable

Create a 3-sheet Excel:

**Sheet 1 — Object to Showcase Mapping**
- One row per object with showcase assignment
- Columns: Gallery, Showcase ID, Object ID, Exhibit ID, Object Name, Status, Notes
- Gallery section dividers (light blue fill)
- Color-coded status: green=Available, amber=TBC/Needs Sourcing
- Red/orange highlights on CG study request notes
- Frozen panes, auto-filter, landscape print layout

**Sheet 2 — Summary**
- Gallery-level totals (showcases, objects)
- Notes on key changes

**Sheet 3 — CG Study Requests**
- Two action items with full descriptions
- "Action Required from NRS/GBH/Structural" column

### Phase 4: Identify Gaps

**Objects without showcase assignment:**
```python
ob_without_sc = [o for o in new_without_showcase if re.match(r'^OB\d', o)]
```
These are objects listed in the schedule but not mapped to any showcase. Common in galleries where CG hasn't provided the mapping yet.

**Non-OB entries without showcase:**
- `CANCELED` — row marker
- `OBJECT CUT 1-6` — objects removed from collection
- Gallery names, AC entries (art commissions) — not objects

### Phase 5: Communicate Findings

**To CG:** Ask when remaining showcase assignments will be provided for galleries without mapping.

**To NRS/GBH/Structural:** Forward the mapping file + object schedule. Highlight:
- Which showcases changed (object count increases/decreases)
- The 2 study requests (cancel showcase, convert to open platform)
- Any dimensional concerns (e.g., Lobby 3 showcases too small for objects)

## Pitfalls

- **Old PDF vs new Excel:** The old schedule is a PDF (pdftotext), the new is an Excel (openpyxl). Object IDs may differ in format (OB225 vs OB225-1, OB227 vs OB227_1-17).
- **Non-OB entries:** The Excel contains gallery names, "CANCELED", "OBJECT CUT" entries, and art commission codes (AC_01) that are not objects. Filter these out.
- **Showcase ID column may be empty for most galleries:** Only G8, G11, G12 had assignments in the Aseer case. Other galleries had objects listed but no Showcase ID.
- **Object Status column:** "To be confirmed" vs "Available" vs "Needs to be sourced and acquired" — these determine whether the object is ready for showcase design or still pending.
- **Large Excel files:** The Aseer object schedule was 180MB with 17 sheets. Use data_only=True and iterate efficiently.
