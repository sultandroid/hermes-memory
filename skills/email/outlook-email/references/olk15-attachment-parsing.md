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
             Terminated by \r\n\r\n (0d 0a 0d 0a)
After headers: base64-encoded payload

For PDFs: payload starts with "JVBER" (base64 encoding of "%PDF")
For JPEGs: payload starts with "/9j/" (base64 encoding of JPEG SOI)
For PNGs: payload starts with "iVBOR" (base64 encoding of PNG header)
```

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

```python
import base64, re, os

def extract_from_olk15(path, output_dir):
    """Extract attachment from .olk15MsgAttachment file."""
    with open(path, 'rb') as f:
        data = f.read()
    
    # Find base64 content start after MIME headers
    header_end = data.find(b'\r\n\r\n')
    if header_end < 0:
        raise ValueError("No MIME header boundary found")
    
    payload = data[header_end + 4:]
    
    # Decode base64 content
    # Content starts after the \r\n\r\n boundary
    for marker, ext in [(b'JVBER', '.pdf'), (b'/9j/', '.jpg'), (b'iVBOR', '.png')]:
        idx = payload.find(marker)
        if idx >= 0:
            b64_text = payload[idx:].decode('ascii', errors='ignore')
            b64_clean = re.sub(r'[^A-Za-z0-9+/=]', '', b64_text)
            raw = base64.b64decode(b64_clean)
            
            # Get filename from headers
            header_text = data[:header_end].decode('ascii', errors='ignore')
            fname_match = re.search(r'name="([^"]+)"', header_text)
            fname = fname_match.group(1) if fname_match else f'extracted{ext}'
            
            out_path = os.path.join(output_dir, fname)
            with open(out_path, 'wb') as out:
                out.write(raw)
            return out_path, len(raw)
    
    return None, 0
```

## Common Issues

1. **Multiple payloads in one file**: Some `.olk15MsgAttachment` files contain both a PDF and a preview JPEG. Only the first non-image payload is the real attachment.

2. **Corrupt base64**: The base64 data may have non-standard whitespace or control characters mixed in. The `re.sub` cleanup is essential.

3. **Magic bytes `d00d`**: Not all files starting with `d00d` are valid — check file size (> 500 bytes minimum).

4. **AppleScript error -1741**: "An error of type -1741 has occurred" = Outlook/Accessibility permissions not granted. Fix: System Settings > Privacy & Security > Automation > allow Terminal/Agent to control Microsoft Outlook. This affects `properties of theMsg` reads AND `save att in saveFile` — both fail silently or with misleading error codes.
