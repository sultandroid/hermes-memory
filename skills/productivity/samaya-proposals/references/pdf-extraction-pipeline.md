# PDF Text Extraction Pipeline

Used for RCRC Exhibition project document analysis (June 2026).

## Goal
Extract text from all project PDFs (BoQ, drawings, specifications, design reports) for downstream analysis.

## Tools
- **PyMuPDF (fitz)** — installed in Samaya environment, best single-library solution
- **pdftotext** (poppler) — also available via Homebrew

## Workflow

### 1. Find all PDFs
```python
import glob, os
pdfs = glob.glob(os.path.join(folder, "**/*.pdf"), recursive=True)
```

### 2. Extract text
```python
import fitz
doc = fitz.open(pdf_path)
text = "".join(page.get_text() for page in doc)
doc.close()
```

### 3. Save as markdown sidecar
Save to `/tmp/pdf_studies/extracted_<slug>.md` for analysis.

### 4. Read key sections
First 50-100 lines reveal: project name, designer, location, budget, key specs, scope areas.

## Expected output
For a typical exhibition project (8 PDFs, mixed sizes):
- Total extracted: 300K-500K chars
- Largest: Scenographic Design (140 pgs), Interior Design (103 pgs)

## Pitfalls
- **Image-based PDFs:** Scanned plans/renders yield no extractable text — use OCR (Tesseract) as fallback
- **BoQ tables:** Column alignment lost — parse line-by-line, look for `$`/`SAR` as value anchors
- **Arabic encoding:** Bilingual PDFs may produce garbled Arabic — check first few pages
- **Large PDFs:** 100+ MB takes 10-30s — use timeout in shell calls
- **Kimi CLI alternative:** Can summarize PDFs but mixes conversation protocol in output. PyMuPDF + manual read is more reliable for structured data.
