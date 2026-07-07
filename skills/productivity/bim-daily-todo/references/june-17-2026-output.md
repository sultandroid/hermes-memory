# June 17, 2026 — Daily TODO Session

## Context
- Registers had NO entries in last 7 days (Aseer CSV latest: May 28)
- Zamzam CSV permanently locked (OneDrive Errno 11 "Resource deadlock avoided")
- Aseer Project_Log equally stale (last entries ~May 26)
- Aseer email summary markdown files readable but stale (May 28)
- Watchdog was the ONLY viable data source

## Watchdog State
- **Aseer**: 138 file changes tracked in `Design Files/` folder (June 10-14)
  - Large batch of A2742 drawings on June 11 (~80 files)
  - RFPs/quotations on June 12 (3D laser scanners, structural design)
  - RFIs (007-011) submitted on June 11
  - Life Safety Drawings (rar) on June 11
  - SI-CG-ASEER-007 Rev.02 on June 10
  - New files in `00_Scope_and_Proposals/` subfolder — cross-project items
- **Zamzam**: 0 recent entries in watchdog
  - One Zamzam reference found in Aseer Scope_and_Proposals (Quotation NO.3451)

## Cross-Project Detection
Files from `00_Scope_and_Proposals/` under Aseer Design Files may contain items for Zamzam or other projects. In this session, a Zamzam quotation was found there. Always scan Aseer watchdog paths for "Zamzam" strings and vice versa.

## Output Format Used
- Single-line format (items short enough to fit)
- Arabic text for actions
- Legend emoji dropped from [Project] tag for brevity
- 14 items total (4 HIGH + 7 MEDIUM + 3 LOW)
- Note about stale registers included at bottom

## Key Filtering Applied
- 138 watchdog events → ~40 meaningful groups → 14 final items
- Major filter: collapse A2742 sheet batch (~80 files) into single LOW item
- Major filter: collapse RFIs into single group item (007-011)
- Major filter: collapse quotations into 2 groups (structural design, 3D scanners)
