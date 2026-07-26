# macOS OneDrive File Provider — Write Block

> Reference for `bulk-file-organization`. Covers the macOS File Provider extension write restriction that blocks ALL file writes to OneDrive volumes from terminal/Python/Finder.

## Symptom

Every write operation to a OneDrive-synced folder fails with:

```
Operation not permitted
```

This affects:
- `cp`, `mv`, `mkdir`, `touch`, `rmdir`
- `ditto`, `ditto --noextattr`, `install`, `rsync`
- Python `open('/path', 'wb')`, `shutil.copy2()`, `os.rename()`, `os.mkdir()`
- AppleScript `tell application Finder to duplicate` (error -8004)
- `cat src > dst` redirect, `sendfile` syscall

## What is NOT affected

- **Reads from local OneDrive files** — `cat`, `cp <source>`, Python `open().read()` work for hydrated files
- **Writes outside OneDrive** — `/tmp/`, `~/Desktop/`, `~/Documents/` work normally
- **Finder drag-and-drop** — dragging via Finder GUI works (through the File Provider's own sandbox)

## Root cause

macOS FileProvider extension sandboxes writes to its volume. Only the File Provider's own process and certain Apple-signed binaries can write. Terminal, Python, and even Finder via AppleScript are blocked.

OneDrive lives under `~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/` with `~/OneDrive - SAMAYA INVESTMENT` as a symlink. Both carry the same restriction.

## Detection

```bash
df /Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/
# → synthesised APFS volume

touch /path/to/onedrive/file.test
# → Operation not permitted
```

## Workaround — stage to /tmp/

Build the organized folder structure in `/tmp/` with a mapping document, then ask the user to drag into OneDrive via Finder:

```bash
mkdir -p /tmp/filed_project/Target/
cp /tmp/doc.pdf /tmp/filed_project/Target/
cat > /tmp/filed_project/_FILE_MAPPING.csv << 'EOF'
Source,Destination,Notes
doc.pdf,Target/Subfolder,CG response
EOF
open /tmp/filed_project/
```

## Comparison

| Operation | OneDrive | iCloud Drive |
|-----------|----------|--------------|
| `cp src dst` | Operation not permitted | Works after `rm -f dst` |
| `mkdir` | Operation not permitted | Works |
| `mv src dst` | Operation not permitted | Works |
| Python `open('wb')` | Operation not permitted | Works |
| Finder drag-drop | Works | Works |

## Best practice

1. Always stage file organization output to `/tmp/` when target is OneDrive
2. Generate a mapping CSV/MD file
3. Open the staged folder in Finder for the user
4. For updating existing OneDrive files, use the repo or temp location and let the user merge
