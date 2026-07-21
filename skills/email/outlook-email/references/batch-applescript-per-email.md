# Batch AppleScript Extraction — One Script Per Email

When extracting attachments from many emails (15+), the ~700-byte AppleScript body limit prevents a single script from handling all IDs. The reliable workaround: write one `.applescript` file per email ID, then run them sequentially.

## Pattern

```bash
# 1. Write one .applescript per email ID (via write_file tool)
# /tmp/extract_48830.applescript
# /tmp/extract_48826.applescript
# ...

# 2. Run in batches of 3-5
osascript /tmp/extract_48830.applescript 2>&1
osascript /tmp/extract_48826.applescript 2>&1
```

## Script Template

```applescript
set outFolder to "/tmp/ad_engineering_attachments/"
tell application "Microsoft Outlook"
    set eidVal to <EMAIL_ID>
    set theMsg to message id eidVal
    set atts to (every attachment of theMsg)
    repeat with att in atts
        if content type of att does not start with "image/" then
            set attName to name of att
            set savePath to outFolder & "<EMAIL_ID>_" & attName
            do shell script "touch " & quoted form of savePath
            save att in (POSIX file savePath as alias)
        end if
    end repeat
end tell
```

## Why This Works

- Each script is ~470 bytes — well under the ~700 byte limit
- No heredoc quoting issues (no `&` in terminal command)
- No bash interpolation problems with special characters in filenames
- Sequential runs are slower but reliable; batch 5-6 at a time for ~30s total
