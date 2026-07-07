---
name: supplier-prequalification
description: Design prequalification packages for suppliers, manufacturers, and contractors. Create checklists, capability statements, compliance matrices, and professional HTML/DOCX profiles for construction project submissions.
version: 1.0.0
author: Hermes Agent
platforms: [macos]
metadata:
  hermes:
    tags: [prequalification, supplier, manufacturer, compliance, procurement]
    examples: [outline-enterprise-prequal]
prerequisites:
  commands: [python3, claude]
  env_vars: []
---

# Supplier / Manufacturer Prequalification Package

## When to Use

- Entity intake (via `entity-intake` skill) identified gaps in prequalification documents
- User asks to "develop prequalification" for a supplier/manufacturer
- Need to create capability statements, checklists, or compliance matrices
- Need a professional printable company profile (HTML/DOCX)

## Distinction from `entity-intake`

This skill covers the **DESIGN** phase — creating submission-ready documents.
The `entity-intake` skill covers the **RESEARCH** phase — understanding who the entity is.
Use entity-intake first, then this skill for document creation.

## Workflow

### Phase 1: Gather Source Data

Collect from entity-intake output + any additional sources:

| Source | Data to extract |
|--------|----------------|
| Corporate profile PDF | CR number, GOSI, VAT, factory location, certifications, project references |
| Company website | Products, services, team, about |
| LinkedIn | Description, sectors served, years in market |
| Google Drive portfolio | Project list, client names, photo/media |
| Local files | Existing BOQs, specs, templates |

Extract all text from any PDF using pdfplumber or PyMuPDF. Use OCR if the PDF is image-based (no text layer).

### Phase 2: Design the Document Set

Create these 4 core documents (MD + DOCX versions):

#### 2a. Prequalification Submission Document
8 sections:
1. Cover page with project info
2. Table of contents
3. Executive summary / company profile
4. Legal & commercial documentation
5. Manufacturing / operational capability
6. Quality management system (ISO, QC)
7. Previous project experience / portfolio
8. HSE compliance & local content (Saudi Arabia)
9. Appendices

#### 2b. Factory/Manufacturer-Specific Checklist
NOT a generic contractor→subcontractor checklist. Include manufacturer-specific items:
- Industrial License / Municipality License
- SASO/SABER certifications
- Production capacity & equipment list
- Factory location & zone details
- Material sourcing & supply chain
- Testing facilities & QC labs
- Worker health & safety records
- Commercial Register with industrial classification
- ISO 9001, 14001, 45001 certifications
- Saudi Building Code compliance
- Local content / Nitaqat / Saudization
- Financial statements

#### 2c. Company Capability Statement
- Overview & group structure
- Key stats (factories, years, employees)
- Product categories & services
- End-to-end process flow
- Certifications & accreditations
- Key client logos / project references
- Factory details (location, area, equipment)

#### 2d. Compliance Matrix Template
- Project spec sections cross-referenced
- Compliance status per item (Compliant / Non-Compliant / Not Applicable)
- Remarks column for clarifications
- Sign-off section

### Phase 3: Generate DOCX Files

Use `python-docx` to create professional Word documents:
- Cover page with company name, project, date
- Styled tables with colored headers
- Proper heading hierarchy (H1/H2/H3)
- Page numbers in footer
- Professional fonts (Times New Roman or Calibri for print)
- Landscape orientation for checklists and compliance matrices

```python
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
```

### Phase 4: Design HTML Professional Profile

Use Claude Code (`claude -p`) to design a print-ready A4 profile HTML:

**Design spec:**
- A4 landscape format: `@page { size: 297mm 210mm; margin: 0 }`
- Company brand colors extracted from logo/identity
- Bilingual content (Arabic primary + English secondary)
- Professional typography (system fonts for print)
- Pure CSS geometric accents (no external images)
- Placeholder blocks for photos labeled in Arabic
- Print button for PDF export
- Page breaks between sections
- Footer with page numbers

Delegate the HTML design to Claude with:
```bash
claude -p "Design a professional A4 landscape HTML profile for [Company] with the following specs: [specs]" --max-turns 25
```

### Phase 5: Build Folder Structure

```
Prequalification_Package/
├── preq_overview.html              # Browser-viewable HTML summary
├── outline_profile_a4_landscape.html # Print-ready A4 profile
├── 01_Submission_Document/
│   ├── PREQUALIFICATION_SUBMISSION_DOCUMENT.md
│   └── PREQUALIFICATION_SUBMISSION_DOCUMENT.docx
├── 02_Checklists/
│   ├── FACTORY_PREQUALIFICATION_CHECKLIST.md
│   └── FACTORY_PREQUALIFICATION_CHECKLIST.docx
├── 03_Capability_Statement/
│   ├── COMPANY_CAPABILITY_STATEMENT.md
│   └── COMPANY_CAPABILITY_STATEMENT.docx
├── 04_Compliance/
│   ├── COMPLIANCE_MATRIX_TEMPLATE.md
│   └── COMPLIANCE_MATRIX_TEMPLATE.docx
└── create_docx.py                  # Reusable DOCX generation script
```

## Saudi Arabia Specific Requirements

Must include these compliance items for KSA construction projects:
- Commercial Register (CR) with industrial classification
- Zakat & Tax certificate
- GOSI certificate
- Nitaqat / Saudization percentages
- Chamber of Commerce membership
- SASO/SABER product certifications
- Saudi Building Code (SBC) compliance
- Local Content & Government Procurement Authority (LCWA/ICP) registration
- Etimad platform registration
- ISO certifications (9001, 14001, 45001)
- Industrial license if manufacturing
- Municipality license
- Civil Defense / Fire Safety approvals

## Tips

- **Tailor to manufacturer, not subcontractor**: Manufacturing prequal focuses on production capacity, equipment, QC labs, material sourcing. The generic "contractor→subcontractor" checklist with covering letter and commercial register items is insufficient.
- **Use real company data**: Extract CR numbers, factory addresses, project names from actual corporate profile PDFs rather than making assumptions.
- **Entity isolation**: If this is NOT a Samaya project, state it clearly in all documents. Never cross-contaminate project labels.
- **DO NOT regenerate HTML files** for Samaya projects — patch only. For non-Samaya entities, full HTML generation is acceptable.
- **Delegate heavy work**: Claude Code for HTML/DOCX design, python-docx for Word generation, pdfplumber for PDF extraction.
- **Photos from Drive**: The entity's Google Drive likely contains project photos. Document them in the profile as placeholders initially, then replace with real images.

## Pitfalls

- **Generic checklist trap** — Don't reuse the standard contractor→subcontractor checklist. A factory prequalification needs items like production capacity, equipment list, industrial license, SASO/SABER.
- **DOCX generation complexity** — python-docx create_docx.py scripts can be 50-60KB. It's often faster to delegate DOCX creation to Claude Code with a single well-crafted prompt than to write the script yourself.
- **PDF extraction fails on scanned docs** — Use PyMuPDF to check for text layer first. If none, use tesseract OCR with appropriate language flags (`-l eng+ara`).
- **Brand colors** — Extract from the company's PDF logo (Adobe Illustrator files often have color info in metadata) or from website CSS.
- **Google Drive row queries** — The Drive DOM may put content in iframes. Query root document first, then check iframe content if rows appear empty.
