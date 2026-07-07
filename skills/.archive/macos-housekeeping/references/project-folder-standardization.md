# Project Folder Standardization — Template-Driven Organization

Standardize a set of project folders by applying a uniform subfolder template and remapping existing content into it.

## When to Use

- A project directory has 5+ project folders, each with a different internal structure (some numbered, some flat, some with custom schemes)
- You want all projects to share a consistent, navigable subfolder hierarchy
- Existing content (proposals, drawings, contracts, designs, site docs) is scattered at root level or in non-standard subdirectories

## The Standard Template

The following 13-folder template covers the full project lifecycle:

```
00_Admin/              — Contracts, budgets, procurement, permits, logos, commercial docs
01_CLIENT_INPUTS/      — RFPs, client emails, briefs, external inputs
02_Submittals/         — Proposals, technical offers, SOWs, tender packages, consultant responses
03_Design/             — Design files, 3D models, renders, visitor center plans, SAP2000
04_Drawings/           — CAD files, architectural drawings, design drawing PDFs
05_Specifications/     — Technical specs, design guides, material specs
06_BIM/                — BIM models, IFC, coordination models
07_Meetings/           — Meeting minutes, MoMs, presentations
08_Schedules/          — Project schedules, timelines, Gantt charts
09_Site/               — Site logs, photos, temp area pages, site reports
10_Calculations/       — Engineering calcs, structural calcs
11_Standards_&_References/ — Heritage compliance docs, standards, regulatory refs
99_Templates/          — Scripts, reusable templates, build tools
```

## Mapping Rules

When remapping existing content into the template, use these rules:

| Original Content Type | Target Template Folder |
|---|---|
| Tender packages, contractor docs | 02_Submittals/ |
| Design proposals, technical offers | 02_Submittals/ |
| Statement of Work (SOW), scope docs | 02_Submittals/ |
| Financial proposals, costing models | 00_Admin/ |
| BOQ, pricing, budgets | 00_Admin/ |
| Contracts | 00_Admin/ |
| Procurement docs | 00_Admin/ |
| Permits | 00_Admin/ |
| Logos, branding assets | 00_Admin/Logos |
| Design files, 3D models, renders | 03_Design/ |
| Visitor center plans, architectural design | 03_Design/ |
| Structural engineering files (SAP2000) | 03_Design/ |
| CAD files, DWG | 04_Drawings/ |
| Design drawing PDFs | 04_Drawings/ |
| Technical Drawings folder | 04_Drawings/ |
| Design guides, material specs | 05_Specifications/ |
| Bills of quantities | 00_Admin/ |
| Project schedules, timelines | 08_Schedules/ |
| Site logs, temp area pages | 09_Site/ |
| Site photos | 09_Site/ |
| Scripts, build tools | 99_Templates/ |
| Heritage compliance docs | 11_Standards_&_References/ |
| RFP documents from client | 01_CLIENT_INPUTS/ |

## Implementation Pattern

### Step 1: Inventory each project
List current contents of each project folder. Identify which have:
- Standard template already (skip or just clean up loose files)
- Non-standard numbered scheme (e.g., `01_Designs`, `02_Contracts` — need remapping)
- Flat/unstructured (all files at root — need full organization)
- Empty numbered folders (structure exists but no content yet)

### Step 2: Create template structure
Use Python's `os.makedirs()` to create all template directories. **Avoid bash for this when paths contain parentheses** (common in OneDrive paths like `OneDrive-Personal(2)` — parentheses break bash command parsing, causing syntax errors).

```python
import os
base = "/path/with(parentheses)/in/name/Project"
dirs = ["00_Admin", "01_CLIENT_INPUTS", "02_Submittals", ...]
for d in dirs:
    os.makedirs(os.path.join(base, d), exist_ok=True)
```

### Step 3: Move content into template
For each source folder or file, move it to the correct template directory:

```python
import os
base = "/path/to/project"
moves = [
    ("01_Designs/", "03_Design/"),
    ("02_Contracts/", "00_Admin/Contracts"),
    ("BOQ", "00_Admin/"),
]
for src, dst in moves:
    full_src = os.path.join(base, src)
    full_dst = os.path.join(base, dst)
    if os.path.exists(full_src):
        os.rename(full_src, full_dst)
```

### Step 4: Handle "Directory not empty" conflicts
When `os.rename()` (or `mv`) fails because the destination directory already exists, merge content iteratively:

```python
for item in os.listdir(source_dir):
    s = os.path.join(source_dir, item)
    d = os.path.join(dest_dir, item)
    if os.path.exists(d):
        if os.path.isdir(s):
            # Nested subdirs: merge contents individually
            for sub in os.listdir(s):
                os.rename(os.path.join(s, sub), os.path.join(d, sub))
            os.rmdir(s)
        else:
            # File conflict — skip (or log for manual review)
            pass
    else:
        os.rename(s, d)
os.rmdir(source_dir)
```

### Step 5: Handle OneDrive cloud-only files
Files synced via OneDrive may be **cloud-only placeholders** (shown as 0 bytes in `ls -la`). Operations to be aware of:

| Operation | Behavior on cloud-only files |
|---|---|
| `mv` (rename/move) | Instant — metadata-only operation, files stay in cloud |
| `cp` / `rsync` | **Triggers download** — may timeout on large files (50MB+ PDFs, 100MB HTML exports) |
| `os.rename()` (Python) | Instant — same as `mv` |
| `shutil.copy*` | Triggers download — may timeout |

**Recommendation:** Use `mv`/`os.rename()` for all OneDrive file operations. Reserve `cp`/`rsync` only when you need to preserve the source (non-destructive copy).

### Step 6: Remove empty legacy directories
After all content moved, remove now-empty source directories from innermost to outermost:

```python
os.rmdir(os.path.join(base, "source_dir/subdir"))
os.rmdir(os.path.join(base, "source_dir"))
# ... eventually
os.rmdir(os.path.join(base, "projects"))  # if empty
```

### Step 7: Verify
- Every project folder has the full template tree (13 dirs)
- No loose source files remain at root (except README.md, .claude/, Docs/ if well-organized internally)
- Legacy `projects/` container removed
- Content exists in appropriate template directories (check a few key ones)

## Verifying Completion

Run this check across all projects:

```bash
for d in 0*_*/; do
    missing=""
    for t in 00_Admin 01_CLIENT_INPUTS 02_Submittals 03_Design 04_Drawings \
             05_Specifications 06_BIM 07_Meetings 08_Schedules 09_Site \
             10_Calculations "11_Standards_&_References" 99_Templates; do
        [ ! -d "$d/$t" ] && missing="$missing $t"
    done
    [ -n "$missing" ] && echo "MISSING in $d:$missing" || echo "✓ $d"
done
```

## Pitfalls

- **Parentheses in OneDrive paths** — Bash interprets them as subshell syntax. Use Python's `os` module or escape/quoted paths in bash.
- **Cloud-only files appear as 0 bytes** — Don't delete files based on size alone. Verify with `fileproviderctl evaluate` before removal.
- **`rsync`/`cp` timeouts on large files** — In cloud-synced dirs, large files may not be locally available. Use `mv`/`os.rename()` for moves.
- **Already-migrated projects** — Some projects may already have template dirs + root-level content. Check first to avoid duplicate work.
- **Well-organized non-template folders** — Some folders like `Docs/` (with internal structure) or `.claude/` (config) are fine at root. Don't force them into the template if they're self-contained and useful.
