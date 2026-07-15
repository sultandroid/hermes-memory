# Pipeline Execution Log — 2026-07-14

Reference file for the first production run of the email pipeline. Shows actual patterns, files, and routing decisions.

## Scan Results

153 emails across 6 folders in 48h window. 13 project-critical attachments extracted.

## Attachments Extracted & Routed

| Email ID | File | Sender | Routed To |
|---|---|---|---|
| 48345 | ACOUSTIEG Company Profile + Certificates | Mohamed Samir | 24_Subcontractors/18_Acoustic_Specialist/01_Prequalification/ |
| 48343 | CG-REPLY MOC-MUS-CG-ASE-NC-1KH-009.pdf | Hossam Mabrouk (CG) | 04_Docs/10_Test_and_Inspection/10.3_NCRs/NC-009_Debris_Chute/ |
| 48342 | Specialists and Designers Tracking & Action.xlsx | Mohamed Samir | 00_Status/ |
| 48336 | MOC-ASE-AR-ARC-LGF-DDD-1211-00.pdf + CGs.xlsx | Hossam Mabrouk (CG) | 02_Submittals/01_DD_Gate/Architecture/ |
| 48331 | Mechanical Material List.xlsx | Amro Mohammed | 04_Docs/09_Registers/22_Procurement_Schedule/MEP_Materials/ |
| 48319 | ZNA Samaya Consultancy Agreement FINAL.pdf | PM Waris | 24_Subcontractors/02_Lighting_Designer/02_Contract/ |
| 48318 | AME Acoustic Proposal.pdf | Mohamed Samir | 04_Docs/09_Registers/22_Procurement_Schedule/AME_Acoustic/ |
| 48037 | ACOUSTIEG Prequal (same as 48345) | Soliman Obiya | 24_Subcontractors/18_Acoustic_Specialist/01_Prequalification/ |
| 48041 | AME Acoustic Proposal (same as 48318) | Soliman Obiya | 04_Docs/09_Registers/22_Procurement_Schedule/AME_Acoustic/ |
| 48136 | Graphics_Specialist_Scope_of_Work.pdf | Sultan Issa (sent) | 24_Subcontractors/03_Graphics_Contractor/01_Scope_of_Work/ |
| 48209 | Aseer_Museum_Consolidated_Risk_Register (3).xlsx | PM Waris | 04_Docs/09_Registers/23_Project_Risk_Register/ |
| 48167 | MOC-MUS-ASE-1KH-PL-02.17_Risk_Management_Plan.docx | PM Waris | 04_Docs/02_Plans_and_Procedures/02.17_Risk_Management_Plan/ |

## Key Routing Patterns Used

- **Duplicate detection**: Same file from 2 senders (48345+48037, 48318+48041) — route both, same destination
- **Aconex notifications** (WTRAN-*): No attachments, skip — CDE-based transmittals
- **OneDrive writes**: Use Python `shutil.copy2()`, NOT terminal `cp` — special chars in paths (parentheses, spaces) break bash
- **Attachments with inline images**: Filter out `image/*` content types
- **Batch AppleScript**: Write `.applescript` to disk, run via `osascript`, handles ~10 emails in <30s

## Register Updates Applied

- `ncr_register.md`: Created with NC-1KH-009 (Open)
- `risk_register.md`: Bumped to C07 with 33 risks
- `email-pipeline-automation` skill: Created

## Cron Job Config

- Schedule: every 3h
- Delivery: Telegram
- Skills: outlook-email, email-pipeline-automation, github
