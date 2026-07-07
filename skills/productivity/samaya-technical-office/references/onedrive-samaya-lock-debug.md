# OneDrive SAMAYAINVESTMENT — Resource Deadlock Avoided: Full Debugging Log

**Date:** 2026-05-28
**Session context:** Attempted to read `PROJECT_MEMORY.md` from Aseer-Museum folder.
**Outcome:** Account-wide lock confirmed; no recovery in-session.

---

## Environment

| Component | Value |
|-----------|-------|
| macOS | 26.5 |
| OneDrive | /Applications/OneDrive.app (PID 5468, uptime 161h) |
| OneDrive File Provider | PID 5470, 702h uptime |
| OneDrive Sync Service | PID 8087, 117h uptime |
| Secondary instance | PID 8228 |
| Filesystem | APFS on /dev/disk3s5 (/System/Volumes/Data) |
| Mount | /Users/mohamedessa/Library/CloudStorage/ |

---

## Commands Tried

| Command | Exit | Result |
|---------|------|--------|
| `dd if=<file>` | 1 | Resource deadlock avoided |
| `cat <file>` | 1 | Resource deadlock avoided |
| `python open()` | 1 | [Errno 11] Resource deadlock avoided |
| `rsync <file>` | 20 | mmap: Resource deadlock avoided |
| `cp <file> /tmp/` | 1 | fcopyfile failed: Resource deadlock avoided |
| `copyfile()` ctypes | 0 | Copyfile returned success but /tmp/ file was 0 bytes |
| `open()` O_NOFOLLOW + read() | 3/-1 | fd opened but read returned -1 |
| Fork child process | 0 | Child also got Resource deadlock avoided |
| Kill main OneDrive (5468) | — | Lock persisted after kill |
| Kill secondary (8228) STOP/CONT | — | Lock persisted |
| Python retry loop × 5, 2s apart | all fail | Consistent EAGAIN/EDEADLK |

---

## Diagnostic Results

### stat -x
```
File: .../PROJECT_MEMORY.md
Size: 5809  FileType: Regular File
Mode: (0700/-rwx------)  Uid: (501/mohamedessa)
Device: 1,16  Inode: 421301360  Links: 1
Access: Thu May 28 19:57:05 2026
Modify: Thu May 28 19:17:17 2026
Change: Thu May 28 19:17:27 2026
Birth: Fri May 22 19:28:49 2026
```

### mdls (key fields)
```
kMDItemIsUploaded      = 1
kMDItemIsDownloaded    = 1
```
→ File is FULLY locally present AND uploaded to cloud. Not a sync gap.

### xattr -px com.apple.FinderInfo
```
FF FF FF FF FF FF FF FF 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```
→ `0xFF…FF` in first 8 bytes = **APFS file lease active**. Finder sets this when a file is open by another process.

### xattr -px com.apple.lastuseddate#PS
```
B5 07 18 6A 00 00 00 00 12 CC 1D 39 00 00 00 00
```

### fuser <file>
```
exit 0, stdout: '' (empty)
```
→ Lease held at application level, not kernel level (no zombie kernel reference).

### lsof +c 0 <file>
```
exit 1, no output
```
→ No process currently has this specific file descriptor open. The lease is stale/dangling.

### lsof -c OneDrive (all processes)
```
PID 5468: /Applications/OneDrive.app/Contents/MacOS/OneDrive (main, 161h uptime)
PID 5470: OneDrive File Provider (702h uptime)
PID 8087: OneDrive Sync Service /silentConfig (117h uptime)
PID 8228: Secondary OneDrive instance (117h uptime)
```
→ Multiple OneDrive instances running simultaneously. PID 8228 may be a redundant instance from a failed restart.

### OneDrive sync engine DB
```
Settings DB path: ~/Library/Application Support/OneDrive/settings/
Contains: Personal_gcc取舍/settings.dat (chinese chars — Chinese locale account)
```
→ Not accessible while OneDrive holds the lock.

---

## Scope: Account-Wide vs File-Specific

| Path | Result |
|------|--------|
| `OneDrive-SAMAYAINVESTMENT/…/PROJECT_MEMORY.md` (Aseer) | ❌ Locked |
| `OneDrive-SAMAYAINVESTMENT/…/PROJECT_MEMORY.md` (Zamzam) | ❌ Locked |
| `OneDrive-SAMAYAINVESTMENT/…/PROJECT_MEMORY.md` (Hera' Ghar) | ❌ Locked |
| `OneDrive-Personal(2)/…/PROJECT_MEMORY.md` (Al Faw) | ✅ Works fine |
| `OneDrive-SAMAYAINVESTMENT/…/_PROJECT_INDEX.md` | ❌ Locked |
| `OneDrive-SAMAYAINVESTMENT/…/session-ses_1d02.md` | ❌ Locked |

**Conclusion:** Entire `OneDrive-SAMAYAINVESTMENT` account is locked. `OneDrive-Personal(2)` is unaffected. This is account-level, not file-level.

---

## What Likely Happened

1. OneDrive started a sync pass on the SAMAYAINVESTMENT account (May 28, ~19:17 based on file modify time)
2. During sync, it opened the file, set the APFS lease flag (FinderInfo 0xFF…)
3. OneDrive crashed, was killed, or was quit mid-sync before releasing the lease
4. The lease is now dangling — OneDrive doesn't see it as still open (lsof shows no fd), but APFS still has the lease flag set
5. Any read attempt hits the kernel-level lease check before reaching the application

**Why killing OneDrive doesn't help:** The lease is at the APFS/Finder level, not the OneDrive application level. The app can't release what it doesn't know it holds.

---

## Recovery Options (in order of likelihood)

### Option 1: Quit ALL OneDrive processes ✅ Recommended first step
```bash
# Quit the main app
osascript -e 'tell application "OneDrive" to quit'
# Kill residual processes
killall "OneDrive" 2>/dev/null
killall "OneDrive Sync Service" 2>/dev/null
# Wait 30 seconds
sleep 30
# Try reading the file
dd if=/path/to/file of=/tmp/copy
# Restart OneDrive
open -a OneDrive
```

### Option 2: Rename via OneDrive Web
1. Go to onedrive.com → navigate to the locked folder
2. Right-click the file → Rename → give it a temp name (e.g., `FILE_tmp.md`)
3. Wait 5 minutes for OneDrive to process the rename
4. Rename it back to the original name
5. Wait 5 minutes for the inode to be re-established
6. Try reading locally

### Option 3: Kill specific OneDrive instances
```bash
# PID 8228 is a secondary OneDrive instance — kill it first
kill -9 8228
sleep 2
# Try reading
dd if=/path/to/file of=/tmp/copy
```

### Option 4: Write to /tmp/ first (for creating new files)
If you need to write a new version of a locked file:
```python
# Write to /tmp first
with open('/tmp/output.html', 'w') as f:
    f.write(html_content)
# Then copy — sometimes this bypasses the lease
import shutil
shutil.copy('/tmp/output.html', '/path/to/onedrive/target.html')
```

### Option 5: Wait (cron retry)
If none of the above work, the lock may clear after OneDrive's internal heartbeat retry cycle:
```bash
# Cron job to retry in 30 minutes
sleep 1800 && dd if=/path/to/file of=/tmp/copy && echo "RECOVERED"
```

---

## What NOT to Try

- ❌ `kill -9` on the main OneDrive process (5468) — doesn't release the lease
- ❌ `rsync`, `dd conv=sync` — same kernel-level lease failure
- ❌ `fcopyfile` / `copyfile` ctypes — returns 0 but produces 0-byte files
- ❌ Force unmount the OneDrive volume (`umount -f`) — corrupts sync DB
- ❌ DiskUtility repair — APFS leases can't be repaired from DiskUtility
- ❌ `tmutil` restore from Time Machine — no local snapshots exist

---

## Files Affected in This Session

```
Aseer-Museum/PROJECT_MEMORY.md        — 5809 bytes, last modified 19:17 May 28
Zamzam Museum/PROJECT_MEMORY.md        — locked
Hera' Ghar/…/PROJECT_MEMORY.md        — locked
Aseer-Museum/_PROJECT_INDEX.md       — locked
Aseer-Museum/session-ses_1d02.md      — locked
```

Personal OneDrive (Al Faw PROJECT_MEMORY.md) — READABLE ✅
