# Bulk Attachment Filing Workflow

## Trigger
When new email attachments land in `~/Documents/04_Outlook_Connection/mails/attachments/` either in the root or in categorized subfolders (`schedules/`, `correspondence/`, `drawings_designs/`, `proposals_contracts/`, `reports/`, `others/`, `site_photos/`).

## Steps

1. **Scan for new files** — Compare flat folder contents against all already-filed filenames in BIM destinations:
   - Aseer-Museum: `OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/`
   - Zamzam Museum: `OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Zamzam Museum/`
   - Samaya Formal Docs: `OneDrive-SAMAYAINVESTMENT/Samaya/Docs/SAMAYA-Formal-Docs/`

2. **Categorize by destination:**
   - `MOC-MUS-ASE*` / `A2742*` / `Aseer*` → Aseer-Museum/ (by type: proposals→Design Files, reports→Reports & Meeting, IFC→Completed Tender Package, etc.)
   - `ZAM-*` → Zamzam/Docs/ (IR/MIR/MAR → 03_Inspection_Requests, DOC → Docs/)
   - Certificates, licenses, permits → Samaya/Docs/SAMAYA-Formal-Docs/ (NOT inside project folders)
   - Site photos, WhatsApp media → Aseer/Docs/00_Admin/99_Images/
   - GUID-named files, tiny images (< 1KB), Outlook-cid*, icons-* → skip (temp/embedded)

3. **Copy with OneDrive workaround:**
   ```
   cat "$SRC" > /tmp/f && mv /tmp/f "$DEST"
   ```
   Never `cp` directly to/from OneDrive — it times out on cloud-only files.

4. **Update registers:**
   - PROJECT_MEMORY.md — add session update section
   - Zamzam section — update document inventory
   - Memory — update with new filing count

## Entity Isolation Reminder
- Samaya formal docs → `Samaya/Docs/SAMAYA-Formal-Docs/`
- Aseer project docs → `Aseer-Museum/` subfolders
- Zamzam docs → `Zamzam Museum/`
- Keep project-operational (resthouse rental, overtime, hoarding projects, templates) inside project admin folders
- Move company-level formal documents (certificates, licenses, permits) to Samaya-level
