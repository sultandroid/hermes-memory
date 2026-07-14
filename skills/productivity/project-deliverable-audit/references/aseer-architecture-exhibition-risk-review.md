# Aseer Museum — Pre-Appointment Architecture/Exhibition Cross-Discipline Risk Review

**Source drawing set:** `02_AS_Pre-Appointment Exhibition Drawings_250313` (RIBA Stage 2-3)
**Date:** 2026-07-14
**Situation:** Samaya Technical Office reviewing the AS-drawing package before IFC. New MoC object list about to arrive — need to identify cross-discipline risks that will affect coordination once placements are finalised.

## Floor-by-Floor Gallery Composition

### Basement Floor (BF) — 10 galleries + Lobby + Circulation
| Space | Files | Sections | Content Layers |
|-------|-------|----------|----------------|
| G4 | 20 | 7 (A-H) | Showcase, AV, Graphics, Interactives, Models & Replicas, Art, Open Display, LL/HL Power, RCP |
| G5 | 19 | 2 | Showcase, AV, Graphics, DI/HI + MI/TI Interactives, Models, Art, Open Display, LL/HL Power, RCP |
| G6 | 36 | 14 (A-N) | Same 6 content layers + dense sections |
| G7 | 23 | 4 | Same 6 layers |
| G8 | 26 | 5 (A-H) | Same 6 layers |
| G9 | 24 | 3 (A-H) | Same 6 layers |
| G10 | 23 | 2 | Same 6 layers |
| G11 | 18 | 4 | Same 6 layers (no Model/Replica/Open Display) |
| G12 | 23 | 5 (A-T) | Same 6 layers |
| G13 | 19 | 2 | Same 6 layers |

### Lower Ground Floor (LGF) — 4 galleries + Lobby + Temporary Gallery
| Space | Files | Sections | Notes |
|-------|-------|----------|-------|
| G1 | 21 | 4 | AV + DI_HI + MI_TI — triple interactive overlay |
| G2 | 19 | 2 | Standard 6-layer set |
| G3 | 19 | 2 | Standard 6-layer set |
| G14 | 18 | 1 | Standard 6-layer set |
| LB2 | 19 | 2 | Lobby — no showcase/interactives |
| TG | 19 | 2 | Temporary Gallery — flexible space |

### Ground Floor (GF) — Amenity/Public zones
| Space | Files | Notes |
|-------|-------|-------|
| LB1 | 16 | Main lobby, welcome desk, security, seating |
| EC | 14 | Children's Educational Centre |
| VI | 13 | VIP Reception |
| RT | 13 | Retail / Gift Shop |
| CL1 | 14 | Circulation — proposed staircase |

### First Floor (1F) — Cafe, Library
| Space | Files | Notes |
|-------|-------|-------|
| CA & TA | 16 | Cafe & Terrace — largest DWG files (35.8 MB) |
| LR & CL1.1F | 17 | Library & Circulation |

## Key Drawing Codes Used (Exhibition Fit-Out Standard)

Every gallery drawing number follows `{Gallery}_{Code}-{Title}`:

| Code | Type |
|------|------|
| `_0000` | GA Plan |
| `_0001` | Key Dimension Plan |
| `_0004` | Setwork / FF&E Locations GA |
| `_0005` | Showcase Locations GA |
| `_0006` | Graphics Locations GA |
| `_0007` | AV Locations GA |
| `_0008` | DI/HI Interactives Locations GA |
| `_0009` | MI/TI Interactives Locations GA |
| `_0010` | Models & Replicas Locations GA |
| `_0011` | Art Commissions Locations GA |
| `_0012` | Open Display Locations GA |
| `_0030` | LL Power and Data GA |
| `_0031` | HL Power and Data GA |
| `_0032` | Reflected Ceiling Plan |
| `_0033` | Building Grid GA |
| `_1000+` | Sections |

## Showcase Types

| Type | Dims (W×D×H mm) | Form | Use Case |
|------|------------------|------|----------|
| T1 | 8300×1000×1420 | Recessed wall, hinged | Long linear wall display |
| T2 | 2600×1000×2950 | Freestanding 4-sided | Large freestanding objects |
| T3 | 5850×1250×978 | Tabletop, mech hood | Flat-lay artefacts |
| T4 | 450×450×975 | Square plinth + mech hood | Single precious object |
| T5A | 760×760×980 | Square plinth, hinged | Small single-object |
| T5B | 1000×1000×2000 | Large plinth + hinged | Taller single-object |
| T6A | 2000×800×2450 | Freestanding cabinet | Medium-large vertical |
| T6B | 2000×800×2450+2075 | Freestanding + back panel | Against-wall w/ fabric |

## Cross-Discipline Risks Identified

### 1. CONFIRMED CONFLICTS

| ID | Risk | Evidence | Priority |
|----|------|----------|----------|
| C-01 | **GF AV Rack Room — rack height conflict** | Arch overall (XX_GF_0000) says "24U 1.1m". AV pack (GF_AR_0000) says BGR-45SA-32 (45U, 2105mm). Direct contradiction. | **CRITICAL** |
| C-02 | **GF AV Rack Room — location TBD** | GF Overall GA note: "Location TBD after 100% submission". No confirmed position. | **CRITICAL** |
| C-03 | **Stramp — MEP/structural deferred** | EX_1000/1001 notes: "by D&B contractor in next stage". 3100mm rise ramp with integrated seating has no engineering. | **CRITICAL** |

### 2. MEP/AV Risks

| ID | Risk | Galleries Affected | Severity |
|----|------|-------------------|----------|
| M-01 | AR rooms need 24/7 HVAC, raised floor, pre-action sprinkler — compact rooms (~2030×2530mm BF). Slab-to-soffit TBC. | BF_AR, LGF_AR, GF_AR, 1F_AR | High |
| M-02 | TG needs reconfigurable MEP — no modular strategy evident | TG (LGF) | Medium |
| M-03 | T2 showcases 2950mm tall — may exceed BF ceiling clearance | All BF galleries with T2 placement | High |
| M-04 | High AV/interactive density in G1 (triple overlay) — power demand unknown | G1, G6, G8, G12 | Medium |

### 3. Structural Risks

| ID | Risk | Evidence | Severity |
|----|------|----------|----------|
| S-01 | CL1 proposed staircase — no structural design | XX_GF_0013: "refer to structural engineers drawings" | High |
| S-02 | Ahmed Mater ceiling-suspended art — weight TBC | XX_GF_0013: "weight TBC by artist" | High |
| S-03 | Rashed AlShashai 200kg floor-mounted art | XX_GF_0013: 200kg floor-mounted | Medium |
| S-04 | G6 complex geometry — 14 sections, highest clash risk | 14 section drawings (most of any gallery) | Medium |

### 4. Spatial Adjacency Risks

| ID | Risk | Zones | Severity |
|----|------|-------|----------|
| A-01 | EC (Children's Ed) adjacent to LB1 (Main Lobby) — noise cross-talk | GF — EC + LB1 | Medium |
| A-02 | TG events adjacent to permanent galleries G2, G3, G14 | LGF — TG | Medium |
| A-03 | RT (Retail) queue can encroach on LB1 lobby circulation | GF — RT + LB1 | Medium |

### 5. Accessibility & Egress Risks

| ID | Risk | Floor | Severity |
|----|------|-------|----------|
| E-01 | 10 galleries on BF — egress distance critical | BF | High |
| E-02 | Stramp gradient ~12% — typical code max is 1:12 (8.3%) | EX (Stramp) | High |
| E-03 | 900mm handrail may need dual-height for wheelchair + children | EX (Stramp) | Medium |
| E-04 | Gallery fit-out (showcase, setwork) may block accessible routes | All floors | Medium |

### 6. MoC Object Sensitivity

| Tier | Galleries | Reason |
|------|-----------|--------|
| **High** | G6, G8, G12, G1 | Many sections + all 6 content layers → object changes cascade through sections, AV, interactives |
| **Moderate** | G4, G5, G7, G9, G10, G11, G13, G14, G2, G3 | Standard set, fewer sections |
| **Low** | TG, LB1-3, EC, RT, VI, CA&TA, LR | Amenity/flexible spaces, less object-dependent |

## Key Recommendations

1. **Resolve GF AR rack spec and location** — highest-priority blocker for all GF MEP
2. **Commission structural engineering for Stramp + CL1 staircase** — on critical path
3. **Prioritize G6 for BIM clash detection** — 14-section complexity = highest MEP/structural clash risk
4. **Verify ceiling heights for T2 (2950mm) showcases** — especially BF
5. **Define TG MEP strategy** as modular/demountable
6. **Cross-check all gallery fit-out against fire escape distances and accessible routes** — BF critical
7. **Establish MoC change protocol** — G6/G8/G12/G1 changes trigger full re-coordination
8. **Resolve Stramp gradient compliance** with KSA building code
