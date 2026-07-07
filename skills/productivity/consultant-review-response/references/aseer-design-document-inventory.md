# Aseer Museum — Design Document Inventory for Schedule Audit

Known design document locations and the brand data they contain, organized by material category.

## Directory Structure

```
Aseer-Museum/
├── B.O.Q/
│   ├── Floor-Finishing-Material-Detail.xlsx      # Floor tile/carpet suppliers
│   ├── Materials & Subcontractor Register (Master).xlsx  # EL-MAT codes, lighting brands
│   └── Copy of Procurement Tracker.xlsx           # AV hardware + subcontractor list
│
├── Design Files/
│   ├── Package_Part 2/
│   │   ├── 03_AS_Pre Design Pack_250313/
│   │   │   └── 03_AS_Pre-Appointment Exhibition Schedules_250313/
│   │   │       ├── Xcel/
│   │   │       │   ├── 6930_Finishes_Schedule_rev A.xlsx       # ← PRIMARY finishes supplier source
│   │   │       │   ├── 6930_Aseer_FF&E Schedule.xlsx            # Furniture brands
│   │   │       │   ├── 6930_Aseer_Showcase Schedule.xlsx        # Showcase types & specs
│   │   │       │   ├── 6930_Aseer_Setwork Schedule_rev A.xlsx   # Setworks description
│   │   │       │   └── 6930_Aseer_Graphic Schedule_rev A.xlsx   # Graphic substrates
│   │   │       └── PDFs/ (same content as Xcel/)
│   │   │
│   │   └── 06-AVHW + AV System Concept_rev A/
│   │       ├── 6930_Aseer_av_boq_v1.11_CONCEPT_210225.xlsx     # ← AV hardware brand source
│   │       ├── AVHW Spec Sheets/                                # Product PDFs confirming brands
│   │       └── 6930_Aseer_avrack_pl_v1.3_CONCEPT_200225.xlsx   # AV rack layouts
│   │
│   ├── 01_AS_Pre-Appointment Exhibition Documentation_250313/
│   │   └── 07-Lighting Design_rev A/
│   │       └── Specifications & Schedules/
│   │           ├── ZNA3297_ARM_SP_01_01 Luminaire Specification R2.pdf  # ← ALL lighting brands
│   │           └── ZNA3297_ARM_SC_02 R3 - Lighting Control Zones.pdf
│   │
│   └── Package_Part 2/04_AS_Commercial Documents_250313/
│       └── 01_AS_Pricing Schedule_250313/
│           └── Pricing Schedule for the Aseer Museum for Ministry of C.xlsx  # BOQ pricing
│
├── Subcontractors/13_MEP_Designer/
│   ├── 09_Offers/
│   │   ├── AD Engineering/AD_Engineering_Technical_and_Financial_Offer.pdf
│   │   ├── BluHaus/BluHaus_Design_Consultancy_Proposal_26May2026.pdf
│   │   ├── SG_Group/SG_Group_Aseer_Museum_Quotation.pdf
│   │   └── MEP_Design_Offer/Aseer Museum Quotaion updated 14 may 2025.pdf
│   └── 00_Prequalification/
│       └── AD_Engineering/ (20+ prequal documents, technical evaluation form)
│
└── Email_Archive/
    └── _aseer_tasks_backlog.md  # Tasks tracker with prequal status
```

## Confirmed Brand Mappings

### Floor Finishes (from Finishes Schedule, Supplier column)

| Design Ref | Description | Supplier |
|---|---|---|
| FI_FL_01 | Bits&Pieces 60x60 Steel Grain Quad | Ceramiche Piemme |
| FI_FL_02 | Bits&Pieces 60x60 Ash Grain Quad | Ceramiche Piemme |
| FI_FL_03 | Glitch Porcelain 1200x1200 Salt | Ceramiche Piemme |
| FI_FL_04 | Micro Concrete 1200x1200 Grey | Concept Tiles |
| FI_FL_05 | Micro Concrete 1200x1200 Anthracite | Concept Tiles |
| FI_FL_06 | Pietre 672x165mm Tile DRSP 02 | Domus |
| FI_FL_08 | Drammen 600x600mm Tile DADR 04 | Domus |
| FI_FL_12 | Carpet Asteranne A411 2903 Green | Tarkett |
| FI_WA_11 | Amazonia 200x65mm Tile DEAM 07 | Domus |

### Ceilings (from Finishes Schedule)

| Design Ref | Description | Supplier |
|---|---|---|
| FI_CL_01/08/10 | Fire-rated Sonacoustic plasterboard | Asona |
| FI_CL_02/07 | Slatted metal baffle V-P-500 | Knauf |
| FI_CL_04/06 | Fibre-reinforced / MR plasterboard | Fermacell or British Gypsum Rigidur |
| FI_CL_09 | Soft cell panel + Hallingdal 65-0200 | Kvadrat |

### Lighting (from ZNA Luminaire Specification R2)

| Luminaire | Location | Manufacturer |
|---|---|---|
| Kalis T55 suspended/recessed linear | General | Intra Lighting / Atrium (Charlie Petsch) |
| Kap 105 Dia | Atrium | Flos |
| Bon Jour Down Light | General | Flos |
| Laser Blade downlight/wall wash | Galleries | iGuzzini (Simon Meanwell) |
| Flexus 11 linear | External | Kemps Lighting |
| Glow Rail GR65 | External | The Light Lab |
| Look Bollard / 5 Cento | Landscape | Simes / Concord |
| LD51 spike mounted | Landscape | Light Graphix |
| 761 Atto Spot | Accent | Precision Lighting (Matthew Nourse) |
| Ultracob corner mini profile | Linear | Atea / Mesh Lighting |
| DALI Control System | All | Architainment Lighting |
| Track spot SP1 (QG46) / SP5 (EI67) | Galleries | Palco |

### AV Hardware (from AV BOQ v1.11 — DHD Services)

| Schedule Activity | Equipment | Brand/Model |
|---|---|---|
| PR4220 | Screens 43" | Samsung QH43C / LH43QHCEBGCXEN |
| PR4230 | Projectors | Panasonic PT-RZ6LW / PT-RZ7L + Epson EB-PU2116W / EB-PU2010W |
| PR4240 | Interactive Screens 13" | Beetronics 13TS7M |
| PR4250 | Screens 55" | Samsung VH55C-R / LH55VHCRBGBXEN |
| PR4260 | Interactive Screens 16" | Wacom Cintiq 16 / DTK-1660 |
| PR4270 | Audio Devices | Yamaha VXC6/VXS8 + XMV8140D amp + Monitor Audio W3M/W180 + Molitor induction loop |
| PR4280 | Screens 85" | Samsung QM85C + Iiyama ProLite LH8665UHSB-B1 86" |
| PR4290 | AV Racks | SY Wizard 4U / Middle Atlantic BGR + DVS Hydra4 PCs + SY Xcalibur 11 + Brightsign HD225/HD1025 + Q-Sys Core 510i + ZYXEL GS2220 + Aten CL6700WM |

### MEP Design Offers

| Company | Fee | Scope Type |
|---|---|---|
| AD Engineering | 171,500 SAR | Design review/verification only |
| BluHaus (TP Bennett) | ~717,440 SAR (lump sum) | Full MEP design + construction support |
| SG Group (v1) | USD 21,000 | Full MEP design |
| SG Group (v2) | USD 18,900 | Full MEP design |
