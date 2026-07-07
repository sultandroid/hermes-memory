# Batch Email Attachment Routing

## Pattern used in June 2026 session

1. Query Outlook SQLite for emails by project/doc-code, filter by `Message_HasAttachment = 1`
2. Collect Record_RecordIDs grouped by project
3. Write 2-3 AppleScripts (one per project batch), each saving to `/tmp/outlook-attachments/<project>/`
4. List staging dir to inspect what was saved
5. Route with Python script mapping filename → target subfolder
6. Clean up `/tmp/outlook-attachments/`

## AppleScript batch template (per project)

```applescript
set baseFolder to "/tmp/outlook-attachments/aseer/"
do shell script "mkdir -p " & quoted form of baseFolder
set emailIds to {35130, 35125, 35081}
set savedCount to 0

tell application "Microsoft Outlook"
    repeat with eid in emailIds
        set eidVal to (eid as integer)
        try
            set theMsg to message id eidVal
            set atts to (every attachment of theMsg)
            repeat with att in atts
                set attName to name of att
                set attType to content type of att
                if attType does not start with "image/" then
                    set savePath to baseFolder & eidVal & "_" & attName
                    do shell script "touch " & quoted form of savePath
                    set saveFile to POSIX file savePath as alias
                    save att in saveFile
                    set savedCount to savedCount + 1
                end if
            end repeat
        on error errMsg
            log "Error on " & eidVal & ": " & errMsg
        end try
    end repeat
end tell
return "Saved: " & savedCount & " files"
```

## Python routing template

```python
import shutil, os

SRC = "/tmp/outlook-attachments/aseer"
BASE = "/path/to/OneDrive/.../Bim Unit/Aseer-Museum"

mapping = {
    "MOC-MUS-ASE-1A0-ZD-0033 Rev.01.pdf": "Design Files",
    "34950_Daily Report 07-06-2026.pdf": "07_Daily_Reports",
    "MOC-MUS-ASE-1KH-SOW-INT-001_Interactive_Design_Scope.docx": "09_Correspondence",
}

for fname, subdir in mapping.items():
    src = os.path.join(SRC, fname)
    dst = os.path.join(BASE, subdir, fname)
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
```

## Key lessons from this session

- AppleScript email IDs come from `Record_RecordID` in SQLite — saves 2s per email vs iterating the whole mailbox
- Prefix staging filename with email ID (`{eid}_{attName}`) to track provenance
- Non-image filtering (`attType does not start with "image/"`) is essential — 90%+ of inline atts are signature images
- `on error` block each ID — deleted/moved emails throw, scpt fails silently otherwise
- Python `shutil.copy2` preserves timestamps (file date = original email date context)
