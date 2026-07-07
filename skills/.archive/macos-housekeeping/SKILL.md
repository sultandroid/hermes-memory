---
name: macos-housekeeping
description: Use when cleaning up or organizing a cluttered macOS folder (Downloads, Desktop, OneDrive/cloud-synced, or BIM/construction project dirs) — scans, flags duplicates/temp/clutter, gets approval, then deletes safely.
tags:
  - macos
  - cleanup
  - file-management
  - downloads
  - duplicates
  - housekeeping
---

# macOS Housekeeping

Scan, identify, present, and clean up cluttered folders (Downloads, Desktop, Documents, etc.) with user confirmation at appropriate granularity.

## Trigger

User says "check my Downloads folder", "clean up Desktop", "this folder is a mess", or anything about file clutter on macOS.

## Workflow

### 1. Scan the target folder

Start with a broad file search, then get total size.

```bash
# Total size
du -sh "$TARGET"

# Size by subfolders
du -sh "$TARGET"/*/ | sort -rh
```

Use `search_files(target='files')` with a broad pattern to enumerate contents. Truncated results mean there are many files — note the total count.

### 2. Identify categories of clutter

Look for these patterns:

| Category | Indicators | Disposition |
|----------|------------|-------------|
| **App duplicates** | Same .app bundle in two locations (e.g. "App 2/") | Delete duplicate |
| **Excel temp files** | `~$*.xlsx`, `~$*.docx` | Delete — Excel crash/lock artifacts |
| **Empty folders** | Folders containing only `.DS_Store` | Delete |
| **Version noise** | `file (1).xlsx`, `file_FINAL.xlsx`, `file_FINAL_CORRECTED.xlsx` | Ask user — keep latest |
| **Iteration chains** | `report_v2.xlsx` → `report_v2_1.xlsx` → `report_v2_7.xlsx` | Ask user — keep latest |
| **Test artifacts** | `.test_*`, temp debug files | Delete |
| **Old installers** | `.dmg`, `.pkg` from past installs | Ask user |
| **Hidden macOS files** | `.DS_Store`, `.localized` | Ignore (or delete at end) |
| **BIM temp/cache** | `.pcp` (AutoCAD plot config), `.bak` (AutoCAD backup), `.slog` (Revit journal), `.rws` (Revit worksharing), `.dat` (Revit DB cache), `.dwl`/`.dwl2` (DWG lock) | Delete — all safe to remove |
| **Render/export temps** | `Bitmap*.png/jpg`, `cd*.jpg`, `881214*.jpg`, numbered cache images | Delete — render farm / visualization cache |
| **Garbled filenames** | Files with corrupted Unicode names (`´`, `¦`, `¢`, etc.) | Delete — corrupted |
| **OneDrive 0-byte placeholders** | Files showing `0` bytes in `ls -la` but are not actual empty files | Treat with caution — content may be cloud-only; verify before delete |
| **Other-project files mixed in** | Files whose naming prefix matches a different project (e.g. `211210_CREATION_*` in a `Zamzam_Museum` folder) | Archive out — belongs in sibling project folder |

### 3. Present findings to user

Organize by folder and category. Use a table format:
- **What was found** (size, count)
- **What's obviously safe to delete** (temp files, duplicates)
- **What needs their decision** (version chains, old installers)

### 4. Execute safe deletions first

Clean these without asking:
- Excel temp files (`~$*`)
- Empty folders (only .DS_Store inside)
- Test artifacts
- Obvious app duplicates (same app, " 2" suffix)

```bash
# Dry-run: list what WOULD be deleted (always do this first)
find "$TARGET" -name '~$*' -type f -print

# Real run, once verified
find "$TARGET" -name '~$*' -type f -delete

# Empty folders containing only .DS_Store
find "$TARGET" -type d -empty -print            # truly empty
# (for ".DS_Store-only" dirs, delete the .DS_Store first, then -empty catches them)
```

### 5. Ask about ambiguous items

For version chains and duplicate file groups, present each group with:
- File names and sizes
- Count of versions
- Ask: "Keep only the latest?" or specify

### 6. For mixed-project folders: detect and separate

When a folder contains files from multiple projects (common in BIM/construction folders):

1. **Count by extension** — `find . -maxdepth 1 -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -30` to understand the scope
2. **Identify project-specific prefixes** — Look for recurring numeric/alphabetic prefixes (e.g. `211210_*`, `4121_*`, `A22-71-KZC-*`) that differ from the folder name theme
3. **Group non-matching files** by prefix → each group is likely a different project
4. **Present to user** as a table of "Other Project" candidates with file counts
5. **Archive to parent** — create `__Archived_Other_Projects/<ProjectName>/` at the parent directory level and move grouped files there

### Detect legacy project subfolder vs. root-level numbered structure

A common pattern in mature project directories: root-level numbered folders (`01_ProjectName`, `02_AnotherProject`) coexist with a legacy `projects/` subfolder. The numbered root folders are the **new standardized structure**; the `projects/` folder is an **older container** where content was originally dumped and never migrated.

**Detection steps:**
1. List root-level folders — look for numbered prefixes (`01_`, `02_`...) alongside a `projects/` folder
2. Check each root-level numbered folder for actual content (empty dirs = not yet migrated)
3. Check inside `projects/` — compare names against root-level folders. Ex: `projects/06_Antara_Rock_Visitor_Center/` vs root `06_Antara_Rock/` — partial name match signals duplicate
4. For each match, decide migration status:
   - **Root has full sub-structure, projects/ has shallow content** → merge into root
   - **Root empty, projects/ has content** → move content to root
   - **Both have content** → merge, checking for unique vs. duplicate files

**Merge workflow:**
1. For each project found in `projects/`:
   - Check if content exists at root level → if empty dir, content lives only in legacy
   - Move individual subfolders/files from `projects/<Project>/` into root `<Number>_<Project>/`
   - **For local/on-disk files:** use `rsync -av` or `cp -rn` to merge — safest with conflict detection
   - **For OneDrive cloud-only files (dataless placeholders):** use `mv` (file/dir → dest/) instead of `cp`/`rsync`. `mv` is a metadata-only rename and completes instantly. `cp`/`rsync` trigger file download from the cloud and timeout on large files (99MB+ PDFs, large HTML exports)
2. After all merges verified, remove empty `projects/` folder
3. Verify no data lost — each root-level project dir should now have meaningful content

**Handling `mv` "Directory not empty" conflicts:**
When a destination directory already exists, `mv` refuses with "Directory not empty." The fix is a step-by-step merge instead of a single bulk mv:

1. `mv source/subdir/* dest/subdir/` — moves the individual files first (instant on OneDrive since it's metadata-only)
2. For nested subdirectories that also conflict at the destination, iterate their contents:
   ```bash
   for item in projects/X/source_subdir/*; do mv "$item" destination/X/source_subdir/; done
   rmdir projects/X/source_subdir
   ```
3. Clean up empty source dirs: `rmdir projects/X/subdir`
4. Repeat for each conflicting directory level
5. At the end, `rmdir projects/X` once empty, then `rmdir projects` if all projects migrated

**Signs the merge is complete:**
- Every numbered project folder has content (not just empty dirs)
- The `projects/` folder is gone (or archived)
- No duplicate project data across two locations

### For BIM/construction project folders

These (AutoCAD DWG, Revit RVT/IFC, PDF submittals, BOQ spreadsheets) benefit from organization into standard discipline folders rather than flat root storage:

- **Design Files/** — DWG, DXF, AI, design PDFs (furniture plans, finish plans, lighting, door schedules, shop drawings)
- **Revit Files/** — .rvt, .ifc, .nwc, .rfa, .fbx, IFC logs
- **Media/** — All JPG/PNG/MP4/HEIC/WEBP (site photos, WhatsApp images, render previews)
- **Docs/** — Project documentation PDFs, reports, spreadsheets, inspection/commissioning records (.md files)
- **B.O.Q/** — Bill of quantities spreadsheets and PDFs
- **Coordination/** — Clash reports, coordination drawings
- **Submittal's/** — Submittal logs, approval docs
- **Email_Archive/** — Email exports (.md, .eml) organized by date
- **Specs & Datasheet/** — Specification PDFs, datasheets

Move files by naming convention batch (e.g. `*Furniture*` → Design Files/, `*BOQ*` → B.O.Q/). For BIM projects, keep the existing folder structure if present — just populate the empty shells.

### 8. Organize emails: separate from project docs

In construction/BIM folders, email thread exports (.md, .eml) often mix with project documents:

- **Email .md files** typically have date prefixes like `2024-05-30 - Subject [ID].md` or contain email-specific keywords (RE:, Fw:, shared 1 item with you, mentioned you, notifications)
- **Project .md files** have structured codes like `ZAM-SAM-121-ADM-INIT-*`, or titles without date prefixes
- Move all email .md + .eml to `Email_Archive/`

### 9. Post-cleanup summary

Report:
- What was removed + how much space freed
- What was kept and why
- Remaining folder size

## Tools to use

| Tool | Use for | Safety |
|------|---------|--------|
| `search_files(target='files')` | enumerate contents (broad glob `*`) | read-only |
| `terminal` + `du -sh` | size checks | read-only |
| `terminal` + `find . -name '...' -type f -delete` | bulk temp-file removal | ⚠️ destructive — scope the path, dry-run first |
| `terminal` + `rm -rf` | last resort deletion | ⚠️ destructive + irreversible — prefer `find -delete` with explicit `-name`; never run on a bare/var-only path |
| `execute_code` + `from hermes_tools import terminal` | bulk ops where filenames have Unicode/Arabic/spaces/special chars (`&`, `'`, `(`, `)`) | guard with `if [ -f "..." ]; then mv "..." "dest/"; fi` |
| `clarify` | ask about ambiguous duplicate/version groups when user said a general "yes" | — |

**⚠️ Destructive-command rules:**
- **Always dry-run first.** Replace `-delete` with `-print` (or `rm` with `echo rm`) and review the list before the real run.
- **Quote every path** (`"$TARGET"`) — unquoted vars + spaces = wrong deletions.
- **Never** `rm -rf "$VAR"` when `$VAR` could be empty (expands to `rm -rf /`). Guard: `[ -n "$TARGET" ] && [ -d "$TARGET" ]`.
- `find -delete` and any `sudo` will trigger an approval prompt — that's expected; do not try to suppress it.

## OneDrive / cloud-sync considerations

When files are in a cloud-synced folder (OneDrive, Dropbox, iCloud):
- `ls -la` may show `0` bytes for many files that actually have content — they're cloud-only placeholders and haven't synced locally. **Do not assume 0-byte = empty/junk.**
- Use `du -sh .` for total size, not file-by-file size checks
- Moving/deleting in a cloud folder will replicate to cloud — verify with user before bulk operations
- Files with the `dataless` flag in `ls -laO` are **cloud-only placeholders** — content is not on disk
- The `fileproviderctl evaluate <file>` command gives the most precise sync status (isDownloaded, isUploading, isKeepDownloaded, etc.)
- When `isUploading=1` and `isDownloaded=0`, the file is an **orphaned placeholder** that can never be materialized — content was evicted before upload completed
- Terminal reads (`cat`, `head`, `dd`, `cp`) all return 0 bytes for dataless files. Recovery via `open <file>` in its native app (Preview for PDFs) triggers hydration, then `mv` works. Fallback: Finder "Always Keep on This Device" or OneDrive web. See `references/onedrive-dataless-diagnostics.md` for full diagnostics and recovery table.
- **`cp` fails with fcopyfile: Operation timed out** — OneDrive files with realistic `ls -la` sizes that fail during `cp` (even to /tmp) can still be copied via `cat src > /tmp/file && mv /tmp/file dst/`. The cat + redirect bypasses the copyfile syscall that OneDrive intercepts. This also works when `dd` reads 0 bytes from dataless-but-sized files. Preferred strategy for OneDrive-to-OneDrive copies.
- For full diagnostic workflow, see `references/onedrive-dataless-diagnostics.md`

### Renaming OneDrive Folders/Files

When you need to rename folders or files inside a OneDrive-synced folder, the method matters:

| Method | File Provider | Syncs to cloud? |
|--------|---------------|-----------------|
| `mv oldname newname` / `os.rename()` | **Bypasses** coordination | ❌ Usually fails |
| AppleScript `set name of folder to newname` | Uses Finder → some coordination | ⚠️ May fail if items are in bad state |
| `URLResourceValues.name` via Swift (`.setResourceValues`) | Proper API for File Provider items | ✅ Best chance |
| OneDrive web UI (onedrive.live.com) | Direct cloud rename | ✅ Always works |

**Recommended approach (renaming stuck items):**
1. First try `URLResourceValues.name` via Swift (see reference file for code)
2. If `isUploading=1` persists after rename, the item is in a stuck sync state
3. Best recovery: rename directly via OneDrive web interface — bypasses local sync issues entirely

```swift
// Swift snippet for renaming OneDrive file provider items
import Foundation
let fm = FileManager.default
let oldURL = URL(fileURLWithPath: "/path/to/item")
var rv = URLResourceValues()
rv.name = "New Name"
try oldURL.setResourceValues(rv)
```

**Troubleshooting stuck renames:**
- Check state: `fileproviderctl evaluate <path>` → look for `isUploading=1, isUploaded=0`
- If stuck, restart OneDrive: quit app, wait, re-open
- If still stuck: the item is in an orphaned state — only OneDrive web rename works
- The `dataless` flag on children prevents parent folder renames from syncing (chicken-and-egg)

**⚠️ Cascade Corruption Warning (batch renames break ALL siblings):**
When you batch-rename multiple folders inside a OneDrive parent using `mv`, the ENTIRE parent's sync context can corrupt — including folders that were never touched. Each sibling shows:
- `isUploading=1, isUploaded=0` (stuck uploading)
- `uploadingError = "The file doesn't exist."` (OneDrive error -2)

This happens because `mv` bypasses the File Provider extension entirely. OneDrive's sync engine loses track of all items under the parent, not just the renamed ones.

**Repair pattern for cascade corruption:**
1. Revert ALL renamed folders back to their original cloud names using `mv`
2. Restart OneDrive app to clear the stuck state
3. Verify with `fileproviderctl evaluate <path>` that each folder returns to healthy state
4. Perform the renames ONE at a time via OneDrive web interface
5. Wait for each rename to sync before doing the next

**Prevention:** Before bulk rename of OneDrive folders:
1. Check all folders are `isDownloaded=1, isUploaded=1` (synced locally + pending cloud)
2. **NEVER batch-rename folders with `mv`** — use OneDrive web for ALL renames in cloud-synced directories
3. Avoid renaming folders with `dataless` children
4. For critical renames, use OneDrive web directly — one folder at a time

### iCloud Drive file coordination locks

Files in the iCloud-synced `~/Documents/Documents - <Device Name>/` tree may get locked by the `bird` (iCloud Drive) daemon and become **unreadable through any POSIX method** — `cat`, `head`, `cp`, `dd`, `find -exec`, `os.open()` all fail with `EAGAIN` (Resource deadlock avoided, errno 11). This is different from OneDrive dataless files (which `cat src > dst` can bypass).

**Symptoms:**
- `cat file` → `Resource deadlock avoided`
- `cp src dst` → `fcopyfile failed: Resource deadlock avoided`
- Python `open()` → `OSError: [Errno 11]`
- `file` command → `ERROR: cannot read`
- File has `com.apple.provenance` extended attribute (`ls -l@`)
- `bird` process is running (iCloud Drive daemon)

**Root cause:** Apple's file coordination system (`NSFileCoordinator` framework) locks the file during sync. All non-coordinated access attempts get denied.

**Fix — use `NSFileCoordinator` via Swift (for reading) or `shutil.copy2()` (for copying):**

For reading: use NSFileCoordinator via Swift (template below). For copying files from iCloud to a local destination, Python's `shutil.copy2()` bypasses the fcopyfile syscall and works even when `cp`/`ditto` fail. See `references/icloud-file-coordination.md` for both approaches with code and limitations.

**Key details:**
- `.withoutChanges` option — read-only coordination, no side effects
- `.uncached` — avoids kernel page cache (also blocked)
- Only Swift/ObjC works — Python, shell, AppleScript cannot bypass this lock
- Writing to coordinated files still fails; use the owning app or iCloud website for writes

**Detection workflow:**
```bash
ls -l@ /path/to/file | grep provenance        # check attribute
ps aux | grep bird | grep -v grep              # check daemon
python3 -c "open('/path/to/file').read(10)"    # test — fails Errno 11
```

For full reference code and diagnostics, see `references/icloud-file-coordination.md`.

## Pitfalls

- **Don't delete the only copy** — always check for duplicates before removing.
- **Don't remove `.app` bundles without user confirmation** — they may be actively used.
- **Watch for `find -delete` requiring approval** — the terminal tool may prompt for approval on `-delete` flag. That's expected behavior.
- **Truncated results** — search_files caps at 50 results by default; use `limit` and `offset` for full listings.
- **Don't touch hidden files** unless user asked or they're clearly test artifacts.
- **Version files with Arabic names** — handle with care, use quoted paths in terminal.
- **Batch renames in OneDrive corrupt ALL siblings** — `mv`-based batch renames inside a cloud-synced parent corrupt every folder under that parent, even untouched ones. Always use OneDrive web for folder renames in synced directories.
- **When the user says "yes" to a general cleanup proposal**, proceed with all safe deletions immediately, then narrow down to ambiguous groups for clarification.
- **Scope to the folder the user asked about** — when a user asks about a specific folder's structure or content ("why is there X in this folder"), focus on that folder only. Don't extrapolate to the parent directory or sibling folders unless they explicitly ask. They'll tell you if they want the broader picture, and premature broadening wastes their time.

## Verification

After cleanup, confirm:
- Target folder still has expected files (nothing essential removed)
- Size reduction is as expected
- No broken symlinks or orphaned references

## Reference files

- `references/downloads-cleanup-guide.md` — General downloads folder cleanup patterns
- `references/bim-project-cleanup.md` — BIM/construction project folder cleanup: detecting other projects by naming convention, OneDrive handling, discipline subfolder organization, email-vs-project-doc separation
- `references/project-folder-standardization.md` — Template-driven project folder organization: applying a uniform 13-folder template (00_Admin → 99_Templates), content mapping rules, handling OneDrive cloud-only files with mv vs cp/rsync, merging directories on conflict, and OneDrive path-parentheses workaround using Python os module.
- `references/icloud-file-coordination.md` — iCloud Drive file coordination locks: diagnosing `EAGAIN` (Resource deadlock avoided) on iCloud-synced files, using Swift `NSFileCoordinator` to read locked files, and full Swift reader template code.
