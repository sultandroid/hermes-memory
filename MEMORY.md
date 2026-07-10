Aseer root: ~/Documents/Asher_Regional_Museum_Document_Control/. Doc codes: 1A0=Arch, 1E0=Elec, 1M0=Mech, 1K0=Gen. CG codes: A=Approved, B=Approved w/Comments, C=Revise&Resubmit.
§
Models: deepseek-v4-flash (default), deepseek-v4-pro (analysis), ministral-3:3b (structured).
§
OneDrive BIM path is the primary location for project files: ~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/. The Document Control folder (~/Documents/Asher_Regional_Museum_Document_Control/) is a working copy only. Always use OneDrive BIM path as the primary destination for new files.
§
Odoo timesheet unit_amount in minutes.
§
DOCX: patch sections only, never regenerate entire file.
§
Flowcharts: SVG via cairosvg. iAcoustics = guide only.
§
User expects actionable fixes not just critique — when structural issues identified, deliver corrected file (DOCX/HTML), not a report.
§
CG responses: respond as Samaya (unified contractor), never mention sub-consultant splits.
§
Cashout: exclude credit POs (Mada/Saba), force-include delivered-unpaid POs. Add [Cash Out Report NO YYYYMMDD] comment to each PO.
§
Aseer email triage 08-Jul: MEP SOW ZD-0068 Rev.01 submitted to CG, Arch 50% DD Basement Code C, Dust Control ZD-0076 Code C, Showcase 08.03_SC_01 omit per Yara, ZNA agreement ready, Time Extension LT-0027 pending, Abu Malha Palace protection needed.
§
Aseer PM repo at ~/aseer-museum-pm (github.com/sultandroid/aseer-museum-pm). Structure: 00_Status/project_status.md (generated from Odoo live sync), 01_Odoo_Mapping/task_mapping.md (full task tree), 01_Odoo_Mapping/status_to_odoo.md (cross-reference). Sync script at ~/.hermes/scripts/aseer-pm-status.py — reads all 347 Odoo tasks from Project 219, generates discipline health, deadlines, critical issues. Cron runs 4× daily (06/10/14/18 KSA).
§
Submission plan = forward schedule only. CR sheet holds explanations. Separate registers for separate scopes. Caveman style for responses.
§
When OneDrive locks files (Operation not permitted), use /Volumes/MIcro/Temp/ as working directory — copy files there, fix, then copy back to OneDrive.