---
name: aseer-email-routing
description: "Document-code-based routing rules for Aseer Museum email attachments — maps MOC-MUS-ASE doc codes to project folder destinations. Reference table for email pipeline automation."
tags:
  - aseer
  - routing
  - document-codes
  - email
  - pipeline
---

# Aseer Museum Email Routing Reference

Document-code-based routing rules for the Aseer Museum project. Maps MOC-MUS-ASE document codes to destination folders under `/Volumes/MIcro/Work/Aseer-Museum/`.

## Trigger

- Extracting email attachments and need to know where to file them
- Setting up or updating a routing script
- Classifying a new document type for the first time

## Document Code Format

`MOC-MUS-ASE-{DISC}{NUM}-{TYPE}-{SEQ}`

| Discipline Code | Discipline |
|----------------|------------|
| 1A0 | Architecture |
| 1C0 | Civil |
| 1E0 | Electrical |
| 1KH | HSE |
| 1K0 | General/Multi |
| 1M0 | Mechanical |
| 1KN | Security/ICT |
| 1L0 | Landscaping |

## Routing Table

### Design Gateway Submittals (1G-*)

| Doc Code | Destination |
|----------|-------------|
| 1A0-1G-0003 | `02_Submittals/01_DD_Gate/Architecture/` |
| 1A0-1G-0004 | `02_Submittals/01_DD_Gate/Architecture/` |
| 1A0-1G-0005 | `02_Submittals/01_DD_Gate/Architecture/` |
| 1A0-1G-0006 | `02_Submittals/01_DD_Gate/Architecture/` |
| 1A0-1G-0007 | `02_Submittals/01_DD_Gate/Architecture/` |
| 1A0-1G-0008 | `02_Submittals/01_DD_Gate/Architecture/` |
| 1A0-1G-0007 | `02_Submittals/01_DD_Gate/Architecture/` |
| 1A0-1G-0008 | `02_Submittals/01_DD_Gate/Architecture/` |
| 1C0-1G-0001 | `02_Submittals/01_DD_Gate/Civil/` |
| 1M0-1G-0001 | `02_Submittals/01_DD_Gate/MEP/` |

### Prequalifications (PQ-*)

| Doc Code | Specialist | Destination |
|----------|------------|-------------|
| 1A0-PQ-0123 | ACOUSTIEG | `24_Subcontractors/11_Acoustic/01_Prequalification/` |
| 1A0-PQ-0124 | AME | `24_Subcontractors/03_Acoustic_AME/01_Prequalification/` |
| 1A0-PQ-0125 | JOCAVI | `24_Subcontractors/07_Acoustic/01_Prequalification/` |
| 1A0-PQ-0128 | TransOrient Solutions | `24_Subcontractors/06_Acoustic/01_Prequalification/` |
| 1C0-PQ-0120 | Civil/Structural | `24_Subcontractors/08_Civil_Structural/01_Prequalification/` |
| 1C0-PQ-0121 | Civil/Structural | `24_Subcontractors/08_Civil_Structural/01_Prequalification/` |
| 1L0-PQ-0122 | Landscaping | `24_Subcontractors/03_Landscaping/01_Prequalification/` |
| 1L0-PQ-0126 | Landscaping (PINE) | `24_Subcontractors/03_Landscaping/01_Prequalification/` |
| 1L0-PQ-0127 | Landscaping (TLC) | `24_Subcontractors/03_Landscaping/01_Prequalification/` |

### General Documents (ZD-*)

| Doc Code | Description | Destination |
|----------|-------------|-------------|
| ZD-0020 | Stakeholder Management Plan Rev.03 | `04_Docs/02_Plans_and_Procedures/02.3_Stakeholder_Management_Plan/01_Source_Files/` |
| ZD-0067 | Fire Alarm & Suppression | `03_Design_Files/Electrical/Fire_Alarm_Suppression/` |
| ZD-0081 | Resource Management Plan | `04_Docs/02_Plans_and_Procedures/02.18_Resource_Management_Plan/01_Source_Files/` |
| ZD-0082 | Sustainability Management Plan | `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` |
| ZD-0085 | Graphics Specialist SOW | `24_Subcontractors/04_Graphics_Graphite/01_Scope_of_Work/` |
| ZD-0086 | Project Execution Plan | `04_Docs/02_Plans_and_Procedures/02.2_Project_Execution_Plan/01_Source_Files/` |
| ZD-0087 | Mechanical Engineer CV/Replacement | `24_Subcontractors/05_Mechanical_Engineer/01_Scope_of_Work/` |
| ZD-0088 | Electrical ATS Assessment | `03_Design_Files/Electrical/ATS_Assessment/` |
| ZD-0089 | Electrical Containment Assessment | `03_Design_Files/Electrical/Containment_Assessment/` |
| ZD-0090 | Electrical MDP Assessment | `03_Design_Files/Electrical/Current_Condition_MDP/` |
| ZD-0091 | Electrical Earthing Assessment | `03_Design_Files/Electrical/Earthing_Lightning/` |
| ZD-0092 | Electrical UPS Assessment | `03_Design_Files/Electrical/UPS_Assessment/` |
| ZD-0093 | Risk Management Plan | `04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/01_Source_Files/` |
| ZD-0094 | Subcontract Management Plan | `04_Docs/02_Plans_and_Procedures/02.18_Subcontract_Management_Plan/01_Source_Files/` |
| ZD-0095 | QA/QC CV (Aftab Adeel) | `24_Subcontractors/09_General/01_Prequalification/` |
| ZD-0096 | Architectural Title Block Template | `03_Design_Files/Architecture/Title_Block/` |
| ZD-0097 | MCC Assessment Report | `03_Design_Files/Electrical/MCC_Assessment/` |
| ZD-0098 | EMDP and SDP Assessment Report | `03_Design_Files/Electrical/` |

### General Documents (ZD-*) — continued

| Doc Code | Description | Destination |
|----------|-------------|-------------|
| ZD-0088/89/90/91/92 | Electrical Assessment (ATS/Containment/MDP/Earthing/UPS) | `03_Design_Files/Electrical/{AssessmentName}/` |
| ZD-0093 | Risk Management Plan | `04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/01_Source_Files/` |
| ZD-0095 | QA/QC CV | `24_Subcontractors/09_General/01_Prequalification/` |
| ZD-0096 | Architectural Title Block Template | `03_Design_Files/Architecture/` |

### Plans (PL-*)

| Doc Code | Description | Destination |
|----------|-------------|-------------|
| PL-02.17 | Risk Management Plan | `04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/01_Source_Files/` |
| PL-0046 | HSE Plan | `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` |
| ZD-0081 | Resource Management Plan | `04_Docs/02_Plans_and_Procedures/02.2_Project_Execution_Plan/01_Source_Files/` |
| ZD-0020 | Stakeholder Management Plan | `04_Docs/02_Plans_and_Procedures/02.3_Stakeholder_Management_Plan/01_Source_Files/` |

### Other Document Types

| Type | Description | Destination |
|------|-------------|-------------|
| TQ-* | Technical Query | `03_Design_Files/{Discipline}/` |
| IR-* | Inspection Request | `04_Docs/03_Inspection_Requests/` |
| NC-* / NCR | Non-Conformance Report | `04_Docs/10_Test_and_Inspection/10.3_NCRs/{NCR-ID}/` |
| SE-* | Safety Instruction | `04_Docs/10_Test_and_Inspection/10.3_NCRs/` |
| NRS Comments_*.xlsx | CG Comments on Submission Plan | `02_Submittals/01_DD_Gate/Architecture/` |
| *Mechanical Submission Plan*.xlsx | Mechanical Submission Plan | `02_Submittals/01_DD_Gate/MEP/` |
| *Lifting Gear Inspection* | HSE Inspection | `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` |
| *Design_Tracker*.xlsx | Design Tracker | `03_Design_Files/` |
| *stakeholder* | Stakeholder List | `00_Status/` |
| *lookahead* | Lookahead | `00_Status/` |
| *Prequalification_Submission_CG* | Prequal Submission | `24_Subcontractors/03_Acoustic_AME/01_Prequalification/` |
| *RE CG*IR-0001* | CG Response to Inspection Request | `04_Docs/10_Test_and_Inspection/10.2_Inspection_Requests/` |
| *RE CG*ZD-0091* or *RE CG*ZD-0092* | CG Response to Electrical Assessment | `03_Design_Files/Electrical/` |
| *SMP_CR_Sheet* or *Review Statement*SMP* or *Appendix T*SMP* | SMP Companion Docs | `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` |
| *SOR-* or *HSE SOR* | Safety Observation Report | `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` |
| *Evergreen*Prequal* | Landscaping Prequal (Evergreen) | `24_Subcontractors/03_Landscaping/01_Prequalification/` |
| *Daily_Report* or *Daily Report* | Daily Report | `00_Status/Daily_Reports/` |
| *WEEKLY* | Weekly Report | `00_Status/` |
| *Archaeological Museums* | AV/IT Proposal | `24_Subcontractors/AV_IT/08_RFP_and_Proposals/` |
| *MediaCast* or *GS324P* | AV/IT Prequal | `24_Subcontractors/AV_IT/01_Prequalification/` |
| *Calibration Certificates* | Calibration Docs | `04_Docs/09_Registers/22_Procurement_Schedule/` |
| *Lighting_Submittal_Register* | Lighting Submittal | `04_Docs/09_Registers/22_Procurement_Schedule/` |
| *Technology BOQ* | Technology BOQ | `04_Docs/09_Registers/22_Procurement_Schedule/` |
| *QT-SGL* | Lab Prequal (Rayat Alnajah) | `24_Subcontractors/01_Materials_Testing_Lab/01_Prequalification/` |
| *Rigging* | Rigging Contractor | `24_Subcontractors/10_Rigging/01_Prequalification/` |
| *Aseer -Package 2* | Rigging Package | `24_Subcontractors/06_Rigging/01_Prequalification/` |
| *TFP_Engineering* | Engineering Design Check | `00_Contracts/` |
| *AD Engineering* or *AGREEMENT* | MEP Agreement | `00_Contracts/` |
| *DESIGN CALCULATION*ASIR* | Drywall Design Calc | `24_Subcontractors/08_Civil_Structural/01_Prequalification/` |
| *Drywall Compliance* | Drywall Compliance Sheet | `02_Submittals/01_DD_Gate/` |
| *ASM_Ceiling_Systems_Compliance* | Ceiling Compliance | `02_Submittals/01_DD_Gate/` |
| *Equipment 00[1-3]* | HSE Equipment Docs | `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` |
| *6930_Finishes_Schedule* or *A2742-M60* | Paint/Finishes Samples | `03_Design_Files/FF&E_Material_Boards/` |
| *MA-0006*CR_Sheet* | Material CR Sheet | `03_Design_Files/FF&E_Material_Boards/` |
| *Asir Museum*Hesham*Outlook* | Hesham Outlook Export | `00_Status/` |
| *Asir Project-Mechanical Submission Plan* | Mechanical Submission Plan | `02_Schedule/` |
| *Rehabilitate*Schedule* | Updated Schedule | `02_Schedule/` |
| *Main stakeholders* | Stakeholder List | `00_Status/` |
| *Design_Tracker* | Design Tracker | `03_Design_Files/` |
| *NRS Comments* | CG Comments on Submission Plan | `02_Submittals/01_DD_Gate/` |
| *RE CG*IR-0001* | CG Response to Inspection Request | `04_Docs/10_Test_and_Inspection/10.2_Inspection_Requests/` |
| *RE CG*ZD-0091* or *RE CG*ZD-0092* | CG Response to Electrical Assessment | `03_Design_Files/Electrical/` |
| *SMP_CR_Sheet* or *Review Statement*SMP* or *Appendix T*SMP* | SMP Companion Docs | `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` |
| *SOR-* or *HSE SOR* | Safety Observation Report | `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` |
| *Evergreen*Prequal* | Landscaping Prequal (Evergreen) | `24_Subcontractors/03_Landscaping/01_Prequalification/` |
| *Daily_Report* or *Daily Report* | Daily Report | `00_Status/Daily_Reports/` |
| *WEEKLY* | Weekly Report | `00_Status/` |
| *.xer | Schedule | `02_Schedule/` |
| *ZNA* or *عقد* | Contract | `00_Contracts/` |
| *MATERIAL-BOARD* | Material Board | `03_Design_Files/FF&E_Material_Boards/` |

## Key Senders

| Sender | Role | Priority |
|--------|------|---------|
| Hossam Mabrouk | CG (PMC) — NCRs, design reviews, submittal responses | High |
| Muhammad Waris Sultan Khan | Project Director — directives, deadlines, contracts | High |
| Mohamed Samir | Construction Manager — coordination, procurement, prequal | High |
| Hesham Abdelhameed | Design submittals, daily reports, material boards | High |
| Francesco Bitelli (NRS) | Design Lead — CG Comments on Arch Submission Plan | High |
| Jim Richards | CG Requests — Scenography & Material Board | High |
| Maged Zamzam | URGENT Resubmission Requests | High |
| Soliman Obiya / Shihab Mohamed | Rawasin (AV/IT subcontractor) — proposals, prequal | Medium |
| Aconex Notification | CDE transmittals — document submissions | Medium |
| Amro Mohammed | MEP — material lists, technical | Medium |
| Ali Abdelrahman | RFQ, procurement, ceiling systems | Medium |
| Mohammed Ahmed | HSE — lookahead reports, lifting gear inspections | Medium |
| Mohammed Elshaikh | Plans (PEP, recovery plans) | Medium |
| Abdrabo Shahin | Design challenges, stakeholder coordination | Medium |
| Anwar Sadat | HSE — Lifting Gear Inspection Reports | Medium |

## Non-Project Filters (skip these)

- Saudi Wood Expo, Instagram, Cognito Forms, Bluebeam Events
- Power Automate reminders, FJDynamics webinars
- Visitor registration, car/vehicle requests, rest house rental
- ERP notifications (salary, tickets, leave, POs)
- SharePoint link notifications
- Read AI meeting summaries (`Read Assistant` sender)
- SPMS notifications (`[Samaya PMS]` prefix)
- Promotional/conference invitations

## Pitfalls

- **Subcontractor folder numbering drifts.** `24_Subcontractors/` has multiple folders for the same specialist (e.g. 02_Landscaping, 06_Landscaping, 07_Landscaping, 50_Landscaping). Always `ls 24_Subcontractors/` and pick the correct numbered folder before routing.
- **Use document-code patterns, not email-ID prefixes.** Routing rules must be based on doc codes (e.g. `ZD-0085`), not email IDs (e.g. `48608_`). Email IDs change every scan cycle.
- **CG Comments (NRS Comments_*.xlsx)** go to `02_Submittals/01_DD_Gate/Architecture/` — they are CG review feedback on the submission plan, not a separate document type.
- **Prequalification_Submission_CG.docx** from Soliman Obiya (AME/Rawasin) goes to `AME_Acoustic/01_Prequalification/`, not the general prequal folder.
- **Zamzam project files** (ZAM-NWC prefix) route to `/Volumes/MIcro/Work/Zamzam-Visitor-Center/`, not Aseer-Museum.
- **Git rebase + post-commit hook conflict.** The repo's post-commit hook regenerates `06_Risk_System/webapp/src/index.html` after every commit. During `git pull --rebase`, each rebase step fires the hook, leaving a dirty index.html that blocks the next step. **Workaround:** `git checkout 06_Risk_System/webapp/src/index.html` before each `git rebase --continue`. If the rebase aborted, redo with `git checkout index.html && git pull --rebase origin main` and repeat the checkout before each continue.
- **Files without doc codes in their names** (e.g. "PROJECT EXECUTION PLAN 01.docx", "TB for approval.pdf") need keyword-based routing rules, not doc-code regexes. Add a keyword pattern alongside the doc-code pattern for the same destination.
- **TU- prefix files** (e.g. TU-26184801) are technical uploads from subcontractors — route to the relevant subcontractor's prequal folder, not a general location.
