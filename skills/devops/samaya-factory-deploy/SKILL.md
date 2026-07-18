---
name: samaya-factory-deploy
description: "Deploy static site to samaya-factory.com shared hosting"
version: 1.0.0
author: Samaya Tech Office
---

# Samaya Factory Deploy

Deploy `aseer` subdirectory site to samaya-factory.com shared hosting.

## Server Path

**Important:** The `.htaccess` at samaya-factory.com rewrites all requests to `/build/`. The actual web root is `domains/samaya-factory.com/public_html/` but the deploy target for the aseer site is:

```
domains/samaya-factory.com/public_html/build/aseer/
```

For Samples subdirectory:
```
domains/samaya-factory.com/public_html/build/Samples/{CODE}/
```

Not `public_html/` directly — that's a catch-all default area, not the domain-specific document root.

## Incremental Deploy (data-only changes)

When only `Gallery.tsx` data changes (no CSS, no new components):

```bash
cd /path/to/repo
npm run build
cd dist
tar czf /tmp/aseer-assets.tar.gz index.html assets/
scp -P 65002 -o StrictHostKeyChecking=no /tmp/aseer-assets.tar.gz u517606786@samaya-factory.com:/home/u517606786/
ssh -p 65002 -o StrictHostKeyChecking=no u517606786@samaya-factory.com "cd /home/u517606786/domains/samaya-factory.com/public_html/build/aseer && tar xzf /home/u517606786/aseer-assets.tar.gz && rm /home/u517606786/aseer-assets.tar.gz"
```

This avoids re-uploading all images (115MB) when only JS/CSS changed.

## Permissions

After uploading, fix file permissions so the web server can read them:
```bash
ssh -p 65002 u517606786@samaya-factory.com 'chmod 644 domains/samaya-factory.com/public_html/build/aseer/index.html domains/samaya-factory.com/public_html/build/aseer/assets/*'
```

**New images uploaded via SCP start with 700 permissions** (macOS SCP default). The web server returns 403. Always fix:
```bash
ssh -p 65002 u517606786@samaya-factory.com 'chmod 644 domains/samaya-factory.com/public_html/build/aseer/images/*.jpg'
```

## Technical Proposal Deploy (RCRC-Exhibition)

The RCRC Exhibition proposal lives at:
```
~/Documents/RCRC-Exhibition/
```

It uses a **page-split + concat** approach — not a complex build pipeline:

```bash
cd ~/Documents/RCRC-Exhibition
npm run build          # concatenates pages/ into dist/index.html
npm run deploy         # scp to server
```

**Project structure:**
```
~/Documents/RCRC-Exhibition/
├── base.html           ← template (DOCTYPE, inline CSS, HTML wrapper)
├── pages/              ← 49 individual page files (01-cover.html … 49-appendices.html)
├── scripts/assemble.js ← simple concat (no post-processing, no placeholder system)
├── dist/index.html     ← output
└── package.json
```

**Key rules:**
- Each page file is ONE `<section class="page">` block — edit any page independently without breaking others
- ALL CSS stays inline in `base.html` — no external CSS files (avoids loading failures)
- No post-processing that modifies HTML tags — regex replacements on tags caused `>>` tag-break bug
- SECTION comments between pages are preserved in the page files
- Page numbers are hardcoded in footers (e.g. `صفحة 2 / 49`) — page position is fixed by `pages/` filenames, so editing content within a page won't shift other pages or break the TOC
- The `dist/index.html` is produced by simple file concatenation in filename order — no template placeholders, no Puppeteer, no page-break measurement

**Converting a monolithic file to page-split:**
```python
# Extract <section class="page"> blocks
page_starts = [m.start() for m in re.finditer(r'<section[^>]*class="[^"]*page[^"]*"[^>]*>', html)]
page_ends = [html.find('</section>', ps) + len('</section>') for ps in page_starts]

# Each page = html[page_starts[i]:page_ends[i]]
# Inter-page SECTION comments come from the gap between page_ends[i-1] and page_starts[i]
# Save each as pages/{NN}-{title}.html
```

**Do NOT use:**
- Placeholder-based rendering ({{page_number}}, {{total_pages}}) — breaks when pages shift
- Puppeteer page measurement — unreliable with file:// protocol
- External CSS files — the original monolithic had all CSS inline and it worked reliably
- Post-processing that regex-replaces HTML tags — always ends up creating broken markup

## Pre-deploy: Check git status

Before editing any file in a git-tracked project, check for uncommitted changes:

```bash
cd /path/to/app
git status
git diff src/sections/Gallery.tsx  # or any file you plan to edit
```

**Why:** The file on disk may have accumulated uncommitted design changes from a previous session. Editing it without checking can deploy unintended design changes alongside your data-only changes. If the user says "go back to the morning version" or "this is the old design", use `git show <commit>:<file>` to restore the exact original, then re-apply only your data changes.

## Steps

1. **Build from /tmp/** (OneDrive paths cause `ETIMEDOUT` and `lseek(SEEK_HOLE)` errors during build and tar)

   ```bash
   APP="/path/to/OneDrive/app"
   mkdir -p /tmp/aseer-build/src/sections /tmp/aseer-build/src/hooks /tmp/aseer-build/src/lib /tmp/aseer-build/src/components /tmp/aseer-build/src/pages /tmp/aseer-build/src/data/schedules /tmp/aseer-build/src/components/ui /tmp/aseer-build/public/images /tmp/aseer-build/public/fonts

   # Config files — use cat pipe to avoid OneDrive timeout
   for f in package.json package-lock.json vite.config.ts tsconfig.json tsconfig.app.json tsconfig.node.json tailwind.config.js index.html; do
     cat "$APP/$f" > "/tmp/aseer-build/$f"
   done

   # Source files
   for f in src/index.css src/main.tsx src/App.tsx; do
     cat "$APP/$f" > "/tmp/aseer-build/$f"
   done
   for f in src/sections/*.tsx; do
     cat "$APP/$f" > "/tmp/aseer-build/$f"
   done
   for f in src/hooks/*.ts src/lib/*.ts; do
     cat "$APP/$f" > "/tmp/aseer-build/$f"
   done
   for f in src/components/*.tsx; do
     cat "$APP/$f" > "/tmp/aseer-build/$f"
   done
   for f in src/components/ui/*.tsx; do
     cat "$APP/$f" > "/tmp/aseer-build/src/components/ui/$(basename $f)"
   done
   for f in src/data/*.json; do
     cat "$APP/$f" > "/tmp/aseer-build/$f"
   done
   for f in src/data/schedules/*.json; do
     cat "$APP/$f" > "/tmp/aseer-build/src/data/schedules/$(basename $f)"
   done

   # Images
   for img in *.jpg *.png; do
     cat "$APP/public/images/$img" > "/tmp/aseer-build/public/images/$img"
   done

   # Install deps (first time only)
   cd /tmp/aseer-build && npm install --legacy-peer-deps

   # Build
   cd /tmp/aseer-build && npx vite build
   ```

2. **Package from /tmp/**
   ```bash
   cd /tmp/aseer-build/dist
   tar czf /tmp/aseer-deploy.tar.gz .
   ```

3. **Upload via SCP**
   ```bash
   scp -P 65002 -o StrictHostKeyChecking=no -o ConnectTimeout=30 /tmp/aseer-deploy.tar.gz u517606786@samaya-factory.com:/home/u517606786/
   ```

4. **Extract and clean on server**
   ```bash
   ssh -p 65002 -o StrictHostKeyChecking=no u517606786@samaya-factory.com "cd /home/u517606786/domains/samaya-factory.com/public_html/build && rm -rf aseer && mkdir aseer && cd aseer && tar xzf /home/u517606786/aseer-deploy.tar.gz && rm /home/u517606786/aseer-deploy.tar.gz && chmod 755 sync.php 2>/dev/null"
   ```

5. **Verify** — open the site and check file listing.

## Technical Office Documents Deploy

Plan documents (SMP, Resource Mgmt Plan, etc.) deploy to:

```
domains/samaya-factory.com/public_html/build/technical-office/
```

**Workflow:**
```bash
cp /tmp/updated_doc.html stakeholder-management-plan.html
tar -czf deploy.tar.gz stakeholder-management-plan.html
cat deploy.tar.gz | ssh u517606786@samaya-factory.com -p 65002 'cd domains/samaya-factory.com/public_html/build/technical-office/ && tar -xzf -'
ssh -p 65002 u517606786@samaya-factory.com 'chmod 644 domains/samaya-factory.com/public_html/build/technical-office/*.html'
```

**Verify:** `curl -s "https://samaya-factory.com/build/technical-office/<filename>" | head -c 200`

## Samples Subdirectory Deploy

Sample landing pages (QR targets) deploy to a different path:

```
public_html/build/Samples/{CODE}/
```

See the `sample-submittal-system` skill's `references/qr-landing-page-deploy.md` for the full workflow.

## Admin Panel
Append `?admin=1` to the URL for admin access.

### Companion document sync

When specialist deployment data changes, plan documents are interdependent. For Aseer Museum: SMP + Resource Plan are paired — update both, not one.

**Pitfall:** deploying an updated SMP without also updating the Resource Plan leaves stale data live. Before deploying, check which companion documents reference the same specialist assignments.

## Public Shared Assets

The server hosts shared project assets (logos, templates, reference files) at public URLs so any agent working outside the repo can fetch them directly.

**Location on server:**
```
domains/samaya-factory.com/public_html/build/assets/logos/
```

**Public URLs (no auth required):**
| Asset | URL |
|-------|-----|
| Samaya logo (transparent) | `https://samaya-factory.com/assets/logos/samaya-logo-trans.png` |
| Samaya logo (opaque) | `https://samaya-factory.com/assets/logos/samaya-logo.png` |

**Why `/build/` prefix:** The `.htaccess` at root rewrites all requests to `/build/`. So `https://samaya-factory.com/assets/logos/...` resolves to `public_html/build/assets/logos/...`.

**To add a new shared asset:**
```bash
# 1. Create the directory
ssh -p 65002 u517606786@samaya-factory.com \
  "mkdir -p ~/domains/samaya-factory.com/public_html/build/assets/logos"

# 2. Upload via SSH pipe (reliable, avoids SCP hang)
cat /path/to/local/file.png | ssh -p 65002 u517606786@samaya-factory.com \
  "cat > ~/domains/samaya-factory.com/public_html/build/assets/logos/filename.png"

# 3. Fix permissions (SSH pipe creates files with 644, but verify)
ssh -p 65002 u517606786@samaya-factory.com \
  "chmod 644 ~/domains/samaya-factory.com/public_html/build/assets/logos/*"

# 4. Verify
curl -s -o /dev/null -w "%{http_code}" https://samaya-factory.com/assets/logos/filename.png
# Expect: 200
```

**Document in AGENTS.md:** After adding a new shared asset, add a row to the style guide table in the repo's `AGENTS.md` so every agent knows the public URL.

## Related References

- `references/html-css-audit-repair.md` — Systematic workflow for auditing and fixing HTML/CSS issues (tag balance, section numbering, page numbers, CSS fixes) on deployed production documents.
- `references/aseer-gallery-data-structure.md` — Gallery entry format, floor classification, VIS-to-gallery mapping, image naming conventions, and server paths for the Aseer Museum viz app.

## Pitfalls
- `npm run build` times out — always use the direct `vite.js` path
- **Never stage work in /tmp** — the user's project files belong in `~/Documents/`. Copy/download files to `~/Documents/{project}/` not `/tmp/`. The user explicitly corrected this.
- **Data-only changes only** — when user says "just add sections, add new photos", do NOT change design/layout/CSS/JSX structure. Only append to the `galleryData` array. Changing the design triggers user frustration ("you changed the design totally").
- **Deploy incrementally** — when only JS/CSS changed, deploy only `index.html` + `assets/`, not the full app (avoids re-uploading 115MB of images).
- **New images get 700 permissions** — macOS SCP sets 700 on uploaded files. Always `chmod 644` new images or they return 403.
- When converting a monolithic HTML to page-split, work in the project directory from the start (`~/Documents/{project-name}/`). Do not create the project in /tmp and copy later.
- OneDrive macOS can corrupt files if written directly — stage build output to the project folder and use AppleScript `duplicate` via Finder if writing to OneDrive paths
- The images symlink at `public/aseer/images` gets reset when OneDrive syncs — check after every deploy
- **_DO NOT_ use complex build pipelines with placeholder systems, Puppeteer, or post-processing that modifies HTML tags.** Simple concat (read files, join, write) is the only approach that has worked reliably for technical proposal documents. Placeholder systems introduce fragility when page counts or section numbers shift. Post-processing regex on HTML tags has caused `>>` tag-break bugs that silently corrupt every `<section>` in the document.
- For technical proposals, keep CSS inline in `base.html`, not in external files. External CSS can fail to load (permissions, path issues, caching) and the user expects everything in one file.
