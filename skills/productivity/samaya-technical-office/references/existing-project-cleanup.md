# Existing Project Folder — Cleanup & Template Alignment

## When to Use

A project folder already exists but has grown organically and needs to be brought back to the standard BIM template. This is **not** for new projects (use `project-initializer`) or for NRS consultant packages (use the Receipt Audit workflow). This is for existing active project directories that have accumulated junk, bad names, and missing structure.

## Signals That Trigger This

- User says "arrange and organize" or "clean up this folder"
- User says "use our template" on an existing project
- User says "remove unrelated files" or "remove junk"
- You discover a project folder with: `New folder/`, `waiting area/`, `Program Files/`, `Users/`, multiple duplicate ZIPS, generic numbered folders like `01/`, `01(2)/`

## Pre-Work: Map Current Structure vs Template

```bash
# Current state
find . -maxdepth 5 -type d -not -path '*/\.*' | sort > /tmp/current_dirs.txt

# Template reference
find "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Template Folder" -maxdepth 4 -type d -not -path '*/\.*' | sort
```

The Template Folder lives at:
`Samaya/Technical Office/Bim Unit/Template Folder/`

Top-level template folders:
- As-Built Docs, B.O.Q, Contracts, Design Files, Docs (with 09_Registers/), Invoices, Reports & Meeting, Revit Files (Cad, Clash Reports, Excel Sch, Nwc, Pdf, Rfa, Rvt), Specs & Datasheet, Submittal's (Arch, Mep, Struc), Time Scheduales

## Cleanup Checklist

### Phase 1: Remove Junk (non-project software artifacts)

These are files and folders that are NOT project deliverables — they leak in from 3rd-party designers sharing their entire 3ds Max user profile:

| What | Why it's junk | Where it hides |
|------|--------------|----------------|
| `Program Files/` | 3ds Max software installation paths backed up by mistake | `Design Files/MAX Files/*/`, `Design Files/waiting area/` |
| `Users/` | 3ds Max user profile folders (config, preferences) | `Design Files/MAX Files/*/`, `Design Files/waiting area/` |
| `MAXFILES.TXT` | 3ds Max render/texture index — temp file | `Design Files/MAX Files/*/` |
| `02-Max Library/MAX MAPS/` | Downloaded texture maps (can stay if linked to .max file, but often bulk-downloaded) | `Design Files/MAX Files/*/02-Max Library/` |
| `plot.log` | AutoCAD plotting log | Inside CAD folders |

**Removal pattern:**
```bash
rm -rf "Design Files/MAX Files/*/Program Files" "Design Files/MAX Files/*/Users"
rm -f "Design Files/MAX Files/*/MAXFILES.TXT"
```

### Phase 2: Remove Lock & Temp Files

| What | Why | Where |
|------|-----|-------|
| `.dwl`, `.dwl2` | AutoCAD lock files — created when a DWG is open | Every folder with DWGs |
| `.bak` | AutoCAD backup files — safe to remove when latest version is confirmed | CAD folders, Revit backup folders, As-Built Docs |
| `.DS_Store` | macOS Finder metadata | Every folder |
| `.lck` | General lock files | Various |

**Removal pattern:**
```bash
find . -name "*.dwl" -o -name "*.dwl2" | while read f; do rm "$f"; done
find . -name "*.bak" -type f | while read f; do rm "$f"; done
find . -name ".DS_Store" -delete
```

**CRITICAL:** NEVER use `rm -rf <folder>` — only `rm <file>` with explicit filenames. OneDrive propagates folder deletions immediately. See the CRITICAL SAFETY RULES in `samaya-technical-office` SKILL.md.

### Phase 3: Remove Duplicate ZIPS

ZIP files that were already extracted and remain as dead weight:

```bash
# Find all ZIPs
find . -name "*.zip" -type f

# Check: does a directory with the same basename exist?
# If yes — the ZIP is a duplicate of the extracted content — remove
rm -f "path/to/duplicate.zip"
```

Also check `Submittal's/Arch/` for .zip files whose extracted content already exists in a subfolder.

### Phase 4: Remove Inter-Project Documents

Documents from OTHER projects that accidentally got filed here. Check:
- `Reports & Meeting/` — PDFs with different project names
- Root-level PDFs with wrong project codes
- Any file whose filename mentions a different project

Search pattern:
```bash
find . -name "*Sada_Uhud*" -o -name "*other_project_name*" -type f
```

### Phase 5: Rename Generic Folders

| Old Name | Clean Name | Rationale |
|----------|-----------|-----------|
| `New folder` | `CAD-Sections` or context-appropriate | Generic, meaningless |
| `New folder (4)` | Remove entirely or rename | Version of generic |
| `waiting area` | `MAX-Waiting-Area` or `Waiting-Area-CAD` | Spaces, lowercase |
| `loby` | `Lobby` | Typo |
| `reception` | `Reception` | Capitalization |
| `cad meuseum` | `CAD-Museum` | Spaces, typo |
| `01/`, `01(2)/` | `Max-01/`, `Max-01-v2/` | Generic numbers |
| `MECH REV 6` | `Mech-Rev-6` | Mixed case, spaces |
| `to revit` | `To-Revit` | Spaces |
| `Reception- Lobby- wating Area Proposals` | `Reception-Lobby-Proposals` | Spaces, typos, inconsistent |
| `AV-Plan-And-Famlies-Al-Ghamama/AV-Plan-And-Famlies-Al-Ghamama/` | Flatten to single `AV-Plan-And-Famlies/` | Double-nested |

**Naming convention:** Title Case · No spaces (use hyphens) · No parentheses · No trailing spaces · Fix obvious typos

### Phase 6: Create Missing Template Folders

Compare the current directory against the template. Common missing items:
- `Docs/09_Registers/` (with all 15 register subfolders)
- `Time Scheduales/` (empty but should exist)

For `Docs/09_Registers/`, create ALL 15 subfolders:
```bash
mkdir -p "Docs/09_Registers/Drawing_Register" \
  "Docs/09_Registers/Submittal_Tracker_IFC_Log" \
  "Docs/09_Registers/Transmittal_Register" \
  "Docs/09_Registers/Material_Sample_Register_MSR" \
  "Docs/09_Registers/RFI_Register" \
  "Docs/09_Registers/AV_Interface_Register" \
  "Docs/09_Registers/BCF_Register" \
  "Docs/09_Registers/Design_Risk_Register" \
  "Docs/09_Registers/Key_Personnel_Register" \
  "Docs/09_Registers/Master_Register_Index" \
  "Docs/09_Registers/Penetration_Register" \
  "Docs/09_Registers/Procurement_Schedule" \
  "Docs/09_Registers/Project_Risk_Register" \
  "Docs/09_Registers/Subcontractor_Prequalification_Register" \
  "Docs/09_Registers/Subcontractor_RFI_Register" \
  "Docs/09_Registers/VE_Register"
```

### Phase 7: Verify Against Template

Final comparison:
```bash
ls -1 "/path/to/Template Folder/"
ls -1 "/path/to/Project/"
```

Keep project-specific extras (Email_Archive, NAVIS MODELS, PROJECT_EMAILS.md) — these are NOT junk, they're workflow artifacts. The template doesn't have them because it's generic.

## Pitfalls

### OneDrive safety: rm -rf is permanent
`rm -rf <folder>` deletes the entire folder through OneDrive cloud sync — unrecoverable. Always remove individual files by name/path: `rm path/to/file.ext`.

### Don't delete project-specific extras
`Email_Archive/`, `NAVIS MODELS/`, `.nwf` files, `PROJECT_*.md` — these are project workflow files, not structure deviations. Only remove them if the user explicitly asks.

### Don't delete CAD source files thinking they're junk
.bak files are safe to remove. But `.dwg`, `.dxf`, `.rvt`, `.rfa`, `.pdf` are project deliverables. Verify before any removal.

### Don't rename things by guessing
If you can't determine what a folder contains (e.g., `01/`, `New folder`), list its contents first. Check file names, dates, and extensions before choosing a name.

### OneDrive performance: mv is safe, cp hangs on cloud-only files
- `mv` renames on the same filesystem — works even on cloud-only files (no data transfer)
- `cp` reads file content — hangs on cloud-only files that need downloading first
- `rm` removes directory entry without reading data — safe

### Check for duplicate folders between root and subdirectory
Sometimes the same content exists in e.g. `Design Files/waiting area/` and `Design Files/MAX Files/waiting area/`. Use `ls -i` to check inode numbers — different inodes = actual duplicates. Remove the one in the less-appropriate location.

## Verification

After cleanup, verify:
- [ ] Top-level folders match template (minus project-specific extras)
- [ ] No `New folder`, `waiting area`, `loby` generic names remaining
- [ ] No `Program Files/`, `Users/` software artifacts
- [ ] No `.dwl`, `.dwl2` lock files
- [ ] No .bak files in non-archive folders
- [ ] No duplicate ZIPs of already-extracted content
- [ ] No documents from other projects
- [ ] `Docs/09_Registers/` exists with all 15 subfolders
- [ ] No `.DS_Store` files
- [ ] All folder names use consistent capitalization and hyphenation
