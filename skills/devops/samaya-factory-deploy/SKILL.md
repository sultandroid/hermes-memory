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

## Permissions

After uploading, fix file permissions so the web server can read them:
```bash
ssh -p 65002 u517606786@samaya-factory.com 'chmod 644 domains/samaya-factory.com/public_html/build/aseer/index.html domains/samaya-factory.com/public_html/build/aseer/assets/*'
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

## Steps

1. **Build**
   ```bash
   node node_modules/vite/bin/vite.js build
   ```
   (Do NOT use `npm run build` — it times out.)

2. **Package**
   ```bash
   tar -czf deploy.tar.gz index.html assets/ sync.php
   ```

3. **Deploy via SSH pipe**
   ```bash
   cat deploy.tar.gz | ssh u517606786@samaya-factory.com -p 65002 'cd build/aseer && tar -xzf -'
   ```

4. **Fix symlink** (if OneDrive resets it)
   ```bash
   ssh u517606786@samaya-factory.com -p 65002 'ln -sfn public/aseer/images build/aseer/images'
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

## Related References

- `references/html-css-audit-repair.md` — Systematic workflow for auditing and fixing HTML/CSS issues (tag balance, section numbering, page numbers, CSS fixes) on deployed production documents.

## Pitfalls
- `npm run build` times out — always use the direct `vite.js` path
- **Never stage work in /tmp** — the user's project files belong in `~/Documents/`. Copy/download files to `~/Documents/{project}/` not `/tmp/`. The user explicitly corrected this.
- When converting a monolithic HTML to page-split, work in the project directory from the start (`~/Documents/{project-name}/`). Do not create the project in /tmp and copy later.
- OneDrive macOS can corrupt files if written directly — stage build output to the project folder and use AppleScript `duplicate` via Finder if writing to OneDrive paths
- The images symlink at `public/aseer/images` gets reset when OneDrive syncs — check after every deploy
- **_DO NOT_ use complex build pipelines with placeholder systems, Puppeteer, or post-processing that modifies HTML tags.** Simple concat (read files, join, write) is the only approach that has worked reliably for technical proposal documents. Placeholder systems introduce fragility when page counts or section numbers shift. Post-processing regex on HTML tags has caused `>>` tag-break bugs that silently corrupt every `<section>` in the document.
- For technical proposals, keep CSS inline in `base.html`, not in external files. External CSS can fail to load (permissions, path issues, caching) and the user expects everything in one file.
