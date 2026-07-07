# macOS `com.apple.provenance` EDEADLK Issue

## Background

Files under `~/Documents/04_Outlook_Connection/mails/` and `~/Library/CloudStorage/` sometimes return `EDEADLK` (Resource deadlock avoided, errno 11) on every read attempt — `cat`, `head`, `cp`, `python open()`, `write_file` all fail with `Resource deadlock avoided`.

**Two independent causes:**

| Cause | Paths affected | Detect via | Recovery |
|-------|---------------|-----------|----------|
| **OneDrive File Provider** holds file handles during sync. Files get `com.apple.provenance` xattr. | `~/Library/CloudStorage/OneDrive-*/` and sometimes `~/Documents/` (OneDrive Desktop app) | `ls -laO` shows `compressed,dataless` flags + `xattr -p com.apple.provenance` returns hex value | `NSFileCoordinator` (Swift), `killall OneDrive`, `/tmp + copy2` |
| **iCloud Drive APFS data purging** — macOS Desktop & Documents sync marks local file content as purgeable when free space is low. Files get `compressed,dataless` flags but **no** `com.apple.provenance` xattr. | `~/Documents/` (anywhere under Documents when iCloud Desktop & Documents sync is ON) | `ls -laO` shows `compressed,dataless`. `mdls` returns null for all kMDItemFS* dates. `brctl download <file>` succeeds. | `brctl download <file>` (iCloud-backed only) |

## Symptoms

Every tool/command fails:
- `cat`, `head`, `dd`, `cp` → `Resource deadlock avoided`
- `python open()` → `OSError: [Errno 11]`
- `write_file` → `Resource deadlock avoided`
- `read_file` (Hermes tool) → returns only `1|` (empty first line with line-number prefix) — file appears empty
- Even writing new files to the `mails/` directory may fail (directory-level lock propagation)

Removing the xattr (`xattr -d com.apple.provenance <file>`) does NOT fully fix it — the lock is from the File Provider extension holding handles, not the attribute itself. However, `xattr -cr <directory>` (recursive clear) can loosen the attribute layer enough for higher-level APIs to work.

**Effective workaround: NSFileCoordinator via Swift** — even when all POSIX calls fail, macOS's coordinated file access API can read locked files:

```swift
swift -e '
import Foundation
let url = URL(fileURLWithPath: NSString(string: "~/path/to/locked.md").expandingTildeInPath)
var error: NSError?
let coordinator = NSFileCoordinator(filePresenter: nil)
coordinator.coordinate(readingItemAt: url, options: .withoutChanges, error: &error) { readURL in
    do {
        let data = try Data(contentsOf: readURL)
        if let str = String(data: data, encoding: .utf8) { print(str) }
    } catch { print("Read: \(error)") }
}
if let e = error { print("Coord: \(e)") }
' 2>&1
```

This works because NSFileCoordinator engages proper macOS file coordination, negotiating locks with File Provider extensions instead of failing. Confirmed 2026-06-11: Swift NSFileCoordinator successfully read 590KB 23.md files and all script .py files that `cat`/`head`/`open()`/`Data(contentsOf:)` all failed on.

**Combined approach:** `xattr -cr <directory>` followed by NSFileCoordinator gives the best results — the clear removes the dataless/provenance markers and the coordinator handles any remaining lock negotiation.

## Detection

```python
import os
try:
    fd = os.open('/path/to/file', os.O_RDONLY | os.O_NONBLOCK)
    data = os.read(fd, 200)
    os.close(fd)
except OSError as e:
    if e.errno == 11:  # EDEADLK
        print("LOCKED by OneDrive File Provider")
```

## Apparent EDEADLK on non-dataless files (confirmed 2026-06-19)

A third variant not explained by the two causes above: a file with **real content on disk** (size > 0, no `compressed,dataless` flag, no `com.apple.provenance` xattr) still returns EDEADLK on every POSIX read attempt — including `cat`, `file`, `python open()`, and `python os.open(O_RDONLY)`.

**Observed:** `download_mails.py` (3057 bytes, size confirmed by `ls -la` and `stat`) returned:
```bash
$ file download_mails.py
# ERROR: cannot read `/Users/mohamedessa/Documents/04_Outlook_Connection/download_mails.py' (Resource deadlock avoided)
```

Yet `ls -laO` showed **no** `compressed` or `dataless` flags. The file had real content on disk.

| Aspect | Value |
|--------|-------|
| Size | 3,057 bytes |
| `ls -laO` flags | None (`-rw-r--r--@`, no `dataless` or `compressed`) |
| `st_blocks` | > 0 (content on disk) |
| `com.apple.provenance` xattr | Not checked at time of error |
| What fails | `cat`, `head`, `file`, `python open()`, `python os.open()` — all `[Errno 11]` |
| What works | `ls -la`, `stat -f`, directory listing |

**Hypothesis:** This is a POSIX lock held by the iCloud File Provider on a file that **was** recently written by a sandboxed process (e.g. Microsoft Outlook via AppleScript `save `). The file has content and no dataless flags because iCloud never purged it, but the File Provider maintains a kernel-level exclusive handle on the inode that blocks all readers — a state between "fully materialized" and "dataless placeholder" that the existing detection flow misses.

**Detection flow (updated):**
```bash
# Step 1: Check basic file info
ls -laO <file>
# If compressed,dataless → content purged (existing cases)
# If no special flags → could be in-between state

# Step 2: Try file command
file <file> > /dev/null 2>&1
# If "ERROR: cannot read (Resource deadlock avoided)" → locked at POSIX level

# Step 3: Check size AND blocks
stat -f '%z bytes, %b blocks' <file>
# If bytes > 0 and blocks > 0 → file has content but is POSIX-locked
# This is the 'apparent EDEADLK' variant

# Step 4: Recovery
# Same as com.apple.provenance recovery — NSFileCoordinator via Swift
# Kill OneDrive processes does NOT resolve this specific variant
```

## Fix

Restart OneDrive to release all handles:
```bash
killall "OneDrive" "OneDrive Sync Service" "OneDrive File Provider"
```

OneDrive auto-restarts via LaunchAgent. After ~10 seconds locks are released.

**⚠️ Does NOT fix `com.apple.provenance` kernel locks.** The provenance lock is enforced by macOS kernel on files created by sandboxed apps — it's not a OneDrive handle lock. Restarting OneDrive does not release it. The only workaround is NSFileCoordinator via Swift (see § above). Confirmed 2026-06-13: all 5 Outlook-downloaded attachment files remained locked after OneDrive restart.

## Key insight: os.listdir + os.stat bypass the lock

`ls -la`, `cat`, `head`, `cp`, and `open()` all trigger EDEADLK on dataless files. But **`os.listdir()` and `os.stat()` work** — they only read directory entries and metadata, never open the file handle:

```python
import os
mails = os.listdir('/path/to/mails/')          # works
st = os.stat('/path/to/mails/23.md')            # works — returns size, mtime
content = open('/path/to/mails/23.md').read()   # EDEADLK ❌
```

Use `os.listdir()` + `os.stat()` to enumerate files and read metadata (size, modification time) when OneDrive has files locked. Confirmed 2026-06-11: `os.listdir` and `os.stat` succeeded on all files in `~/Documents/04_Outlook_Connection/mails/` while every shell command and `open()` call failed.

## Reading locked .md files with `os.open()` + basic O_RDONLY

When `cat`, `head`, and `python open()` all fail with EDEADLK, `os.open()` with basic `O_RDONLY` (no special flags) can sometimes succeed — confirmed 2026-06-12 on a 457KB, 9,224-line `24.md` file that all shell commands could not read:

```python
import os
f = '/path/to/locked.md'
try:
    fd = os.open(f, os.O_RDONLY)          # basic flags — no O_NONBLOCK, no O_EXLOCK
    with os.fdopen(fd, 'r') as fp:
        content = fp.read()
    print(f'Read OK: {len(content)} chars')
except OSError as e:
    print(f'Still locked: {e.errno} {e.strerror}')
```

The technique works because `os.open()` with basic `O_RDONLY` bypasses Finder-level coordination in some OneDrive states where higher-level POSIX APIs (fopen, shell redirects) trigger the File Provider lock negotiation. It doesn't work on files with `st_blocks=0` (truly dataless placeholders) but does work on files that are partially materialized.

**Limitation:** Only works when the file has at least some blocks allocated (`os.stat().st_blocks > 0`). On pure dataless placeholders (`st_blocks == 0`), fall back to NSFileCoordinator via Swift.

## Group Containers path — alternative to CloudStorage

The `~/Library/CloudStorage/` symlink often shows zero-byte placeholders for OneDrive files. The **actually materialized copies** live under `~/Library/Group Containers/UBF8T346G9.OneDriveStandaloneSuite/`:

```bash
# CloudStorage path (often dataless placeholder):
#   ~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/.../file.md

# Group Containers path (materialized):
#   ~/Library/Group Containers/UBF8T346G9.OneDriveStandaloneSuite/
#     OneDrive - SAMAYA INVESTMENT.noindex/
#     OneDrive - SAMAYA INVESTMENT/.../file.md
```

When trying to read/write OneDrive files, always try the Group Containers path first — it accesses the actual sync cache where files have real content. The CloudStorage path is a File Provider extension integration point that presents placeholder stubs.

**Discovery command:**
```bash
find ~/Library/Group\ Containers/UBF8T346G9.OneDriveStandaloneSuite -name "PROJECT_MEMORY.md" 2>/dev/null
```
This quickly reveals all accessible PROJECT_MEMORY.md files across projects (Aseer, Zamzam, Masjid Alnoor, etc.) — confirmed 2026-06-13: found 5 PROJECT_MEMORY.md files here while all were unreadable via the CloudStorage path.

## `brctl download` — force-sync files on non-CloudStorage paths

For files outside `~/Library/CloudStorage/` that are stuck as OneDrive placeholders (e.g. files under `~/Documents/04_Outlook_Connection/`), `brctl download` can force a sync:

```bash
brctl download ~/Documents/04_Outlook_Connection/mails/pipeline_run_2026-06-11.md
sleep 3   # give it a moment — 2s was insufficient on Jun 17
```

After this, `cat`/`open()` usually work because the file content is actually on disk. Confirmed 2026-06-11: a 618-byte pipeline_run file went from blocks=0 to blocks=8 after `brctl download`, making it readable.

**⚠️ `brctl download` exit 0 ≠ file readable (confirmed 2026-06-17).** A freshly-created file (pipeline log written minutes earlier by download_mails.py, 2781 bytes with `com.apple.provenance` xattr) returned `brctl download` exit 0 AND lost its `dataless` flag (confirmed via `ls -laO`), but `cat`/`head`/`os.open()` ALL still failed with EDEADLK. Even `xattr -d com.apple.provenance` after `brctl download` did not release the kernel-level lock. The file remained unreadable for the entire session (45+ minutes).

Meanwhile, a larger file (24.md, 521KB, also with `com.apple.provenance` + `dataless`) from the same directory **became readable** after two `brctl download` attempts + a 3-second wait. **Same directory, same xattr, different outcome.**

**Hypothesis:** Newly-created files (written within minutes by Outlook-downloaded content) may have a stronger provenance lock that `brctl download` cannot immediately dissolve. Older files (written days ago) are more likely to be fully materialized by the same command. The `brctl download` exit code cannot distinguish these cases.

**Recovery sequence for EDEADLK on iCloud-backed files:**

```
# Step 1: Attempt materialization
brctl download <file>
sleep 3
cat <file> > /dev/null 2>&1 && echo "READABLE" || echo "STILL LOCKED"

# Step 2: If still locked, try xattr removal + second download
xattr -d com.apple.provenance <file> 2>/dev/null
brctl download <file>
sleep 3

# Step 3: If still locked after Step 2, fall back to NSFileCoordinator
# See "Effective workaround: NSFileCoordinator via Swift" below
```

**Limitation:** `brctl` is for Apple CloudDocs-backed paths only. It does **NOT** work on `~/Library/CloudStorage/` (OneDrive File Provider) paths:

```
Error Domain=BRCloudDocsErrorDomain Code=6
"Path is outside of any CloudDocs app library, will never sync"
```

Files under `~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/` use the OneDrive File Provider extension, not Apple CloudDocs, so `brctl` is useless there. Use NSFileCoordinator instead.

## Path distinction: iCloud Drive vs OneDrive vs local

Three file-state mechanisms exist on this system:

| Path prefix | Managed by | `compressed,dataless`? | Recovery |
|-------------|-----------|------------------------|----------|
| `~/Documents/04_Outlook_Connection/` | iCloud Drive (Desktop & Documents sync) | Yes — APFS data purged to save space | `brctl download <file>` (Apple CloudDocs) |
| `~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/` | OneDrive File Provider extension | Yes — placeholder for cloud file | `NSFileCoordinator` (Swift) — **only reliable option**. `rm` + `cp` works for dataless placeholders but **fails for `com.apple.provenance` kernel-locked files** (confirmed 2026-06-13). `cat src > dest` also fails on provenance-locked files. |
| Other local paths (e.g. `/tmp`) | No sync | No | Always accessible |

**Detection flow:**
```bash
# Step 1: Check flags
ls -laO <file>
# If "compressed,dataless" → file content is purged

# Step 2: Try brctl (works for iCloud-backed only)
brctl download <file> 2>&1
# If success + "blocks=N" after → iCloud Drive path. Wait 2s then read.
# If "Error Domain=BRCloudDocsErrorDomain Code=6" → OneDrive or other File Provider

# Step 3: Check xattr provenance
xattr -p com.apple.provenance <file> 2>&1
# If returns hex value → OneDrive File Provider lock
# If "No such xattr" + dataless → iCloud Drive purge
```

If all BIM files under `~/Library/CloudStorage/` are placeholders, fall back to writing pipeline_run logs to the local `~/Documents/04_Outlook_Connection/mails/` directory instead, and note the lock in the report.

## Writing new files to locked directories via /tmp

Direct writes to a locked mails/ directory can fail. Workaround: write to /tmp first, then `shutil.copy2()`:

```python
with open('/tmp/log.md', 'w') as f: f.write(content)
shutil.copy2('/tmp/log.md', '/path/to/mails/pipeline_run.md')  # often succeeds
```

The new file doesn't have the `dataless` attribute yet so the copy bypasses the lock. Works even when `cp` and direct `open(path, 'w')` on the mails/ path both fail.

## Replacing a dataless OneDrive file (rm + cp)

When a OneDrive file is stuck in `compressed,dataless` state and direct overwrite (`cp`, `shutil.copy2`, `write_file`) fails with `Resource deadlock avoided`, use rm+cp:

```bash
rm "/path/to/OneDrive/locked.md"
cp "/path/to/replacement.md" "/path/to/OneDrive/locked.md"
```

`rm` removes the dataless placeholder inode, and `cp` creates a fresh non-dataless file. The OneDrive sync engine then picks up the new file and uploads it. **Confirmed 2026-06-12** on `~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/.../PROJECT_MEMORY.md` — rm succeeded immediately and cp created a writable file where every other method had failed.

**⚠️ Limitation: does NOT work for `com.apple.provenance` kernel-locked files.** When the file was created by a sandboxed macOS app (e.g. Microsoft Outlook via AppleScript `save attachment`), the kernel tracks the file's provenance at the vnode level — not just as an xattr. Removing the xattr (`xattr -d com.apple.provenance`) does not release the kernel lock. `rm` succeeds (removes the inode) but all reads including `cp`, `cat`, and Python `open()` still fail with EDEADLK because the kernel blocks cross-provenance access. **Confirmed 2026-06-13**: all 5 files from `~/Documents/04_Outlook_Connection/mails/attachments/` (saved by Outlook) remained locked after `xattr -d` and `rm`+`cp` attempts. Only `NSFileCoordinator` via Swift could read them (see § above).

**Detection flow:**
1. `ls -laO <file>` — check for `compressed,dataless` flags
2. `xattr -p com.apple.provenance <file>` — if hex value returned → **kernel provenance lock** → NSFileCoordinator required
3. If no provenance xattr but still `compressed,dataless` → plain dataless placeholder → rm+cp or brctl works

⚠️ Risk: if OneDrive syncs the rm before the cp completes, the file briefly disappears for other users. Use only when no other method works and the file is not actively being edited by someone else.

## Cross-cloud deadlock (source = iCloud, dest = OneDrive)

**Confirmed 2026-06-13:** When source files are under `~/Documents/` (iCloud-synced via Desktop & Documents sync — confirmed by `com.apple.fileprovider.detached#B` xattr on the `~/Documents/` directory itself) and the target is under `~/Library/CloudStorage/OneDrive-*/` (OneDrive), both cloud systems contend for access, causing a **systemic EDEADLK** that blocks ALL read AND write operations:

- Source read: `cat`, `dd`, Python `open()`, `os.open()` — all fail with `[Errno 11]`
- Dest unlink: `os.unlink()` succeeds on the 0B OneDrive placeholder
- Dest write: `cp`, `shutil.copy2`, `os.rename()`, `cat src > dest` — all fail with `[Errno 11]`
- The OneDrive File Provider re-locks the directory entry immediately even after `os.unlink()` removes the placeholder

**Recovery:** Only `NSFileCoordinator` via Swift works for provenance-locked source files. For dest stubs that were unlinked but unreplaceable, log the file as "Exists as stub — may auto-sync from prior copy" — the 0B placeholder may get populated by OneDrive sync if a prior pipeline run already delivered content.

**Detection on the directory (not file) level:**
```bash
xattr -l ~/Documents/
# Returns: com.apple.file-provider-domain-id
#          com.apple.fileprovider.detached#B  ← confirms iCloud Directory sync
```

## Copying provenance-locked files from iCloud source to OneDrive target

Confirmed 2026-06-13: `~/Documents/04_Outlook_Connection/mails/attachments/` files (saved by Outlook, `com.apple.provenance` kernel-locked) cannot be directly copied to OneDrive. All methods fail:
- `shutil.copy2` → `[Errno 11]`
- `cp -p` → `Resource deadlock avoided`
- Python `os.open()` + `write()` → `[Errno 11]`
- `dd` → 0 bytes transferred
- `rm` dest stub + `cp` from source → still fails (provenance lock on source)

**Working sequence: NSFileCoordinator read → /tmp → cp to OneDrive:**

```bash
# Step 1: Read via Swift NSFileCoordinator, write to /tmp
cat > /tmp/read_coordinated.swift << 'SWIFT'
import Foundation
let src = URL(fileURLWithPath: "/path/to/iCloud/provenance-locked.pdf")
let dst = URL(fileURLWithPath: "/tmp/intermediate.pdf")
let coordinator = NSFileCoordinator(filePresenter: nil)
var error: NSError?
coordinator.coordinate(readingItemAt: src, options: .withoutChanges, error: &error) { readURL in
    do {
        let data = try Data(contentsOf: readURL)
        print("Read \(data.count) bytes")
        try data.write(to: dst)
        print("Written to /tmp")
    } catch { print("Error: \(error)") }
}
if let err = error { print("Coord error: \(err)") }
SWIFT
swift /tmp/read_coordinated.swift

# Step 2: cp from /tmp to OneDrive target
cp /tmp/intermediate.pdf "/path/to/OneDrive/target/file.pdf"
rm /tmp/intermediate.pdf /tmp/read_coordinated.swift
```

This works because NSFileCoordinator negotiates the kernel provenance lock at the macOS file coordination level, while POSIX `cp` to the OneDrive target (which has no provenance xattr) succeeds cleanly.

## Scripts that need NSFileCoordinator patching

| Script | Failure mode | Fix needed |
|--------|-------------|------------|
| `download_mails.py` — `append_to_weekly_file()` | Opens weekly `.md` archive files on iCloud Drive for append — crashes with `[Errno 11]` mid-archive, losing the email batch | Replace `f = open(path, 'a+')` with NSFileCoordinator read → modify content → NSFileCoordinator write, or use /tmp intermediate + shutil.copy2 |
| `compare_and_file.py` — `shutil.copy2()` / `cp -p` calls | Copies files from iCloud-synced `~/Documents/` attachments to OneDrive BIM target — all POSIX methods fail on provenance-locked source files | Add Swift NSFileCoordinator helper or fallback that reads via Swift and writes via `cp` from /tmp (see pattern above) |

Until patched, the pipeline can work around these by:
1. For `download_mails.py`: Run the script, expect crash on first lock, the queued emails remain in Outlook for next run
2. For `compare_and_file.py`: After script failure, manually copy using the NSFileCoordinator Swift pattern above

## Workaround during pipeline runs

If EDEADLK is encountered on the mails/ directory during a cron pipeline run:

1. Note it in the report but proceed — the pipeline itself (download_mails.py, fast_organize.py, project_organize.py) functions independently of file-level reads.
2. For metadata reads, use `os.listdir()` + `os.stat()` instead of shell commands.
3. Write pipeline_run records via the /tmp+copy2 workaround (above).
4. Existing `.md` digest content is unrecoverable while locked; do not retry in the same turn.
5. The pipeline scripts (download, organize) use their own Outlook API connections and are unaffected.
6. **For copying provenance-locked attachments to OneDrive**: Run the NSFileCoordinator Swift pattern manually after the scripts fail (see § above).
7. **Logging wins**: Write the pipeline run report to the local `~/Documents/04_Outlook_Connection/mails/` directory even if OneDrive targets are locked — local writes to iCloud Drive are less prone to EDEADLK than OneDrive writes.
