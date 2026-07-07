# Samaya Factory Profile — surge.sh Workflow

**Domain:** `samaya-factory-profile.surge.sh`
**Local source:** `.../samaya-profile/v6/index.html` + `css/` + `assets/img/projects/`

## Core Rules (DO NOT BREAK)

1. **NEVER add new blocks/sections** — only replace existing photos and text in-place. The user will correct you immediately and decisively if you add a new gallery, tile, or section. Adding content where none existed is the #1 frustration.

2. **Delegate design to Claude Code CLI** — use `delegate_task()` with Claude for:
   - Layout/design changes (hero blocks, grids, galleries)
   - Text rewrites ("play with text")
   - Photo rearrangement and curation
   - Any change that modifies structure or visual layout

3. **Direct replacements only** — when replacing photos:
   - Copy the source photo to the correct `assets/img/projects/...` directory
   - Find the exact `background-image:url()` line in index.html
   - Use `patch()` to replace just the path

4. **Surge deploy** requires bumping the deploy dir each time:
   ```bash
   rm -rf /tmp/samaya-profile-deploy && mkdir -p /tmp/samaya-profile-deploy
   cp "$v6/index.html" /tmp/samaya-profile-deploy/index.html
   cp -R "$v6/css/" /tmp/samaya-profile-deploy/css/
   # Rewrite ../assets/ -> assets/ for surge
   sed 's|../assets/|assets/|g' ... 
   # Copy referenced assets
   python3 /tmp/copy_assets2.py
   surge --project /tmp/samaya-profile-deploy --domain samaya-factory-profile.surge.sh
   ```

## Photo Management

- **Source folder:** `OneDrive/.../00000 صور واتساب سنة 2025 الورشة/classified/website-ready/`
- **WhatsApp temp:** `~/Library/Containers/net.whatsapp.WhatsApp/Data/tmp/documents/`
- **Assets subfolders:** `assets/img/projects/` by section:
  - `material-samples/` — Materiality & Craft grid photos
  - `wayfinding/` — Wayfinding gallery
  - `replicas/` — Replica works gallery
  - `bim/` — Engineering/BIM pipeline
  - `madinah-royal-reception/` — Flagship project
  - `scope-replicas/process/` — 3D scanning methodology
- **OneDrive asset root:** `.../Samaya/Technical Office/samaya-profile/assets/img/projects/`
- **Every image must be used exactly once** — run Counter() check on all `../assets/img/` references in HTML after batch replacement

## CSS Workflow

- **NEVER use `write_file` on CSS files** — it **overwrites the entire file**. Always use `patch()` for targeted edits.
- Main CSS file: `css/30-redesign.css` (4276 lines)
- Section-specific: `css/18-projects.css`, `css/17-archetypes.css`
- Global tokens: `css/00-tokens.css`
- Page overflow fix pattern:
  - `.page { height: auto; min-height: 210mm; overflow: visible; }` in 00-tokens.css
  - Individual page `.content { height: calc(210mm - 22mm - 14mm); }` if needed
  - Back cover: `.ed-back-cover { height: 210mm; overflow: hidden; }`

## Text Style

- **Keep it concise** — "dont talk too much". Short bullet steps over lengthy paragraphs.
- Bilingual AR/EN — Arabic is primary, English secondary.
- Navy (#1E293B) headings, gold (#C9A24B) accents, cream (#F6F0E4) backgrounds.
- Fonts: Tajawal (AR), Inter (EN), Cormorant Garamond (serif).

## Page Layout Constraints

- A4 landscape: 297mm × 210mm
- Content area: `calc(210mm - 22mm - 14mm)` (header 22mm + footer 14mm)
- Each page needs `height: calc(210mm - 22mm - 14mm)` + `overflow: hidden` on `.content` to prevent spillover
- For multi-page sections (Materiality & Craft), remove `overflow: hidden` and let content flow naturally with `grid-auto-rows: auto`

## Known Surge Auth
- Email: mohamedsultanabbas@gmail.com
- Login via `surge login` in PTY terminal
- Password stored in ~/.netrc after successful login

## TOC Update After Page Changes

Whenever a section is added, removed, or renumbered, UPDATE THE TOC (section id="p2"). The TOC lists all sections with page numbers — stale entries cause navigational confusion.

Steps:
1. Read the current TOC entries (look for `.v3-toc-item` blocks)
2. List all actual section IDs (grep for `id="p"`) and their section-tag text
3. For any mismatch: update the TOC entry's page number, title, or both
4. For new pages (e.g. p13b), insert a new entry in correct order
5. For removed pages, delete the TOC entry
6. Verify entry count matches section count

## Flagship Hero Photo Flipping

Alternate the hero photo between left and right across adjacent flagship pages (p4-flag4 through p4-flag8). The `.proj-flagship .content` uses `grid-template-columns: 1.2fr 0.8fr` — in RTL, first DOM child = right column. To flip: swap the DOM order of `.pf-panel` (text) and `.pf-hero` (photo) in the HTML. Pattern: flag4 flipped, flag5 default, flag6 flipped, flag7 default, flag8 flipped.
