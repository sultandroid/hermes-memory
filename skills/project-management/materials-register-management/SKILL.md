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
