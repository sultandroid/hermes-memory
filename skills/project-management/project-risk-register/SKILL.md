---
name: project-risk-register
description: Build professional Excel-based Project Risk Registers (PRR) for construction/museum/infrastructure projects — 31+ evidence-based risks, governance-grade styling, RBS taxonomy, P×I heat map, severity matrix, and PM dashboard with KPI cards, charts, and health checks.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [risk-register, prr, excel, openpyxl, project-management, construction, dashboard, risk-matrix]
    related_skills: [bim-project-register, project-register-manager, evm-analysis-chart]
---

# Project Risk Register (PRR) — Excel Builder

## When to Use

- User asks for a "risk register", "PRR", "project risk register", "risk matrix" Excel file
- Building a risk register for a construction, museum, infrastructure, or fit-out project
- Need a professional workbook: 2 sheets (Summary + Register) for phase-specific registers, or 3 sheets (+ dashboard) for full project registers
- Required: evidence-based risks (from project memory, NOT generic templates), P×I scoring, severity classification
- **Always prioritize real risks from project memory over template/generic risks** — the user explicitly wants evidence-based entries

## Variants

| Variant | Sheets | When |
|---------|--------|------|
| **Full** | Risk Register + RBS/Scoring Guide + Dashboard | Single consolidated register for entire project (31+ risks) |
| **Phase** | Summary + Risk Register | Phase-specific register (24 risks, lighter, faster) — ideal when user says "phase after phase" |
| **Subcontractor** | Markdown document (not Excel) | Package-specific register for a single subcontractor (e.g. MEP Designer, AV Contractor). Phase-gate aligned (Pre-Appointment → Mobilisation → 50% → 90% → IFC → AFC). Sourced from contract documents (offer, SOW, DMP, specialist SOWs), not project memory. See `references/subcontractor-risk-register-pattern.md`. |
| **Subcontractor → Enhanced Excel** | Two-phase: Markdown first, then openpyxl Excel | When the user needs both a decision-support tool during negotiation AND a governance deliverable. Phase 1 = markdown (fast, contract-sourced). Phase 2 = enhanced Excel with data validation, conditional formatting, alternating rows, status/review-date columns, and summary sheet. See `references/subcontractor-risk-register-pattern.md` §Two-Phase Workflow. |
| **Audit** | Multi-sheet audit report | QA an existing risk register (supplier, consultant, or internal). See `references/risk-register-audit-methodology.md` for the full 9-step checklist, common findings, and output format. |
| **Reconcile RMP + DRR** | RMP DOCX + repo + DRR Excel | Cross-reference the Risk Management Plan (DOCX) against the repo Markdown RMP and the Design Risk Register (Excel). Identify discrepancies in scoring scale, RBS categories, risk counts, EMV values, register architecture, and status definitions. Fix all documents to achieve alignment. See `references/rmp-drr-reconciliation.md`. |
| **Template Application** | Source register's layout + styling applied to target | Apply one existing register's full 24-column template, styling, RBS guide, and dashboard to another existing register with different column structure. See `references/template-application-pattern.md`. |
| **Quick** | Single sheet Risk Register | <12 risks, quick stand-up for a meeting |

## Do NOT Use When

- The user only needs a simple list of risks (use a table in conversation instead)
- The project already has a risk register — update the existing file via `project-register-manager` patterns
- The request is about EVM / financial risk — use `evm-analysis-chart` instead

## Workflow

### Phase 0: Mine Project Memory for Real Risks (MANDATORY)

**Never start with template risks.** The user expects evidence-based entries sourced from actual project records. Search in this priority order:

1. **PROJECT_MEMORY.md** (project root) — sections on disputes, rejections, staffing gaps, technical decisions, meetings log, knowledge gaps, and action items all contain latent risks
2. **disputes_and_rejections.md** (Scripts/notes/) — formal rejections (Code C, Code D), SI disputes, variation claims, NCRs, escalation timeline
3. **code_c_d_inventory.md** (Scripts/notes/) — active Code C submittals blocking the pipeline, each is a schedule risk
4. **itc_integrity_technology.md** (Scripts/notes/) — MEP designer variation claim, scope creep, work stoppage
5. **CG_STATUS files** (under each 02.X subfolder) — CG response statuses, SLAs
6. **submittals_cg_responses_matrix.md** — response cycle tracking, rejection patterns
7. **Email archives** (if accessible) — JSI events, NCR rejections, schedule feedback

For each risk extracted, trace the **source reference** in the Description field (e.g., "PROJECT_MEMORY.md §5, disputes_and_rejections.md, JSI MOC-MUS-CG-ASE-1KN-1E0-017"). This provides auditability.

**Mapping real events to risk fields:**

| Project Memory Signal → | Risk Field |
|-------------------------|------------|
| Disputed SI → | Cause = the SI and rebuttal history |
| Code C submittal → | Risk Event = approval delay, Impact = schedule slippage |
| Key personnel departure → | Risk Event = knowledge loss, Impact = decision delays |
| Variation claim received → | Risk Event = commercial exposure, Impact = cost overrun |
| JSI/NCR issued → | Risk Event = compliance breach, Impact = stop-work/penalties |
| Contract at risk → | Risk Event = long-lead procurement gap, Impact = programme extension |

**Do NOT extract risks from:**
- Generic risk taxonomies (ISO 31000 checklists)
- Previous project risk registers from different projects
- Industry-standard templates without evidence from this project's records

### Phase 1: Gather Risk Data

For an evidence-based register, source risks from:
1. **Project status reports and CG status mappings** — identify delayed approvals, Code C submittals, open NCRs
2. **Subcontractor register** — identify not-onboarded specialists (lighting designer, interactive designer, AV/IT)
3. **Procurement lead times** — long-lead items (showcases 14wks, MEP 12-16wks, FF&E 8-12wks)
4. **Contract analysis** — VO caps, SI-007 compliance disputes, schedule compression
5. **Site conditions** — demolition coordination, heritage fabric, scaffolding, weather (Abha fog/rain, summer heat)
6. **Stakeholder dependencies** — CG review capacity, SEC coordination, regulatory permits

Each risk needs:
| Field | Description |
|-------|-------------|
| **Risk Event** | What could happen — specific, single sentence |
| **Cause** | Root cause — evidence-based, grounded in project records |
| **Impact** | Consequence if it occurs — link to cost, schedule, quality, safety |
| **Probability (1-5)** | Likelihood: 1=Rare (<10%) → 5=Almost Certain (>90%) |
| **Impact (1-5)** | Severity: 1=Negligible → 5=Catastrophic (>10% cost, >3mo delay) |
| **P×I Score** | prob × imp (1-25) |
| **Response Strategy** | Mitigate, Reduce, Transfer, Accept, Monitor |
| **Response Action** | Specific action with target dates and responsible party |
| **Risk Owner** | Who is accountable |
| **Status** | OPEN, MITIGATED, WATCH, CLOSED |
| **Residual P/I** | After mitigation, what remains |
| **Contingency Plan** | What to do if risk materializes |
| **Trigger** | Early warning indicator |
| **Linked Risks** | Cross-references to other risk IDs |

### Phase Variant: Phase-Based Register (2-sheet)

When the user says "phase by phase" or "design phase first", build a lighter 2-sheet workbook:

**Sheet 1 — Summary:** Overall counts, severity distribution, RBS category breakdown, data source citation
**Sheet 2 — Risk Register** (14 columns):

```
Risk ID, RBS Code, Risk Category, Risk Title,
Description (Cause → Consequence),
Probability (1-5), Impact (1-5), Risk Score (P×I), Severity,
Response Strategy, Mitigation Measures, Owner, Status, Target Date
```

**When to use this variant:**
- User explicitly requests phase-specific risks ("design phase first")
- 20-25 risks expected (not 31+)
- No dashboard/charts needed yet — aggregate at end of project

**RBS for Phase-Based Register (5 categories, design-phase oriented):**

| RBS | Category | Example Risks |
|-----|----------|--------------|
| RBS-1.x | Technical / Design | SI disputes, DMP cycles, IFC blocks, interface gaps, coordination conflicts, NFPA non-compliance |
| RBS-2.x | Programme / Schedule | Code-C pipeline, CG SLA breaches, designer response times, authority NOC delays |
| RBS-3.x | Resources / Personnel | Key departures, subcontractor declines, BIM resource gaps, vacancies |
| RBS-4.x | Commercial / Contractual | Variation claims, unmade contracts, supplier contract risk, long-lead procurement |
| RBS-5.x | External / Environmental | Regulatory compliance, supply chain disruption, HSE incidents, data/IT risks |

### Phase 2: Build the Workbook

Create a Python script using `openpyxl` (system Python 3.13 on macOS has it).

**Sheet 1 — Risk Register** (24 columns):

```
#, Risk ID, RBS Category, Risk Event, Cause, Impact,
Probability (1-5), Impact (1-5), P×I Score, Severity,
Response Strategy, Response Action, Risk Owner,
Current Status, Target Close Date, Date Identified, Last Review Date,
Residual Probability, Residual Impact, Residual P×I,
Contingency Plan, Trigger/Early Warning, Linked Risk IDs, Notes/Source
```

**Data Validation (dropdown lists):** Add these to make the register interactive:

```python
dv_severity = DataValidation(type="list", formula1='"CRITICAL,HIGH,MEDIUM,LOW,VERY LOW"', allow_blank=True)
ws.add_data_validation(dv_severity)
dv_severity.add(f"I2:I{len(risks)+1}")

dv_prob = DataValidation(type="list", formula1='"1,2,3,4,5"', allow_blank=True)
ws.add_data_validation(dv_prob)
dv_prob.add(f"F2:F{len(risks)+1}")

dv_status = DataValidation(type="list", formula1='"OPEN,MITIGATED,WATCH,CLOSED"', allow_blank=True)
ws.add_data_validation(dv_status)
dv_status.add(f"M2:M{len(risks)+1}")

dv_response = DataValidation(type="list", formula1='"Avoid,Mitigate,Transfer,Accept,Escalate"', allow_blank=True)
ws.add_data_validation(dv_response)
dv_response.add(f"J2:J{len(risks)+1}")
```

**File Naming Convention:**

```
{ProjectCode}-{Org}-{DocType}-{Seq#}_{Phase}_Risk_Register.xlsx
```

Example: `ASR-SAM-RRG-001_Design_Phase_Risk_Register.xlsx`

| Component | Meaning | Aseer Example |
|-----------|---------|---------------|
| ProjectCode | Client/project abbreviation | ASR (Aseer) |
| Org | Your organization | SAM (Samaya) |
| DocType | Document type | RRG (Risk Register) |
| Seq# | 3-digit sequence number | 001 (first version) |
| Phase | Design/Procurement/Construction/Handover | Design_Phase |

**Sheet 2 — RBS & Scoring Guide**:
- 8 RBS categories with descriptions
- Severity bands (CRITICAL 20-25 → VERY LOW 1-3) with required actions
- Probability scale (1-5) and Impact scale (1-5)
- P×I Heat Map matrix (5×5 grid)
- Color legend

**Sheet 3 — Dashboard**:
- RAG Health indicator (RED/AMBER/GREEN based on High+Critical count)
- KPI cards: Total, Open, Mitigated, Watch, Critical, High+Critical
- Status Distribution (Donut chart)
- Severity Distribution (Bar chart)
- Top 8 Risks by P×I (executive table)
- Risk Breakdown by RBS Category
- Risk Owner Workload table
- Risk Register Health Check

### Phase 3: Styling

**⚠️ CRITICAL: Never use `cell.value = val` as a function call inside the cell-writing loop.** The most common openpyxl bug is setting all cell properties (font, fill, alignment, border) but forgetting `cell.value = val`.

**Navy Header Theme:**
- Header row fill: `#0F172A` (navy), font: white bold 9pt
- Alternate row shading: `#F8FAFC` (very light gray) on odd rows
- Thin borders: `#CBD5E1`

**Severity Colors (applied to Severity column):**
| Severity | Fill | Font Color |
|----------|------|------------|
| CRITICAL | `#FEE2E2` | `#991B1B` bold |
| HIGH | `#FEF3C7` | `#92400E` bold |
| MEDIUM | `#FEF9C3` | `#854D0E` bold |
| LOW | `#DBEAFE` | `#1E40AF` |
| VERY LOW | `#F0FDF4` | `#166534` |

**Status Colors (applied to Status column):**
| Status | Fill | Font Color |
|--------|------|------------|
| OPEN | `#FEF2F2` | `#DC2626` bold |
| MITIGATED | `#FEF9C3` | `#B45309` bold |
| WATCH | `#FFF7ED` | `#D97706` bold |
| CLOSED | `#F0FDF4` | `#166534` bold |

**Heat Map Colors (P×I matrix 5×5):**
| Range | Fill | Font |
|-------|------|------|
| 20-25 (Very High) | `#DC2626` | White bold |
| 12-16 (High) | `#EA580C` | White bold |
| 8-9 (Medium) | `#EAB308` | Dark bold |
| 1-6 (Low) | `#22C55E` | Dark bold |

### Phase 4: Dashboard Charting

**Donut chart for Status distribution:**
```python
donut = PieChart()
donut.style = 10
donut.dataLabels = DataLabelList()
donut.dataLabels.showPercent = True
donut.dataLabels.showCatName = True
colors = ["DC2626", "EAB308", "F97316", "22C55E"]  # Open, Mitigated, Watch, Closed
for i, color in enumerate(colors):
    pt = DataPoint(idx=i)
    pt.graphicalProperties.solidFill = color
    donut.series[0].data_points.append(pt)
donut.series[0].explosion = 10  # explode the first slice (Open)
```

**Column chart for Severity distribution:**
```python
bar = BarChart()
bar.type = "col"
bar.style = 10
bar.y_axis.title = "Count"
colors = ["DC2626", "EA580C", "EAB308", "2563EB", "22C55E"]  # Critical→Very Low
```

### Phase 5: Delivery

After generating:
1. **Verify** — re-open and check risk IDs, counts, chart presence, KPI values
2. **Print setup** — A4 landscape, fit-to-width, show gridlines off
3. **Freeze panes** at row below header on the risk register sheet
4. **Auto-filter** on the risk register header row
5. **Deliver** — the file lives at `/tmp/`; user can download or you can copy to project folder

## Scoring Scale Variants

Different registers on the same project can use different scales. Document each register's scale explicitly:

| Register | Scale | Range | Critical | High | Medium | Low |
|----------|-------|-------|----------|------|--------|-----|
| Master Risk Register (PRR) | P x S 1-4 | 1-16 | >=12 | 8-11 | 4-7 | <=3 |
| Designer Risk Register (DRR) | P x I 1-5 | 1-20 | >=15 | 10-14 | 5-9 | <=4 |
| HSE Risk Register | C x L 1-5 | 1-25 | >=16 | 10-15 | 5-9 | <=4 |
| AV Risk Register | P x S 1-4 | 1-16 | >=12 | 8-11 | 4-7 | <=3 |

When reconciling, verify each register's scale matches its actual data distribution. A mismatch means either the thresholds or the scoring data needs updating.

## RBS Categories Standard (8)

| # | Category | Description |
|---|----------|-------------|
| 1 | Design & Documentation | Design documentation, drawings, specifications, BIM models, technical submittals |
| 2 | Procurement & Supply Chain | Procurement strategy, supplier/subcontractor onboarding, lead times, materials |
| 3 | Construction & Installation | Site works, demolition, MEP installation, fit-out, scaffolding, construction methods |
| 4 | Coordination & Interface | Coordination between disciplines and external stakeholders (SEC, CG) |
| 5 | Contract & Commercial | Contractual compliance, variations, claims, EOT, commercial terms, dispute resolution |
| 6 | Health, Safety & Environment | Worker welfare, fire safety, heat stress, weather, site safety, environmental protection |
| 7 | Stakeholder & Approvals | CG/PMC approvals, employer decisions, regulatory permits, heritage authority |
| 8 | Quality & Compliance | NCR close-out, inspection, testing, document control, quality audits, compliance |

## Severity Scoring Rules

```
CRITICAL: P×I ≥ 20  (2 risks max per register is normal)
HIGH:     P×I ≥ 12
MEDIUM:   P×I ≥ 8
LOW:      P×I ≥ 4
VERY LOW: P×I < 4
```

**RAG Health Logic:**
- **RED** — 5+ High+Critical risks → Immediate management attention
- **AMBER** — 2-4 High+Critical risks → Active monitoring
- **GREEN** — 0-1 High+Critical risks → Acceptable thresholds

## Pitfalls

### 🔴 Font has no `wrap` parameter
`Font(name="Calibri", wrap=True)` raises `TypeError: Font.__init__() got an unexpected keyword argument 'wrap'`. The `wrap_text` parameter belongs on `Alignment`, not `Font`. Correct pattern:
```python
# WRONG
cell.font = Font(name="Calibri", size=9, wrap=True)

# RIGHT
cell.font = Font(name="Calibri", size=9)
cell.alignment = Alignment(wrap_text=True)

# Or define once and reuse:
BODY_FONT = Font(name="Calibri", size=9)
ALIGN_WRAP = Alignment(vertical="top", wrap_text=True)
cell.font = BODY_FONT
cell.alignment = ALIGN_WRAP
```

### 🔴 Forgetting `cell.value = val` in cell-writing loops
The most common bug. You set font, fill, alignment, and border on each cell but forget `cell.value = val`. Data appears in the file as NULL/empty. **Always set value first, then styling.**

### 🔴 MergedCell objects on write-after-merge
After `ws.merge_cells("A1:X1")`, cells A1 through X1 of that row become MergedCell objects. Any subsequent attempt to write to those cells (e.g., `ws.cell(row=1, column=3).value = "x"`) raises `AttributeError: 'MergedCell' object attribute 'value' is read-only`.
- **Fix:** Only write to the TOP-LEFT cell of the merge range (e.g., `ws["A1"].value = "Title"`). Write to other cells in the merge range ONLY for styling (fill, border — and even then, only do it once, not in a loop over merged cells).

### 🔴 Walrus operator in function call keywords
```python
# BROKEN — syntax error
apply_cell(ws["A3"], "title", font=SUBTITLE_FILL := Font(...), fill=..., alignment=...)
```
The walrus operator `:=` inside a keyword argument is valid Python 3.8+ but causes lint confusion and can produce `SyntaxError: invalid syntax` depending on surrounding context. **Don't use walrus operators inside function calls.** Assign variables separately.

### 🔴 Heat map matrix row order
The P×I matrix should display Probability 5→1 descending (high probability at top), and Impact 1→5 ascending (low impact on left). This matches standard PM heat map conventions.

### 🔴 DOCX rebuild_table column count mismatch
When rebuilding a python-docx table with `clear_table()` + `add_row()`, the new rows must have the same number of cells as the `w:tblGrid` column count. If they don't, Word renders extra blank columns. After rebuild always verify:
```python
grid = table._tbl.find(qn('w:tblGrid'))
actual_cols = len(grid.findall(qn('w:gridCol')))
header_cells = len(table.rows[0].cells)
# These must match
```
If they differ, either pad the grid (remove extra gridCol elements) or pad the data rows (add empty cells).

### 🔴 Deleting paragraphs shifts indices
In python-docx, `p._element.getparent().remove(p._element)` removes the paragraph from the XML body tree. This shifts the index of every subsequent `doc.paragraphs[i]`. After any paragraph deletion, re-verify all paragraph index references before further modification.

### 🔴 Cover table row index is not sequential document section
The cover page table (Table 0) has rows that map to cover fields. Contract value is at Row 1 (not Row 3), Contractor at Row 3. Always print and verify before editing. Use `cell.text.strip()` to check current content.

### 🔴 openpyxl not in execute_code sandbox
`execute_code` sandbox does NOT have `openpyxl`. Use `terminal(python3 -c "..." )` with system Python (3.13 on macOS).

### 🔴 DataPoint import from wrong module
`from openpyxl.chart import DataPoint` raises `ImportError: cannot import name 'DataPoint'`. The correct import is `from openpyxl.chart.series import DataPoint`. Always use the series submodule for DataPoint, DataPointList, etc.

### 🔴 Chart data in hidden area
Charts need data references in the worksheet. Place chart data in a hidden area (e.g., row 50+) with minimal styling. Keep the chart data references simple — use contiguous ranges.

## Related Skills

- `bim-project-register` — For updating an existing Risk_Register.xlsx (minimal 7-column template)
- `project-register-manager` — For appending rows to existing Excel registers (append-only pattern)
- `evm-analysis-chart` — For financial risk / cost variance reporting (different domain)
- `samaya-technical-office` — For project context and document conventions

## Reference Files

- `references/design-coordination-risk-identification.md` — 7-phase methodology for extracting coordination risks between AV/IT/ELV specialist submissions and base build MEP infrastructure. Covers BOQ power load extraction, rack room heat analysis, projection path spatial conflicts, containment segregation, UPS strategy gaps, and scope boundary risks. Use when reviewing a specialist design submission (AV, IT, Security, ELV) before IFC or before D&B tender.
- `references/template-application-pattern.md` — Apply one existing register's column layout, styling, sheets, and dashboard structure to another existing register. Covers data column mapping, scoring scale bridging, source styling capture, Cover preservation, and verification.
- `references/subcontractor-risk-register-pattern.md` — Markdown risk register for single-subcontractor packages during contract negotiation. Phase-gate aligned (D0→D300), sourced from contract documents (offer, SOW, DMP), not project memory. Use when the user is negotiating with a specific subcontractor and needs decision-support risks, not a governance deliverable.
- `references/risk-register-audit-methodology.md` — 9-step audit checklist for QA-checking an existing risk register. Covers scoring integrity, cross-referencing, lifecycle gaps, residual risk, mitigation quality, and dashboard verification. Use when the user sends an existing XLSX and asks "check this" or "audit this."
- `references/rmp-drr-reconciliation.md` — Cross-reference RMP DOCX, repo Markdown RMP, and DRR Excel to eliminate conflicts. Covers scoring scale alignment, RBS category sync, risk count verification, EMV values, register architecture, status definitions, common DOCX fixes (heading styles, cantSplit, rebuild_table), and common Excel fixes (legends, formulas). Use when the user asks to "check" or "fix" risk management documents that should agree but don't.
