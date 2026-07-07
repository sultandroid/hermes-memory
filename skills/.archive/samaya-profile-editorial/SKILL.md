---
name: samaya-profile-editorial
description: Edit, redesign, and deploy the Samaya Factory company profile website — page-by-page editorial redesign, photo replacement, overflow fixing, and surge.sh deployment.
related_skills: [productivity/samaya-factory-profile]
---

# Samaya Factory Profile — Editorial Workflow

## Design System
- **Colors**: Navy `#111827` (var(--v3-ink)), Gold `#C9A24B` (var(--v3-gold)), Cream `#F7F2E8` (var(--v3-paper))
- **Fonts**: **Cairo** (Arabic, 400-900 weights), **Inter** (English), **Cormorant Garamond** (serif/italic)
- **Format**: RTL, A4 landscape (297mm × 210mm)
- **Brand slogan**: "هندسة الفنّ. لصناعة الإرث." / "Engineering Art. For Crafting Legacy." — **never change this**
- **Google Fonts URL format**: use `wght@` (with `@`) not `wght;` — `family=Cairo:wght@400;500;600;700;800;900` is correct, `wght;500` silently fails

## Key Rules (from user corrections)
1. **No new blocks/sections** — replace existing photos/content only unless explicitly asked
2. **Photos in Materiality grid use `background-size: contain`** (NOT `cover`) — user rejected cropping
3. **Page overflow**: Remove `overflow: hidden` + `height: calc(210mm - 22mm - 14mm)` from every `.content` rule. Also change global `.page` in `00-tokens.css` from `height: 210mm; overflow: hidden` to `height: auto; min-height: 210mm; overflow: visible` — this is THE ROOT fix for all overflow
4. **Check overflow on every page** after any change — re-add `height: calc()` only on specific pages that must fill exactly one page (like `.ed-back-cover`)
5. **Update TOC** (section id="p2") whenever pages are added/removed/renumbered — always verify after content changes
6. **Concise editorial text** — active Arabic verbs ("نصنع", "نبني"), em-dash rhythm, museum-catalog tone. No marketing fluff. User said "dont talk too much". AR primary, EN secondary. Use `·` bullet separators for compact lists
7. **Delegate**: Claude for design/text/redesign, Kimi for fixes/overflow patches
8. **Never change the brand slogan** on the cover: "صناعة الإرث. هندسة الفنّ." / "Crafting Legacy. Engineering Art." — this is sacred
9. **Gallery curation**: When too many photos overflow a page, curate to 6-9 best — don't add more pages unless user asks. Keep: most impressive/credible, Remove: duplicates/weak
10. **Materiality grid cell height**: 22mm (reduced from 48mm to prevent massive overflow with 70+ cells). Cells use `background-size: contain` + `background-repeat: no-repeat`

## Photo Source Paths
- WhatsApp downloads: `/Users/mohamedessa/Library/Containers/net.whatsapp.WhatsApp/Data/tmp/documents/`
- OneDrive workshop photos: `/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Orders/2025/`
- From Downloads: `/Users/mohamedessa/Downloads/`
- Best high-res: `.../classified/website-ready/06-Best-High-Res/`
- Copy target: `assets/img/` (organized by section)

## Image Organization (Section-Based Folders)

All images live under `assets/img/` organized by section:

```
assets/img/
  01-cover/               — cover & about page photos
  02-about/               — about section photos
  03-capacity/            — operational capacity
  04-engineering/         — BIM/engineering CAD screenshots
  05-qa-lab/              — QA/QC lab instruments, testing
  06-machinery/           — CNC, laser, edge banders
  07-projects/            — project photos (prefixed by source/project)
  08-scope/               — scope photos (veneer, doors, print, replicas, FFE)
  09-wayfinding/          — wayfinding/signage
  10-material-samples/    — patina, finishes, material boards
  11-process/             — workshop process, fabrication
  brand/                  — logos (keep as-is)
  badges/                 — Vision 2030, Saudi Made, BIM (keep as-is)
  vendors/                — software vendor logos (keep as-is)
```

When adding new photos:
1. Copy to the correct section folder
2. Use clean lowercase-hyphenated names (e.g. `cnc-router-clean.jpg`)
3. Update all `../assets/img/` references in HTML and CSS
4. Verify no broken refs: check each `url('../assets/img/...')` resolves to a file

## Image Requirements
- Compress large files with `sips -Z 2000` before copying to assets
- Every image used exactly once — run Counter() check on all `../assets/img/` references
- Grid photos must be equal size (Materiality: 48mm height, background-size: contain, background-repeat: no-repeat)
- Multi-page OK for dense content (Materiality, Replicas gallery)

## Deploy to Surge.sh

### Quick Deploy Script
```bash
# Build deploy directory from scratch
rm -rf /tmp/samaya-profile-deploy && mkdir -p /tmp/samaya-profile-deploy/css
v6="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/samaya-profile/v6"

# Copy HTML + fix asset paths
sed 's|../assets/|assets/|g' "$v6/index.html" > /tmp/samaya-profile-deploy/index.html

# Copy all CSS (33 files)
cp "$v6/css/"*.css /tmp/samaya-profile-deploy/css/

# Copy referenced assets (run the deploy script)
cd "$v6/.." && python3 -c "
import os, re, shutil
from urllib.parse import unquote
src = '$v6/..'
dst = '/tmp/samaya-profile-deploy'
paths = set()
# Collect all refs from HTML + CSS
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

# Clean up
rm -rf /tmp/samaya-profile-deploy
```

### Verify
```bash
curl -s -o /dev/null -w "%{http_code}" "https://samaya-factory-profile.surge.sh/"
```

### Auth
- Email: mohamedsultanabbas@gmail.com (Student plan)
- If `surge logout` was run, re-auth requires interactive `surge login` via PTY mode

## Page-by-Page Redesign
1. Read page HTML + CSS rules
2. Understand what it communicates
3. Redesign: rewrite text, resize/reposition photos, vary layout
4. Check overflow — remove `height: calc(210mm - 22mm - 14mm)` if content overflows
5. Update TOC if page count changed
6. Patch index.html + relevant CSS
7. Move to next page

## Version Tracking — CHANGE LOG Mandatory

**Every change to the profile MUST be recorded in CHANGELOG.md** at `/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/samaya-profile/CHANGELOG.md`.

Format:
```
| Date | Page(s) | Change | Author | Backup |
|---|---|---|---|---|
| 2026-06-07 | #p14 | Fixed CMYK page — matched CSS | Claude | — |
```

This enables undo by restoring from git, v5 backup, or snapshot.

Three reference docs exist alongside the project:
- `README.md` — project overview, deploy instructions
- `STYLEGUIDE.md` — design system, page structure, images per page, git undo commands
- `CHANGELOG.md` — version tracking, backup/restore workflow

## Pre-Change Backup Workflow

Before making ANY change to the profile (HTML, CSS, or images):

```bash
BACKUP_DIR="/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/samaya-profile/v6-backups"
TS="v6-code-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR/$TS/css"
cp "v6/index.html" "$BACKUP_DIR/$TS/"
cp "v6/css/"*.css "$BACKUP_DIR/$TS/css/"
echo "Backup: $BACKUP_DIR/$TS"
```

- **Code-only** (no images — too large, images rarely change path)
- Backup label used in CHANGELOG entry for easy restore

## Version Tracking — CHANGELOG Mandatory

**Every change MUST be recorded in CHANGELOG.md** at:
`/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/samaya-profile/profile-info-and-control/CHANGELOG.md`

Use vX.Y versioning:
```markdown
## v6.4 — Description (2026-06-07)

- **#pN** Page/page description
- Backup: `v6-backups/v6-code-20260607_073458`
```

## Documentation Files

All project docs live in `profile-info-and-control/`:
- `README.md` — project overview, deploy instructions
- `STYLEGUIDE.md` — design system, 39-page structure, images per page, undo commands
- `CHANGELOG.md` — version tracking with vX.Y format
- `font-gallery.html` — Arabic font comparison tool

## Undo Workflow
```bash
# Restore from backup
cp "v6-backups/v6-code-20260607_073458/index.html" v6/index.html
cp "v6-backups/v6-code-20260607_073458/css/"*.css v6/css/

# Or from git
git log --oneline
git checkout <hash> -- v6/index.html

# Or from v5 reference
# Extract a section block from v5/index.html manually
```

## No-Deploy Workflow (User-Enforced)

The user explicitly said: "dont deploy to surge without i asked you to deploy." This is a hard rule:

1. Do NOT run surge or any deploy command
2. Make changes to v6/index.html and v6/css/*.css only
3. Verify images exist on disk (no curl to surge URLs)
4. Show the change summary — wait for explicit approval before deploying

## Hold Point Icons Pattern

When the user says "use icons" for the 5 QA/QC hold points:

Replace numbered spans with inline SVG icons (viewBox="0 0 20 20", stroke="#A47A1F", fill="none", stroke-width="1.5"):
01=document, 02=checkmark, 03=magnifier, 04=flask, 05=box
Keep small number (10pt italic) beside icon. CSS: `.v3-method .v3-method-tl-icon { inline-size: 7mm; block-size: 7mm; flex-shrink: 0; }`

## Version Tracking — CHANGE LOG Mandatory

After structural edits (pages added/removed/renumbered), audit all footer `.num` values for gaps and mismatches:
- p1 (cover) and p27 (back cover) have no page number — expected
- All other pages should have sequential numeric (or letter-suffixed like 13b) footers
- Section tags may not match footer numbers — fix the footer to match actual page position, not tag prefix
- TOC (`#p2`) page references must match footer numbers — update both

```python
# Audit pattern
import re
with open("v6/index.html") as f: html = f.read()
for m in re.finditer(r'<div class="num">([^<]+)<', html):
    print(f"  Page num: {m.group(1)}")
```

## Big Task Execution (User-Enforced)

For large multi-page redesigns (e.g. splitting Materiality into 5 pages):

1. **Break into small controlled sub-tasks** — one goal per agent call
2. **Never rewrite the full profile in one pass** — use sequential focused edits
3. After each sub-task, verify (deploy + curl check) before moving on
4. Monitor progress with CLI checks between sub-tasks
5. If a fix fails, stop and diagnose root cause before retrying

**Pitfall**: Patching the same file twice in rapid succession causes "file was modified by sibling subagent" warnings. Wait for one agent to finish before starting the next on the same file.

## Flagship Project Layout
Each flagship (p4-flag4 through p4-flag8) has `.proj-flagship .content { grid-template-columns: 1.2fr 0.8fr; }` in RTL. 
- Default: `pf-panel` (text) first → text on RIGHT, `pf-hero` (photo) second → photo on LEFT
- To flip: swap DOM order (put `pf-hero` before `pf-panel`)

## CSS Architecture (v6.1+)

The CSS is split into 33 focused files:

```
00-tokens.css      — design tokens, CSS variables, print, grid-12, reset
01-reset.css       — page chrome (page-header, .content, @page rules)
02-utilities.css   — grid helpers, spacing, typography utilities
03-components.css  — shared components: cards, badges, stats, process
01-base.css        — reduced: page-specific styles only
02-scope-base.css  — scope-detail page styles
10-cover.css       — cover monograph (editorial v1)
11-toc.css         — table of contents (editorial v2)
12-about.css       — about page (v2, v3 stats)
13-scope.css       — scope-overview utilities
14-process.css     — process page primitives
15-closing.css     — closing pages
16-about-magazine.css — about v5 (magazine spread)
17-archetypes.css  — archetype layout shells
18-projects.css    — project history
19-org.css         — org chart SVG styles
20-redesign.css    — .ed- page overrides
31-cover.css       — v3-cover archetype (from 30-redesign.css split)
32-toc.css         — v3-toc archetype
33-about.css       — v4-about archetype
34-capacity.css    — v4-capacity archetype
35-method.css      — v3-method QA/QC archetype
36-scope.css       — v3-scope, v4-scope, v4-atelier, v4-mosaic
37-catalog.css     — v4-catalog, v4-tier, v4-prequal
38-cmyk.css        — v4-cmyk print archetype
39-type.css        — v4-type wayfinding archetype
40-macro.css       — v4-macro GRC archetype
41-blueprint.css   — v4-blueprint engineering
42-gallery.css     — v4-replica-gallery, v4-landmark, v4-materiality
43-scan.css        — v4-scan-meth archetype
44-p25.css         — p25a-p25e materiality chapter
45-overrides.css   — print safety, back cover, page-specific fixes
50-replicas.css    — extracted from HTML inline <style>
```

**Order matters** — load in numeric sequence. The old `30-redesign.css` monolith (6,344 lines) was split into files 31-45.

## Pitfalls
- `write_file` COMPLETELY OVERWRITES — use `patch()` for targeted edits
- Write_file on multi-file CSS projects destroys the file. Only safe for creating new single files
- Surge CDN serves stale. Verify with `?t=$(date +%s)` cache-bust
- After `surge logout`, re-auth requires interactive `surge login`
- **Filename encoding**: Files with spaces (`Oddy Test_Lab.jpg`) referenced as URL-encoded (`Oddy%20Test_Lab.jpg`) fail to copy unless the deploy script uses `unquote()`. Always decode paths before checking existence: `from urllib.parse import unquote; sp = unquote(source_path)`
- **OneDrive sluggishness for new files**: When copying photos from Orders/ directories, `shutil.copy2` may fail silently on files just created by sips. Verify with `os.path.getsize()` after copy.
- **Subagent corruption of adjacent sections**: When delegating broad HTML redesigns, limit context to the specific section ID range. After the subagent returns, verify 2-3 adjacent sections are unchanged.
- **Google Fonts URL needs `wght@` not `wght;`** — the format `wght;500` silently fails, use `wght@500;600;700`
