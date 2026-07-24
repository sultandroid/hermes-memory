# Pipeline Execution — 2026-07-23 19:00 KSA

## New Routing Patterns Discovered

| Filename Pattern | Correct Destination | Notes |
|-----------------|-------------------|-------|
| `ZD-0098` (EMDP and SDP Assessment Report) | `03_Design_Files/Electrical/EMDP_SDP_Assessment/` | New electrical assessment code — added to routing table |
| `PROJECT EXECUTION PLAN 01.docx` (no doc code) | `04_Docs/02_Plans_and_Procedures/02.2_Project_Execution_Plan/01_Source_Files/` | Keyword-based route needed — matches "PROJECT EXECUTION PLAN" |
| `TU-26184801` / `TU-26184802-03` / `TU-26184804` (MITSUBISHI chain block certs) | `24_Subcontractors/10_Rigging/01_Prequalification/` | TU- prefix = technical upload, route to Rigging prequal |
| `SMP_CR_Sheet_Rev01.xlsx` | `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` | SMP CR sheet — companion to SMP document |
| `Review Statement – Appendix T SMP Integration Workflows.pdf` | `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` | SMP review statement — companion to SMP |
| `Appendix T — SMP Integration Workflows _ Aseer Museum DMP.pdf` | `04_Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/` | SMP appendix — companion to SMP |
| `Executive Level Minutes Of Metting NO.02.pdf` | `00_Status/Meeting_Minutes/` | Keyword "Executive Level Minutes" |
| `Executive level minutes of meeting - Actions list.xlsx` | `00_Status/Meeting_Minutes/` | Same keyword, different format |
| `6930_Finishes_Schedule_rev A.pdf` | `24_Subcontractors/09_General/08_RFP_and_Proposals/` | Baffle Ceiling RFQ companion |
| `A2742-1910C.pdf` | `24_Subcontractors/09_General/08_RFP_and_Proposals/` | Baffle Ceiling RFQ companion |
| `TB for approval.pdf` | `03_Design_Files/Architecture/` | Title Block — keyword match |
| `Authorized Distributor Certificate - UAE 2026.pdf` | `24_Subcontractors/09_General/01_Prequalification/` | Netgear/MediaCast prequal companion |
| `GS324P_GS324PP_GS348PP.pdf` | `24_Subcontractors/09_General/01_Prequalification/` | Netgear/MediaCast prequal companion |
| `MediaCast FZ DPC License - Expiry 30 April 2027.pdf` | `24_Subcontractors/09_General/01_Prequalification/` | Netgear/MediaCast prequal companion |
| `gs724tpv2_gs724tpp.pdf` | `24_Subcontractors/09_General/01_Prequalification/` | Netgear/MediaCast prequal companion |
| `Molitor-20260628T081956Z-3-001.zip` | `24_Subcontractors/09_General/01_Prequalification/` | Molitor scope companion zip |

## Git Rebase + Post-Commit Hook Workaround

When `git pull --rebase` fails mid-rebase because the post-commit hook regenerates `06_Risk_System/webapp/src/index.html`:

```bash
# 1. Discard the auto-generated index.html
git checkout 06_Risk_System/webapp/src/index.html

# 2. Continue the rebase
git rebase --continue
```

The post-commit hook fires on every commit (including rebase commits), regenerating index.html. After each rebase step, the working tree has a dirty index.html. The fix is to `git checkout` it before each `git rebase --continue`.

If the rebase already aborted, redo with:
```bash
git checkout 06_Risk_System/webapp/src/index.html
git pull --rebase origin main
# If it fails again mid-rebase:
git checkout 06_Risk_System/webapp/src/index.html
git rebase --continue
# Repeat until rebase completes
```

## AppleScript -2700 Errors This Session

Emails that failed with -2700 (Outlook internal error, likely malformed attachment metadata):
- 49079 (Ali Abdelrahman — First Floor drawing issue)
- 49037 (Mohammad Elbaz — Site Survey)
- 49019 (Mohamed Samir — Weekly Progress Meeting)
- 48975 (Amro Mohammed — Weekly Progress Meeting)

All four had `.eml` attachments (forwarded messages) which are `message/rfc822` type — AppleScript cannot save these. The actual documents were extracted from the original emails (49066, 49088, etc.). This is consistent with the known `message/rfc822` limitation.

## Folder Path Corrections

The routing table had wrong paths for:
- ZD-0020 Stakeholder Plan: was `02.19_Stakeholder_Management_Plan` → corrected to `02.3_Stakeholder_Management_Plan`
- ZD-0081 Resource Plan: was `02.18_Resource_Management_Plan` → corrected to `02.2_Project_Execution_Plan`
