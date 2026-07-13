# DOCX Audit-and-Fix Workflow

Systematic audit and structural fix for an existing DOCX that was NOT generated via SamayaDoc. Covers heading styles, table splitting, content consistency, and table rebuilding via XML.

## When to use

- User says "check this [plan docx]" — first run the audit
- Document has all "Normal" style paragraphs (no heading styles) with section titles in bold direct formatting
- Document has RBS/category inconsistencies between sections
- Timelines or dates are stale (need updating)
- Missing project-specific risks or content items
- Tables split across pages (no cantSplit)

## Audit Phase

Run these checks on the DOCX before making any changes. For any multi-section audit that covers the full document, present findings as a table with Arabic summaries for each point (one line per finding, plain Arabic, no symbols, no AI fingerprints).

Arabic summary rule: after each English finding point, add `{arabic text}` on its own line. Keep it short (10-15 words), simple everyday words, no formal/compound Arabic.

```python
from docx import Document
from docx.oxml.ns import qn

doc = Document(path)

# 1. Check heading styles
styles_used = {}
for p in doc.paragraphs:
    s = p.style.name if p.style else 'None'
    styles_used[s] = styles_used.get(s, 0) + 1
print("Styles:", styles_used)
# If only 'Normal' with no Heading 1/2/3 -> need style fix

# 2. Check cantSplit on tables
missing = False
for ti, table in enumerate(doc.tables):
    for ri, row in enumerate(table.rows):
        cant = row._tr.findall('.//' + qn('w:cantSplit'))
        if not cant:
            missing = True
if missing:
    print("Need cantSplit on tables")

# 3. Check RBS/Content consistency
# Compare category codes between section X.1 (RBS hierarchy) and X.2 (distribution)
# Look for codes in one that don't exist in the other

# 4. Check stale timelines
for p in doc.paragraphs:
    if 'months remaining' in p.text.lower():
        print(f"Timeline: {p.text[:100]}")
# Cross-reference against current date

# 5. Check for missing risks (e.g., Mostadam/sustainability)
```

## Fix Phase

### 1. Apply Heading Styles

Map paragraph index to style name. Pattern:
- Main sections (1, 2, 3...) -> Heading 1
- Sub-sections (1.1, 1.2, 2.1...) -> Heading 2
- Appendices (A, B, C..., DOCUMENT CONTROL) -> Heading 1 or 2 per hierarchy

```python
heading_map = {
    30: 'Heading 1',   # 1  PURPOSE & SCOPE
    31: 'Heading 2',   # 1.1  PURPOSE
    37: 'Heading 2',   # 1.2  SCOPE
}

for pi, style_name in heading_map.items():
    if pi < len(doc.paragraphs):
        doc.paragraphs[pi].style = doc.styles[style_name]
```

**Pitfall:** Ensure heading style names exist in the document. After applying, the TOC must be updated manually in Word (right-click > Update Field).

### 2. Add cantSplit to All Table Rows

```python
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

for table in doc.tables:
    for row in table.rows:
        tr = row._tr
        existing = tr.findall('.//' + qn('w:cantSplit'))
        if not existing:
            trPr = tr.find(qn('w:trPr'))
            if trPr is None:
                trPr = parse_xml(f'<w:trPr {nsdecls("w")}/>')
                tr.insert(0, trPr)
            cant = parse_xml(f'<w:cantSplit {nsdecls("w")} w:val="true"/>')
            trPr.append(cant)
```

### 3. Rebuild a Table via XML

Use when the table structure needs complete replacement (e.g., RBS alignment):

```python
# Remove all data rows
header_row = table.rows[0]
for row in list(table.rows)[1:]:
    row._tr.getparent().remove(row._tr)

# Create new rows with cells
for row_data in data_rows:
    row_elem = parse_xml(f'<w:tr {nsdecls("w")}><w:trPr/></w:tr>')
    for ci, cell_text in enumerate(row_data):
        tc = parse_xml(f'<w:tc {nsdecls("w")}><w:tcPr><w:tcW w:w="{widths[ci]}" w:type="dxa"/></w:tcPr><w:p><w:r><w:t>placeholder</w:t></w:r></w:tc>')
        tc.find('.//' + qn('w:t')).text = cell_text
        row_elem.append(tc)
    table._tbl.append(row_elem)
    # Add cantSplit
    cant = parse_xml(f'<w:cantSplit {nsdecls("w")} w:val="true"/>')
    row_elem.find(qn('w:trPr')).append(cant)
```

**Pitfall:** When removing rows, iterate from end to start or use `list(table.rows)[1:]` for a stable copy.

### 4. Fix Text Content

```python
# For table cells
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    if 'old_text' in r.text:
                        r.text = r.text.replace('old_text', 'new_text')

# For paragraphs
for p in doc.paragraphs:
    for r in p.runs:
        if 'old_text' in r.text:
            r.text = r.text.replace('old_text', 'new_text')
```

**Pitfall:** Text may be split across multiple runs. If target text not found in any single run, do XML-level replacement:

```python
from lxml import etree
xml_str = etree.tostring(doc.element, encoding='unicode')
xml_str = xml_str.replace('old_text', 'new_text')
doc.element = etree.fromstring(xml_str.encode())
```

### 5. Add a Row to an Existing Table

Same XML construction as step 3, but append only one row via `table._tbl.append(row_elem)`.

## Verification Phase

```python
doc.save(path)
doc2 = Document(path)

# Verify heading styles
for p in doc2.paragraphs:
    if 'PURPOSE' in p.text and 'SCOPE' in p.text:
        assert p.style.name == 'Heading 1'

# Verify cantSplit on all tables
for table in doc2.tables:
    for row in table.rows:
        assert row._tr.findall('.//' + qn('w:cantSplit'))

# Verify content fixes
for table in doc2.tables:
    for row in table.rows:
        for cell in row.cells:
            assert '3.5 months' not in cell.text
```

## Common Issues Found During Audit

| Issue | Detection | Fix |
|-------|-----------|-----|
| No heading styles | All paragraphs show "Normal" style | Apply Heading 1/2/3 by index |
| Tables split across pages | No cantSplit on rows | Add cantSplit to all rows |
| RBS/category codes mismatch | Compare codes across sections | Rebuild one table to match the other |
| Stale timeline/dates | Search for old month counts | Run-level or XML replacement |
| Missing project-specific risks | Compare against known risk factors | Add row to risk profile table |
| Embedded images broken | Word shows broken image icons | Fix cNvPr names + RGBA->RGB |

## Content Cross-Reference Audit (DOCX vs Repo Markdown)

When the DOCX is a formal CG submittal version and the repo holds a working/internal markdown version of the SAME plan, compare them systematically:

### What to check

| Check | What to look for |
|-------|-----------------|
| Scoring scale | DOCX PxI 1-5 vs repo PxS 1-4? Align to repo (it reflects actual risk register) |
| RBS / Risk categories | DOCX has 8 codes but repo has 17? Update DOCX to match repo's 17-code RBS |
| Risk count | DOCX says 29, repo says 33 (Master)? Also check DRR: repo says 37, actual Excel may have 76 |
| Risk ID format | DOCX uses PRR-001, repo uses PRR-COM-01? Update to match repo format |
| Risk profile factors | DOCX lists Heritage Context/Dual GF, repo lists Zero Cash Flow/Permit Block/EOT Dispute? Remove stale, add missing |
| EMV / Quantitative | DOCX SAR 3.4M, repo SAR 7.5M? Update to repo values |
| Sample register | DOCX shows old PRR-001 samples, repo has no sample (uses live register)? Remove sample section or update |
| Response strategies | DOCX has Exploit/Enhance/Share, repo has SOW-Protect? Add SOW-Protect |
| Appendices | DOCX has "Templates", repo has "Open Data Gaps"? Replace content |
| Document control | DOCX shows only v1.0, repo shows v1.0 + C01 + C01.1? Update version history |
| HSE scoring | DOCX missing HSE-specific scale, repo has separate 5x5 scale? Add HSE scale section |

### Procedure

1. Load the DOCX and repo markdown via read_file
2. Build a comparison table (like above) with 3 columns: finding, DOCX value, repo value
3. For each mismatch: decide which is the authoritative source. Repo markdown that was explicitly updated (e.g. "C01 2026-07-12 Full revision aligned to Consolidated Risk Register") is authoritative. The DOCX needs updating to match.
4. Add Arabic summary to each finding row in the format: `{short arabic sentence explaining the gap in simple words}`
5. After the audit report, ask user if they want the DOCX updated to match the repo

### Example finding format

```
### 3. Risk Count Mismatch

| Source | Risks |
|--------|-------|
| DOCX | 29 |
| Repo | 33 (Master) + 37 DRR + 41 HSE + ~30 AV |

عدد المخاطر في المستند 29 بينما الريبو 33 في السجل الرئيسي فقط - يجب تحديث الرقم
```

**Rule:** No AI fingerprints in audit reports. Use plain text tables, plain hyphens, no decorative symbols. Arabic summaries in simple everyday words (not formal/administrative Arabic).

## Related Register (Excel) Alignment Audit

When a plan document references a risk register or other register (e.g., "DRR has 37 risks" or "scoring per RMP"), check the actual Excel file against those references.

### What to check in an Excel risk register

| Check | Method | Typical finding |
|-------|--------|----------------|
| Risk count | Read all data rows | RMP says 37, actual Excel has 76 |
| Scoring scale | Check P and I columns min/max | RMP says PxS 1-4, but Excel uses P(1-4) x I(1-5) |
| Threshold documentation | Search for legend/key in all sheets | Missing threshold legend (Critical >=15 undocumented) |
| Summary formulas | Check if summary cells contain =SUM formulas or hardcoded numbers | Hardcoded numbers = stale risk on update |
| Risk ID format | Check pattern (PRR-001 vs PRR-COM-01 vs DB-A-001) | DRR uses DB-A-001, RMP mentions PRR-COM-01 |
| Category alignment | Compare RBS codes in Excel vs RMP | DRR has 10 categories, RMP lists 17 |
| Status column | Check if status (Open/Watch/Mitigated/Closed) exists | Often missing in design-stage registers |
| Owner codes | Check if code legend exists | DSN-A, CTR PM undefined |
| Data completeness | Count empty cells in P, I, mitigation, owner columns | Should be zero for a mature register |
| Duplicates | Check risk IDs for duplicates | Should be zero |

### Procedure

1. Open the Excel with openpyxl (data_only=True)
2. Extract all data rows, scoring columns, and summary section
3. Build comparison: what the plan says vs what the Excel actually contains
4. Score the register health: completeness (pass/fail per column), formula correctness, threshold documentation
5. Present findings with Arabic summaries, same format as DOCX audit

### Example finding format

```
### Scoring Scale Mismatch

| Item | DRR Excel | RMP says |
|------|-----------|----------|
| P scale | 1-4 | 1-4 |
| I/S scale | 1-5 | 1-4 |
| Critical threshold | >=15 (undocumented) | >=12 |

الـ DRR يستخدم مقياس شدة 1-5 بينما الـ RMP يتطلب 1-4 - غير متوافق مع مبدأ التوحيد المذكور في الـ RMP
```

## Arabic Summary Formatting Rules for Audit Reports

When the user requests Arabic summaries for audit findings, follow these rules:

- One Arabic line per finding point, placed immediately after the English finding summary
- 10-15 words max per line
- Simple everyday vocabulary (write as a site engineer speaks, not as a government document)
- No formal/compound Arabic (no مقرر نقاش, جدولة عرضية, الإجراءات التخفيفية)
- No symbols or decorative punctuation
- The Arabic line should state the gap simply: "X is Y but should be Z" or "X is missing"
- Use numbers where applicable (عدد المخاطر 29 بينما الصحيح 33)

Example:
```
عدد المخاطر في المستند 29 بينما الريبو 33 - يجب التحديث
```

Bad (formal/compound):
```
توجد اختلافات في تصنيف المخاطر بين المستندين مما يستدعي إعادة التقييم
```
Good (simple):

```
تصنيف المخاطر مختلف بين المستند والريبو - 8 تصنيفات مقابل 17
```

## Related References

- `references/docx-formatting-fixes.md` - Page breaks, table splitting, column widths
- `references/docx-editing-techniques.md` - Editing existing DOCX (remove rows, update paragraphs)
- `references/docx-image-rendering-fix.md` - Fix for images disappearing after bulk edits
- `references/retrofit-samaya-branding.md` - Retrofitting full Samaya branding onto existing DOCX
