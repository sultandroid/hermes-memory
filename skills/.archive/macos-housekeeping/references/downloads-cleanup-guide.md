# Downloads Cleanup Guide

## Common duplicate families

When scanning ~/Downloads (or similar), these file patterns appear frequently and are safe to consolidate:

### Excel version chains
- `*_FINAL.xlsx`, `*_FINAL_CORRECTED.xlsx`, `*_FINAL_ALL_MATCHED.xlsx`, `*_COMPLETE_V3.xlsx`
- `*_v2.xlsx`, `*_v2_1.xlsx`, ... `*_v2_7.xlsx`
- `* (1).xlsx`, `* (2).xlsx`, `* (3).xlsx`
- Keep the most recent by modification date or highest version number.

### Spreadsheet register dumps
- `Register Log_*.csv` files — each is a separate register type (RFI, NCR, Shop Drawings, etc.)
- These may all be exports from the same master workbook (`Register Log.xlsb`)
- Check with user before deleting: they may be actively used as individual registers.

### Temp/lock artifacts
- `~$*.xlsx`, `~$*.docx` — always safe to delete (Excel/Word crash recovery files)
- `~$*.*` at any depth under the target folder

## Presentation format for findings

```
**Folder:** ~/Downloads
**Total:** 902 MB, ~400 items

**Organized folders:**
| Folder | Size |
|--------|------|
| Images | 247 MB |
| Media  | 105 MB |
| ...    |       |

**Root-level files:**
- 2 PDFs, 1 audio, 1 app bundle, etc.

**Clutter identified:**
- Duplicate app: 254 MB (same WezTerm in " 2" folder)
- Temp files: 8 (~$*.xlsx)
- Version chains: 11 groups
```

## Ask pattern for ambiguous groups

```
| Group | Count |
|-------|-------|
| employee_list_*.xlsx | 10+ versions |
| overtime_january_2026*.xlsx | 6 versions |
| ... | ... |

Want me to nuke all old versions keeping only the latest from each group?
```
