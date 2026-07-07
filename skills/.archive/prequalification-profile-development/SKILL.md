---
name: prequalification-profile-development
description: "Develop prequalification submission documents and professional capability profiles for Saudi industrial/manufacturing/construction companies. Covers: company research, PDF extraction, document creation (DOCX/MD/HTML), photo extraction, and Claude-driven design."
version: 1.0.0
author: hermes
tags:
  - prequalification
  - capability-profile
  - saudi-construction
  - factory-prequal
  - profile-design
  - pdf-extraction
related_skills:
  - claude-code
  - html-print-layout
  - document-analysis
prerequisites:
  commands: [python3, claude]
  python_packages: [PyMuPDF, python-docx, pdfplumber]
---

# Prequalification & Capability Profile Development

## When to Use

- Client needs prequalification documents for a Saudi industrial/manufacturing company
- Creating a professional corporate capability profile (HTML or DOCX)
- Need to extract company data from corporate profile PDFs
- Designing A4 printable submission documents for NHC/Royal Court/hospitality projects
- Any task requiring proper bilingual (English-led) profile output

## NOT for
- Samaya-specific tech office workflows (use `samaya-technical-office`)
- Standard subcontractor prequalification forms (use the existing generic checklist)
- Pure text documents without design requirements

## The Workflow

### Phase 1: Company Research

1. **Internet research**: Search LinkedIn, company website, Google for company info
2. **Extract CR, GOSI, factory data** from corporate profile PDF
3. **Check Google Drive** for project portfolio structure
4. **Create portfolio MD** file with all project folders and Drive IDs

### Phase 2: PDF Image Extraction

Always extract images from source PDFs before building:

```bash
python3 -c "
import fitz
doc = fitz.open('corporate_profile.pdf')
print(f'Pages: {doc.page_count}')
for i, page in enumerate(doc):
    images = page.get_images()
    for j, img in enumerate(images):
        xref = img[0]
        base = doc.extract_image(xref)
        fname = f'page{i+1}_img{j+1}.{base[\"ext\"]}'
        with open(fname, 'wb') as f:
            f.write(base['image'])
        print(f'Extracted: {fname} ({base[\"width\"]}x{base[\"height\"]})')
doc.close()
"
```

Also render pages as images for spread/layout reference:
```python
pix = page.get_pixmap(dpi=150)
pix.save(f'page{i+1}_render.jpg')
```

### Phase 3: Create Prequalification Document Package

Create 4 document types:

| Folder | Document | Purpose |
|--------|----------|---------|
| `01_Submission_Document/` | PREQUALIFICATION_SUBMISSION_DOCUMENT | Main 8-section submission |
| `02_Checklists/` | FACTORY_PREQUALIFICATION_CHECKLIST | Tailored for manufacturer (not generic subcon) |
| `03_Capability_Statement/` | COMPANY_CAPABILITY_STATEMENT | Professional company overview |
| `04_Compliance/` | COMPLIANCE_MATRIX_TEMPLATE | Project-fillable compliance matrix |

**Key differentiator**: These are MANUFACTURER-FACTORY focused, not subcontractor-focused. Include:
- Industrial License, SASO/SABER
- Production capacity & equipment list
- Factory zones (carpentry, painting, assembly, QC, packaging)
- Local Content (LCWA/ICP), Nitaqat/Saudization
- Saudi Building Code compliance
- ISO certs with certifying body

**Format**: Create `.md` for readability + `.docx` (python-docx) for professional submission.

### Phase 4: Design HTML Capability Profile (CRITICAL — use Claude)

**Always delegate HTML profile design to Claude Code.** Do not attempt to write the design HTML yourself.

```bash
cd /project/path && claude -p 'Create A4 landscape capability profile...' --max-turns 25 --dangerously-skip-permissions
```

#### Design Mandates (from user corrections)
| Mandate | Why |
|---------|-----|
| **English-led bilingual** | English heading FIRST, Arabic in smaller text below |
| **Modern fonts** | Google Fonts: Inter (headings), Plus Jakarta Sans (body) |
| **Logo from source PDF** | Extract and embed as base64 — never placeholder |
| **Real photos as base64** | Extract from corporate profile PDF — never colored blocks |
| **A4 Landscape** | `@page { size: 297mm 210mm landscape; margin: 0 }` |
| **7-page structure** | Cover, About, Manufacturing, Products, Portfolio, Quality, Why Us |
| **Print button** | `onclick="window.print()"` for one-click PDF export |
| **Self-contained** | All CSS inline/in `<style>`, all images as base64 data URIs |

#### Image Embedding Pattern

```python
import base64, fitz

def build_profile():
    # 1. Extract logo and photos from corporate PDF
    doc = fitz.open('corporate.pdf')
    # ... extract images
    
    # 2. Convert to base64 data URIs
    def uri(data, mime='image/jpeg'):
        return f'data:{mime};base64,' + base64.b64encode(data).decode()
    
    LOGO = uri(logo_data, 'image/png')
    PHOTO = uri(photo_data, 'image/jpeg')
    
    # 3. Write HTML template with __PLACEHOLDER__ tokens
    html = '''...<img src="__LOGO__">...'''
    
    # 4. Replace placeholders with data URIs
    html = html.replace('__LOGO__', LOGO)
    
    # 5. Write file
    with open('profile.html', 'w') as f:
        f.write(html)
```

### Phase 5: OCR & Document Analysis

When source PDFs have no text layer (image-based):

```bash
# Export page as image from PyMuPDF
python3 -c "
import fitz
doc = fitz.open('doc.pdf')
page = doc[0]
pix = page.get_pixmap(dpi=300)
pix.save('page.png')
doc.close()
"

# OCR with tesseract
tesseract page.png stdout -l eng+ara
```

For PDFs with real tables: use pdfplumber or pdftotext (see `document-analysis` skill).

### Phase 6: Convert to A4 Portrait Technical Proposal (the "Real Document")

When the user says "make it like a real technical proposal" — **reorient from landscape brochure to portrait document**.
See `html-print-layout` skill → `references/technical-proposal-structure.md` for the standard 16-page proposal structure, TOC design pattern, and steel spec conventions (epoxy not galvanized, generic HSS not specific profiles).

### Conversion: Landscape → Portrait

```css
/* Landscape (brochure) */
@page { size: 297mm 210mm landscape; margin: 0; }
.page { width: 297mm; min-height: 210mm; max-height: 210mm; }

/* Portrait (technical proposal) */
@page { size: 210mm 297mm; margin: 12mm 15mm; }
.page { width: 178mm; min-height: 267mm; max-height: 267mm; }
```

**What changes:**
- Font sizes drop ~1-2pt (body text 8-9pt, headings proportionally smaller)
- Margins/padding compress ~30%
- Two-column grids may become single column
- Image heights reduce ~30% (e.g., 120mm → 80mm)
- Total page count increases ~40% (landscape 7 → portrait 12+)
- `.pd` padding from 28px 36px → 18px 24px
- Table cells: 5px 8px → 3px 6px

### CRITICAL: Follow the 11-Section Checklist Structure

The user WILL CORRECT you if you write a proposal that doesn't follow the factory prequalification checklist. **Read the checklist FIRST**, then map every section of the checklist to a page in the proposal.

**Mandatory section mapping (from FACTORY_PREQUALIFICATION_CHECKLIST):**

| Section | Page Title | Checklist Items |
|---------|-----------|-----------------|
| A | Legal & Corporate Documentation | A.1 → A.11 |
| B | Certifications & Accreditations | B.1 → B.10 |
| C | Factory & Manufacturing Capability | C.1 → C.10 |
| D | Quality Control | D.1 → D.10 |
| E | Material Sourcing & Supply Chain | E.1 → E.7 |
| F | Health, Safety & Environment | F.1 → F.8 |
| G | Project Experience | G.1 → G.6 |
| H | Financial | H.1 → H.5 |
| I | Local Content & Saudization | I.1 → I.6 |
| J | Project-Specific Scope | Actual BOQ items, quantities, specs |
| K | Submission Documents Checklist | All items with ✓ status |

Each checklist item should appear as a table row with columns: `# | Document Requirement | Status | Reference / Remarks`.

### Project-Specific Scope (Section J)

This is the most important section — address the ACTUAL project scope:

```markdown
1. List every BOQ item with quantity and spec reference
2. For each item: material type, finish, dimensions, drawing reference
3. Reference the relevant spec sections (e.g., Section 061000, 064023)
4. State material compliance standards (BS EN 942, ANSI A208.2, BS 1088, ASTM E84)
```

Example from Project 010 (Wood Finishes):
- 20mm wood veneer Type IW-10 — 465 m²
- Prayer Room bookshelf (walnut IWD-51 + laminate IPL-52) — 10 No.
- Mehrab wall feature (walnut + laser-cut bronze + backlighting) — 5 No.
- Shoe rack units (4 sizes, walnut + laminate + SS mocha gold) — 5 total
- 100mm skirting SK02/SK03 — 116 LM

### Appendix Pages Structure

Appendices must include BOTH external doc references AND fillable templates:

| Appendix | Content | Type |
|----------|---------|------|
| A — Legal | CR, Industrial License, Zakat, GOSI, Chamber, Civil Defense with ref numbers/dates | 📄 External scans |
| B — Certifications | ISO 9001, SASO/SABER table, **Supplier Authorization Letter template** | 📋 Template |
| C — Factory | **Equipment Inventory template** (pre-filled), **Workforce Statement** (pre-filled) | 📋 Template |
| D — Quality | **ITP template** (pre-filled with example), **NCR Form**, **Calibration Register** | 📋 Template |
| E — Materials | **Material Submittal Form** for each BOQ item, **Compliance Statement Matrix** | 📋 Template |
| F — Execution | **Shop Drawing Register**, **Mock-up Approval Form**, **RFI Form** | 📋 Template |
| G — HSE | **HSE Policy statement** (ready to print), **Risk Assessment**, **PPE Matrix** | 📋 Template |
| H — Submission | **Transmittal Letter**, **Prequalification Cover Sheet**, **Document Receipt Acknowledgment** | 📋 Template |

Templates should have UNDERLINES / BLANK SPACES for hand-filling. Pre-fill company data where known (CR, equipment lists, workforce numbers) but leave client-specific fields blank.

## Profile Content Structure (7 Pages)

| Page | Content | Image |
|------|---------|-------|
| 1 — Cover | Full-bleed navy, company name, stats (3 factories/8 companies/25+ yrs/5000+ m²), tagline | Hero factory photo (opacity 0.10-0.15) |
| 2 — About | Company overview, CR, GOSI, factory location, ISO certs, Vision/Mission | Factory building photo |
| 3 — Manufacturing | Production capacity (wardrobes/day, beds/day, etc.), equipment, 5 zones | Factory floor photo |
| 4 — Products | 5 categories with icons, 4-step service flow | Product gallery (4 photos) |
| 5 — Portfolio | Project table by sector, key clients strip | — |
| 6 — Quality | ISO, SASO/SABER, SBC, Local Content cards, QC flow | QC lab photo |
| 7 — Why Us | 6 differentiator grid + contact CTA | — |

## Color Scheme

- Primary: Navy `#1a3a5c`
- Dark: `#0f2a45`
- Accent: Gold `#c9a84c`
- Gold light: `#e8d49a`
- Background: Beige `#f8f6f2` / Cream `#faf8f4`
- Text: Charcoal `#1a1a1a`
- Muted: Gray `#6b7280`

## DOCX Generation Pattern

Use python-docx for Word documents:

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Set default font
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

# Add heading
doc.add_heading('Section Title', level=1)

# Add table
table = doc.add_table(rows=5, cols=3)
table.style = 'Light Grid Accent 1'

# Save
doc.save('output.docx')
```

## Pitfalls

| Pitfall | Fix |
|---------|-----|
| Using Chinese/emoji-like placeholder blocks for photos | Extract and embed real photos from source PDF |
| Arabic-led design | English heading first, Arabic secondary |
| Forgetting the logo | Extract from source PDF and embed prominently on cover + footer |
| Oversized HTML (5+ MB) | Resize images before embedding or use JPEG at reasonable quality |
| HTML file not self-contained | Embed ALL images as base64, ALL CSS inline |
| Page overflow in print | Use `@page` with exact mm, test with `window.print()` preview |
| Wrong document type for the entity | Manufacturer/factory prequal ≠ subcontractor prequal |
| No print button | Add `onclick="window.print()"` for easy PDF export |
| Delegating design to yourself instead of Claude | Always use Claude Code for HTML profile design |

## Verification Checklist

- [ ] English-led bilingual (English heading, Arabic below)
- [ ] Logo from source PDF embedded
- [ ] Real photos from corporate PDF (not placeholders)
- [ ] Google Fonts loaded via @import
- [ ] A4 landscape CSS (@page + .page class)
- [ ] 7 pages, each with page-break-after
- [ ] Self-contained single file
- [ ] Print button present
- [ ] Opens in browser without errors
- [ ] Footer with page numbers on every page

## Related Skills

- `claude-code` — delegate the actual HTML design to Claude
- `html-print-layout` — fixing page overflow in dense tabular profiles
- `document-analysis` — extracting text from PDFs, handling OneDrive-locked files
- `subagent-driven-development` — delegating the individual document creation tasks
