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

When `pdftotext` returns empty (CAD plots, stamped redline drawings, scanned Arabic review forms):
```bash
# Convert to image
sips -s format jpeg -Z 1200 input.pdf --out ~/output.jpg
tesseract ~/output.jpg ~/ocr_out
cat ~/ocr_out.txt
```

**Pitfall — tesseract fails to open files in some directories.** If tesseract errors `failed to open locally with tail <file>` / `image file not found`, `cd /tmp` first and pass the absolute path — it cannot read files from certain working dirs (e.g. a `/tmp/email_attachments/` subdir). Run from `/tmp`.

**Pitfall — `sips` only converts page 1 of a multi-page PDF.** For multi-page scanned docs use `pdftoppm` per page:
```bash
pdfinfo file.pdf | grep -i pages
pdftoppm -f 1 -l 1 -r 200 -jpeg "<pdf>" /tmp/out
tesseract /tmp/out-1.jpg stdout -l ara+eng
```
`-l ara+eng` is required for Arabic review forms (consultant/NAMA/CG stamped approvals).

**Pitfall — CG/consultant review code is a checked box, not text.** On Arabic review forms the A/B/C/D code is a checkbox in the "Review Result" section. OCR that region to confirm the code (e.g. Code C = Resubmit). The code governs the register status, not the transmittal subject line.

**Pitfall — nested/unsaveable attachments save as 0-byte files.** A `.zip` CAD attachment may extract as 0 bytes via AppleScript `save` (it "succeeds" but writes nothing). Detect with `ls -la` and flag for manual open in Outlook rather than retrying.

## Batch "read all attachments" workflow (proven)

When the user asks to read/extract every attachment from recent emails:

1. **Query attachments by email id** — get `PathToDataFile` from `Mail_OwnedBlocks` JOIN `Blocks` for each `Record_RecordID` with `Message_HasAttachment=1`. Path lives under `.../Data/`, replace `%20` with space before opening.
2. **Decode each `.olk15MsgAttachment`** — find `Content-transfer-encoding: base64`, take bytes after it (+35), strip the MIME boundary (`split(b"--=_")[0]`), strip all whitespace, re-pad base64, decode. Save as a real file; identify type by magic bytes (PDF/ZIP/PNG/JPG/OLE).
3. **Convert to text**: `pdftotext -layout` for text PDFs; `openpyxl` for xlsx; **OCR** any PDF whose text is 1 byte (image-only scan).
4. **OCR pitfall (reconfirmed):** `pdftoppm -f 1 -l N -r 200 -jpeg <pdf> /tmp/out` then run `tesseract /tmp/out-N.jpg <out> -l ara+eng` **from `/tmp`** — tesseract fails from arbitrary dirs. Note base64-encoded attachment filenames produce near-identical strings (e.g. `...2YbYqtmK2KzYqQ_` vs `...2YbYqtmK2zYqQ_`) — run `ls` on the actual filename before OCR, don't trust the pattern.
5. **Delegate reading to a labor** (Kimi/Claude): concatenate text files into batches ≤~20KB each (Kimi times out on larger single-turn payloads), then fire one `kimi -p "$(cat batch.md)" --output-format text` per batch as **parallel background terminal calls**. Returns structured per-doc summaries. Note: Kimi CLI now takes the prompt as a positional `-p <prompt>` arg — the legacy `--print` / stdin-pipe interface is removed (2026-08).

## Pitfalls

- Column `Message_Body` does NOT exist — use `Message_Preview` for text content- Timestamps are **plain Unix epoch seconds** — use `datetime(Message_TimeReceived, 'unixepoch', 'localtime')`. Do NOT apply a Windows `10000000-11644473600` adjustment; that yields empty/zero rows. For date filtering use `Message_TimeReceived > strftime('%s','YYYY-MM-DD')` (Unix epoch works directly in comparisons).
- `Message_Preview` is truncated (~255 chars). Full body text is NOT in the SQLite row — for long bodies, extract the `.olk15MsgAttachment` MIME (or an HTML `Email_Content.html` block) rather than relying on the preview. Search only needs subject/preview; content extraction needs the block file.
- **`.olk15Message` body blocks are TNEF-encoded and NOT plaintext — `tnefparse` fails on them** ("Wrong TNEF signature: 0x00000dd0"). The MIME `Content-Type: application/ms-tnef` (winmail.dat) confirms it, but the TNEF magic bytes aren't found at the expected offset. The subject/headers are plaintext-readable via `strings`, but the body is a binary block. So for Outlook bodies, `Message_Preview` (≤255 chars) is the practical content source; do not expect to recover full body text from the `.olk15Message` binary in the common case. (Verified 2026-08-15.)
- The `Files` table is a virtual table (`FilesVTabModule`) — cannot query directly
- `.olk15MsgAttachment` files have a binary header followed by MIME headers then base64 payload
- Some attachment PDFs are image-only (CAD plots) — `pdftotext` returns empty; use OCR
- OneDrive placeholders with "Resource deadlock avoided" — use Outlook DB or GitHub repo clone as fallback
- **Cross-check registers BEFORE adding entries** — the daily email-sync cron (`register-auto-update`) auto-captures many CG responses/submittals (e.g. PQ-0130 rigging Code D, HVAC/Drain gateways, SOR-003/013 closeout were already in `submittal_register.md` / `risk_register.md` when the manual pass ran). After reading attachments, `grep` the target register for the doc ref (e.g. `PQ-0130`, `1G-0004`) and add ONLY genuinely missing entries — do not duplicate rows the cron already filed. The manual pass should backfill gaps (e.g. SOR-016 missing from `sor_register.md`, PQ-0130 missing from `prequalification_register.md`) rather than re-add what exists.

## References

- `references/kimi-attachment-qc.md` — Kimi v0.23.3 QC of extracted email attachments: flags, background-run pattern for large batches, OCR of scanned Arabic review forms, 0-byte attachment pitfall
