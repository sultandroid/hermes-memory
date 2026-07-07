# Outlook Attachment Extraction via AppleScript

When the Outlook `olk15MsgAttachment` format prevents direct file reads (binary format, not a PDF), use AppleScript to extract attachments directly.

## Direct AppleScript Extraction

```bash
osascript -e '
tell application "Microsoft Outlook"
    set theMsg to message id 44904
    set atts to (every attachment of theMsg)
    set outFolder to "/tmp/outlook_extracts/"
    do shell script "mkdir -p " & quoted form of outFolder
    repeat with att in atts
        set savePath to outFolder & (id of theMsg) & "_" & (name of att)
        save att in (POSIX file savePath as alias)
    end repeat
end tell
'
```

**Key points:**
- `message id ID` — the database `Record_RecordID` from Outlook SQLite
- `(every attachment of theMsg)` — iterates all attachments
- `name of att` — includes original filename (may have special chars)
- Prepends `{id}_` to avoid filename collisions
- Saves to `/tmp/outlook_extracts/` (avoids OneDrive EDEADLK issues)
- Files saved as new copies — no OneDrive lock problems

## Batch Extraction Pattern

For multiple emails, iterate in bash:

```bash
for id in 44904 44911 44898; do
    osascript -e "
tell application \"Microsoft Outlook\"
    set theMsg to message id $id
    set atts to (every attachment of theMsg)
    set outFolder to \"/tmp/outlook_extracts/\"
    do shell script \"mkdir -p \" & quoted form of outFolder
    repeat with att in atts
        set savePath to outFolder & (id of theMsg) & \"_\" & (name of att)
        save att in (POSIX file savePath as alias)
    end repeat
end tell
"
done
```

## Large Batch Extraction

For 50+ emails, write the script to a file first to avoid heredoc issues:

```bash
cat > /tmp/batch_extract.sh << 'SCRIPT'
#!/bin/bash
for id in 44904 44911 44898 44871 44873 44875; do
  osascript <<EOF
tell application "Microsoft Outlook"
    set theMsg to message id $id
    set atts to (every attachment of theMsg)
    set outFolder to "/tmp/outlook_extracts/"
    do shell script "mkdir -p " & quoted form of outFolder
    repeat with att in atts
        set savePath to outFolder & (id of theMsg) & "_" & (name of att)
        save att in (POSIX file savePath as alias)
    end repeat
end tell
EOF
done
SCRIPT
bash /tmp/batch_extract.sh
```

## Error Handling

- **Error 401:421** = "An error has occurred" — usually a corrupt/unsupported message. Skip and continue.
- **Message with zero attachments** — AppleScript succeeds silently (loop doesn't execute).
- **Large attachments (>20MB)** — may timeout Outlook's AppleScript handler. Extract individually with `timeout 30`.

## Reading Extracted PDFs

After extraction, use `pdftotext` (brew install poppler) to read:

```bash
pdftotext /tmp/outlook_extracts/44904_MOC-MUS-ASE-1K0-PL-0057.pdf - | head -30
```

Or Python pdfminer:
```bash
python3 -m pdfminer.high_level /tmp/outlook_extracts/44904_doc.pdf | head -30
```

## File Routing by Document Code

After extracting, file to the correct project subfolder based on the document code prefix:

```python
import shutil, os

BASE = "/path/to/project/base"
SRC = "/tmp/outlook_extracts"

# Route by filename patterns
routes = {
    'PL-0057': 'Docs/02_Plans_and_Procedures/02.8_Master_Programme/02_CG_Responses/',
    'ZD-0056': 'Subcontractors/02_Lighting_Designer/05_Returned_Submittals/',
    'MS-0015': 'Docs/02_Plans_and_Procedures/02.15_Method_Statements/02_CG_Responses/',
    'PQ-0096': 'Docs/09_Registers/27_Subcontractor_Prequalification_Register/Namaa/',
}

for fname in os.listdir(SRC):
    for kw, dest in routes.items():
        if kw in fname:
            shutil.copy2(os.path.join(SRC, fname), os.path.join(BASE, dest, fname))
            break
```

## Integration with Odoo Task Creation

After extracting and reading attachments, create/update Odoo tasks with actual submission dates and CG status codes from the emails. See the `odoo` skill's `references/odoo-task-hierarchy.md` for the full task creation pattern.
