# Aseer-Museum Document Code → Folder Routing

## Primary Routing (Document Type)

| Code | Meaning | Target Folder |
|------|---------|---------------|
| `PL` | Plan / Procedure | `Docs/02_Plans_and_Procedures/` (→ subfolder by type) |
| `ZD` | General Document / Design Doc | `Docs/11_Correspondence/` |
| `TQ` | Technical Query | `Docs/04_RFIs/` |
| `RP` | Report | `Docs/07_Reports/` |
| `IR` | Inspection Request | `Docs/10_Test_and_Inspection/` |
| `SI` | Site Instruction | `Docs/05_SIs/` |
| `NC` / `NCR` | Non-Conformance | `Docs/12_Compliance_and_Audit/` |
| `DOC` | Transmittal | `Docs/11_Correspondence/` |
| `MIN` | Meeting Minutes | `Docs/08_Meeting_Minutes/` |
| `SDR` | Shop Drawing | `Docs/03_Submittals/` |
| `MAR` | Material Approval | `Docs/03_Submittals/` |
| `SC` | HSE Deliverable / Submittal | `Docs/02_Plans_and_Procedures/02.5_HSE_Plan/` |
| `PQ` | Prequalification | `Invoices/Docs/` or `Docs/03_Submittals/` |

## Secondary Routing (Discipline Code — Originator)

The Originator code (digit 8-9 of the document code, e.g. `1KH` in `MOC-MUS-ASE-1KH-PL-0054`) determines the subfolder within the primary target:

| Code | Originator | Filing Convention |
|------|------------|-------------------|
| `1KH` | Samaya HSE (health/safety/environment) | HSE-related PL → `02.5_HSE_Plan/01_Source_Files/` |
| | | HSE-related ZD/SC → `02.5_HSE_Plan/01_Source_Files/` |
| `1K0` | Samaya General (management/design) | ZD → `Docs/03_Submittals/03.1_Design_Submittals/` |
| | | PL (non-HSE) → `Docs/02_Plans_and_Procedures/` subfolder |
| `1A0` | Architecture / NRS design | ZD → `Docs/03_Submittals/03.6_Architectural_Submittals/` |
| `1E0` | Electrical | ZD → appropriate discipline subfolder |
| `1M0` | Mechanical | ZD → appropriate discipline subfolder |
| `1C0` | Civil | ZD → appropriate discipline subfolder |

### ⚠️ Always Check Existing Pattern First

Before filing a new document:
1. Search the Correspondence/ folder for similarly-coded documents (e.g., `find ... -name "*ZD-005*"`)
2. Search the HSE plan source files for PL documents of nearby numbers
3. Follow the pattern set by the most recent similar document — if ZD-0052 (1KH) went to `Correspondence/` only, start there
4. If the document has CG review comments embedded (same-day response), also file CG response in `02.5_HSE_Plan/02_CG_Responses/`

## Universal Secondary Location

**All filed documents should also be copied to `Correspondence/`** (the flat folder at project root). This is the universal inbox for transmitted documents regardless of type. The canonical archive lives in the `Docs/` subfolder; `Correspondence/` is for quick reference.

Example: `MOC-MUS-ASE-1KH-PL-0054.pdf` goes to both `02.5_HSE_Plan/01_Source_Files/` AND `Correspondence/`.

## CG-Reviewed Documents — Register Updates

When a document has a CG response (Code A/B/C/D), update these registers:

| Register | Location | What to Add |
|----------|----------|-------------|
| CG_Response_Register.md | `02.5_HSE_Plan/04_Registers/CG_Response_Register.md` | New row in Full Document Register table, update Key Statistics counts, add to Critical Actions (if Code C/D), add to CG Response Timeline |
| PROJECT_MEMORY.md | `_Project_Memory/PROJECT_MEMORY.md` | Add row in Latest Status Updates section |

### CG Response Codes (Embedded on Cover Page)

| Code | Meaning | Action Required |
|:----:|---------|----------------|
| A | Approved | File and close |
| B | Approved with Comments | Address comments, resubmit if needed |
| C | Revise and Resubmit | ↳ Row in Critical Actions section |
| D | Disapproved | ↳ Row in Critical Actions section (highest priority) |

### CG Response Date Convention

When the cover page shows both a Submittal Date and a CG Response Date on the same day (e.g., 6-Jun-2026 for both), the CG reviewed and responded the same day. The response is embedded in the PDF itself — no separate email reply exists. Record the CG reviewer name from the signature block (e.g., Anwar Sadat for HSE reviews).

## PL Documents — Subfolder Resolution

`Docs/02_Plans_and_Procedures/` has numbered sub-folders by plan type:

| Subfolder | Content |
|-----------|---------|
| `02.1_DMP/` | Design Management Plan |
| `02.2_BEP_MIDP_TIDP/` | BIM Execution Plan |
| `02.3_PEP/` | Project Execution Plan |
| `02.4_PQP/` | Project Quality Plan |
| `02.5_HSE_Plan/` | **HSE plans** (most PL docs) |
| `02.6_NRS_Methodology/` | NRS Design Methodology |
| `02.7_Communication_Plan/` | Communication Plan |
| `02.10_Subcontractor_Deliverables/` | Subcontractor documents |

HSE-related PL docs go specifically to `02.5_HSE_Plan/01_Source_Files/` (the PDF source file directory, not the root).

## Document Code Breakdown

```
MOC-MUS-ASE-1KH-PL-0054 Rev.00
│   │    │   ││  │  │
│   │    │   ││  │  └── Sequential number
│   │    │   ││  └───── Type code (PL=Plan, ZD=Design Doc, SC=HSE Submittal,
│   │    │   ││                 TQ=Tech Query, RP=Report, IR=Inspection,
│   │    │   ││                 SI=Site Instruction, PQ=Prequalification,
│   │    │   ││                 SH=Schedule, MS=Method Statement)
│   │    │   │└─────── Originator code (1KH=Samaya HSE, 1K0=Samaya General,
│   │    │   │                  1A0=NRS/Architecture, 1E0=Electrical,
│   │    │   │                  1M0=Mechanical, 1C0=Civil, 0PS=Programme)
│   │    │   └───────── Project code (ASE=Aseer, ALF=Al Faw, EG=El-Ghamama)
│   │    └───────────── Entity (MUS=Museum)
│   └────────────────── Client/Authority (MOC=Ministry of Culture)
```

## Conventions by Session (from recent filing operations)

- **1KH + PL = HSE Plan** → `02.5_HSE_Plan/01_Source_Files/` + `Correspondence/`
- **1KH + ZD + HSE content** (training programs, notice boards) → `02.5_HSE_Plan/01_Source_Files/` + `Correspondence/`
- **1KH + ZD + non-HSE** → `Correspondence/` only (per ZD-0052 pattern)
- **1K0 + PL** (non-HSE, e.g. Stakeholder Plan) → `02.7_Communication_Plan/` or appropriate subfolder + `Correspondence/`
- **1K0 + ZD** (design-related, e.g. MEP Team) → `Docs/03_Submittals/03.1_Design_Submittals/` + `Correspondence/`
- New submittals (Rev.00) without prior pattern → check `Email_Archive/` for submission email first

## Common Email Sender → Project Mapping

| Sender Domain | Project Assignment |
|---------------|-------------------|
| `@samayainvest.com` | Internal — classify by subject code |
| `@cg.com.sa` | CG Consultant → **Aseer** (all MOC-MUS-ASE docs) |
| `@nissenrichardsstudio.com` | NRS (Showcase Designer) → **Aseer** |
| `@glasbau-hahn.de` | GBH (Showcase Fabricator) → **Aseer** |
| `@adeng.com.sa` | Supervision/Adeng → **Aseer** |
| `@egec.com.sa` | EGEC → **Zamzam** |
| `@3d-me.com` | 3DME (Artec Spider) → **Aseer/Replica** |
| `@sitml.com` | SITML (Lidar scanning) → **Aseer** or **General** |

## Non-Aseer Attachments

| Sender | Subject Pattern | Project | Target |
|--------|----------------|---------|--------|
| `Kareem.Hussain` | jabal omar | Jabal Omar | `Jabal Omar - Samaya Scope/Docs/` |
| `M.almakarem` | زمزم / Zamzam | Zamzam MVC | `Zamzam Museum/Submittal's/` |
| `erp@samayainvest.com` | P0xxxx | Various | Route by project code in title |
| `sultan@samayainvest.com` | تسعير / Quotation | General | `Samaya/Estimations/` |
| `maged@samayainvest.com` | تسعير / Quotation | General | `Samaya/Estimations/` |
| Supplier quotes | Quotation | General | `Samaya/Estimations/` |

## Aseer-Museum HR / CV Routing

CV attachments from recruitment emails → `Aseer-Museum/HR/CVs/`

## Zamzam Museum Submittals

Zamzam documents from M. Almakarem use code pattern `ZAM-NWC-CTR-{TYPE}-{DISC}-{NUM}_Rev.XX.pdf`:
- `WIR` → Work Inspection Request
- `IR` → Inspection Request  
- `DOC` → Document Transmittal
- `CLR` → Clearance

All go to `Zamzam Museum/Submittal's/` (note the possessive apostrophe — this is the existing folder name).
