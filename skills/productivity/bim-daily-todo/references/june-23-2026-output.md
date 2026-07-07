# June 23, 2026 — Zero-Register, Watchdog + Find Supplement

**Context:** Registers have no entries since May 28 (26 days stale). Zamzam CSV locked by OneDrive (hydrated but locked: 356KB on disk, `read_file` returned `total_lines=0, file_size=356832`). Zamzam mtime is April 10, 2026 (73 days stale).

## Data Sources Used

| Source | Status | Freshness |
|--------|--------|-----------|
| Aseer register | Readable — 285 rows, 46KB | May 28 (stale) |
| Zamzam CSV | Hydrated but locked (`read_file`: 0 lines, 356KB) | Apr 10 (very stale) |
| Aseer Watchdog state | Readable — 57K lines, 4.5MB | Mix of Apr-Jun 2026 |
| `find -newermt` (filesystem metadata) | Works on locked stubs | June 16-23 |

## Key Findings

### Zamzam (Last 7 Days, `find -mtime -7`)

- **Jun 22:** `ZAM-SAM-ZZ-MEC-MD-ARC-M.F-040-03a.rvt` — 401MB Revit ARCH model update (major)
- **Jun 20:** `Zamzam Museum - Ali Abdelrahman shared 1 item with_3005.eml` — shared document notification
- **Jun 17:** Ceiling lightbox .rfa files (×6: `lightbox8`, `lightbox8.0001`, `lightbox9`, `lightbox9.0002`, `lightbox10`, `lightbox10.0001`)

### Aseer Design Files (Last 7 Days, `find -mtime -7`)

- **Jun 22:** `RE: Urgent : Dry wall system .eml` (0 bytes syncing) — in Architecture/Freestanding_Walls/
- **Jun 21:** `Asser Mobilization Plan (MECH).eml` (0 bytes syncing) — in 00_Scope_and_Proposals/
- **Jun 18:** `6930_Aseer_FF&E Schedule.xlsx` — schedule update
- **Jun 18:** `Meged.pdf` — showcase types in 4_Showcase Types/
- **Jun 17:** `6930_Aseer_Graphic Schedule_rev A.xlsx` — schedule revision

### Watchdog Only: Aseer Design Files (Last 14 Days)

Files from Jun 9-11 not in 7-day window but notable for activity pulses:

- `34932_MOC-MUS-ASE-1A0-ZD-0033 Rev.01.pdf` (Jun 9)
- Electrical/Temp_Power/ — 7 sheets including `MOC-MUS-ASE-1E0-ZD-0042.pdf` (Jun 11)
- Electrical/CCTV/ — `MOC-MUS-ASE-1E0-ZD-0038.pdf` + `v2` (Jun 11)
- Life_Safety/ — `A2742-SK-01.pdf`, `LIFE SAFETY DRAWINGS.rar`, `A-02 As Built.pdf` (Jun 11)
- 3D_Visualization/External_Stairs/ — 6 drawings (Jun 11)
- Project_Query/ — `A2742-10.05-004.docx` + `v2` (Jun 11)

## Priority Classification Applied

| Source | HIGH | MEDIUM | LOW |
|--------|------|--------|-----|
| Aseer register (backlog) | RFQ Artec Spider, Showcase SDR, HSE plans | M&E coordination, HSE board, Temp power, SI-007 | Invoice, Weekly recaps |
| Zamzam find | — | Revit ARCH model (401MB) | .rfa families, shared .eml |
| Aseer find | — | FF&E Schedule, Graphic Schedule, Showcase Types | Dry wall .eml, Mobilization .eml |

## Output Strategy

Since the registers had zero entries in the 7-day window, the output:
1. Opened with a summary table showing 0 new entries
2. Pulled the most recent Open/Active items from the Aseer register backlog (May 23-28)
3. Flagged watchog findings (design files, Revit model) as actionable items
4. Added a note: "Registers show no new activity since May 28"
5. Capped at 11 items (under the 15 max)

## Diagnostic Note: `read_file` on Locked Hydrated Files

The Zamzam CSV (356KB on disk) produced this `read_file` output:
```
total_lines=0, file_size=356832, truncated=false
content: "1|"
```

This is the **hydrated but locked** pattern: bytes exist on disk (non-zero `file_size`) but the file system cannot serve the content because OneDrive holds an exclusive lock. The `"1|"` is `read_file`'s line-number prefix artifact from attempting to parse a locked binary stream.

Contrast with **dataless stub** (0 bytes, no content): both produce `Errno 11` on terminal reads but `read_file` distinguishes them via `file_size`.
