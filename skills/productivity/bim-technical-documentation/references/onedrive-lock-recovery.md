# OneDrive File Lock Recovery — `ditto` Workaround

## Problem

`write_file` overwrites the entire OneDrive-synced file, which OneDrive interprets as a completely new file. This triggers extended-attribute locks that make the file unreadable:

```
[Errno 1] Operation not permitted
```

`cp`, `cat`, `python3 open()`, `xattr -c` all fail.

## Solution: `ditto`

`ditto` (macOS built-in) bypasses the extended-attribute lock by cloning the file descriptor rather than reading byte-stream.

```bash
# Copy FROM locked OneDrive path (recovery source)
ditto "/original/onedrive/path/file.html" "/tmp/backup.html"

# Copy INTO locked OneDrive path (restore)
ditto "/tmp/backup.html" "/original/onedrive/path/file.html"
```

## Verification

```python
with open('/path/to/file.html') as f:
    print(len(f.read()))  # If [Errno 1], lock persists
```

If still locked, wait 3–5 seconds, then retry `ditto`.

## Prevention

- Never use `write_file` on OneDrive paths — always use `patch`
- `patch` does delta edits that OneDrive syncs gracefully
- For large section replacements, use `patch` with a multi-line `old_string` (even 200+ lines) rather than `write_file`
