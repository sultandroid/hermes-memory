# Excel Data Prep for Odoo Imports — Raw Materials Standardization

## Session Context

Standardized Product_raw_materials_final.xlsx (1,377 items) for Odoo import. Original had 79 category prefixes like "Paint Primer", "Steel SHS", "3D Printing", "Acrylic Paint", etc. Collapsed into 11 high-level codes.

## Final Category Map

| Code | Category | Count | Includes |
|------|----------|-------|----------|
| WDM | Wood Materials | 136 | Solid wood, MDF, MFC, plywood, veneer, particle board, WPVC, edge banding |
| MTL | Metal Materials | 432 | All steel shapes, aluminum, copper, sheet metal, perforated sheet, alucobond |
| PNT | Painting Materials | 108 | All paint types, primers, thinners, putty, stains, acrylic paint |
| PKG | Packing Materials | 11 | Packaging material |
| PRT | Printing/Fabrication | 299 | 3D printing, resin, acrylic/forex/plastic sheet, silicone rubber, lexan |
| HDW | Hardware/Infrastructure | 240 | Electrical, plumbing, insulation, adhesive, chemicals, bitumen |
| ACC | Accessories/Fasteners | 98 | Fasteners, tapes, hinges, gift/stationery material |
| TLE | Tiles & Flooring | 19 | Tiles, flooring |
| FBR | Fabric & Textiles | 26 | Fabric, carpet, leather, foam |
| TLS | Tools & Sundry | 5 | Signage material, wax |
| GEN | General | 3 | General, artificial grass, solid surface |

## User Preference — High-Level Buckets

DO NOT propose granular codes like PNT=paint, ACR=acrylic, ALM=aluminum, etc. The user explicitly rejected that. They want broad buckets: wood materials, metal materials, painting materials, packing materials, accessories, hardware, tools.

When presenting category proposals, use the table format above with "Includes" column showing what's inside each bucket. Counts help the user assess the distribution.

## Full Prefix Map (used successfully)

```python
PREFIX_MAP = {
    'solid wood': 'WDM', 'wood veneer': 'WDM', 'mdf': 'WDM', 'mfc': 'WDM',
    'plywood': 'WDM', 'particle board': 'WDM', 'wpvc': 'WDM', 'edge banding': 'WDM',
    'steel': 'MTL', 'steel shs': 'MTL', 'steel pipe': 'MTL', 'steel angle': 'MTL',
    'steel rhs': 'MTL', 'steel channel': 'MTL', 'steel bar': 'MTL',
    'steel round bar': 'MTL', 'steel rod': 'MTL', 'steel flange': 'MTL',
    'steel t bar': 'MTL', 'steel beam': 'MTL', 'square steel tube': 'MTL',
    'aluminum': 'MTL', 'aluminum profile': 'MTL', 'alucobond sheet': 'MTL',
    'copper': 'MTL', 'sheet metal': 'MTL', 'perforated sheet': 'MTL',
    'paint': 'PNT', 'paint polyurethane': 'PNT', 'paint primer': 'PNT',
    'paint putty': 'PNT', 'paint water base': 'PNT', 'paint oil': 'PNT',
    'paint thinner': 'PNT', 'paint topcoat': 'PNT', 'paint enamel': 'PNT',
    'paint epoxy': 'PNT', 'paint stain': 'PNT', 'water-based paint': 'PNT',
    'acrylic paint': 'PNT',
    'packaging material': 'PKG', 'packaging materials': 'PKG',
    'printing material': 'PRT', 'printing materials': 'PRT', '3d printing': 'PRT',
    'resin fiber': 'PRT', 'acrylic sheet': 'PRT', 'forex sheet': 'PRT',
    'plastic sheet': 'PRT', 'lexan sheet': 'PRT', 'silicone rubber': 'PRT',
    'electrical material': 'HDW', 'electrical materials': 'HDW',
    'plumbing material': 'HDW', 'plumbing materials': 'HDW',
    'insulation': 'HDW', 'insulation materials': 'HDW', 'adhesive': 'HDW',
    'bitumen filler': 'HDW', 'joint fillers & bitumen': 'HDW', 'chemical': 'HDW',
    'fastener': 'ACC', 'fasteners': 'ACC', 'tape': 'ACC', 'tapes': 'ACC',
    'hinge': 'ACC', 'gift material': 'ACC', 'stationery material': 'ACC',
    'tiles & flooring': 'TLE', 'tile': 'TLE',
    'fabric': 'FBR', 'carpet': 'FBR', 'leather': 'FBR', 'foam': 'FBR',
    'signage material': 'TLS', 'wax': 'TLS',
    'general': 'GEN', 'artificial grass': 'GEN', 'solid surface': 'GEN',
}
```

## Edge Case

Lexan Sheet was not in the original map and slipped through as untransformed. Fixed by adding `'lexan sheet': 'PRT'`. Always verify with a Counter after transformation.

## Source File Details

- Original: `Product_raw_materials_final.xlsx` (1,377 rows, 16 cols)
- Output: `Product_raw_materials_standardized.xlsx`
- Columns transformed: Col2 (Name) and Col3 (English Name)
- Pattern: `Prefix - Rest | Arabic` → `CODE - Rest | Arabic`
- Arabic name (Col4) had no prefix to change

## Phase 2 — Native Naming (strip codes from names)

After prefix→code transformation, names still have codes embedded (e.g. `"PNT - Ditto Staircases..."`). Codes belong in a Category column (Col5/Col6), NOT in the Name column.

### Detection of non-descriptive names

Names that are just dimensions or cryptic need a material type prepended:

```python
import re

# Patterns that indicate a name is non-descriptive
DIMENSION_PATTERNS = [
    re.compile(r'^\d+\s*[+xX*]\s*\d+'),   # 40+40, 10x10, 5*10
    re.compile(r'^\(\d+\)$'),             # (40), (20)
    re.compile(r'^\d+\s*mm'),             # 10 mm, 5mm
    re.compile(r'^\d+["\']'),             # 1", 2"
    re.compile(r'^\d+\.?\d*\s*[xX]'),     # 0.5x, 1.2x
    re.compile(r'^\d{1,3}$'),             # single number like 1, 10, 40
]

def is_non_descriptive(name):
    if not name or name.strip() == '':
        return True
    n = name.strip()
    # Too short single-word item
    if len(n.split()) == 1 and len(n) < 10:
        return True
    # Pure number
    if re.match(r'^\d{1,3}$', n):
        return True
    # Starts with dimension pattern
    for pat in DIMENSION_PATTERNS:
        if pat.match(n):
            return True
    return False
```

### Fixing non-descriptive names

Use the **original raw prefix** (before code transformation) to prepend as a natural word:

```python
def make_native(name, original_prefix):
    """Prepends material type naturally for dimension-only names."""
    if not is_non_descriptive(name):
        return name
    # Map raw prefix to clean English label
    LABEL_MAP = {
        'solid wood': 'Solid Wood', 'mdf': 'MDF', 'plywood': 'Plywood',
        'steel': 'Steel', 'steel shs': 'Steel SHS', 'steel pipe': 'Steel Pipe',
        'aluminum': 'Aluminum', 'aluminum profile': 'Aluminum Profile',
        'acrylic sheet': 'Acrylic Sheet', 'acrylic paint': 'Acrylic Paint',
        'forex sheet': 'Forex Sheet', 'plastic sheet': 'Plastic Sheet',
        'paint': 'Paint', 'tile': 'Tile',
        'adhesive': 'Adhesive', 'chemical': 'Chemical',
        'fastener': 'Fastener', 'tape': 'Tape',
        'fabric': 'Fabric', 'carpet': 'Carpet',
        # add more as needed
    }
    label = LABEL_MAP.get(original_prefix.lower(), original_prefix.title())
    return f"{label} {name}"
```

### Full verification pass

After Phase 2, scan all names and fail if any still have codes or bare dimensions:

```python
from collections import Counter

def verify_native_names(ws, name_col=2, code_col=5):
    issues = []
    for row in range(2, ws.max_row + 1):
        name = str(ws.cell(row=row, column=name_col).value or '')
        # Check for leftover codes
        if re.match(r'^[A-Z]{3}\s*[-–—]', name):
            issues.append(f"Row {row}: code still in name - {name}")
        # Check for bare dimensions
        if is_non_descriptive(name):
            issues.append(f"Row {row}: non-descriptive name - {name}")
    return issues
```

### Key result

After Phase 2 the output file has:
- **Col1**: ID
- **Col2**: Native Name (e.g. `"Ditto Staircases Paint 1L"` — NO codes)
- **Col3**: English Name (same transformation)
- **Col4**: Arabic Name (unchanged)
- **Col5**: Raw Materials Category code (e.g. `PNT`, `MTL`)
- **Col6+**: remaining original columns
