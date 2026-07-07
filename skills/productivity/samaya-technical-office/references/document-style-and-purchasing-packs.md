# Document Style Guide & Purchasing Pack Creation

## Document Style Guide Workflow

### When to use
The Technical Office needs to produce a formal .docx document (report, purchasing pack, submittal, meeting minutes).

### Step 1: Check or create the style guide
1. Check `_Style-Guides/Doc Style Guide/` for an existing guide
2. If none exists, develop one BEFORE writing the document
3. The guide must be created with python-docx helper code — consult Claude to produce a working `SamayaDocument` class

### Step 2: Style guide requirements
| Element | Setting |
|---|---|
| Page | A4 portrait, 21.0 x 29.7 cm |
| Margins | 2.5 cm top, 2.0 cm bottom, 2.5 cm left, 2.0 cm right |
| Font | Calibri throughout |
| Title (H1) | 16pt Bold, Navy #1E293B, bottom border |
| Section (H2) | 12pt Bold, Navy, bottom border |
| Body | 10pt, justified, 12pt line spacing |
| Tables | Navy header (#1E293B), white text, 8pt. Alternating white/light gray rows. Column widths sized to content. |
| Note boxes | Left red border (#B01E2F), light gray bg (#F8FAFC) |
| Header | 7.5pt — project name, doc ref, date |
| Footer | 8pt — doc number, page X of Y, company name |
| Actions | Checkbox-table format with muted bg |

### Formatting rules
- No emoji or icons in formal documents
- No markdown-style formatting in docx
- No AI-isms ("delve", "navigate", "let's", exclamation marks)
- No background images — light shading only for table rows
- Print-friendly: black text on white, borders for structure
- For bilingual content: _set_rtl() for Arabic paragraphs, right alignment

### Step 3: Python-docx implementation
Use the `SamayaDocument` class pattern:
```python
doc = SamayaDocument(project_name='...', doc_ref='...', date='...')
doc.add_title('DOCUMENT TITLE')
doc.add_h2('1.  SECTION HEADING')
doc.add_body('Body text here.')
doc.add_table(['HEADER1', 'HEADER2'], [['data1', 'data2']], col_widths_cm=[3, 13])
doc.add_note('Important note.', label='IMPORTANT')
doc.add_actions(['Action 1', 'Action 2'])
doc.save('output.docx')
```

### Step 4: Save to project
- Style guide: `_Style-Guides/Doc Style Guide/Samaya_Doc_Style_Guide_vX.X.md`
- Document: in the relevant subcontractor or project folder

---

## Purchasing Information Pack Creation

### When to use
The Technical Office needs to brief the Purchasing Department on materials to source that are NOT covered by subcontractor scope.

### What Purchasing handles (not subcontractors)
- Door hardware
- Floor finishes (sample stage)
- Setworks/joinery raw materials (for in-house factory)
- Replica/model-making materials
- Graphics/signage materials
- Patinated brass (NRS-suggested supplier available)

### What subcontractors handle (not Purchasing)
- AV equipment — Rawasin
- Lighting fixtures — Studio ZNA (once contracted)
- MEP equipment — MEP designer/installer
- Showcases — Glasbau Hahn
- Ceiling finishes — subcontractor
- Drywall/metal studs — subcontractor (Mada)
- Acoustic panels — acoustic specialist
- General construction materials — subcontractor

### Folder structure
```
<Subcontractor_Folder>/10_Purchasing/
├── 01_NRS_Specs/        # NRS specification PDFs
├── 02_Datasheets/       # Manufacturer datasheets (reference)
├── 03_Drawings/         # Schedules, type drawings
├── Purchasing_Info.docx  # Summary per style guide
└── README.md             # Markdown version
```

### Required sections in the DOCX
1. Summary (brand spec, finish, standards, quantities)
2. Specification reference (documents and their descriptions)
3. Materials/hardware table (item, specs, quantities)
4. Quantities by location
5. Reference brands (marked "reference only — not specified")
6. Actions checklist for Purchasing (checkbox format)
7. Note boxes for critical requirements

---

## Subcontractor Contract Status — Current (Jun 2026)

| Subcontractor | Status | Contacts |
|---|---|---|
| **Rawasin (AV/IT)** | ✅ Executed — Samaya sister company | Soliman Obiya (soliman@rawasin.com), Al Zeeny, Shehab, Mutai Alrahamn |
| **ITC (MEP Designer)** | 🔴 ON HOLD — variation claim | New MEP designer being negotiated |
| **Studio ZNA (Lighting)** | ❌ Not yet made — proposal under review | Via Mohammed Hakami (m.hakami@samayainvest.com) |
| **MEP Installation** | ❌ Not awarded — tied to designer | — |
| **Glasbau Hahn (Showcases)** | 🟡 Contract at risk | Awaiting client decision |
| **Ahmed Albahrawi** | LEFT Samaya. Adel Darwish is Project Director. | adel@samayainvest.com |
