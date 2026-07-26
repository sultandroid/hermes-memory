# Base64 Attachment Extraction from .olk15MsgAttachment Files

When AppleScript fails (Outlook 16.90+ regression) or the SQLite database is locked, attachments can be extracted directly from the `.olk15MsgAttachment` files stored on disk.

## Location

```
~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Message Attachments/{folder}/{UUID}.olk15MsgAttachment
```

## File Format

The `.olk15MsgAttachment` file is a simple binary wrapper containing:
1. A 16-byte binary header (`d00d 0000 0100 0000 0200 0000 0300 0000`)
2. A UUID string
3. MIME headers (Content-type, Content-disposition, Content-transfer-encoding)
4. Base64-encoded attachment data

## Finding the Right Block

Use the `Mail_OwnedBlocks` + `Blocks` tables in the Outlook SQLite database to find the attachment path:

```sql
SELECT mb.Record_RecordID, mb.BlockTag, b.PathToDataFile
FROM Mail_OwnedBlocks mb
JOIN Blocks b ON mb.BlockID = b.BlockID
WHERE mb.Record_RecordID = <EMAIL_ID>
ORDER BY mb.BlockTag;
```

- `BlockTag = 1098151011` = attachment block
- Other block tags (e.g. 1297314403) may exist for email body content

## Extraction Pattern (Python)

```python
import base64, subprocess
from pathlib import Path

# Read the .olk15MsgAttachment file
data = Path('/path/to/file.olk15MsgAttachment').read_bytes()
text = data.decode('latin-1')

# Find base64 start after MIME headers
idx = text.find('base64')
if idx < 0:
    raise ValueError('No base64 content found')

b64 = text[idx + 7:].strip()  # skip 'base64\n'
pdf_data = base64.b64decode(b64)

# Save to PDF
pdf_path = '/tmp/extracted.pdf'
Path(pdf_path).write_bytes(pdf_data)

# Extract text (if text PDF)
result = subprocess.run(['pdftotext', pdf_path, '-'], 
                       capture_output=True, text=True, timeout=30)
print(result.stdout)

# If empty, PDF is image-based — try OCR
if not result.stdout.strip():
    subprocess.run(['sips', '-s', 'format', 'jpeg', '-Z', '1200', pdf_path, 
                   '--out', '/tmp/for_ocr.jpg'], check=True)
    subprocess.run(['tesseract', '/tmp/for_ocr.jpg', '/tmp/ocr_out'])
    print(Path('/tmp/ocr_out.txt').read_text())
```

## When to Use This

- AppleScript `message id <N>` fails with `Can't make |subject| of incoming message id N into type specifier`
- SQLite database is locked (Outlook holds WAL lock)
- The email is in a subfolder where `plain text content` returns empty
- You need the raw PDF for OCR (image-based stamped drawings)

## Worked Example — NRS Stage 3 Audit

**Context:** Email thread "Aseer Regional Museum : Stage 3 Audit" from Jim Richards (NRS), May 2026. The actual 12-page audit PDF was embedded as base64 inside `.olk15MsgAttachment` files.

### Finding the path

```sql
SELECT mb.Record_RecordID, mb.BlockTag, b.PathToDataFile
FROM Mail_OwnedBlocks mb
JOIN Blocks b ON mb.BlockID = b.BlockID
WHERE mb.Record_RecordID IN (34017, 34020, 34046);
```

Construct full path: `Data/<PathToDataFile>` under the Outlook profile directory.

### Key detail — check ALL versions in a thread

| Email | RecordID | Attachment | Content |
|-------|----------|------------|---------|
| Initial (13-May) | 33454 | A2742-10.07-001.pdf | Drawing only — NOT the audit |
| Updated (15-May) | 34017 | A2742-10.07-001A.pdf | **Stage 3 Audit PDF** (12 pages) |
| Updated v3 (16-May) | 34046 | A2742-10.07-001B.pdf | Same + extra items (blockwork, library finish) |

**Important:** The initial email only contained a drawing. The **Updated** version (15-May) had the actual audit document. Always check all versions.

### Full extraction command

```bash
cp "/path/to/34017.olk15MsgAttachment" /tmp/audit.olk
python3 -c "
import base64
with open('/tmp/audit.olk', 'rb') as f:
    data = f.read()
text = data.decode('latin-1')
idx = text.find('base64')
with open('/tmp/audit.pdf', 'wb') as out:
    out.write(base64.b64decode(text[idx+7:].strip()))
"
pdftotext /tmp/audit.pdf -
```

The extracted PDF was 2.2MB, 12 pages, with full text content. Contained 15 audit items from Jim Richards across architecture coordination, finishes, BOQ, and materials.

## Limitations

- Only works for emails whose attachments have been cached by Outlook
- Some attachments may be stored in EFMData format (encrypted)
- Image-based PDFs (CAD plots, stamped drawings) need OCR via tesseract
- The base64 extraction may fail for very large files or multipart MIME
