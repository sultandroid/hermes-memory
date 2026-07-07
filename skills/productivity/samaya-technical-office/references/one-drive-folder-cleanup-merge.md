# OneDrive Folder Cleanup & Merge Pattern

## When to use
A project has duplicate or legacy folders at root level that duplicate content in the canonical Docs/ structure (e.g., `Submittals/` at root vs `Docs/03_Submittals/`).

## Canonical structure (Aseer template)
```
Docs/
  00_Project_Charter/
  01_Contracts_and_ER/
  02_Plans_and_Procedures/   (02.1_DMP, 02.2_BEP, ..., 02.6_NRS_Methodology, 02.7_...)
  03_Submittals/             (03.1–03.7 numbered subfolders)
  04_RFIs/
  05_SIs/
  09_Registers/
  ...
Subcontractors/
  01_Replica ... 12_MEP_Installation ... 18_MEP_Designer
  _ARCHIVE/
```

## Merge steps

1. **Classify source content**
   - Date-based packages → `Docs/03_Submittals/03.7_Submittal_Packages/`
   - Arch drawings → `03.6_Architectural_Submittals/`
   - Engineering (MEP, Struc, AV) → `03.2_IFC_Packages/`
   - Design submittals → `03.1_Design_Submittals/`
   - Reviews / analysis → `_Analysis/`
   - Reports → `_Analysis/Reports/`
   - Templates not fitting submittals → `Docs/00_Project_Charter/`

2. **Handle name collisions** (same filename in source and dest)
   - If sizes match → compare MD5 or sha256
   - If hash matches → delete source (true duplicate)
   - If hash differs → rename source with date prefix, move

3. **Move discipline folders with `mv`** (atomic on same OneDrive mount)
   ```bash
   mv "Submittals/Arch" "Docs/03_Submittals/03.6_Architectural_Submittals/"
   ```
   If `mv` fails with "Directory not empty", merge sub-items individually.

4. **Handle loose root-level files** — move all to a `_Legacy_Loose/` subfolder.

5. **Clean up empty source** — remove `.DS_Store`, then `rmdir`.

## Pitfalls
- **NEVER use `rm -rf`** on OneDrive paths. Only `rm <file>` for individual files, `mv` for whole dirs.
- **OneDrive sync can timeout** on large `cp -r` operations. Use `mv` instead.
- **Zero-byte files** are OneDrive sync stubs. Delete them, not the real file in dest.
- **OS metafiles** (`.DS_Store`, `Thumbs.db`) are often the only leftovers. `rm` then `rmdir`.
- **Document the move** — search for old path strings in `.md` files before/after.
