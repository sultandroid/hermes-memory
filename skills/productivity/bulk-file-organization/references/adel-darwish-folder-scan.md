# Adel Darwish Folder Scan — Daily Report Processing

Recurring workflow triggered by the `check_adel_files.sh` cron (runs daily at 9:00, 17:00). The cron detects new/changed files in Adel's OneDrive folder but does NOT read them — the agent must process each file.

## Trigger

Cron output lists new/changed files in:
```
Adel Darwish's files - 01- Execution Documents/04- Daily Report/<Month> <Year>/
```

## Workflow

### 1. Hydrate one file at a time

All files in Adel's folder are OneDrive cloud-only placeholders (0 blocks on disk). Batch operations fail with `Resource deadlock avoided`.

```bash
ADEL_DIR="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Adel  Darwish's files - 01- Execution Documents/04- Daily Report/05- May 2026"

for f in "Daily Report 13-05-2026.pdf" "Daily Report 14-05-2026.pdf"; do
  echo "Opening: $f"
  open -a Preview "$ADEL_DIR/$f"
  sleep 20
  blocks=$(stat -f "%b" "$ADEL_DIR/$f")
  echo "  Blocks: $blocks"
done
```

**Critical:** One file at a time. Never batch. Each needs 15-20s for OneDrive to hydrate.

### 2. Extract text

```bash
pdftotext -layout "$ADEL_DIR/$f" "/tmp/${f%.pdf}.txt"
```

Reports are Arabic/English mixed. Key sections to extract:
- **Header**: Date, report number, project stats (elapsed days, remaining, % complete)
- **Manpower tables**: Consultant team (6 staff), Contractor team (12-13), HVAC/BMS workers (10)
- **Work description**: "بيان باالعمال الجارية باملوقع" section — lists ongoing and planned activities
- **Safety notes**: "مالحظات" / "Safety Notes" section
- **Sign-off**: Who signed (Adel Darwish or Mohamed Samir)

### 3. Update the daily report register

File: `aseer-museum-pm/01_Registers/daily_report_register.md`

Add new entries with:
- Date, report number, prepared by
- Key activities (translated from Arabic)
- Manpower counts
- Issues/notes (especially persistent items like temp fence banner)

**Register structure** (Markdown table, not Excel):

| # | Date | Report No | Prepared By | Key Activities | Manpower (Contractor) | Issues / Notes |
|---|------|-----------|-------------|----------------|----------------------|----------------|

Include:
- **Pre-existing reports** already in the folder (not new) — mark as "Pre-existing" in activities
- **Weekend/holiday gaps** — add rows with "Fri (weekend)" or "Holiday" so the date sequence is complete
- **Sign-off changes** — note when the signatory changes (e.g., Adel Darwish → Mohamed Samir at report 107)
- **Persistent issues** — flag if the same issue appears across multiple reports (e.g., temp fence banner pending)
- **Project stats** from the header (elapsed days, remaining, % complete, target date)

### 4. Check for reporting gaps

After processing the current month's reports, check if subsequent month folders exist and have content:

```bash
ls -la "/path/to/next-month-folder/"
```

If folders exist but are empty, add a **Gap Analysis** section to the register:

| Period | Reports | Status |
|--------|---------|--------|
| May 2026 | 21 reports | Consistent |
| Jun 2026 | 0 | **GAP** — no reports for N days |
| Jul 2026 | 0 | **GAP** — no reports for N days |

Flag the gap prominently — the user needs to follow up with the site team.

### 4. Known patterns in these reports

| Field | Typical Value |
|-------|-------------|
| Report numbers | Sequential (101, 102, 103...) |
| Sign-off transition | Adel Darwish → Mohamed Samir (happened at report 107, 20-May) |
| Persistent issue | Temp fence banner pending owner approval |
| Work evolution | Early month: HVAC/BMS assessment → Late month: Mobilization, TBT, floor protection |
| Weekend | Fri — no reports |
| Project stats | 53.8% elapsed (163/303 days), 140 remaining, target 30-Sep-2026 |

### 5. Pitfalls

- **OneDrive deadlock**: `cp`, `cat`, `head`, `dd`, `brctl download` all fail on cloud-only placeholders. Only `open -a Preview` reliably hydrates.
- **Preview leaves app open**: After hydration, Preview stays running. Close it or leave it — doesn't affect subsequent operations.
- **Arabic text extraction**: `pdftotext -layout` works but produces right-to-left artifacts. Read the work description section carefully — it's the most informative part.
- **Report gaps**: Check for missing dates (weekends, holidays). Don't flag as errors.
