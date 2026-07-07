# BIM / Construction Project Folder Cleanup

Reference guide for organizing Autodesk/Revit/AutoCAD project folders with mixed-project, email, and temp-file clutter.

## Typical BIM folder patterns

| Pattern | Meaning | Action |
|---------|---------|--------|
| `.dwg` | AutoCAD drawing | Keep — move to Design Files/ |
| `.rvt` | Revit project file | Keep — move to Revit Files/ |
| `.ifc` | IFC export | Keep — move to Revit Files/ |
| `.nwc` | Navisworks cache | Keep — move to Revit Files/ or Coordination/ |
| `.rfa` | Revit family | Keep — move to Revit Files/ |
| `.pcp` / `.pc3` | AutoCAD plot config | Delete — temp/recreateable |
| `.bak` | AutoCAD backup | Delete — DWG supersedes |
| `.dwl` / `.dwl2` | DWG lock file | Delete — orphaned after DWG closes |
| `.slog` | Revit journal | Delete — session log |
| `.rws` | Revit worksharing | Delete — sync temp |
| `.dat` (projectinformation.*, etc.) | Revit DB cache | Delete — temp |

## Detecting other projects by naming convention

In BIM units, multiple project files often accumulate in one folder. Use the naming prefix to identify the project:

| Prefix example | Likely project |
|----------------|---------------|
| `211210_CREATION_*`, `211210_Creation Story_*` | "Creation" project (date-coded) |
| `4121 MIN OF CULTURE_*` | Ministry of Culture project |
| `Shisha_*`, `241216_Shisha_*` | Shisha lounge/bar fit-out |
| `A22-71-KZC-*` | KZC project |
| `GHCC-*` | GHCC project |
| `AlGalal` / `AlGamal` | AlGalal & AlGamal project |
| `121-135 مكة*` | 121-135 Mecca project |
| `1121x` (worker numbers) | Labor sheets for a separate project |
| `EST-1-121-Jaba-Alnoor-*` | Jaba Alnoor project |

**Rule of thumb:** If the prefix doesn't match the folder name theme (e.g. "Shisha" files in "Zamzam Museum"), it's almost certainly a different project.

## BIM email vs project document separation

In BIM folders, `.md` files come in two flavors:

**Email exports** (move to Email_Archive/):
- Date-prefixed: `2024-05-30 - Subject.md`
- Email keywords: `RE:`, `Fw:`, `shared 1 item`, `mentioned you`, `Hourly Notifications`, `Welcome to`
- `.eml` files

**Project documents** (keep in Docs/):
- Structured codes: `ZAM-SAM-121-ADM-INIT-*`, `PROJECT_*.md`
- Naming with SpecSection numbers: `09_78_00_A1`, `08_34_19_A1`
- Project names without date prefix: `35_Zamzam Museum & Visitor Center.md`

## Legacy projects/ subfolder vs. root-level numbered structure

A common pattern in mature project directories: **root-level numbered folders** (`01_ProjectName`, `02_AnotherProject`) coexist with a **legacy `projects/` subfolder**. This happens when someone introduces a numbered organizational scheme but the old content was never migrated.

**Detection:**
- Root has folders like `01_Darin_Visitor_Center`, `02_Shobra`, `03_Albiaa` etc.
- A `projects/` subfolder also exists with overlapping names: `projects/02_Shobra/`, `projects/03_Albiaa/`
- Some root folders may be **empty** — they're placeholders waiting for content from `projects/`
- Some may have partial content in both locations

**Migration status categories:**

| State | Root folder | projects/ folder | Action |
|-------|-------------|------------------|--------|
| Fully migrated | Has full sub-structure | Empty or has old copies | Clean up projects/ copy |
| Partially migrated | Has some content | Has complementary content | Merge both into root |
| Not migrated | Empty (just the numbered folder exists) | Has all content | Move content from projects/ to root |
| Root-only | Has content | Doesn't exist in projects/ | Nothing to do |

**Merge procedure:**
1. For each project in `projects/`, check if its root counterpart has content
2. If root is empty → `mv projects/<X>/* <Number_X>/` (instant on OneDrive since it's metadata-only)
3. If both have content → move subfolders one by one from `projects/<X>/` into root `<Number_X>/`, checking for conflicts
4. When `mv` fails with "Directory not empty", the destination already has that subfolder — merge contents: `mv projects/<X>/subdir/* root/<Number_X>/subdir/`, then clean up empty source dirs with `rmdir`
5. After all merges, verify every numbered root folder has content
6. Archive or delete the now-empty `projects/` folder

**Key OneDrive rule:** Always use `mv` (not `cp`, not `rsync`) for files inside OneDrive-synced folders. `mv` is a metadata operation that completes instantly regardless of file size. `cp`/`rsync` trigger actual file downloads from the cloud and timeout on large (99MB+) files.

**Real example (Tqanny_Projects):**
```
Tqanny_Projects/
├── 01_Darin_Visitor_Center/   ← has content (root-only)
├── 02_Shobra/                 ← EMPTY — content lives in projects/
├── 03_Albiaa/                 ← EMPTY — content lives in projects/
├── 04_Al_Faw/                 ← has content (root-only)
├── 05_Alrakaa_Center/         ← partial content (some new PDFs)
├── 06_Antara_Rock/            ← FULLY MIGRATED (00_Admin → 99_Templates)
├── 07_Said_Alshohadaa/        ← EMPTY — content lives in projects/
├── 08_Tabuk_Castle/           ← FULLY MIGRATED
├── projects/                  ← LEGACY container
│   ├── 02_Shobra/             ← has tender package, design
│   ├── 03_Albiaa/             ← has proposals, BOQ, design
│   ├── 05_Alrakaa_Center/     ← has Designs, Contracts, Budget
│   ├── 06_Antara_Rock_Visitor_Center/  ← has 3D, BOQ, drawings
│   ├── 07_Said_Alshohadaa_Hoarding/    ← has proposals, costing
│   └── 08_Tabuk_Castle_Visitor_Center/ ← has 3D, BOQ, drawings
├── DOCs/
├── Organization Chart/
└── Tenders/
```

## OneDrive considerations

- BIM folders under OneDrive show `0` bytes for all files not locally cached
- `du -sh` still reports actual size
- Moving files triggers cloud sync — confirm with user before bulk operations
- Use `if [ -f "..." ]` guards to safely skip already-absent files

## Organizing into discipline subfolders

Standard BIM discipline folders to populate:

```
Project_Root/
  Design Files/        → DWG, AI, DXF, design PDFs (furniture, finishes, lighting, shop drawings)
  Revit Files/         → RVT, IFC, NWC, RFA, FBX, IFC logs
  Docs/                → PDF reports, XLSX schedules, .md inspection records, sub-folders
  Docs/Inspections/    → ZAM-SAM-121-ADM-* / COMM-* / FAB-* / SITE-INST-* inspection markdowns
  B.O.Q/               → BOQ PDFs, quantity spreadsheets
  Coordination/        → Clash reports, coordination drawings
  Submittal's/         → Submittal logs, approval docs
  Email_Archive/       → Email .md + .eml
  Specs & Datasheet/   → Spec PDFs, cut sheets
  Media/               → JPG, PNG, MP4, HEIC (site photos, WhatsApp images)
  ID121_*/             → Project-specific sub-projects (e.g. Path Rehab)
  odoo/                → Odoo ERP staging (if used)
```

## Safe bulk-move pattern for special characters

When filenames contain Arabic, Unicode, `&`, or parentheses, use `execute_code` with shell-safe guards:

```python
from hermes_tools import terminal

# Safe move with existence check
files = ["file (1).pdf", "فاتورة-121.pdf", "Project & Co.docx"]
for f in files:
    terminal(f'if [ -f "{f}" ]; then mv "{f}" "Destination/" && echo OK; fi')
```

For bulk pattern moves:
```python
terminal("find . -maxdepth 1 -type f -name '*Furniture*' -exec mv -n {} 'Design Files/' \\;")
```
