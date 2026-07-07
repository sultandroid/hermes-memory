# CRS Register Filling — Originator Reply Pattern

When a formal CRS (Comments Resolution Sheet) Excel template is provided with CG comments, fill the **Originator Reply** column with Samaya's disposition response per Rev 02+ updates.

## CRS Excel Structure

Typical formal CRS template:
- **Sheet:** `CRS`
- **Rows 5-9:** Document header (project, document number, revision, title)
- **Row 12:** Column headers
- **Rows 13-31:** CRS items (1–19 for the ICT/Security-focused CG batch)
- **Row 32+:** Legend, reviewer blocks, signatures

### Column Mapping

| Column | Field | Action |
|--------|-------|--------|
| A | No. | Already filled — sequential 1..N |
| B | Initial | CG reviewer initials — leave as-is |
| C | Page/Section/Section | Source reference — leave as-is |
| **E** | **Reviewer Comment** | **CG comment text — NEVER modify** |
| **J (col 10)** | **Originator Reply** | **Fill with Samaya's disposition** |
| P (col 16) | Reply Status by Reviewer | Leave blank for CG to fill |

## Reply Writing Rules

1. **Match the response to what was actually done in Rev 02** — don't describe what "will be done"
2. **Reference specific role IDs (T1-07, T2-15, T2-22)** when applicable
3. **Use past tense** — "Added", "Updated", "Implemented", "Set"
4. **Be concise** — one sentence is usually enough
5. **Don't repeat the CG comment** — just state the action taken
6. **If PQD/CV is pending**, say "PQD submission in progress" or "CV flagged for submission via DS"

## Example Replies

| CRS # | CG Comment (abbreviated) | Originator Reply |
|-------|--------------------------|------------------|
| 1 | Interior design oversight needed | Interior Designer (T2-21) appointed by Samaya for full-time interior/fit-out oversight per Rev 02. |
| 2 | Complete missing stakeholder names, add procurement team | All stakeholders completed in register. Procurement Manager (T1-08) added - Hani Alghamdi. ORG chart to be issued separately. |
| 3 | Comply with Contractual Priority Documents | Contractual Priority notes added in Section 1.2 per Clause 2.5. VE reference document noted. |
| 4 | Missing Supervision Consultant | Supervision Consultant added in Execution Phase. Specialists set as primary deliverable producers. |
| 5 | Interest/power scores need raising | Scores updated: Site Manager & QA/QC interest raised to 5; HSSE power raised to 5. BIM Manager already at 5. |
| 6 | Structural Engineer scope non-compliant | Structural Engineer scope updated to comply with ER Section 3.10 and Project Structural Report. Slab-load interface I-14 added. |
| 7 | Missing interface for exhibition loads vs structural | Interface I-14 (Exhibition Loads vs Structural slab-load verification) added to Interface Matrix. |
| 8 | CG-03 closure not supported by submittals | CG-03 remains RE-OPENED pending IT/Security Specialist CV and ICT PQD submission. These will be submitted progressively. |
| 9 | T2-15 still TBC | T2-15 set as ICT/Security System Integrator role. PQD submission in progress via DMP-03-REG-008. |
| 10 | IT/Data role misclassified | IT/Security Specialist added as T1-07 Key Personnel. Full-time site-based role. CV to be submitted via DS. |
| 11 | Site Instruction not reflected | Site Instruction referenced in T1-07 scope. Appendix B / SoW references included. |
| 12 | No differentiation between Specialist and Integrator | Split implemented: T1-07 (Specialist) for monitoring/coordination vs T2-15 (System Integrator) for design/delivery. |
| 13 | Missing duties definition | Duties added to T1-07 scope per CRS-03 covering design review, shop drawings, testing, commissioning, and handover. |
| 14 | MOI Security/CITC misclassified as specialist | T3-09 (MOI Security / CITC) classified as Authority-liaison only. Specialist in T1-07, Integrator in T2-15. |
| 15 | MEP design agency omitted | MEP Design Agency (T2-22) added. PQD to be submitted per 18-May-26 agreement. |
| 16 | Structural Engineer CV missing | Structural Engineer CV flagged for submission via DS. |
| 17 | MEP team in coordination-only role | Current MEP team (T2-02/03) marked as coordination-only. T2-22 MEP Design Agency handles formal design initiation. |
| 18 | ORG chart missing | ORG chart to be issued as separate submission per CRS-16. |
| 19 | Procurement team not in plan | Procurement Manager (T1-08) added - Hani Alghamdi. Procurement team now reflected in register. |

## Merged Cells Safety

The CRS Excel uses extensive merged cells. When writing via openpyxl:
- Write to the **top-left cell** of each merged range only
- The merged range handles display automatically
- Do NOT try to unmerge/write/remerge — this breaks the template formatting

## Verification

After filling, verify row-by-row that:
1. Every CRS number has a reply (no gaps)
2. No CG comment text was modified (column E unchanged)
3. The document header rows (5-9) were not accidentally overwritten
4. Save with a new filename or confirm overwrite
