# Acoustic Specialist Prequalification — SOW + RACI Pattern

## Context

CG rejected acoustic specialist prequalifications (ACOUSTIEG, AME, JOCAVI) because the submissions lacked the project Scope of Work and RACI matrix. The fix: generate a prequalification support document that includes BOTH the full SOW and a RACI matrix as integral sections, not as separate attachments.

## Company Folder Structure

Under the specialist's main folder (e.g., `18_Acoustic_Specialist/`), create numbered company folders:

```
18_Acoustic_Specialist/
├── 10_ACOUSTIEG/
│   └── 00_Prequalification/
│       └── ACOUSTIEG_Prequalification_Support_Document.docx
├── 11_AME/
│   └── 00_Prequalification/
│       └── AME_Prequalification_Support_Document.docx
└── 12_JOCAVI/
    └── 00_Prequalification/
        └── JOCAVI_Prequalification_Support_Document.docx
```

Each company folder also gets `01_Proposals/`, `02_Correspondence/`, `03_Approvals/` subfolders.

Numbering: sequential (10, 11, 12...) under the parent specialist folder.

## Document Structure (10 sections)

| Section | Content |
|---------|---------|
| Cover | Project name, contract ref, trade, proposed specialist, PQ ref, doc ref |
| 1.0 | Introduction & Purpose — Samaya invites the specialist to submit |
| 2.0 | Project Overview — location, altitude, contract type, team (MoC, NRS, CG) |
| 3.0 | Acoustic Scope of Work — assessment, design recommendations, commissioning |
| 4.0 | Design Deliverables — 21 items (AC-001 to AC-021) by phase |
| 5.0 | RACI Matrix — 11 activities × 6 roles |
| 6.0 | Prequalification Requirements — certs, experience, technical capabilities |
| 7.0 | Submission Requirements — company info, portfolio, CVs, method statement, programme |
| 8.0 | Coordination Interfaces — BIM, AV, MEP, structural, FLS |
| 9.0 | Standards & References — BS 8233, ISO 3382, DIN 18041, etc. |
| 10.0 | Declaration & Company Stamp — signature block |

## RACI Matrix (Acoustic Specialist)

11 activities × 6 roles:

| Activity | Specialist | Samaya PM | NRS | CG | MEP Coord | BIM Unit |
|----------|-----------|-----------|-----|-----|-----------|----------|
| Acoustic Assessment & Survey | R | A | C | I | C | I |
| Acoustic Design Development | R | A | C | C | C | I |
| Material Selection & Specification | R | A | C | C | I | I |
| BIM Coordination (LOD 300) | C | I | C | I | C | R/A |
| Submittal Preparation & Review | R | A | C | C | I | C |
| CG Review & Approval | C | C | C | A | I | I |
| Material Procurement & Samples | R | A | C | C | I | I |
| Site Installation Witnessing | R | A | C | C | C | I |
| Inspection & Testing (ISO 3382-1) | R | A | C | C | I | I |
| Commissioning & Certification | R | A | C | A | I | I |
| Handover Documentation & O&M | R | A | C | C | I | I |

## Key Lesson

The prequalification support document is Samaya's document sent TO the supplier. It must include the SOW content and RACI matrix as integral sections — not as separate attachments. The CG rejection was specifically because the SOW and RACI were not attached to the prequalification submission.

## Generation Approach

Use `SamayaDoc` from `samaya_doc_template.py` (python-docx wrapper). The script:

1. Creates a `SamayaDoc` instance with header/footer
2. Adds title page with project info table
3. Adds each section using `add_h2(number, text)` and `add_h3(number, text)`
4. Builds tables using `format_header_cell()` and `format_data_cell()`
5. The RACI matrix is a full table with navy headers and centered RACI codes
6. Saves to `00_Prequalification/<Company>_Prequalification_Support_Document.docx`

See the full generation script at `templates/gen_acoustic_prequal.py` for the complete implementation.
