# Subcontractor Risk Register Pattern (Markdown)

## When to Use

Instead of an Excel PRR, build a markdown risk register when:
- The scope is a **single subcontractor package** (MEP Designer, AV Contractor, Showcase Supplier)
- The user wants **phase-gate alignment** (Pre-Appointment → Mobilisation → 50% → 90% → IFC → AFC)
- Risks are sourced from **contract documents** (the subcontractor's offer, the project SOW, the DMP, specialist SOWs) — not from project memory / disputes history
- The user is in **contract negotiation** phase and needs a decision-support tool, not a governance deliverable

## Source Documents (in priority order)

1. **Subcontractor's offer/proposal** — scope exclusions, role statements, fee structure, timeline, validity
2. **Approved SOW** (project-level) — contractual obligations the subcontractor must meet
3. **DMP (Design Management Plan)** — gate structure, programme, risk section, interface management
4. **Specialist SOWs** (e.g. ICT & BMS Specialist SOW) — interface boundaries with the subcontractor
5. **Baseline programme** — day references (D0, D35, D65, D88, D300) for phase alignment

## Structure

### Header Block
```
# {Subcontractor} Design Risk Register — {Project}

**Project:** {Project name} | **Package:** {Package name}
**Date:** {Date} | **Status:** {Current status}
**DMP Reference:** {DMP doc code}
**Baseline Programme:** {Programme ref}
```

### Risk Scoring
Standard 5×5 P×I matrix (1-5 each, 1-25 total):

| Score | Level | Review |
|-------|-------|--------|
| 1-4 | Low | Quarterly |
| 5-9 | Medium | Monthly |
| 10-16 | High | Bi-weekly |
| 17-25 | Critical | Weekly |

### Phase Sections (6 phases)

| Phase | DMP Gate | Typical Risks |
|-------|----------|--------------|
| **Pre-Appointment & Contract** | Before D0 | Role ambiguity, scope gaps, BIM exclusion, timeline unrealistic, offer expiry |
| **Mobilisation & Site Surveys** | D0–D28 | Missing as-builts, inaccurate SLDs, utility capacity unknown, geotechnical gaps |
| **50% Design Development** | D0–D35 / G2 | Ceiling clashes, load calc delays, lighting interface, ICT design gap, late architectural background |
| **90% Design Development** | D35–D65 / G3 | CG rejection of 50%, FLS strategy not approved, AV integration, BMS points, material submittal timing |
| **100% IFC Production** | D65–D88 / G4 | Authority NOC delays, clash detection not zeroed, calculation register incomplete, spec non-compliance |
| **AFC & Construction Support** | D88–D300 | TQ volume, as-built documentation, COBie handover |

### Risk Table Columns

```
| ID | Risk | P | I | PxI | Level | Owner | Mitigation | Contingency |
```

### Summary Table

```
| Phase | Critical | High | Medium | Low | Total |
```

### Top 5 Critical Actions

Numbered list of the highest-priority actions with owner and target date.

## Two-Phase Workflow: Markdown → Enhanced Excel

When the user needs both a decision-support tool during negotiation AND a governance deliverable, use a two-phase approach:

### Phase 1: Markdown (during contract negotiation)
- Build the markdown register first — fast, focused on decision support
- Source risks from contract documents (offer, SOW, DMP)
- Phase-gate aligned (D0→D300)
- 9 columns: ID, Risk, P, I, PxI, Level, Owner, Mitigation, Contingency
- Include Summary table + Top 5 Critical Actions

### Phase 2: Enhanced Excel (after markdown is approved)
- Convert the markdown register to an openpyxl workbook
- Add these enhancements on top of the base data:

| Enhancement | Implementation |
|-------------|---------------|
| **Legend row** | Green-banded instruction row at top explaining P/I/PxI/Level/Status conventions |
| **Status column** | New column with dropdown validation: Open / Mitigated / Closed |
| **Review Date column** | New column for tracking next review |
| **Data validation** | P (1-5 integer), I (1-5 integer), Level (Critical/High/Medium/Low dropdown), Status (Open/Mitigated/Closed dropdown) |
| **Conditional formatting** | PxI column: 17-25 → red fill, 10-16 → yellow, 5-9 → blue, 1-4 → green |
| **Level colour coding** | Critical → red/white, High → yellow/black, Medium → blue/black, Low → green/black |
| **Alternating row shading** | Light blue/white alternating within each phase group |
| **Phase header styling** | Blue fill with bold dark text, medium borders |
| **Page setup** | Landscape, A3, fit-to-width, gridlines hidden |
| **Frozen panes** | Below header row |
| **Auto-filter** | On header row |

### Excel Enhancement Code Pattern

```python
# Data validation for dropdowns
dv_severity = DataValidation(type="list", formula1='"CRITICAL,HIGH,MEDIUM,LOW"', allow_blank=True)
ws.add_data_validation(dv_severity)
dv_severity.add(f"G2:G{len(risks)+1}")

dv_prob = DataValidation(type="list", formula1='"1,2,3,4,5"', allow_blank=True)
ws.add_data_validation(dv_prob)
dv_prob.add(f"D2:D{len(risks)+1}")

dv_status = DataValidation(type="list", formula1='"Open,Mitigated,Closed"', allow_blank=True)
ws.add_data_validation(dv_status)
dv_status.add(f"K2:K{len(risks)+1}")

# Conditional formatting for PxI scores
from openpyxl.formatting.rule import CellIsRule
red_fill = PatternFill(start_color='FEE2E2', end_color='FEE2E2', fill_type='solid')
yellow_fill = PatternFill(start_color='FEF3C7', end_color='FEF3C7', fill_type='solid')
blue_fill = PatternFill(start_color='E0F2FE', end_color='E0F2FE', fill_type='solid')
green_fill = PatternFill(start_color='F0FDF4', end_color='F0FDF4', fill_type='solid')

ws.conditional_formatting.add(f"F2:F{len(risks)+1}",
    CellIsRule(operator='greaterThanOrEqual', formula=['17'], fill=red_fill))
ws.conditional_formatting.add(f"F2:F{len(risks)+1}",
    CellIsRule(operator='between', formula=['10', '16'], fill=yellow_fill))
ws.conditional_formatting.add(f"F2:F{len(risks)+1}",
    CellIsRule(operator='between', formula=['5', '9'], fill=blue_fill))
ws.conditional_formatting.add(f"F2:F{len(risks)+1}",
    CellIsRule(operator='lessThanOrEqual', formula=['4'], fill=green_fill))
```

### Sheets in the Enhanced Excel

| Sheet | Content |
|-------|---------|
| **Risk Register** | 27 risks × 10 columns (ID, Phase, Risk, P, I, PxI, Level, Owner, Mitigation, Contingency) + Status + Review Date |
| **Summary** | Count by phase and risk level, with total row |
| **Top 5 Actions** | Priority actions with owner and target date |

### When to Skip Phase 2
- User only needs the markdown for their own decision-making
- The subcontractor is not yet appointed (Excel is premature)
- User explicitly says "just the markdown is fine"

## Key Differences from Excel PRR

| Aspect | Excel PRR (Full/Phase) | Markdown Subcontractor | Enhanced Excel Subcontractor |
|--------|----------------------|----------------------|------------------------------|
| Format | .xlsx with openpyxl | .md file | .xlsx with openpyxl |
| Source | Project memory (disputes, NCRs, rejections) | Contract documents (offer, SOW, DMP) | Contract documents (same as markdown) |
| Audience | PM / governance | Decision-maker during negotiation | Management / governance |
| Columns | 14-24 columns with dropdowns | 9 columns, no dropdowns | 12 columns with dropdowns |
| Charts | Donut + bar on dashboard | None | None (summary sheet instead) |
| Phase alignment | Generic RBS categories | DMP gate-aligned (D0→D300) | DMP gate-aligned (D0→D300) |
| Risk count | 24-31+ | 20-30 | 20-30 |
