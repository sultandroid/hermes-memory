# Materials-to-Supplier Traceability — Schedule Audit Workflow

Extract named suppliers/brands from design documents and map them against Primavera P6 schedule procurement activities (Stage 3 — Specifications & Data Sheet Materials).

## When to Use

- User asks to audit a contractor schedule for materials with named suppliers
- Need to build a materials-to-brand traceability matrix from schedule + design docs
- Reviewing a Stage 3 / Material Submittals phase for completeness against design specifications

## Source Document Hierarchy

Extract brands in this order — each document type covers different materials:

| Priority | Document | What It Covers | Typical Location |
|----------|----------|---------------|------------------|
| 1 | **Finishes Schedule** (from exhibition design consultant) | Flooring, ceilings, wall finishes, fabrics, solid surfaces, paints, cladding — with supplier column | `Design Files/*/XX_AS_Pre-Appointment*Schedules*/Xcel/*Finishes_Schedule*.xlsx` |
| 2 | **Luminaire Specification** (from lighting designer) | All light fixture types (track spots, downlights, linear, external, controls) | `Design Files/*/07-Lighting Design*/Specifications/*Luminaire Specification*.pdf` |
| 3 | **AV BOQ** (from AV designer/contractor) | Screens, projectors, audio, media players, racks, control systems — make/model per item | `Design Files/*/06-AVHW*/AV BOQ/*av_boq*.xlsx` |
| 4 | **FF&E Schedule** (from interior/exhibition designer) | Furniture, loose FF&E — with supplier URLs | `Design Files/*/Schedules/*FF&E Schedule*.xlsx` |
| 5 | **Materials & Subcontractor Register** (contractor's procurement) | All materials with categories, some brand references in descriptions | `B.O.Q/Materials & Subcontractor Register (Master).xlsx` |
| 6 | **Floor Finishing Detail** (design specification) | Detailed tile/carpet specs with supplier name | `B.O.Q/Floor-Finishing-Material-Detail.xlsx` |
| 7 | **BOQ / Pricing Schedule** (commercial) | Confirms known brands, rarely adds new ones | `B.O.Q/*BOQ*.xlsx`, `*Pricing Schedule*.xlsx` |
| 8  | **Procurement Tracker** (contractor's log) | Some brand references in descriptions | `B.O.Q/Copy of Procurement Tracker.xlsx` |
| 9 | **AV Spec Sheets** (manufacturer datasheets) | Verifies exact model numbers | `*AVHW Spec Sheets/*.pdf` |

## Step-by-Step Workflow

### Step 1: Extract Stage 3 Activities from Schedule

From the Primavera P6 export (PDF or XER), identify all activities under the **Specifications & Data Sheet Materials** phase (typically 30-day duration, 0 float, labelled as "Stage 3" in procurement WBS).

For P6 PDF exports (multi-page Gantt charts):
- Read all 30-40 pages via pdftotext
- Extract block between the "Specifications & Data Sheet Materials" header and the next WBS header (Purchase Order, Material Delivery, etc.)
- Each row is: ID | Activity Name | Duration | Start | Finish | Float

### Step 2: Organize by Discipline

Group activities into:
- **Structural** — rebar, concrete, steel, waterproofing
- **Architectural** — finishes, ceilings, doors, custom elements (showcases, graphics, wayfinding, signage, FF&E, setworks)
- **Electrical** — lighting, CCTV, fire alarm, PAVA, access control, BMS, security
- **Mechanical** — ductwork, CHW piping, diffusers, dampers, FCUs, clean agent, sanitary
- **AV** — screens, projectors, interactive displays, audio, racks

### Step 3: Cross-Reference Each Discipline Against Design Docs

For each schedule activity, search the relevant design document for the material reference.

**Architectural Finishes:** Open Finishes Schedule Excel, search for material descriptions matching the schedule activity, read the Supplier column. Items marked "TBC Locally Sourced" have no design-stage supplier.

**Lighting:** Open Luminaire Specification PDF — each luminaire has a spec sheet. Extract manufacturer from description field. One schedule activity maps to 10+ luminaire types. Document all of them.

**AV Hardware:** Open AV BOQ Excel — each item has description + model number. Extract brand from item rows. Map to schedule activities by screen size/type.

### Step 4: Handle TBC Items

Items marked as "TBC Locally Sourced" in design docs — material type/color specified but no supplier. Contractor will source locally. Leave as TBC.

### Step 5: Identify Design-Stage vs Contractor-Proposed

| Category | Who Specifies Brand | Example |
|----------|-------------------|---------|
| Design-specified | Exhibition / lighting / AV / FF&E designer | iGuzzini, Ceramiche Piemme, Samsung, &Tradition |
| System-specified | Design team via Materials Register | Palco/iGuzzini/ECL Prolight track spots |
| Performance-specified | Design team via spec criteria | "Museum-grade LED, CRI>=90" |
| Contractor-proposed | Contractor chooses after award | MEP equipment, security systems |

### Step 6: Build the Traceability Matrix

Output to Excel with columns: #, Activity ID, Material/Product, Design Spec Ref, Supplier/Brand, Source Document, Submittal Start, Submittal End, Float, Critical.

Format: green fill for confirmed brands, red fill for critical-path items, bold for brand names, freeze panes, auto-filter.

### Step 7: Report Coverage Gaps

Report: X of Y items branded, Z items TBC grouped by discipline, which TBC items are design-stage vs contractor-procured, whether TBC affects critical path.

## Pitfalls

- Schedule activity names are generic — cross-reference design docs to find actual brands
- P6 exports never contain supplier names in activity fields
- Pricing BOQs confirm known brands but rarely add new ones
- Showcase fabricator is typically TBC at design stage
- MEP equipment brands are contractor-proposed (performance-specified)
- Security system brands TBC until AV specialist appointed
- Save output to 10_Plans/Schedule_Programme/ under project OneDrive — never Desktop
