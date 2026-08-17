# Design Phase Deliverables Tracker — Overdue Monitoring + Email Cross-Reference

The CG's `Design Phase Deliverables Tracker*.xlsx` is the **authoritative granular
source** for per-deliverable design submission status (real drawing numbers
`MOC-ASE-...-DDD-XXXX`, per-deliverable status, forecast dates). The master
submission tracker (`02_Schedule/submission_tracker.md`) is a coarser summary.
When the user asks "what's overdue in <discipline>", read the CG tracker, not the
summary.

## Sheet structure (12-08-2026 version)

11 sheets: `Design Deliverables Tracker` (dashboard) + 10 discipline detail sheets:
`Arch Deliverables`, `STR Deliverables `, `Mech Deliverables `, `AV Deliverables`,
`scenography Deliverables`, `BIM Model Deliverables`, `Electrical Deliverables`,
`Exhibition Lighting Deliverable`, `Low Current & ICT Deliverables `,
`SHOWCASES Deliverables  `.

**Note the trailing spaces in sheet names** (`Mech Deliverables `, `Low Current &
ICT Deliverables `, `SHOWCASES Deliverables  `) — openpyxl sheet lookup is
exact-match, so the script's `SHEET_LABELS` must carry the exact names.

Two sheet layouts exist:
- **Electrical / Low Current / Exhibition Lighting** — wide format: `Gate |
  Level/Zone | Discipline | Submission Category | Drawing Package/Item |
  Submission Description | Responsibility | Revision | Forecast | Status | Prep |
  Submitted | Approved% | ...`. Section headers (e.g. "Earthing, Bonding, Surge &
  Lightning Protection System") are merged rows with no forecast/status.
- **AV / Showcases / BIM / Scenography / Arch / Mech / Str** — narrow format:
  `# | P6 Activity ID | Discipline | Floor/Zone | Drawing No. | Drawing Title |
  Revision | Date Submitted | Forecast | Status | Prep | Submitted | Approved%`.

The header row is NOT always row 1 — the script scans rows 1-5 for a row
containing "forecast"/"status"/"drawing" and uses that as the header.

## Pitfalls

- **`Submitted.` (trailing period) is a DONE status.** The CG sheet writes
  "Submitted." with a period. If `DONE_STATUS` only has `"submitted"`, every
  submitted item is misclassified as overdue. Include `"submitted."`.
- **Electrical sheet has a corrupted dimension** (`A1:XFD16384`). Iterating
  `ws.iter_rows()` over the full width explodes output (millions of cells).
  Always cap columns at 15 when dumping, and in the parser only read columns
  1-15.
- **Section-header rows repeat titles.** Merged category rows (e.g. "Cable
  Containment System") carry a title but no forecast/status. The parser skips
  rows with no forecast date OR no status — but a header row that happens to
  have a status cell can slip through. Filter by checking the title against
  known header phrases if needed.
- **Forecast dates are `datetime` cells** — `_parse_date` must handle
  `datetime`, `date`, and string forms (`%Y-%m-%d`, `%d/%m/%Y`, `%d.%m.%Y`,
  `%d-%m-%y`).
- **Prep% is a 0-1 float** (0.6 = 60%). Format as `{v*100:.0f}%`.

## Email cross-reference workflow (which overdue items got cleared)

After generating the overdue report, cross-check Outlook for new submittals that
clear overdue items:

1. Query Outlook SQLite for the last 24-48h of Aconex transmittals and submittal
   emails:
   ```sql
   SELECT datetime(Message_TimeReceived,'unixepoch','localtime'),
          Message_NormalizedSubject, Message_SenderList
   FROM Mail
   WHERE Message_TimeReceived > strftime('%s','now','-2 days')
     AND Message_IsOutgoingMessage=0
     AND (Message_NormalizedSubject LIKE '%WTRAN%'
          OR Message_NormalizedSubject LIKE '%TRANSMIT%'
          OR Message_NormalizedSubject LIKE '%Submittal%'
          OR Message_NormalizedSubject LIKE '%DD%')
   ORDER BY Message_TimeReceived DESC;
   ```
2. Match Aconex `SIC.-WTRAN-000NNN (WF-000NNN)` subjects against the overdue
   list. A new transmittal for a package that was overdue = **cleared**.
3. Update `01_Registers/submittal_register.md` with the new submittal row
   (ref, date, `**Submitted**`, Aconex ref, "clears the overdue X package").
4. Commit + push.

**Example (2026-08-17):** Fire Alarm & Detection 50% DD was overdue (forecast
15-Aug, 60% prep on the 12-08 tracker). Email `SIC.-WTRAN-000181 (WF-000254)
Fire Alarm & Detection System 50% Detailed Design - EL` arrived 17-Aug → cleared.
Also `Smoke Management System Layout` (MEP/HVAC) submitted via link.

## Cron

A daily cron (`design-tracker-daily-status`, 08:00) runs
`python3 scripts/design_tracker_overdue.py` and delivers the report. The script
auto-finds the newest tracker xlsx in `~/.hermes/cache/documents`, `~/Desktop`,
`~/Downloads`, OneDrive, and the repo — so a new CG tracker dropped into cache
is picked up automatically without editing the cron.
