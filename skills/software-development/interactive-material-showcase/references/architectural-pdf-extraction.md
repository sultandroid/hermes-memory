# Extracting VIS / View Numbers from Architectural Plan PDFs

When working with NRS visualisation location plans (floor plans showing where each VIS photo was taken), standard text extraction has limitations because labels are scattered across a large technical drawing.

## Tools

| Tool | Package | Use Case |
|------|---------|----------|
| `pdftotext` | poppler | Quick text dump — good for title blocks, revision tables, legend boxes |
| `pdftotext -layout` | poppler | Positional text — preserves approximate layout, but very wide output for large A0 drawings |
| `pdftoppm` | poppler | Rasterise to PNG for visual inspection |
| `pdfimages` | poppler | Extract embedded images |

## Extraction Strategy

### 0. Primary Source: Folder Structure (Fastest, Most Reliable)

The NRS visualization folders are organized by floor **in their folder names**. Use these as the primary source for floor classification — do NOT try to re-derive the floor from PDF text extraction alone.

| Folder Name (actual) | Floor | VIS Range |
|----------------------|-------|-----------|
| `VIS - VISUALS (0_BASEMENT)` | Basement Floor (BF) | VIS001–VIS016 |
| `VIS - VISUALS (1_LOWER GROUND FLOOR)` | Lower Ground Floor (LGF) | VIS017–VIS020 |
| `VIS - VISUALS (2_Ground Floor)` | Ground Floor (GF) | VIS021–VIS025 |

When the user provides paths, **use the folder structure directly** as the authority for which VIS images belong to which floor. The user's folder paths are the primary source — supplement with PDF text extraction for gallery *names*, but the floor classification comes from the folders.

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

**⚠ A0 Limitation:** At A0 scale, `-layout` produces extremely wide lines (up to 2000+ chars each) with extensive whitespace padding. The text objects' positions are relative to the full sheet, not to logical gallery areas — gallery labels and VIS numbers that appear near each other visually may be far apart in the text stream. Don't rely on spatial proximity in the text dump for VIS-to-gallery mapping.

### 3. Rasterise to PNG (fallback for dense drawings)

```bash
pdftoppm -png -r 150 "plan.pdf" /tmp/plan
```

At 150 DPI the image is readable but manageable size (~2MB for an A0 drawing). The PDF labels are often too small to read below 150 DPI.

### 4. Use Vision Model on Cropped Sections

For floor plan images too large for vision APIs (e.g., 13750x9634 A0 drawing):
- Crop into quadrants or 3×2 grid sections first (`PIL.Image.crop`)
- Resize each section to ~1200px wide before sending
- Vision analysis works on each section independently

```python
from PIL import Image
img = Image.open('/tmp/plan.png')
w, h = img.size
# Crop into 3×2 sections
cols, rows = 3, 2
cw, ch = w // cols, h // rows
for r in range(rows):
    for c in range(cols):
        box = (c*cw, r*ch, (c+1)*cw, (r+1)*ch)
        crop = img.crop(box)
        # Resize
        crop.resize((crop.width // 4, crop.height // 4))
```

### 5. OneDrive Folder Name Restructure

OneDrive may rename folders with numeric prefixes. The user may reference old names (without numbers) but actual paths use the new names:

| User Reference (old) | Actual Path (new) |
|----------------------|-------------------|
| `VIS - VISUALS (BASEMENT)` | `VIS - VISUALS (0_BASEMENT)` |
| `VIS - VISUALS (LOWER GROUND FLOOR)` | `VIS - VISUALS (1_LOWER GROUND FLOOR)` |
| `VIS -Ground Floor` | `VIS - VISUALS (2_Ground Floor)` |

When the user provides a path that fails with "No such file or directory":
1. Use `find` with `-maxdepth` (avoiding OneDrive timeout) to locate the actual directory
2. The structure is correct but the folder name differs — find the actual path first
3. Once located, use the actual path directly for all subsequent operations

```bash
find "/OneDrive/.../Arch Visualization 3d Shots/" -maxdepth 1 -type d -name "*BASEMENT*" 2>/dev/null
find "/OneDrive/.../Arch Visualization 3d Shots/" -maxdepth 1 -type d -name "*LOWER GROUND*" 2>/dev/null
find "/OneDrive/.../Arch Visualization 3d Shots/" -maxdepth 1 -type d -name "*Ground Floor*" 2>/dev/null
```

## Complete Floor-to-Gallery Mapping (verified from NRS plans + folder structure)

### Basement Floor (BF) — VIS001–VIS016

| Gallery | Name | VIS Images (existing) |
|---------|------|-----------------------|
| G4 | Saudi Art (Landscape & Architecture) | g4_G4_View_1.jpg, g4_G4_View_2.jpg |
| G5 | Making Space | g5_G5_View_11B.jpg |
| G6 | Saudi Art (Abstract, People & Traditional Practice) | g6_G6_View_3.jpg, g6_G6_View_3B.jpg, g6_G6_View_4.jpg |
| G7 | Contemporary Art Commission: Reem Alnasser | bf_VIS13.jpg (from VIS013) |
| G8 | Al Qatt | g8_G8_View_5.jpg, g8_G8_View_6.jpg |
| G9 | Flowersmen & Photography | g9_G9_View_7.jpg |
| G10 | Contemporary Art Commission: Faisal Samra | bf_VIS14.jpg (from VIS014) |
| G11 | Script | g11_G11_View_8.jpg, g11_G11_View_8B.jpg |
| G12 | Archaeology | g12_G12_View_9.jpg, g12_G12_View_10.jpg, g12_G12_View_10B.jpg |
| G13 | Contemporary Art Commission: Tarek Atoui | bf_VIS15.jpg (from VIS015) |
| LB3 | Lobby Basement Level | lb3_LB3_View_11.jpg, lb3_LB3_View_12.jpg |

**11 galleries with 20 view images on BF.** 16 original NRS VIS images.

### Lower Ground Floor (LGF) — VIS017–VIS020

The LGF location plan PDF (`MOC-ASE-AR-ARC-LGF-DDD-1211-00.pdf` or similar) was not found as a visualization location plan — only 4 JPG renders + a wall types PDF exist. Gallery names from space schedule verified against LGF wall types PDF:

| Gallery | Name | VIS Images |
|---------|------|------------|
| G1 | Welcome Gallery | lgf_VIS17.jpg, lgf_VIS18.jpg |
| G2 | Contemporary Art Commission: Ayman Zedani | lgf_VIS19.jpg |
| G3 | Al Muftaha | lgf_VIS20.jpg |
| G14 | Event Space & Contemporary Art Commission: Hamra Abbas | (shared) |
| LB2 | Lobby King Khaled Entrance | (shared) |
| TG | Temporary Gallery | (shared) |

**6 spaces with 4 VIS images on LGF.** Some galleries share images.

### Ground Floor (GF) — VIS021–VIS025

| Gallery | Name | VIS Images |
|---------|------|------------|
| LB1 | Al Bahar Main Entrance (Lobby) | gf_VIS21.jpg |
| EC | Children's Education Centre | gf_VIS22.jpg |
| RT | Retail / Gift Shop | gf_VIS23.jpg |
| VI | VIP Reception | gf_VIS24.jpg |
| EX1-2 | Exterior Landscape | gf_VIS25.jpg |

**5 spaces with 5 VIS images on GF.**

## Gallery Title Corrections (from NRS plans vs old app)

| Gallery | Old Title (app) | Corrected Title (NRS plan) |
|---------|-----------------|---------------------------|
| G5 | G5 – Children's Room | G5 – Making Space |
| G9 | G9 – Flowersmen | G9 – Flowersmen & Photography |
| G11 | G11 – Scripts | G11 – Script |
| LB3 | LB3 – Link Bridge | LB3 – Lobby Basement Level |

## Limitations

- pdftotext may miss labels inside callout bubbles, annotation blocks, or curved text
- Labels placed at an angle or inside complex shapes may not be extractable
- Some VIS numbers appear only as visual annotations (drawn objects) and never enter the text stream
- Floor plans at A0 scale have text that's physically small (~6-8pt) — OCR would need high resolution
- The PDF is primarily a vector drawing — pdftotext extracts text objects but their positions are relative to the full sheet, not to logical areas

## When Text Extraction Fails

If you can't extract VIS-to-gallery mappings from the PDF:

1. **Ask the user directly** — they have the drawing open and can read the labels. The user also has the folders organized by floor.
2. **Use the folder structure** — the NRS VIS folders are organized by floor (0_BASEMENT, 1_LOWER GROUND FLOOR, 2_Ground Floor). The floor suffix number is the primary classifier.
3. **Use the admin panel** — create placeholder entries with `hotspots:[]`, let the user add pins later at `?admin=1`
4. **Cross-reference with the space/gallery schedule** — JSON files in `src/data/schedules/space_gallery_schedule*.json` contain exhibition zone descriptions that may hint at which spaces are on which floor
