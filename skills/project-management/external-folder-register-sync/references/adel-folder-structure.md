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

## Key Dates

- Most Letters: Dec 2025–Mar 2026 (historical)
- Most TQs: Jan–Jul 2026
- DD packages: Jun–Jul 2026
- Latest items (20-Jul-2026): 1G-0005 (updated), 1G-0007, 1G-0008
