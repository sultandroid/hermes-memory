# Phantom Photo Path Detection — Post-Delegation Verification

Subagents (Claude, Kimi) frequently invent photo paths that look plausible but don't exist on disk. This is the #1 source of broken images after any delegated redesign.

## Common Failure Modes

| Failure | Example Path | Root Cause |
|---------|-------------|------------|
| Wrong folder | `06-qa-lab/` instead of `05-qa-lab/` | Old folder name before v6.3 reorganization |
| Made-up filename | `projects/material-samples/patina-work.jpg` | File never existed — Claude invented it |
| Made-up filename | `06-qa-lab/real-quality-check.jpg` | Same — no such file |
| AI-generated | `GenAIImage_*.jpg` | Claude created an SVG/AI placeholder |
| Stale prefix | `../samaya-web/assets/` | Pre-v6.3 path not migrated |

## Detection Script (Run AFTER every delegated redesign)

```python
import re, os

BASE = "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/samaya-profile"
with open(f"{BASE}/v6/index.html") as f:
    html = f.read()

paths = set()
for m in re.findall(r"url\('([^']+)'\)", html):
    paths.add(m)

missing = []
for p in sorted(paths):
    full = os.path.join(BASE, p)
    if not os.path.exists(full):
        missing.append(p)

print(f"Total refs: {len(paths)}, Missing: {len(missing)}")
if missing:
    print("BROKEN PATHS:")
    for m in missing:
        fname = os.path.basename(m)
        found = []
        for root, dirs, files in os.walk(os.path.join(BASE, "assets")):
            for f in files:
                if f == fname:
                    rel = os.path.relpath(os.path.join(root, f), BASE)
                    found.append(rel)
        if found:
            print(f"  {m} → file exists at: {found}")
        else:
            print(f"  {m} → NOT FOUND anywhere in assets/")
```

## Fix Patterns

### Wrong folder (06-qa-lab → 05-qa-lab)
```bash
sed -i '' 's|06-qa-lab/|05-qa-lab/|g' v6/index.html
```

### Stale prefix (samaya-web/assets)
```bash
sed -i '' 's|../samaya-web/assets/|../assets/|g' v6/index.html
sed -i '' 's|../samaya-wassets/|../assets/|g' v6/index.html
```

### Made-up files
Search `assets/img/` for the filename, then patch the HTML to use the correct path. If not found, find a contextually similar real photo from the same section's asset folder.

### AI-generated images
Replace with a real project photo. Search `assets/img/07-projects/` or the appropriate scope folder for a relevant photo.

## Prevention (in delegation prompts)

Always include this instruction in every delegation task that adds/modifies photos:

```
"Use ONLY photo paths from EXISTING files in assets/img/ — verify each path exists on disk.
Do NOT invent file paths. If unsure what photo to use, list candidate paths for approval first."
```
