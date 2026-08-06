# Pipeline Execution — 05 Aug 2026 (Evening)

## Context

Morning scan (19:30) had extracted 44+ attachments to `/tmp/email_attachments/` but **not routed them to OneDrive**. This session completed the routing and updated registers.

## Key Finding

The routing script from the morning scan was never run. Attachments sat in `/tmp/email_attachments/` with no OneDrive copies. This is a recurring risk — the pipeline's extraction step runs but the routing step can be skipped if the session ends early.

## Routing Script Used

`/tmp/route_aseer_attachments.py` — a keyword-based routing script that matched filenames against known doc codes and keyword patterns. 44 files routed.

## New Doc Codes Added to Routing Table

| Doc Code | Destination |
|----------|-------------|
| ZD-0100 | `Subcontractor_Deliverables/01_Source_Files/02_PDFs/03_ZD-0100_Mechanical_Submittal/` |
| ZD-0101 | `Electrical/Lighting_Design/` |
| ZD-0102 | `PEP/01_Source_Files/` |
| ZD-0103 | `Electrical/Earthing_Lightning/` |
| ZD-0104 | `PEP/01_Source_Files/` |
| ZD-0105 | `Electrical/Generator_Assessment/` |
| ZD-0106 | `AV/` |
| ZD-0078 | `Electrical/Wiring_Devices/` |
| ZD-0084 | `Electrical/Active_Component_Assessment/` |
| PQ-0136/7/8/9 | `Setwork/01_Prequalification/` |
| 1M0-1G-0002 | `Submittals/01_DD_Gate/MEP/` |
| 1A0-1G-0009 | `Submittals/01_DD_Gate/Architecture/` |

## New Keyword Patterns Added

| Pattern | Destination |
|---------|-------------|
| ELECT/COMPLIANCE or BMR | `Electrical/Compliance_Reports/` |
| BMS or GITCO | `Mechanical/BMS/` |
| Fire Fighting | `Mechanical/Fire_Fighting/` |
| Long Lead*Mechanical | `Mechanical/Long_Lead_Items/` |
| DS02 or Audit Report | `Architecture/Audit_Reports/` |
| GBH Letter | `Showcases_Contractor/06_Correspondence/` |
| TransOrient or TOSRMP | `Acoustic_Specialist/01_Scope_of_Work/` |
| Executive Level Minutes or MOM | `Meeting_Minutes/08.1_Weekly_Coordination/` |
| Scenography | `Meeting_Minutes/08.3_Workshops/` |
| Civil_Defense | `HSE_Plan/01_Source_Files/` |
| Design_Phase_Deliverables_Tracker | `Registers/01_Design_Deliverables_Tracker/` |
| Calibration*Report | `Calibration_Reports/` |

## Action Items Added

8 new items to `00_Status/action_items.md`:
- Review NRS Submissions (Audit Report 02, SMP Rev.01, First Floor drawings)
- Respond to GBH Letter 003
- Download Stage 4 Showcase Lighting Package (WeTransfer)
- Identify alternative setwork supplier (PQ-0138 Code D)
- Revise & resubmit PQ-0136 Anaroque (Code C)
- Verify CG response on ZD-0084 Rev.02
- Verify CG response on ZD-0089 Rev.01
- Review Samaya Factory Papers
- Review Mechanical Design Drawings Resubmission
- Review Long Lead Mechanical Items Replacement

## Git

Commit `c82d88f` pushed to `sultandroid/aseer-museum-pm`. Post-commit hook regenerated index.html; `git checkout --` + `git push` after rebase.
