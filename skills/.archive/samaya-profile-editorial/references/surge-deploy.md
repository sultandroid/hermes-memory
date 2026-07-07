# Surge.sh Deploy — Samaya Profile

## Quick Deploy (recommended, handles all 33 CSS files + assets)
```bash
rm -rf /tmp/samaya-profile-deploy && mkdir -p /tmp/samaya-profile-deploy/css
v6="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/samaya-profile/v6"

# HTML path fix
sed 's|../assets/|assets/|g' "$v6/index.html" > /tmp/samaya-profile-deploy/index.html

# CSS (33 files)
cp "$v6/css/"*.css /tmp/samaya-profile-deploy/css/

# Asset copy (from the profile root)
python3 -c "
import os, re, shutil
from urllib.parse import unquote
src = '$v6/..'
dst = '/tmp/samaya-profile-deploy'
paths = set()
for f in ['$v6/index.html'] + [os.path.join('$v6/css',f) for f in os.listdir('$v6/css') if f.endswith('.css')]:
    with open(f) as fh:
        for m in re.finditer(r'\.\./assets/[^\"\'\\)\\s]+', fh.read()): paths.add(m.group())
for rp in list(paths):
    sp = os.path.join(src, rp.replace('../','',1))
    dp = os.path.join(dst, unquote(rp).replace('../','',1))
    if os.path.isfile(sp): os.makedirs(os.path.dirname(dp), exist_ok=True); shutil.copy2(sp, dp)
"

# Deploy
cd /tmp/samaya-profile-deploy && surge --project ./ --domain samaya-factory-profile.surge.sh
rm -rf /tmp/samaya-profile-deploy
```

## Auth
- Email: mohamedsultanabbas@gmail.com (Student plan)
- If `surge logout` was run, re-auth requires interactive `surge login` via PTY
- DO NOT run `surge logout` unless explicitly asked — it breaks auth permanently until the user re-enters credentials

## Verify deployment
```bash
curl -s -o /dev/null -w "%{http_code}" "https://samaya-factory-profile.surge.sh/"
```

## Pitfalls
- Surge CDN may return 504 on first load, then 200 after a few seconds — normal
- Always rebuild deploy dir from scratch; stale assets cause confusion
- Current deploy size: ~90-120MB (depending on image count)
