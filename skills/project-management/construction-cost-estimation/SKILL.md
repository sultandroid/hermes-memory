---
name: construction-cost-estimation
description: "Build construction cost estimates and pricing plans from BOQ, design docs, and BIM/IFC models. Covers steel quantity takeoff from Tekla IFC, Excel costing sheets with clean formulas, Riyadh market rate application, and cost-per-m² build-up."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [cost-estimation, construction, quantity-takeoff, ifc, bim, pricing, samaya, moqtana]
    related_skills: [samaya-technical-office, odoo, project-deliverable-audit]
---

# Construction Cost Estimation Workflow

## When to Use
- Building a cost estimate / pricing plan from a BOQ or scope document
- Comparing structural design options (e.g., containers vs steel frame)
- Extracting steel tonnage from BIM/IFC models for pricing
- Building Excel-based costing sheets with market rates

## Workflow

### 1. Understand the Project Structure

Navigate to the project directory and read key documents:

```
cd ~/OneDrive/Work/PWork/01_PROJECTS/<Program>/<Project>/
```

Look for:
- **ER / SOW** — contract scope documents (typically in `00_Admin/Contracts/`)
- **BOQ** — bill of quantities (typically `08_Schedules/` or named `.xlsx`)
- **Design drawings / calculations** — for structural details (`03_Design/`)
- **BIM / IFC models** — for quantity takeoff (`03_Design/.../06-IFC/`)

### 2. Categorize BOQ Items into Work Packages

Group BOQ items into logical packages:
- **Steel & Structural Works** — frames, columns, beams, bracing, concrete, foundations
- **Facade Works** — glazing, doors, cladding, signage
- **MEP Works** — HVAC, electrical, low current, fire protection, plumbing
- **Interior Finishes & Fit-Out** — flooring, walls, ceilings, joinery, FF&E, sanitary

### 3. Extract Steel Quantities from IFC/Tekla Model

When the design calculations PDF contains SAP2000 screenshots (unreadable by OCR), use the IFC file instead:

**IFC file location:** `03_Design/<model>/06-IFC/IFC.ifc`
**IFC format:** STEP physical file (ISO-10303-21), text-based

1. Parse the IFC file to count entities by type:
   - `IFCCOLUMN` = columns
   - `IFCBEAM` = beams/members
   - `IFCMEMBER` = bracing/secondary
   - `IFCPLATE` = plates

2. Extract profile names from the Tekla IFC format:
   ```
   #123= IFCCOLUMN('...',$,'STANCHION','HEA220',$,...)
   ```
   The 4th quoted string is the profile name (Tekla internal name matches standard: HEA220, IPE240, IPE220, UPN180, RSA60×60×6, etc.)

3. Count occurrences per profile:
   ```python
   import re
   from collections import Counter
   counts = Counter()
   for m in re.finditer(r'#\d+= IFCBEAM\(', content):
       text = content[m.end():m.end()+500]
       quotes = re.findall(r"'([^']*)'", text)
       profile = quotes[2]  # 3rd quoted string = profile name
       counts[profile] += 1
   ```

4. Calculate weight:
   - Look up standard kg/m for each profile
   - Estimate average length from building dimensions (grid spacing, floor heights)
   - Weight = count × avg length × kg/m

**Standard section weights:**
| Profile | kg/m |
|---------|------|
| HEA220 | 50.1 |
| IPE240 | 30.7 |
| IPE220 | 26.2 |
| UPN180 | 22.8 |
| RSA60×60×6 | 5.42 |
| SHS70×4 | 7.52 |
| TUBE50×3 | 3.48 |
| TUBE30×2 | 1.38 |
| PL300×6 | 14.13 |

### 4. Build Excel Costing Plan

**Tool:** openpyxl

**Sheet structure per package:**
- Row 1: Title
- Row 3: Column headers (#, Item, Description, Qty, Unit, Unit Rate SAR, Total SAR, Notes)
- Row 4+: Data items
- Grand Total row at bottom

**CRITICAL — Formula structure (avoid double-counting):**

```python
# ✓ CORRECT: Simple SUM of only item rows
ws.cell(row=grand_row, column=7).value = "=SUM(G5:G{last_item})"

# ✗ WRONG: SUMIF > 0 (includes subtotal rows, doubles the total)
ws.cell(row=grand_row, column=7).value = "=SUMIF(G4:G{row-1},\">0\")"  # BAD
```

**Never add subtotal rows** between items and grand total. If you want subgroups, use subheader rows (no formula, no value in column G) between item groups. The grand total formula must be a plain `=SUM(Gfirst:Glast)` covering only item rows.

### 5. Apply Riyadh Market Rates

Use current Riyadh construction market averages:

| Item | Rate (SAR) | Unit |
|------|-----------|------|
| Fabricated structural steel (incl. marine coating) | 10,000 | /ton |
| RMC K350 ready-mix concrete (pump + labor) | 600-650 | /m³ |
| Rebar | 3,500 | /ton |
| SS316 handrails installed | 1,000 | /lm |
| PWD ramps concrete + finish + rails | 2,000 | /m² |
| Auto sliding door 386cm | 24,000 | /nos |
| Auto sliding door 200cm | 16,000 | /nos |
| DG 6/12/6mm glass façade installed | 1,350 | /m² |
| GRC cladding installed | 950 | /m² |
| Illuminated acrylic lettering | 2,000 | /lm |
| Packaged AC 5-ton installed | 22,000 | /nos |
| 220V outlet Legrand Arteor | 420 | /nos |
| LVT vinyl flooring installed | 145 | /m² |
| Gypsum board partition | 120 | /m² |
| Paint full system (Jotun) | 45 | /m² |
| Gypsum ceiling | 135 | /m² |
| Rockwool 100mm | 80 | /m² |

### 6. Scale for Design Alternatives

When comparing structural options with different built-up areas, scale non-structural packages by area ratio:

```python
SCALE = new_built_up_m2 / baseline_built_up_m2
```

### 7. Calculate Cost per m²

```python
cost_per_m2 = grand_total / total_built_up_m2
```

Always state whether the figure is excl. or incl. VAT (15%).

## Cover Page Structure

For each costing plan option, include a Cover Page with:
1. Project name and contract reference
2. Building data (footprint, storeys, total built-up area)
3. Steel weight breakdown (component × profile × length × kg/m = total kg)
4. Package cost summary table
5. Grand total excl. VAT
6. Cost per m²
7. VAT calculation
8. Comparison table (if multiple options)
9. All assumptions listed

## Additional Steel Tonnage Methodology

### For Container-Based Structures
When the project uses shipping containers (absorbed from `project-costing`):
- **40ft HC container tare weight**: ~3,900 kg each (industry standard)
- **Reinforcement**: W8×31 I-beams at 46.1 kg/m for clear-span openings
- **Cladding**: steel sheet weight = area (m²) × thickness (m) × 7,850 kg/m³
- **Staircase**: ~2,500 kg for external 2-storey steel stair
- **Connections/bolts/anchors**: ~1,800 kg allowance

### Steel Frame Estimation (Fallback Method)
When IFC/Tekla models are unavailable, this manual estimation method (absorbed from `construction-costing-plan`) provides accurate approximations:

1. **Identify profiles from drawings**: HEA columns, IPE beams, UPN channels, EA bracing
2. **Count from structural grid:**
   - Columns = grid intersections (e.g., 7 × 4 = 28 typical) × height (G+1 ~7.5m) × kg/m
   - Main beams = grid lines × floors × span length × kg/m
   - Secondary beams = bays per floor × beams per bay × floors × span × kg/m
3. **Add bracing, connections, base plates**: ~3-5 tons
4. **Add staircase**: ~2-2.5 tons for 2-storey
5. **Cross-check with rule-of-thumb**: 2-storey steel frame ≈ 50-65 kg/m² built-up area

## Tender BoQ Analysis & Pricing Strategy

### When to Use
- You receive an existing consultant/designer BoQ and need to price it as a contractor
- The project is a **fit-out / exhibition / museum** with multiple trade packages (AV, lighting, furniture, scenography)
- You need to decompose a complex BoQ into subcontract packages for pricing
- You're producing comprehensive documentation to support a tender submission

### Workflow

#### 1. Read the BoQ First (Macro View)
- Open the BoQ `.xlsx` with `openpyxl(data_only=True)`
- Read the **summary sheet** first — identify the two key numbers: base cost and all-in cost
- Note currency (USD/SAR/EUR) and the conversion rate used
- Check for add-on percentages: art direction, mobilisation, overhead, financial cost, contingency, profit
- Check which sheets actually have unit prices filled vs blank — AV technical BOQs often have specs but no rates

#### 2. Identify ALL Source Documents
Inventory every supporting file in the project folder before reading anything:
- **Material schedules** — finishes, codes, areas
- **AV specifications** — BOQs often have blank unit prices; read the technical spec sheets separately
- **Lighting schedules** — fixture types, brands, quantities, control systems
- **Furniture schedules** — codes, suppliers, origins, dimensions
- **CAD drawings** — for spatial context (check subdirectories)
- **PDF design docs** — scenographic design, detailed design, material schedules

#### 3. Read ALL Sources in Parallel via delegate_task
**Critical rule:** Read every source file comprehensively before producing output. **Do NOT read Excel files via inline Python heredocs** — these are error-prone (syntax issues with f-strings in heredocs, unterminated strings). Instead, use `delegate_task` to run parallel extraction:

```python
# Parallel extraction of 3-4 groups simultaneously
results = delegate_task(tasks=[
    {
        "goal": "Extract ALL sheets from this BoQ Excel file with openpyxl(data_only=True). Output every row with values in structured format.",
        "context": "File path: /path/to/BoQ_v04.xlsx",
        "toolsets": ["terminal"]
    },
    {
        "goal": "Read ALL Excel files in the AV/lighting subfolder. For each file, list sheets and extract all data rows.",
        "context": "File paths under: /path/to/AV_Excel_Files/",
        "toolsets": ["terminal"]
    },
    {
        "goal": "Read Material Schedule + Furniture Schedule Excel files. Extract all sheets and rows.",
        "context": "File paths under: /path/to/Supporting_Areas_Excel_Files/",
        "toolsets": ["terminal"]
    }
])
```

**Why parallel:** Reading 3+ multi-sheet Excel files sequentially is slow and wastes context. Each subagent gets an isolated terminal with openpyxl. Results come back as summaries. This avoids heredoc syntax issues with f-strings, escape characters, and multi-line strings.

**If a subagent fails** (content filter, timeout), retry that specific task individually — don't re-run all 3.

#### 4. When Inline Scripts Are Acceptable
Use inline `execute_code` or heredoc Python ONLY for:
- **Quick verification queries** — count rows, check specific sheet names, verify column headers (single output cell)
- **Post-extraction analysis** — cross-referencing data already extracted by sub-agents
- **Simple file stats** — `wc -l`, `head`, `tail` type commands

**Do NOT use inline heredocs for bulk data extraction** — multi-line heredocs with f-strings and escape sequences are fragile. The user explicitly corrected this: "always delegate to labors" for heavy extraction.

#### 5. Organise Data into Work Packages

For exhibition/fit-out projects, typical packages:

| Code | Package | Typical % of Total | Notes |
|------|---------|-------------------|-------|
| P01 | AV Supply & Install | ~30-35% | Largest single cost — verify blank unit prices |
| P02 | Lighting Supply & Install | ~4-5% | DMX control integration, commissioning |
| P03 | Furniture Supply & Install | ~3-5% | Often Italian/European imports — check lead times |
| P04 | Exhibition Fit-Out (galleries) | ~20-25% | Custom joinery, scenic theming, showcases |
| P05 | Supporting Areas Fit-Out | ~15-20% | Majlis, cafe, library, corridors |
| P06 | Scenography / Theming | ~3-5% | Curved walls, scenic finishes, art direction |
| P07 | Civil & MEP Works | ~5-8% | Base build, electrical, mechanical |
| P08 | Graphics Production & Install | ~1-2% | Wall graphics, labels, signage |

#### 5. Create Structured Documentation

Use a `_PRICING_DOCS/` subfolder with numbered MD files that cover the full project scope:

```
_PRICING_DOCS/
+-- 01_PROJECT_OVERVIEW.md          # Identity, financial summary, currency, stakeholders
+-- 02_BOQ_BREAKDOWN.md             # Itemised breakdown by area/package, cost ratios
+-- 03_{AREA}_DETAIL.md             # Per-zone scope (e.g. EXHIBITION_GALLERIES)
+-- 04_{AREA}_DETAIL.md             # Second area (e.g. SUPPORTING_AREAS)
+-- 05_{DISCIPLINE}_TECHNICAL.md    # e.g. AV_TECHNICAL — productions, hardware, installation
+-- 06_{DISCIPLINE}_TECHNICAL.md    # e.g. LIGHTING_TECHNICAL — fixtures, control, installation
+-- 07_MATERIALS_FINISHES.md        # Material codes, finishes, specifications
+-- 08_FURNITURE_SCHEDULE.md        # Furniture codes, suppliers, origins, dimensions
+-- 09_PRICING_STRATEGY.md          # KEY FILE — work packages, margins, risk, next steps
+-- 10_{PACKAGE}_GAP_ANALYSIS.md    # e.g. AV_PRICING_GAP — main BoQ vs consultant file
+-- 11_MARKET_AUDIT_REPORT.md       # Market rate verification across ALL categories
```

Each file should be **self-contained** (reader should not need to open other files to understand that topic). Use tables for structured data.

#### 6. Run Parallel Market Audit

After creating the documentation, verify the BoQ rates against current market by running parallel research sub-agents:

```python
# Parallel market audit — each agent researches one category
results = delegate_task(tasks=[
    {
        "goal": "Research market prices for AV equipment (Epson projectors, QSC speakers, LOPU/Muxwave LED walls, Nexmosphere sensors, Visual Production controllers). Compare each BoQ unit price against current market and flag over/under/fair.",
        "context": "Project context, BoQ item list with unit prices",
        "toolsets": ["web"]
    },
    {
        "goal": "Research market prices for lighting fixtures (DGA, FLOS, Prolights, LUXAM, Enttec, Visual Production). Compare each BoQ EUR/USD price against market.",
        "context": "Lighting fixture list with brand, model, and BoQ unit prices",
        "toolsets": ["web"]
    },
    {
        "goal": "Research market pricing for (A) Italian furniture imported to KSA and (B) construction fit-out rates in Riyadh. Compare BoQ rates against market.",
        "context": "Furniture schedule with Italian brands + fit-out unit rates",
        "toolsets": ["web"]
    }
])

# Compile results into 11_MARKET_AUDIT_REPORT.md
```

Covers all categories in one parallel pass (limited to 3 concurrent). If the project has more than 3 distinct categories, batch them.

#### 7. Pricing Strategy (09_PRICING_STRATEGY.md)

Cover these sections:
- **BoQ rate verification** — cross-check unit rates against current market (supplier quotes, past projects)
- **Blank/incomplete prices** — common in AV BOQs (technical specs with quantities but no rates); flag for supplier pricing
- **Work package breakdown** — P01-P08 with estimated values
- **Margin structure** — GC overhead, profit, contingency, mobilisation, financial cost (as per BoQ add-on percentages)
- **Risk register** — technical complexity (AV integration), import logistics (Italian furniture), currency exposure (EUR to SAR), schedule coordination
- **Top-N value items** — list the 20 highest-value line items for priority pricing
- **Procurement timeline** — lead times for key imported items
- **Decision matrix** — make-vs-buy analysis for packages

#### 7. Key Checks When Reviewing a BoQ

- [ ] Unit prices are entered for ALL line items (not just quantities)
- [ ] Currency conversion is consistent across all sheets
- [ ] Material schedule codes match BoQ references
- [ ] AV equipment specs match suppliers' current product lines
- [ ] Lighting control system scope (DMX programming, commissioning) is scoped
- [ ] Furniture supplier origins and lead times are noted
- [ ] Installation & commissioning is scoped separately from equipment supply
- [ ] Any local content / Saudization requirements apply

### Pitfalls

- **Blank AV unit prices:** Many AV BOQs are technical specifications first, pricing second. The quantities may be accurate but rates are to be filled by the AV subcontractor. Do not assume blank cells mean zero. Cross-reference the main BoQ summary totals against the detailed AV spec sheets — if the summary has a total but the detail sheet has blanks, someone filled prices after the detail sheet was created.
- **Inline Python heredoc fragility:** Do NOT write multi-line Python scripts inside shell heredocs for Excel extraction. F-strings with `\n` escape sequences, multi-line string literals, and single/double quote mismatches cause hard-to-debug syntax errors. Write the script to a `.py` file first, then execute it. Or better: delegate to a sub-agent.
- **Lighting in EUR:** European lighting suppliers (DGA, FLOS, etc.) often quote in EUR. Verify the EUR/USD/SAR exchange rate applied in the BoQ and the date of conversion. The lighting designer may have a different rate than the AV consultant.
- **Italian furniture lead times:** Imported furniture (Calligaris, B&B Italia, Poltrona Frau, Molteni&C) has 8-16 week lead times plus customs clearance. Factor into schedule.
- **Scopey AV integration:** DMX lighting control, show control, and AV systems need to be coordinated. The AV contractor and lighting contractor must share the same control protocol (usually DMX or Art-Net).
- **Subcontractor double-scoping:** Ensure the AV installation package and lighting installation package have clearly defined boundaries (who provides cable trays? who terminates DMX lines?).
- **Design responsibility:** The BoQ may include 'coordination by AVL contractor' clauses that transfer design risk. Read the fine print.
- **Currency assumptions:** When the BoQ shows USD to SAR at 3.75 (pegged rate), confirm this matches the actual conversion your suppliers use. Importers may face different effective rates.

## Verification Checklist (absorbed from construction-costing-plan)

Before delivering any costing plan:
- [ ] All formulas auto-calculate: check grand total ≠ 0 when rates entered
- [ ] Sheet names are unique and descriptive
- [ ] Cover page has project name, date, assumptions, and cost/m²
- [ ] Freeze panes at row 4 on data sheets
- [ ] Page setup: landscape, fit to width
- [ ] Every work package tab has rates entered — never leave a tab empty
- [ ] Open the generated file to confirm all sheets exist
- [ ] Test a rate entry to verify formula calculates

## 8. Origin Market Price Verification

**Do NOT accept BoQ prices at face value.** BoQ prices are often the consultant's EUR/USD list prices with zero logistics markup (no shipping, customs, clearance, or distributor margin added). The user explicitly corrected: "dont take the Original BOQ price as its right."

### 8.1 Detect the BoQ's Price Source

| Signal | What It Means | Action |
|--------|---------------|--------|
| BoQ has EUR to USD at exactly 1.18 or 1.1585 | Prices are exchange-rate converted; no logistics added | Must add 25-33% for KSA landed cost |
| BoQ has USD to SAR at exactly 3.75 | SAR is pegged; no hidden markup | Verify USD column independently |
| AV BoQ has blank unit prices | Consultant's technical spec only — prices need filling by subcontractor | Get subcontractor quotes |
| PC Sum / Provisional Sum | Amount directed by client, not priced by consultant | Exclude from contractor risk |

### 8.2 Classify Import Category by Keywords

For each item, detect origin from brand/description keywords, then apply the correct logistics multiplier:

**Import_EU (×1.33):** DGA, FLOS, Armonia, Ariel, Tono, Calligaris, B&B Italia, Poltrona Frau, Molteni, Draenert, NORR11, LAGO, ACERBIS, BK CONTRACT, ARTEMEST, brunner, Laskasas, gianfranco, XLINE, Twils, DESIGNCONCEPTS, Cooledge, LUXAM, Prolights, Visual Production, Enttec, Eldoled, LTECH, DMX, CueCore, B Station, Kiosc, Seki Han
- Breakdown: shipping 4% + insurance 0.4% + customs 5.2% + clearance 2.5% + bank 1% + distributor 17.5% = 33%

**Import_US (×1.25):** Epson, QSC, Crestron, Brightsign, Cisco, Eaton, Nexmosphere, Chief, Iiyama, Binepad, Exact Solutions
- Breakdown: shipping 3% + insurance 0.4% + customs 5.2% + clearance 2.5% + bank 1% + distributor 15% = 25%

**Import_China (×1.20):** LOPU, Muxwave, Brainsalt, Barrisol, Leben
- Breakdown: shipping 5% + insurance 0.4% + customs 5.2% + clearance 2.5% + bank 1% + distributor 12% = 20%

**Local KSA (×1.00):** installation, labour, commission, demolition, civil, paint, gypsum, drywall, MDF, Riyadh stone, Jotun, Sadu, plaza

**Mixed (×1.15):** marble, carpet, vinyl, glass, aluminium, steel, Corian, dibond, acoustic fabric, antireflective glass

### 8.3 Search Origin-Country Market Prices

| Origin | Where to Search | Currency |
|--------|----------------|----------|
| China | Alibaba, manufacturer sites (LOPU, Muxwave) | USD FOB |
| Italy/EU | Manufacturer list prices (dga.it, flos.com) | EUR |
| US | B&H Photo, Markertek, CDW | USD |
| KSA | Local suppliers, Saudi Building Cost Index | SAR |

Compare BoQ rate to origin price:
- Gap > +30%: RED — BoQ overpriced, get supplier quote
- Gap +15-30%: AMBER — slight markup, cross-check
- Gap < +15%: GREEN — fair pricing
- Negative (BoQ < origin): verify — possible error, bulk discount, or used goods

### 8.4 Build Excel Pricing Model with Evidence

Create a multi-sheet workbook with openpyxl tracking every price to source:

**Required sheets:** ITEM PRICING (all items, flat table), EVIDENCE (source ref, market verification, confidence), SUMMARY BY CATEGORY, LOGISTICS MATRIX (multiplier definitions), MARGIN ANALYSIS (variance per category).

**ITEM PRICING columns:** Item ID, Category, Subcategory, Description, Qty, Unit, BoQ Unit Rate, BoQ Total, Origin Market Price, Currency, Price Source, BoQ vs Market %, Final Unit Rate (origin × logistics), Import Category, Logistics Multiplier, Adjusted Rate, Adjusted Total, Hidden Costs (3%), Overhead (7%), Profit (15%), All-in Total, Notes.

**MULTI-SOURCE AUDIT columns (22 per item):** Item ID, Category, Subcategory, Description, Qty, Unit, BoQ Unit Rate, Source 1: Name, Source 1: Price ($), Source 1: Reference, Source 2: Name, Source 2: Price ($), Source 2: Reference, Source 3: Name, Source 3: Price ($), Source 3: Reference, Median Market ($), Low ($), High ($), BoQ vs Median (%), Verdict (color-coded), Action/Recommendation.

See `references/multi-source-audit-workbook.md` for the full workbook structure, verdict logic (red/amber/green), source strategy by import category, category-to-sheet mapping, and the openpyxl implementation pattern.

See `references/import-logistics-matrix.md` for the complete origin classification table (EU ×1.33, US ×1.25, China ×1.20, Local ×1.00, Mixed ×1.15), brand-to-origin mapping, component breakdown of each multiplier, and worked examples.

**Confidence levels:** HIGH (known brand/model with researchable market price from 3+ sources), MEDIUM (generic descriptions, installation, civil — 2 sources), LOW (PC sums, provisional items — no market comparison). Color-code cells.

**Cascade applied per item:** origin_price × logistics_mul = landed cost → +3% hidden → +7% overhead → +15% profit = all-in.

### 8.5 Furniture Pricing Warning

Italian/European furniture BoQ lump sums are often grossly inadequate for listed brands. Common pattern: "$32,000 for Main Majlis" but the Furniture Schedule lists 56 Calligaris chairs + 26 B&B Italia chairs + 13 Poltrona Frau chairs. At European retail alone, the chairs cost €100K-230K. Always cross-reference the Furniture Schedule quantities against European retail before accepting lump sums.

## 9. Joinery/Furniture Costing from Drawings

### When to Use
- User provides a 2D CAD elevation, photo, or rendering of a custom joinery piece (counter, kiosk, reception desk, cabinet, screen)
- Need to produce a material + labor + finishing cost breakdown
- Need to quickly recalculate when material spec changes

### Workflow

#### 1. Analyze the Drawing/Image

If the active model cannot process images (no vision support), delegate vision analysis:

```python
delegate_task(
    goal="Describe this joinery piece in complete detail for costing purposes: components, dimensions (proportional), wood type, joinery, hardware, decorative elements, style.",
    context=f"Image path: {path}",
    toolsets=["browser", "terminal", "file"]
)
```

**The subagent should:** start a local HTTP server to serve the image, navigate browser to it, then use browser_vision for detailed analysis covering: overall proportions, components (base/countertop/back panel/shelves/drawers/trim), joinery type, material clues, finish, hardware, decorative elements, style classification.

**Alternative (delegate to Kimi):** If user says "let kimi read for you":
```python
delegate_task(
    goal="Analyze this image and describe it in complete detail for costing purposes.",
    context=f"Image path: {path}. Active model can't see images. Use browser tool: "
            "start http.server in /tmp, copy image there, navigate browser to it, "
            "then use browser_vision for detailed visual analysis.",
    toolsets=["browser", "terminal", "file"]
)
```
The subagent will: (1) start a temporary HTTP server, (2) copy the image, (3) navigate browser to display it, (4) use browser_vision to analyze — returning a complete furniture-designer-level spec sheet.

**What to extract from the analysis:**
- Overall dimensions (estimate from proportions using standard counter height ~1100mm as reference)
- Number and type of components (frame, panels, countertop, base, shelves, doors)
- Decorative complexity (carved/CNC panels vs flat panels)
- Material clues (solid wood vs MDF, wood species, finish type)

**Fallback when vision is unavailable:** If the subagent's browser_vision also fails (model lacks vision support), use Python PIL pixel analysis to infer structure:

```python
from PIL import Image, ImageFilter
img = Image.open(path)
gray = img.convert('L')
edges = gray.filter(ImageFilter.FIND_EDGES)
mask = gray.point(lambda x: 0 if x > 200 else 255)
bbox = mask.getbbox()  # object bounding box

# Edge density by horizontal strips → identifies countertops, shelves, base
for y in range(0, h, strip_height):
    strip = edges.crop((0, y, w, min(y+strip_height, h)))
    edge_count = sum(1 for px in strip.getdata() if px > 128)
    # High density = horizontal feature (countertop, shelf, base)

# Color analysis → wood tone (dark = walnut/wenge, medium = oak/mahogany)
obj_colors = [(c, color) for c, color in colors if sum(color[:3]) < 700]
# >90% near-black = dark wood or painted black
# Green pixels = plant decoration
```

Signals from pixel analysis: strong horizontal bands at y=50-60 (top/crown), y=280-310 (countertop), y=420-430 (base); strong vertical columns at x=80-90 and x=320-330 (side supports).

#### 2. Structure the Cost Breakdown

Use the standard cost structure — three main groups:

**A. Materials** — list with quantity, unit rate, total
**B. Labor** — list with estimated days, daily rate, total
**C. Finishing** — materials + labor (stain/paint/lacquer)
**D. Overhead & Logistics** — workshop overhead, transport, installation

#### 3. Material Estimation from CAD Elevations

For a typical reception kiosk/counter (~1250mm W × 1100mm H):

| Material | Qty | Notes |
|----------|-----|-------|
| MDF 18mm (frame + carcass + base) | 3 sheets | 2440×1220mm |
| MDF 25mm (countertop build-up) | 1 sheet | For solid-feel counter |
| MDF 12mm (decorative panels) | 1 sheet | For CNC-carved inserts |
| Adhesives, screws, dowels | 1 lot | |
| Hardware (push-latches, hinges) | 1 set | Concealed type |
| Finishing materials | 1 lot | Primer + paint or stain + lacquer |
| Abrasives | 1 lot | |

**Switching from hardwood to MDF:**
- Eliminate: hardwood framing (mortise & tenon)
- Add: more MDF sheets (frame is cut from MDF instead)
- Reduce: frame assembly labor (pocket screws + glue instead of mortise & tenon)
- Eliminate: stain + lacquer materials
- Add: water-based primer + water-based paint

#### 4. Labor Estimation

| Work | Days (Hardwood) | Days (MDF) | Notes |
|-----|----------------|------------|-------|
| Frame joinery | 3 | 2 | Hardwood needs mortise & tenon; MDF uses pocket screws |
| CNC routing panels | 1 | 1 | Same regardless of substrate |
| Countertop fab + routing | 1 | 0.5 | MDF routes faster |
| Assembly & fitting | 1.5 | 1 | Fewer joints with MDF |
| Sanding + prep | 1 | 0.5 | MDF sands easier |
| Finishing | 1.5 | 1 | Paint faster than stain+lacquer |

#### 5. Finishing Options

| Finish | Materials | Labor | Durability |
|--------|-----------|-------|------------|
| Stain + satin lacquer | 1 lot stain + 2L lacquer | 1.5 days spray + sand | High |
| Water-based paint (primer + 2 coats) | 1 gal primer + 2L paint | 1 day spray | Medium-High |
| High-gloss paint | Primer + 2L gloss paint | 1.5 days | High (more coats) |

**Key difference:** Water-based paint is simpler and cheaper but less durable than lacquer. MDF requires edge sealer/filler before painting.

#### 6. Quick Recalculation when Spec Changes

When user changes the material spec (e.g., "no solid wood, all MDF and water-based paint"):

1. **Materials swap:** Remove hardwood → add MDF sheets; remove stain+lacquer → add primer+water paint
2. **Labor reduce:** Frame assembly 3→2 days; sanding/prep 1→0.5 days; finishing 1.5→1 day
3. **Total saving:** ~42% vs hardwood+lacquer

Pattern for recalculating (openpyxl or Python):
```python
materials = {
    "MDF 18mm": {"qty": 3, "rate": 120},
    "MDF 25mm": {"qty": 1, "rate": 180},
    # ...
}
labor = {
    "Frame assembly MDF": {"days": 2, "rate": 300},
    # ...
}
total_m = sum(d["qty"] * d["rate"] for d in materials.values())
total_l = sum(d["days"] * d["rate"] for d in labor.values())
overhead = (total_m + total_l) * 0.10
grand = total_m + total_l + overhead + transport + install
```

#### 7. Output Format

User prefers this format when delivered:

```
**ITEM:** Name of the piece
**Description:** [paragraph — construction method, materials, finish, dimensions, key features]
**Scope excludes:** [items explicitly not included — screens, furniture, lighting, AV]
**Unit price (manufactured, delivered, installed): SAR X,XXX

COSTING BREAKDOWN:
| # | Item | Qty | Rate | SAR |
|---|---|---|---|---|
| A | MATERIALS | | | X,XXX |
| B | LABOR | | | X,XXX |
| C | FINISHING | | | X,XXX |
| D | OVERHEAD + LOGISTICS | | | X,XXX |
| | GRAND TOTAL | | | X,XXX |

Quantity discounts: 2u -5%, 3-5u -10%, 6+ -15%
Variables: wood type, dimensions, hand carving vs CNC, countertop material
```

#### 8. Common Corrections & Pitfalls

- **User corrects material:** "no solid wood all mdf and waterbase paint" → don't ask follow-up, recalculate immediately
- **User wants description + price:** Deliver both together — description paragraph with exclusions + unit price
- **Price always in SAR** — KSA market, no VAT mention unless asked
- **"Without screen and furniture"** means the kiosk/counter structure only — no electronic screens, no loose furniture, no chairs
- **Pixel-level analysis of CAD elevations:** When image resolution is limited (458×521, 5.4% object coverage), use edge-density analysis to identify structural features (horizontal bands = countertops/shelves, vertical columns = supports)
- **Typical counter height assumption:** 1100mm for reception counters (used to scale dimensions from pixel measurements)
- **Painted MDF needs edge sealing:** Always include edge filler/sealer in materials when using MDF with paint finish

#### 9. When to Read BoQ Source Data

**Always delegate BoQ reading to sub-agents, never inline.** Multi-sheet Excel files with special characters in sheet names (🟡, 🔴, 🟢) and inconsistent column layouts are fragile to handle via inline Python heredocs. Use delegate_task with toolsets=["terminal"] for parallel extraction of 3-4 file groups, then compile results.

Do NOT use inline python3 << PYEOF heredocs for bulk Excel extraction — escape sequences, f-string newlines, and mixed quotes cause hard-to-debug syntax errors. Write the script to a .py file first, or delegate.

## Cost Reclassification (Capitalization → Execution Categories)

When reviewing MR Yosry-style capitalization registers (IAS 16 asset categories), reclassify into execution categories: On-Site Work, Off-Site Manufacturing, AV & IT Equipment, Furniture, Tools & Consumables, Indirect Costs. See `references/capitalization-to-execution-cost-classification.md` for full methodology, on-site install rates per category, overhead allocation, and flags to watch.

## Pitfalls

- **Subtotal double-counting:** Never have both item rows AND subtotal rows in the SUM range. Use a plain `=SUM(Gfirst:Glast)` that covers only item rows. No `SUMIF` with ">0".
- **SAP2000 PDF screenshots:** Design calculation PDFs often have image-based output. OCR fails on dark-themed SAP2000 screenshots. Use the IFC/Tekla export file instead for quantity extraction.
- **Duplicate profile counts:** In Tekla IFC exports, a single beam may have sub-elements (bolts, nuts, washers) that share the parent's profile name. Filter these out — M12_HEAVY_HEX_NUT, M12_WASHER, D16 are not structural steel.
- **TEKLA profile naming:** Tekla uses standard EN profile names in IFC exports (HEA220, IPE240, IPE220, UPN180, RSA60×60×6, SHS70×4, etc.). These match standard section tables.
- **Column height assumption:** If floor-to-floor height isn't explicit in the drawings, use plan elevations (Plan +0, Plan +7480, etc.) from the drawing PDF. G+1 building with total height 7.48m = ~3.74m per storey.
- **Excel cell references:** After deleting/inserting rows, verify the grand total formula references the correct range. Deletions shift references.
