# Steady-State Detection & Attachment Comparison

## When to use

During a cron pipeline run when `download_mails.py` exits with code 0 and no stdout, and you need to determine if there's anything new to process.

## Three conditions → steady state

| Condition | How to check |
|-----------|-------------|
| No new emails | `download_mails.py` exits 0, no stdout |
| No new attachments | `find attachments/ -type f -newer LAST_RUN_MD` returns empty |
| No new archive | `ls mails/NN.md` — no increment beyond latest (23.md) |

All three = steady state. Write a pipeline_run record and exit.

## Attachment-vs-BIM comparison

Full Python workflow to identify unfiled attachments:

```python
import os

attach_base = os.path.expanduser('~/Documents/04_Outlook_Connection/mails/attachments')
bim_base = os.path.expanduser('~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit')

# Collect BIM-filed filenames (lowercase, case-insensitive)
BIM_TARGETS = [
    'Aseer-Museum/Completed Tender Package From NRS/05_Correspondence_Archive',
    'Aseer-Museum/Completed Tender Package From NRS/04_Specifications_and_BOQ',
    'Aseer-Museum/Reports & Meeting/00_Daily Reports',
    'Aseer-Museum/Design Files/00_Scope_and_Proposals',
    'Aseer-Museum/Subcontractors/14_MEP_Contractor',
    'Aseer-Museum/Docs/00_Admin/99_Images',
    'Zamzam Museum/Docs/03_Inspection_Requests',
]

bim_filed = set()
for rel in BIM_TARGETS:
    folder = os.path.join(bim_base, rel)
    if os.path.exists(folder):
        for f in os.listdir(folder):
            bim_filed.add(f.lower())

# Walk all 7 attachment project subfolders
for proj in sorted(os.listdir(attach_base)):
    proj_path = os.path.join(attach_base, proj)
    if not os.path.isdir(proj_path):
        continue
    for cat in sorted(os.listdir(proj_path)):
        cat_path = os.path.join(proj_path, cat)
        if not os.path.isdir(cat_path):
            continue
        unfiled = [f for f in os.listdir(cat_path) if f.lower() not in bim_filed]
        if unfiled:
            print(f'[{proj}/{cat}] {len(unfiled)} unfiled of {len(os.listdir(cat_path))}')
            for f in unfiled:
                print(f'    {f}')
```

## Note on general/ and admin_hr/ folders

Files in `general/` and `admin_hr/` subfolders are typically non-project-specific (equipment specs, brochures, admin docs). They will always show as "unfiled" against BIM project folders — filter them out unless the filename clearly indicates a project (e.g. contains "ASEER", "ASE", "ZAM", "MOC-MUS").

## PROJECT_MEMORY_UPDATE fallback

When main PROJECT_MEMORY.md is EDEADLK-locked by OneDrive:
1. Extract new findings from email archive md files
2. Write a PROJECT_MEMORY_UPDATE_YYYY-MM-DD.md to the BIM Aseer-Museum root directory
3. Write to /tmp first, then shutil.copy2 to BIM path (bypasses the coordinator deadlock for writes)
4. Note in the pipeline report that merge is pending

## BIM Target Folder Mapping

### Aseer-Museum
| BIM Folder | Attachment Category |
|---|---|
| `.../05_Correspondence_Archive` | correspondence |
| `.../04_Specifications_and_BOQ` | technical_specifications |
| `.../00_Daily Reports` | reports |
| `.../00_Scope_and_Proposals` | drawings_designs, proposals_contracts |
| `.../14_MEP_Contractor` | technical_specifications (MEP) |
| `.../99_Images` | site_photos |

### Zamzam Museum
| BIM Folder | Attachment Category |
|---|---|
| `.../03_Inspection_Requests` | correspondence (IRs, MIRs, WIRs) |

## Comparison results snapshot (June 11, 2026)

- 201 total attachment files across 7 project subfolders
- Aseer Museum: 53 files — all filed
- Zamzam: 14 files — all filed
- General/Admin: ~9 unclassified files (equipment specs, proposals) — not project-specific
- Steady state confirmed: no new emails or attachments since June 8
