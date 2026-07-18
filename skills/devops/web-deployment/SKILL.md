---
name: web-deployment
description: "Deploy static HTML/CSS/React sites to Surge.sh or shared hosting (Hostinger, cPanel) via SSH. Covers asset extraction, path fixing, image optimization, PHP data persistence, and CDN lifecycle."
version: 2.0.0
author: Hermes Agent
tags: [deployment, hosting, surge, ssh, hostinger, cpanel, static-site]
---

# Web Deployment

Deploy static sites (HTML/CSS, React/Vite builds) to Surge.sh preview hosting or production shared hosting (Hostinger, cPanel). Covers all phases: build, asset extraction, image optimization, deploy, verification, and iteration.

## Contents

1. [Surge.sh Deployment](#1-surgesh-deployment)
2. [Shared Hosting (SSH) Deployment](#2-shared-hosting-ssh-deployment)
3. [Pre-Deploy Checklist](#3-pre-deploy-checklist)

---

## 1. Surge.sh Deployment

### Prerequisites

```bash
# Check auth
surge whoami
# If not logged in: surge login (interactive, requires user password)
# NEVER run `surge logout` — it deletes ~/.netrc and requires password recovery
```

### Step-by-Step

**1. Build the app** (if React/Vite):
```bash
cd app && npm run build
# Output: dist/
```

**2. Copy to /tmp/ (avoid OneDrive slowness):**
```bash
rm -rf /tmp/surge-deploy && mkdir -p /tmp/surge-deploy
```

**3. Extract only referenced assets** (not entire multi-GB asset dirs):
Use Python regex to find all `url()` and `src=` references in HTML, copy only those files. See `surge-deploy` (now absorbed) for the full selective-asset-copy script.

**4. Fix relative paths** for flat root serving:
```bash
sed 's|\.\./assets/|assets/|g' index.html > deploy/index.html
```

**5. Check deploy size** — Surge Student/Free plan limit ~1GB:
```bash
du -sh deploy/
```

**6. Batch-optimize oversized images** (macOS):
```bash
find assets/ -type f -iname "*.jpg" -size +500k \
  -exec sips --resampleWidth 1920 --setProperty format jpeg \
    --setProperty formatOptions 85 {} --out {} \;
```

**7. Deploy:**

> ⚠️ **User approval required.** The user has explicitly forbidden deploying to Surge without a prior request (`"dont deploy to surge.sh until i asked you"`). Summarize what changed and ask before running any deploy command.

```bash
surge --project ./ --domain your-domain.surge.sh
# For large files (>2MB), use npx surge instead:
npx surge /tmp/deploy/ my-domain.surge.sh
```

**8. Verify:**
```bash
for i in 1 2 3; do
  code=$(curl -s -o /dev/null -w "%{http_code}" https://your-domain.surge.sh/)
  [ "$code" = "200" ] && break
  sleep 5
done

# Verify ALL referenced assets load (images, CSS, JS)
# HTML with relative paths like src="assets/logo.png" will 404 if assets/ wasn't copied to deploy dir
for url in $(grep -oP 'src="[^"]+"' index.html | sed 's/src="//;s/"//'); do
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://your-domain.surge.sh/$url")
  [ "$code" != "200" ] && echo "BROKEN ASSET: $url → $code"
done
```

### CDN Cold Start

Surge CDN edge nodes take 10-30 seconds to refresh after deploy. First hit may return 504 — this is normal. Wait and retry. Do NOT redeploy because of a 504.

### Web Content Extraction for Blocked Pages

When deploying content that references external articles (Medium, Cloudflare-protected), use `r.jina.ai` to extract clean markdown. See [`references/web-content-extraction.md`](references/web-content-extraction.md).

### CDN Cold Start — Asset 504

Surge's edge CDN nodes load assets progressively. A 504 on first hit for a large image (e.g. 150KB PNG) is normal — wait 5-10 seconds then retry. If the asset was just added by the deploy, the edge may not have it yet. ✅ Do NOT redeploy for a 504 on a freshly uploaded asset.

### Named HTML Files (not index.html)

When deploying standalone HTML documents (reports, plans, docs — not SPAs), use a descriptive filename instead of `index.html` so multiple documents can coexist in the same Surge domain:

```bash
rm -rf /tmp/surge-deploy && mkdir -p /tmp/surge-deploy
cp report-name.html /tmp/surge-deploy/report-name.html
# Also copy any referenced assets (images, CSS)
cp -r assets/ /tmp/surge-deploy/
npx surge /tmp/surge-deploy/ my-domain.surge.sh
```

Access: `https://my-domain.surge.sh/report-name.html`

### Asset Verification After Deploy

After every static-HTML deploy, verify ALL referenced images load. Relative paths like `src="assets/logo.png"` will 404 if `assets/` wasn't included in the deploy:

```bash
for img in $(grep -oP 'src="([^"]+\.(png|jpg|jpeg|gif|svg))"' index.html | sed 's/src="//;s/"//'); do
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://your-domain.surge.sh/$img")
  [ "$code" != "200" ] && echo "BROKEN: $img → $code"
done
```

### Cache-Busting

If old content persists after verified deploy, add `?v=N` to CSS `<link>` and redeploy:
```html
<link rel="stylesheet" href="css/main.css?v=2">
```

---

## 2. Shared Hosting (SSH) Deployment

### Prerequisites

- SSH access to web host (keys or password via sshpass)
- Knowledge of web root path
- PHP support (for data persistence)

### Finding the Source Code

When the user says the source isn't local, check these locations in order:

1. **OneDrive** — many project files live under `~/Library/CloudStorage/OneDrive-<org>/`
2. **Desktop** — check `~/Desktop/` for loose `.html` files and asset folders
3. **Backup directories** — look for `*-backups/` folders with `src-<timestamp>/` or `dist-<timestamp>/`
4. **`~/projects/`** — common dev projects location

Use `find` with grep for project indicators (vite.config, package.json, etc.) but avoid deep searches on OneDrive (slow). Check the `src/sections/` directory structure to identify the project type.

### Gallery/View Data Management (Vite + React Projects)

When adding or replacing gallery views (3D visualization photos with hotspot pins):

**1. Upload images to the server first:**

```bash
cat /path/to/new_photo.jpg | ssh -p <port> -o BatchMode=yes user@host "cat > /path/to/web-root/images/new_photo.jpg"
```

Use short readable server filenames (e.g., `lgf_vis017.jpg` instead of full MoC codes).

**2. Update gallery data in `Gallery.tsx` (or equivalent section file):**

```typescript
// New view in existing gallery
{viewName:'Gallery_View_N', filename:'/aseer/images/new_photo.jpg', desc:'View N – Description',
 hotspots:[{code:'MAT_CODE',x:50.0,y:50.0}]},

// New gallery entirely
{id:'gXX', title:'GXX – New Gallery', views:[
  {viewName:'GXX_View_1', filename:'/aseer/images/photo.jpg', desc:'View 1 – Overview',
   hotspots:[...]},
]},
```

**3. If hotspot data isn't ready**, create entries with empty hotspots `[]` — user can add them via admin panel (`?admin=1`).

**4. Rebuild and deploy only changed files** (see incremental deploy below).

**5. Preserve hotspot positions when replacing photos:** keep the same `hotspots:[{code, x, y}]` array — only change the `filename` path.

### Step-by-Step

**1. Build the app:**
```bash
npm run build
```

**2. Fix subdirectory paths** — if app lives at `domain.com/subdir/`, ALL absolute paths must use `/subdir/` prefix:
```bash
# Common offenders: gallery images, logo paths, background images in CSS
sed 's|/images/|/subdir/images/|g' src/file.tsx
```

In Vite, set `base: '/subdir/'` in `vite.config.ts`.

**3. Package:**
```bash
tar czf /tmp/deploy.tar.gz -C dist .
```

**4. Upload via SSH:**

Prefer SSH pipe over SCP — SCP can hang indefinitely on large transfers (observed on Hostinger/cPanel shared hosting port 65002), while SSH pipe with stdin redirection completes reliably:

```bash
# ✅ SSH pipe (reliable — use when SCP hangs)
cat /tmp/deploy.tar.gz | ssh -p <port> -o BatchMode=yes user@host "cat > /home/user/deploy.tar.gz"

# ❌ SCP (may hang on some hosts)
scp -P <port> /tmp/deploy.tar.gz user@host:/home/user/
```

If using SCP, always pass `-o BatchMode=yes` and `-o ConnectTimeout=10` to avoid hanging at the authentication prompt.

**6. Extract and clean on server:**
```bash
ssh -p <port> user@host "
  cd /path/to/web-root/subdir &&
  tar xzf /home/user/deploy.tar.gz &&
  rm /home/user/deploy.tar.gz &&
  rm -f ._* assets/._*     # remove Apple Double files macOS creates in tarballs
  chmod -R 755 .            # Hostinger/LiteSpeed: fix permissions for web server
"
```

### Incremental Deploy (only changed files, preferred)

When only a few files changed (e.g., JS + CSS bundles after rebuild), avoid the full tarball:

```bash
# 1. Build
node node_modules/vite/bin/vite.js build   # direct call (bypasses npm hang on OneDrive)

# 2. Copy PHP backend alongside build
cp sync.php dist/sync.php

# 3. Identify new asset hashes from build output:
#    dist/assets/index-<hash>.js  ← new JS
#    dist/assets/index-<hash>.css ← new CSS (may be unchanged)

# 4. Upload only changed files via SSH pipe:
tar czf /tmp/deploy-update.tar.gz -C dist index.html assets/index-<hash>.js assets/index-<hash>.css sync.php
cat /tmp/deploy-update.tar.gz | ssh -p <port> user@host "cat > /tmp/deploy-update.tar.gz"

# 5. Extract and clean old bundles on server:
ssh -p <port> user@host "
  cd /path/to/web-root/subdir &&
  tar xzf /tmp/deploy-update.tar.gz &&
  rm -f /tmp/deploy-update.tar.gz &&
  rm -f assets/._* assets/index-<old-hash>.js assets/index-<old-hash>.css
  # Remove ALL old bundles that aren't referenced by the new index.html
  for f in assets/index-*.js; do
    grep -q \"\$f\" index.html || rm -f \"\$f\"
  done
"
```

**Key benefits:**
- Much faster (KB instead of MB)
- Images stay on server — no re-upload
- Only the HTML + JS + CSS bundles change

### Vite Build Directly (OneDrive Workaround)

When `npm run build` hangs or terminal blocks it (detects as a server), use the Vite CLI directly:

```bash
node node_modules/vite/bin/vite.js build
```

This also bypasses TypeScript type-checking (avoids tsc timeout on OneDrive).
Use only when you know there are no type errors.

### PHP Data Persistence

For team collaboration, a single PHP endpoint on shared hosting reads/writes JSON to disk:

```php
$dataDir = __DIR__ . '/../../hotspot-data';  // OUTSIDE deploy dir
```

**🔴 Critical:** Data directory must be outside the build directory, otherwise `rm -rf <build-dir>` wipes all saved data on every deploy. Use `__DIR__ . '/../../hotspot-data'` (two levels above sync.php).

### SSH Troubleshooting

| Issue | Solution |
|-------|----------|
| Raw IP times out | Use hostname instead (different network interface behind CDN) |
| File too large | Source may be on OneDrive — extract only referenced assets |
| Hostinger subdomain 404 | Create directory manually: `mkdir -p ~/domains/sub.domain.com/public_html/` |
| Hostinger 403 Forbidden | SCP uploads create files with `-rw-------` (600) permissions. Web server cannot read them. Always `chmod -R 755` after upload on Hostinger/LiteSpeed. |
| Hostinger subfolder 404 (htaccess rewrite) | Hostinger sometimes has a root `.htaccess` that rewrites everything to a `/build/` subdirectory via `RewriteRule ^(.*)$ /build/$1 [L]`. Your files must go inside `/build/` as well. See [`references/hostinger-htaccess-rewrite.md`](references/hostinger-htaccess-rewrite.md) for the exact rule and fix. |
| Apple extended attributes | Use `COPYFILE_DISABLE=1` or strip with `dot_clean` |

### Deploying Named HTML Files (not index.html)

When deploying static HTML files that aren't the site root (e.g. `resource-management-plan.html` in a subfolder), the file must be named explicitly — not `index.html`. This allows multiple documents in the same subfolder.

```bash
scp -P <port> file.html user@host:~/domains/domain.com/public_html/subfolder/filename.html
ssh -p <port> user@host "chmod -R 755 ~/domains/domain.com/public_html/subfolder/"
```

Access URL: `https://domain.com/subfolder/filename.html`

If the HTML references local assets:
```bash
scp -P <port> -r assets/ user@host:~/domains/domain.com/public_html/subfolder/assets/
ssh -p <port> user@host "chmod -R 755 ~/domains/domain.com/public_html/subfolder/"
```

---

## 3. Pre-Deploy Checklist

### Contamination Check
Before every deploy, run these checks on the HTML file:

```bash
# 1. Line-number contamination (read_file → write_file bug)
if grep -qP '^\s*\d+\|' index.html; then
  echo "Line-number contamination! Fix with: sed -i '' 's/^[[:space:]]*[0-9]*|//' index.html"
fi

# 2. Truncation check
actual_lines=$(wc -l < index.html)
if [ "$actual_lines" -lt 500 ]; then
  echo "File may be truncated"
fi

# 3. Placeholder/leftover text
if grep -qi 'lorem ipsum\|todo\|tbd\|xxxx' index.html; then
  echo "Placeholder text found"
fi
```

### CSS Class Completeness
```bash
python3 -c "
import re
with open('index.html') as f: html = f.read()
style_m = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
css = style_m.group(1) if style_m else ''
html_classes = set(re.findall(r'class=\"([^\"]+)\"', html))
all_css = [c for m in re.findall(r'\.([a-zA-Z0-9_-]+)\s*\{', css) for c in m]
missing = sorted(html_classes - set(all_css))
if missing: print(f'MISSING CSS for: {missing}')
"
```

### Build Config Verification (SPA/React)

After building a React/Vite SPA with a config object (e.g. `SCHEDULE_FIELD_GROUPS` for tooltip cards, column definitions, API endpoints), verify the built JS contains your expected values:

```bash
# 1. Find the built JS asset
BUILT_JS=$(ls -t dist/assets/index-*.js 2>/dev/null | head -1)

# 2. Search for a unique key from your config that should NOT be in the build
if grep -q 'Ext. Height' "$BUILT_JS" 2>/dev/null; then
  echo "WARNING: Old dimension field 'Ext. Height' found — config may be stale"
fi

# 3. Positive check — new config value present
if grep -q 'Climate Control' "$BUILT_JS" 2>/dev/null; then
  echo "OK: Expected field found"
else
  echo "WARNING: Expected field NOT found — rebuild needed"
fi
```

**Why this matters:** The build can carry stale config if tsc times out on OneDrive-hosted JSON data files, or if an old build artifact wasn't cleaned. When source looks correct but deployed UI is wrong, compare deployed vs source config by grepping the minified JS:

```bash
curl -s 'https://your-domain.com/assets/index-*.js' | grep -c 'Climate Control'
```

### Asset Completeness Check — External Files (src=, url=)

**Check for broken image/asset paths:**
```python
import re, os, sys
with open('index.html') as f: html = f.read()
paths = set()
# CSS url() references
for m in re.finditer(r"url\('?\"?([^'\"\)]+)'?\"?\)", html): paths.add(m.group(1))
# HTML src= references (skip base64 data URIs)
for m in re.finditer(r'src="([^"]+)"', html):
    p = m.group(1)
    if not p.startswith('data:'): paths.add(p)
for m in re.finditer(r"src='([^']+)'", html):
    p = m.group(1)
    if not p.startswith('data:'): paths.add(p)
# Check each path exists relative to deploy directory
deploy_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
missing = []
for p in sorted(paths):
    full = os.path.join(deploy_dir, p)
    if not os.path.exists(full) and not p.startswith(('http://', 'https://', '//')):
        missing.append(p)
if missing:
    print(f'BROKEN ASSETS ({len(missing)}):')
    for m in missing: print(f'  ✗ {m}')
    sys.exit(1)
else:
    print(f'All {len(paths)} asset paths resolved ✓')
```

### Surge Auth Recovery (if ~/.netrc deleted)

1. **Plan A**: Write credentials directly:
   ```bash
   cat > ~/.netrc << 'NETRC'
   machine surge.sh
     login user@example.com
     password yourpassword
   machine api.surge.sh
     login user@example.com
     password yourpassword
   NETRC
   chmod 600 ~/.netrc
   ```
2. **Plan B**: Interactive PTY: `surge login` via `terminal(pty=true, background=true)`
3. **Plan C**: Ask user to run `surge login` directly

### Vite Build Warnings → Silent Runtime Crash (Three.js)

When Vite build output includes warnings like:
```
src/hooks/useInfiniteLights.ts (148:31): "WebGLRenderer" is not exported by ...
```
These are **not harmless**. `import * as THREE from 'three'` with older three.js (v0.184) fails rollup's export analysis — the bundle loads but Three.js symbols resolve to `undefined`, crashing before React mounts. Browser shows silent JS exception with no visible error.

**Pre-deploy check:**
```bash
npm run build 2>&1 | tee /tmp/build.log
if grep -q 'is not exported by.*three.module' /tmp/build.log; then
  echo "WARNING: Three.js import failure — verify rendering before deploy"
fi
```

**Fix:** Use individual named imports:
```typescript
// ❌ Breaks with three.js v0.184 + Rollup:
import * as THREE from 'three';
// ✅ Works:
import { WebGLRenderer, Scene } from 'three';
```

### Script `crossorigin` + No CORS Headers = Silent Failure

Vite builds emit `<script type="module" crossorigin>`. The `crossorigin` attribute requires CORS headers. Hostinger/shared hosting typically omit `Access-Control-Allow-Origin`. Result: script **fails silently** — blank page, no error message.

**Fix options (both verified working):**

1. **Remove only `crossorigin`** (recommended — preserves module behavior):
   ```bash
   sed -i '' 's/ crossorigin//g' dist/index.html
   ```
   The script still loads with `type="module"` — module scripts load same-origin without CORS headers. This keeps Vite's deferred module loading intact.

2. **Remove `type="module"` too** (only if MIME type is also wrong):
   ```bash
   sed -i '' 's/type="module" //g; s/ crossorigin//g' dist/index.html
   ```
   Vite's production bundle is an IIFE and runs as a regular script. Only needed if the server serves `.js` as `application/x-javascript` — browsers reject non-standard MIME types for module scripts but accept them for regular scripts.

**Prefer option 1** — it preserves Vite's deferred module loading (scripts load in parallel, execute after DOM parse) and only fixes the CORS issue.

### Server MIME Type for `.js` Files

Hostinger/LiteSpeed serves `.js` as `application/x-javascript`. For `<script type="module">`, browsers reject non-standard MIME types silently. After removing `type="module"`, the MIME type no longer matters (regular scripts don't enforce MIME checks).

**Quick check:** `curl -sI 'https://domain/assets/index-*.js' | grep -i content-type` — should be `application/javascript`, not `application/x-javascript`.

### Pitfalls

- **Stale build on server**: The most common cause of "source looks correct but UI is wrong" is a stale deployment. Run the Build Config Verification steps above against the LIVE URL (not just dist/) to confirm. Vite/tsc can silently produce different output if large JSON data files on OneDrive cause `tsc -b` to time out — the resulting build may exclude recent source changes.
  - **Workaround:** When `tsc -b` hangs on OneDrive-hosted JSON data files, bypass it by running vite build directly via a small script:
    ```js
    // build.mjs — place at project root, then `node build.mjs`
    import { build } from 'vite';
    const result = await build({ logLevel: 'info' });
    console.log('Build completed');
    ```
    This skips TypeScript type-checking but produces the correct JS/CSS output. Only use when you know there are no type errors.
- **Full tarball deploy is slow (47MB+ with images):** When the deploy includes a `tar czf` of the entire `dist/` (HTML + JS + CSS + all images), SCP takes minutes. Prefer incremental deploy of only changed files:
  ```bash
  # Identify the new asset filenames from the build output, then:
  scp -P <port> assets/index-<hash>.js   user@host:/remote/assets/
  scp -P <port> assets/index-<hash>.css  user@host:/remote/assets/
  scp -P <port> index.html               user@host:/remote/
  scp -P <port> sync.php                 user@host:/remote/
  # Clean up old backups and Apple Double files:
  ssh -p <port> user@host "cd /remote && rm -f ._* assets/._*"
  # Clean old bundles not referenced by current index.html:
  ssh -p <port> user@host "cd /remote && for f in assets/index-*.js; do grep -q \"\$f\" index.html || rm -f \"\$f\"; done"
  ```
  Images rarely change between builds (they're static reference photos) and don't need re-uploading.
- **Ask before deploying**: User said "dont deploy to surge without i asked you to deploy". Always summarize changes and ask before running surge.
- **Patching deployed JS is fragile**: When the build toolchain is broken (Node version incompatibility, corrupted node_modules), you may be tempted to patch the compiled JS directly. See [`references/patching-deployed-js.md`](references/patching-deployed-js.md) for the technique and its many pitfalls. **Always backup the original file** and verify the page renders after upload — a single wrong character in minified JS crashes the entire app silently.
- **CHANGELOG before deploy**: Every change must be logged before deploying.
- **`npx surge` required for files >2MB with embedded images**: Local `surge` CLI fails with `TypeError: Cannot read properties of undefined (reading 'filename')` at varying upload percentages (27%, 73%, 77% observed) on files >2MB with embedded base64 images. The fix is `npx surge` instead. **However, even `npx surge` may take 2-4 attempts at different failure points before succeeding.** Each attempt must use a completely fresh `/tmp/` directory — reusing a previous attempt's directory carries stale metadata that perpetuates the error. Upload speed on Student plan: ~20-30 minutes for 6.7MB. Deploy via background PTY with 600s timeout and `notify_on_complete=true`. Monitor: poll every 60-180s to see the upload bar advancing 2-5% per poll. Once past the last failure point (typically 77-82%), success follows within 3-5 minutes.
- **Surge `--project ./` from `/tmp/` picks up ALL files**: Running `surge --project ./` from `/tmp/` deploys every file in `/tmp/` (hundreds of files, potentially >100MB). Always create an isolated deploy directory with only the files to publish:
  ```bash
  rm -rf /tmp/surge-deploy && mkdir -p /tmp/surge-deploy
  cp index.html /tmp/surge-deploy/
  cp -r assets/ /tmp/surge-deploy/
  npx surge --project /tmp/surge-deploy/ --domain my-domain.surge.sh
  ```
- **OneDrive + git slowness**: Git init/commit/push operations on OneDrive paths can time out. Copy files to `/tmp/` first, run git from there, push. The `/tmp/` version becomes the authoritative git source.
- **OneDrive file locks**: Files under OneDrive may be unreadable. Copy to `/tmp/` first.
- **OneDrive sparse files break tar**: OneDrive macOS creates sparse files that cause `tar: lseek(SEEK_HOLE) failed: Operation timed out` and produce truncated archives (e.g. 757B instead of 90MB). **Always copy dist/ to /tmp/ before packaging:** `cp -R dist /tmp/aseer-dist && cd /tmp/aseer-dist && tar czf /tmp/aseer-deploy.tar.gz .`
- **URL-encoded filenames**: `Oddy%20Test_Lab.jpg` won't match filesystem. Use `urllib.parse.unquote()`.
- **macOS TCC permission**: Files from Downloads may have quarantine flags preventing copy.
- **React/Vite base path**: Must match deploy subdirectory. Set `base: '/app/'` in `vite.config.ts`.
- **Pre-deploy build verification**: Three.js import warnings, `crossorigin`/MIME type, and config staleness can all cause deployed-but-broken sites. Run the checks in [`references/build-verification-pre-deploy.md`](references/build-verification-pre-deploy.md) before every deploy.

### Project Reference Files

- [`references/aseer-material-explorer-deployment.md`](references/aseer-material-explorer-deployment.md) — Exact server paths, port, SSH commands, incremental deploy template, and gallery structure for the Aseer Museum Material Explorer site on `samaya-factory.com`.
- **technical-proposals folder structure** — When deploying technical proposals/project plans to samaya-factory.com, use the standard folder hierarchy:
  `/home/u517606786/domains/samaya-factory.com/public_html/build/technical-office/Technical-Proposals/PROJECT-NAME/index.html`
  - Example: `RCRC-Exhibition/index.html` → https://samaya-factory.com/build/technical-office/Technical-Proposals/RCRC-Exhibition/index.html
  - Create the directory chain before upload: `ssh ... mkdir -p .../PROJECT-NAME/`
  - Upload via SSH pipe (cat file | ssh ... cat > ...)
  - Set chmod 755 on the project folder after upload
  - Use `index.html` as filename so the URL resolves cleanly without the filename
  - HTTP 200 verification: `curl -s -o /dev/null -w "%{http_code}" https://samaya-factory.com/build/technical-office/Technical-Proposals/PROJECT-NAME/index.html`
