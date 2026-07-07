# iCloud + OneDrive EDEADLK During Pipeline Runs

## Symptom

During cron runs, terminal commands fail with:
```
Resource deadlock avoided
```
on any file inside:
- `~/Documents/04_Outlook_Connection/` (iCloud Drive)
- `~/Library/CloudStorage/OneDrive-*/` (OneDrive File Provider)

AppleScript returns I/O error -36.

## Root cause

macOS cloud storage providers (both iCloud Drive and OneDrive File Provider) acquire exclusive file locks during sync operations. Any filesystem read attempt — `cat`, `head`, `cp`, `ditto`, `rsync`, `hexdump`, `file`, `python3 open()`, `os.read()`, even `osascript open for access` — can fail with `EDEADLK` (Error 11 on Linux, Error -36 on macOS).

The error is **transient**: it resolves once the cloud provider finishes its sync cycle. It is NOT permanent — retrying later works.

This affects all files that are "cloud-only" (not yet downloaded locally) OR files being actively synced.

## Detection

```bash
# Check if it's an iCloud-backed path
brctl status ~/Documents/04_Outlook_Connection/ 2>&1 | head -5

# Check OneDrive download status
mdls -name com_apple_provenance_isDownloaded /path/to/file

# Simple test — if `wc -c` works but `cat` fails, it's a cloud lock
wc -c /path/to/file  # succeeds (size known)
cat /path/to/file    # fails (content not available)
```

## Workarounds (priority order)

### 1. AppleScript shell execution (works on both iCloud + OneDrive)

When shell commands fail to read files, `osascript -e 'do shell script "..."'` can still execute Python scripts:

```bash
osascript -e 'do shell script "python3 ~/Documents/04_Outlook_Connection/scripts/download_mails.py 2>&1"'
```

This uses a different I/O path (launchd → sandbox-extended) that bypasses the kernel lock.

### 2. Time-based change detection (works when content unreadable)

Use ctime/mtime (metadata lives in directory index, not file content) to detect new files:

```bash
# Files changed in last day (regardless of readability)
find ~/Documents/04_Outlook_Connection/mails/attachments -type f -ctime -1

# Files newer than a reference
find ~/Documents/04_Outlook_Connection/mails/ -name "*.md" -newer /tmp/last_run.md

# Files modified after a timestamp
find ... -newermt "2026-06-10 19:00"
```

### 3. BIM folder comparison without reading files

To check if an attachment is already filed:

```bash
base=$(basename "$file" | sed 's/\.[^.]*$//')
found=$(find "/path/to/Bim/Unit/Project" -name "${base}*" -type f 2>/dev/null | head -1)
if [ -z "$found" ]; then echo "NOT IN BIM"; fi
```

### 4. Python script execution (OneDrive only)

Python can execute `.py` files from cloud-locked directories:

```bash
python3 ~/Documents/04_Outlook_Connection/scripts/fast_organize.py 2>&1
```

This works because the interpreter loads via mmap + execute, bypassing the read lock.

### 5. Brctl force download

```bash
brctl download /path/to/file  # iCloud
# For OneDrive, no equivalent — wait for sync to finish
```

## Confirmed on

- macOS 26.5.1
- OneDrive 25.x (File Provider extension)
- iCloud Drive (Documents sync enabled)
- All shell commands: bash, zsh, python3 subprocess, AppleScript shell

## See also

- `outlook-email` skill's `references/onedrive-edeadlk.md` for dedicated OneDrive diagnostics
- The `outlook-email` pitfall "iCloud + OneDrive EDEADLK on cloud-only files" section
