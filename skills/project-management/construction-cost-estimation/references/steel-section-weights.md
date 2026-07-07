# Steel Section Weights Reference

## European Profiles (IPE — I-beam with parallel flanges)

| Profile | Weight (kg/m) | Height (mm) | Flange Width (mm) |
|---------|--------------|-------------|-------------------|
| IPE 200 | 22.4 | 200 | 100 |
| IPE 220 | 26.2 | 220 | 110 |
| IPE 240 | 30.7 | 240 | 120 |
| IPE 270 | 36.1 | 270 | 135 |
| IPE 300 | 42.2 | 300 | 150 |

## European Wide Flange (HEA)

| Profile | Weight (kg/m) | Height (mm) | Flange Width (mm) |
|---------|--------------|-------------|-------------------|
| HEA 200 | 42.3 | 190 | 200 |
| HEA 220 | 50.1 | 210 | 220 |
| HEA 240 | 60.3 | 230 | 240 |
| HEA 260 | 68.2 | 250 | 260 |

## W-Sections (ASTM A6 — US)

| Profile | Weight (kg/m) | Notes |
|---------|--------------|-------|
| W8×31 | 46.1 kg/m (31 lb/ft) | Common reinforcement beam |
| W10×30 | 44.6 kg/m | Moderate duty |
| W12×26 | 38.7 kg/m | Light frame |

## UPN Channels (European — UNP)

| Profile | Weight (kg/m) | Height (mm) |
|---------|--------------|-------------|
| UPN 180 | 22.0 | 180 |
| UPN 200 | 25.3 | 200 |
| UPN 220 | 29.4 | 220 |

## Angle Profiles (EA — Equal Angle)

| Profile | Weight (kg/m) |
|---------|--------------|
| EA 200×200×20 | 59.9 |
| EA 200×200×16 | 48.7 |
| EA 150×150×15 | 33.8 |
| EA 100×100×10 | 15.1 |

## Container Reference Data

| Type | External Dims (L×W×H) | Tare Weight (kg) | Internal Area (m²) |
|------|----------------------|------------------|-------------------|
| 20ft Standard | 6.06m × 2.44m × 2.59m | ~2,200 | ~14.0 |
| 40ft Standard | 12.19m × 2.44m × 2.59m | ~3,700 | ~28.3 |
| 40ft HC | 12.19m × 2.44m × 2.89m | ~3,900 | ~28.3 |
| 45ft HC | 13.72m × 2.44m × 2.89m | ~4,300 | ~31.9 |

## Steel Frame — Counting Methodology

For a 2-storey steel frame building from design drawings:

**1. Count the structural grid:**
- Column grid = numbered along length × lettered along width
- Typical grid for ~22m × ~12m building: 7 × 4 = 28 column positions

**2. Columns:**
- Count = grid intersections (typically 28)
- Height = ground-to-first-floor (~5.0m) + first-floor-to-roof (~2.5m) = ~7.5m total
- Weight = count × height × section kg/m
- Example: 28 × 7.5m × 50.1 kg/m (HEA220) = ~10,500 kg

**3. Main beams (girders):**
- Run along column lines, typically IPE240
- Count = grid lines × floors × span
- Example: 4 lines × 2 floors × 22.36m × 30.7 kg/m = ~5,500 kg

**4. Secondary beams (joists):**
- Span between main beams, typically IPE220 at ~1.55m c/c
- Count = bays per floor × beams per bay × floors
- Example: 3 bays × 3 beams × 2 floors × 12.6m × 26.2 kg/m = ~5,900 kg

**5. Edge/roof beams:**
- Perimeter × 2 (edge + roof) × section weight
- Example: 2 × (2 × (22.36 + 12.6)) × 30.7 = ~4,300 kg

**6. Add-ons:**
- Bracing (EA angles): ~2.5 tons
- Connections + base plates + stiffeners: ~3.5 tons
- Steel staircase (2-storey): ~2.5 tons
- Shear studs + decking: if composite

**7. Cross-check:**
- 2-storey commercial frame: 50-65 kg/m² built-up area
- Total built-up = footprint × floors = ~563 m²
- Expected total: 28-37 tons

## Rule-of-Thumb Steel Quantities

| Building Type | Steel Weight (kg/m² of built-up area) |
|--------------|--------------------------------------|
| 1-storey steel frame (light) | 35-50 |
| 2-storey steel frame (commercial) | 50-65 |
| 3-storey steel frame | 65-80 |
| Container-based (6 units, modified) | 90-110 (includes container tare) |

## Saudi Market Rates Reference (2026)

### Structural
| Item | Rate (SAR) | Unit |
|------|-----------|------|
| Structural steel fabricated + marine coating | 9,000-11,000 | per ton |
| RMC K350 (4,000 psi) delivered | 350-400 | per m³ |
| Reinforcement steel (rebar) Grade 60 | 3,000-4,000 | per ton |
| SS316 handrails installed | 900-1,200 | per lm |
| PWD ramp (concrete + finish + rail) | 1,800-2,500 | per m² |
| Pad footing (RMC + rebar + formwork) | 500-650 | per m³ |

### Facade
| Item | Rate (SAR) | Unit |
|------|-----------|------|
| Auto sliding door 386cm full-height | 22,000-25,000 | nos |
| Auto sliding door 200cm | 15,000-18,000 | nos |
| Auto sliding door 120cm | 12,000-14,000 | nos |
| Glass facade DG 6/12/6mm installed | 1,200-1,500 | m² |
| GRC/GRP cladding installed | 800-1,100 | m² |
| Illuminated 3D acrylic lettering | 1,800-2,500 | lm |

### MEP
| Item | Rate (SAR) | Unit |
|------|-----------|------|
| Packaged AC 5-ton installed (MERV 14) | 18,000-25,000 | nos |
| Extract fan 24×24, 250-350 m³/h | 800-1,200 | nos |
| Air curtain 1m, cross-flow | 2,500-3,500 | nos |
| Electrical first-fix + MDB | 85,000-120,000 | LS |
| 220V outlet Legrand Arteor/Belanko | 350-500 | nos |
| Track lighting + DALI control full system | 90,000-140,000 | LS |
| Cat 6A data outlet (shielded, 10 Gbps) | 400-600 | nos |
| CCTV first-fix + NVR (4K IP) | 45,000-65,000 | LS |
| Fire protection (addressable alarm + sprinklers + FM-200) | 120,000-180,000 | LS |
| Plumbing first-fix (PPR + PVC) + ceramic tiling (2 WCs) | 35,000-55,000 | LS |

### Interior Finishes
| Item | Rate (SAR) | Unit |
|------|-----------|------|
| LVT vinyl flooring (R10, Commercial Grade 34) | 120-180 | m² |
| Gypsum board partition 12mm + metal stud | 95-140 | m² |
| Paint full system (primer + 2 putty + base + 2 finish) | 35-55 | m² |
| Gypsum board ceiling 12.5mm | 110-160 | m² |
| Rockwool thermal insulation 100mm + vapour barrier | 65-95 | m² |
| CNC cladding MDF + painted finish | 450-650 | m² |
| Canvas printing 800+ DPI + frame + install | 180-280 | m² |
| Kitchen aluminium + Corian solid-surface counter | 4,000-6,000 | lm |
| Kitchen melamine cladding + shelving 18mm | 200-350 | m² |
| Reception counter melamine 200×70×83cm | 8,000-12,000 | nos |

### FF&E
| Item | Rate (SAR) | Unit |
|------|-----------|------|
| Executive reception chair (high-back, leather) | 3,000-5,000 | nos |
| Upholstered seating 200×80×75cm | 8,000-12,000 | nos |
| Dining table set (MDF Oak + 4 chairs) | 4,000-6,000 | set |
| Artificial decorative trees (porcelain planter) | 1,500-2,500 | nos |
| Shelving unit 4.85×2.9m melamine | 12,000-18,000 | nos |

### Sanitary
| Item | Rate (SAR) | Unit |
|------|-----------|------|
| One-piece European WC (back-to-wall) | 1,200-2,000 | nos |
| Vanity wash-basin + mixer + MDF unit | 1,500-2,500 | nos |
| Hand-shower (Shataf) + hose 1.2-1.5m | 200-400 | nos |
| Bathroom mirror 6mm Belgian-grade | 300-500 | nos |
| Bathroom door green MDF 40-45mm | 1,500-2,500 | nos |

### External
| Item | Rate (SAR) | Unit |
|------|-----------|------|
| Landscaping 97m² native xeriscaping + drip irrigation | 120,000-180,000 | nos |
