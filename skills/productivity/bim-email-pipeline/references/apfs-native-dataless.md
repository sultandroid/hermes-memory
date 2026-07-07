# APFS Native Compression — Dataless Without a Cloud Provider

Confirmed: 2026-06-11, entire `~/Documents/04_Outlook_Connection/` tree (mails/ + scripts/ files) entered `compressed,dataless` state **without** being on iCloud Drive or OneDrive.

## How This Differs From Cloud-Backed Dataless

| Attribute | Cloud-backed (iCloud / OneDrive) | APFS native compression |
|-----------|----------------------------------|-------------------------|
| Root cause | Cloud provider evicted local content to save space | APFS kernel-level compression / extent eviction |
| `ditto` workaround | Works (iCloud) | **Does NOT work** |
| `NSFileCoordinator` | Works (rehydration via fileprovi) | **Does NOT work** (no provider to rehydrate from) |
| `osascript` bypass | Works for some paths | **Does NOT work** |
| `brctl download` | Works (iCloud) | N/A (not a cloud file) |
| `lsof +D` | Shows file provider process | **Shows nothing** — no process holds the lock |
| Recovery | Cloud sync rehydrates on access | Needs disk space freed or system reboot |
| `com.apple.provenance` xattr | May be present | **Present** (set by Microsoft-signed apps) |

## Symptoms

```
# Every read tool returns the same error
cat file.md       → Error reading file.md
head file.md      → Error reading file.md
cp file.md /tmp   → fcopyfile failed: Resource deadlock avoided
python3 open()    → OSError: [Errno 11] Resource deadlock avoided
osascript read    → Error -36 (I/O error)
xattr -d, then read → still fails (xattr appears removed but isn't)
```

But `stat` and `mdls` still return correct metadata:
```
stat -x file.md   → Size: 590616 bytes (correct)
mdls file.md      → LogicalSize = 590616 (correct)
```

## Detection

```bash
ls -lO file.md
# Look for "compressed,dataless" in the flags column
# -rw-r--r--@ 1 user staff  compressed,dataless 590616 Jun 8 01:44 file.md

# Check extended attributes
xattr -l file.md
# com.apple.provenance     ← key marker

# Verify no process has the file open
lsof +D /path/to/directory/
# (empty output = filesystem-level lock, not process-level)

# Check disk space (trigger condition)
df -h /
# If capacity > 95%, APFS may evict local file extents
```

## Root Cause

APFS on macOS can mark files as `compressed,dataless` when:

1. The **disk is critically full** (>95% capacity). APFS evicts local extents to free space, leaving only the metadata stub. Unlike iCloud/OneDrive files, there is NO remote copy — the extents are purged in-place, and the file is effectively **lost until the system decides to reclaim the extent or the volume is remounted**.

2. A **Microsoft-signed or sandboxed app** (like Outlook) wrote the files using the `com.apple.provenance` entitlement. The provenance xattr marks these files as belonging to a protected app's data scope. When APFS later compresses them, the cron job process cannot read them because the provenance seal prevents rehydration outside the original app's sandbox.

## Why Existing Workarounds Fail on APFS Native Dataless

| Workaround | Why it fails |
|------------|-------------|
| `ditto --norsrc` | `fcopyfile()` uses the same `read()` syscall path APFS blocks |
| `NSFileCoordinator` | No file provider extension registered for these paths — coordinator just falls through to POSIX |
| `osascript open for access` | AppleScript's `read` also goes through the sandboxed POSIX path |
| `xattr -d com.apple.provenance` | APFS rejects the removal on sealed extents; `xattr -d` returns 0 spuriously |
| Python `os.open(..., O_RDONLY)` | Same syscall, same block |
| `mmap` | Maps via file descriptor — same `read()` gate |
| `sudo -u user cat` | User identity doesn't bypass APFS extent sealing |

## Workarounds That MAY Work (Not Tested From Cron)

1. **Free disk space below 90%** — APFS may rematerialize extents when space is available
2. **Reboot** — volume remount clears transient extent locks
3. **Move the directory out of Documents** — `~/Documents` may have special APFS flags (Desktop Documents sync)
4. **Run the pipeline as a user LaunchAgent** instead of a cron job — user-context processes have the `fileprovi` entitlement chain needed to read provenance-sealed files
5. **`fs_trim` or `diskutil apfs trim`** — may consolidate free space and allow extent recovery

## If All Workarounds Fail

If none of the above work (the common case from cron context), the pipeline must:

1. **Log the failure** — record which files were unreadable
2. **Fall back to file-name-only processing** — use `find -ctime` to detect new files by timestamp, compare basenames against BIM inventory, report counts without reading content
3. **Flag for manual intervention** — the files need to be read from a user-interactive session, or the disk needs maintenance

## See Also

- `references/icloud-onedrive-edeadlk.md` — for cloud-provider-backed dataless
- `references/ditto-icloud-workaround.md` — ditto workaround for iCloud only
- `references/nsfilecoordinator-workaround.md` — Swift NSFileCoordinator for iCloud
