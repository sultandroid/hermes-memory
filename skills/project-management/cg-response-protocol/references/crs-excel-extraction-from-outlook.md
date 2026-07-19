# CRS Excel Extraction from Outlook .olk15MsgAttachment

Extract CG Comment Resolution Sheet (CRS) Excel files from Outlook email attachments and parse them into structured markdown.

## Workflow

### 1. Find the CG Response Email

Query Outlook SQLite for the submittal reference:

```sql
SELECT Record_RecordID, Message_TimeReceived, Message_NormalizedSubject, Message_SenderList
FROM Mail
WHERE Message_NormalizedSubject LIKE '%1C0-1G-0001%'
ORDER BY Message_TimeReceived DESC;
```

### 2. Find Attachment Block IDs

```sql
SELECT hex(BlockID) FROM Mail_OwnedBlocks WHERE Record_RecordID = <ID>;
```

### 3. Locate .olk15MsgAttachment Files

```sql
SELECT hex(BlockID), PathToDataFile FROM Blocks
WHERE hex(BlockID) IN ('<UUID1>','<UUID2>',...);
```

The `PathToDataFile` is relative to `Data/Message Attachments/`. The subdirectory is the first 1-3 hex digits of the GUID (e.g., `95/5FE5984C-...`).

### 4. Extract Base64 Content

The `.olk15MsgAttachment` format:
- 4-byte magic header: `d00d 0000`
- GUID (16 bytes)
- `cttA` + 4 bytes
- `Content-type: ...` header
- `Content-transfer-encoding: base64\r\r`
- Base64-encoded file content

**Key boundary marker:** `base64\r\r` (two CRs, NOT `\r\n\r\n`). Using `\r\n\r\n` will fail.

```python
import base64

with open('file.olk15MsgAttachment', 'rb') as f:
    data = f.read()

b64_start = data.find(b'base64\r\r')
b64_data = data[b64_start + 8:]  # skip 'base64\r\r'

# Collect only valid base64 chars
b64_text = b''
for byte in b64_data:
    c = chr(byte)
    if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=\r\n':
        b64_text += bytes([byte])
    else:
        break

b64_str = b64_text.decode('ascii').strip()
# Fix padding
padding = 4 - len(b64_str) % 4
if padding != 4:
    b64_str += '=' * padding

decoded = base64.b64decode(b64_str)
```

### 5. Identify File Type

| Magic Bytes | Format |
|-------------|--------|
| `%PDF` | PDF |
| `PK\x03\x04` | ZIP/DOCX/XLSX |
| `\xff\xd8` | JPEG |

For ZIP files, check `[Content_Types].xml` to determine if it's an XLSX (Excel) or DOCX (Word).

### 6. Parse CRS Excel (XLSX)

```python
import zipfile, io, xml.etree.ElementTree as ET

z = zipfile.ZipFile(io.BytesIO(decoded))

# Read shared strings
ss = z.read('xl/sharedStrings.xml')
ss_root = ET.fromstring(ss)
ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
strings = [si.find('s:t', ns).text if si.find('s:t', ns) is not None else ''
           for si in ss_root.findall('.//s:si', ns)]

# Read sheet
sheet = z.read('xl/worksheets/sheet1.xml')
root = ET.fromstring(sheet)
rows = root.findall('.//s:row', ns)

for row in rows:
    cells = row.findall('s:c', ns)
    vals = []
    for c in cells:
        v = c.find('s:v', ns)
        t = c.get('t')
        if v is not None:
            if t == 's':
                idx = int(v.text)
                vals.append(strings[idx] if idx < len(strings) else f'[{idx}]')
            else:
                vals.append(v.text or '')
        else:
            vals.append('')
    print(' | '.join(vals))
```

### 7. Build Markdown Table

Map the Excel columns to a markdown table. Typical CRS columns:

| # | Consultant Comment | Contractor Response | Rev.00 Status | Consultant Comment (Rev.01) | Rev.01 Status |

Key observations to add:
- How many comments closed vs open
- Which items the contractor thought were closed but CG re-opened
- What type of evidence CG is demanding (physical vs documentary)

## Pitfalls

- **Large files timeout.** A 17MB PDF attachment takes ~30s to extract via Python base64 decode. Use `timeout=60` on the terminal command. For very large files, extract only the first few KB to identify the type, then use `pdftotext` on the saved file.
- **Multiple attachments per email.** CG response emails often have 2-6 attachments (CRS Excel, stamped PDFs, images). Extract all and identify by content type.
- **`base64\r\r` vs `base64\r\n\r\n`.** Always check for `\r\r` first. The `\r\n\r\n` variant appears in some older Outlook versions.
- **Base64 padding.** The base64 data may be missing padding `=`. Always calculate and add it.
- **Arabic text in CRS.** The shared strings may contain Arabic. Handle with UTF-8 encoding throughout.
