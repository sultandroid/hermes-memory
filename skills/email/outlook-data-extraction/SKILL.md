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

### Search by sender/recipient email address (precise)
Use `Message_SenderAddressList` and `Message_ToRecipientAddressList` for exact email matching (more reliable than `Message_SenderList`/`Message_DisplayTo` which may contain display names only):
```sql
SELECT datetime(Message_TimeReceived, 'unixepoch') as dt,
       Message_NormalizedSubject as Subject,
       Message_SenderList as Sender,
       Message_DisplayTo as Recipient,
       Message_SenderAddressList as SenderEmail,
       Message_ToRecipientAddressList as ToEmail,
       substr(Message_Preview, 1, 200) as Preview
FROM Mail
WHERE Message_SenderAddressList LIKE '%raoof@samayainvest.com%'
   OR Message_ToRecipientAddressList LIKE '%raoof@samayainvest.com%'
ORDER BY Message_TimeReceived DESC
LIMIT 30;
```

### Search by person name (sender/recipient display name)
```sql
SELECT datetime(Message_TimeReceived, 'unixepoch') as dt,
       Message_NormalizedSubject,
       Message_SenderList,
       Message_DisplayTo
FROM Mail
WHERE Message_SenderList LIKE '%Raoof%'
   OR Message_DisplayTo LIKE '%Raoof%'
ORDER BY Message_TimeReceived DESC
LIMIT 20;
```

### Combined: person + keyword + folder context
```sql
SELECT m.Record_RecordID as ID,
       datetime(m.Message_TimeReceived, 'unixepoch') as Received,
       m.Message_NormalizedSubject as Subject,
       m.Message_SenderList as Sender,
       m.Message_DisplayTo as Recipient,
       m.Message_SenderAddressList as SenderEmail,
       m.Message_ToRecipientAddressList as ToEmail,
       f.Folder_Name as Folder,
       substr(m.Message_Preview, 1, 100) as Preview
FROM Mail m
LEFT JOIN Folders f ON m.Record_FolderID = f.Record_RecordID
WHERE (m.Message_NormalizedSubject LIKE '%مصنع%'
   OR m.Message_SenderAddressList LIKE '%raoof@samayainvest.com%'
   OR m.Message_ToRecipientAddressList LIKE '%raoof@samayainvest.com%')
ORDER BY m.Message_TimeReceived DESC
LIMIT 50;
```

### Classify direction (FROM/TO a person)
```sql
SELECT m.Record_RecordID as ID,
       CASE WHEN m.Message_SenderAddressList LIKE '%raoof@samayainvest.com%' THEN 'FROM'
            WHEN m.Message_ToRecipientAddressList LIKE '%raoof@samayainvest.com%' THEN 'TO'
            ELSE 'Related'
       END as Direction,
       datetime(m.Message_TimeReceived, 'unixepoch') as Received,
       m.Message_NormalizedSubject as Subject,
       m.Message_SenderList as Sender,
       m.Message_DisplayTo as Recipient,
       substr(m.Message_Preview, 1, 100) as Preview
FROM Mail m
WHERE m.Message_SenderAddressList LIKE '%raoof@samayainvest.com%'
   OR m.Message_ToRecipientAddressList LIKE '%raoof@samayainvest.com%'
ORDER BY m.Message_TimeReceived DESC
LIMIT 30;
```

### Count total matching emails
```sql
SELECT COUNT(*) as Total
FROM Mail
WHERE Message_NormalizedSubject LIKE '%keyword%'
   OR Message_SenderAddressList LIKE '%person@domain.com%';
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

### List all folders
```sql
SELECT Record_RecordID, Folder_Name, Folder_SpecialFolderType
FROM Folders
ORDER BY Record_RecordID;
```

### List tables
```sql
.tables
```

### Show table schema
```sql
PRAGMA table_info(Mail);
PRAGMA table_info(Folders);
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

3. Decode the base64-encoded PDF (⚠️ marker is `Content-transfer-encoding: base64\r\r`, offset +35):
```python
import base64, subprocess
from pathlib import Path

data = Path('file.olk15MsgAttachment').read_bytes()
idx = data.find(b'Content-transfer-encoding: base64')
b64_data = data[idx + 35:]  # skip marker + \r\r
text = b64_data.decode('ascii', errors='replace')
clean = text.replace('\r', '').replace('\n', '')
pad = len(clean) % 4
if pad:
    clean += '=' * (4 - pad)
pdf_data = base64.b64decode(clean)

Path('/tmp/output.pdf').write_bytes(pdf_data)
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
