# Corrected Base64 Extraction from .olk15MsgAttachment Files

## Key Fix: Marker Format

The `Content-transfer-encoding: base64` marker is followed by **`\r\r`** (two carriage returns), **not** `\n` or `\r\n`. The base64 data starts immediately after the 35-byte marker.

## Corrected Extraction Pattern

```python
import base64, re
from pathlib import Path

data = Path('/path/to/file.olk15MsgAttachment').read_bytes()

idx = data.find(b'Content-transfer-encoding: base64')
if idx < 0:
    raise ValueError('No base64 content found')

# Marker is followed by \r\r — skip 35 bytes total
b64_start = idx + 35
b64_data = data[b64_start:]

# Decode as ascii, strip \r\n line breaks
b64_text = b64_data.decode('ascii', errors='replace')
clean = b64_text.replace('\r', '').replace('\n', '')

# Add padding if needed
pad = len(clean) % 4
if pad:
    clean += '=' * (4 - pad)

decoded = base64.b64decode(clean)
Path('/tmp/extracted.pdf').write_bytes(decoded)
```

## Verification

After extraction, verify the file type:
```bash
file /tmp/extracted.pdf
# Expected: "PDF document, version 1.7"
```

## Common Pitfalls

- **`text.find('base64')` is wrong** — the marker is `Content-transfer-encoding: base64`, not just `base64`. Searching for `base64` alone may match other content.
- **`text[idx+7:]` is wrong** — the marker is 33 chars, not 7. The correct offset is `idx + 35` (33 for the marker + 2 for `\r\r`).
- **`b64.decode('ascii').strip()` loses data** — the base64 body has `\r\n` line breaks that must be removed, but `.strip()` only removes leading/trailing whitespace. Use `.replace('\r', '').replace('\n', '')` instead.
- **Padding may be missing** — always add `=` padding to make length a multiple of 4.
- **The base64 data may contain non-base64 chars** — if `b64decode` fails, check for stray characters with `re.sub(r'[^A-Za-z0-9+/=]', '', clean)`.
