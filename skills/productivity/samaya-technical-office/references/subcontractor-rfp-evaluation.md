# Subcontractor RFP & Evaluation Workflow

> For Aseer Museum subcontractor packages. Last updated May 29, 2026.

## RFP Document Template

### File Structure
```
Subcontractors/<NN>_<Category>/
├── RFP/
│   ├── ASM-RFP-<CAT>-NNN_<Description>_RevA.md
│   └── Attachments/
│       ├── A_<Schedule>_BOQ.md
│       ├── B_<Technical_Drawing_Refs>.md
│       ├── C_<Hardware_Schedule>.md
│       ├── D_<Standards_Matrix>.md
│       ├── E_Contract_Terms.md
│       └── F_Performance_Bond_Sample.md
├── SUBCONTRACTOR_EVALUATION.md
└── Prequalification/
    ├── <Vendor 1>/
    ├── <Vendor 2>/
    └── ...
```

### Naming Convention
- RFP Number: `ASM-RFP-<CAT>-NNN` where CAT = two-letter code (DM=Doors&Metal, SC=Showcase, AV=AV/IT, LT=Lighting, etc.)
- Category folders: `<NN>_<Category>` numbered sequentially (17_Doors_Metal_Contractors)
- Vendor folders inside `Prequalification/`: use Arabic company name as-is

### RFP Sections (standard 7-section format)

| # | Section | Content |
|---|---------|---------|
| 1 | Project Overview | Aseer Regional Museum, contract 0010003521, MoC client, NRS design lead, Samaya as fit-out contractor |
| 2 | Scope of Work | Subdivided by product type (fire-rated, non-rated, hardware, installation, testing) |
| 3 | Technical Requirements | Standards table (ASTM, UL, BS, SBC), specs table, certification requirements, warranty |
| 4 | Submission Requirements | Technical proposal, commercial (separate), compliance docs (CR, VAT, Zakat, insurance, classification) |
| 5 | Evaluation Criteria | Two-stage weighted: Tech Compliance 35%, Experience 20%, Commercial 25%, Capacity 10%, Local Presence 10%. Minimum 70% technical score to proceed |
| 6 | Timeline | 14-day submission window typical; include site visit, clarification deadline, award date, mobilization |
| 7 | Attachments | A–F as listed above |

### Evaluation Criteria Weights (Standard for Aseer Subcontractors)

| Criteria | Weight |
|----------|:------:|
| Technical Compliance | 35% |
| Experience & Track Record | 20% |
| Commercial Competitiveness | 25% |
| Capacity & Resources | 10% |
| Local Presence & Support | 10% |

### Standard Attachments

**Attachment A — BOQ/Schedule Template:**
```
| Item # | Door Tag | Type | Width | Height | Fire Rating | Acoustic | Finish | Qty | Unit Price | Total |
|--------|----------|------|-------|--------|-------------|----------|--------|:---:|:----------:|:-----:|
```
Include a summary BOQ with sections for each major scope line item.

**Attachment B — Technical Drawings Reference:**
- List the NRS drawing sheet numbers relevant to this scope (e.g., A2742 series)
- Reference the Design Files location in the BIM Unit structure

**Attachment C — Hardware/Schedule Matrix:**
```
| Set | Door Type | Hinges | Lockset | Closer | Exit Device | Pull/Push | Seals | Threshold |
|:---:|-----------|--------|---------|--------|-------------|-----------|-------|-----------|
| HS-01 | Single HM-FR | 4x BB1199 | ML2000 | SC81 | — | 2x Pull | Brush | Aluminum |
```
Include approved manufacturers list.

**Attachment D — Standards/Compliance Matrix:**
- Table of locations × fire rating × assembly type × test standard
- Reference standards: UL 10B/10C, ASTM E152, BS 476:22, NFPA 80/105, SBC 601

**Attachment E — Contract Terms:**
- Payment: advance 10%, monthly milestones, retention 10%
- Performance bond: 5%
- Insurance: CAR + third-party SAR 5M + statutory
- LD: 0.1%/day (max 10%)
- Warranty: 5 years construction, 2 years hardware
- Defects liability: 12 months

**Attachment F — Performance Bond Sample:**
- Bank guarantee format with principal/surety/obligee fields
- Standard Saudi bank guarantee language

## Evaluation Report Template

### File: `SUBCONTRACTOR_EVALUATION.md`

```
# Subcontractor Pre-Qualification Evaluation — <Category>

**Project:** Aseer Regional Museum
**Date:** <date>
**Category:** <NN>_<Category>

## Evaluation Summary

| # | Company | Specialty | Docs Quality | Scope Fit | Est. Capability | Overall |
|---|---------|-----------|:-----------:|:---------:|:---------------:|:-------:|
| 1 | Company A | — | ★★★★ | ★★★★★ | ★★★★ | Strong |
| 2 | Company B | — | ★★★ | ★★★★ | ★★★ | Good |
| 3 | Company C | — | ★★ | ★★ | ★★ | Weak |

## Detailed Assessment (per vendor)

### <Vendor Name>

**Scope:** <description>
**Documents:** N files (X MB total)

| File | Size | Pages | Notes |
|------|------|:-----:|-------|
| file.pdf | X MB | N | Description |

**Assessment:**
- ✅ Strength
- ⚠️ Concern
- ❌ Gap

**Verdict:** RECOMMENDED / CONDITIONAL / NOT RECOMMENDED

## Overall Recommendations

### Priority Shortlist:
1. Company A — reason
2. Company B — reason
3. ...

### Key Questions for Procurement:
- Question 1?
- Question 2?
```

## Vendor Evaluation Rubric

| Rating | Docs Quality | Scope Fit | Capability |
|:------:|:------------:|:---------:|:----------:|
| ★★★★★ | Full technical submittal + certs + references | Exact match | Major projects completed |
| ★★★★ | Good technical submittal, minor gaps | Mostly matches | Established capability |
| ★★★ | Basic company profile/catalogue | Partial match | Some relevant experience |
| ★★ | Registration docs only | Unclear scope | Limited evidence |
| ★ | No documentation | Mismatched | Unknown |

## Pitfalls

- **Don't accept registration-only packages** (CR, VAT, bank certs) as proof of technical capability
- **Don't skip the site visit** in the RFP timeline — door/metal work requires accurate field measurements
- **Don't evaluate commercial before technical** — enforce the 70% minimum technical score gate
- **Don't accept expired certifications** — check UL/fire test dates, CR validity, Zakat clearance
- **Watch for identical files across vendor folders** — sometimes vendors forward each other's submittals
- **Fire-rated assemblies require third-party labeling** — UL/Warnock Hersey/FM — verify labels in submittals
- **Hardware should be BHMA Grade 1 minimum** — specify in RFP, verify in evaluation
- **BOQ quantities in RFP Attachment A:** When the NRS MasterFormat BOQ.xlsx cannot be read (OneDrive file lock / "Resource deadlock avoided"), DO NOT leave quantities as TBD. Estimate from project scope (floor count, room types, typical door density) and flag clearly:
  > "Preliminary estimates only — pending audit against NRS MasterFormat BOQ (OneDrive file lock prevented direct read). Quantities to be confirmed from IFC drawings."
  This keeps the RFP actionable for bidders while documenting the data-source gap. Update quantities once the BOQ becomes readable.
