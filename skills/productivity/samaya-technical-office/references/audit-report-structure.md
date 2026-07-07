# Audit Report Template — Samaya Technical Office

## Purpose

A standardized 14-page audit report structure for project reviews at any stage. Used for concept design audits, design development reviews, compliance checks, and phase-gate reviews.

## When to Use

- User asks for an "audit report" or "تدقيق" for any Samaya/Tqanny project
- Phase-gate review is needed before moving to the next design stage
- Heritage Commission/UNESCO compliance check
- Contractor or consultant deliverable review
- Risk assessment or quality audit

## Structure Overview

### Page 1 — Cover
- Logo strip with project code (e.g., `ALF-AUD-001`)
- Cover hero with bilingual title
- Meta-grid: Project, Client, Consultant, Document No, Date
- QC block: Prepared by / Reviewed by / Approved by (Sultan / Medhat / Adel Darwish)
- Page footer with doc code + Rev + page number

### Page 2 — ToC + Executive Summary
- Table of contents listing all 13 sections
- Findings tally: Critical / Major / Minor / Observation counts
- Overall assessment paragraph (Arabic lead + English following)
- Progress bar visual showing distribution
- Bottom-line alert

### Page 3 — Design Compliance Audit
- Audit scope statement
- Finding items in `finding-grid` layout:
  - Each finding: ID tag → Arabic title → English title → Detail (Ar + En)
  - Severity tag: tag-fail / tag-warn / tag-info / tag-pass
- Compliance Rating alert

### Page 4 — Technical Design Audit
- Structural system review
- MEP strategy assessment
- Material and system analysis
- Each major system gets its own finding-item block

### Page 5 — Regulatory & Code Compliance
- SBC compliance table (7 key codes: 201, 301, 401, 601, 701, 801, 1001)
  - Columns: Code | Requirements | Status | Notes
  - Status tags: tag-pass / tag-warn / tag-fail
- Heritage Commission requirements section
- Overall compliance percentage alert

### Page 6 — Risk Management Audit
- Current register assessment
- Recommended additional risks table:
  - ID | Description | Likelihood | Impact | P×I Score | Strategy
  - Score threshold: Critical ≥16 · Major 10–15 · Minor 5–9 · Low <5
- Risk heat map matrix (3×3: Low/Medium/High × Low/Medium/High)

### Page 7 — Quality Management Audit
- Quality plan assessment
- RACI matrix check
- Submittal register review
- ISO 9001 readiness evaluation
- Document core quality (PROJECT_MEMORY.md, etc.)

### Page 8 — Schedule & Progress Audit
- Phase-by-phase schedule table:
  - Phase | Duration | Expected Start | Notes
- Seasonal impact analysis (Hajj, Ramadan, sandstorm seasons)
- Imported material lead time assessment
- Critical path recommendations

### Page 9 — Cost & Value Audit
- Cost breakdown table by element (SAR/m², total, %)
- Preliminary total estimate with contingency breakdown
- Value engineering recommendations
- Cost-box summary (direct cost → consultancy → PM → contingency → total)

### Page 10 — Documentation & Submittal Audit
- Document inventory table:
  - Document Type | Status | Notes
  - Status: tag-pass (exists), tag-warn (missing but planned), tag-fail (missing, critical)
- Folder structure observations
- Native design file (CAD/BIM) availability assessment
- Submittal register completeness

### Page 11 — UNESCO Heritage Compliance
- OUV principles assessment (8-row table)
- Heritage Impact Assessment (HIA) status
- Heritage interpretation strategy review
- Buffer zone compliance
- Material authenticity assessment

### Page 12 — HSE & Sustainability
- Remote site HSE challenges
- Site security and access control
- Sustainability element assessment table:
  - Element | Status | Notes
- Passive design assessment (thermal mass, natural ventilation)
- Certification readiness (Mostadam/LEED)

### Page 13 — Findings Register
- Consolidated action table:
  - ID | Description | Severity | Corrective Action | Responsible | Deadline
- All findings from all sections consolidated here
- Alert note on priority findings

### Page 14 — Conclusion & Recommendations
- Overall summary paragraph (Ar + En)
- Overall scorecard table:
  - Audit Domain | Score | Level
  - Overall average at bottom
- Top-10 recommendations table:
  - # | Recommendation | Priority
- Signature block: Prepared by / Reviewed by / Approved by

## HTML Implementation Notes

### Finding Items Pattern
```html
<div class="finding-item">
  <div class="finding-id"><span class="tag tag-fail">ID-01 · <span class="en">Critical</span></span></div>
  <div class="finding-title">Arabic title <span class="en">English title</span></div>
  <div class="finding-detail">Arabic detail text.</div>
  <div class="finding-detail en" style="direction:ltr;text-align:left;color:var(--muted);">English detail text.</div>
</div>
```

### Cost Summary Box Pattern
```html
<div class="cost-box">
  <div class="cost-row total"><span>Item</span><span>SAR X,XXX</span></div>
  <div class="cost-row"><span>Sub-item</span><span>SAR XXX</span></div>
  <div class="cost-row total"><span>Total</span><span><strong>SAR X,XXX</strong></span></div>
</div>
```

### Findings Summary Dashboard
```html
<div class="findings-summary">
  <div class="stat"><div class="num" style="color:var(--fail);">N</div><div class="label"><span class="en">Critical</span></div></div>
  <div class="stat"><div class="num" style="color:var(--warn);">N</div><div class="label"><span class="en">Major</span></div></div>
  <div class="stat"><div class="num" style="color:var(--info);">N</div><div class="label"><span class="en">Minor</span></div></div>
  <div class="stat"><div class="num" style="color:var(--pass);">N</div><div class="label"><span class="en">Observation</span></div></div>
</div>
```

### Scorecard Table
```html
<table>
  <tr><th>Audit Domain</th><th>Score</th><th>Level</th></tr>
  <tr><td>Domain Name</td><td>XX%</td><td><span class="tag tag-{pass|warn|fail}">Level Text</span></td></tr>
  ...
  <tr style="font-weight:700;background:#f0f4f8;"><td>Overall Average</td><td>XX%</td><td>...</td></tr>
</table>
```

## Severity Tag Colors
| Severity | Class | Color | Meaning |
|----------|-------|-------|---------|
| Critical | `tag-fail` | `--fail:#a11` | Blocking issue, immediate action |
| Major | `tag-warn` | `--warn:#d97706` | Significant gap, must fix |
| Minor | `tag-info` | `--info:#2563eb` | Needs attention |
| Observation | `tag-pass` | `--pass:#15803d` | Good finding to preserve |

## Project-Specific Adaptations

- **Zamzam Museum (ID 121):** Add MEP clash coordination audit (Area G-5), facade redesign alternatives, and NWC-specific compliance
- **Aseer Regional Museum (3092):** Add GBH showcase audit (pull & slide doors), NRS submittal review status, and MoC-specific heritage requirements
- **Al Faw Visitor Center:** Add UNESCO OUV assessment, Heritage Commission buffer zone, desert HSE, and tent roof structural audit
- **El-Ghamama Gift Shop:** Simpler audit — focus on retail fit-out compliance, fire safety, and finishes approval status

## Related References
- `bilingual-document-template.md` — Samaya CV Pack HTML style
- `reference_files/PEP_PROJECT_EXECUTION_PLAN.rev05.html` — full bilingual example
- `reference_files/VE_REPORT.rev01.html` — standalone VE analysis example
