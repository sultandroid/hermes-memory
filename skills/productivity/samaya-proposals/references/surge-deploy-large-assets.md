# Surge Deploy — Large Asset Folders from OneDrive

When deploying static HTML sites where `assets/` is >100MB and lives on OneDrive, direct folder copy times out. Use selective extraction.

## Recipe: Copy Only Referenced Assets

```python
import os, re, shutil

src_base = "/path/to/project"
dst_base = "/tmp/surge-deploy"
os.makedirs(dst_base, exist_ok=True)

# Read HTML
with open(f"{src_base}/index.html", "r") as f:
    html = f.read()

# Read CSS files
css_text = ""
css_dir = f"{src_base}/css"
if os.path.isdir(css_dir):
    for fn in os.listdir(css_dir):
        if fn.endswith('.css'):
            with open(os.path.join(css_dir, fn)) as f:
                css_text += f.read()

# Collect all ../assets/ references from HTML + CSS
paths = set()
for text in [html, css_text]:
    for m in re.finditer(r'\.\./assets/[^"\')\\s]+', text):
        paths.add(m.group())

# Copy selectively, fixing ../ prefix
for rel in paths:
    clean = rel.replace("../", "", 1)
    src = os.path.join(src_base, clean)
    dst = os.path.join(dst_base, clean)
    if os.path.isfile(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    else:
        print(f"MISSING: {clean}")
```

## Path Fixing for Flat Deploy

If index.html was in a subdirectory (e.g., `v6/`) and uses `../assets/...` paths, convert to flat paths:

```bash
sed 's|\.\./assets/|assets/|g' src/index.html > /tmp/surge-deploy/index.html
```

## Verification

```bash
# HTML
curl -s -o /dev/null -w "%{http_code}" https://domain.surge.sh/
# CSS
curl -s -o /dev/null -w "%{http_code}" https://domain.surge.sh/css/00-tokens.css
# Image asset
curl -s -o /dev/null -w "%{http_code}" https://domain.surge.sh/assets/img/brand/logo.png
```

## Common Pitfalls

- **sed on macOS**: `sed -i` requires an extension arg on macOS (`sed -i '' 's//'`). Use pipe to new file instead.
- **Asset paths in CSS**: Also check CSS files for `url('../assets/...')` references — may not appear in HTML.
- **Background images in inline style**: `style="background-image:url('../assets/...')"` — use the regex `url\([^)]*\)` on the full HTML text.
- **Arabic directory names**: OneDrive folder names in Arabic script copy fine with Python `shutil`; just check `os.path.isfile()` before copying.
- **Missing references**: Some assets may be referenced but not present on disk (e.g., staging images, old variants). Log them but don't block deploy.
