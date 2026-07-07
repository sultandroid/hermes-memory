# BIM Email Pipeline — Execution Reference (v2.33)

Running the pipeline as LEADER (cron job):

## Sequence

1. **Check Outlook** — `osascript -e 'tell app "System Events" to (name of processes) contains "Microsoft Outlook"'`
2. **Download mails** — `cd ~/Documents/04_Outlook_Connection && python3 scripts/download_mails.py`
   - Silent exit code 0 = no new emails
   - Any output = new mail processed into `mails/<N>.md`
   - Check `mails/pipeline_run_*.md` for the latest run state
3. **Delegated comparison** — Always delegate to **Codex** (`codex exec`). Provide:
   - Source: `~/Documents/04_Outlook_Connection/mails/attachments/`
   - Target base: `/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/`
   - Full target subfolder list (see below)
   - Instruction: `unicodedata.normalize('NFC', name)` on Arabic filenames before comparison
   - Copy: `cp -p` new files; verify they landed
4. **PROJECT_MEMORY check** — Main file at: `Aseer-Museum/_Project_Memory/PROJECT_MEMORY.md` inside OneDrive BIM Unit
   - Check `mails/PROJECT_MEMORY_WEEK*_UPDATE.md` for prepared updates
5. **Log** — Write run summary to `mails/pipeline_run_YYYY-MM-DD_HH-MM.md`

## Target BIM Subfolder Mappings

```
base=/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit

# Aseer Correspondence
$base/Aseer-Museum/Completed Tender Package From NRS/05_Correspondence_Archive/
  ← aseer_museum/correspondence/

# Aseer Specs & BOQ
$base/Aseer-Museum/Completed Tender Package From NRS/04_Specifications_and_BOQ/
  ← aseer_museum/technical_specifications/

# Aseer Daily Reports
$base/Aseer-Museum/Reports & Meeting/00_Daily Reports/
  ← aseer_museum/reports/

# Aseer Proposals
$base/Aseer-Museum/Design Files/00_Scope_and_Proposals/
  ← aseer_museum/proposals_contracts/

# Aseer MEP Contractor
$base/Aseer-Museum/Subcontractors/14_MEP_Contractor/
  ← aseer_museum/others/ (MEP-related files only)

# Aseer Images
$base/Aseer-Museum/Docs/00_Admin/99_Images/
  ← aseer_museum/site_photos/ + aseer_museum/drawings_designs/ (images/PDFs)

# Zamzam Inspection Requests
$base/Zamzam Museum/Docs/03_Inspection_Requests/
  ← zamzam_nwc/correspondence/ (files with IR in name)
```

## Pitfalls

### macOS OneDrive "Resource deadlock avoided"
When reading files inside the OneDrive-synced `Bim Unit/` folder:
- `head`, `cat`, `file`, `md5` → may fail with "Resource deadlock avoided"
- `cp -p` → fails on extended attributes (xattr) but **data is written correctly** — the file lands despite the error
- **Python** `open()` and **cp data** work fine; only metdata ops (xattr, md5, `file` magic) are affected
- Workaround: use `cp` without `-p`, or Python's `shutil.copy2` to write files
- When verifying a file was copied, check `ls -l` exists; don't use `md5` or `file` on the target

### Download script not at root
The download script is at `scripts/download_mails.py`, not at `~/Documents/04_Outlook_Connection/download_mails.py`. Always use the `scripts/` prefix.

### Pipeline run files are append-only
Each run creates `pipeline_run_YYYY-MM-DD_HH-MM.md`. Check the most recent one for the last run's state, don't overwrite them.
