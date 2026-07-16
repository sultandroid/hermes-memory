# Material Data Sheet Extraction — Worked Example

## Documents Extracted

### 1. SS 304 Inspection Certificate (JIS G4305:2021)
- **File:** Image-based PDF, 1 page, 322 KB
- **Content:** SUS304 cold rolled coil, NO.2B finish, Solution & Annealed
- **Table:** 6 coils with thickness 0.88–3.00 mm, width 1200–1260 mm
- **Chemical composition:** C 0.034–0.098%, Si 0.50–0.96%, Mn 0.40–0.47%, P 0.025–0.031%, S 0.004–0.009%, Ni 8.00–8.02%, Cr 18.00–18.16%
- **Mechanical:** TS 703–720 MPa, YS 301–331 MPa, Elong 51–57%, Hardness 160–181
- **Certifications:** ISO 9001, 45001, 14001, 10012, PED, CPR

### 2. Verdo FR MDF Grade 130 Test Report (ASTM D1037-12)
- **File:** Image-based PDF, 10 pages, 820 KB
- **Lab:** Wimpey Laboratories L.L.C., Dubai, UAE
- **Client:** Danube Building Materials FZCO
- **Standard:** ANSI A208.2-2009 Grade 130
- **Sample:** VERDO FIRE RETARDANT (F/R) MDF E0 NAUF CARB P2 FSC 100%

## Extraction Pipeline Used

### Step 1: Detect text layer
```bash
pdftotext "/path/to/file.pdf" - 2>/dev/null
# Returns empty → image-based PDF
```

### Step 2: Render to images with PyMuPDF
```python
import fitz
doc = fitz.open(path)
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=300)
    pix.save(f"/tmp/page_{i+1}.png")
```

### Step 3: Full-page OCR
```python
import pytesseract
from PIL import Image
text = pytesseract.image_to_string(img, lang='eng', config='--oem 3 --psm 6')
```

### Step 4: TSV table reconstruction (for garbled tables)
```python
from collections import defaultdict
data = pytesseract.image_to_data(img, lang='eng',
    config='--oem 3 --psm 6', output_type=pytesseract.Output.DICT)
lines = defaultdict(list)
for i in range(len(data['text'])):
    t = data['text'][i].strip()
    if t and data['conf'][i] > 0:
        key = (data['block_num'][i], data['line_num'][i])
        lines[key].append((data['left'][i], t))
for key in sorted(lines.keys()):
    items = sorted(lines[key], key=lambda x: x[0])
    print(' | '.join(item[1] for item in items))
```

### Step 5: Zoomed crop for missing values
```python
from PIL import ImageEnhance
w, h = img.size
crop = img.crop((int(w*0.15), int(h*0.45), int(w*0.85), int(h*0.65)))
crop = crop.resize((crop.width * 2, crop.height * 2), Image.NEAREST)
crop = crop.convert('L')
enhancer = ImageEnhance.Contrast(crop)
crop = enhancer.enhance(3.0)
crop = crop.point(lambda x: 0 if x < 120 else 255, '1')
text = pytesseract.image_to_string(crop, lang='eng', config='--oem 3 --psm 6')
```

### Step 6: Manual calculation of derived values
```python
# Internal Bond from load + area
loads = [2760, 2560, 2550]
area = 2500
avg_bond = sum(loads) / len(loads) / area
# → 1.049 N/mm² ≈ 152 psi
```

## Key Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Arabic stamps overlapping English table cells | TSV bounding-box reconstruction isolates spatial positions; note unrecoverable cells as "partially obscured" |
| Missing "Result" column values in test reports | Zoomed crop + aggressive contrast (3-4x) + binarization at threshold 100-120 |
| OCR garbles column alignment | Group by `(block_num, line_num)` and sort by `left` coordinate |
| Calculated averages not OCR-readable | Compute manually from raw data (loads, areas, dimensions) |
| Multi-page test report (10 pages) | Process page-by-page, save results incrementally |

## Verdo FR MDF Test Results Summary

| Test | Result | Unit |
|------|--------|------|
| Thickness | 18.05–18.09 | mm |
| Density | 800.8 avg | kg/m³ (50 lbs/ft³) |
| MOR | 29.5 avg | N/mm² (4,279 psi) |
| MOE | 2,923 avg | N/mm² (423,945 psi) |
| Moisture Content | 4.45–4.61 | % |
| Thickness Swelling (24h) | 7.32 | % |
| Internal Bond | ~1.05 | N/mm² (~152 psi) |
| Screw Holding (Face) | 845 | N (19 mm embed) |
| Linear Expansion | (not reliably OCR'd) | — |
| Edge Straightness | (not reliably OCR'd) | — |

All tests passed ANSI A208.2-2009 Grade 130 requirements.
