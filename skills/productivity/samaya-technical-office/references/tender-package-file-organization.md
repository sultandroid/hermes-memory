# Tender Package File Organization

## When to use

A completed tender package from a consultant/contractor (e.g., NRS) has been delivered as a folder dump. You need to:
- Fix spelling and naming inconsistencies across thousands of files
- Remove empty/orphan directories that overlap with numbered folders
- Normalize directory naming conventions (spaces → underscores, consistent casing)
- Find and handle duplicate files (stub deletions, content comparison)
- Generate a serialized file register (CSV index)
- Do all of the above safely on a OneDrive-synced directory

## Systematic workflow

### Phase 1: Reconnaissance

Always start by understanding the structure before touching anything:

```
# Top-level structure
ls -1 "<BASE>"

# Full directory tree (max depth)
find "<BASE>" -maxdepth X -type d | sort

# File counts per directory
for d in "$BASE"/*/; do echo "$(basename $d): $(find "$d" -type f | wc -l) files"; done

# Full file listing
find "<BASE>" -type f ! -name '.DS_Store' | sort
```

**Key things to check:**
- Are there empty dirs that duplicate numbered folders? (e.g., `Approval and Stamping` while `02_Approved_Stamped_Packages` exists)
- Is there a numbering gap in the top-level dirs? (e.g., 01, 02, 04, 05 — no 03)
- Are there overlapping folder categories?
- What's the total file count? (critical for OneDrive sync performance)

### Phase 2: Catalog all spelling/naming issues

Search systematically for common misspellings in both dir names and filenames:

```bash
# Common BIM/construction misspellings to check
MISSPELLINGS=("Visulizations" "Regester" "Basment" "Digram" "Schamatic"
              "Requierments" "Appencices" "Musuem" "Asser" "Oko-Tex")

for term in "${MISSPELLINGS[@]}"; do
    echo "=== $term ==="
    find "$BASE" -type d -iname "*${term}*" 2>/dev/null
    find "$BASE" -type f -iname "*${term}*" 2>/dev/null
done

# Also check for formatting issues
find "$BASE" -type f -name "*  *" 2>/dev/null          # double spaces
find "$BASE" -type f -name "* (1)*" -o -name "*_(1)*"  # Windows dup markers
find "$BASE" -type d -name "*  *" 2>/dev/null          # dirs with double spaces
find "$BASE" -type d -name "New folder" 2>/dev/null    # Windows default name
```

**Categorize by action type:**
| Category | Example | Action |
|----------|---------|--------|
| Dir spelling | `07_Visulizations` → `07_Visualizations` | Safe to rename |
| File spelling | `Drawing Regester.xlsx` → `Drawing Register.xlsx` | Safe to rename |
| Official doc ID | `MOC-Asser-SIC-*.pdf` (vs correct `MOC-MUS-ASE-*`) | DO NOT rename — sender's document control ID |
| Double spaces | `CCTV  Museum.dwg` → `CCTV Museum.dwg` | Safe to fix |
| Windows dup | `file (1).pdf` | Check if stub or real duplicate |
| Empty dir | `Approval and Stamping/` (empty) | Safe to remove |
| Generic name | `New folder/` | Rename descriptively |
| Trailing whitespace | `file .ext` | Safe to fix |

### Phase 3: Fix directory name spelling

Use `mv` on directories (safe — only renames the dir, contents move with it):

```python
import subprocess as sp, os

BASE = "/path/to/project"

# Define corrections
find_issues = [
    ("Visulizations", "Visualizations"),
    ("Digram", "Diagram"),
    ("Schamatic", "Schematic"),
    ("Requierments", "Requirements"),
    ("Appencices", "Appendices"),
    ("Musuem", "Museum"),
]

for wrong, correct in find_issues:
    # Use find -iname for case-insensitive search, -depth to handle nesting
    cmd = f'find "{BASE}" -depth -type d -iname "*{wrong}*" 2>/dev/null'
    r = sp.run(cmd, shell=True, capture_output=True, text=True)
    for dirpath in r.stdout.strip().split('\n'):
        if not dirpath:
            continue
        new_name = dirpath.replace(wrong, correct)
        # Clean ampersands and trailing spaces
        new_name = new_name.replace(' & ', ' and ')
        import re
        new_name = re.sub(r'  +', ' ', new_name)
        if new_name != dirpath:
            sp.run(['mv', '-n', dirpath, new_name])
```

### Phase 4: Fix file name spelling

Same pattern but for files:

```python
file_fixes = {
    "Regester": "Register",
    "Basment": "Basement",
}

for wrong, correct in file_fixes.items():
    cmd = f'find "{BASE}" -depth -type f -iname "*{wrong}*" 2>/dev/null'
    r = sp.run(cmd, shell=True, capture_output=True, text=True)
    for filepath in r.stdout.strip().split('\n'):
        if not filepath:
            continue
        dirpath, filename = filepath.rsplit('/', 1)
        new_filename = filename.replace(wrong, correct)
        new_path = f"{dirpath}/{new_filename}"
        if new_path != filepath:
            sp.run(['mv', '-n', filepath, new_path])
```

**⚠️ Rule:** Skip files where the misspelling is part of an **official document code** (e.g., `MOC-Asser-SIC-*`). These are the sender's document control IDs and must not be changed.

### Phase 5: Handle empty/overlapping directories

Identify directories that are empty AND overlap with numbered counterparts:

```bash
for d in "Approval and Stamping" "Latest Version (Drawing & Specs)" "Submittals"; do
    target="$BASE/$d"
    if [ -d "$target" ] && [ "$(find "$target" -type f | wc -l)" -eq 0 ]; then
        rm -rf "$target"
        echo "Removed empty: $d"
    fi
done
```

### Phase 6: Handle duplicate (1) files

Files with `(1)` in name are typically Windows auto-rename duplicates. Check each:

```python
# For each (1) file, check:
# 1. Is it a stub (0-4 bytes)? → Delete.
# 2. Does a matching original exist? → Compare MD5 hashes.
#    - Same hash → Delete duplicate.
#    - Different content → Keep both (different revisions).
# 3. No matching original? → Orphan — keep but flag in register.
```

### Phase 7: Normalize spacing conventions

```python
# Fix double spaces in filenames
cmd = f'find "{BASE}" -depth -type f -name "*  *"'
for fp in ...:
    dirpath, filename = fp.rsplit('/', 1)
    new_name = filename.replace('  ', ' ').strip()
    if new_name != filename:
        sp.run(['mv', '-n', fp, f"{dirpath}/{new_name}"])

# Fix dirs with spaces → underscores (for consistency with numbered dirs)
# Except: "Version 01/02/03" — keep semantic spaces
#        Vendor content dirs with natural English — evaluate case-by-case
```

### Phase 8: Generate serialized file register

Create a CSV index with all metadata and issue flags:

```python
import csv, os
from pathlib import Path

BASE = Path("/path/to/project")
OUTPUT = BASE / "01_Registers_and_Logs" / "File_Register_Index.csv"

with open(OUTPUT, "w", newline="", encoding="utf-8") as csvfile:
    w = csv.writer(csvfile)
    w.writerow(["Serial", "Category", "Subcategory", "FilePath", "FileName",
                 "Extension", "Size_KB", "Modified", "Issues"])

    for i, fp in enumerate(sorted(BASE.rglob("*")), 1):
        if not fp.is_file() or fp.name == ".DS_Store":
            continue
        rel = fp.relative_to(BASE)
        parts = rel.parts
        category = parts[0]
        subcategory = "/".join(parts[1:-1]) if len(parts) > 1 else ""
        size_kb = round(fp.stat().st_size / 1024)
        # Check issues (spelling, duplicates, formatting)
        issues = []
        fn_lower = fp.name.lower()
        if "regester" in fn_lower:       issues.append("SPELL")
        if " (1)" in fp.name:            issues.append("DUP")
        if "  " in str(rel):             issues.append("FORMAT")
        # ... add more checks as needed
        w.writerow([i, category, subcategory, str(rel.parent),
                     fp.name, ext, size_kb, mtime, "; ".join(issues)])
```

### Phase 9: Rebuild and verify

Run the register script again after all fixes to confirm no issues remain:

```bash
python3 build_register.py
# Check output for remaining ISSUES column entries
```

## Pitfalls

- **OneDrive sync sensitivity**: Bulk rename operations on 19,000+ files may trigger extended OneDrive sync. Work in batches if latency is a concern. `mv -n` (no-clobber) prevents accidental overwrites.
- **Official doc IDs vs local typos**: `MOC-Asser-SIC-*` files use 'Asser' as part of an official document numbering system from the sender. Renaming these would break traceability to the originating correspondence. Only rename clearly wrong text in non-document-ID filename segments.
- **`(1)` files with same size but different content**: Always check MD5 hash before deleting. Same byte count ≠ same file.
- **Stubs**: Files of 4 bytes or less that happen to have `(1)` in name are likely failed copies/empty stubs. Safe to delete.
- **Case sensitivity**: macOS APFS is case-insensitive by default. `find -iname` may return both `Visulizations` and `visualizations`. Account for this when verifying fixes.
- **Deep paths**: macOS has a path length limit (~1016 chars for APFS). Very long paths in `find` output may fail `mv`. Check with `find ... | awk '{print length, $0}' | sort -rn | head`.
- **Register size**: For 19,000+ files, the CSV register is ~2-3 MB. Skip `.DS_Store` and the register file itself to avoid recursion issues.

## Common misspellings found in NRS tender packages

| Wrong | Correct | Notes |
|-------|---------|-------|
| Visulizations | Visualizations | Common typo |
| Regester | Register | Spreadsheet naming |
| Basment | Basement | Missing 'e' |
| Digram | Diagram | Missing 'a' |
| Schamatic | Schematic | 'c' → 'ch' |
| Requierments | Requirements | 'i' before 'e' |
| Appencices | Appendices | 'c' → 'd' |
| Musuem | Museum | Reversed 'se' → 'se' |
| Asser | Aseer | Official doc ID — DO NOT rename |
