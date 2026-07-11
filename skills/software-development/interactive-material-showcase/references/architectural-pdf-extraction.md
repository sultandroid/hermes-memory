# Extracting VIS / View Numbers from Architectural Plan PDFs

When working with NRS visualisation location plans (floor plans showing where each VIS photo was taken), standard text extraction has limitations because labels are scattered across a large technical drawing.

## Tools

| Tool | Package | Use Case |
|------|---------|----------|
| `pdftotext` | poppler | Quick text dump — good for title blocks, revision tables, legend boxes |
| `pdftotext -layout` | poppler | Positional text — preserves approximate layout, but very wide output for large drawings |
| `pdftoppm` | poppler | Rasterise to PNG for visual inspection |
| `pdfimages` | poppler | Extract embedded images |

## Extraction Strategy

### 1. Try pdftotext first (fast)

```bash
pdftotext "MOC-ASE-AR-ARC-BF-DDD-1210-00.pdf" /tmp/output.txt
grep -o 'VIS[0-9][0-9][0-9]\\|MOC-ASE-AR-ARC-BF-DDD-VIS[0-9][0-9][0-9]' /tmp/output.txt | sort -u
```

**Limitation:** Only captures labels that pdftotext can reconstruct from the PDF's text stream. Labels placed inside annotation blocks, callout bubbles, or tightly packed areas may be missed.

### 2. Try pdftotext -layout for positional context

```bash
pdftotext -layout "plan.pdf" /tmp/layout.txt
# Then look near expected gallery areas:
grep -B 10 -A 3 "VIS013" /tmp/layout.txt
```

Useful when you need context around a VIS number (nearby gallery labels like G4, G8, etc.).

### 3. Rasterise to PNG (fallback for dense drawings)

```bash
pdftoppm -png -r 150 "plan.pdf" /tmp/plan
# Upload to server for browser viewing, or use vision analysis
```

At 150 DPI the image is readable but manageable size (~2MB for an A0 drawing). The PDF labels are often too small to read below 150 DPI.

### 4. Upload to browser for visual inspection

```bash
# Upload to server
ssh -p <port> user@host "cat > /remote/path/tmp_plan.png" < /tmp/plan-1.png
# Then navigate browser to https://domain.com/path/tmp_plan.png
```

## Known Patterns for VIS Number Locations

On the Basement Floor plan (MOC-ASE-AR-ARC-BF-DDD-1210-00):

| Area | Gallery | VIS Numbers Found |
|------|---------|-------------------|
| G4 – Saudi Art | Saudi Art (Landscape & Architecture) | VIS001, VIS002, VIS005 |
| G6 – Saudi Art | Saudi Art (People, Abstract, etc.) | VIS003, VIS004 |
| G8 – Al Qatt | Al Qatt Al-Aseeri | VIS006, VIS007 |
| G9 – Flowersmen | Flowersmen | VIS008 |
| G11 – Scripts | Scripts & Calligraphy | VIS009, VIS010 |
| G12 – Archaeology | Archaeology | VIS011, VIS013 |
| LB3 – Link Bridge | Link Bridge | VIS015? |
| G5 – Children's Room | Making Space / Children's Education | varies |

On the Lower Ground Floor plan (MOC-ASE-AR-ARC-LGF-DDD-1211-00):

| Area | Gallery | VIS Numbers |
|------|---------|-------------|
| G1 – Welcome Gallery | Welcome Gallery | VIS017 |
| G3 – Al Muftaha | Al Muftaha | VIS018 |
| LB2 – Lobby | Main Lobby | VIS019 |
| TG – Temporary Gallery | Temporary Gallery | VIS020 |

On the Ground Floor plan (MOC-ASE-AR-ARC-GF-DDD-1212-00):

| Area | Gallery | VIS Numbers |
|------|---------|-------------|
| LB1 – Main Lobby | Lobby & Welcome Desk | VIS021, VIS023 |
| V1 – VIP Reception | VIP Reception | VIS022 |
| EC – Children's Educational Centre | Educational Centre | VIS024 |
| RT – Gift Shop & Retail | Gift Shop / Retail | VIS025 |

## Limitations

- pdftotext may miss labels inside callout bubbles, annotation blocks, or curved text
- Labels placed at an angle or inside complex shapes may not be extractable
- Some VIS numbers appear only as visual annotations (drawn objects) and never enter the text stream
- Floor plans at A0 scale have text that's physically small (~6-8pt) — OCR would need high resolution
- The PDF is primarily a vector drawing — pdftotext extracts text objects but their positions are relative to the full sheet, not to logical areas

## When Text Extraction Fails

If you can't extract VIS-to-gallery mappings from the PDF:

1. **Ask the user directly** — they have the drawing open and can read the labels
2. **Use the admin panel** — create placeholder entries with `hotspots:[]`, let the user add pins later at `?admin=1`
3. **Cross-reference with the space/gallery schedule** — JSON files in `src/data/schedules/space_gallery_schedule*.json` contain exhibition zone descriptions that may hint at which spaces are on which floor
