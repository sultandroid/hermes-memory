# Arabic Folder Names & Unicode Space Characters

## The Problem

When Codex writes Python scripts that rename folders with Arabic names on macOS, the script may fail to match actual folder names because macOS/APFS uses **non-breaking space characters** (0xC2 0xA0 in UTF-8 = U+00A0) in place of or alongside regular spaces (0x20).

## Detection

Use `xxd` to inspect the actual bytes of the folder name:

```bash
ls /path/to/dir/ | grep "keyword" | xxd
```

Compare: a regular space is `20`, a non-breaking space is `c2 a0`.

## Reproduction Pattern

1. Codex writes a Python rename script with folder names hardcoded using regular spaces
2. The actual folder on disk has non-breaking spaces (e.g., `بمركز زوار سدايا ب` — space + NBSP before "سدايا")
3. `os.path.isdir()` returns False for the Codex-generated name because the strings don't match byte-for-byte
4. The folder gets silently skipped ("Skipped missing: ...")

## Fix Options

### Option A: Detect and handle (preferred)
Before renaming, scan the directory with `os.listdir()` and do fuzzy matching:

```python
import unicodedata

def normalize_spaces(name):
    """Replace all Unicode space varieties with regular space."""
    return ''.join(
        ' ' if unicodedata.category(c) == 'Zs' else c 
        for c in name
    )
```

### Option B: Manual remap
After Codex runs, use `ls | grep` with the imperfect name to capture the exact byte sequence, then `mv "exact" "XX. exact"`:

```bash
EXACT=$(ls /path/to/dir/ | grep "partial_name")
mv "$EXACT" "05. $EXACT"
```

### Option C: Read from disk (most robust)
Have Codex write a script that first reads actual folder names from the directory, then maps them:

```python
actual_folders = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f)) and not f.startswith('.')]
# Then match by heuristics (substring, remove all spaces, etc.)
```

## Why It Happens

- macOS APFS supports Unicode normalization forms
- OneDrive sync / copied-from-Windows folders often have NBSP characters where users typed space+space or shift+space
- Terminal `ls` output looks identical — visual inspection won't reveal the difference
- Python string comparison is byte-exact, so `" "` (0x20) ≠ `"\u00a0"` (0xC2 0xA0)

## Applicable Contexts

- Arabic, Farsi, Urdu folder names in construction/tendering projects
- Any OneDrive-synced directory with non-ASCII names
- macOS filesystems where folders were created or manipulated by multiple OSes
