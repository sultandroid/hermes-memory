# Design Study Workflow — PDF Extraction → Summaries → Proposal Update

Pattern used for RCRC Exhibition tender: extracting text from design PDFs, creating organized summaries, then updating the technical proposal.

## Step 1: Extract All Design/Tender PDFs

Use PyMuPDF (fitz) for reliable text extraction from project PDFs:

```python
import fitz
doc = fitz.open("path/to/file.pdf")
text = []
for page in doc:
    text.append(f"--- PAGE {page.number + 1} ---\n{page.get_text()}")
doc.close()
```

⚠ Save `len(doc)` to a variable BEFORE closing — `len(doc)` after `close()` raises "document closed" error.

Extract Excel data with openpyxl for material/furniture/BoQ schedules.

## Step 2: Create Organized MD Summaries

Two approaches:

### A. Small files (<20KB) — Direct summarization
Read the extracted text, identify key data (materials, finishes, furniture items, room names), and write structured MD with headings, tables, bullet lists.

### B. Large files (>50KB) — Kimi summarization
Pipe the extracted text to Kimi with a concise prompt:

```bash
kimi -p "Read this document text and create an organized markdown summary. Include: 1) Document info, 2) Section breakdown, 3) Key specs. Output ONLY the markdown." --print --max-steps-per-turn 10
```

⚠ Kimi may time out on files >100KB. For those, read key sections manually (sheet index, first pages, grep for keywords) and build summary directly.

## Step 3: Master Index (README.md)

Create a `README.md` in the studies folder with:
- Gallery/area map (tables)
- Cross-reference to original source files
- Links to each summary

## Step 4: Feed Findings Into Proposal

Map design study findings to proposal sections:

| Finding | Proposal Section |
|---------|-----------------|
| Gallery themes & AV | Scope of Work → Gallery Breakdown |
| Supporting area finishes | Scope → Supporting Areas |
| Key materials | Technical Methodology |
| Designer credit | Project Understanding |

## Step 5: Update Odoo

After generating the design studies, append the summary location to the relevant Odoo task's description and log a timesheet.
