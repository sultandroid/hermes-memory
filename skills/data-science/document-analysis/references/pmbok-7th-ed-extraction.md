# PMBOK Guide 7th Edition — PDF Extraction Reference

**Source:** PMBOK Guide 7th Edition (2021), 20MB, ~370 pages
**Tool used:** `pdftotext` (poppler) via terminal
**OneDrive path:** OneDrive-locked, hydrated via `open` (Preview) before extraction

## Extraction Strategy for Large Structured PDFs

When a PDF is too large to extract in one pass (20MB, 370+ pages), use **targeted page-range extraction** to get specific sections without overwhelming the context window.

### 1. Get the Table of Contents first

```bash
# Extract first ~20 pages to get the TOC
pdftotext -f 1 -l 20 "/path/to/book.pdf" /tmp/toc.txt
```

This gives you the chapter/section structure and page numbers. Read the TOC to identify which page ranges correspond to which sections.

### 2. Extract by section, not by whole document

```bash
# Principles section (pages 21-60 in PMBOK 7th Ed)
pdftotext -f 21 -l 60 "/path/to/book.pdf" /tmp/principles.txt

# Performance domains (pages 61-130)
pdftotext -f 61 -l 130 "/path/to/book.pdf" /tmp/domains.txt
```

### 3. Find section boundaries within extracted text

After extraction, use `grep` to locate where each subsection starts:

```bash
grep -n "3\.4\|3\.5\|3\.6\|3\.7\|3\.8\|3\.9\|3\.10\|3\.11\|3\.12" /tmp/principles.txt
```

### 4. Read targeted chunks with offset/limit

```bash
read_file(path="/tmp/principles.txt", offset=401, limit=300)
```

### 5. Handle PDF formatting artifacts

`pdftotext` output often has **scrambled letters in headers** due to PDF text-rendering artifacts (kerning, letter-spacing, or text-positioning operators). Example:

```
STEWARDSHIP → STEWARDSHIP
STAKEHOLDERS → STAKEHOLDERS
```

These are **not OCR errors** — they're artifacts of how the PDF stores character positioning. The actual text content is correct; only the display is garbled. Ignore the scrambled headers and read the body text.

### 6. Handle repeated content (form feed markers)

`pdftotext` inserts `\f` (form feed) characters at page boundaries. These appear as `\f` in the extracted text. They're harmless but can be stripped:

```bash
# Remove form feeds for cleaner output
sed 's/\f//g' /tmp/principles.txt > /tmp/principles_clean.txt
```

### 7. Handle page number / running header noise

PDFs often repeat the book title, chapter title, and page number on every page. These create noise in the extracted text. Filter them out by:
- Skipping lines that match known header patterns
- Using `grep -v` to exclude lines matching `PMBOK® Guide` or page number patterns

## PMBOK 7th Edition Page Map

| Section | Pages | Content |
|---------|-------|---------|
| Front matter / TOC | 1-20 | Title, preface, TOC, figures/tables list |
| Standard: System for Value Delivery | 2-20 | Value delivery, governance, functions, environment |
| Standard: 12 Principles | 21-60 | Principles 3.1 through 3.12 |
| Guide: 8 Performance Domains | 61-130 | Stakeholder, Team, Dev Approach, Planning, Project Work, Delivery, Measurement, Uncertainty |
| Tailoring | 131-152 | Tailoring process, diagnostics |
| Models, Methods, Artifacts | 153-196 | Reference catalog |
| Appendices + Glossary | 197-270 | Contributors, PMO, Product, Research, Glossary |

## Key Differences from 6th Edition

| Aspect | 6th Edition | 7th Edition |
|--------|-------------|-------------|
| Structure | 5 Process Groups + 10 Knowledge Areas | 12 Principles + 8 Performance Domains |
| Focus | Process-based (prescriptive) | Principles-based (guidance) |
| Delivery approach | Primarily predictive | All approaches (predictive, hybrid, adaptive) |
| Outcome focus | Deliverables | Outcomes + value |
| Tailoring | Per-knowledge-area notes | Dedicated tailoring section |
| Digital | Print-only | Links to PMIstandards+ platform |

## Construction-Specific Sections to Prioritize

For construction project management, focus extraction on:

1. **Planning Performance Domain** (Section 2.4) — WBS, estimating, scheduling, budgeting
2. **Delivery Performance Domain** (Section 2.6) — Requirements, scope definition, quality, DoD
3. **Measurement Performance Domain** (Section 2.7) — EVM, KPIs, baselines, forecasts
4. **Uncertainty Performance Domain** (Section 2.8) — Risk management, ambiguity, complexity
5. **Stakeholder Performance Domain** (Section 2.1) — Engagement, analysis, communication
6. **Tailoring Section** (Section 3) — How to adapt for construction projects
7. **Models, Methods, Artifacts** (Section 4) — WBS, RACI, risk register, contracts
