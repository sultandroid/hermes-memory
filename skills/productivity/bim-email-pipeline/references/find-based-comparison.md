# Find-Based Attachment Comparison (Sub-Agent Fallback)

When `fast_organize.py` or `compare_and_file.py` can't run (OneDrive EDEADLK, script path issues, `com.apple.provenance` lock), use this fallback via `delegate_task`.

## Why this exists

The pipeline scripts can be blocked by macOS OneDrive File Provider's `com.apple.provenance` extended attribute on cloud-stub files. The `find` command works on stubs because it only reads directory metadata — it never opens files for content. This approach lets you compare 200+ attachments against 10K+ BIM files without triggering EDEADLK.

## Delegation template

```
goal: Compare Outlook attachments against BIM directories to identify unfiled files and copy them.
context: |
  Step 1 — Inventory attachments at ~/Documents/04_Outlook_Connection/mails/attachments/
  Use: find <dir> -type f | sort (works on OneDrive stubs).
  
  Step 2 — Inventory BIM targets:
  - Aseer-Museum:
    .../05_Correspondence_Archive/
    .../04_Specifications_and_BOQ/
    .../00_Daily Reports/
    .../00_Scope_and_Proposals/
    .../14_MEP_Contractor/
    .../99_Images/
  - Zamzam Museum:
    .../03_Inspection_Requests/
  Base: ~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/
  
  Use: find <dir> -type f | sort for ALL targets. Recursive is fine — find reads directory metadata only.
  
  Step 3 — For each attachment basename, check if it exists in the BIM file list.
  - Match on basename (strip directory prefix, keep extension)
  - Arabic normalization: unicodedata.normalize('NFC', name).lower()
  - Alef variants (أإآٱ → ا), Yeh variants (ىئ → ي), Teh Marbuta (ة → ه)
  - difflib.SequenceMatcher ratio > 0.9 for _1/_2 suffix variants
  
  Step 4 — Copy unfiled files.
  - If _1 variant already exists in target, append _2 suffix
  - OneDrive EDEADLK workaround for cp failures:
    1. brctl download <src> (force local sync)
    2. cp -X <src> /tmp/copy && mv /tmp/copy <dest>
    3. Or: cat <src> > /tmp/x && mv /tmp/x <dest>
  - mkdir -p dest dir before copy
  
  Step 5 — Return structured report: totals per project, which files were new, where copied, any errors.
```

## Pitfall: Verify actual new files, not just exit code

`download_mails.py` may exit 0 with zero output — this doesn't guarantee new emails were actually downloaded. Always verify by checking the attachments directory for files with recent modification times (`find -ctime -1`). If the script ran but no new files appeared, the pipeline is in steady state (no new email since last run), not a failure.

## Routing map

| Source subfolder | BIM target |
|---|---|
| `aseer_museum/correspondence/` | Aseer/05_Correspondence_Archive/ |
| `aseer_museum/drawings_designs/` | Aseer/Design Files/00_Scope_and_Proposals/ |
| `aseer_museum/reports/` | Aseer/Reports & Meeting/00_Daily Reports/ |
| `aseer_museum/others/` (specs/BOQ) | Aseer/04_Specifications_and_BOQ/ |
| `aseer_museum/proposals_contracts/` | Aseer/Design Files/00_Scope_and_Proposals/ |
| `general/site_photos/` | Aseer/Docs/00_Admin/99_Images/ |
| `aseer_museum/site_photos/` | Aseer/Docs/00_Admin/99_Images/ |
| `zamzam_nwc/correspondence/` | Zamzam Museum/Docs/03_Inspection_Requests/ |
| `admin_hr/` | Cross-project — check subfolders individually |
