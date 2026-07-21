# Email Pipeline Execution — 2026-07-21 13:50

## Extraction Stats

- 33 emails with attachments processed
- 80 files routed to project folders
- 2 emails returned AppleScript error -2700 (Baffle Ceiling RFQ) — skipped
- 54 unclassified files (Zamzam project files, previous scan artifacts)
- 11 files skipped (images, .eml copies, .crdownload)

## Key CG Items Received

| Email ID | Sender | Document | Action |
|---|---|---|---|
| 48788 | Hossam Mabrouk | NC-1M0-005 CLOSURE.pdf | Filed to NCRs/1M0-005/ |
| 48784 | Hossam Mabrouk | MOC-MUS-ASE-1A0-1G-0005.pdf (GF Arch DD) | Filed to DD_Gate/Architecture/ |
| 48833 | Hossam Mabrouk | MOC-MUS-ASE-1K0-ZD-0087.pdf (Mech Eng replacement) | Filed to Mechanical_Engineer/ |
| 48829 | Hossam Mabrouk | MOC-MUS-ASE-1E0-IR-0001.pdf (CCTV IR) | Filed to Inspection_Requests/ |
| 48780/48822 | Hossam/Samir | PQ-0123 (ACOUSTIEG) | Filed to Acoustieg/ |
| 48783/48820 | Hossam/Samir | PQ-0124 (AME) | Filed to Acoustic_Specialist_AME/ |
| 48782/48821 | Hossam/Samir | PQ-0125 (JOCAVI) | Filed to 06_Acoustic/ |

## New Routing Destinations Discovered

| Document Pattern | Destination Folder | Category |
|---|---|---|
| `NRS Comments_*.xlsx` (CG comments on submission plan) | `02_Submittals/01_DD_Gate/Architecture/` | CG Comments |
| `*Mechanical Submission Plan*.xlsx` | `02_Submittals/01_DD_Gate/MEP/` | Mechanical Submission Plan |
| `*Lifting Gear Inspection*` | `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` | HSE Inspection |
| `*Design_Tracker*.xlsx` | `03_Design_Files/` | Design Tracker |
| `*stakeholder*` or `*Main stakeholders*` | `00_Status/` | Stakeholder List |
| `*lookahead*` | `00_Status/` | Lookahead |
| `*Prequalification_Submission_CG*` | `24_Subcontractors/AME_Acoustic/01_Prequalification/` | Prequal Submission |
| `ZD-0094` (Subcontract Management Plan) | `04_Docs/02_Plans_and_Procedures/02.18_Subcontract_Management_Plan/01_Source_Files/` | Plan |
| `ZD-0095` (QA/QC CV) | `24_Subcontractors/09_General/01_Prequalification/` | General CV |
| `1G-0007`, `1G-0008` (Arch DD 50% Gate 1F) | `02_Submittals/01_DD_Gate/Architecture/` | Design Gateway |

## New Key Senders

| Sender | Role | Priority |
|---|---|---|
| Francesco Bitelli (NRS) | Design Lead — CG Comments on Arch Submission Plan | High |
| Abdrabo Shahin | Design challenges, stakeholder coordination | Medium |
| Mohammed Ahmed | HSE — Lifting Gear Inspection Reports | Medium |
| Anwar Sadat | HSE — Lifting Gear Inspection Reports | Medium |
| Shihab Mohamed (Rawasin) | AV/IT — NETGEAR Prequalification | Medium |

## New Non-Project Filters

- Read AI meeting summaries (`Read Assistant` sender, `Read Meeting Report` subject)
- SPMS notifications (`[Samaya PMS]` prefix)
