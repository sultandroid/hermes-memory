# Weekly Email Archive Processing Workflow

Use this when processing sequential weekly email archives (`{week_no}.md`) 
produced by `download_mails.py` at `~/Documents/04_Outlook_Connection/mails/`.

## Overview

Each `.md` file contains 80-200 email threads with inline attachment references.
The goal is to find new (unfiled) attachments, copy them to correct BIM destinations,
and log the week's key events in PROJECT_MEMORY.md.

## Procedure

### Step 1: Check the source file

```bash
wc -l "mails/{week_no}.md"
grep "^## " "mails/{week_no}.md" | wc -l          # count email threads
grep -o 'attachments/[^)]*' "mails/{week_no}.md" | sort -u | wc -l  # unique attachments
```

### Step 2: Build the already-filed set

Python: walk all BIM destination trees and build a `set(f.lower())`:

```python
already = set()
for d in [ASEER, ZAMZAM, SAMAYA_DOCS]:
    for root, dirs, files in os.walk(d):
        for f in files:
            already.add(f.lower())
```

### Step 3: Find unfiled attachments

Extract attachment references from the `.md` file. For each:

1. URL-decode the path
2. Get basename, skip GUIDs (`{8}-{4}-{4}-{4}-{12}`), inline images (`imageNNN.*`, `Outlook-*`, `icons-*`), tiny files (< 1KB)
3. Check if basename.lower() is in `already`
4. Verify the actual file exists on disk (not just referenced)
5. Report what's still unfiled

### Pre-Flight: Locate the Download Script

The `download_mails.py` script exists in two possible locations:
- **Root level** (preferred, always present): `~/Documents/04_Outlook_Connection/download_mails.py`
- **Scripts subdirectory** (may or may not exist): `~/Documents/04_Outlook_Connection/scripts/download_mails.py`

Run the root-level version:
```bash
python3 ~/Documents/04_Outlook_Connection/download_mails.py
```

If the file returns `Resource deadlock avoided` (APFS `compressed,dataless`), use `rsync` to materialize first:
```bash
rsync ~/Documents/04_Outlook_Connection/download_mails.py /tmp/download_mails.py && python3 /tmp/download_mails.py
```

### Filing Targets: Attachment Subfolder → BIM Destination

After `download_mails.py` extracts attachments, they land in `mails/attachments/` sorted into 7 project subfolders (`aseer_museum/`, `zamzam_nwc/`, `general/`, `admin_hr/`, `haramein_ghamamah/`, `hoarding_signage/`, `makkah_jabal_omar/`). Each project subfolder has 8 categorized subdirs: `correspondence/`, `drawings_designs/`, `others/`, `proposals_contracts/`, `reports/`, `schedules/`, `site_photos/`, `technical_specifications/`.

Map both levels to BIM destinations:

#### Aseer-Museum: Subfolder → BIM Destination

| Attachment Subfolder | BIM Destination |
|---------------------|-----------------|
| `aseer_museum/correspondence/` | `Aseer-Museum/09_Correspondence/` or `Completed Tender Package From NRS/05_Correspondence_Archive/` |
| `aseer_museum/drawings_designs/` | `Aseer-Museum/Design Files/00_Scope_and_Proposals/` |
| `aseer_museum/reports/` | `Aseer-Museum/Reports & Meeting/00_Daily Reports/` |
| `aseer_museum/proposals_contracts/` | `Aseer-Museum/Subcontractors/<specific_sub>/` |
| `aseer_museum/schedules/` | `Aseer-Museum/Time Schedules/` |
| `aseer_museum/site_photos/` | `Aseer-Museum/Docs/00_Admin/99_Images/` |
| `aseer_museum/technical_specifications/` | `Aseer-Museum/Specs & Datasheet/` or `Completed Tender Package From NRS/04_Specifications_and_BOQ/` |
| `aseer_museum/others/` | Classify by filename keyword (see below) |

`others/` keyword rules: `StudioZNA`/`Aseer 2026` → `Design Files/00_Scope_and_Proposals/`; `AV Power`/`AV Racks` → `Docs/00_Admin/`; `Dogan Kozan` → `Subcontractors/`; `SI-CG` → `Correspondence/`; `Samaya BLK360` → `Specs & Datasheet/`.

#### Zamzam Museum: Subfolder → BIM Destination

| Attachment Subfolder | BIM Destination |
|---------------------|-----------------|
| `zamzam_nwc/correspondence/` | `Zamzam Museum/Docs/03_Inspection_Requests/` or `Zamzam Museum/Email_Archive/` |

#### PROJECT_MEMORY.md: Use the Hydrated Copy

The root `Aseer-Museum/PROJECT_MEMORY.md` is often a OneDrive cloud placeholder (EDEADLK). **The working copy lives at `Aseer-Museum/_Project_Memory/PROJECT_MEMORY.md`** — always attempt writes there first. If that is also locked, create companion files (`WEEK{N}_EMAIL_SUPPLEMENT.md`) at the same level (writes to OneDrive succeed even when reads fail).

### Step 4: File by document prefix

| Prefix | Destination |
|--------|-------------|
| `ZAM-` (Zamzam) | `Zamzam/Docs/` (or `03_Inspection_Requests/` for IR/MIR/MAR) |
| `MOC-MUS-ASE-` | `Aseer-Museum/Completed Tender Package From NRS/05_Correspondence_Archive/` |
| `MOC-ASEER-` | Same as above |
| `PL-` (HSE plans) | Aseer `05_Correspondence_Archive/` or project-specific |
| `ZD-` (General doc) | Aseer `05_Correspondence_Archive/` |
| `TQ-` (Query) | Aseer `05_Correspondence_Archive/` |
| `IR-` (Inspection) | Aseer `05_Correspondence_Archive/` |
| `PQ-` (Prequal) | Aseer `04_Specifications_and_BOQ/` |
| Daily/Weekly reports | Aseer `Reports & Meeting/` |
| Arabic-named certs (شهادة, رخصه, etc.) | `Samaya/Docs/SAMAYA-Formal-Docs/` |
| HR/personnel letters | Aseer `Docs/00_Admin/HR/` |
| Site photos (IMG_*, WhatsApp*) | Aseer `Docs/00_Admin/99_Images/` |
| Hoarding projects | Aseer `Docs/00_Admin/` |
| Datasheets/catalogues | Aseer `Docs/00_Admin/99_Images/` |
| Jabal Omar/Ghamama cross-refs | Aseer `Docs/00_Admin/` |

### Filing Targets — Additional Project Subdirectories

The download script also sorts attachments into these project subfolders. Use keyword-based routing when they lack explicit BIM target folders:

| Attachment Subfolder | Keywords → BIM Destination |
|----------------------|---------------------------|
| `haramein_ghamamah/` | `خير الخلق` → `Khair El-Khalq Museum/` ; `الغمامة` → `El-Ghamama Gift Shop/` ; `تجاليد وعلفات` → `El-Ghamama Gift Shop/` ; others → `Samaya/Docs/` for classification |
| `makkah_jabal_omar/` | `جبل عمر` → `Zamzam Museum/Docs/` or `Masjid Alnoor/Docs/` ; `مسجد النور` → `Masjid Alnoor/Docs/` ; `ورشة الراشدية` → `Makkah/` project area; `RAK` → `Zamzam Museum/Docs/` |
| `hoarding_signage/` | All → `Samaya/Docs/Signage_and_Hoarding/` (no dedicated BIM project tree yet) |
| `admin_hr/` | All → `Aseer-Museum/Docs/00_Admin/HR/` or `Samaya/Docs/HR/` |

### Detecting `compressed,dataless` files (macOS APFS)

Use `ls -lO` to see file flags:
```bash
ls -lO ~/Documents/04_Outlook_Connection/mails/attachments/*.pdf | grep dataless
```

Files with `compressed,dataless` flag have their content offloaded by macOS APFS compression. They show correct file sizes but every read attempt returns `Resource deadlock avoided`. Detection pattern:
- `ls -lO` shows `compressed,dataless` flags
- `file {path}` returns `ERROR: cannot read (Resource deadlock avoided)`
- `cat`, `cp`, `open()`, `os.open()` all fail with EDEADLK
- **Fix:** use `rsync` to copy to `/tmp/` first (Workaround A above)

### Step 5: Copy files (OneDrive/APFS-safe copy)

OneDrive cloud files and APFS `compressed,dataless` files fail consistently with `Resource deadlock avoided` (EDEADLK, errno 11) when using `cp`, `cat`, `ditto`, or `touch`+`cat`. Python's `os.open()` also fails. Three workarounds, tried in order:

**Workaround A — rsync (preferred):** `rsync` bypasses macOS File Provider locks because it uses a different I/O path through the VFS layer. Works on `compressed,dataless` APFS files that resist all other read attempts.

```bash
rsync "$src_path" "/tmp/$(basename "$src_path")" && cp "/tmp/$(basename "$src_path")" "$dest_path"
```

Note: The intermediate `/tmp/` copy is needed — `rsync` directly to the OneDrive destination may still deadlock if the destination has file-provider hooks. Copy to `/tmp/` first, then `cp` into place.

**Workaround B — os.open() bypass (OneDrive files only):** Python's low-level `os.open(path, os.O_RDONLY)` bypasses the Foundation file-coordination layer that OneDrive hooks into. Works for OneDrive cloud-placeholder files when `cat` and `open()` fail. **Does NOT work for APFS `compressed,dataless` files** (those still return EDEADLK). Use only for pure OneDrive lock scenarios.

```python
import os

fd = os.open(src_path, os.O_RDONLY)
data = os.read(fd, file_size)  # use stat to get size first
os.close(fd)

with open(dst_path, 'wb') as fout:
    fout.write(data)
```

**Workaround C — cat-to-tmp-then-mv (fallback):**
```bash
cat "$src" > "/tmp/$basename" && mv "/tmp/$basename" "$dest_path"
```

This reads the file in 4KB chunks, writes to non-OneDrive `/tmp/`, then moves into place.
**Note:** If even `cat` and `rsync` fail with `Resource deadlock avoided`, the NSFileProvider has an exclusive lock or the file is irrecoverably `compressed,dataless`. Retry on next pipeline cycle, or open the file in Finder to force materialization.

### Step 6: Extract key events from the week

For PROJECT_MEMORY.md, extract:

- **From/Date** of each CG/NRS/GBH email thread (>cg.com.sa, >nissenrichards, >glasbau-hahn)
- **Attachment names** — indicate what was submitted/returned
- **Meeting invites** with 🗓 / 🗓 prefix — these are Read AI meeting summaries
- **First body lines** — capture the action (submittal sent, response received, meeting scheduled)
- **CG response codes** (Code A/B/C/D) from attachment names or email body

### Step 7: Update PROJECT_MEMORY.md

Add a session update block at the end of the file:

```
## Session Update — {Date} (Week {N} Finished)

| Item | Detail |
|------|--------|
| **Action** | Processed week {N} email archive |
| **Source** | `{N}.md` — {lines} lines, {threads} threads, {attachments} attachments |
| **New files** | {count} filed ({dest summary}) |
| **Key events** | {bullet list of notable events} |
| **CG activity** | {summary of CG responses this week} |
| **NRS activity** | {any NRS coordination} |
```

### Step 8: Update Hermes memory

Replace the Aseer Museum entry to reflect the latest week processed.

## Common Filters (inline images to skip)

```python
# Skip GUID-only filenames
if len(name_no_ext) == 36 and '-' in name_no_ext: continue

# Skip auto-generated inline images
if re.search(r'^(image\d+|Outlook-|icons-|thumbnail_)', name_lower): continue

# Skip known web artifacts
if basename in ['d66938.webp']: continue

# Skip tiny files (email signature icons, spacing images)
if size < 1000: continue
```

## Notes

- Weeks 13+ are the "modern" weekly format from download_mails.py
- Earlier weeks (pre-13) use a different format and are not yet processed
- The already-filed set is case-insensitive — OneDrive can sync files with 
  different casing than the source attachment filename
- CG emails typically CG-REPLY-{doc}.pdf — extract code from the Classification 
  line or the response PDF filename, not the email subject
- Zamzam IR/MIR/MAR/WIR/SDR docs go to `Zamzam/Docs/03_Inspection_Requests/` 
  unless they're DOC-type, which go to `Zamzam/Docs/`
