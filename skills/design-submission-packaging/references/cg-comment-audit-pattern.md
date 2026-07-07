# CG Comment Audit Pattern

How to audit a CG review PDF against DMP/SOW/best practice and update submission plans accordingly.

## Process

1. **Extract CG comments** — Read the PDF (use pdfplumber or PyMuPDF). Number each comment. Note the overall status (A/B/C/D) and response date.

2. **Categorize by priority**:

   | Priority | Criteria | Action |
   |----------|----------|--------|
   | 🔴 Critical | Rejection reason, missing mandatory deliverable, contractual non-compliance | Must fix before next submission |
   | 🟡 Important | Process improvement, missing recommended item, terminology correction | Should address |
   | 🟢 Minor | Acknowledgment, clarification, general statement | Note and move on |

3. **Audit each comment** against:
   - **DMP/MIDP** — does the deliverable exist in the project's information delivery plan?
   - **SOW/Contract** — is the comment contractually required?
   - **Best practice** — ISO 19650, NFPA, SBC standards
   - **Current plans** — does the item already exist in the submission register?

4. **Present verdict table**:

   | # | Comment | DMP Check | SOW Check | Best Practice | Verdict |
   |---|---------|-----------|-----------|---------------|---------|
   | 2 | Drawing list rejected | MIDP requires explicit per-LOD deliverables | Contract requires unique refs | ISO 19650 §5 | ✅ CG correct |

5. **Identify missing deliverables** — items that need to be added to the plan:

   | Missing Item | Gate | Discipline | CG Comment |
   |-------------|------|------------|------------|
   | Existing Systems Survey | Gate 1 | MEP/ELEC | #5, #14 |
   | Concept Design Review Report | Gate 1 | MEP/ELEC | #10 |
   | MEP Design Risk Register | Gate 1 | MEP/ELEC | #17 |
   | MEP Value Engineering Study | Gate 3 | MEP/ELEC | #17 |
   | RACI Matrix | Gate 2 | MEP/ELEC | #4 |

6. **Update plans** — Add missing items, fix terminology, update responsibilities. Wait for user confirmation before editing.

## Common CG Comment Patterns on Aseer Museum

| Pattern | Typical CG Wording | Standard Fix |
|---------|-------------------|--------------|
| Drawing list rejected | "rejected as final DD drawing list" | Generate unique per-floor IFC refs |
| RACI missing | "RACI matrix between ZNA, RAWASIN, BMS specialist" | Create standalone RACI Excel file |
| Terminology | "Consultant shall be replaced with MEP Designer Office" | Update Responsibility column globally |
| Missing deliverables | "shall be listed explicitly" | Split generic items into individual rows |
| Site survey | "add existing as-built drawing for all existing systems" | Add survey deliverable to Gate 1 |
| LOD definitions | "LOD 350 shall include coordination above ceilings" | Add note to plan about LOD 350 scope |
