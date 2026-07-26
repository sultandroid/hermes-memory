---
name: outlook-data-extraction
title: Outlook for Mac — Email & Attachment Data Extraction
description: Search, extract, and decode email content from Outlook for Mac's local SQLite database. Export base64-encoded MIME attachments and OCR image-based PDFs.
---

# Outlook for Mac — Data Extraction

Use when project files are OneDrive placeholders (Resource deadlock avoided) and email content is the only accessible data source.

## Database

```
~/Library/Group Containers/UBF8T346G9.Office/Outlook/
  Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite
```

## Common Queries

### Search emails by keyword
```sql
SELECT datetime(Message_TimeReceived, 'unixepoch') as dt,
       Message_NormalizedSubject,
       Message_SenderAddressList,
       substr(Message_Preview, 1, 300) as preview
FROM Mail
WHERE Message_NormalizedSubject LIKE '%keyword%'
ORDER BY Message_TimeReceived DESC
LIMIT 10;
```

### Find CG response codes (B / C)
```sql
SELECT datetime(Message_TimeReceived, 'unixepoch') as dt,
       Message_NormalizedSubject,
       substr(Message_Preview, 1, 60) as code
FROM Mail
WHERE Message_NormalizedSubject LIKE '%doc-ref%'
  AND Message_SenderAddressList LIKE '%@cg.com.sa%'
ORDER BY Message_TimeReceived DESC;
```

### Find emails with attachments
```sql
SELECT Record_RecordID, datetime(Message_TimeReceived, 'unixepoch'), Message_NormalizedSubject
FROM Mail
WHERE Message_HasAttachment = 1
  AND Message_NormalizedSubject LIKE '%keyword%';
```

## Extracting Attachments from .olk15MsgAttachment Files

1. Find the attachment path from the Blocks table:
```sql
SELECT mb.Record_RecordID, b.PathToDataFile
FROM Mail_OwnedBlocks mb
JOIN Blocks b ON mb.BlockID = b.BlockID
WHERE mb.Record_RecordID = <EMAIL_ID>;
```

2. Full path: `~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/<PathToDataFile>`

3. Decode the base64-encoded PDF:
```python
import base64, subprocess

with open('file.olk15MsgAttachment', 'rb') as f:
    data = f.read()
text = data.decode('latin-1')
idx = text.find('base64')
b64 = text[idx+7:].strip()
pdf_data = base64.b64decode(b64)

with open('/tmp/output.pdf', 'wb') as out:
    out.write(pdf_data)

r = subprocess.run(['pdftotext', '/tmp/output.pdf', '-'],
    capture_output=True, text=True, timeout=30)
print(r.stdout)
```

## OCR for Image-Based PDFs (Stamped Drawings)

When `pdftotext` returns empty (CAD plots, stamped redline drawings):
```bash
# Convert to image
sips -s format jpeg -Z 1200 input.pdf --out ~/output.jpg
tesseract ~/output.jpg ~/ocr_out
cat ~/ocr_out.txt
```

## Pitfalls

- Column `Message_Body` does NOT exist — use `Message_Preview` for text content
- The `Files` table is a virtual table (`FilesVTabModule`) — cannot query directly
- `.olk15MsgAttachment` files have a binary header followed by MIME headers then base64 payload
- Some attachment PDFs are image-only (CAD plots) — `pdftotext` returns empty; use OCR
- OneDrive placeholders with "Resource deadlock avoided" — use Outlook DB or GitHub repo clone as fallback
