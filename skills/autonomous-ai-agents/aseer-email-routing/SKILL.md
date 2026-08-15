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
| 1A0-1G-0003 | Arch Material Board — Basement | `02_Submittals/01_DD_Gate/Architecture/` |
| 1A0-1G-0004 | Arch Material Board — LGF | `02_Submittals/01_DD_Gate/Architecture/` |
| 1A0-1G-0005 | Arch DD Drawings — Ground Floor | `02_Submittals/01_DD_Gate/Architecture/` |
| 1A0-1G-0006 | Arch Material Board — GF | `02_Submittals/01_DD_Gate/Architecture/` |
| 1A0-1G-0007 | — | `02_Submittals/01_DD_Gate/Architecture/` |
| 1A0-1G-0008 | — | `02_Submittals/01_DD_Gate/Architecture/` |
| 1A0-1G-0009 | Showcases DD 50% | `02_Submittals/01_DD_Gate/Architecture/` |
| 1A0-1G-0010 | Arch Viz 3D Shots — First Floor | `02_Submittals/01_DD_Gate/Architecture/` |
| 1A0-1G-0011 | Arch Viz 3D Shots — Ground Floor | `02_Submittals/01_DD_Gate/Architecture/` |
| 1C0-1G-0001 | Civil/Structural DD | `02_Submittals/01_DD_Gate/Civil/` |
| 1E0-1G-0002 | AV DD Drawings 50% Part II | `02_Submittals/01_DD_Gate/AV/` |
| 1M0-1G-0001 | MEP DD | `02_Submittals/01_DD_Gate/MEP/` |
| 1M0-1G-0002 | Plumbing DD 50% | `02_Submittals/01_DD_Gate/MEP/` |

### Prequalifications (PQ-*)

| Doc Code | Specialist | Destination |
|----------|------------|-------------|
| 1A0-PQ-0123 | ACOUSTIEG | `24_Subcontractors/11_Acoustic/01_Prequalification/` |
| 1A0-PQ-0124 | AME | `24_Subcontractors/18_Acoustic_Specialist/01_Prequalification/` |
| 1A0-PQ-0125 | JOCAVI | `24_Subcontractors/07_Acoustic/01_Prequalification/` |
| 1A0-PQ-0128 | TransOrient Solutions | `24_Subcontractors/06_Acoustic/01_Prequalification/` |
| 1A0-PQ-0136 | Furniture (Anaroque) | `24_Subcontractors/04_Setwork/01_Prequalification/` |
| 1A0-PQ-0137 | Setwork (Tannah) | `24_Subcontractors/04_Setwork/01_Prequalification/` |
| 1A0-PQ-0138 | Setwork (Saudi Emaar) | `24_Subcontractors/04_Setwork/01_Prequalification/` |
| 1A0-PQ-0139 | Setwork (BTT) | `24_Subcontractors/04_Setwork/01_Prequalification/` |
| 1C0-PQ-0120 | Civil/Structural | `24_Subcontractors/08_Civil_Structural/01_Prequalification/` |
| 1C0-PQ-0121 | Civil/Structural | `24_Subcontractors/08_Civil_Structural/01_Prequalification/` |
| 1C0-PQ-0131 | Rigging (ACT) | `24_Subcontractors/10_Rigging/01_Prequalification/` |
| 1C0-PQ-0132 | Rigging (AL FARIS) | `24_Subcontractors/10_Rigging/01_Prequalification/` |
| 1E0-PQ-0133 | ICT Security / Network Solutions (NETGEAR) | `24_Subcontractors/04_AV_IT_Contractor/01_Prequalification/` |
| 1E0-PQ-0134 | ICT Security / Audio Solutions (Molitor) | `24_Subcontractors/04_AV_IT_Contractor/01_Prequalification/` |
| 1E0-PQ-0135 | ICT Security (SPS) | `24_Subcontractors/04_AV_IT_Contractor/01_Prequalification/` |
| 1L0-PQ-0122 | Landscaping (Evergreen) | `24_Subcontractors/21_Landscaping_Specialist/01_Prequalification/` |
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
| ZD-0099 | DP-AC1 & MDP-AC Assessment Report | `03_Design_Files/Electrical/DP-AC1_MDP-AC_Assessment/` |
| ZD-0100 | Mechanical Submittal Plan | `04_Docs/02_Plans_and_Procedures/02.10_Subcontractor_Deliverables/01_Source_Files/02_PDFs/03_ZD-0100_Mechanical_Submittal/` |
| ZD-0101 | Lighting Base Design Report | `03_Design_Files/Electrical/Lighting_Design/` |
| ZD-0102 | Electrical Submission Plan — Gate 1 DD | `04_Docs/02_Plans_and_Procedures/02.2_Project_Execution_Plan/01_Source_Files/` |
| ZD-0103 | Earthing LPS Compliance Understanding Report | `03_Design_Files/Electrical/Earthing_Lightning/` |
| ZD-0104 | Design Phases Recovery Plan | `04_Docs/02_Plans_and_Procedures/02.2_Project_Execution_Plan/01_Source_Files/` |
| ZD-0105 | Generator Assessment | `03_Design_Files/Electrical/Generator_Assessment/` |
| ZD-0106 | AV / ICT Specialist | `03_Design_Files/AV/` |

### General Documents (ZD-*) — continued

| Doc Code | Description | Destination |
|----------|-------------|-------------|
| ZD-0084 | Active Component Assessment | `03_Design_Files/Electrical/Active_Component_Assessment/` |
| ZD-0078 | Wiring Devices Assessment | `03_Design_Files/Electrical/Wiring_Devices/` |
| ZD-0084 CG Response | CG response to Active Component Assessment (Code C) | `03_Design_Files/Electrical/Active_Component_Assessment/` |
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
| *CG Response*ZD-0084* or *CG Response*ZD-0086* | CG Response to PEP/Active Component | `04_Docs/02_Plans_and_Procedures/02.2_Project_Execution_Plan/02_CG_Responses/` |
| *CG Response*ZD-0093* or *CG Response*ZD-0094* | CG Response to RMP | `04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/02_CG_Responses/` |
| *CG Response*ZD-0090* | CG Response to MDP Assessment | `03_Design_Files/Electrical/Current_Condition_MDP/` |
| *CG Response*ZD-0099* | CG Response to DP-AC1 Assessment | `03_Design_Files/Electrical/DP-AC1_MDP-AC_Assessment/` |
| *SMP_CR_Sheet* or *Review Statement*SMP* or *Appendix T*SMP* | SMP Companion Docs | `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` |
| *SOR-* or *HSE SOR* | Safety Observation Report | `04_Docs/10_Test_and_Inspection/10.3_NCRs/{SOR-ID}/` |
| *Water Leakage*Safety* | Electrical Water Leakage Safety Report | `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` |
| *Lighting Control* or *Lighting_Control_Zones* | Lighting Control Protocol | `03_Design_Files/Electrical/Lighting_Control/` |
| *Daily_Report* or *Daily Report* | Daily Report | `00_Status/Daily_Reports/` |
| *WEEKLY* | Weekly Report | `00_Status/Weekly_Reports/` |
| *.xer | Schedule | `02_Schedule/` |
| *WEEKLY* | Weekly Report | `00_Status/Weekly_Reports/` | Leakage*Safety* | Electrical Water Leakage Safety Report | `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` |
| *Lighting Control* or *Lighting_Control_Zones* | Lighting Control Protocol | `03_Design_Files/Electrical/Lighting_Control/` |
| *Daily_Report* or *Daily Report* | Daily Report | `00_Status/Daily_Reports/` |
| *WEEKLY* | Weekly Report | `00_Status/Weekly_Reports/` |
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
| *CG Response*ZD-0084* or *CG Response*ZD-0086* | CG Response to PEP/Active Component | `04_Docs/02_Plans_and_Procedures/02.2_Project_Execution_Plan/02_CG_Responses/` |
| *CG Response*ZD-0093* or *CG Response*ZD-0094* | CG Response to RMP | `04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/02_CG_Responses/` |
| *CG Response*ZD-0090* | CG Response to MDP Assessment | `03_Design_Files/Electrical/Current_Condition_MDP/` |
| *CG Response*ZD-0099* | CG Response to DP-AC1 Assessment | `03_Design_Files/Electrical/DP-AC1_MDP-AC_Assessment/` |
| *SMP_CR_Sheet* or *Review Statement*SMP* or *Appendix T*SMP* | SMP Companion Docs | `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` |
| *SOR-* or *HSE SOR* | Safety Observation Report | `04_Docs/10_Test_and_Inspection/10.3_NCRs/{SOR-ID}/` |
| *Water Leakage*Safety* | Electrical Water Leakage Safety Report | `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` |
| *Lighting Control* or *Lighting_Control_Zones* | Lighting Control Protocol | `03_Design_Files/Electrical/Lighting_Control/` |
| *Daily_Report* or *Daily Report* | Daily Report | `00_Status/Daily_Reports/` |
| *WEEKLY* | Weekly Report | `00_Status/Weekly_Reports/` |
| *.xer | Schedule | `02_Schedule/` |
| *WEEKLY* | Weekly Report | `00_Status/Weekly_Reports/` | Leakage*Safety* | Electrical Water Leakage Safety Report | `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` |
| *Lighting Control* or *Lighting_Control_Zones* | Lighting Control Protocol | `03_Design_Files/Electrical/Lighting_Control/` |
| *Daily_Report* or *Daily Report* | Daily Report | `00_Status/Daily_Reports/` |
| *WEEKLY* | Weekly Report | `00_Status/Weekly_Reports/` |
| *WEEKLY* | Weekly Report | `00_Status/` |
| *.xer | Schedule | `02_Schedule/` |
| *KPI_Dashboard* or *Material Tracker* | KPI / Material Tracker | `04_Docs/09_Registers/22_Procurement_Schedule/MEP_Materials/` |
| *Molitor* | Molitor SOW | `24_Subcontractors/14_Molitor/01_Scope_of_Work/` |
| *INV-* or *Invoice* | Invoice | `00_Contracts/Invoices/` |
| *INV-4883* or *NRS*Invoice* | NRS Invoice (Stage 5 off-site fabrication) | `18_Invoices/NRS/` |
| *الجدول* or *Door*Inspection* | Door Inspection Table (Woodworks) | `24_Subcontractors/03_Woodworks_Door/01_Prequalification/` |
| *ARIVAL NOTICE* or *Arrival Notice* | Shipment Arrival Notice | `00_Status/Logistics/` |
| *MVii* or *Scale Model* | Scale Models | `24_Subcontractors/12_Scale_Models/01_Prequalification/` |
| *Baffle* or *Ceiling* | Ceiling RFQ | `04_Docs/09_Registers/22_Procurement_Schedule/` |
| *3D*Scanner* or *Faro* | 3D Scanning | `24_Subcontractors/13_3D_Scanning/01_Prequalification/` |
| *Door_BOQ* | Door BOQ | `03_Design_Files/Architecture/Door_Schedule/` |
| *Compliance_Sheet* | Compliance Sheet | `04_Docs/09_Registers/22_Procurement_Schedule/` |
| *LT-003* or *MOC-MUS-ASE-LT* | Letter / Warning | `04_Docs/09_Correspondence/` |
| *SMP* or *Sustainability* | Sustainability Plan | `04_Docs/02_Plans_and_Procedures/02.2_Project_Execution_Plan/01_Source_Files/` |
| *KAF*MAT* or *Al Watania* | Material Submittal | `04_Docs/09_Registers/22_Procurement_Schedule/MEP_Materials/` |
| *ZNA* or *عقد* | Contract | `00_Contracts/` |
| *MATERIAL-BOARD* | Material Board | `03_Design_Files/FF&E_Material_Boards/` |
| *ELECT/COMPLIANCE* or *BMR* | Compliance Understanding Report | `03_Design_Files/Electrical/Compliance_Reports/` |
| *BMS* or *GITCO* | BMS System Design | `03_Design_Files/Mechanical/BMS/` |
| *Fire Fighting* | Fire Fighting Systems | `03_Design_Files/Mechanical/Fire_Fighting/` |
| *Long Lead*Mechanical* | Long Lead Mechanical Items | `03_Design_Files/Mechanical/Long_Lead_Items/` |
| *DS02* or *Audit Report* | NRS Audit Report | `03_Design_Files/Architecture/Audit_Reports/` |
| *GBH Letter* | Showcases Contractor Correspondence | `24_Subcontractors/05_Showcases_Contractor/06_Correspondence/` |
| *TransOrient* or *TOSRMP* | Acoustic Specialist SOW | `24_Subcontractors/03_Acoustic_Specialist/01_Scope_of_Work/` |
| *Executive Level Minutes* or *MOM* | Weekly Progress Meeting Minutes | `04_Docs/08_Meeting_Minutes/08.1_Weekly_Coordination/` |
| *Scenography* | Scenography Workshop | `04_Docs/08_Meeting_Minutes/08.3_Workshops/` |
| *Civil_Defense* | Civil Defense Requirements | `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` |
| *Design_Phase_Deliverables_Tracker* | Design Deliverables Tracker | `04_Docs/09_Registers/01_Design_Deliverables_Tracker/` |
| *Calibration*Report* | Calibration Reports | `00_Status/Calibration_Reports/` |

## Email Intel — cross-project intelligence layer (hermes-memory)

Separate from the per-project routing above. Lives in `~/hermes-memory/email_intel/` (hub repo, NOT a project repo). It is the **analyst**; the Mac/Outlook agent is only the **sensor** (exports emails, never analyzes).

- Layout: `inbox/*.md` (one per email), `contacts.json`, `projects.json`, `behavior/sender_profiles.json`, `threads/THREAD-*.md`, `issues/ISSUE-NNN.md`. MD/JSON only — no binaries, no Excel.
- Scripts: `scripts/email_intel_agent.py` (pipeline: ingest→classify→route→behavior→thread→issues) and `scripts/email_intel_backfill.py` (reads `email_scan_*.md` reports). Run `--run` for full pipeline, `--issues` to list open issues.
- **The scan-report backfill only reaches back to when the `email_scan_*.md` reports start (mid-July).** To backfill further (e.g. to April), pull directly from the Outlook SQLite DB — see `references/email-intel-outlook-backfill.md` for the recipe and the `scripts/email_intel_outlook_backfill.py` importer.
- **Issue detector is keyword-based and over-raises.** It flags any email containing urgent/please/action/confirm as "reply-required" (306 of 318 issues in one run). Treat the issue list as raw flags needing a triage pass against the project registers — do NOT report them as verified action items.

### READ-THE-CONTENT RULE (user correction 2026-08-15)

**Metadata-only email processing is NOT acceptable.** The user explicitly rejected classifying emails by subject/sender alone: *"No we have to read and understand for updating registers and projects … also we have to read and understand attached."* A scan that only logs subjects, routes files, and writes a review log is a FAILED run. For every project-critical email you must:

1. **Read the actual body** — `Message_Preview` is truncated (~255–500 chars). For full content use AppleScript `plain text content of msg` (see `outlook-email` skill) or `.olk15Message` body extraction. CG codes, instructions, and action requests may live in the forwarded/quoted body below the preview.
2. **Read the attachments** — extract and read CG response PDFs (Code C/D especially), contracts, SOWs, comment sheets. The register-driving content (reviewer comments, rejection reasons, approval conditions) is in the attachments, not the subject.
3. **Update the actual registers** — submittal, prequalification, letters, invoice, si, risk, action_items — with the understood content, not just note "email received."
4. **Process in batches of ~10** — read 10 emails (bodies + attachments), update registers, commit, then the next 10. The user explicitly asked for this cadence ("make it 19 mails by 10 mails and take your time"). Do not try to bulk-process hundreds in one pass.

**Pitfall — backfill inbox files are header-only.** The `email_intel/inbox/*.md` files created by the backfill importer contain ONLY `From/Subject/Date/Project` — no body, no attachments (median ~350 bytes). They are a metadata index, NOT readable content. Do not claim you "read" emails from these files. To actually read, pull from Outlook SQLite (`Message_Preview`) or AppleScript (`plain text content`).

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
| Mohammad Elbaz | CG Senior Electrical Engineer — lighting, electrical design | Medium |
| Anwar Sadat | HSE — Safety Observation Reports, Lifting Gear Inspection | Medium |lbaz | CG Senior Electrical Engineer — lighting, electrical design | Medium |
| Anwar Sadat | HSE — Safety Observation Reports, Lifting Gear Inspection | Medium |

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
- **Git rebase + post-commit hook conflict.** The repo's post-commit hook regenerates `06_Risk_System/webapp/src/index.html` after every commit. During `git pull --rebase`, each rebase step fires the hook, leaving a dirty index.html that blocks the next step. See `references/git-rebase-post-commit-hook.md` for the full recovery procedure.
- **Files without doc codes in their names** (e.g. "PROJECT EXECUTION PLAN 01.docx", "TB for approval.pdf") need keyword-based routing rules, not doc-code regexes. Add a keyword pattern alongside the doc-code pattern for the same destination.
- **TU- prefix files** (e.g. TU-26184801) are technical uploads from subcontractors — route to the relevant subcontractor's prequal folder, not a general location.
- **Two-pass routing for large batches.** When extracting 20+ files, write a primary script for this session's files and a separate stranded-cleanup script for orphaned files from prior cycles. See `references/two-pass-routing.md`.
- **`00_Contracts/` is git-hook protected.** The repo has a pre-commit hook that blocks any commit touching `00_Contracts/`. If `git add -A` picks up contract files (e.g. from a sibling agent's work), `git commit` fails with `BLOCKED: Commit modifies protected 00_Contracts/ files.` Fix: `git reset HEAD 00_Contracts/` before committing. The contract files remain on disk — they just aren't committed.
- **`patch` with `replace_all=true` on table rows can duplicate.** When adding new rows to a markdown table register, the old_string may match both the original row AND the newly added rows (because `replace_all` replaces every occurrence). This creates duplicate rows. Fix: always use a unique old_string with enough surrounding context (previous row + next row) to match exactly once. Never use `replace_all=true` on table rows in registers.
