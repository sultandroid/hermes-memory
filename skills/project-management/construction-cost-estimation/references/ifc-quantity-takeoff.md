# IFC Quantity Takeoff — Steel Weight Extraction

## When to Use

When you need steel tonnage from a BIM model but the design calculation PDF has image-only SAP2000 output that OCR can't read.

## Where to Find the IFC File

```
03_Design/<model>/06-IFC/IFC.ifc
```

Or alongside other Tekla exports. The file is a STEP physical file (ISO 10303-21), which is plain text.

## IFC Entity Types in Tekla Export

| Entity | Meaning |
|--------|---------|
| `IFCCOLUMN` | Vertical structural columns |
| `IFCBEAM` | Horizontal structural beams (includes main beams, secondary beams, edge beams, purlins) |
| `IFCMEMBER` | Bracing, diagonal members, sag rods |
| `IFCPLATE` | Base plates, connection plates, stiffeners, gratings |
| `IFCELEMENTASSEMBLY` | Bolted groups, stair assemblies |
| `IFCSLAB` | Floor/roof slabs |
| `IFCSTYLEDITEM` | Visual/style elements (ignore for quantities) |

## Extracting Profile Counts

### Tekla IFC Format

```
#123= IFCBEAM('2znU$cJ795FA08qVJpVydi',$,'THREAD','IPE240',$,#381,#406,'S235',.NOTDEFINED.);
                                    ↑name   ↑profile ↑...↑material
```

The 4th parameter (3rd quoted string, index 2) is the profile name. Tekla uses standard European profile names.

### Python Extraction

```python
import re
from collections import Counter

with open("IFC.ifc", "rb") as f:
    content = f.read().decode("latin-1")

profile_counts = Counter()
element_by_type = {t: Counter() for t in ["COLUMN", "BEAM", "MEMBER", "PLATE"]}

for etype in ["COLUMN", "BEAM", "MEMBER", "PLATE"]:
    for m in re.finditer(r'#\d+= IFC' + etype + r'\(', content):
        text_before = content[m.end():m.end()+500]
        quotes = re.findall(r"'([^']*)'", text_before)
        profile = quotes[2] if len(quotes) >= 3 else "?"
        profile_counts[profile] += 1
        element_by_type[etype][profile] += 1
```

### Filter Out Non-Structural Items

Tekla exports include bolts, nuts, and washers as separate entities that share profile naming. These are NOT structural steel:

- `M12_HEAVY_HEX_NUT` — bolt hardware
- `M12_WASHER` — washer
- `D16` — rebar / dowel

Filter these out before weight calculation.

## Weight Calculation

### Section Weight Table

| Profile Type | Standard kg/m | Use |
|-------------|---------------|-----|
| HEA 100-300 | varies (HEA220 = 50.1) | Columns |
| IPE 200-300 | varies (IPE220 = 26.2, IPE240 = 30.7) | Beams |
| UPN 180-200 | varies (UPN180 = 22.8) | Edge channels / purlins |
| RSA L-angles | 5.42 (60×60×6) | Bracing |
| SHS (square hollow) | 7.52 (70×4) | Secondary supports |
| CHS/TUBE round | 3.48 (50×3), 1.38 (30×2) | Handrails, guards, supports |
| PL (flat plate) | thickness × width × 7.85 kg/m³ | Base plates, connections |

### Estimating Average Length

From the building's structural grid dimensions (visible on plan drawings):

```
Building footprint width / number of bays = average bay width
floor-to-floor height from elevation drawings
```

For columns: height = storey height × number of storeys
For beams: average bay span in the beam's orientation
For bracing: diagonal of typical bay = √(bay_width² + storey_height²)

### Formula

```
Weight (kg) = count × average_length (m) × kg_per_m
Weight (tons) = weight_kg / 1000
```

## Verifying Against Industry Rules of Thumb

| Building Type | Typical Steel Weight |
|--------------|---------------------|
| 2-storey steel frame (office/commercial) | 45-65 kg/m² |
| Steel frame with composite deck | 55-75 kg/m² |
| Modular container structure | 80-110 kg/m² |

Cross-check your IFC-based total against the rule of thumb for the building type.

## Example Output

```
IFC Entity Counts:
  BEAM: 428
  COLUMN: 469
  MEMBER: 78
  PLATE: 303
  SLAB: 58

Profile Breakdown (structural only, filtered):
  IPE240: 72 beams  →  355m × 30.7 kg/m = 10,905 kg
  HEA220: 20 cols   →  150m × 50.1 kg/m = 7,495 kg
  IPE220: 77 beams  →  358m × 26.2 kg/m = 9,374 kg
  ...
  TOTAL: 41,422 kg = 41.42 tons
```

## Limitations

- IFC "Reference View" exports (ReferenceView_V1.2) may omit parametric section definitions — you can still get profile names from the entity parameters.
- The IFC file may not contain QTO (quantity takeoff) data sets — only geometry and profile references.
- Average length estimation introduces ~5-10% uncertainty versus exact model takeoff. For procurement, verify with the fabricator's own takeoff from the Tekla model.
