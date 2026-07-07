# Batch Inventory Comparison & File Copy Pattern

Proven when processing 421 backlog files (Jun 5, 2026) across Aseer + Zamzam projects.

## When to Use

The user's `download_mails.py` pipeline has produced weekly `.md` archives and organized attachments into project/category subfolders under `~/Documents/04_Outlook_Connection/mails/attachments/`. You need to copy unfiled files to BIM destinations under OneDrive.

> ⚠️ **Path note:** The actual directory is `~/Documents/Documents - Mohamed's MacBook Pro/04_Outlook_Connection/`. The path `~/Documents/04_Outlook_Connection/` is a shorter alias that doesn't exist on disk. Code examples below work with both paths if the abbreviated form exists; if not, use the glob `~/Documents/Documents*/04_Outlook_Connection/`.

## Decomposition (3 parallel + 1 sequential)

### Phase 1 — Parallel (3 sub-agents via delegate_task)

| Task | Goal | Output |
|------|------|--------|
| **Task 1** (inventory attachments) | Recursively walk `~/Documents/04_Outlook_Connection/mails/attachments/` | JSON array: full_path, size, mtime, project (aseer_museum/zamzam_nwc/...), category, filename |
| **Task 2** (inventory BIM destinations) | Recursively walk all 7 BIM destination folders under OneDrive | JSON dict: {destination_key: [lowercase_basename, ...]} |
| **Task 3** (state/status) | Read `.watchdog_state.json`, `.email_pipeline_state.json`, routing reports | Existing processing state |

### Phase 2 — Sequential (1 sub-agent for comparison + copy)

Load both JSON inventories. For each file in attachments inventory:
1. Skip non-target projects (admin_hr, general, haramein_ghamamah, hoarding_signage, makkah_jabal_omar)
2. Apply routing rules to determine destination
3. Check basename (lowercase) against BIM inventory
4. If not found AND file is from a target project → copy via cat workaround

## Routing Rules (for attachments/ organized by download_mails.py)

```
aseer_museum/correspondence/*  → Aseer-Museum/05_Correspondence_Archive/
aseer_museum/technical_specifications/*  → Aseer-Museum/04_Specifications_and_BOQ/
aseer_museum/reports/*  → Aseer-Museum/00_Daily Reports/
aseer_museum/proposals_contracts/*  → Aseer-Museum/Design Files/00_Scope_and_Proposals/
aseer_museum/site_photos/*.{jpg,jpeg,png}  → Aseer-Museum/Docs/00_Admin/99_Images/
aseer_museum/drawings_designs/*  → Aseer-Museum/05_Correspondence_Archive/
aseer_museum/others/*MEP*  → Aseer-Museum/Subcontractors/14_MEP_Contractor/

zamzam_nwc/*  → Zamzam Museum/Docs/03_Inspection_Requests/
```

## Copy Implementation (Python, uses cat workaround for OneDrive)

```python
import json, os, subprocess

ATTACHMENTS_BASE = os.path.expanduser(
    "~/Documents/04_Outlook_Connection/mails/attachments"
)
ONEDRIVE_BASE = os.path.expanduser(
    "~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit"
)

ROUTING = {
    ("aseer_museum", "correspondence"): "Aseer-Museum/Completed Tender Package From NRS/05_Correspondence_Archive",
    ("aseer_museum", "technical_specifications"): "Aseer-Museum/Completed Tender Package From NRS/04_Specifications_and_BOQ",
    ("aseer_museum", "reports"): "Aseer-Museum/Reports & Meeting/00_Daily Reports",
    ("aseer_museum", "proposals_contracts"): "Aseer-Museum/Design Files/00_Scope_and_Proposals",
    ("aseer_museum", "site_photos"): "Aseer-Museum/Docs/00_Admin/99_Images",
    ("aseer_museum", "drawings_designs"): "Aseer-Museum/Completed Tender Package From NRS/05_Correspondence_Archive",
    ("zamzam_nwc",): "Zamzam Museum/Docs/03_Inspection_Requests",
}

def route(project, category, filename):
    project_lower = project.lower()
    cat_lower = category.lower()
    # zamzam_nwc: everything goes to inspection_requests
    if project_lower == "zamzam_nwc":
        key = (project_lower,)
    elif project_lower == "aseer_museum":
        key = (project_lower, cat_lower)
        # aseer others/: only MEP-named files
        if cat_lower == "others" and "MEP" not in filename.upper():
            return None
    else:
        return None
    dest = ROUTING.get(key)
    if dest:
        return os.path.join(ONEDRIVE_BASE, dest)
    return None

def copy_cat(src, dst_dir):
    """Copy file via cat -> /tmp -> mv to avoid OneDrive fcopyfile lock."""
    basename = os.path.basename(src)
    tmp = f"/tmp/{basename}"
    subprocess.run(["cat", src], stdout=open(tmp, "wb"), check=True)
    dst = os.path.join(dst_dir, basename)
    subprocess.run(["mv", tmp, dst], check=True)
    return dst
```

## Performance Reference

| Phase | Duration | Files Processed |
|-------|----------|-----------------|
| Parallel scan (3 sub-agents) | ~65s | 1,058 attachments + 13,893 BIM files |
| Comparison + copy (1 sub-agent) | ~82s | 421 files copied, 109 skipped |
| **Total** | **~2.5 min** | **421 new files filed** |

## Pitfalls

- **BIM inventory size:** Aseer Correspondence Archive has 13,525 files. Loading all into memory as a set is fine (~few MB).
- **Duplicate basenames:** Same filename may exist in multiple BIM subdirectories. The set approach (first match = already filed) is correct for dedup.
- **Arabic filenames:** Use `conn.text_factory = str` for SQLite, `ensure_ascii=False` for JSON dump.
- **Modification time snafu:** The download_mails.py "Fast Organize" step changes mtime on ALL files in the attachments folder, making everything look "modified today". Use basename comparison against BIM inventory, not mtime.
- **🔴 Shell `find | xargs basename` misses files with special characters (confirmed 2026-06-08):** When building a filename set for comparison, a shell pipeline like `find ... | xargs -I{} basename '{}' | sort -u` silently drops files whose names contain parentheses `()`, spaces, commas, or non-ASCII characters. In one run, 13,545 BIM files collapsed to only **15 unique basenames** via this method, causing 39 files to falsely appear "new." Always use Python `os.walk()` or `pathlib.rglob()` to build filename sets — these handle all characters correctly. **Sanity-check your count:** if `sort -u` returns far fewer entries than the raw file count, the pipeline is broken. Use `find ... -type f -exec basename '{}' \; | sort -u` only for small, guaranteed-ASCII file sets.
- **🔴 Always verify "new" files against BIM with targeted `find -name` before copying (confirmed 2026-06-08):** After the comparison pass flags files as "not in BIM," run a targeted `find <BIM_root> -name "<filename>"` for each flagged file. Files that exist under a different path (e.g., `Docs/`, `Email_Archive/`, `Correspondence/` top-level) than the expected target folder will be missed by the basename-set comparison if the set-building approach was flawed. This verification step caught 39 false positives in a single run. Confirm each file is genuinely absent before any `cat`/`mv` copy.
