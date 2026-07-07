# Design Instruction Extraction from Concept PDFs

## Use Case
Extract all design instructions, objectives, space programs, and technical notes from an architectural concept design PDF. Organize by page/sheet for traceability.

## Workflow

### Step 1: Metadata Check
```bash
pdfinfo "/path/to/document.pdf"
```
- Extract: page count, creator (InDesign/Revit/AutoCAD), creation date
- Confirm document identity before diving into full extraction

### Step 2: Text Extraction (pdftotext for Arabic/English bilingual)

```bash
pdftotext -layout -enc UTF-8 "/path/to/document.pdf" -
```

For bilingual (Arabic+English) architectural PDFs:
- `-layout` preserves columnar layout crucial for side-by-side text
- `-enc UTF-8` handles Arabic characters
- Outputs all text to stdout — pipe to file for analysis

If pdftotext fails or returns garbled text, fall back to PyMuPDF:
```python
import fitz
doc = fitz.open("/path/to/document.pdf")
for page in doc:
    print(page.get_text())
```

### Step 3: Parse by Page/Section

The extraction output uses `\f` (form feed) as page separator. Pages follow the sheet naming from the document:

| Sheet Prefix | Meaning |
|-------------|---------|
| SP-01 | Site Plan |
| MS-01 | Massing Study |
| CS-01 | Concept Sketches |
| CD-01 | Concept Diagrams |
| SO-01 | Selected Option |
| SE-01 | Sections & Elevations |
| STR-01 | Structural Considerations |
| LS-01 | Landscape / Shading |
| NE-01 | Naturalistic Engineering |
| RND-01 | Render |

### Step 4: Organize Content Categories

Extract and group into these categories:

1. **Design Objectives** — bullet list of project aims
2. **Space Program** — zones, areas (m²/mq), functions, operational notes
3. **Design Characteristics** — architectural principles (e.g., "reference to traditional X architecture")
4. **Circulation Strategy** — entry + path + exit logic
5. **Structural Instructions** — load assumptions, materials, dimensions, constraints (NOT recommended vs. approved solutions)
6. **Landscape / Site** — dune engineering, paving, shading
7. **Renders** — subjects and viewpoints

### Step 5: Note Anomalies

During extraction, flag discrepancies:
- Area values that differ between pages (e.g., lounge shows 60 m² in one place and 20.3 m² elsewhere)
- Terms needing clarification (e.g., "armed ground" = reinforced/compacted ground, not armor)
- Missing items flagged by earlier audits (accessible WCs, 2nd egress, fire strategy)

### Step 6: Save as Structured Markdown

Save the organized output to the project's design folder:
```bash
`03_Design/00_Concept Design/CONCEPT_INSTRUCTIONS_LIST.md`
```

Structure:
```markdown
# Project Name — Document Title
## All Instructions & Design Notes Extracted

> Source: `filename.pdf`
> N pages | Created by | Reviewed by

---

## A. COVER
...

## B. CONCEPT STUDIES
| Sheet | Subject |
...

## C. DESIGN OBJECTIVES (N items)
1. ...
```

### Verification Checklist
- [ ] All sheet numbers/pages accounted for (compare against document control log)
- [ ] Every "not recommended" constraint captured (structural, material)
- [ ] All area values, dimensions, and loads captured
- [ ] Render subjects identified and matched to page numbers
- [ ] Discrepancies between concept doc and other project docs flagged
- [ ] Saved to `03_Design/00_Concept Design/` (or relevant design phase folder)
