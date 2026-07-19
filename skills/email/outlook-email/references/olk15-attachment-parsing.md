# .olk15MsgAttachment Binary Parsing

**Referenced from:** `email/outlook-email` SKILL.md — "Direct Attachment Extraction (fallback)" section.
**Prefer AppleScript** for extraction; use this only as fallback.

Outlook for Mac stores attachments in `.olk15MsgAttachment` files with a proprietary binary format. AppleScript (`save att in saveFile`) is the preferred extraction method, but this reference covers the binary format for when AppleScript fails.

## File Structure

```
Offset 0x00:  4 bytes magic = d00d 0000 (little-endian)
Offset 0x04:  12 bytes unknown/padding
Offset 0x10:  16 bytes GUID
Offset 0x20+: MIME-style headers (Content-Type, Content-Disposition, Content-Transfer-Encoding)
             Terminated by \r\r (0d 0d) — NOT \r\n\r\n
After headers: base64-encoded payload

For PDFs: payload starts with "JVBER" (base64 encoding of "%PDF")
For JPEGs: payload starts with "/9j/" (base64 encoding of JPEG SOI)
For PNGs: payload starts with "iVBOR" (base64 encoding of PNG header)
```

**CRITICAL: The header boundary is `\r\r` (two CRs), NOT `\r\n\r\n`.** The Content-transfer-encoding header ends with `base64\r\r` followed immediately by base64 data. Using `\r\n\r\n` will fail to find the boundary. Verified on macOS 26.5.2 Outlook 16.97.

## Header Content

The MIME header section (before the base64 payload) contains:

```
Content-type: application/pdf; name="filename.pdf";
x-mac-creator=BOBO
x-mac-type=PDF 
Content-ID: <UUID>
Content-Disposition: attachment; filename="filename.pdf"
Content-Transfer-Encoding: base64
```

## Python Extraction

### Finding attachment file paths (SQLite → filesystem)

The `Mail_OwnedBlocks` table maps email IDs to attachment BlockIDs. The `Blocks` table maps BlockIDs to filesystem paths:

```sql
SELECT hex(b.BlockID), b.BlockTag, b.PathToDataFile
FROM Blocks b
JOIN Mail_OwnedBlocks m ON m.BlockID = b.BlockID
WHERE m.Record_RecordID = <RECORD_ID>
ORDER BY m.BlockTag;
```

The `PathToDataFile` column returns paths like `Message%20Attachments/35/<UUID>.olk15MsgAttachment` — URL-encoded spaces. Resolve with `urllib.parse.unquote` or bash `$'...'` quoting.

### Decoding the .olk15MsgAttachment file

```python
import base64, re, os

def extract_from_olk15(path, output_dir):
    """Extract attachment from .olk15MsgAttachment file."""
    with open(path, 'rb') as f:
        data = f.read()

    # Find base64 content start after MIME headers
    # CRITICAL: boundary is \r\r (two CRs), NOT \r\n\r\n
    b64_marker = data.find(b'base64\r\r')
    if b64_marker < 0:
        raise ValueError("No base64 marker found")

    payload = data[b64_marker + 8:]  # skip 'base64\r\r'

    # Find where base64 ends (next non-base64 character)
    end = 0
    for i, byte in enumerate(payload):
        c = chr(byte)
        if c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=\r\n':
            end = i
            break
    if end == 0:
        end = len(payload)

    b64_text = payload[:end].decode('ascii', errors='ignore').strip()

    # Fix padding
    padding = 4 - len(b64_text) % 4
    if padding != 4:
        b64_text += '=' * padding

    raw = base64.b64decode(b64_text)

    # Get filename from headers
    header_text = data[:b64_marker].decode('ascii', errors='ignore')
    fname_match = re.search(r'name="([^"]+)"', header_text)
    ext = '.pdf' if raw[:4] == b'%PDF' else '.jpg' if raw[:2] == b'\xff\xd8' else '.bin'
    fname = fname_match.group(1) if fname_match else f'extracted{ext}'

    out_path = os.path.join(output_dir, fname)
    with open(out_path, 'wb') as out:
        out.write(raw)
    return out_path, len(raw)
```

## Common Issues

1. **Multiple payloads in one file**: Some `.olk15MsgAttachment` files contain both a PDF and a preview JPEG. Only the first non-image payload is the real attachment.

2. **Corrupt base64**: The base64 data may have non-standard whitespace or control characters mixed in. The `re.sub` cleanup is essential.

3. **Magic bytes `d00d`**: Not all files starting with `d00d` are valid — check file size (> 500 bytes minimum).

4. **AppleScript error -1741**: "An error of type -1741 has occurred" = Outlook/Accessibility permissions not granted. Fix: System Settings > Privacy & Security > Automation > allow Terminal/Agent to control Microsoft Outlook. This affects `properties of theMsg` reads AND `save att in saveFile` — both fail silently or with misleading error codes.

5. **Large files (10MB+) timeout in multi-attachment scripts**: When extracting multiple attachments in a single Python script, a single large file (e.g., 17.5MB PDF) can cause the entire script to hit the 300s timeout. **Fix:** Extract one attachment per script call with a short timeout (30s). The base64 decode is fast even for large files — the timeout is from the file read + decode loop, not the decode itself. Pattern:

   ```python
   # One file per call, timeout=30
   python3 -c "
   import base64
   with open('file.olk15MsgAttachment', 'rb') as f:
       data = f.read()
   b64_start = data.find(b'base64\r\r')
   b64_data = data[b64_start+8:]
   end = 0
   for i, byte in enumerate(b64_data):
       c = chr(byte)
       if c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=\r\n':
           end = i; break
   if end == 0: end = len(b64_data)
   b64_str = b64_data[:end].decode('ascii').strip()
   padding = 4 - len(b64_str) % 4
   if padding != 4: b64_str += '=' * padding
   decoded = base64.b64decode(b64_str)
   with open('/tmp/output.pdf', 'wb') as f:
       f.write(decoded)
   print(f'Saved: {len(decoded)} bytes')
   " 2>&1
   ```
