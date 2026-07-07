# OneDrive Dataless File Diagnostics

When OneDrive files appear in `ls` with non-zero sizes but cannot be read (0 bytes returned by `cat`, `head`, etc.), they are **dataless placeholders** — the content exists only in the cloud.

## Detection

```bash
# The `dataless` flag in ls output
ls -laO file.md
# → -rw-r--r--@ 1 user  staff  compressed,dataless 2707 file.md

# 0 blocks allocated but non-zero size
stat -f "%b %z %N" file.md
# → 0 2707 file.md   (0 blocks = no local data)
```

## Diagnosis via File Provider

The most precise diagnostic tool is `fileproviderctl evaluate`:

```bash
fileproviderctl evaluate /path/to/file.md
```

Key fields in the output:

| Field | Meaning | Implication |
|-------|---------|-------------|
| `isDownloaded = 0` | Content not on local disk | Can't read the file |
| `isDownloading = 0` | Not currently downloading | Won't auto-resolve |
| `isUploading = 1` | Waiting to upload to cloud | **Stuck state** — content was evicted before upload |
| `isKeepDownloaded = 0` | Not pinned locally | User hasn't chosen "Always Keep" |
| `isDownloadRequested = 0` | No download queued | OneDrive isn't trying |
| `isUploaded = 0` | Not uploaded to cloud | Cloud has no copy either |
| `mostRecentVersionDownloaded = 0` | No version synced | Truly orphaned |

## State: Stuck Uploading

The most common stuck state encountered:

- `isUploading = 1` + `isDownloaded = 0` = **orphaned placeholder**
- The file was created/modified locally
- The local data was evicted (put online-only) before upload completed
- The upload never finished
- **Result:** File can never be materialized from terminal. Only recovery: re-create the file from source or check OneDrive web.

## Approaches That Do NOT Force Materialization

All of these were attempted and returned 0 bytes for dataless files (unless noted otherwise):

| Approach | Tool/API | Result |
|----------|----------|--------|
| Basic read | `cat`, `head -c`, `dd` | 0 bytes |
| Copy | `cp`, `ditto` | Fails or 0 bytes |
| File coordination | `NSFileCoordinator` (Swift) | 0 bytes |
| Raw fd | `os.open(os.O_RDONLY)` | 0 bytes |
| Finder open (non-native) | `open -a TextEdit file.pdf` | Opens blank — TextEdit can't read PDF |
| URL cache | NSURLCache | No cached content |
| Spotlight | `mdfind`, `mdls -name kMDItemTextContent` | null |

## Recovery Options

1. **`open <file>` in its native app** — triggers macOS LaunchServices to hand the file to its default handler (e.g. Preview for PDFs). Once the app opens and reads the content, OneDrive hydrates the local copy. The `dataless` flag disappears and the file becomes a regular file that can be `mv`-ed or `cp`-ed. **Wait a few seconds after opening** before attempting to move. Works even when `cp`/`ditto`/`cat` all return 0 bytes. Does NOT work when opening via a non-native app (e.g. `open -a TextEdit file.pdf` — opens blank).
2. **Finder → Right-click → Always Keep on This Device** — triggers download if cloud copy exists
3. **OneDrive web** (onedrive.live.com) — check if the file actually exists in the cloud
4. **Check other OneDrive accounts** — the user may have multiple OneDrive mounts (Personal, Business1, Business2, old syncs)
5. **Search all OneDrive paths** for the file:
   ```bash
   find ~/Library/CloudStorage/ -name "filename*" -maxdepth 6 2>/dev/null
   ```
6. **Re-create** — if the file was never uploaded (isUploading=1 + isUploaded=0), the content is lost locally

## Renaming OneDrive Items (Critical: Method Matters)

When renaming OneDrive-managed folders or files, the method determines whether the rename syncs to the cloud:

### Methods compared

| Method | File Provider | Sync result |
|--------|---------------|-------------|
| `mv old new` / `os.rename()` | **Bypasses** File Provider entirely | ❌ Stays local |
| `cp old new && rm old` | Copy triggers materialization → hangs on dataless | ❌ Hangs |
| AppleScript `set name of folder` | Partial — goes through Finder's FS layer | ⚠️ May fail if items are stuck |
| `URLResourceValues.name` via Swift `.setResourceValues` | Uses proper `FPItem` rename API | ✅ Best local option |
| OneDrive web UI (onedrive.live.com) | Direct cloud rename — no local coordination needed | ✅ Always works |

### Swift renaming code (preferred local method)

```swift
import Foundation
let fm = FileManager.default
let oldURL = URL(fileURLWithPath: "/path/to/folder")
var rv = URLResourceValues()
rv.name = "01. New Name"
try oldURL.setResourceValues(rv)  // Notifies File Provider
```

Save as a `.swift` file and run with `swift /path/to/script.swift`.

### AppleScript alternative (runs via Finder)

```applescript
tell application "Finder"
    set theFolder to POSIX file "/path/to/folder" as alias
    set name of theFolder to "01. New Name"
end tell
```

Run with: `osascript /path/to/script.applescript`

### Troubleshooting stuck renames

If after renaming the File Provider still shows `isUploading=1, isUploaded=0`:

1. **Restart OneDrive** — quit and re-open the OneDrive app
2. **Check File Provider** — restart the OneDrive File Provider extension:
   ```bash
   kill -TERM $(pgrep -f "OneDrive File Provider")
   ```
   macOS automatically restarts it.
3. **If still stuck** — the item is in an orphaned sync state. **No local method will sync it.** Use OneDrive web.
4. **Chicken-and-egg problem** — if children inside a folder are dataless, the parent folder's rename won't sync. OneDrive refuses to process folder renames until children are synced, but children can't sync.

### Renaming multiple folders (batch pattern)

```swift
let basePath = "/path/to/parent"
let pairs: [(String, Int)] = [
    ("Old Name 1", 1), ("Old Name 2", 2), ...
]
for (name, num) in pairs {
    let serial = num < 10 ? "0\(num)" : "\(num)"
    let newName = "\(serial). \(name)"
    let oldURL = URL(fileURLWithPath: basePath + "/" + name)
    var rv = URLResourceValues()
    rv.name = newName
    try oldURL.setResourceValues(rv)
}
```

### ⚠️ Cascade Corruption from Batch mv Renames

**Observed in production (May 31, 2026):** Batch-renaming 19 folders inside a OneDrive parent using shell `mv` corrupted ALL 22 folders — including 3 that were never touched.

**Error signature on every sibling (even untouched):**
```
isUploading = 1
isUploaded = 0
uploadingError = "Error Domain=NSCocoaErrorDomain Code=4 \"The file doesn't exist.\"
                  UserInfo={NSUnderlyingError=... {OneDrive Code=-2 \"(null)\"}}"
```

**Root cause:** `mv` bypasses the File Provider extension. OneDrive's sync engine tracks items by internal identifiers tied to cloud names. When you `mv` a folder, OneDrive still thinks the old-name item exists and hasn't been told about the new-name item. But more insidiously, this confuses the parent folder's sync context so badly that even items with unchanged names become orphaned. The parent directory's item list is corrupted.

**Repair pattern:**
1. **Revert all renamed folders** back to their original names exactly matching the cloud
2. **Restart OneDrive app** — quit and re-open to clear the stuck state
3. **Verify** — `fileproviderctl evaluate <path>` on each folder should show `isUploading=0, isUploaded=1`
4. **Rename on OneDrive web** — ONLY use onedrive.live.com for renames going forward
5. **One folder at a time** — do not batch; let each rename sync before doing the next

```bash
# Quick health check after repair
BASE="/path/to/parent"
for d in "$BASE"/*/; do
  name=$(basename "$d")
  status=$(fileproviderctl evaluate "$d" 2>&1)
  isUp=$(echo "$status" | grep "isUploading" | grep -oE "[01]")
  isDone=$(echo "$status" | grep "isUploaded" | grep -oE "[01]")
  err=$(echo "$status" | grep -c "uploadingError")
  if [ "$isUp" = "1" ] || [ "$err" != "0" ]; then
    echo "STUCK: $name"
  else
    echo "OK:    $name"
  fi
done
```

## Prevention: Avoiding Stuck Renames

Before batch-renaming OneDrive folders:

1. **Check sync health first:**
   ```bash
   fileproviderctl evaluate "./Folder Name" | grep -E "isDown|isUp|isKeep"
   ```
2. **Verify all children are healthy** — folders containing dataless files won't rename-sync
3. **NEVER batch-rename with `mv`** — the cascade effect corrupts siblings. Always use OneDrive web for folder renames in synced directories.
4. **Prefer OneDrive web for critical renames** — especially when serializing project folders with children
5. **Create new folders + move content** instead of renaming, when children are healthy: new folders generate proper `FPItem` creation events

## Checking OneDrive Sync Databases (Read-Only)

For forensic purposes only — never write to these:

```bash
# File provider status DB
~/Library/Application\ Support/OneDrive/settings/FileSyncFSCache.db

# Per-account sync engine DBs:
~/Library/Application\ Support/OneDrive/settings/Personal/SyncEngineDatabase.db
~/Library/Application\ Support/OneDrive/settings/Business1/SyncEngineDatabase.db
~/Library/Application\ Support/OneDrive/settings/Business2/SyncEngineDatabase.db
```

Query pattern (read-only, with bytes text factory for Arabic names):

```python
import sqlite3, os
db = os.path.expanduser('~/Library/Application Support/OneDrive/settings/Business2/SyncEngineDatabase.db')
conn = sqlite3.connect(db)
conn.text_factory = bytes  # handle Arabic/Unicode
cursor = conn.cursor()
cursor.execute("SELECT fileName, size, fileStatus FROM od_ClientFile_Records WHERE fileName LIKE '%keyword%'")
```

Tables of interest: `od_ClientFile_Records` (all tracked files), `od_UnrealizedFile_Records` (pending sync), `od_ClientFolder_Records` (folder structure).

## Identifying Different OneDrive Accounts

Multiple OneDrive mounts are common. Check CloudStorage:

```bash
ls -d ~/Library/CloudStorage/*/
```

Account naming convention:
- `OneDrive-Personal/` — Personal Microsoft account
- `OneDrive-Personal(2)/` — Additional personal account
- `OneDrive-SAMAYAINVESTMENT/` — Business/org account
- `OneDrive-SAMAYAINVESTMENT (22-05-2026 6:47 PM)/` — Old sync with date suffix
- `OneDrive-SharedLibraries-*` — SharePoint libraries
- `iCloudDrive-*` — Apple iCloud

## See Also

- `macos-housekeeping` skill: OneDrive / cloud-sync considerations section
- `references/downloads-cleanup-guide.md`: General file cleanup patterns
