# PEP Stage-Gate Build Workflow (Proven 2026-05-29)

## Overview

Successful multi-agent pipeline for building a **20-page bilingual (Arabic/English, RTL) A4 print-ready Project Execution Plan (PEP)** with Stage-Gate methodology (Stages 3–7, Gates 3–7) for a Saudi construction project (Al Faw Visitor Center, Maqtana for Projects).

This workflow applies to any **construction PEP / PMP document** requiring:
- Stage-Gate execution framework
- Design compliance matrix (objectives → VE → stages → gates)
- Risk register (23+ risks with heat map)
- 7+ work packages with budget allocation
- Bilingual Arabic/English print-ready HTML

## Prerequisites

- **Concept design PDF** (source document, 28+ pages)
- **Architectural audit** (to identify gaps)
- **VE workshop report** (10+ proposals with cost data)
- **Existing PEP** (for CSS/format reference)
- **Reference images** (renders, diagrams for visual sections)
- **Climate/location research** (for MEP/HVAC sections)

## The Chain (Proven Order)

```
User Order → Codex Rewrites (fixes 15-20 issues) → Research Phase → Claude Code Executes → Codex Audits → Fix → Deliver
```

### Step 1: Project Discovery
Before ANY work: explore the project root folder → read PROJECT_MEMORY.md → identify:
- Company name (contractor)
- Client name
- Design consultant
- Current phase
- Budget, area, duration

### Step 2: Source Document Extraction
Extract ALL text and instructions from the concept PDF:
```bash
pdftotext "path/to/concept.pdf" -
```
Save as `CONCEPT_INSTRUCTIONS_LIST.md` with:
- 12+ design objectives (explicit list)
- Space program (areas per zone)
- 5+ design characteristics
- Cirulation strategy
- Structural notes (loads, materials, constraints)
- Material specifications
- All numeric parameters

### Step 3: Image Extraction
Extract renders and diagrams from the concept PDF:
```python
import fitz
doc = fitz.open("concept.pdf")
for page_num in range(doc.page_count):
    page = doc[page_num]
    images = page.get_images(full=True)
    # Extract with descriptive names
```
Organize into:
- `RENDER_*.jpg` — Architectural renders (for cover + sections)
- `DIAGRAM_*.jpg` — Concept diagrams (for technical sections)
- `full_pages/page_*.png` — Full page references

### Step 4: Write the ORDER
Comprehensive markdown document with ALL content for the PEP:
- Every section's content requirements
- 7 packages mapped to stages
- Gate criteria (checklist items)
- Risk descriptions
- Budget allocations
- Reference images to include
- CSS/format requirements

### Step 5: Codex Rewrites (QC Gate 1)
Send the raw ORDER to **Codex CLI** for review and restructuring:
```bash
codex exec "Read ORDER_PEP_REV06.md and rewrite it fixing all technical gaps, contradictions, and missing items. Cross-reference against the existing PEP, audit, BOQ, and VE data." --sandbox workspace-write
```
Codex typically finds **15-20 issues** including:
- Missing HIA (Heritage Impact Assessment) requirements
- Wrong wind load values (1.5→1.8 kN/m²)
- Missing AACE cost classification levels (esp. Class 1)
- Budget percentages that don't total 100%
- Wrong stage assignments for packages
- Missing geotechnical, commissioning, accessibility items
- VE prerequisites not listed

### Step 6: Research Phase (if needed)
Fast research → **Kimi** (Pattern A — simple lookups, climate data)
Parallel research → **delegate_task** with toolsets=["web"] (Pattern B)
Deep synthesis → **Claude Code** with WebSearch (Pattern C)

### Step 7: Claude Code Executes (Build HTML)
Provide Claude Code with:
1. The rewritten ORDER (full content)
2. Reference PEP rev05 for CSS format
3. Image paths (relative to HTML location)
4. Climate research data

```python
delegate_task(
    goal="Build a 20-page bilingual A4 print-ready PEP HTML...",
    context="ORDER content + CSS reference + image paths + research data...",
    toolsets=["terminal", "file", "search"]
)
```

**CRITICAL:** Do NOT re-read the HTML file with `read_file()` after Claude Code creates it, unless you pass `limit=N` where N > file's total lines. Default 500-line limit WILL truncate.

### Step 8: Fix Image Paths
Images referenced with `../../` paths won't serve via http.server (it can't serve parent directories). Fix:
1. Create `assets/images/` in the HTML's serving directory
2. Copy + resize images there
3. Change HTML to use `assets/images/` relative paths

### Step 9: Codex Audits (QC Gate 2)
Send the built HTML to **Codex CLI** for comprehensive audit:
```bash
codex exec "QC audit of PEP_PROJECT_EXECUTION_PLAN.rev06.html against the ORDER requirements. Check: 20 pages? 12 objectives? all 10 VE proposals with correct SAR? 23 risks? Gates 3-7? Packages budget 100%? AACE ladder? Lounge discrepancy flagged? HIA? Wind load correction? CSS formatting? Image paths? Arabic/English bilingual? Risk matrix CSS classes exist?" --sandbox workspace-write
```
Codex produces a structured QA report with PASS/FAIL per item and severity.

Typical issues Codex finds:
- **CRITICAL:** Risk heat map CSS classes missing from HTML
- **MAJOR:** Missing required image
- **MINOR:** Budget rounding, percentage labels

### Step 10: Fix Issues
Apply all critical and major fixes before delivery:
- Add missing CSS classes to the `<style>` block
- Add missing image references
- Fix rounding/percentage labels

### Step 11: Overflow Test (PEP Driver)
Run the Playwright-based PEP driver to verify A4 overflow:
```bash
cd /project/root
python3 .claude/skills/run-al-faw-pep/driver.py --doc pep --pdf
```
All pages must be within A4 bounds (1123px @ 96dpi).

### Step 12: Update PROJECT_MEMORY
Update the project memory file:
- Mark PEP rev as current
- Add to Document Control Log
- Update phase description

### Step 13: Deliver
Provide a structured delivery summary with:
- File paths and sizes
- Page count and structure
- Pipeline steps executed
- Key improvements over previous revision

## File Structure Convention

```
08_Schedules/00_Master Program/
├── ORDER_PEP_REV06.md          ← Rewritten order (Codex)
├── PEP_PROJECT_EXECUTION_PLAN.rev06.html  ← Final deliverable
├── PEP_PROJECT_EXECUTION_PLAN.html        ← Copy as current
├── PEP_PROJECT_EXECUTION_PLAN.pdf         ← PDF export
├── PEP_REV06_CHANGELOG.md                 ← Change log
└── assets/images/                         ← Resized reference images
    ├── RENDER_Aerial_View.jpg
    ├── RENDER_South_Elevation_Overlooking_Al_Faw.jpg
    ├── DIAGRAM_*.jpg
    └── page_*.png
```

## Pitfalls

| # | Pitfall | Mitigation |
|---|---------|------------|
| 1 | **read_file 500-line truncation** | Always pass `limit=10000` or use `terminal(cat path)` |
| 2 | **Image 404 via http.server** | Parent-directory paths fail; use local `assets/images/` |
| 3 | **Risk matrix CSS not included** | Claude Code may copy HTML structure without corresponding CSS rules |
| 4 | **Old PEP left as current** | Remember to copy rev06 → PEP_PROJECT_EXECUTION_PLAN.html |
| 5 | **Incomplete rev (like rev05)** | Verify pages count matches target (grep -c 'class="sheet') |
| 6 | **Budget % not totaling 100%** | Cross-check against actual BOQ totals, not rough estimates |
| 7 | **VE SAR values wrong** | Cross-check every CapEx and NPV against VE_DATA_EXTRACTION.md |
| 8 | **Lounge area discrepancy unresolved** | Flag both values (60 vs 20.3 m²) — do not choose unilaterally |
