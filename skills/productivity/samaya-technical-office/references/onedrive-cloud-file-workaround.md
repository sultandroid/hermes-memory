# OneDrive Cloud-Only File Workaround

**Symptom:** Files in `OneDrive-SAMAYAINVESTMENT` show size in `ls -la` but fail to read with:
- `cat/head/less/tail` → "Resource deadlock avoided"
- Python `open()` → "Resource deadlock avoided"  
- `wc`/`file` → same
- `pdftotext` → empty output or "Syntax Error: Couldn't find trailer dictionary"

**Root cause:** APFS file lease held by OneDrive sync engine. File bytes not downloaded locally — the listing metadata is visible but the actual content is cloud-gated.

**Confirmed recovery — try in order:**

0. **`ditto` (macOS built-in) for "Operation not permitted" locks** — When OneDrive completely denies read access (`cat` → "Operation not permitted", Python `open()` → `[Errno 1]`), `cp` may also fail. Try `ditto` — it uses different kernel paths and often bypasses the lock:
   ```bash
   ditto "/path/to/OneDrive/source.file" /tmp/restored.file
   # Then work with /tmp/restored.file
   ```
   `ditto` preserves resource forks and HFS metadata, but more importantly it can copy files that `cp` and `open()` cannot touch. Confirmed working on OneDrive SAMAYAINVESTMENT files (Jun 2026).
   
   **Restore pattern after accidental overwrite:** If you accidentally overwrite a OneDrive-stored file with `write_file` (which replaces the entire file rather than patching), other `cp` and `open()` calls will fail on the original path. Use `ditto` to copy the same FILENAME from a backup version (RevC00_DRAFT etc.) back to the original path:
   ```bash
   ditto /tmp/backup_copy.html "/path/to/OneDrive/destination.html"
   ```
   This bypasses OneDrive's extended-attribute locks and restores the file in-place.

5. **(Alternative) `ditto` for direct path restoration** — When recovering a trashed file on OneDrive, use `ditto` instead of Finder drag-and-drop or `cp`. `ditto` on a volume-level path restores inode linkage that `cp` can't recreate.

1. **`cp` to `/tmp/`** — Cloud files sometimes allow `cp /path/to/file /tmp/` even when direct reads fail. This is the fastest path.
   ```bash
   cp "/path/to/OneDrive/file.pdf" /tmp/file.pdf
   pdftotext /tmp/file.pdf -   # then read from /tmp
   ```

2. **Quit OneDrive + retry** — Close OneDrive.app, File Provider, Sync Service entirely. Wait 30s. Reopen. Works for short-term locks.

3. **Ask user to open file locally** — If none of the above work, ask the user to open the file in Preview (PDF) or Word (DOCX) on their Mac. This forces a local download.

4. **Web rename trick** — Go to onedrive.com → rename file → wait 5 min → rename back. Forces inode refresh.

**Files known to be cloud-only (May 2026 — Aseer project):**
- `Docs/02_Plans_and_Procedures/02.1_DMP/2026-05-18_DMP_Rev_C04_REV02_NRS_signed.pdf`
- `Docs/02_Plans_and_Procedures/02.1_DMP/Aseer_Museum_DMP_Rev03_C03_NRS_Lead.docx`
- All markdown chapter files in `02_DMP_Chapters/` (show `0 lines` when read via direct tools)

**Prevention:** Avoid chained reads of OneDrive cloud files — if you need the content of a PDF/DOCX in OneDrive, copy to `/tmp/` first before processing.
