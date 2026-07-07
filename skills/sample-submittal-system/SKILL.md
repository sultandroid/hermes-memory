---
name: sample-submittal-system
description: "Design system for physical material sample submittal pages — A4 print-ready HTML, approval workflow, logo header"
version: 2.0.0
author: Samaya Technical Office
---

# Sample Submittal System

Creates A4-print-ready material sample submittal pages for Aseer Museum. Each sample gets its own folder under `public_html/build/Samples/{CODE}/` with index.html, photo, QR, and logos.

## File Structure

Each sample gets TWO page types deployed to the same URL:

```
build/Samples/{CODE}/
├── index.html                    ← Kimi-style folder cover (primary landing page)
├── submittal.html                ← A4 formal submittal sheet
├── photo-{CODE}.jpg              ← sample specimen photo
├── qr-{CODE}.png                 ← QR code for the page URL
├── datasheet-*.pdf               ← (optional) material datasheets
└── assets/
    ├── moc-logo.png
    ├── pmc-logo-trans.png
    ├── cg-logo-trans.png
    ├── nrs-logo-trans.png
    └── samaya-logo-trans.png
```

Local OneDrive copy keeps `label.html` (the Kimi cover source) and `submittal.html` (the A4 sheet) in the sample's working folder under `03.3_Material_Submittals/{CODE-PREFIX}/`.

**IMPORTANT — confirm landing page with user before deploying.** Early samples (PB-001, SS-001) used the A4 submittal as `index.html` with the Kimi cover as `cover.html`. Later convention (from SS-002) uses the Kimi cover as `index.html` with the A4 sheet as `submittal.html`. The user will flag a mismatch — ask first.

## Template A: Kimi-Style Folder Cover (Front + Back)

The primary landing page for each sample. Dark navy (`#13151A`) double-sided cover with Playfair Display title, specs panel, QR, and party logos.

### Variant 1: A4 Portrait (210×297mm) — Two Separate Pages

Two separate A4 pages: front cover on page 1, back cover on page 2. Print double-sided. Used for PB-001 and early samples.

### Variant 2: A3 Booklet Spread (420×297mm) — Single Page (PREFERRED)

A single A3 landscape page with front cover on the **left half** and back cover on the **right half**. Print on A3, fold in half to create a booklet cover. This is the **preferred variant** for new samples (confirmed on SS-002).

**IMPORTANT — orientation:** Front cover goes on the **left** half, back cover on the **right** half. The user corrected this from the initial right→left layout. When folded, the front cover faces up on the right side of the booklet.

Key CSS differences from A4 variant:
- `.spread` container: `width:420mm; height:297mm; display:flex;`
- `.half` children: `width:50%; height:100%;`
- `.front` has `border-right:1px solid rgba(255,255,255,.06)` to mark the fold line (left half)
- All font sizes and spacing are slightly smaller (the spread is wider but each half is A4-sized)
- Decorative rings: 180px and 130px (smaller than A4 variant's 220/160px)
- `@page{size:420mm 297mm landscape; margin:0;}`

### Variant 3: A3 Booklet Spread with Photo Background

Same as Variant 2 but the front cover (left half) has the sample photo as a subtle background image:

```css
.front-photo-bg{
  position:absolute; top:0; left:0; width:100%; height:100%;
  object-fit:cover; object-position:center;
  opacity:.2; pointer-events:none;
}
```

The specs panel gets a darker overlay for text readability:
```css
.specs-panel{
  background:rgba(0,0,0,.75); border:1px solid rgba(255,255,255,.12);
}
```

All party logos on the dark cover need `filter:brightness(0) invert(1)` to render white — without this, dark-colored logos are invisible on the dark background.

**Print readability** — Add `@media print` overrides to darken panels further (print rendering can wash out semi-transparent overlays):
```css
@media print{
  .front-photo-bg{opacity:.15 !important;}
  .specs-panel{background:rgba(0,0,0,.85) !important;}
  .party-strip{background:rgba(0,0,0,.6) !important;}
}
```

### Sample Name Format

The user corrected the name format on SS-002. Use this pattern:

```
METAL SS PVD Coated Patinated Brass Effect
```

- **Material type prefix** in ALL CAPS: `METAL SS`, `BRASS`, `STAINLESS STEEL`, etc.
- **Process/coating** in Title Case: `PVD Coated`
- **Effect/colour match** in Title Case: `Patinated Brass Effect`
- Line breaks in the Playfair Display title should break at natural phrase boundaries (e.g. `METAL SS PVD<br>Coated Patinated<br>Brass Effect`)

### Front Cover Layout
- **Background**: `#13151A` with subtle radial gradient decoration (`radial-gradient(ellipse at center, rgba(200,144,74,.08) 0%, transparent 70%)`)
- **Top bar**: Samaya logo (left, 18px, 0.7 opacity) — "Material Code" label (7px, uppercase, 0.35 opacity) + code in bronze monospace (right)
- **Hero**: Material name in Playfair Display 52px, subtitle with type badge (bronze border, 9px uppercase), divider dot, finish description
- **Specs panel**: Semi-transparent panel (`rgba(255,255,255,.04)` bg, `rgba(255,255,255,.06)` border, 4px radius) with Substrate, Finish, Hardness, Corrosion, Applications (tag grid), Status indicator (green dot + "Active")
- **Ref area**: "Submittal Reference" label + doc ref with bronze-highlighted section
- **QR float**: 50px QR code in bottom-right corner
- **Party strip**: CG, NRS, PMC, Glasbau Hahn logos (14px height, 0.5 opacity) + names in a row at bottom

### Back Cover Layout
- **Background**: Same `#13151A` with decorative concentric rings (280px and 200px, 0.04/0.03 opacity) and horizontal line
- **Top**: Samaya logo centered (20px, 0.4 opacity)
- **Center**: QR code (60px) in circular frame (90px, `rgba(255,255,255,.1)` border, `rgba(255,255,255,.02)` bg)
- **Brand**: "Samaya Technical Office" (10px, uppercase, 0.4 opacity) + "Aseer Museum · KSA" (8px, 0.2 opacity)
- **Ref block**: Code (14px, bronze), submittal ref (8px, 0.25 opacity), accent line (30px, `rgba(200,144,74,.3)`), "Material Sample" label (7px, uppercase, 0.2 opacity)
- **Bottom**: Party logos only (no names, 14px, 0.3 opacity)

### Key CSS
- Fonts: `Playfair Display` for title, `Inter` for everything else
- Accent color: `#C8904A` (bronze/gold)
- Cover dimensions: `210mm × 297mm` (A4 portrait) — NOT 240×330mm. The user corrected this from booklet size to A4.
- Print: `@page{size:A4 portrait; margin:0;}`
- `-webkit-print-color-adjust:exact` preserves dark background
- Decorative rings: 220px and 160px (scaled for A4, not the original 280/200px from the Kimi prototype)

### Creating a Kimi Cover
Build from scratch using the structure above, or adapt an existing live cover:
```bash
curl -sL "https://samaya-factory.com/build/Samples/SAM-FIN-SS-002/" > /tmp/reference-cover.html
```
Variables to replace: title, code, finish description, specs, applications, submittal ref, QR filename, photo filename.

---

## Template B: A4 Submittal Sheet

Kept as a local copy in the OneDrive working folder. Print-friendly A4 page with approval workflow.

### Top Bar — 5 Project Logos
White-on-navy bar. Left: MoC, PMC, CG, NRS, Samaya logos (16px, `filter:brightness(0) invert(1)` for white rendering). Thin vertical dividers between logos. Right: "Material Submittal · Aseer Museum" in bronze small caps.

### Title Block
- Sample name (24px bold), code (monospace bronze), category tags (Material Type · Finish Type · Status)
- Meta line: DMP ref, Museum, Project #, Client, Review entities

### Main Body — Two Columns
- **Left (42%)**: Sample photo — `max-height:135mm; object-fit:cover` (crops to fit A4)
- **Right (58%)**: Three info blocks with bronze h2 + separator line:
  1. Material — paragraph
  2. Specifications — key-value rows (Substrate, Finish, Coating, Gauges)
  3. Applications — 2-column bullet list

### Bottom Strip — Three Cells
1. **QR code** — 20mm×20mm
2. **Technical Datasheets** — inline links with PDF badge
3. **Approval table** — 5 rows (Prepared: Glasbau Hahn, Reviewed: NRS/CG/PMC, Approved: Client — MoC). Each has 18px signature line + 30mm date column with its own signature line + "Date" label.

### Footer
`Samaya Technical Office · Submittal {DOC-REF} · Aseer Museum`

## Creating a New Sample (Full Workflow)

### 1. Photo Preparation
Convert HEIC (iPhone) to JPG for web:
```bash
sips -s format jpeg IMG_XXXX.heic --out photo-{CODE}.jpg --resampleWidth 1600
```

### 2. Generate QR Code
```bash
qrencode -o qr-{CODE}.png -s 12 -m 2 "https://samaya-factory.com/Samples/{CODE}"
```

### 3. Create index.html
Clone an existing live sample page as a reference, then swap all variables:
```bash
curl -sL "https://samaya-factory.com/build/Samples/SAM-FIN-PB-001/" > /tmp/reference.html
```

Variables to replace:
- Title, h1, code, category tags (Material Type · Finish Type · Status)
- Material description paragraph
- Specifications (substrate, finish, coating, gauges)
- Applications list (7 items)
- Datasheet names and filenames
- Prepared-by entity (varies per sample — e.g. Glasbau Hahn, Samaya Technical Office)
- Submittal ref in footer

### 4. Deploy to Server

Server: `samaya-factory.com` (port 65002)
Path: `domains/samaya-factory.com/public_html/build/Samples/{CODE}/`
User: `u517606786`

#### Steps

1. **Create folder on server:**
   ```bash
   ssh -p 65002 u517606786@samaya-factory.com 'mkdir -p domains/samaya-factory.com/public_html/build/Samples/{CODE}/assets'
   ```

2. **Download logos from existing live sample** (fastest — avoids OneDrive slowness):
   ```bash
   curl -sL "https://samaya-factory.com/build/Samples/SAM-FIN-PB-001/assets/moc-logo.png" -o assets/moc-logo.png
   curl -sL "https://samaya-factory.com/build/Samples/SAM-FIN-PB-001/assets/pmc-logo-trans.png" -o assets/pmc-logo-trans.png
   curl -sL "https://samaya-factory.com/build/Samples/SAM-FIN-PB-001/assets/cg-logo-trans.png" -o assets/cg-logo-trans.png
   curl -sL "https://samaya-factory.com/build/Samples/SAM-FIN-PB-001/assets/nrs-logo-trans.png" -o assets/nrs-logo-trans.png
   curl -sL "https://samaya-factory.com/build/Samples/SAM-FIN-PB-001/assets/samaya-logo-trans.png" -o assets/samaya-logo-trans.png
   ```
   (Alternative source: `{OneDrive}/Samaya/Technical Office/Bim Unit/Aseer-Museum/04_Docs/02_Plans_and_Procedures/02.15_Method_Statements/01_Source_Files/01_HTML/assets/`)

3. **Package and upload via SSH pipe** (more reliable than SCP — SCP can hang on Hostinger port 65002):
   ```bash
   tar czf /tmp/deploy.tar.gz -C /tmp/deploy-dir/ .
   cat /tmp/deploy.tar.gz | ssh -p 65002 u517606786@samaya-factory.com "cat > /home/u517606786/deploy.tar.gz"
   ssh -p 65002 u517606786@samaya-factory.com "cd domains/samaya-factory.com/public_html/build/Samples/{CODE} && tar xzf /home/u517606786/deploy.tar.gz && rm /home/u517606786/deploy.tar.gz && echo 'Deploy OK'"
   ```

4. **Fix permissions** — CRITICAL: SSH pipe uploads create files with `-rw-------` (600), causing 403 Forbidden:
   ```bash
   ssh -p 65002 u517606786@samaya-factory.com "chmod 755 domains/samaya-factory.com/public_html/build/Samples/{CODE} && chmod 755 domains/samaya-factory.com/public_html/build/Samples/{CODE}/assets && chmod 644 domains/samaya-factory.com/public_html/build/Samples/{CODE}/* domains/samaya-factory.com/public_html/build/Samples/{CODE}/assets/* && echo 'Permissions fixed'"
   ```

5. **Verify:** open `https://samaya-factory.com/build/Samples/{CODE}/` and check all elements load (photo, QR, logos, datasheet links). Use <kbd>Cmd+P</kbd> to check A4 print fit.

### Pitfalls
- **403 Forbidden after deploy** = permissions issue. Files uploaded via SSH pipe get mode 600. Always run chmod 644 on files + 755 on directories after deploy.
- **Logo download from live server** is faster than OneDrive for asset retrieval. Use curl from an existing live sample.
- **Prepared-by entity** varies per sample — not always Glasbau Hahn. Set to the actual supplier/submitter (e.g. "Samaya Technical Office" for in-house samples).
- **Datasheet PDFs** are optional placeholders. The page works without them — links just won't resolve until PDFs are uploaded.
- **Landing page template mismatch** — The skill specifies the Kimi-style folder cover as `index.html`, but early samples (PB-001, SS-001) were deployed with the A4 submittal sheet as `index.html` instead. Before deploying a new sample, CONFIRM with the user which template should be the landing page. If the A4 sheet is the landing page, the Kimi cover goes in a separate `label.html` file (local copy only). If the Kimi cover is the landing page, the A4 sheet goes in `submittal.html`. Do not assume — the user will flag a mismatch.
- **Apple Double files (._*)** — macOS creates hidden `._filename` resource fork files when copying to non-Apple filesystems. These appear on the server as `._index.html`, `._photo-*.jpg`, etc. They are harmless but clutter the directory. Remove them after deploy: `ssh ... "find ... -name '._*' -delete"`.
- **Cover size correction** — The Kimi prototype uses 240×330mm (booklet). The user wants A4 (210×297mm). Always set cover dimensions to A4 portrait unless explicitly told otherwise. Also scale decorative elements (rings, font sizes) proportionally when resizing.
- **Booklet spread orientation** — When using the A3 booklet spread variant (420×297mm), front cover goes on the **left** half, back cover on the **right** half. The user will correct a right→left flip.
- **Finish description for PVD-coated SS matching patinated brass** — When the finish is a colour match to another material, phrase it as: "PVD Coating — Brushed colour finish to match Patinated Brass". Do NOT list generic options like "Satin / Brushed / Mirror" — the user will correct this.
- **Sample name format** — Material type prefix in ALL CAPS (e.g. `METAL SS`), process in Title Case (`PVD Coated`), effect in Title Case (`Patinated Brass Effect`). The user corrected this on SS-002.
- **Photo as cover background** — On the booklet spread cover, add the sample photo as a subtle background image (`opacity:.2`, `object-fit:cover`) on the front half. Use a semi-transparent dark overlay (`rgba(0,0,0,.75)`) on the specs panel for text readability.
- **Logo rendering on dark backgrounds** — All party logos on the dark navy cover need `filter: brightness(0) invert(1)` to render white. Without this, dark-colored logos are invisible on the dark background.
- **Print readability** — For dark-background covers, ensure sufficient contrast: specs panel bg at least 75% black, spec values at 0.9 opacity, spec keys at 0.5 opacity, title weight 700. Add `@media print` overrides to darken panels further for print (print rendering can wash out semi-transparent overlays).
- **Project name on cover** — Add "Aseer Regional Museum · KSA" below the subtitle on the front cover (8px, uppercase, 0.3 opacity, letter-spacing 1.5px).

## Template Variables

| Variable | Example | Description |
|----------|---------|-------------|
| {SAMPLE-NAME} | Patinated Brass | Full material name |
| {CODE} | SAM-FIN-PB-001 | Sample code |
| {MATERIAL-TYPE} | Metal Finish | Category 1 |
| {FINISH-TYPE} | Chemical Patination | Category 2 |
| {STATUS} | Approval in Progress | Status |
| {DMP-REF} | MOC-MUS-ASE-1K0-PL-0029 Rev.C04 | Project doc ref |
| {MATERIAL-DESC} | CuZn37 brass with chemical patina finish... | 1-2 sentences |
| {SUBSTRATE} | CuZn37 (C27200 CW508L) · 2.0mm | Substrate spec |
| {FINISH-DESC} | Chemical Patination — EDEN-CD/CC | Finish spec |
| {COATING-DESC} | Clear coat sealed · Touch-up kit | Coating |
| {GAUGES} | 0.8mm (light-duty), 1.2mm, 2.0mm | Available thicknesses |
| {APPLICATIONS} | cladding, hardware, handrails... | 7 use cases |
| {DATASHEET-1-NAME} | KME CuZn37 Brass Datasheet | First datasheet |
| {DATASHEET-2-NAME} | Eden Patination Process Datasheet | Second datasheet |
| {DATASHEET-1-FILE} | datasheet-kme.pdf | First datasheet file |
| {DATASHEET-2-FILE} | datasheet-patination.pdf | Second datasheet file |
| {PREPARED-BY} | Glasbau Hahn | Sample supplier |
| {SUBMITTAL-REF} | MOC-MUS-ASE-1A0-MA-0007 | Submittal doc number |

---

## Template B: A4 Submittal Sheet

Kept as a local copy in the OneDrive working folder. Print-friendly A4 page with approval workflow.

### Top Bar — 5 Project Logos
White-on-navy bar. Left: MoC, PMC, CG, NRS, Samaya logos (16px, `filter:brightness(0) invert(1)` for white rendering). Thin vertical dividers between logos. Right: "Material Submittal · Aseer Museum" in bronze small caps.

### Title Block
- Sample name (24px bold), code (monospace bronze), category tags (Material Type · Finish Type · Status)
- Meta line: DMP ref, Museum, Project #, Client, Review entities

### Main Body — Two Columns
- **Left (42%)**: Sample photo — `max-height:135mm; object-fit:cover` (crops to fit A4)
- **Right (58%)**: Three info blocks with bronze h2 + separator line:
  1. Material — paragraph
  2. Specifications — key-value rows (Substrate, Finish, Coating, Gauges)
  3. Applications — 2-column bullet list

### Bottom Strip — Three Cells
1. **QR code** — 20mm×20mm
2. **Technical Datasheets** — inline links with PDF badge
3. **Approval table** — 5 rows (Prepared: varies, Reviewed: NRS/CG/PMC, Approved: Client — MoC). Each has 18px signature line + 30mm date column with its own signature line + "Date" label.

### Footer
`Samaya Technical Office · Submittal {DOC-REF} · Aseer Museum`

### Print Behavior
- `@page { size:A4 portrait; margin:0; }` — exact dimensions
- `@media print` strips gray mockup background and shadow
- `-webkit-print-color-adjust:exact` preserves navy bar and bronze accents
- Photo crops via `object-fit:cover` to 135mm height
- Status "Approval in Progress" during review cycle

### Approval Workflow
| Row | Role | Entity | Action |
|-----|------|--------|--------|
| 1 | Prepared by | Supplier/ manufacturer | Submit sample |
| 2 | Reviewed by | NRS | Design review |
| 3 | Reviewed by | CG | Consultant review |
| 4 | Reviewed by | PMC | Project management review |
| 5 | Approved by | Client — MoC | Final approval |

Each row has an 18px signature line (stamp-capable) and a 30mm date column with its own signature line + "Date" label.
