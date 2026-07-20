---
name: materials-register-management
title: Materials Register Management
description: Create, maintain, and analyze comprehensive materials registers for construction/museum fit-out projects. Extract from NRS schedules, track ~100+ materials across categories, produce Excel deliverables for procurement, prioritize by critical path.
trigger: user asks to create a materials register, track material submittals, list approved materials/brands from design schedules, or analyze material procurement status
tags: [materials, register, procurement, finishes, schedule, aseer, excel, openpyxl]
---

# Materials Register Management

## When to Use

- User asks to "list approved materials and brands" from design schedules
- User asks to create a materials register or tracker
- Need to analyze material procurement status vs project requirements
- Need to produce an Excel deliverable for the procurement team
- User says "only two materials?" — indicating a gap analysis is needed

## Source Data

The primary source for specified materials in museum fit-out projects is the **NRS (or equivalent designer) Finishes Schedule** — typically named `6930_Finishes_Schedule_rev A.xlsx` or similar. Other schedules that contain material specs:

| Schedule | What it contains |
|----------|-----------------|
| Finishes Schedule | Flooring, ceilings, walls, stone, glass, wood, metal, fabric, solid surface, composites, graphic substrates, lighting |
| Setwork Schedule | Materials used in custom setworks (brass, fabric, wood, lightboxes) — references Finishes IDs |
| Showcase Schedule | Showcase-specific materials (glass, Corian, powder coated steel, fabric backing) |
| FF&E Schedule | Furniture brands, finishes, upholstery fabrics |
| AV Equipment Schedule | Brand-name AV hardware (Q-Sys, Yamaha, Epson, Samsung) |

## Workflow

### Step 1: Locate Source Schedules

Check these locations in order:
1. External drive: `/Volumes/MIcro/Work/Aseer-Museum/03_AS_Pre-Appointment Exhibition Schedules_250313/PDFs/` and `Xcel/`
2. OneDrive BIM path: `05_BOQ/` or `04_Submittals/`
3. Project repo: `99_Archive/02_Scope_Management/`

The schedules are typically `.md` (converted from PDF) and `.xlsx` files. Read the `.md` versions for text extraction.

### Step 2: Extract Materials by Category

Read the Finishes Schedule markdown file. It has a tabular format with columns:

```
Material ID | Exhibition Element Component | Material Description | Treatment/Finish | Colour | Supplier | Oddy Testing
```

Extract each row into a structured list by category (FLOORING, CEILINGS, WALLS, STONE, GLASS, WOOD, METAL, FABRIC, SOLID SURFACE, COMPOSITES, GRAPHIC SUBSTRATES, LIGHTING).

**Key fields to capture per material:**
- MA Ref (assign sequentially: MA-0007, MA-0008, etc.)
- Material name
- Finishes ID (FI_FL_01, FI_ME_01, etc.)
- Brand / Supplier
- Colour / Finish
- Location / where used
- Oddy test required (🧪)
- Sample required
- Lead time (estimate from material type)
- Procurement responsibility (Samaya / GBH / Rawasin / Subcon)
- Status: ✅ Approved / ⏳ In Prep / 🔴 Not Started

### Step 3: Cross-Reference with Other Schedules

- **Setwork Schedule** — identifies which Finishes IDs are used in setworks (e.g., FI_ME_01 Patinated Brass appears in every gallery)
- **Showcase Schedule** — identifies showcase-specific materials (anti-reflective glass, Corian plinths, fabric backboards)
- **FF&E Schedule** — identifies furniture brands and upholstery fabrics
- **AV Equipment Schedule** — identifies brand-name AV hardware

### Step 4: Build the Register

Create a markdown file at `01_Registers/materials_register.md` with:

**Header:** YAML frontmatter (last_updated, owner_agent, status, source)

**Sections by category** (each with a table):

| MA Ref | Material | Finishes ID | Brand / Supplier | Colour / Finish | Location | Oddy | Sample | Lead Time | Procurement By | Status | CG Resp | Notes |

**Summary table at the end:**

| Category | Total | Submitted | Approved | In Prep | Not Started |

### Step 5: Create Excel Deliverable

Use openpyxl to create a formatted Excel file at `01_Registers/materials_register.xlsx`:

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Styles
hdr_font = Font(name='Calibri', bold=True, size=10, color='FFFFFF')
hdr_fill = PatternFill(start_color='1F3864', end_color='1F3864', fill_type='solid')
cat_font = Font(name='Calibri', bold=True, size=10, color='1F3864')
cat_fill = PatternFill(start_color='D6E4F0', end_color='D6E4F0', fill_type='solid')
body_font = Font(name='Calibri', size=9)

# Status colors
green_fill = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')  # Approved
amber_fill = PatternFill(start_color='FFEB9C', end_color='FFEB9C', fill_type='solid')  # In Prep
red_fill = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')     # Not Started
```

**Two sheets:**
1. **Materials Register** — full data with category bands and color-coded status
2. **Summary** — category totals

**Formatting rules:**
- Navy headers (`#1F3864`), white text
- Category bands in light blue (`#D6E4F0`)
- Status column color-coded (green/amber/red)
- Frozen header row
- Column widths set for readability
- Wrapped text for long descriptions

### Step 6: Priority Analysis

Flag critical path items:

| Priority | Criteria | Examples |
|----------|----------|----------|
| **P1** | Long lead time, fabrication dependency, large area | Corian (GBH dependency), anti-reflective glass, Kvadrat fabrics, Ceramiche Piemme tiles, Asona/Knauf ceilings |
| **P2** | Medium lead, affects finishes but not fabrication | Paint, wood veneer, composites, graphic substrates |
| **P3** | Short lead, can be ordered later | FF&E furniture, lighting fixtures (pending ZNA design) |

### Step 7: Update the Submittal Register

Add the materials register entries to `01_Registers/submittal_register.md` under the **In Preparation** section:

```
| MOC-MUS-ASE-1A0-MA-0008 | Metal SS PVD Coated Patinated Brass Effect — SAM-FIN-SS-002 | Materials | **In Preparation** | ... |
```

## Cross-Register Material Submittal Pipeline Audit

When the user asks to "track" materials submittals and prequalifications, the answer spans **four registers** that must be cross-referenced:

| Register | File | What it tracks |
|----------|------|----------------|
| Material Submittal (MA) | `01_Registers/material_submittal_register.md` | Material submittals submitted to CG, with codes |
| Prequalification (PQ) | `01_Registers/prequalification_register.md` | Supplier/vendor prequalifications, with codes |
| Compliance Gaps | `Technical_Office/Compliance_System/compliance_gaps.md` | Gaps between approved PQs and missing MAs |
| Risk Register | `01_Registers/risk_register.md` | Formal risks with PxS scoring and treatment plans |

### Audit Workflow

1. **Read all four registers** to get the full picture
2. **Identify materials with no MA submission** — cross-reference the MA register against the Finishes Schedule. Materials specified in design but not in the MA register are "not yet submitted."
3. **Identify PQs with no corresponding MA** — a supplier may be prequalified (PQ Code B) but the material submittal (MA) may not have been made yet. This is a compliance gap.
4. **Identify compliance gaps not in the risk register** — each open gap should have a corresponding risk ID. If not, create one.
5. **Report the consolidated picture** — use a table like:

| Status | Count | Details |
|--------|-------|---------|
| MA submitted, Code B | N | Approved w/ comments |
| MA submitted, Code C/D | N | Needs resubmission |
| PQ approved, no MA | N | Compliance gap — submit MA |
| No PQ, no MA | N | Need to source + PQ + MA |
| Not yet in any pipeline | N | From design schedule, not started |

### Common Findings Pattern

| Finding | Action |
|---------|--------|
| MA-0006/0007 Code C with outstanding conditions | Build resubmission support folder; decouple look-and-feel from certifications |
| PQ approved (Code B) but no MA submitted | Create compliance gap; submit MA per spec |
| Material in design schedule but no PQ or MA | Add to procurement pipeline; assign MA ref |
| Compliance gap exists but no risk ID | Create new risk (PRR-PRC-08 style) with treatment plan |
| Risk exists but no treatment plan | Create treatment file in `03_Plans/08_Risk/treatment/` |

### Pitfall — MA Register is Sparse

The MA register typically has only 8-10 entries while the design schedule specifies 100+ materials. This is normal for early stages — most materials haven't entered the submittal pipeline yet. The audit should distinguish between:
- **Materials that should have been submitted** (critical path, long lead, CG-chasing) — flag as risk
- **Materials that are not yet due** (per programme) — note but don't flag
- **Materials with no procurement path at all** (no supplier identified, no PQ) — flag as critical gap

### Pitfall — Prequalification Register Has 125+ Entries

The PQ register is large (110+ from old log + 15+ recent). Most are historical (Jan-Jun 2026). The active PQs to watch are the recent ones (PQ-0100 onwards) under the current `MOC-MUS-ASE-` prefix. Filter by:
- Status = U (Under Review) — actively pending
- Status = C (Revise & Resubmit) — needs action
- Recent date (Jul 2026+) — current pipeline

## Supplier Technical Datasheet Risk Analysis

Supplier datasheets contain risk signals that are easy to miss but critical for museum-grade materials. When a supplier submits a datasheet, analyze it for disclaimers before relying on it for CG submission or procurement.

### What to extract from every datasheet

| Signal | What to look for | Risk implication |
|--------|-----------------|------------------|
| **"Random" or "varying" finish disclaimer** | "Randomly generated surface finish", "final result will differ from sample" | Sample approval is meaningless — production units will differ. CG may reject as-delivered finish. |
| **Variation exclusion clause** | "Color variations within a single piece and from batch to batch do not constitute grounds for complaint" | Supplier explicitly disclaims liability. If finish is rejected, you have no recourse. |
| **Complaint limitation** | "Final appearance is not a basis for subsequent complaints" | **Red flag.** The datasheet is a legal document stating the supplier will not accept returns or claims for appearance. |
| **Process type** | "Chemically darkened", "hand-applied patina", "batch process" vs "production line" | Batch chemical processes have higher variability than production-line automation. Oddy testing one batch does not guarantee the next. |
| **Clear coat / sealant type** | "Clear coat sealed", "lacquer", "wax" | Affects Oddy test parameters, VOC emissions, and long-term durability. Verify all coating materials also pass Oddy. |

### How to connect datasheet findings to project risks

| Datasheet finding | Risk to create/update | Example |
|---|---|---|
| Supplier disclaims appearance variation | **Finish matching risk** — same material on multiple applications will vary batch-to-batch | EDEN-DESIGN CD/CC patinated brass on showcases (Glasbau Hahn), doors, cladding → each application will differ |
| Batch chemical process (not production line) | **Oddy testing risk** — one batch passes, next may not. Re-test cycle is 3-4 months. | EDEN CD/CC: chemically darkened non-ferrous metal. Each batch = unique chemical reaction. |
| Single supplier named across multiple trades | **Supply concentration risk** — if that supplier fails or can't scale, all trades affected | Single German patination source serving showcase, doors, cladding |
| Supplier explicit disclaimer language | **CG rejection risk** — CG will reject a material whose own datasheet says "final result will differ from sample" | EDEN datasheet: "final appearance is not a basis for subsequent complaints" |

### The "Look and Feel First" Strategy

When a material submittal is rejected (Code C) because certifications are missing but visual/functional properties are acceptable:

1. **Request CG to approve LOOK AND FEEL** (visual appearance, colour, texture) of the submitted sample **now**
2. **Pursue test reports in parallel** (Oddy, fire, VOC, off-gassing, MSDS, chemical composition)
3. **Develop alternatives in parallel** — e.g., PVD-coated sample from local KSA suppliers as risk mitigation
4. **Document risk to CG** — explicitly state that batch variation is inherent (citing the datasheet), so look-and-feel approval covers a representative range, not exact match

This decouples aesthetic approval (CG decides immediately) from technical certification (takes weeks/months).

### Workflow

1. Extract datasheet text with `pdftotext`
2. Search for: "random", "vary", "batch", "not a basis", "complaint", "differ", "sample", "chemical"
3. If disclaimers found, flag the material row with ⚠️ in Notes
4. Add risk to DDR (under relevant discipline — Showcase, Metal, Finish)
5. Escalate to Procurement Manager (07) and Materials Manager (06) lanes
6. Disclose variation risk explicitly in CG submission — never hide supplier disclaimers

### Reference file

See `references/patinated-brass-datasheet-eden-analysis.md` for a worked example of EDEN-DESIGN patinated brass datasheet analysis.

## Submittal Statement Format (to CG)

Keep statements **very short** — the user explicitly rejected verbose framing. Pattern:

> **Submittal Statement — [Supplier] [Equipment] Prequalification Package**
>
> This prequalification is for the **[purpose]** to the Aseer Museum [system], in compliance with the approved project specifications. Equipment types and technical specs match the approved design.
>
> **Details:**
> - Supplier: [Name] ([role])
> - Contractor: [Main contractor]
> - Proposed Ref: MOC-MUS-ASE-1K0-PQ-NNNN
>
> **Provided files:**
> [numbered list]

No explanation, no context paragraph, no quantity variance notes. Just the statement and the file list.

## Pitfalls

- **Only 2 materials submitted out of ~110+** is the typical starting state — don't be alarmed, this is normal for Stage 4
- **~35 items marked "TBC Locally Sourced"** need local supplier identification (stone, glass, paint, some flooring)
- **Oddy testing is a museum-specific requirement** — materials inside showcases (glass, fabric, powder coated steel) need museum-grade Oddy testing before approval
- **GBH fabrication dependencies** — Corian plinths and anti-reflective glass are on GBH's critical path; delays here delay showcase production
- **Kvadrat fabrics** are all branded and need Oddy testing for 2 of 9 items — order samples early
- **Do NOT copy binary files to the repo** — the Excel is a working tool for procurement, the markdown is the repo source of truth
- **The finishes schedule may have "Removed Items" and "Added Items" columns** — check for these to understand scope changes between revisions
- **FF&E brands are mostly European** — &Tradition, Muuto, HAY, Kvadrat — lead times 8-12 weeks, order early

## Resubmission Support Folder Pattern

When a material submittal is rejected (Code C) and the supplier has already provided a technical rebuttal, build a structured support folder for the Rev.01 resubmission.

### Folder structure

```
MA-NNNN_Rev01_Support/
├── 01_CG_Rejection/              CG rejection letter (original)
├── 02_Supplier_Reply/             Supplier's comments reply sheet
├── 03_Manufacturer_Datasheet/     Manufacturer technical datasheet (e.g. Guardian Clarity)
├── 04_Technical_Data_Sheets/      All supplier data sheets (Corian, fabric, silicone, etc.)
├── 05_PQ_Approval/                Original prequalification approval
├── 06_Sample_Board/               Sample board photo
├── 07_Related_Submittal_Support/  Cross-referenced materials (e.g. brass patination for MA-0007)
├── 08_Email_Thread/               Full email chain (Samaya → Supplier → NRS)
└── 09_Checklist/                  What's ready vs what's still missing
```

### When to build

- CG returns Code C with specific technical complaints
- Supplier has already replied with technical justification (check Outlook email attachments)
- The rejection is about material compliance, not supplier qualification
- You need to demonstrate to CG that the technical issue is resolved

### Email attachment extraction for supplier replies

When checking if a supplier replied to a CG rejection:

1. Search Outlook SQLite for the submittal ref (MA-NNNN) in subject lines
2. Filter by sender — the supplier's project manager (e.g. Ahmed Metwally@glasbau-hahn.de)
3. Extract attachments via AppleScript osascript (see outlook-email skill)
4. Read with pdftotext — supplier reply sheets often contain verbatim technical rebuttals
5. Cross-reference the supplier's claims against the CG's rejection points
6. Build the support folder with the supplier's reply as the centrepiece

### Key argument pattern

When the supplier has already proven technical compliance but CG demanded "3 alternative suppliers":

- The "3 suppliers" demand was based on the initial non-compliant submission
- Since technical compliance is now proven (supplier datasheet + comments reply), request CG to accept single supplier with technical justification
- If CG insists, then source 3 alternatives — but the supplier's existing reply is the strongest negotiating position

### Checklist items for any resubmission

- [ ] Conservation test certificates for ALL internal materials (PQ condition)
- [ ] Integration shop drawings (HVAC/electrical/humidity)
- [ ] Approved samples of contested materials
- [ ] Preventive maintenance plan + spare parts
- [ ] Full-scale on-site mock-up commitment
- [ ] On-site technical team confirmation
- [ ] SI compliance statement (if SI was cited in rejection)
- [ ] Designer (NRS) stamp confirmation on drawings
- [ ] Cover letter to CG: "Rev.01 resubmission addressing all comments"
