# OneDrive EDEADLK — Resource Deadlock Avoided

## Symptom

Any attempt to read a cloud-only OneDrive file fails with:

```
Resource deadlock avoided
[Errno 11] Resource deadlock avoided
```

OS-level error: `EDEADLK (11)` — macOS OneDrive File Provider returns this for files whose content is not downloaded locally.

## Detection

```bash
# Check if a file is cloud-only
mdls -name com_apple_provenance_isDownloaded /path/to/file.pdf
# → com_apple_provenance_isDownloaded = 0  (cloud-only)
# → com_apple_provenance_isDownloaded = 1  (downloaded locally)

# Check if download is in progress
mdls -name com_apple_provenance_isDownloading /path/to/file.pdf

# Check extended attributes
xattr -l /path/to/file.pdf | grep provenance
```

## What fails (everything)

| Method | Result |
|--------|--------|
| `cp`, `cp -X`, `cp -c` | EDEADLK |
| `ditto`, `ditto --noextattr` | EDEADLK |
| `rsync --inplace` | EDEADLK |
| `tar` / `cat > file` | EDEADLK |
| `ln` (hardlink) | EDEADLK |
| `dd` | EDEADLK |
| `head`, `cat`, `file` CLI | EDEADLK |
| Python `open().read()` | EDEADLK (open succeeds, read fails) |
| Python `shutil.copyfile()` | EDEADLK |
| `brctl download` | May work, often returns silently |
| Finder double-click | Downloads the file |

## No shell-level workaround

Once a file is in cloud-only state with `isDownloaded=0`, no piped/copied read operation succeeds through the shell. The file provider extension holds an exclusive lock. Even `os.open()` succeeds but `os.read()` on the descriptor returns EDEADLK.

## Detection via stat (alternative to mdls)

```bash
# Returns "-" when fully local, "compressed,dataless" when cloud-only
stat -f "%Sf" /path/to/file.pdf
```

More reliable than `mdls` for OneDrive — works even when `mdls -name com_apple_provenance_isDownloaded` returns `(null)`.

## iCloud vs OneDrive: key differences

| Aspect | OneDrive | iCloud Drive |
|--------|----------|--------------|
| Deadlock on read | `cp`, `cat`, `Python open().read()` all fail with EDEADLK | Same — EDEADLK, plus `file` and `stat` also fail |
| `brctl download` | **Does NOT work** — returns "Path is outside of any CloudDocs app library" error | Works |
| `stat -f "%Sf"` | Returns `-` (local) or `compressed,dataless` (cloud) | Returns `-` or `compressed,dataless` |
| Safe operations | `find`, `ls -la`, `stat` on filenames, directory listing | `find`, `ls` (but `stat` fails) |
| Python read via AppleScript | Fails (same EDEADLK) | May work |
| Delete-and-copy workaround | `os.remove()` + `cp -X` | **`rm -f` + `cp` WORKS** — produces correct file size (unlike `cat >` which races with sync engine) |
| **`read_file` tool** | Returns EDEADLK error | Returns **empty content** (no error, just blank) — the tool's dedup cache then returns "unchanged" on retry, masking the problem |
| **`osascript -e 'do shell script "cat ..."'`** | Fails (EDEADLK) | Also fails — returns empty string with exit 0 |
| **Python script via `osascript -e 'do shell script "python3 /tmp/script.py"'`** | Fails | **WORKS** — AppleScript's `do shell script` bridges permissions and can read iCloud files that direct shell access cannot |

## iCloud-specific detection

When `read_file` returns empty content and `file` command says "cannot read (Resource deadlock avoided)", the file is an iCloud dataless stub. The `read_file` tool's dedup cache then reports "unchanged" on subsequent reads, making it look like the file is empty. **Workaround:** Write a Python script to `/tmp/` and execute it via `osascript -e 'do shell script "python3 /tmp/script.py"'` — this bypasses the iCloud file provider lock.

## Solutions

1. **Force download via Finder**: open the containing folder in Finder — files auto-download on access.
2. **OneDrive manual sync**: right-click → "Always keep on this device"
3. **`brctl download`** (sometimes works):
   ```bash
   brctl download --progress /path/to/file.pdf
   ```
4. **Delete-and-copy (rm -f + cp)** — removes the iCloud stub, then cp uses fcopyfile which handles the replacement atomically. This works (unlike cat > which races with the sync engine and produces 0-byte stubs). Confirmed: rm -f <target> && cp <source> <target> produces correct file size.
5. **Prevent the problem**: ensure OneDrive is set to "Download all files" or mark target folders as "Always keep on this device" in OneDrive preferences.

## BIM scanning workaround: list-only matching

When comparing attachments against BIM OneDrive folders, **do NOT try to read file contents**. Instead, use `find` for filename-based matching:

```bash
# Check if a file exists in BIM (works on OneDrive without EDEADLK)
find "/path/to/Bim/Unit" -iname "MOC-MUS-ASE-*.pdf" 2>/dev/null

# Get all filenames in a BIM folder tree for bulk comparison
find "/path/to/Bim/Unit/Aseer-Museum" -type f -print 2>/dev/null > /tmp/bim_files.txt
```

### Python bulk-comparison approach (preferred for Arabic filenames)

```python
import subprocess, unicodedata, difflib, os

def list_bim_files(bim_root):
    """Get all filenames (not full paths) from BIM using find."""
    result = subprocess.run(
        ["find", bim_root, "-type", "f"],
        capture_output=True, text=True, timeout=120
    )
    # Extract just filenames, normalize for matching
    names = set()
    for path in result.stdout.strip().split("\n"):
        name = os.path.basename(path)
        names.add(normalize_arabic(name))
    return names

def normalize_arabic(name):
    name = unicodedata.normalize("NFC", name).lower()
    for variant in "أإآٱ":
        name = name.replace(variant, "ا")
    name = name.replace("ى", "ي").replace("ئ", "ي")
    name = name.replace("ة", "ه")
    for c in name:
        if 0x064B <= ord(c) <= 0x0652:
            name = name.replace(c, "")
    return name

def is_already_filed(filename, bim_files, threshold=0.9):
    norm = normalize_arabic(filename)
    if norm in bim_files:
        return True
    for bf in bim_files:
        if difflib.SequenceMatcher(None, norm, bf).ratio() > threshold:
            return True
    return False
```

Key: `find` only reads directory metadata, never file contents, so it never triggers EDEADLK on OneDrive.

## Why it happens

macOS's FileProvider extension (com.apple.fileservices.FileProvider) manages cloud storage on behalf of OneDrive. When a file is "online-only" (the default for newly synced folders), the kernel delegate yields EDEADLK to signal "I can't serve this content right now without blocking the caller indefinitely." This is by design — it prevents the kernel from blocking on network I/O.
