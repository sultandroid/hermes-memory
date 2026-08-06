# .olk15Message Body Extraction (No AppleScript)

When AppleScript is unavailable or `message id N` property access fails on Outlook 16.90+, the full email body can be extracted directly from the `.olk15Message` file on disk.

## How it works

The `.olk15Message` file is a proprietary binary format with this structure:
- **Bytes 0-3**: Header (0x0D 0x00 0x00 0x01)
- **Bytes 4-19**: 16-byte UUID
- **Bytes 20+**: Raw email content (MIME headers + body)

The email body is stored as HTML embedded in the binary data. You can extract it by searching for HTML tags.

## Extraction Pattern

```python
import os, re

data_dir = "/Users/.../Outlook/Outlook 15 Profiles/Main Profile/Data"
relpath = "Messages/27/1B19B732-D661-4CDA-98CD-1B250B0DA606.olk15Message"

with open(os.path.join(data_dir, relpath), 'rb') as f:
    data = f.read()

# Skip 20-byte binary header
content = data[20:]

# Decode as latin-1 (preserves all bytes)
text = content.decode('latin-1', errors='replace')

# Find HTML body
html_start = text.find('<html')
if html_start >= 0:
    html_end = text.find('</html>', html_start)
    if html_end >= 0:
        html = text[html_start:html_end + 7]
        
        # Strip HTML tags to get plain text
        html_clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        html_clean = re.sub(r'<style[^>]*>.*?</style>', '', html_clean, flags=re.DOTALL)
        text_only = re.sub(r'<[^>]+>', ' ', html_clean)
        text_only = text_only.replace('&nbsp;', ' ').replace('&amp;', '&')
        text_only = re.sub(r'\s+', ' ', text_only).strip()
```

## When to use this

1. **AppleScript `message id N` fails** with `Can't make |subject| of incoming message id X into type specifier` (-1700) on Outlook 16.90+
2. **AppleScript is unavailable** (no Accessibility permissions, headless environment)
3. **You need the full body** — `Message_Preview` in SQLite is truncated (~500 chars)

## Limitations

- **TNEF emails** (`Content-Type: application/ms-tnef`) store the body in a proprietary format that is NOT directly extractable from the .olk15Message file. The body is encoded inside the TNEF stream, which requires a TNEF decoder. These emails show no HTML content when searched.
- **RTF-only emails** (no HTML alternative) also won't have HTML content to extract.
- **The body may contain UTF-16LE encoded text** mixed with binary data. The latin-1 decode preserves all bytes but may show garbled characters for non-ASCII content.

## Finding the .olk15Message path

```sql
SELECT PathToDataFile FROM Mail WHERE Record_RecordID = <ID>;
```

Path is relative to `Data/` — construct full path:
`~/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/<PathToDataFile>`

## Example: ZNA Lighting Protocol Email (49771)

This email had a full HTML body with embedded inline images. The extraction produced the complete email text including the quoted previous message and signature block. The key content was:

> "Yes we have this schedule, but this doesn't show the showcase lighting circuits. In the issued Stage 3 showcase drawings and Lighting control narrative, it clearly mentions that the showcase circuits should have timed control."

This was NOT visible in the `Message_Preview` column (which only showed the first sentence).
