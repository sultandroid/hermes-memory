# TNEF / UTF-16LE HTML Body Extraction from .olk15Message Files

When AppleScript fails (permissions, timeout) and `Message_Preview` is truncated (~500 chars), extract the full email body directly from the `.olk15Message` file using Python.

## When to use this

- AppleScript `plain text content of msg` returns empty or errors (-1741)
- `Message_Preview` from SQLite is truncated (only first ~500 chars)
- The email body contains Arabic, tables, or structured content you need in full

## How it works

Outlook for Mac stores emails in TNEF (winmail.dat) format inside `.olk15Message` files. The HTML body is embedded as UTF-16LE encoded text. The key is finding the UTF-16LE `<div>` tag pattern in the binary.

## Extraction script

```python
import re

with open('/path/to/file.olk15Message', 'rb') as f:
    data = f.read()

# UTF-16LE encoded '<div' = b'\x3c\x00\x64\x00\x69\x00\x76\x00'
pattern = b'\x3c\x00\x64\x00\x69\x00\x76\x00'
idx = data.find(pattern)
if idx >= 0:
    chunk = data[idx:idx+15000]
    text = chunk.decode('utf-16le', errors='replace')
    # Remove nulls and control chars
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
    # Strip HTML tags to get readable text
    text_only = re.sub(r'<[^>]+>', '\n', text)
    text_only = re.sub(r'\n\s*\n', '\n', text_only)
    text_only = text_only.strip()
    print(text_only)
```

## Finding the right .olk15Message file

Use `mdfind` (Spotlight) to find the file by subject:

```bash
mdfind -name "subject keyword" -onlyin ~/Library/Group\ Containers/UBF8T346G9.Office/
```

Or query SQLite first to get the `PathToDataFile` column, then resolve relative to the Messages/ directory.

## Pitfalls

- **The `<div>` pattern is UTF-16LE.** Searching for `<html` or `<body` in raw bytes won't find it — those are also UTF-16LE encoded. Always search for the byte pattern `\x3c\x00\x64\x00\x69\x00\x76\x00` (UTF-16LE `<div`).
- **Extract 15000+ bytes.** The HTML body can be large (signatures, embedded images, long tables). Start with 15000 and increase if truncated.
- **`strings` is unreliable.** The TNEF format interleaves binary metadata with text. `strings` output is mostly noise. Use the Python pattern above.
- **`textutil` also fails.** macOS `textutil -convert txt` on `.olk15Message` files produces garbage — it doesn't understand the TNEF container format.
- **Not all .olk15Message files have HTML.** Some are plain text only. If `<div>` isn't found, try `<p>` or `<span>` patterns in UTF-16LE.
- **The extracted HTML may contain `&nbsp;` entities.** These are non-breaking spaces — strip them with `text.replace('&nbsp;', ' ')` if they clutter the output.
