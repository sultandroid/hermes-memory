# DOCX Editing Techniques — Existing Files (not from scratch)

**When to use:** You need to modify an existing `.docx` file — remove/add table rows, update paragraph text, change cells, save as a new revision (R00→R01). The SamayaDoc class is for *generation*; this reference is for *editing existing documents*.

## Runtime: terminal heredoc, NOT execute_code sandbox

python-docx is installed system-wide (`pip3 install python-docx`) but NOT in the Hermes `execute_code` sandbox. Always use:

```python
python3 << 'PYEOF'
from docx import Document
# ... your code ...
PYEOF
```

Run this directly in `terminal()`, not in `execute_code()`.

## Read the DOCX structure first

Always inspect before editing — tables and paragraphs interleave in the document body:

```python
doc = Document(path)

# Find your tables
for ti, table in enumerate(doc.tables):
    print(f"Table {ti}: {len(table.rows)} rows x {len(table.columns)} cols")
    for ri, row in enumerate(table.rows):
        cells = [cell.text.strip()[:50] for cell in row.cells]
        print(f"  R{ri}: {cells}")

# Find your paragraphs
for i, para in enumerate(doc.paragraphs):
    txt = para.text.strip()
    if txt:
        print(f"P{i}: [{para.style.name}] {txt[:80]}")
```

Paragraphs inside tables appear in `doc.paragraphs` too! Use the table index to distinguish.

## Removing table rows

**CRITICAL rule: remove from highest index first** to avoid index shifting:

```python
tbl = doc.tables[table_index]
# Remove rows 1 and 2 — remove row 2 (higher index) first
tbl._tbl.remove(tbl.rows[2]._tr)
tbl._tbl.remove(tbl.rows[1]._tr)
```

If you remove row 1 then row 2, the old row 2 becomes row 1 after the first removal, and you delete the wrong row.

## Updating paragraph text

```python
doc.paragraphs[129].text = "Your new text here"
```

This replaces ALL runs in the paragraph. For styled text (mixed bold/normal), recreate the runs or use the SamayaDoc approach instead.

## Updating table cell text

```python
row = doc.tables[2].rows[2]
row.cells[1].text = "New cell value"
```

Cell text fully replaces the cell content.

## Saving as a new revision

```python
outpath = original_path.replace("_R00_", "_R01_")
doc.save(outpath)
```

Pattern: always save as R01 (or next rev), never overwrite the original R00. The subfolder convention in the SOW path keeps both available.

## Adding rows to tables (post-creation)

Use `add_row()` to append after the last row:

```python
row = doc.tables[table_index].add_row()
row.cells[0].text = "New Code"
row.cells[1].text = "New Description"
row.cells[2].text = "New Value"
```

### Guard: check before adding

Always check if the row content already exists to avoid duplicates:

```python
t = doc.tables[table_index]
exists = any("New Code" in cell.text for row in t.rows for cell in row.cells)
if not exists:
    row = t.add_row()
    row.cells[0].text = "New Code"
```

## Find-and-replace across all paragraphs (preserving formatting)

**Set `.text` on paragraphs replaces ALL formatting** (bold, italic, font changes). To preserve runs, iterate `p.runs`:

```python
replacements = {
    "Rev C02": "Rev C03",
    "DRAFT": "CG REVIEW",
    "Internal Review": "Issued for CG Review",
}

for p in doc.paragraphs:
    for run in p.runs:
        for old, new in replacements.items():
            if old in run.text:
                run.text = run.text.replace(old, new)
```

This preserves per-run formatting (bold in the title, italic in notes, etc.).

### ⚠️ Run-level text concatenation pitfall

**Problem:** When you replace text in a paragraph where the *old* string is split across multiple runs, a simple `run.text.replace(old, new)` won't work — the old text is fragmented. Worse, if you use `replace_text_in_paragraph()` (which finds the start run and splices), the *new* text may land in the middle of a run, and a subsequent run still carries the old suffix, producing concatenated artifacts like:

```
"- CITC/STC submissions coordinated through BMS/ICT Specialist then SamayaCITC/STC submissions: coordinated through Samaya"
```

This happens because:
1. Run A gets the new text spliced in (ending with "Samaya")
2. Run B still contains the old suffix ("CITC/STC submissions: coordinated through Samaya")
3. The paragraph renders as Run A + Run B = concatenated mess

**Fix pattern — clear all runs and set text on the first run only:**

```python
# Find the problematic paragraph
idx, para = find_paragraph_containing(doc, "SamayaCITC/STC")
if para:
    # Save formatting from the first run
    first_run = para.runs[0]
    fmt_bold = first_run.bold
    fmt_italic = first_run.italic
    fmt_underline = first_run.underline
    fmt_name = first_run.font.name
    fmt_size = first_run.font.size
    fmt_color = first_run.font.color.rgb if first_run.font.color and first_run.font.color.rgb else None
    
    # Clear ALL runs
    for run in para.runs:
        run.text = ""
    
    # Set the correct text on the first run only
    first_run.text = "- CITC/STC submissions coordinated through BMS/ICT Specialist then Samaya"
    
    # Restore formatting
    first_run.bold = fmt_bold
    first_run.italic = fmt_italic
    first_run.underline = fmt_underline
    if fmt_name:
        first_run.font.name = fmt_name
    if fmt_size:
        first_run.font.size = fmt_size
    if fmt_color:
        first_run.font.color.rgb = fmt_color
```

**Prevention:** When replacing text that spans multiple runs (common in DOCX files where bold/italic formatting splits a sentence), always check the paragraph's `runs` list after replacement. If the paragraph text contains concatenated fragments (e.g., "SamayaCITC/STC"), use the clear-all-runs pattern above.

**Detection:** After any find-and-replace pass, scan for concatenation artifacts:
```python
for p in doc.paragraphs:
    # Check for doubled text where old suffix survived
    if "SamayaCITC" in p.text or "then SamayaCITC" in p.text:
        print(f"CONCATENATION in paragraph: {p.text[:100]}")
```

### Apply same replacements to table cells

Paragraphs inside tables are ALSO in `doc.paragraphs`, so the above loop catches them. For explicit table-cell replacement:

```python
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            for run in cell.paragraphs[0].runs:
                for old, new in replacements.items():
                    if old in run.text:
                        run.text = run.text.replace(old, new)
```

## Full revision-bump pattern

When bumping a document from one revision to the next:

```python
import copy
from docx import Document

doc = Document(src)

# 1. Replace revision metadata across all paragraphs + tables
REPLACE = {
    "Rev C02": "Rev C03",
    "REV C02": "REV C03",
    "2026-06-12": "2026-06-16",
    "Issued for Internal Review": "Issue for CG Review",
    "DRAFT · INTERNAL REVIEW": "ISSUED FOR CG REVIEW",
    "DRAFT": "CG REVIEW",
    "REVISION C02 · Updated": "REVISION C03 · Updated",
}

for p in doc.paragraphs:
    for run in p.runs:
        for old, new in REPLACE.items():
            if old in run.text:
                run.text = run.text.replace(old, new)

# 2. Add/update content — new table rows, new paragraphs
# (add references, new sections, synced content from other docs)

# 3. Save as new revision
doc.save(dst)

# 4. Verify key changes
doc2 = Document(dst)
print(doc2.paragraphs[0].text[:80])  # Title
# Check first table, check last table, etc.
```

## Renaming the revision folder

After editing, the folder name needs to match the new revision:

```python
import shutil
src_folder = "/path/to/Project_Plan_RevC02/"
dst_folder = "/path/to/Project_Plan_RevC03_CG_REVIEW/"
shutil.move(src_folder, dst_folder)
# Then create a fresh symlink or index pointing to the new folder
```

Also update any `index.html` redirects or `latest` pointers within the HTML source.

## Full edit workflow example

1. Open doc, inspect tables + paragraphs to locate targets
2. Build replacement dict for revision metadata (Rev ID, date, status)
3. Apply replacements across paragraph runs (preserves formatting)
4. Check each paragraph style — some footers/headers repeat per-section
5. Modify tables (remove rows highest-index-first, add rows, update cells)
6. Check for existing content before adding (guard clauses on table rows)
7. Update cross-reference sections (companion docs, authority basis, sign-off table)
8. Save as new rev in same folder
9. Rename parent folder from RevC02 to RevC03
10. Verify: re-open saved file, re-print key paragraphs and tables
