# CRP Compliance Check Against Roadmap (Round 1 Rev.00)

## Context

When CG reviews Rev.00 of a plan and responds not with a formal DS form but with an emailed directive/workbook (e.g., Project Delivery Workflow Roadmap), that **attachment IS the Round 1 comment**. It must be dispositioned in the cumulative table alongside subsequent Code A/B/C/D rounds.

## Compliance Checklist Template

| # | Roadmap Requirement | CRP § | Status | Notes |
|---|--------------------|-------|--------|-------|
| 1 | **Technical Submittal Sequence** (6 steps) | §7.0 | ✅/⚠️/❌ | Note any sequence changes per later CG direction |
| 2 | **Project Phases/Gates** | §13 | ✅/⚠️/❌ | CRP may refine into more granular gates |
| 3 | **Discipline Staging** (3-stage per discipline) | §7.3 | ✅/⚠️/❌ | Verify all disciplines covered |
| 4 | **Specialized Systems Workflow** (N-stage) | §7.5 | ✅/⚠️/❌ | Match stage count and names |
| 5 | **Site Work Sequence** | §7.6 | ✅/⚠️/❌ | Match node sequence |
| 6 | **T&C Framework** (tiers) | §7.7 | ✅/⚠️/❌ | Verify tier structure |
| 7 | **Handover Deliverables** | §7.4 + Appendix | ✅/⚠️/❌ | Check all types catalogued |
| 8 | **Authority Liaison Chain** | §10 | ✅/⚠️/❌ | Verify routing chain |
| 9 | **Documentation Format** | §11 | ✅/⚠️/❌ | CDE protocol coverage |
| 10 | **Submission Compliance Rule** | §7.0 | ✅/⚠️/❌ | Override clause present |

## Override Rule

Roadmap often includes a clause: *"All project submissions and site activities shall follow the above sequence unless otherwise formally instructed by the Consultant."* This means later CG Code C comments that change the sequence are valid overrides. The CRP correctly follows the latest CG direction.

## Cross-Round Contradiction Example

**Round 1 (Roadmap, Afifi, 8-Mar-2026):**
```
Design Package → Shop Drawings → Material Submittals → Method Statements → WIR → T&C
```

**Round 2 (Code C Comment 3, Elbaz, 25-May-2026):**
> "Material submittal stage must be finalized before the submission of shop drawings"

```
Design Package → Material Submittals → Shop Drawings → Method Statements → WIR → T&C
```

**Resolution:** The CRP follows the latest CG direction (Code C Comment 3) and cites the Roadmap's override provision (§02) as authority. The contradiction is transparently documented in a red alert box under §7.0.

## Key Action When Finding Contradictions

1. **Don't RFI the CG about their own comment** — the later comment IS the formal instruction
2. **Document the contradiction transparently** — add a note in the CRP explaining what the Roadmap says, what the Code C comment says, and which takes precedence with citation
3. **Cite the Roadmap's override provision** as the authority for following the latest CG direction

## Verify CG Comment Resolutions Against Actual Diffs

Before marking a CG comment as "addressed" in the disposition table, verify the document actually changed:

- Diff the old revision (C01) against the new revision (C02) for the relevant section
- **A disclaimer note appended to an unchanged table is not a resolution** — the structure/table that CG objected to must change or be clearly reframed
- Use `diff` between the two HTML files to confirm the change was applied

### Example: Comment 4 (SAMAYA contractual responsibility)
- Old approach: Add a "does not reduce liability" note to the unchanged workload table
- Correct approach: Reframe the table as communication touch-points, not workload/liability split. Update the title, column header, and footnote to match. The disposition table should accurately describe what changed — not what you hoped would address it.

## Sources

- Rev.00 CG response: `02_CG_Responses/Project Delivery Workflow (Roadmap).pdf` (email from Mohamed Afifi, 8-Mar-2026)
- Rev.01 CG response: `02_CG_Responses/PL-0018_Rev01_CG_Reply_CodeC.pdf` (Mohamed Elbaz, 25-May-2026)
