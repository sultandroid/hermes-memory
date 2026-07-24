# Plan Folder Cleanup Pattern

When a project's plan folder structure has accumulated duplicates, misclassified folders, and empty directories, use this pattern to clean up.

## Detection

1. List all folders in the plans directory
2. For each folder, count actual files (excluding `.DS_Store` and `._*` AppleDouble files)
3. Identify duplicates by comparing folder names for the same plan topic (e.g., multiple "Stakeholder" folders with different numbering)
4. Check each folder's content — some "empty" folders may have 1-2 files that need merging

## Classification

| Category | Action |
|----------|--------|
| **Real plan** (full structure, many files) | Keep as-is |
| **Duplicate** (same plan, fewer files) | Merge files into the real folder, then delete |
| **Misclassified** (not a plan) | Move to appropriate location (e.g., Method Statements → operational docs) |
| **Empty** (0 files) | Delete immediately |

## Merge Pattern

```bash
# Copy unique files from duplicate into real folder
cp -n "$DUPLICATE/01_Source_Files/"* "$REAL/01_Source_Files/"

# Delete duplicate
rm -rf "$DUPLICATE"
```

Use `cp -n` (no-clobber) to avoid overwriting existing files.

## Common Misclassifications

| Folder | Correct Location | Reason |
|--------|-----------------|--------|
| Method Statements | `04_Docs/03_Method_Statements/` | Operational documents, not management plans |
| RACI matrices | Under the relevant plan or `01_Registers/` | Cross-reference tool, not a standalone plan |
| Subcontractor deliverables | Under the relevant plan or `01_Registers/` | Deliverable tracking, not a plan |

## OneDrive Deadlock

When deleting folders on a OneDrive-synced path, the `rm -rf` may trigger "Resource deadlock avoided" errors. Kill OneDrive first, wait 30s, then proceed. Restart OneDrive after.
