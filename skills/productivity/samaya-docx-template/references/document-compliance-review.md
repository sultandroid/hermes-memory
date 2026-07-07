# Document Compliance Review — BEP / ISO 19650

## Methodology (worked example: Sheet Numbering System)

When a consultant or reference document needs compliance checking against project standards:

### 1. Extract source document content

```python
from docx import Document
doc = Document("/path/to/source.docx")
for para in doc.paragraphs:
    print(para.text)
for i, table in enumerate(doc.tables):
    for row in table.rows:
        print(" | ".join(cell.text for cell in row.cells))
```

### 2. Find the authoritative project standard

The BEP is the primary reference. Key locations for Aseer Museum:

| Document | Location |
|----------|----------|
| BEP Rev R02 | `Bim Unit/Aseer-Museum/Docs/02_Plans_and_Procedures/02.2_BEP_MIDP_TIDP/` |
| BEP Comment Response | `Asher_Regional_Museum_Document_Control/06_PDFs/General/` |
| Naming Convention Appendix | Referenced as `223032-SAM-XX-XX-BEP-B-XX-Appendix-05_Naming_Convention` (not always filed) |

### 3. Extract BEP reference tables

Key tables from BEP Table 24 (Sheet Naming Convention) and Table 30 (Discipline Codes):

```python
# BEP Table 24 — Sheet naming container format
# 223032 - SAM - XX - XX - RVT - AR - 001
# Project - Orig. - Vol. - Level - Type - Disc. - No.

# BEP Table 30 — Authoritative discipline codes
DISCIPLINE_CODES = {
    "AR": "Architecture",
    "ST": "Structure",
    "ID": "Interior Design",
    "HV": "HVAC",
    "EL": "Electrical",
    "PL": "Plumbing/Drainage",
    "FF": "Fire Fighting",
    "LS": "Landscape",
    "IT": "ICT/ELV",
    "INF": "Infrastructure",
    "LC": "Low Current",
    "GAS": "Gas System",
    "FA": "Fire Alarm",
}
```

### 4. Compare against each compliance dimension

| Dimension | Check against | Typical findings |
|-----------|--------------|------------------|
| Discipline codes | BEP Table 30 — two-letter codes (AR, ST, ID...) vs single-letter US codes (A, S, M...) | **CRITICAL** — single-letter US codes (G, C, S, A, M, E, F, T) do not match BEP (AR, ST, ID, HV, EL, PL, FF, IT). Must flag. |
| Format structure | ISO 19650 container code at CDE level vs simplified title-block code | **Minor** if doc acknowledges the distinction. Acceptable as long as full container code is maintained at CDE. |
| Sequential numbering length | BEP uses 3-digit (001); doc uses 2-digit (01) | **Low** — can be explained as title-block vs CDE difference, but should note. |
| Type/category system | Not always in BEP; compare against US NCS (National CAD Standard) if BEP is silent | **Low** — acceptable internal convention if no BEP conflict. |
| Missing disciplines | Does the doc cover all BEP disciplines needed for this project? | **Moderate** — e.g., INF (Infrastructure), GAS, LS may or may not be in scope. On this project, ID is treated as an AR sub-discipline (no separate ID code) — confirm with Tech Office before flagging as a gap. |

### 5. Produce structured report

Format findings as a summary table:

```
| Aspect | Verdict | Severity |
|--------|---------|----------|
| ISO 19650 container code compliance | Partially compliant (title-block only) | Minor |
| BEP discipline code alignment | NOT COMPLIANT — codes don't match | CRITICAL |
| Format structure consistency | Mixed | Moderate |
| Type/category system | Not in BEP but acceptable | Low |
| Sequential numbering | Mismatched (2-digit vs 3-digit) | Low |
| Missing disciplines | Several BEP disciplines uncovered | Moderate |
```

Then list each issue with its fix:

- Issue 1: Replace single-letter codes with BEP Table 30 codes
- Issue 2: Align sequential number length
- Issue 3: Verify missing BEP disciplines (INF, GAS, LS) are not needed or added. Note: ID is treated as an AR sub-discipline on this project — do not create a separate ID code unless the user confirms otherwise.

### 6. Reformatted document placement

After analysis and reformatting, file the Samaya-styled DOCX in the correct project folder:

| Document type | Place here |
|--------------|------------|
| Naming convention / sheet standard | `Bim Unit/Aseer-Museum/Docs/02_Plans_and_Procedures/02.2_BEP_MIDP_TIDP/` |
| BEP companion documents | Same folder as BEP |

## Key BEP data for Aseer Museum (for quick reference)

### Project codes
- Project number: 223032
- Originator: SAM (Samaya)
- Volume/Level: XX (not specified / all)
- Document types: RVT, 3DM, PDF, DWG
- Drawings at sheet level: e.g., A001 (discipline prefix + 3-digit number)

### Discipline code mapping (US → BEP)

| US code | BEP code | Notes |
|---------|----------|-------|
| A (Arch) | AR | Architecture |
| S (Struct) | ST | Structure |
| M (Mech) | HV / PL | Split HVAC vs Plumbing |
| E (Elec) | EL | Electrical |
| F (Fire) | FF / FA | Fire Fighting vs Fire Alarm |
| T (Telecom) | IT / LC | ICT vs Low Current |
| G (General) | — | Not in BEP; assign as needed |
| C (Civil) | — | Limited scope on museum fit-out |
| — | ID | Interior Design — **treated as AR sub-discipline on this project** (use AR code, confirmed Tech Office Mgr) |

### ISO 19650 container code structure

```
223032 - SAM - XX - XX - {DOC_TYPE} - {DISCIPLINE} - {###}
  (1)    (2)    (3)   (4)      (5)           (6)         (7)

Where:
(1) Project number     = 223032
(2) Originator         = SAM
(3) Volume/Zone        = XX
(4) Level              = XX
(5) Document type      = RVT / 3DM / PDF / DWG
(6) Discipline         = AR / ST / ID / HV / EL / PL / FF / IT / FA / GAS / LC / LS
(7) Sequential number  = 001–999
```
