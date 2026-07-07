# Attachment Categorization Rules (Un-Coded Files)

For email attachments that lack a standard document code prefix (PL-, ZD-, ZAM-, etc.), use this decision tree to route to the correct BIM destination.

## Principle

Classify by **content type** first, then **project affiliation**. When the filename gives no project hint, default to Samaya Admin.

## Scan ALL Locations — Not Just Root

The `download_mails.py` script creates categorized subfolders under `attachments/`. Files can be in TWO places:

1. **Root of attachments/** (flat) — uncategorized files
2. **Subfolders** — files sorted by the download script:
   - `attachments/schedules/` — time schedules, milestone updates
   - `attachments/correspondence/` — CG replies, letters, transmittals
   - `attachments/drawings_designs/` — drawings, 3D models, design files
   - `attachments/proposals_contracts/` — scope docs, fee proposals, contracts
   - `attachments/reports/` — daily/weekly reports, BMS reports
   - `attachments/site_photos/` — site inspection photos, construction images
   - `attachments/technical_specifications/` — datasheets, brochures, certs
   - `attachments/others/` — catch-all miscellany

**Scan both root AND all subfolders.** The subfolder classification by the download script is a starting hint, not authoritative — always verify the file belongs where the subfolder suggests.

## Decision Tree (Priority Order)

### 1. Zamzam Museum (prefix check)
Any filename containing `ZAM-`, `ZVC-`, `Zamzam`, `زمزم`, `P0639`, `P083`, `EGEC` → **Zamzam Museum/Docs/** (or `Docs/03_Inspection_Requests/` for IR/MIR/MAR forms)

Sub-rules for Zamzam:
- `DOC-AR/GN/STR/CONT` → `Docs/` (general documents)
- `IR-ME/STR/AR` → `Docs/03_Inspection_Requests/` (inspection requests)
- `MIR-AR/STR/EL` → `Docs/03_Inspection_Requests/` (material inspection requests)
- `MAR-AR/ME` → `Docs/03_Inspection_Requests/` (material approval requests)
- `SDR-` → `Docs/` (structural design reports)
- `P0639` or `P083` → `Docs/` (visitor center design packages)

### 2. Aseer Museum — Proposals & Scope
Filenames containing `PROPOSAL`, `ASIR REGIONAL MUSEUM`, `Scope`, `Fee`, `عسير`, `متحف عسير`, `Aseer 2026` → **Aseer-Museum/Design Files/00_Scope_and_Proposals/**

### 3. Weekly Reports
Filenames containing `Weekly Project Status Report`, `التقرير الاسبوعي`, `Progress Report` → **Aseer-Museum/Reports & Meeting/02_Progress Reports/**

### 4. Submittal Archives
Filenames containing `Submittal` + date/7z/zip → **Aseer-Museum/Completed Tender Package From NRS/Submittals/**

### 5. Subcontractor Documents
Filenames containing `Submital` (with one 't'), `LG_`, `MVii`, `Glasbau`, `GBH`, `HAHN` → **Aseer-Museum/Subcontractors/03_AV_IT_Contractor/** (LG) or `02_Showcases_Contractor/` (GBH)

### 6. Technical Datasheets
Filenames containing `Technical data sheet`, `Datasheet`, `Specification` (non-project-specific), `Silicone`, `sealant`, `brochure`, `Labels_Sample` → **Aseer-Museum/Docs/00_Admin/99_Images/**

### 7. Cross-Project References
Filenames containing `Jabal Omar`, `Jabal_Omar`, `El-Ghamama`, `غمامة`, `شحنات المدينة` → **Aseer-Museum/Docs/00_Admin/** (filed under Aseer for reference)

### 8. Samaya Company Admin (Arabic documents)
Any Arabic-named file belonging to one of these categories:

| Category | Arabic Keywords | English Equivalent |
|----------|----------------|-------------------|
| Company Profile | بروفايل, ملف تعريفي, Factory Profile | Company profile, factory brochure |
| Company Record | سجل | Company record |
| Municipal License | رخصه بلدي | Municipal/building license |
| Zakat/Tax | زكاة, ضريبة | Zakat certificate, tax |
| Saudization | توطين | Saudization certificate |
| Social Insurance | تامينات, التأمينات | Social insurance |
| Chamber of Commerce | غرفة تجارية | Chamber of Commerce |
| National Address | عنوان وطني | National address |
| Media License | ترخيص اعلامي | Media/commercial license |
| Environmental Permit | تصريح بيئي | Environmental permit |
| Quality/Safety Manual | QUALITY, OCCUPATIONAL HEALTH | QMS/OH&S manuals |
| Contractor Classification | تصنيف مقاولين | Contractor classification |
| Contractor Membership | عضوية مقاول | Contractor membership |
| Final/Settlement Cert | شهادة نهائية, مديونيات | Final/debt certificates |
| Rental Contract | ايجار | Rental/lease agreement |
| Cash / Overtime | Cash out, OVER TIME, overtime | Financial docs |

→ **Samaya/Docs/SAMAYA-Formal-Docs/** (company-level, NOT project-specific)

**CRITICAL: These do NOT belong in Aseer-Museum.** They are Samaya Investment company documents, not project deliverables. The correct destination is `~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Docs/SAMAYAYA-Formal-Docs/`.

Exception — operational/admin items that ARE project-specific stay in Aseer/Docs/00_Admin/:
- Resthouse rental, SOW templates, punch list templates
- Cash out/overtime records tied to project labor
- Procurement process references
- Hoarding project designs (Samaya company projects, not Aseer)
- Site media, WhatsApp images, embedded email images

### 9. HR / Personnel
Filenames containing `Mr.`, `Letter`, `Itinerary`, `شكوي`, `زيادة راتب`, `استقالة`, `CV`, `سيرة` → **Aseer-Museum/Docs/00_Admin/HR/**

### 10. Hoarding Projects
Filenames containing `hoarding`, `Hoarding RFQ`, `Hoarding Pricing` → **Aseer-Museum/Docs/00_Admin/** (Samaya company hoarding designs for Dammam, Gas Station, Showrooms)

### 11. Site Media (Photos/Videos)
| Pattern | File Extension | Destination |
|---------|---------------|-------------|
| `WhatsApp Image` | .jpeg, .jpg, .png | Aseer-Museum/Docs/00_Admin/99_Images/ |
| `WhatsApp Video` | .mp4 | Aseer-Museum/Docs/00_Admin/99_Images/ |
| `IMG-` / `IMG_` | .jpg, .jpeg, .pdf | Aseer-Museum/Docs/00_Admin/99_Images/ |
| `VID-` | .mp4 | Aseer-Museum/Docs/00_Admin/99_Images/ |
| Arabic-dated file | .jpg (like ٢٠٢٦٠٤٢٠) | Aseer-Museum/Docs/00_Admin/99_Images/ |

### 12. Embedded Email Images
Small images under 100KB originating from Outlook (no meaningful project content):
- `Outlook-cid_*`, `image*.jpg/png/emz`, `icons-*`, `page_1.*`, `extracted_img.*`, `signeture.*`, `image.png`, `1000000873*` → **Aseer-Museum/Docs/00_Admin/99_Images/**

### 13. Catch-All / Unknown
Any file not matching rules 1-12 → **Aseer-Museum/Docs/00_Admin/** (default)

## Filename Pattern Examples from Weeks 05-23 Filing

| Actual Filename | Rule Applied | Destination |
|----------------|--------------|-------------|
| التقرير الاسبوعي 3 مايو.docx | 3. Weekly Reports | Reports & Meeting/02_Progress Reports/ |
| شهادة الزكاة.PDF | 8. Samaya Admin (Zakat) | Samaya/Docs/SAMAYA-Formal-Docs/ |
| التصريح البيئي ورشة الحدادة.pdf | 8. Samaya Admin (Environmental) | Samaya/Docs/SAMAYA-Formal-Docs/ |
| Mr. Ahmed Elbahrawy.pdf | 9. HR | Docs/00_Admin/HR/ |
| Hoarding RFQ.pdf | 10. Hoarding Projects | Docs/00_Admin/ |
| Jabal_Omar_Executive_Dashboard.pdf | 7. Cross-Project | Docs/00_Admin/ |
| 01 - Silicone sealant - Dow Corning 993.pdf | 6. Technical Datasheets | Docs/00_Admin/99_Images/ |
| LG_Submital rev08.pdf | 5. Subcontractor | Subcontractors/03_AV_IT_Contractor/ |
| PROPOSAL - ASIR REGIONAL MUSEUM - CEILING.pdf | 2. Proposals | Design Files/00_Scope_and_Proposals/ |
| Submittal 04 04-14-2026.7z | 4. Submittal Archive | Completed Tender Package From NRS/Submittals/ |
| ZAM-NWC-CTR-MAR-*-Rev.00.pdf | 1. Zamzam MAR | Zamzam/Docs/ |
| TRUSS.rar | 1. Zamzam structural | Zamzam/Docs/ |
| Connections.zip | 1. Zamzam connections | Zamzam/Docs/ |
| Eaton-Technical-data-sheet-UL.pdf | 6. Technical Datasheets | Docs/00_Admin/99_Images/ |
| IMG_7782.jpeg | 11. Site Media | Docs/00_Admin/99_Images/ |
| G137786969.pdf | — | Desktop/invoices/Microsoft/ |

## Deduplication Before Copy

Before copying any file to BIM destination:

1. Normalize filename to lowercase
2. Check if exact filename exists at destination
3. If exists, compare file sizes:
   - Same size → skip (already filed)
   - Different size → overwrite (updated version)
4. Log duplicate skips for reporting

## Weekly Archive Scanning Workflow

When processing weekly email archive files (`{week_no}.md` in `~/Documents/04_Outlook_Connection/mails/`):

1. **Extract attachment refs:** `grep -o 'attachments/[^)]*' {week}.md | sort -u`
2. **Build the "already filed" set:** Walk all BIM destination trees (Aseer, Zamzam, Samaya Formal Docs) collecting lowercase filenames
3. **Classify by destination:** For each unique attachment ref, URL-decode the filename and check against the decision tree rules above
4. **Skip inline/temp:** GUID names (36-char hex UUIDs), imageNNN, Outlook-cid-*, icons-*, files < 1KB, `d66938.webp`
5. **Copy to destination:** Use `cat src > /tmp/name && mv /tmp/name dst/name` for OneDrive cloud files
6. **Update PROJECT_MEMORY.md:** Add session update with counts per destination category
7. **Update Zamzam table:** Add new row per filed Zamzam doc

### OneDrive Copy Workaround (Refined)

`cp` on OneDrive cloud files often fails with "fcopyfile failed: Operation timed out" even when copying to `/tmp/`. The reliable method:

```bash
# This works: cat reads the file content directly, bypassing the copy lock
cat "$src_file" > "/tmp/$basename" && mv "/tmp/$basename" "$dst_path"

# This fails: cp triggers OneDrive sync engine lock
cp "$src_file" "/tmp/$basename"   # ❌ fcopyfile failed

# This also fails: dd triggers fcopyfile
dd if="$src_file" of="/tmp/$basename" bs=1M  # ❌ fcopyfile failed (0 bytes transferred)
```

The `cat` redirect forces a raw read of the file bytes without involving the OneDrive file provider's fcopyfile optimization, which avoids the cloud lock.

**Files that are truly cloud-only** (not cached locally) will show as 4 bytes in `ls -la` and `file` will fail. For these, `cat` also times out — the file needs to be fully synced first. Touch/read the file with `ls -la` first; if it shows 4 bytes, skip and try again later.

### Skip Analysis Files in Subfolders

The email pipeline creates AI-generated `.md` analysis files in subfolders (e.g., `others/MOC-MUS-ASE-1KH-PL-0047_Analysis.md`, `schedules/Aseer_Museum_Schedule_Analysis.md`). These are working notes from the `summarize_attachments.py` script and should **remain in their subfolder** — do not copy them to BIM destinations.

## Verification After Filing

After a batch filing operation, verify:
1. Count of files copied vs skipped vs errors
2. Validate destination paths exist and are within the correct project
3. **Check BIM target folder existence before bulk copy** — Two known mismatches between user instructions and actual tree:
   - `Aseer-Museum/Docs/00_Admin/99_Images/` → does NOT exist, must `mkdir -p`
   - `Aseer-Museum/Subcontractors/14_MEP_Contractor/` → does NOT exist, use `Subcontractors/12_MEP_Installation/` instead
   General rule: verify every destination path before copying. Files moved to a non-existent dir silently create a regular file at the intended parent path instead of landing inside it.
4. Update PROJECT_MEMORY.md session update section
5. Update Zamzam section if any Zamzam files were added
