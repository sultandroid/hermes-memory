# Adel Darwish OneDrive — Folder Structure (Discovered 2026-07-21)

## Root Path

```
/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Adel  Darwish's files - 01- Execution Documents/
```

## Existing Subfolders (with content)

| Subfolder | Content | Notes |
|-----------|---------|-------|
| `01- Letters/IN/CG/01-/` | CG incoming letter + attachments (NCR-CG-001.pdf, TQ-0014 CG reply, TQ-0018 CG response) | NCRs found here, not in 12-NCR |
| `01- Letters/IN/CG/02-/` | Letter 02 SAMAYA.pdf (27-Jun-2026) | |
| `01- Letters/OUT/CG/01–21/` | Outgoing letters to CG (Dec 2025–Mar 2026) | Historical — ARM-SIC-MOC-LET-001 through 021 |
| `05- Request For Information-RFI/` | 24 TQ/RFI folders (TQ-0005 through TQ-0026) | Most have Approval/ subfolders with CG replies |
| `06- Weekly Meeting MOM/` | Empty | |
| `10- CG Site Instruction SI/` | 20 SI folders (SI-001 through SI-020) | Status: CLOSED/OPEN/U |
| `20- DDD/AR/` | 8 DD packages (1G-0001 through 1G-0008) | Architecture DD 50% Gateway |
| `20- DDD/ELE/` | 1 DD package (1E0-1G-0001) | Electrical DD 50% Gateway |
| `20- DDD/ME/` | 1 DD package (1M0-1G-0001) | Mechanical DD 50% Gateway |
| `20- DDD/ci/` | 1 DD package (1C0-1G-0001) + Rev.01 | Structural DD 50% Gateway |
| Root | `ASM_Material_Procurement_Schedule_ARCH.xlsx` (13-Jul-2026) | Procurement schedule |

## Subfolders That DO NOT Exist

| Expected Path | Status |
|---------------|--------|
| `07-Pre-Qualification Submittal/` | ❌ Does not exist |
| `08-Material Submittal MA/` | ❌ Does not exist |
| `09-Method Statement MWS/` | ❌ Does not exist |
| `12-NCR/` | ❌ Does not exist (NCRs in Letters attachments) |
| `13-Weekly Report/` | ❌ Does not exist |
| `14-Inspection Request IR/` | ❌ Does not exist |
| `15-Start New Activity SNA/` | ❌ Does not exist |
| `17-SOR/` | ❌ Does not exist |

## DDD Package Structure Pattern

Each 1G-xxxx package follows this pattern:

```
20- DDD/{DISC}/{NN}- MOC-MUS-ASE-{DISC}-1G-{NNNN}/
    MOC-MUS-ASE-{DISC}-1G-{NNNN}.pdf          ← Submittal PDF
    MOC-MUS-ASE-{DISC}-1G-{NNNN}.xlsx         ← Submittal XLSX (register)
    Approval/                                  ← CG-reviewed version
        MOC-MUS-ASE-{DISC}-1G-{NNNN}.pdf      ← CG-stamped PDF
        MOC-MUS-ASE-{DISC}-1G-{NNNN} CRS CG.xlsx  ← CG comment response sheet
        MOC-MUS-ASE-{DISC}-1G-{NNNN}.BS.rar   ← Back-up source files
        MOC-MUS-ASE-{DISC}-1G-{NNNN}.BS/       ← Extracted BS folder with DDD-xxxx PDFs
```

## TQ Folder Structure Pattern

```
05- Request For Information-RFI/{NN}- MOC-ASEER-SIC-{DISC}-TQ-{NNNN}/
    MOC-ASEER-SIC-{DISC}-TQ-{NNNN}.pdf        ← TQ document
    MOC-ASEER-SIC-{DISC}-TQ-{NNNN}.xlsx       ← TQ register
    Approval/                                  ← CG response (when present)
        MOC-ASEER-SIC-{DISC}-TQ-{NNNN}.pdf    ← CG reply PDF
```

## 02. DOC - Document Submittal/GN/ (98 Submittals)

**Root:** `Adel  Darwish's files - 01- Execution Documents/02. DOC - Document Submittal/GN/`

98 numbered submittal folders (01 through 98), each containing:
- A transmittal PDF (cover sheet)
- An XLSX register
- Supporting documents (PDFs, DOCXs, BOQs)
- Sometimes `Approval/` or `Done/` or `Rev.0x/` subfolders

**Doc ID prefixes and types:**

| Prefix | Type | Count |
|--------|------|-------|
| `ARM-DS-GN-xxxx` | General submittals (mobilization, narrative, etc.) | 9 |
| `MOC-ASEER-SIC-1K0-PL-xxxx` | Plans (submission plan, HSE plan, etc.) | 8 |
| `MOC-ASEER-SIC-1K0-ZD-xxxx` | Shop Drawings (structural/arch) | 3 |
| `MOC-ASEER-SIC-1K0-QT-xxxx` | BOQ / Quantities | 2 |
| `MOC-ASEER-SIC-1A0-TP-xxxx` | Test Procedures | 2 |
| `MOC-ASEER-SIC-1A0-ZD-xxxx` | Shop Drawings (architectural) | 5 |
| `MOC-MUS-ASE-1KH-PL-xxxx` | Plans (specialist/coordination) | 12 |
| `MOC-MUS-ASE-1KH-ZD-xxxx` | Shop Drawings (specialist) | 6 |
| `MOC-MUS-ASE-1KH-SC-xxxx` | SC Requirements | 1 |
| `MOC-MUS-ASE-1E0-ZD-xxxx` | Shop Drawings (electrical/MEP) | 15 |
| `MOC-MUS-ASE-1E0-RP-xxxx` | Reports (electrical) | 1 |
| `MOC-MUS-ASE-1K0-PL-xxxx` | Plans (coordination) | 3 |
| `MOC-MUS-ASE-1K0-ZD-xxxx` | Shop Drawings (coordination) | 8 |
| `MOC-MUS-ASE-1M0-PL-xxxx` | Plans (mechanical) | 1 |
| `MOC-MUS-ASE-1M0-ZD-xxxx` | Shop Drawings (mechanical) | 3 |
| `MOC-MUS-ASE-1A0-ZD-xxxx` | Shop Drawings (architectural) | 6 |
| `MOC-MUS-ASE-MEP-ZD-xxxx` | Shop Drawings (MEP combined) | 2 |
| `MOC-MUS-ASE-1V0-ZD-xxxx` | Shop Drawings (AV/visual) | 1 |

**Converted DOCX files (saved to repo):**

| File | Source Folder | Content |
|------|--------------|---------|
| `001_Mobilization_Plan_Rev03.md` | `01- ARM-DS-GN-0001/` | Mobilization plan: risk matrix, schedule, noise/dust control |
| `006_Narrative_Report_Rev05.md` | `06- ARM-DS-GN-0006/Rev.05/` | Final baseline narrative report |
| `006_Comment_Response_Rev03.md` | `06- ARM-DS-GN-0006/Rev.03/` | Comment resolution sheet |
| `013_Submission_Plan_Meeting_Minutes.md` | `13- MOC-ASEER-SIC-1K0-PL-0013/` | Meeting minutes for submission plan |
| `015_BEP_Comment_Response.md` | `15- MOC-ASEER-SIC-1K0-PL-0015/Rev.01/` | BEP consultant comment response |
| `Submittal_Index.md` | (index of all 98 folders) | Master index with file counts and status |

**Output location:** `Aseer-Museum/04_Docs/08_Adels_Submittals/`

**Status breakdown:** 82 Approved, 13 Done, 3 Submitted (as of 25-Jul-2026)

## Key Dates

- Most Letters: Dec 2025–Mar 2026 (historical)
- Most TQs: Jan–Jul 2026
- DD packages: Jun–Jul 2026
- Latest items (20-Jul-2026): 1G-0005 (updated), 1G-0007, 1G-0008
