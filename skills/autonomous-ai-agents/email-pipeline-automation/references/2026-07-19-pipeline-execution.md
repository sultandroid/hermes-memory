# Pipeline Execution — 2026-07-19

## Context
- Cron-run, no user present
- SQLite accessible (Unix epoch confirmed)
- 48h scan window: 17 Jul 14:00 – 19 Jul 05:30

## Scan Results
- 55 project-relevant emails identified
- 42 non-image attachments extracted from 31 emails
- 42/42 routed to project folders
- 20+ non-project items filtered out

## Key Routing Decisions

| Doc Code | Classification | Destination |
|----------|---------------|-------------|
| MOC-MUS-CG-ASE-1KN-SE-021 | NCR (Safety Instruction) | `10.3_NCRs/SE-021_Unsafe_Hot_Work/` |
| MOC-MUS-ASE-1KH-PL-02.17 | Risk Management Plan | `02.17_Risk_Management_Plan/01_Source_Files/` |
| MOC-MUS-ASE-1A0-1G-0003/4/5/6 | DD Gate — Architecture | `02_Submittals/01_DD_Gate/Architecture/` |
| MOC-MUS-ASE-1C0-1G-0001 | DD Gate — Civil | `02_Submittals/01_DD_Gate/Civil/` |
| MOC-MUS-ASE-1M0-1G-0001 | DD Gate — MEP (HVAC) | `02_Submittals/01_DD_Gate/MEP/` |
| MOC-MUS-ASE-1E0-ZD-0088/90/91 | Electrical Assessments | `03_Design_Files/Electrical/{Assessment}/` |
| MOC-MUS-ASE-MEP-ZD-0067 Rev.01 | Fire Alarm/Suppression | `03_Design_Files/MEP/Fire_Alarm_Suppression/` |
| MOC-MUS-ASE-1K0-ZD-0082 | Sustainability Mgmt Plan | `02.5_HSE_Plan/01_Source_Files/` |
| MOC-MUS-ASE-1K0-ZD-0086 | Project Execution Plan | `02.2_Project_Execution_Plan/01_Source_Files/` |
| MOC-MUS-ASE-1A0-ZD-0085 | Graphics Specialist SOW | `24_Subcontractors/04_Graphics_Graphite/01_Scope_of_Work/` |
| MOC-MUS-ASE-1K0-ZD-0087 | Mechanical Engineer CV | `24_Subcontractors/05_Mechanical_Engineer/01_Scope_of_Work/` |
| PQ-0120/0121 | Materials Testing Lab | `24_Subcontractors/01_Materials_Testing_Lab/` |
| PQ-0122 | Landscaping — Evergreen | `24_Subcontractors/02_Landscaping/` |
| PQ-0124 | Acoustic — AME | `24_Subcontractors/03_Acoustic_AME/` |
| Door Technical Review | Door/Joinery | `03_Design_Files/Architecture/Door_Schedule/` |
| Rigging.rar | Rigging Specialist | `24_Subcontractors/06_Rigging/` |
| INV-4863 | Invoice | `00_Contracts/Invoices/` |
| Technology BOQ | ICT | `03_Design_Files/ICT/` |
| GBH Letter (Patinated Brass) | Material Finish Testing | `03_Design_Files/FF&E_Material_Boards/` |
| NRS Reference PDF | Architecture Reference | `03_Design_Files/Architecture/Reference/` |

## Errors Encountered
1. **Email 48580** — attachment filename contained `/` ("Re: MOC-MUS-ASE-MEP-ZD-0067 Rev.01 / Fire Alarm..."). `touch` created a directory instead of a file. The `.pdf` attachment from the same email extracted fine; only the `.eml` copy failed.
2. **Email 48547** — Outlook returned error -2700 (generic). Skipped, not retried. Landscape proposal was already extracted from email 48546.
3. **AppleScript ~700-byte limit** — initial scripts with filename sanitization (text item delimiters + repeat loop) exceeded the limit. Simplified to minimal scripts without sanitization.

## Registers Updated
- NCR Register: No change (SE-021 already listed)
- Risk Register: No change (PRR-HSE-01 already references SE-021)
- Review log: `03_Plans/08_Risk/reviews/email_scan_2026-07-19.md`

## Action Items Flagged
1. Risk Management Plan needs Waris's signature before CG submission
2. NCR SE-021 (Unsafe Hot Work) due 01-Aug — HSE Manager action
3. Acoustic Specialist prequalifications (AME, JOCAVI, ACOUSTIEG) pending review
4. Graphics Specialist SOW CG-approved — proceed with procurement
5. Door Technical Review from Johnny-Klein needs response
6. Electrical assessments (ATS, MDP, Earthing) — route to design team for review
