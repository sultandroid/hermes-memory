# DOCX Claim Verification / QC Audit

When the user provides a set of claims about what a document contains (a "Summary" or cross-reference), verify them systematically against the actual source document.

## Workflow

### Step 1: Locate the correct source

The path the user gives may point to the wrong file (e.g., a submittal form instead of the plan document itself, or a different revision). Do not assume the path is correct.

- Search the surrounding directory tree for files matching expected names/types
- Aseer-style pattern: DMP/BEP/PEP docs live under `04_Docs/02_Plans_and_Procedures/02.1_DMP/01_Source_Files/03_Word/` or `Word/` subdirectories
- Rev ID is embedded in the filename: `*Rev03_C03*`, `*C02*`, etc.

```bash
# When the given PDF turns out to be a submittal form, search the DMP folder
search_files(target="files", pattern="*DMP*", path="/path/to/Plans_and_Procedures")
# Look for .docx files under Source_Files/Word/ or 03_Word/
```

### Step 2: Extract content

Primary extraction path for DOCX:

```python
from docx import Document
doc = Document("/path/to/document.docx")

# Method A: Read all paragraphs sequentially
for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    if text:
        print(f"[P{i}] [{para.style.name}] {text}")

# Method B: Search all tables
for ti, table in enumerate(doc.tables):
    for ri, row in enumerate(table.rows):
        cells = [cell.text.strip() for cell in row.cells]
        print(f"TABLE {ti}, ROW {ri}: {' | '.join(cells)}")
```

Or use `read_file` which auto-extracts DOCX natively (faster, zero setup). This is ideal for a first pass:

```python
# read_file(path, offset=1, limit=500) works directly on .docx files
# Tables and paragraphs are extracted to readable text automatically
```

But `read_file` truncates at ~4100 lines / ~100K chars. For deep searches, use python-docx directly.

### Step 3: Search for specific claim patterns

When verifying claims, search the document for exact naming patterns mentioned in the claims:

```python
# Search paragraphs and tables for specific identifiers
found_g0_g8 = False
for para in doc.paragraphs:
    t = para.text.strip()
    if "G0" in t or "G8" in t:
        found_g0_g8 = True
        print(f"Match: {t[:200]}")

# Search tables for INT-01, ICE, etc.
import re
for table in doc.tables:
    for row in table.rows:
        row_text = " | ".join(cell.text.strip() for cell in row.cells)
        if re.search(r'INT-\d{2}|ICE|coordination wheel|turnaround', row_text, re.I):
            print(f"TABLE MATCH: {row_text[:200]}")
```

### Step 4: Identify the actual section structure

DMP/BEP style documents may have:
- A Table of Contents on the first few pages (often in tables, not paragraphs)
- Sections numbered 4, 5, 6, 7 in the heading style
- Sub-sections (6.1, 6.2, 7.1, 7.2) developed under each heading
- Appendices (Appx M, Appx X) that contain the detailed content

Extract the TOC first to map the claimed section number to the actual heading:

```python
# Find section headings
for para in doc.paragraphs:
    t = para.text.strip()
    if para.style.name.startswith("Heading"):
        print(f"[{t[:80]}]")

# Or search for section markers
for para in doc.paragraphs:
    t = para.text.strip()
    if t.startswith(("4.", "5.", "6.", "7.")):
        print(f"SECTION HEADER: {t[:150]}")
```

### Step 5: Build the discrepancy report

Structure each discrepancy as a 3-part finding:

| Component | What to fill |
|-----------|-------------|
| **Claim** | What the Summary says the section contains |
| **Actual** | What the document actually contains (heading, scope, key content description) |
| **Discrepancy** | Nature of mismatch: wrong section attribution, wrong naming convention, content absent entirely |

For each claim, determine:
1. **Does the section number match the claimed topic?** (section attribution error)
2. **Does the naming convention match?** (G0-G8 vs DG-0→DG-7, INT-01 vs A2742-AV-Interface-Register)
3. **Does the content exist anywhere in the document?** (totally absent vs. present elsewhere)

Report structure:

```
## Finding #N — §X: Summary claims "..." [VERDICT: CORRECT / PARTIAL / WRONG / ABSENT]

| Aspect | Summary Claim | Actual DMP Content |
|---|---|---|
| §N topic | ... | ... |
| [Key detail] | ... | ... |

**Discrepancy:** ...
```

---

## Common pitfalls in document claim verification

1. **Given path is wrong** — The path in the request may point to a submittal cover letter, a different revision, or a different document altogether. Always verify: check page count, check document title/header, search for the actual revision code in the first few lines.

2. **TOC vs Body alignment** — The Table of Contents may list a section heading that doesn't match the body content, or the section may be a placeholder with no body text. Always check both.

3. **Naming convention mismatch** — Claims often use a different naming scheme from what the document actually uses. Search for the claimed pattern (e.g., `INT-01`) even outside the claimed section.

4. **Tables are content-heavy** — In structured documents like DMPs, most critical content lives in tables (RACI matrices, stakeholder registers, vendor lists, code tables), not in paragraphs. Python-docx table iteration is essential.

5. **Headings in Body Text style** — Many documents use Body Text style for headings instead of Heading 1/2/3. Don't rely solely on `para.style.name.startswith("Heading")` — also check for patterns like `^\d+\.\s` or `SECTION \d+`.
