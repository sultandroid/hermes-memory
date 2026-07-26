# Document Classification Guide — Aseer Museum Project Folders

When a user sends an arbitrary document (PDF, xlsx, docx, image) for the Aseer Museum project, classify it into the **Docs/** numbered folder system based on its content/purpose.

## Quick-Classification Table

| If Document Is About… | Destination | Example |
|---|---|---|
| Permits, licences, authority approvals | `06_Authority_Submissions/` | Heritage permit tracker, municipality NOC, Civil Defence approval |
| CG consultant correspondence | `11.1_To_From_CG/` | Email threads with Noman Siddiqui, Mansour Alrezeni |
| PMC consultant correspondence | `11.2_To_From_PMC/` | PMCM coordination letters |
| Internal Samaya memos/emails | `11.3_Internal_Samaya/` | Internal instructions, org changes |
| NRS/subcontractor correspondence | `11.4_NRS_and_Subs/` | Subcontractor submittals, vendor letters |
| Design deliverables (drawings, models) | `03_Submittals/` (or discipline subfolder under Submittals/) | Shop drawings, BIM models, design reports |
| RFIs | `04_RFIs/` | Technical queries to consultant |
| SIs (Site Instructions) | `05_SIs/` | Site observations, instructions |
| Reports & meeting minutes | `07_Reports/` or `08_Meeting_Minutes/` | Weekly reports, progress photos |
| Registers & trackers | `09_Registers/` | Risk register, submittal register, material tracker |
| Test & inspection records | `10_Test_and_Inspection/` | Material test reports, inspection requests |
| Compliance & audit | `12_Compliance_and_Audit/` | Compliance matrices, audit findings |
| Plans & procedures | `02_Plans_and_Procedures/` | DMP, BEP, PEP, HSE plan, PQP |
| Contracts & ERs | `01_Contracts_and_ER/` | Contract docs, scope of work, ER |
| Project charter | `00_Project_Charter/` | Project initiation docs |
| Time schedules | `Time Schedules/` (root level) | Primavera/xer schedules, milestone plans |
| Emails (raw .eml/.msg) | `Email_Archive/` (root level) | Raw inbox exports |
| Specs, datasheets, catalogues | `Specs & Datasheet/` (root level) | Product datasheets, material specs |

## Docs/ Numbered Subfolder Convention

The `Docs/` folder uses numbered prefixes for consistent ordering:

```
00_Project_Charter
01_Contracts_and_ER
02_Plans_and_Procedures
03_Submittals
04_RFIs
05_SIs
06_Authority_Submissions
  06.1_Saudi_Civil_Defense
  06.2_MOC
  06.3_MoMRAH_Municipality
  06.4_MOI_Security
  06.5_Heritage_Authority     ← created when needed
07_Reports
08_Meeting_Minutes
09_Registers
10_Test_and_Inspection
11_Correspondence
  11.1_To_From_CG
  11.2_To_From_PMC
  11.3_Internal_Samaya
  11.4_NRS_and_Subs
  11.X_ITC_Integrity_Technology
12_Compliance_and_Audit
99_Archive
99_Reference
```

**Rules:**
- To create a new sub-subfolder, follow the decimal numbering (e.g., `06.5_` after `06.4_`). Never use letters or abbreviations.
- Use descriptive English names with underscores for spaces.
- Date-prefix filenames for correspondence: `YYYY-MM-DD_Descriptive_Name.pdf`

## Authority Submissions — Authority-Specific Subfolders

| Code | Authority | When to Use |
|------|-----------|-------------|
| 06.1 | Saudi Civil Defense | Fire safety, evacuation, suppression |
| 06.2 | MoC (Ministry of Culture) | Heritage-related, museum content |
| 06.3 | MoMRAH / Municipality | Building permits, demolition, enabling works |
| 06.4 | MOI / Security | Security systems, access control |
| 06.5 | Heritage Authority | Heritage zone permits, restoration, facade |

## Correspondence — Counterparty-Specific Subfolders

| Code | Counterparty | When to Use |
|------|-------------|-------------|
| 11.1 | CG (Consultant) | Noman Siddiqui, Mansour Alrezeni, Sameh Elnaggar |
| 11.2 | PMC (Project Management Consultant) | PMCM coordination |
| 11.3 | Samaya Internal | Internal memos, org changes |
| 11.4 | NRS & Subcontractors | Subcontractor correspondence, vendor letters |
| 11.X | ITC / Integrity Technology | IT systems, AV/tech correspondence |

## Naming Convention

- **Correspondence PDFs:** `YYYY-MM-DD_Short_Description.pdf`
- **Registers / trackers:** `Aseer_Museum_<Name>.xlsx`
- **Submittal packages: follow existing discipline subfolder naming**
