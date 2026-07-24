# RMP ZD-0093 — CG Response Worked Example

> Risk Management Plan submitted 20-Jul-2026, CG returned Code C 23-Jul-2026.
> Reviewer: Muhammad Noman Siddiqui (Sr. Planning Engineer) / Mansour Alrezeni (CG PM)
> CRS: 5 comments, all Closed by Technical Office.

## The 5 CG Comments and Responses

### Comment I — Risk Register not attached

**CG:** "This submission only includes the Risk Management Plan (methodology and summary tables in Sections 2.1, 4.2, 14) not the actual registers. The PRR, DDR, HSE Register, and AV Register... are missing. Please submit these registers along with the Plan for proper review."

**Response:** "Noted. The registers are live operational documents maintained in the project CDE and updated weekly. A snapshot of each register as of the submission date is attached as Appendix A (PRR), Appendix B (DDR), Appendix C (HSE Register), and Appendix D (AV Register). CG may request the latest version of any register at any time."

**Pattern:** Plan vs Register distinction. The plan is methodology, the register has the data. Comply by attaching snapshots, not by embedding the full register in the plan.

### Comment II — Section 7.3 should be deferred

**CG:** "Section 7 (Quantitative Risk Analysis) should be deferred, not filled with placeholders. This is a Design & Build fit-out contract and the BOQ is not yet finalised... Recommend stating that quantitative analysis will follow once the BOQ ready."

**Response:** "Noted. Section 7.3 has been revised. Quantitative risk analysis (EMV, Monte Carlo simulation) will be performed once the BOQ is finalised and firm cost inputs per risk are available. Until then, qualitative scoring (P x S on the 4x4 scale) governs all risk assessment and response planning."

**Pattern:** CG correctly identified placeholders. Remove them, state when the section will be populated, and confirm what governs in the meantime. Never submit placeholders ("To be recalculated", "To be confirmed") — CG will flag them.

### Comment III — Standardise scoring to 5x5

**CG:** "Qualitative scoring should be standardised to 5x5 (25), not 4x4 (16), across all registers. Currently: PRR and AV Register use a 4x4 scale (max 16), HSE Register already uses 5x5 (max 25), DDR uses a 5-point impact scale with unclear pairing."

**Response:** "Noted. Per PMBOK 6th Ed Ch. 11.3, different risk types may use different scales appropriate to their nature. Section 6.5 has been added to the RMP documenting each register's scale and rationale: PRR and AV use 4x4 (project-level PxS), HSE uses 5x5 (industry standard), DDR uses 5-point impact (design risks). All scales are clearly documented and cross-referenced. No rescoring of existing risks is required."

**Pattern:** This is the key push-back. CG asked to change the methodology, but the correct answer is to document the existing approach more clearly, not change it. PMBOK Ch. 11.3 explicitly allows different scales per risk type. The response:
1. Cites the authority (PMBOK)
2. Documents each scale with rationale
3. States no rescoring needed
4. Closes the comment without changing the methodology

### Comment IV — Schedule integration not demonstrated

**CG:** "The schedule integration is referenced but not demonstrated. Please provide a sample PRR entry linked to the corresponding Primavera P6 Activity ID, WBS, and available float."

**Response:** "Noted. The RMP is a methodology document describing how schedule-risk integration works (Section 5.1). Actual P6 Activity IDs, WBS codes, and float values are operational data maintained in the live PRR register, which is updated weekly. Section 5.4 has been updated to confirm that all PRR entries include P6 Activity ID and Float columns. The latest PRR register is available for CG review upon request."

**Pattern:** Again, plan vs register. The plan describes the method, the register has the data. Add a section confirming the method is implemented, but don't embed operational data in the plan.

### Comment V — No Middle East shipping risk

**CG:** "No risk addressing long lead and overseas procurement exposure from the current Middle East shipping/logistics situation."

**Response:** "Noted. The RMP identifies 'Middle East Shipping Disruption' as a Critical risk factor in Section 2 (Project Risk Profile). The detailed risk entry (PRR-PRC-07) with full scoring, response plan, and ownership has been added to the live PRR register, which is available for CG review upon request."

**Pattern:** Valid content gap. Add the risk factor to the plan's risk profile section, add the detailed entry to the live register. The plan gets the summary, the register gets the detail.

## DOCX Changes Made

| Section | Change | Method |
|---------|--------|--------|
| Revision History (T2) | Added REV01 row | `table.add_row()` + set cell text |
| Section 2 | Added Middle East Shipping Disruption risk factor | `insert_paragraph_before()` on next paragraph |
| Section 5.4 (new) | Schedule-Risk Integration | `insert_paragraph_before()` on paragraph after 5.2 |
| Section 6.5 | Added scoring rationale per PMBOK | `insert_paragraph_before()` on paragraph before Section 7 |
| Section 7.3 | Deferred quantitative analysis | `insert_paragraph_before()` on paragraph before Section 8 |
| Section 9.1 | Added appendix references (A-D) | `insert_paragraph_before()` on paragraph before 9.2 |

## Key Technique: python-docx insert_paragraph_after() Workaround

`python-docx` does NOT have `insert_paragraph_after()`. To insert after a paragraph:

```python
def insert_after(doc, after_idx, text, bold=False, italic=False, size=10):
    """Insert paragraph after given index by inserting before the next one."""
    if after_idx + 1 < len(doc.paragraphs):
        new_p = doc.paragraphs[after_idx + 1].insert_paragraph_before('')
    else:
        new_p = doc.add_paragraph('')
    run = new_p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    return new_p
```

This works because `insert_paragraph_before()` on the NEXT paragraph effectively inserts AFTER the current paragraph.

## Verdict

- 5 CG comments, all Closed
- 2 push-backs (scoring standardisation, schedule integration) — defended original design
- 2 complies (registers as appendices, defer quantitative) — added methodology notes
- 1 content gap (shipping risk) — added to plan + register
- No rescoring of existing risks required
- Plan is methodology, register has the data — this distinction was the key to all 5 responses
