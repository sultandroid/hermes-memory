# Scope Audit Checklist — Deliverable Tree vs Contract Scope

## When To Use
Audit a RIBA deliverable tree/report against Samaya's contractual scope defined by ER (Employer's Requirements), SOW (Scope of Work), and BOQ (Bill of Quantities / Pricing Schedule).

## Workflow
User order → Codex rewrites/structures → Claude Code executes audit → Codex audits output → fix → deliver

## Contract Scope Reference Documents

| Doc | Description | Location |
|-----|-------------|----------|
| **ER** | Employer's Requirements — MEPF engineering scope, 170pp | `Package_Part 2/05_AS_Employer's Requirements Documents_250313/Contractors Employers Requirements - Engineering_250313/` |
| **SOW** | Scope of Work — 7 Parts, 46pp | `Package_Part 2/05_AS_Employer's Requirements Documents_250313/Contractors Scope of Works Document - Technical_250313/` |
| **BOQ** | Pricing Schedule — 15 sections (001-015) | `Package_Part 2/04_AS_Commercial Documents_250313/01_AS_Pricing Schedule_250313/` |

## Known Scope Boundaries (Aseer Museum D&B)

| Item | Status | Reference |
|------|--------|-----------|
| AV software/content | **EXCLUDED** (MoC) | BOQ §012 — all lines "By MoC" |
| AV hardware | **IN SCOPE** | BOQ §011 |
| Exhibition text/labels/content research/copyright/mounts | **EXCLUDED** (MoC-supplied) | SOW §2.2 |
| Mock-ups, samples, prototypes | **IN SCOPE** | BOQ §014 — SAR 120K samples + SAR 250K spares |
| All authority approvals/NOCs | **IN SCOPE** (Samaya resp.) | ER §2.4, SOW §13.6 |
| Design certification | **MANDATORY** | SOW §6.8 |
| BIM Execution Plan (BEP) | **MANDATORY** | ER §2.3.D |
| ITCA (Independent Testing & Commissioning Agent) | **MANDATORY** | ER §2.6 |
| Handover (17 items) | **IN SCOPE** | ER §2.7 |
| Exterior landscape (EX1/EX2) | **DEFERRED** | Scope note |
| Landscape/hardscape/softscape/irrigation within site | **IN SCOPE** | CG confirmation |
| Structural modifications for exhibition | **IN SCOPE** | Secondary structural per Samaya scope |
| MEP & FLS upgrades | **IN SCOPE** | ER §3.x |
| Exhibition & scenography | **IN SCOPE** | SOW Part 1 |
| NRS stamp = "design intent only" | **Note** | No construction/coordination/dimensional liability |

## Classification Categories

Classify EACH deliverable as one of:
- **In Scope** — Required under ER, SOW, or BOQ
- **Excluded** — Explicitly assigned to MoC or another party
- **Deferred** — Not currently required for delivery
- **Clarification Required** — Not clearly supported or excluded by available scope docs

## Audit Questions

For each deliverable:
1. Does the contract require this? (cite ER/SOW/BOQ clause)
2. Is it correctly labelled ([MoC], [NRS], [SAMAYA])?
3. Is the RAG status accurate given contractual obligation?
4. If missing from the tree, should it be added?

## Output Format

Produce a structured report with:
1. **Executive Summary** — classification counts, overall compliance
2. **Per-Category Matrix** — category-by-category with item-level classification
3. **Gap Register** — missing items, extra items, data integrity issues
4. **Risk & Action Log** — CRITICAL/HIGH/MEDIUM/LOW risks with owner and action

## Common Findings From Previous Audits

### Data Integrity
- Cover page total vs actual item count mismatch (most common)
- Dashboard RAG totals not matching per-item counts
- Legend text with wrong total
- Category-level RAG sum not matching actuals

### Scope Classification
- AV hardware/software boundary must be split per BOQ §011 vs §012
- Graphics content (MoC) vs production hardware (Samaya) — mark clearly
- Mock-ups are IN scope (BOQ §014 has budget) — don't miss
- Landscape within site is IN scope (per CG) even though EX1/EX2 deferred
- BEP, Design Cert, ITCA are MANDATORY — flag if missing

### Reporting
- Include precise ER/SOW/BOQ clause numbers, not generic references
- Note conflicting ownership (e.g., "PMC managing Cost Plan" ≠ Samaya deliverable)
- Flag mixed-scope items for formal Interface Responsibility Matrix (D12)
