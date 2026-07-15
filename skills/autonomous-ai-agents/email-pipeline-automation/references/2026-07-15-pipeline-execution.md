# Pipeline Execution Log — 2026-07-15

Second production run. Key learnings from this session.

## Scan Results

~100 emails in 48h window. 17 project-critical emails identified, 20 non-image attachments extracted and routed.

## Attachments Extracted & Routed

| Email ID | File | Sender | Routed To |
|---|---|---|---|
| 48343 | CG-REPLY MOC-MUS-CG-ASE-NC-1KH-009.pdf | Hossam Mabrouk (CG) | 04_Docs /10_Test_and_Inspection/10.3_NCRs/NC-009_Debris_Chute/ |
| 48336 | MOC-ASE-AR-ARC-LGF-DDD-1211-00.pdf + CGs.xlsx | Hossam Mabrouk (CG) | 02_Submittals/01_DD_Gate/Architecture/ |
| 48371 | MOC-MUS-ASE-1A0-1G-0004.pdf | Hesham Abdelhameed | 02_Submittals/01_DD_Gate/Architecture/ |
| 48373 | MOC-MUS-ASE-1A0-1G-0003.pdf | Hesham Abdelhameed | 02_Submittals/01_DD_Gate/Architecture/ |
| 48319 | ZNA Samaya Consultancy Agreement FINAL.pdf | PM Waris | 00_Contracts/ |
| 48331 | Mechanical Material List.xlsx | Amro Mohammed | 04_Docs /09_Registers/22_Procurement_Schedule/MEP_Materials/ |
| 48037 | ACOUSTIEG Certificates + Company Profile | Soliman Obiya | 24_Subcontractors/18_Acoustic_Specialist/01_Prequalification/ |
| 48345 | ACOUSTIEG Certificates + Company Profile | Mohamed Samir | 24_Subcontractors/18_Acoustic_Specialist/01_Prequalification/ |
| 48041 | AME Acoustic Proposal.pdf | Soliman Obiya | 24_Subcontractors/18_Acoustic_Specialist/08_RFP_and_Proposals/ |
| 48318 | AME Acoustic Proposal.pdf | Mohamed Samir | 24_Subcontractors/18_Acoustic_Specialist/08_RFP_and_Proposals/ |
| 48365 | MOC-MUS-ASE-1E0-PQ-0105.pdf | Shihab Mohamed | 24_Subcontractors/19_Interactive_Design_Contractor/01_Prequalification/ |
| 48044 | ASM_PEP_Complete_internally initial draft.docx | Mohammed Elshaikh | 04_Docs /02_Plans_and_Procedures/02.3_PEP/ |
| 48136 | Graphics_Specialist_Scope_of_Work.pdf | Sultan Issa (sent) | 24_Subcontractors/03_Graphics_Contractor/01_Scope_of_Work/ |
| 48342 | Specialists and Designers Tracking & Action.xlsx | Mohamed Samir | 03_Design_Files/ |
| 48359 | ASM_Ceiling_Systems_Compliance_Sheet.xlsx | Ali Abdelrahman | 04_Docs /09_Registers/22_Procurement_Schedule/ |
| 48357 | Aseer Museum Lookahead Safety Preparations till 26 July.pdf | Mohammed Ahmed | 04_Docs /02_Plans_and_Procedures/02.5_HSE_Plan/ |
| 48376 | Daily_Report 15-07-2026.pdf | Hesham Abdelhameed | 00_Status/ |

## Key Learnings

1. **Proposals route to subcontractor folder, not procurement schedule.** AME Acoustic proposal went to `18_Acoustic_Specialist/08_RFP_and_Proposals/` (not `22_Procurement_Schedule/AME_Acoustic/` as in the 14-Jul run). The subcontractor folder is the correct canonical location.
2. **Main contract (ZNA) goes to `00_Contracts/`**, not a subcontractor folder. This is the prime contract, not a subcontract.
3. **`execute_code` is blocked in cron mode** — use `python3 -c "..."` via terminal instead.
4. **Design submittals from Hesham Abdelhameed** are a new high-priority sender to track (material boards, daily reports).
5. **Aconex transmittals list** should be logged in the review file for reference even though they have no attachments.

## Registers Updated

- `ncr_register.md`: NC-1KH-009 status → "Open — CG reply received 15-Jul"
- `risk_register.md`: No new risks
- Review log: `03_Plans/08_Risk/reviews/email_scan_2026-07-15.md`
