# Design Coordination Risk Identification — AV/IT/ELV ↔ MEP

## When to Use

You need to identify coordination risks between a specialty systems designer's submission (AV, IT, ELV, Low Current, Security) and the base build MEP infrastructure (electrical power, cooling, containment, structural). Typical triggers:

- AV/IT/ELV Concept Design or Developed Design submission arrives for review
- Power & Data GA drawings need checking against equipment schedules
- Rack room layouts need verification against architectural room sizes and MEP capacity
- Before IFC, to identify scope gaps between the specialist fit-out and base build
- When the base build D&B contractor hasn't been appointed yet (pre-tender coordination)

## Methodology

### Phase 1: Assemble All Relevant Documents

Collect from at least these disciplines:

| Discipline | What to look for | Key risk signals |
|---|---|---|
| **AV/IT/ELV Design** | BOQ, rack plan, cable schedule, power consumption sheet, AV GA drawings, projection drawings, equipment datasheets | Specs without power data, missing lead times, "D&B to design" notes |
| **Electrical (Power & Data GAs)** | Power outlet layouts, data outlet layouts, circuit schedules, single-line diagrams | Outlet counts not matching equipment count, missing dedicated circuits |
| **Architectural GA** | Room layouts, ceiling plans, door schedules | Rack room size vs equipment depth, ceiling clearance for projectors |
| **HVAC / Cooling** | Cooling load calculations (if available), air handler schedules | Rack room cooling capacity vs computed heat load |
| **Structural** | Beam/column layouts, slab thickness | Projection path obstructions, mount point availability |
| **Cable Containment** | Cable tray routing drawings, tray schedules, segregation requirements | Tray sizing not matching cable bundle counts |
| **Scope/SOW Documents** | D&B scope matrix, specialist SOW, responsibility matrix | "TBC" or "by others" without clear boundary |

### Phase 2: Compute Equipment Loads

Extract from the AV/IT BOQ or equipment schedule:

**Power consumption per item:**
```python
# Typical BOQ structure (openpyxl on system Python)
for row in ws.iter_rows(min_row=header_row, values_only=True):
    if row[qty_col] and row[unit_watts_col]:
        total_w += row[qty_col] * row[unit_watts_col]
```

**Heat load per item:**
- If BTU/h is not stated in the BOQ, compute: `BTU/h = Watts × 3.412`
- For vendor datasheets that list BTU directly, use that value (it includes power supply losses)
- Media servers (DVS Hydra4 RTX5000 etc.) are major heat sources: 850W → ~2,900 BTU/h each

**Per-floor aggregation:**
Group equipment by floor/zone. The zone name often encodes floor level:
```python
floor_map = {
    '- FF': 'First Floor', '- GF': 'Ground Floor',
    '- LG': 'Lower Ground', '- B': 'Basement',
    '- 1F': 'First Floor'
}
```

### Phase 3: Analyze Rack Rooms

For each AV/IT rack room:

1. **Cross-reference rack size:**
   - Architectural GA may show a different rack size/height than the AV pack
   - E.g., architectural says "24U / 1.1m" while AV says "45U / 2.1m" — flag for IFC resolution
   
2. **Compute rack heat load:**
   Sum all equipment BTU/h in each rack from the rack plan layout
   
3. **Assess room adequacy:**
   - Room internal dimensions: is there ≥800mm front clearance, ≥600mm rear clearance per standards?
   - Door width: can the rack be brought in? (rack depth ~812mm)
   - Floor loading: ~300kg for a fully-populated 45U rack in ~5m²
   
4. **Cooling requirement:**
   - Rack heat load in BTU/h / 12,000 = tons of cooling
   - Check if HVAC design exists or note "D&B to design" risk

### Phase 4: Analyze Projections & Spatial Conflicts

For each projection-based gallery:

1. **Extract projection geometry from drawings:**
   - Screen/image size (e.g., 16,700 × 3,700mm)
   - Throw ratio (e.g., 0.35:1 UST — ultra-short-throw)
   - Blend zones for multi-projector setups
   - Mount type and position (above/below ceiling)

2. **Identify spatial conflicts:**
   - Does the projection path cross public circulation zones? → Visitor shadow risk
   - Is the projector surface-mounted below ceiling? → Conflict with lighting grid, HVAC diffusers
   - Is there image spill onto floor/walls? → Physical masking requirement
   - Is keystone/distortion correction needed? → Resolution impact
   
3. **Check structural overlay:**
   - AV GA drawings typically lack structural overlays → beam/column conflicts unknown
   - UST mirror lenses (Panasonic ET-DLE035, Epson ELPLX02WS) are large assemblies needing extra ceiling clearance

### Phase 5: Assess Cable Routing & Containment

From the cable schedule, identify:

1. **Longest runs:**
   - Audio amplifier to first speaker: often 40m+
   - HDBaseT extender runs: CAT6a limit is 100m
   - HDMI passive runs: limit ~15m → need active extenders

2. **Bundle sizing:**
   - Each projector typically needs: 1x CAT6a (video), 1x CAT6a (control), 1x CAT6a (network), 1x power
   - For 16 screens in one gallery: 48+ CAT6a cables + 16 power cables
   - Multiply by 7mm per CAT6a (Type A cable) → significant tray fill

3. **Segregation:**
   - Audio signal cables need separation from power cables (EMI risk)
   - Is segregation strategy documented? (separate trays, shielded cables, minimum spacing)
   - External/weatherproof runs: cable entry sealing not always addressed

### Phase 6: Identify Infrastructure Gaps

Critical gaps to flag:

| Gap | Signal | Impact |
|-----|--------|--------|
| **No MEP design exists** | "D&B contractor to design in next stage" on rack room drawings | No electrical/cooling/containment for AV at all |
| **No UPS strategy** | Rack plan shows PDU only, no UPS; gallery equipment has no backup | Power bump crashes media servers, requires projector cool-down |
| **No scope separation** | SOW says "AV contractor provides equipment, base build provides infrastructure" with no detailed matrix | Change orders when D&B discovers loads |
| **Power outlet shortage** | Equipment count >> outlets shown on Power & Data GAs | Daisy-chaining = fire risk, voltage drop |
| **No procurement timeline** | No lead times in BOQ or datasheets | Critical items (16K projectors, media servers) have 12-20 week leads |
| **Ambient light not addressed** | Projection drawings note "masking may be required dependent on ambient light" | Image washout without lighting control integration |
| **Ceiling clearance unknown** | Mounting method shown but slab-to-soffit not stated | UST lens + mount may not fit in ceiling void |

### Phase 7: Compile Risk Register

Output a structured risk assessment with:

1. **Executive summary** — key findings, critical items
2. **Equipment summary** — projector types, media server count, display count, total load
3. **Per-floor breakdown** — power (kW), heat load (BTU/h), dominant equipment
4. **Rack room analysis** — per floor: size, population, heat load, cooling need
5. **Spatial conflict analysis** — per gallery with projection issues
6. **Cable routing gaps** — containment, segregation, longest runs
7. **Infrastructure gaps** — MEP, UPS, scope, procurement
8. **Risk register table** — ID, category, likelihood, impact, priority, action

## Common Risk Categories Found in AV/MEP Coordination

| RBS | Category | Example Risks |
|-----|----------|---------------|
| RBS-1 | **Spatial Coordination** | Projection path crosses circulation; mount clashes with lighting; beam blocks throw |
| RBS-2 | **MEP Integration** | No rack cooling design; insufficient power outlets; tray sizing inadequate |
| RBS-3 | **Scope Boundaries** | D&B infrastructure undefined; UPS not provided; ambient light treatment unassigned |
| RBS-4 | **Infrastructure Capacity** | Rack heat density exceeds room cooling; single circuit for multiple projectors |
| RBS-5 | **Design Consistency** | Rack size varies between architectural and AV packs; conflicting floor labels |
| RBS-6 | **Procurement** | Long-lead un-ordered; lens availability risk; datasheet missing power data |
| RBS-7 | **Cable Infrastructure** | No containment routes; segregation unaddressed; HDBaseT length exceeds spec |

## Pitfalls

- **The BOQ may have no unit costs populated.** The line items still contain the equipment types, quantities, power ratings, and heat loads — these are what matter for coordination risk, not the cost.
- **AV GA PDFs from Vectorworks may have no extractable text.** Text extraction (pypdf) returns blank. Use pdftoppm to convert to PNG then vision analysis. If vision is unavailable, the drawing title/frame info in the PDF metadata and the folder index (_README.md) are alternative sources.
- **Cable schedules may reference the wrong project.** Check the project code in the header (e.g., "6930 - Aseer Regional Museum") and verify drawing number prefix matches.
- **Power consumption sheets may use 220V or 230V reference.** Aseer uses 220V. Confirm the project's voltage before computing current.
- **Rack rooms noted as "D&B to design" = no MEP exists.** This is the single biggest coordination risk. Flag it every time it appears.
- **Heat load per rack can exceed 15,000 BTU/h in small rooms (~5m²).** This requires active cooling (CRAC unit or in-row cooling), not just ceiling diffusers.
- **GF rack height discrepancies.** The architectural GA may label a rack 24U/1.1m while the AV pack specifies 45U/2.1m. The architectural GA controls spatial allocation — if it says 24U, the AV equipment physically won't fit.
- **Drawings marked "All dimensions to be confirmed on site" cannot be scaled for coordination.** These are conceptual only — any coordination decision based on them carries risk.
