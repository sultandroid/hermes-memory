# NRS Exhibition Schedules — Inventory & Data Guide

## Location

`Design Files/Package_Part 2/03_AS_Pre Design Pack_250313/03_AS_Pre-Appointment Exhibition Schedules_250313/`

Subfolders: `Xcel/` (source Excel), `PDFs/` (issued PDFs + verification MDs)

## Schedule Files (21 total)

| File | Items | Key Columns | Purpose |
|------|-------|-------------|---------|
| `6930_Finishes_Schedule_rev A.xlsx` | 84 | Material ID, Exhibition Element Component, Material Description, Treatment/Finish, Colour, Supplier, Oddy Testing | Floor/wall/ceiling/stone/glass/wood/metal/fabric/solid surface/composites/graphic substrates/planting/lighting |
| `6930_Aseer_FF&E Schedule.xlsx` | 43 | FF&E ID, Space Name, Existing Design, Bespoke Dimensions, FF&E Replacement, Supplier (URL), Finish | Furniture, fixtures, equipment — procurement-ready with supplier URLs |
| `6930_Aseer_Setwork Schedule_rev A.xlsx` | 255 | Setwork ID, Exhibition ID, Exhibit Name, Type, Description, Finishes, Drawing Code Ref | Joinery/setworks — wayfinding housings, graphic housings, AVHW housings, benches, display units |
| `6930_Aseer_Showcase Schedule.xlsx` | 534 | Showcase ID, Exhibit Number, Showcase Type, Ext/Int dims, Glass Thickness, AR Coating, Climate Control, AER, Lock Type, Lighting Level | Conservation-grade display cases — 11.5mm AR glass, RH 40-60%, museum-grade locks |
| `6930_Aseer_AV_Equipment Schedule` (JSON) | 178 | code, description, product, qty, zone, category, voltage | Audio (Yamaha), video, projection, Dante network, PAVA |
| `6930_Aseer_Lighting Schedule` (JSON) | 119 | code, fixture_type, description, manufacturer, lamp_type, wattage, CRI, CCT, lumens, dimming, control_zone | iGuzzini spotlights & track, custom light boxes (Unibox), DALI control |
| `6930_Aseer_Space and Gallery Schedule.xlsx` | — | Gallery ID, Gallery Name, Floor, Area | Space allocation per gallery |
| `6930_Aseer_Wayfinding Schedule.xlsx` | — | — | Wayfinding signage types & locations |
| `6930_Aseer_Tactile & Manual Interactives Schedule.xlsx` | — | — | Tactile exhibit interactives |
| `6930_Aseer_Object Schedule.xlsx` | — | Object ID, Exhibit, Description | Museum objects per exhibit |
| `6930_Aseer_Exhibit Schedule.xlsx` | — | Exhibit ID, Gallery, Name | Exhibit catalog |
| `6930_Aseer_Model & Replica Schedule.xlsx` | — | — | Physical models & replicas |
| `6930_Aseer_Mockups and Prototypes Schedule.xlsx` | — | — | Mockup & prototype specs |
| `6930_Aseer_Graphic Schedule_rev A.xlsx` | — | — | Graphic panels & signage content |
| `6930_Aseer_Art Commission Schedule.xlsx` | — | AC ID, Artist, Title, Media, Dimensions | Contemporary art commissions |
| `6930_Aseer_Media Schedule.xlsx` | — | — | AV media content per exhibit |
| `6930_Aseer_Asset Schedule.xlsx` | — | — | Asset tracking |
| `6930_Aseer_Tactile & Manual Interactives Schedule.xlsx` | — | — | Tactile exhibits |

## Finishes Schedule — Categories & Named Suppliers (16)

| Category | Items | Named Suppliers |
|----------|-------|-----------------|
| Flooring (FI_FL) | 14 | Ceramiche Piemme, Concept Tiles, Domus, Tarkett |
| Ceilings (FI_CL) | 8 | Asona, Knauf, Fermacell/British Gypsum, Kvadrat |
| Walls (FI_WA) | 10 | Domus (rest TBC Locally Sourced) |
| Stone (FI_ST) | 4 | Existing (granite), TBC Locally Sourced |
| Glass (FI_GL) | 4 | TBC Locally Sourced |
| Wood (FI_WO) | 3 | ARPA |
| Metal (FI_ME) | 5 | TBC Locally Sourced |
| Fabric (FI_FA) | 10 | Kvadrat (Remix 3, Hallingdal 65, Volume) |
| Solid Surface (FI_SS) | 5 | Corian, Hi Macs, Smile Plastics |
| Composites (FI_CO) | 6 | Valchromat, Viroc, Clay-works |
| Graphic Substrates (FI_GR) | 13 | GF Smith, Viroc |
| Planting (FI_PL) | 1 | TBC Locally Sourced |
| Lighting (FI_LI) | 2 | TBC Locally Sourced (Perspex) |

## FF&E Suppliers (by URL domain)

| Brand | URL Domain | Product Types |
|-------|-----------|---------------|
| &Tradition | andtradition.com | Loafer chairs/sofas, In-between chairs |
| Chaplins | chaplins.co.uk | Tradition Loafer dining chairs, sofas |
| HAY | hay.com | Palissade outdoor lounge, Neu table |
| Muuto | muuto.com | Cover Armchair |
| Andreu World | andreuworld.com | Sand chairs, tables |
| Studio Twenty Seven | studiotwentyseven.com | Andrill table (walnut) |
| Linie Design | liniedesign.com | Halo, Lucens rugs |
| Kvadrat | kvadrat.dk | Allround curtains |
| Elefine Tech | elefinetech.com | X-ray luggage scanner |

## Showcase Key Specs

- Glass: 11.5mm, anti-reflective coating (all cases)
- Climate: RH 40-60%, Air Exchange Rate 0.1
- Locks: Museum Grade High Security × 2
- Case Ratings: 2P (most), some 1P
- Lighting: 50 lux (gallery standard), integral lighting per case
- Types: Type 1–6B (various configurations)

## Setwork Key Materials

- Patinated brass (wayfinding housings, graphic housings, AVHW totems, benches, security desks)
- Dark wood (benches, children's stools)
- Viroc composite (desks, tables, till desks)
- Solid surface (tables, plinths)
- Natural concrete (plinths with integrated lighting)

## Reading Notes

- Excel files use openpyxl: `openpyxl.load_workbook(path, data_only=True)`
- Finishes schedule header is at row 5 (Material ID, Exhibition Element Component, Material Description, Treatment/Finish, Colour, Supplier, Oddy Testing)
- Category headers are in column A, all-caps without underscore (FLOORING, CEILINGS, etc.)
- Data rows start at row 6, IDs prefixed `FI_` + category code (FL, CL, WA, ST, GL, WO, ME, FA, SS, CO, GR, PL, LI)
- JSON versions at `Completed Tender Package From NRS/07_Visualizations/Kimi_Agent_Interactive 3D Material Showcase/app/src/data/schedules/` — same data, JSON format
- JSON keys use Title Case (Material Description, Treatment/Finish) while materials.json uses lowercase — always verify keys against the source
