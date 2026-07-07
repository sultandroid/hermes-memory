# Recovering localStorage Data from Chrome LevelDB

When a deploy wipes server-side data, the user's hotspot/settings data may still exist in Chrome's LevelDB storage on their local machine. This reference covers extraction without browser access.

## Where Chrome Stores localStorage

```
~/Library/Application Support/Google/Chrome/Default/Local Storage/leveldb/
```

Files:
- `*.log` — Most recent journal (uncompressed, easiest to parse)
- `*.ldb` — Compacted SSTables (Snappy-compressed, hard to extract without LevelDB library)

## Quick Extraction (from .log files)

.log files contain recent writes in uncompressed format. Extract JSON arrays directly:

```python
import os, re, json

storage = os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/Local Storage/leveldb/')
all_data = {}

for fname in os.listdir(storage):
    if not fname.endswith('.log'):
        continue
    with open(os.path.join(storage, fname), 'rb') as f:
        raw = f.read()
    text = raw.decode('latin-1')
    # Find all localStorage keys
    for m in re.finditer(r'aseer_hotspots_([a-zA-Z0-9_]+)', text):
        key = m.group(0)
        if key in all_data:
            continue
        # Find JSON array after the key
        content = text[m.end():]
        for offset in range(min(50, len(content))):
            if content[offset] == '[':
                try:
                    depth, in_str, esc = 0, False, False
                    for end in range(offset, min(len(content), 5000)):
                        c = content[end]
                        if esc: esc = False; continue
                        if c == '\\': esc = True
                        elif c == '"': in_str = not in_str
                        elif not in_str:
                            if c == '[': depth += 1
                            elif c == ']':
                                depth -= 1
                                if depth == 0:
                                    candidate = content[offset:end+1]
                                    parsed = json.loads(candidate)
                                    if isinstance(parsed, list) and len(parsed) > 0:
                                        all_data[key] = parsed
                                        break
                except:
                    continue
                break

# Save to desktop
if all_data:
    outpath = os.path.expanduser('~/Desktop/recovered_hotspots.json')
    with open(outpath, 'w') as f:
        json.dump(all_data, f, indent=2)
    print(f"Saved {len(all_data)} views to {outpath}")
```

## Limitations

- **.ldb files use Snappy compression within LevelDB block framing** — The value IS in the .ldb file (the key is found) but is inside a LevelDB SSTable block with Snappy compression plus block trailer (CRC + compression type). The `python-snappy` package alone cannot decompress this because LevelDB uses its own framing. You need the actual LevelDB library (`plyvel` or `brew install leveldb` + `ldb` tool) to read the database properly.
- **To install Snappy for Python** (partial, log files only): `pip3 install --break-system-packages python-snappy` (macOS with system Python).
- **The key is found in .ldb files** even when the value can't be extracted — confirms data exists. The key names list what was stored, even if values are inaccessible.
- **Executed Python code runs in a sandbox** — the `execute_code` tool does not have access to pip-installed libraries. Run extraction scripts via `terminal()` tool instead.
- **Browser must not have cleared storage** — localStorage survives browser restarts but is cleared on private browsing close, site data clear, or browser reset.
- **Snapshot writes only** — Chrome writes .log files in batches. If the browser was force-closed, unsaved writes are lost. The .log file may only contain the last write, not all writes from the session.

## Prevention

Move persistent data storage OUTSIDE the build directory (see PHP persistence pitfall in the main skill) so future deploys don't wipe server-side data. Team members should export hotspots (via admin UI export button) as a backup before any deploy.
