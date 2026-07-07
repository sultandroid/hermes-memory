# OneDrive macOS Sandbox Workaround

## Problem
Files in the OneDrive folder (`~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/`) are regularly inaccessible from the terminal with:
```
Operation not permitted
```
This is a macOS TCC (Transparency, Consent, and Control) issue — the sandboxed terminal process doesn't have Full Disk Access for OneDrive cloud files, especially after `mv` operations trigger sync locks.

## When it happens
- After any `mv` or reorganization of files within a OneDrive folder
- When files are "cloud-only" (not locally cached)
- Randomly — OneDrive sync state is unreliable

## Recovery pattern

### Step 1: Check if Finder can access
```bash
osascript -e 'tell application "Finder" to get name of file POSIX file "/path/to/file"'
```
If this returns the filename, Finder CAN access it even when terminal cannot.

### Step 2: Copy via Finder AppleScript
```bash
osascript -e 'tell application "Finder" to duplicate file POSIX file "/path/to/source" to POSIX file "/private/tmp/" with replacing'
```

### Step 3: Work with the /tmp copy
All tools can access the copied file. After processing, if the result needs to go back to OneDrive, use the Hermes `write_file` tool which runs in a different process context.

## Copying INTO OneDrive (writing)

When you need to place a generated file (DOCX, PDF, HTML) into a OneDrive folder:

```bash
# 1. Stage to /tmp first (always)
python3 gen_script.py -o /tmp/output.docx

# 2. Create destination folder via shell
#    mkdir -p works on CloudStorage paths even when reads are blocked
DEST="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/..."
mkdir -p "$DEST"

# 3. Copy via Finder AppleScript (bypasses TCC sandbox)
osascript -e \
  'set srcPath to "/tmp/output.docx"
   set destFolder to "'"$DEST"'"
   tell application "Finder"
      set srcFile to POSIX file srcPath as alias
      set destPath to POSIX file destFolder as alias
      duplicate srcFile to destPath with replacing
   end tell'
```

### Verify after copy

After the script runs, verify via AppleScript:

```bash
osascript -e \
  'tell application "Finder" to get size of file POSIX file "'"$DEST"'/output.docx"'
```

Then verify the file isn't a zero-byte OneDrive placeholder by checking the magic header at /tmp (before AppleScript copy) or via the Group Containers path (after copy):

```bash
# DOCX: must start with PK\x03\x04
python3 -c "
with open('/tmp/output.docx', 'rb') as f:
    h = f.read(8)
    assert h[:2] == b'PK', f'BAD DOCX placeholder (not PK archive): {h.hex()}'
    print('OK: DOCX valid')
"

# PDF: must start with %PDF
# JPEG: must start with \xff\xd8\xff
```

A corrupt OneDrive placeholder will have the *right file size* on disk but contain all-zero bytes. Always verify header bytes before telling the user the file is ready.

### Group Containers fallback reads

When the standard CloudStorage path is TCC-blocked for reads, try the Group Containers path:

```bash
GCP="/Users/mohamedessa/Library/Group Containers/UBF8T346G9.OneDriveStandaloneSuite/OneDrive - SAMAYA INVESTMENT.noindex/OneDrive - SAMAYA INVESTMENT"
ls "$GCP/Samaya/Technical Office/..."
```

This often allows read access when CloudStorage is blocked. **Do NOT write directly to the Group Containers path** — it produces corrupted placeholder files (all-zero bytes, not valid PK headers). Always use AppleScript `duplicate` for writes.

## Advanced AppleScript patterns for OneDrive

### List files in a OneDrive folder (without TCC error)

```applescript
tell application "Finder"
    set fRef to POSIX file "/path/to/OneDrive/folder" as alias
    set fileList to every file of fRef
    repeat with f in fileList
        log (name of f) & " (" & (size of f) & " bytes)"
    end repeat
end tell
```

### Delete a specific file

```applescript
tell application "Finder"
    set f to POSIX file "/path/to/OneDrive/file.docx" as alias
    delete f
end tell
```

### Delete a OneDrive folder entirely

Finder's `delete` may hang on folders. Use `do shell script` via osascript:

```bash
osascript -e 'do shell script "rm -rf " & quoted form of "/path/to/OneDrive/folder"'
```

### Rename a file

```applescript
tell application "Finder"
    set fRef to POSIX file "/path/to/OneDrive/folder" as alias
    set fileList to every file of fRef
    repeat with f in fileList
        if name of f contains "oldname" then
            set name of f to "newname.docx"
        end if
    end repeat
end tell
```

### Copy from /tmp to OneDrive and rename

```bash
osascript -e '
tell application "Finder"
    -- Delete existing file at destination (if any)
    set destFile to "/path/to/OneDrive/dest/finalname.docx"
    try
        set f to POSIX file destFile as alias
        delete f
    end try
    
    -- Copy from /tmp
    set src to POSIX file "/tmp/tempname.docx" as alias
    set destFolder to POSIX file "/path/to/OneDrive/dest/" as alias
    duplicate src to destFolder with replacing
    
    -- Rename if saved with wrong name
    set fileList to every file of destFolder
    repeat with f in fileList
        if name of f contains "tempname" then
            set name of f to "finalname.docx"
        end if
    end repeat
end tell'
```

### Verify file integrity after copy

AppleScript can report file size. For DOCX header verification, copy back to /tmp then check:

```bash
osascript -e '
tell application "Finder"
    set srcFile to "/path/to/OneDrive/dest/finalname.docx"
    set src to POSIX file srcFile as alias
    set dest to POSIX file "/tmp" as alias
    duplicate src to dest with replacing
end tell'
python3 -c "
with open('/tmp/finalname.docx', 'rb') as f:
    h = f.read(8)
    assert h[:2] == b'PK', f'BAD DOCX placeholder: {h.hex()}'
    print('Valid DOCX')
"
```

## When it doesn't work
- If Finder itself cannot access (times out with error -10006), the file is truly offline/unsynced
- In that case, ask the user to open the folder in Finder to trigger the download

## Prevention
- Avoid `mv` operations within OneDrive folders — use Finder AppleScript for file moves
- Keep project files flat (no subfolder reorganization)
- Prefer reading/writing to /tmp for intermediate work
- `write_file` and `cp` to OneDrive CloudStorage paths fail with `Operation not permitted` — never use them as the primary write approach
