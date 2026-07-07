# Compare & File: Attachment-to-BIM Pipeline

Script: `~/Documents/04_Outlook_Connection/scripts/compare_and_file.py`

## Purpose
After `download_mails.py` downloads emails and classifies attachments into project subfolders (`attachments/aseer_museum/`, `attachments/zamzam_nwc/`, etc.), this script compares the attachments against the BIM folder contents on OneDrive and copies any new files.

## Project Mapping

| Project | Source subfolder | BIM target folder |
|---------|-----------------|-------------------|
| Aseer Museum | correspondence/ | `Aseer-Museum/Completed Tender Package From NRS/05_Correspondence_Archive` |
| Aseer Museum | technical_specifications/ | `Aseer-Museum/Completed Tender Package From NRS/04_Specifications_and_BOQ` |
| Aseer Museum | reports/ | `Aseer-Museum/Reports & Meeting/00_Daily Reports` |
| Aseer Museum | drawings_designs/ | `Aseer-Museum/Design Files/00_Scope_and_Proposals` |
| Aseer Museum | site_photos/ | `Aseer-Museum/Docs/00_Admin/99_Images` |
| Aseer Museum | schedules/ | `Aseer-Museum/Completed Tender Package From NRS/05_Correspondence_Archive` |
| Aseer Museum | proposals_contracts/ | `Aseer-Museum/Design Files/00_Scope_and_Proposals` |
| Zamzam NWC | correspondence/ | `Zamzam Museum/Docs/03_Inspection_Requests` |

## Key Technique: Coping with iCloud Dataless Files

Files under `~/Documents/04_Outlook_Connection/mails/attachments/` are on iCloud-synced storage and may have the APFS `dataless` flag. Shell commands (`cp`, `ditto`) fail with `fcopyfile: Resource deadlock avoided` (EDEADLK, errno 11).

**Solution:** Python's `shutil.copy2()` uses `open()` + `read()` + `write()` instead of the `fcopyfile()` syscall, bypassing the iCloud coordination lock:

```python
import shutil
shutil.copy2(src_path, dst_path)
```

## Running

```bash
cd ~/Documents/04_Outlook_Connection && python3 scripts/compare_and_file.py
```

## Filename Comparison

- Case-insensitive comparison
- Arabic Unicode normalization (Alef variants → ا, Yeh variants → ي, diacritic stripping U+064B–U+0652)
- `.DS_Store` files are always excluded
