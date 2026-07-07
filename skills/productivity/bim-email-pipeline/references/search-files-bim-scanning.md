# BIM Scanning with search_files (ripgrep)

Alternative to `os.walk` for comparing attachment filenames against the BIM tree. Faster on large trees (14K+ files), handles OneDrive placeholders gracefully (only needs stat metadata, not file open).

## Why search_files instead of os.walk

| Aspect | os.walk | search_files |
|--------|---------|-------------|
| Speed | Slower on deep dirs with many files | Ripgrep-backed, millisecond scans on 14K files |
| OneDrive placeholders | Works (stat only), but Python recursion overhead | Works — rg uses stat too |
| Remote/symlinked paths | Can hit EDEADLK on traversal into CloudStorage symlinks | Only inspects the directory you point it to — avoids crossing provenance symlinks |
| Output shape | Raw list, needs normalization | Returns `files_only` mode with paths sorted by mtime |
| Integration | Requires manual dedup with attachments list | Use Python `set()` comparison on returned paths |

## Pattern

```python
from hermes_tools import search_files

# Step 1: Get all BIM files by scanning target folders
bim_files = set()
for target_path in BIM_TARGETS:
    result = search_files(
        pattern='*',
        target='files',
        path=target_path,
        limit=100000  # high enough to get everything
    )
    for entry in result['files']:
        # Extract just the filename, normalize for comparison
        fname = entry.split('/')[-1].lower()
        bim_files.add(fname)

# Step 2: Get attachments root (scoped to files only, NOT subdirs)
import os
attach_root = '/path/to/attachments/'
root_files = [f for f in os.listdir(attach_root) 
              if os.path.isfile(os.path.join(attach_root, f))]

# Step 3: Find new files
new_files = [f for f in root_files 
             if f.lower() not in bim_files]
```

## Benchmarks

Tested 2026-06-12: Scanning 7 BIM target folders (total ~14,300 files) via `search_files` completed in ~2 seconds total. Equivalent `os.walk` on same tree would take 15-30 seconds depending on Python overhead.

## Pitfall: search_files output_mode='count' for bulk scanning

When scanning a single very large folder, use `output_mode='count'` to get file counts per path without loading all filenames. For cross-reference comparisons, you need actual filenames, so use `output_mode='files_only'`.

## Pitfall: Arabic filename matching

When comparing filenames from search_files (utf-8 paths) against os.listdir output, normalize both sides:

```python
import unicodedata

def normalize_name(name):
    """Normalize Arabic filenames for comparison."""
    n = unicodedata.normalize('NFC', name).lower()
    # Map Arabic variants to base forms
    replacements = {
        '\u0623': '\u0627', '\u0625': '\u0627', '\u0622': '\u0627', '\u0671': '\u0627',  # Alef variants → ا
        '\u0649': '\u064a', '\u0626': '\u064a',  # Yeh variants → ي
        '\u0629': '\u0647',  # Teh Marbuta → ه
    }
    for src, dst in replacements.items():
        n = n.replace(src, dst)
    # Strip Arabic diacritics (Fatha, Damma, Kasra, etc.)
    import re
    n = re.sub(r'[\u064B-\u0652]', '', n)
    return n

bim_normalized = {normalize_name(f): f for f in bim_files}
attachments_normalized = {normalize_name(f): f for f in root_files}
new = [attachments_normalized[n] for n in attachments_normalized 
       if n not in bim_normalized]
```

## Linked from

Pipeline Execution Guide Step 4 — when using `search_files` for BIM comparison instead of Python `os.walk`.
