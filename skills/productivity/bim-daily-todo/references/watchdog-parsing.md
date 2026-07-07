# Watchdog State JSON Parsing

## File Characteristics

| Property | Value |
|----------|-------|
| Path | `~/.hermes/scripts/.watchdog_state.json` |
| Size | ~4.3 MB (grows over time) |
| Lines | ~53,000 |
| Format | Single JSON object — file paths as keys, `{hash, mtime}` as values |

## Preferred Method: `json.load()` (works, use this)

`json.load()` works directly on the watchdog file. The previous concern about "control characters breaking json.load" was incorrect — the real problem was `terminal("cat")` truncating the output to ~330 lines.

```python
from datetime import datetime, timedelta
import json

def extract_watchdog_files(project_keyword='Zamzam', days_back=7, watchdog_path=None):
    """
    Extract recently-modified files from the watchdog JSON.

    Args:
        project_keyword: substring to filter paths (e.g., 'Zamzam', 'Aseer')
        days_back: how far back to look (default 7 days)
        watchdog_path: path to watchdog_state.json

    Returns:
        list of dicts: [{path, name, date, mtime}, ...] sorted newest first
    """
    if watchdog_path is None:
        import os
        watchdog_path = os.path.expanduser(
            '~/.hermes/scripts/.watchdog_state.json'
        )

    cutoff_ts = (datetime.now() - timedelta(days=days_back)).timestamp()

    with open(watchdog_path, 'r') as f:
        data = json.load(f)

    results = []
    for path, info in data.items():
        if project_keyword not in path:
            continue
        mtime = info.get('mtime', 0)
        if mtime < cutoff_ts:
            continue
        name = path.split('/')[-1]
        fdate = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
        results.append({
            'path': path,
            'name': name,
            'date': fdate,
            'mtime': mtime
        })

    results.sort(key=lambda x: x['mtime'], reverse=True)
    return results
```

## Edge Cases

### 1. Empty hash values
Some entries have `"hash": ""` — these are large binary files (rar, pdf, dwg) that weren't checksummed. Still valid for mtime checking.

### 2. Control characters in file paths
Some paths contain Unicode (Arabic) characters encoded as `\uXXXX` escape sequences. Python's `json.load()` handles these correctly.

### 3. Duplicate paths
If the same file appears multiple times with different mtimes, the last key in the JSON wins. In practice mtimes are stable.

## Categorization by Filename

After extraction, group files by discipline using **filename string matching**.
**Critical ordering rule:** Match MEP-specific patterns (HVAC, CCTV) BEFORE architectural/generic ones
like `el-hramein` or `fa-` — otherwise `El-Hramein Musuem - Final HVAC dwg.zip` matches
`el-hramein` first and gets misclassified as architectural.

```python
counts = {'FR': 0, 'WF': 0, 'FL': 0, 'PR': 0, 'SK': 0, 'AV': 0, 'SUB': 0,
          'DOC': 0, 'MEP': 0, 'MATERIAL': 0}
for path, info in data.items():
    if 'Zamzam' not in path:
        continue
    mtime = info.get('mtime', 0)
    if mtime < cutoff:
        continue
    name = path.split('/')[-1]
    nl = name.lower()

    # MEP patterns FIRST (before architectural)
    if 'hvac' in nl:
        counts['MEP'] += 1; cat = 'MEP-HVAC'
    elif 'cctv' in nl:
        counts['MEP'] += 1; cat = 'MEP-CCTV'
    # Submittal logs
    elif 'log' in nl and 'submittal' in nl:
        counts['SUB'] += 1; cat = 'SUB'
    # Architectural design packages (P083, P0639)
    elif 'p083_' in nl or 'p0639-' in nl or name.startswith('Architectural'):
        counts['DOC'] += 1; cat = 'DOC-DESIGN'
    # El-Hramein architectural (after MEP patterns)
    elif 'el-hramein' in nl:
        counts['DOC'] += 1; cat = 'DOC-HRAMEIN'
    # Shop drawing disciplines
    elif 'fr-' in nl or name.startswith('Zamzam_Museum-Furniture'):
        counts['FR'] += 1; cat = 'SDR-FR'
    elif 'wf-' in nl or name.startswith('Zamzam_Museum-Wall Finish'):
        counts['WF'] += 1; cat = 'SDR-WF'
    elif 'fl-' in nl or name.startswith('Zamzam_Museum-Flooring'):
        counts['FL'] += 1; cat = 'SDR-FL'
    elif 'pr-' in nl or name.startswith('Zamzam_Museum-Partition'):
        counts['PR'] += 1; cat = 'SDR-PR'
    elif 'skr-' in nl or name.startswith('Zamzam_Museum-Skirting'):
        counts['SK'] += 1; cat = 'SDR-SK'
    elif 'a&v' in nl or 'av ' in nl or 'audio' in nl:
        counts['AV'] += 1; cat = 'SDR-AV'
    elif 'sdr-' in nl:
        counts['SDR'] += 1; cat = 'SDR'
    # Material samples (tiles, cladding, proposed finishes)
    elif 'proposed' in nl or 'tiles' in nl or 'الارفف' in name or \
         'تكسية' in name or 'بوابة' in name:
        counts['MATERIAL'] += 1; cat = 'MATERIAL'
    elif 'landscape' in nl:
        counts['DOC'] += 1; cat = 'LANDSCAPE'
    else:
        counts['OTHER'] = counts.get('OTHER', 0) + 1; cat = 'OTHER'
```

## Quick Count (No Extraction Needed)

```bash
grep -c 'Zamzam' ~/.hermes/scripts/.watchdog_state.json     # count entries
grep 'Zamzam' ~/.hermes/scripts/.watchdog_state.json | head -5  # sample paths
```
