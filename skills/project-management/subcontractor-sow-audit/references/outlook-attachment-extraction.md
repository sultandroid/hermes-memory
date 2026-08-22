# Extracting Email Attachments from Outlook on macOS (raw .olk15MsgAttachment)

Worked 2026-08-21 while pulling a scanned TLC bid PDF (email 50632). The
AppleScript `save` route fails, but the raw attachment blob is on disk and can
be base64-decoded directly.

## Why AppleScript save fails

`osascript` `save <attachment> in <path>` often returns:
`Microsoft Outlook got an error: An error has occurred. (-2700)`
even though the attachment is fully present. This is a known Outlook scripting
quirk; do not waste turns retrying it. Also note `name of attachment` works but
`path`/`file of attachment` return `missing value`.

## Where attachments live on disk

```
~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/
  Message Attachments/<n>/<GUID>.olk15MsgAttachment   <- the actual binary
```

- The `Mail` table in `Outlook.sqlite` maps a message to its message file:
  `SELECT PathToDataFile FROM Mail WHERE Record_RecordID=<msgid>;`
  e.g. `Messages/57/<GUID>.olk15Message`.
- The actual attachment BLOB is NOT inside that message file — it lives under
  `Message Attachments/`. The `.olk15Message` only carries a metadata pointer.
- List attachments on a message via osascript:
  `repeat with a in attachments of m ... name of a` (names come back fine, e.g.
  `E 26263-26-3304-001-Rev2 ... TLC_Offer.pdf`).

## Finding the right attachment blob

The blob's first ~2 KB contain MIME headers including the real filename:

```bash
BASE="$HOME/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data"
find "$BASE/Message Attachments" -type f -newermt "2026-08-06" ! -newermt "2026-08-15" | while read f; do
  head -c 2000 "$f" | strings | grep -ioE 'name="[^"]*"' | head -1
done | grep -iE 'offer|TLC|3304'   # narrow by expected filename fragment
```

Do NOT `grep -r` the whole `Message Attachments` tree for content — it is huge
and times out. Scope by mtime window first, then by filename metadata.

## Decoding the PDF out of the blob

The `.olk15MessageAttachment` is a text shell: MIME headers, then a base64 blob.
Find the base64 (starts `JVBERi0` = `%PDF-`), strip non-base64 chars, decode:

```python
import os, re, base64
base=os.path.expanduser("~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data")
f=os.path.join(base,"Message Attachments/125/7D6DFCDF-6B14-4770-860F-4819611125FF.olk15MsgAttachment")
raw=open(f,'rb').read()
i=raw.find(b'JVBERi0')                      # start of base64 PDF
b64=re.sub(rb'[^A-Za-z0-9+/=]', b'', raw[i:])  # strip headers/whitespace
open('/tmp/offer.pdf','wb').write(base64.b64decode(b64))
```

## Reading scanned/image PDFs

Many bidder offers are scanned → no text layer. `pdftotext` returns ~0 bytes and
`pdfminer` raises `PDFSyntaxError: No /Root object`. Convert to PNG and read by
vision:
```bash
python3 -c "from pdf2image import convert_from_path; [im.save(f'/tmp/p{i+1}.png') for i,im in enumerate(convert_from_path('offer.pdf', dpi=150))]"
```
Then `vision_analyze` each page, asking specifically for fee, payment terms,
exclusions, and Revit/BIM mentions. Scan page-by-page — bidder offers frequently
CONTRADICT themselves page-to-page (e.g. p1 "Revit included", p2 fee table
"Revit excluded"), which is itself the crux of a scope dispute.
