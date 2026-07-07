# Samaya Document Style Guide — Quick Start

**Style guide location:** `Samaya/Technical Office/_Style-Guides/Doc Style Guide/Samaya_Doc_Style_Guide_v1.0.md`
**Reusable builder template:** `templates/samaya-docx-builder.py`

## When to Use
Creating formal .docx deliverables for Samaya Technical Office: reports, submittals, purchasing info packs, method statements, inspection requests.

## Core Rules
- **Font:** Calibri throughout
- **Page:** A4 portrait, margins 2.5/2.0/2.5/2.0 cm
- **Title:** 16pt Bold, Navy (#1E293B), bottom border
- **H2:** 12pt Bold, Navy, bottom border
- **Body:** 10pt, justified, line spacing 12pt exactly
- **Tables:** Navy header (#1E293B) with white text, alternating white/light gray rows
- **Note boxes:** Left red border (#B01E2F) 3pt, muted bg (#F8FAFC)
- **No AI footprint:** No emoji, no transitional phrases, no hedging, no markdown in docx
- **Print-friendly:** Light shading only, no background images, black text on white

## Quick Python Pattern
```python
from samaya_docx_builder import SamayaDocument
doc = SamayaDocument(project_name='Aseer Regional Museum', doc_ref='PUR-DH-001', date='06 June 2026')
doc.add_title('DOOR HARDWARE - PURCHASING INFORMATION')
doc.add_h2('1. SUMMARY')
doc.add_table(['ITEM', 'DETAIL'], [['Brand specified', 'No']], col_widths_cm=[3.0, 13.5])
doc.add_note('This is important.', label='IMPORTANT')
doc.add_bullet('Contact suppliers')
doc.save('output.docx')
```

## Complete Builder Class
The `samaya-docx-builder.py` template includes:
- SamayaColors — color constants matching the style guide
- setup_page() — A4 portrait, standard margins
- create_header() / create_footer() — doc strip with ref, page X of Y
- add_title(), add_h2(), add_h3() — heading hierarchy
- add_body() — justified body text
- add_table() — navy headers, alternating rows, fixed column widths
- add_note() — red left-border note boxes
- add_bullet() — indented bullet lists
- add_actions() — checkbox action lists for purchasing/todo

## Pitfalls
- pip install python-docx required
- Images in header need absolute paths (use os.path.abspath())
- Column widths must sum to ~16.5 cm (page width minus margins)
- Never use set_row_height() — breaks wrapped text
- Metric cards need 3 separate paragraphs per cell
- Style guide markdown is authoritative reference; builder is convenience
