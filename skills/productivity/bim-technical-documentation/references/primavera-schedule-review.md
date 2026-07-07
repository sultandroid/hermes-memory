# Primavera P6 Schedule Review — Workflow

Reviewing contractor-submitted Primavera P6 programme exports (PDF) for Samaya Technical Office.

## When to Use

- Contractor submits a P6 schedule export for review
- Need to assess baseline logic, critical path, float, and risks
- Producing a formal review report and/or schedule data extract

## Input

Primavera P6 PDF export (typically A3 landscape, multi-page Gantt chart with activity table). Not an XER or XLS — PDF only.

## Step 1 — PDF Extraction

```bash
# Get file info
pdfinfo "path/to/schedule.pdf"

# Extract text (layout mode preserves column alignment)
pdftotext -layout "path/to/schedule.pdf" /tmp/schedule.txt

# Check page count and size
wc -l /tmp/schedule.txt
```

## Step 2 — Read & Map Structure

Read the extracted text in sections (200 lines at a time via `read_file`). Map the WBS:

| WBS Level | Example | Duration |
|---|---|---|
| Project summary | Top row | 261d |
| Milestones | MS1000-1020 | — |
| Phase | Engineering | 237d |
| Sub-phase | Design work | 78d |
| Discipline | Structural / Architectural | 30d / 19d |
| Activity | EN1020 | 12d |

Key fields per activity: **ID, Name, Original Duration, Start, Finish, Total Float**.

## Step 3 — Analyze Phase by Phase

For each major WBS node, extract and assess:

### Critical path
- All activities with 0 float
- List them in sequence — the longest chain drives project completion
- Flag any 0-float chain with no contingency

### Float analysis
- 0 float = critical. 1–10d = tight. >20d = manageable.
- High-float items (>30d) indicate slack in that workstream — useful for resource reallocation

### Design phase deep-dive
- Check 50% / 90% / 100% IFC sequencing — do they overlap? If yes, flag rework risk
- Does 3D survey come before or after technical design starts?
- Are client-supplied items (content, copyrights, text) on the critical path with no client milestone?
- Is FLS (Fire Life Safety) integrated into or parallel to architectural design?
- Are specialized exhibition designs (showcase, AV, graphic, lighting) linked to base building design?

### Procurement / Materials
Four-stage procurement pattern in P6:
1. **Supplier Pre-Qualification** (select vendors)
2. **Supplier Approval** (approve selected)
3. **Specifications & Data Sheet Materials** (submit material samples/datasheets)
4. **Purchase Order** (place orders)

For Stage 3, identify materials where the design has specified a named product/brand (color codes, product-line names in quotes, custom items). Schedule entries are generic — **cross-reference with design schedules and BOQ for actual supplier names**. The P6 activity names will NOT carry brand names.

#### Cross-Referencing Design Schedules for Brand Data (Aseer Museum)

When the user asks for supplier/brand names against schedule materials, search these project folders:

| Source | Location | What It Contains |
|---|---|---|
| **Finishes Schedule** | `Design Files/Package_Part 2/03_AS_Pre Design Pack_250313/.../Xcel/6930_Finishes_Schedule_rev A.xlsx` | All finish materials with Supplier column: flooring, ceilings, wall finishes, fabrics, solid surfaces, HPL, paints — organized by Material ID |
| **FF&E Schedule** | Same folder: `6930_Aseer_FF&E Schedule.xlsx` | Furniture items with supplier URLs: &Tradition, Muuto, HAY, Studio Twenty Seven, Chaplins, Linie Design, Andreu World, Elefine Tech |
| **AV BOQ (DHD Services)** | `Design Files/Package_Part 2/06-AVHW + AV System Concept_rev A/6930_Aseer_av_boq_v1.11_CONCEPT_210225.xlsx` | AV hardware with make/model: Samsung screens, Yamaha audio, Panasonic/Epson projectors, Q-Sys control, Brightsign media players, SY racks |
| **AV Spec Sheets** | Same folder: `AVHW Spec Sheets/` folder | PDF datasheets for each branded AV component |
| **Materials Register** | `B.O.Q/Materials & Subcontractor Register (Master).xlsx` | Master list of 210+ materials with specs, standards, and some supplier references |
| **Floor Finishing Detail** | `B.O.Q/Floor-Finishing-Material-Detail.xlsx` | Consolidates floor finishes with supplier column (Ceramiche Piemme, Concept Tiles, Domus, Tarkett) |
| **Showcase Schedule** | Pre-Appointment Schedules Xcel folder: `6930_Aseer_Showcase Schedule.xlsx` | 534 showcase entries by gallery — types, dimensions, glass, locks, lighting specs |
| **Setwork Schedule** | Same folder: `6930_Aseer_Setwork Schedule_rev A.xlsx` | 255 entries — custom joinery, casework, walls per gallery |
| **Graphic Schedule** | Same folder: `6930_Aseer_Graphic Schedule_rev A.xlsx` | 250+ graphic elements — substrates (Viroc, Duratran, GF Smith paper, brass), print methods |
| **Media Schedule (PDF)** | `PDFs/6930_Aseer_Media Schedule.pdf` | AV content narrative per gallery — describes what each screen/projector/audio system does; does NOT name hardware brands |
| **Lighting Design / Luminaire Spec R2** | `Design Files/01_AS_Pre-Appointment Exhibition Documentation_250313/07-Lighting Design_rev A/Specifications & Schedules/ZNA3297_ARM_SP_01_01 Luminaire Specification R2.pdf` | Complete luminaire schedule by ZNA Lighting Design — 30+ pages with manufacturer, model, CRI, IP rating, control protocol for every fitting. Key brands: iGuzzini Laser Blade, Intra Lighting Kalis T55, Flos Kap 105 + Bon Jour, Kemps Flexus 11, Precision Lighting 761 Atto Spot, Atea/Mesh Ultracob, The Light Lab Glow Rail, Simes/Concord Look Bollard + 5 Cento, Light Graphix LD51, Architainment DALI control |

#### Extraction workflow for brand data:

1. **Read the P6 schedule** — extract all activity names from Stage 3 (Specifications & Data Sheet Materials)
2. **Map to Material IDs** — match the schedule description to the Finishes Schedule Material IDs (FI_FL_XX, FI_CL_XX, etc.) by searching the `Material Description` column
3. **Look up Supplier** — extract the `Supplier` column from the Finishes Schedule row
4. **For AV items** — open the AV BOQ Excel (`6930_Aseer_av_boq_v1.11_CONCEPT_210225.xlsx`), search by equipment type (Screens 43, Projectors, etc.) to find the make/model. Be precise: distinguish between touch screen monitors (Beetronics), pen displays (Wacom), and control touch screens (Q-Sys). Check the Item Description column, not just the category header.
5. **For lighting items** — the P6 schedule treats all lighting as one submittal (PR3800). The Materials Register breaks it into 7 categories (EL-MAT-01 to EL-MAT-07). For actual manufacturer names, open the ZNA Luminaire Specification R2 PDF in `07-Lighting Design_rev A/Specifications & Schedules/`. Each luminaire type has a dedicated sheet with MANUFACTURER / SUPPLIER field.
6. **For FF&E** — open the FF&E Schedule, search by space/description for the supplier URL
7. **For items not found** — mark as TBC and note which document to check next
8. **Write to Excel** — create a clean extract with columns: #, Activity ID, Material/Product, Design Spec/Ref, Supplier/Brand, Source Document, Submittal Start, End, Float, Critical. Highlight 0-float rows in red, brand-identified cells in green.

#### AV brand mapping — common pitfall

The AV BOQ lists multiple types of touch screens. Match carefully:

| P6 Activity | AV BOQ Description | Correct Brand | Don't Confuse With |
|---|---|---|---|
| Interactive Screens 13" | Touch Screen Monitor 13" | Beetronics 13TS7M | Q-Sys TSC-50-G3 (5" control touch screen) |
| Interactive Screens 16" | Pen Display 16" | Wacom Cintiq 16 / DTK-1660 | Q-Sys or other control panels |
| AV Racks | Rack + PC + Media Player | SY Wizard 4U + DVS 4U Hydra4 + Brightsign | Don't list as a single item — it's an assembly |
| Audio | Speakers + Amp + Induction | Yamaha VXC6/VXS8 + XMV8140D + Monitor Audio in-wall + Molitor induction loop | Don't list only one component |

Rule: **search the AV BOQ Item Description column** for the exact size/spec from the P6 activity name. Don't guess based on category alone — a "13\" touch screen" in the schedule is NOT the same as a 5\" Q-Sys control panel even though both are touch-enabled.

### Construction
- Floor-by-floor sequencing — check for concurrency (are all floors starting within days of each other?)
- Resource loading — P6 PDF exports rarely include this. Flag as a gap.
- Look for demolition-to-assessment gap — if assessment was done months before demolition starts, conditions may have changed.

### Testing & Handover
- Check float on TOC milestone — zero float to project completion is a critical risk
- Verify COBie/BIM handover milestones are early enough to accumulate data progressively
- Check for missing system testing (IT/network often omitted)

## Step 4 — Formal Review Document

Create an HTML review report with:

1. **Cover page** — dark navy, doc ref (TO-ASEER-SCH-RVW-NNN), project name, revision, date, prepared by
2. **Executive Summary** — severity count cards (High/Med/Low), recommendation box
3. **Findings table** — each finding with ref ID, severity badge, observation, requirement, reference
4. **Assessment table** — per-aspect rating (Satisfactory / Caution / Not Adequate)
5. **Conclusion & Recommendation** — qualified acceptance or reject with conditions
6. **Distribution list**

HTML classes to use: `.rtable`, `.badge-high/med/low`, `.summary-grid`, `.s-card`, `.rec-box`, `.pg-footer`.

**Save directly to:** `10_Plans/Schedule_Programme/TO-ASEER-SCH-RVW-NNN_Title.html`

## Step 5 — Excel Data Extract (when requested)

If user asks for material/supplier data as Excel:

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = openpyxl.Workbook()
ws = wb.active
# Headers: #, Activity ID, Discipline, Material/Product, Design Specification, Submittal Start, Submittal End, Float, Critical
# Highlight 0-float rows in red fill
# Freeze header row, add auto-filter
```

**Save to:** same `Schedule_Programme/` folder with descriptive filename.

## Step 6 — Output Location Rules

| Deliverable | Folder |
|---|---|
| Schedule review report (HTML) | `10_Plans/Schedule_Programme/` |
| Excel extract | `10_Plans/Schedule_Programme/` |
| PDF version | `10_Plans/Schedule_Programme/` |
| Correspondence letter | `09_Correspondence/YYYY-MM/` |

**Never save to Desktop.** Always use the OneDrive project path:
`~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/10_Plans/Schedule_Programme/`

## Doc Ref Convention

```
TO-ASEER-SCH-RVW-NNN
```

Where NNN = sequential number. TO = Technical Office, ASEER = project, SCH = schedule, RVW = review.

## User Interaction Pattern

Mohamed (Tech Office Manager) prefers **iterative drilling**:
1. Start with a broad audit of the full schedule
2. He'll ask for specific phase deep-dives (design, procurement, construction)
3. Then for specific data extracts (materials, suppliers, dates)
4. Deliverables go directly to OneDrive path — never ask "where should I save this"

Respond concisely. Don't explain the project back to him — he knows it intimately.
