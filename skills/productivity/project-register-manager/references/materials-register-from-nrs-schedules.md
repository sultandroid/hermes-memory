# Materials Register from NRS Exhibition Schedules

## Source Documents

NRS 6930 Pre-Appointment Exhibition Schedules (Rev A, 21-Feb-25) contain 15 schedule types:

| Schedule | File Pattern | Key Data |
|----------|-------------|----------|
| Finishes Schedule | `6930_Finishes_Schedule_rev A` | All materials with FI_XX_XX codes, brands, colours, Oddy flags |
| FF&E Schedule | `6930_Aseer_FF&E Schedule` | Furniture with brand, model, URL, finish |
| Setwork Schedule | `6930_Aseer_Setwork Schedule_rev A` | Setwork items with finishes references (FI_ME_01, FI_WO_01, etc.) |
| Showcase Schedule | `6930_Aseer_Showcase Schedule` | Showcase types with materials |
| Object Schedule | `6930_Aseer_Object Schedule` | Artifacts (not materials) |
| Art Commission, Asset, Exhibit, Graphic, Media, Mockups, Model & Replica, Space & Gallery, Tactile, Wayfinding | Various | Supporting data |

## NRS Spec Reference Format

From `12_Procurment/Architecture/` folder structure, NRS spec references follow the pattern `A2742-{CODE}`:

| Code | Trade | File Location |
|------|-------|---------------|
| K10E, K40B | Ceilings | `Architecture/Ceiling/Specs/` |
| K11A | Linning | `Architecture/Linning/Specs/` |
| L10 | Setwork | `Architecture/Setwork/Specs/` |
| L20A | Doors | `Architecture/Doors/Specs/` |
| L30 | Stairs | `Architecture/Stairs/Specs/` |
| M40D | Flooring | `Architecture/Flooring/Specs/` |
| M60 | Wall Finishes | `Architecture/Wall Finishes/Specs/` |
| N10E | Furniture | `Architecture/Furniture/Specs/` |
| N17A | Showcases | `Architecture/Showcases/Specs/` |

## Materials Register Column Structure

| Column | Description |
|--------|-------------|
| MA Ref | MOC-MUS-ASE-1A0-MA-XXXX |
| Material | Name per NRS schedule |
| Finishes ID | FI_ME_01, FI_FL_03, etc. |
| NRS Spec Reference | A2742-XXXX |
| Brand / Supplier | Named or TBC Locally Sourced |
| Colour / Finish | Per NRS schedule |
| Location | Which galleries / zones |
| Oddy | Required / Passed / — |
| Sample | Yes/— |
| Lead Time | Weeks |
| Procurement By | Samaya / GBH / Rawasin / Subcon |
| Status | Approved / In Preparation / Not Started |
| CG Response | Date + Code |
| Notes | Dependencies, critical path flags |

## Full Project Materials Scope (~170+)

### Architecture Finishes (82 items from Finishes Schedule)
- Metal (6): Patinated brass, PVD SS304, powder coated steel, stainless steel
- Flooring (14): Ceramiche Piemme, Concept Tiles, Domus, Tarkett, local stone
- Ceilings (8): Asona, Knauf, Fermacell, Kvadrat
- Walls (10): Paint (RAL colours), Domus tiles
- Stone (4): Marble, limestone, cast concrete
- Glass (4): Low-iron, frosted, tinted, anti-reflective (showcase)
- Wood (3): Oak veneer, ARPA HPL
- Fabric (9): All Kvadrat (Remix 3, Hallingdal 65, Volume)
- Solid Surface (5): Hi Macs, Corian, Smile Plastics
- Composites (6): Valchromat, Viroc, Clay-works
- Graphic Substrates (13): Viroc, GF Smith, Duratran

### AV Equipment (Rawasin) — ~50+ items from AV BOQ
- Show Control: Q-Sys Core 510i, TSC-50-G3, TSC-70-G3
- Audio: Yamaha VXC6, VXS8, XMV8140-D
- Projection: Epson EB-PU2116W/2010W, Panasonic PT-RZ
- Displays: Samsung VH55C-R, Iiyama 86" 4K
- Media Players: Brightsign HD225/HD1025
- Accessories: Peerless mounts, SY Xcalibur extenders, Unicol PSU

### MEP Equipment — from Procurement Schedule
- HVAC: FAHUs, FCUs, split units
- Plumbing: Pipes, fittings
- Fire alarm, BMS, fire suppression

### Showcase (GBH)
- Anti-reflective glass, Corian plinths, hydraulic lifters, Abloy locks

### Lighting (Studio ZNA) — pending Stage 4 delivery

### FF&E — from NRS FF&E Schedule
- &Tradition, Muuto, HAY, Kvadrat, Studio Twenty Seven, Ligne Design

## Oddy Testing Required Materials

| Material | Finishes ID | Supplier |
|----------|-------------|----------|
| Showcase Glass (anti-reflective) | FI_GL_04 | TBC |
| Powder Coated Steel (showcase) | FI_ME_02 | TBC |
| Powder Coated Steel (showcase) | FI_ME_04 | TBC |
| Kvadrat Remix 3 — Rust Orange | FI_FA_03 | Kvadrat |
| Kvadrat Hallingdal 65 — Light Beige | FI_FA_04 | Kvadrat |
| Crane'sCrest Archival Paper | FI_GR_08 | GF Smith |

## Excel Generation Pattern

Use openpyxl with:
- Two sheets: "Materials Register" (data) + "Summary" (category totals)
- Navy headers (#1F3864), category bands (#D6E4F0)
- Color-coded status: green=Approved, amber=In Prep, red=Not Started
- Frozen header row, wrapped text
- Summary sheet with totals per category

```python
# Key structure
categories = [
    ("CATEGORY NAME", [
        [MA Ref, Material, Finishes ID, NRS Spec Ref, Brand, Colour, Location, Oddy, Sample, Lead Time, Procurement By, Status, CG Response, Notes],
    ]),
]

headers = ["MA Ref", "Material", "Finishes ID", "NRS Spec Reference", "Brand / Supplier", "Colour / Finish", "Location", "Oddy", "Sample", "Lead Time", "Procurement By", "Status", "CG Response", "Notes"]
```

## Critical Path Items

1. **Patinated Brass (FI_ME_01)** — covers all setworks, showcases, doors, reception
2. **Corian (FI_SS_02)** — Showcase plinth fabrication (GBH dependency)
3. **Anti-reflective Glass (FI_GL_04)** — Showcase fabrication + Oddy test
4. **Kvadrat Fabric (FI_FA_01-10)** — All fabric-wrapped panels, acoustic treatment
5. **Ceramiche Piemme Tiles (FI_FL_01-03)** — Large floor areas, long lead
6. **Asona/Knauf Ceilings (FI_CL_01-10)** — Ceiling closure dependency
