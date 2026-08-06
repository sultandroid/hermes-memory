# NRS Audit Report Workflow — Worked Example

## Source

**Email:** 50122 — Jim Richards, 5-Aug-2026
**Subject:** Aseer Regional Museum : Audit Report 02
**Attachment:** MOC-ASE-AR-ARC-GEN-DDD-DS02-00_compressed.pdf
**Email body:** "Dear All - please find attached the audit report which we partially presented today covering the proposed design studies requested by CG, and also highlighted areas of concern or clarification required."

## Step 1: Extract Content

The email body is short — the detail is in the PDF. Outlook save failed (common error), so use the email body as primary source and note the PDF as image-based.

## Step 2: Create Analysis Sidecar

Filed at: `03_Design_Files/Architecture/NRS_Reports/50122_NRS_Audit_Report_02_analysis.md`

```yaml
---
last_updated: 2026-08-05
owner_agent: Hermes
status: active
source: 50122_MOC-ASE-AR-ARC-GEN-DDD-DS02-00_compressed.pdf
---
```

Key findings extracted:
- Showcase 03.05-SC-01: 5.2m length insufficient for 34+ objects
- NRS recommends: angled plinth + integrated label rail, extend to 6400mm (4x1600mm bays)
- Vertical labels not recommended (shadow + readability issues)
- GBH would need to amend fabrication drawings if variation instructed
- MoC must provide: comprehensive object list, groupings/hierarchy, star objects

## Step 3: Consolidate with Stage 3 Audit

Stage 3 Audit (May 2026) has 15 items already tracked in `01_Registers/nrs_stage3_audit_register.md`. Audit 02 is a new report with different focus (showcase design study vs architectural discrepancies).

**Decision:** Keep separate analysis files but cross-reference in the risk register. A full master register is only needed if reports keep accumulating.

## Step 4: Cross-Map Against Existing Risks

| Finding | Existing Risk | Action Taken |
|---------|--------------|--------------|
| Showcase too short for 34+ objects | PRR-PRC-02 (Critical 12) | Add evidence + new action: confirm variation for extended showcase with GBH |
| Object list not frozen | PRR-CNS-03 (Score 4 Medium) | Flag for upgrade to 9 High — 4 Medium is too low for 34+ objects in G3 alone |
| GBH drawing amendments | PRR-PRC-02 | Add action: issue variation instruction |
| Label design | PRR-PRC-02 evidence | Note in evidence |

## Step 5: Action Plan

| # | Finding | Action | Owner | Status |
|---|---------|--------|-------|--------|
| 1 | Showcase 5.2m insufficient | Confirm variation for extended showcase (6400mm, 4x1600mm bays) | TO / Procurement | Pending |
| 2 | Object list incomplete | MoC to provide comprehensive object list for G3 | PM / MoC | Pending |
| 3 | Object groupings unclear | MoC to clarify groupings, hierarchy, star objects | PM / MoC | Pending |
| 4 | Vertical labels cast shadows | Redesign with angled plinth + integrated label rail | NRS | Pending |
| 5 | GBH needs drawing amendments | Issue variation instruction to GBH | Procurement | Pending |

## Key Lessons

1. **NRS audit reports are proactive quality checks**, not CG comments. They flag issues before they become CG problems.
2. **Email body is often sufficient** for analysis — Jim Richards summarises key findings in the email text. The PDF is the detailed version.
3. **Most findings map to existing risks** — PRR-PRC-02 covers showcase issues broadly. Don't create new risks unless there's a genuine gap.
4. **Score upgrades need evidence** — the NRS report is the evidence to justify raising PRR-CNS-03 from 4 Medium to 9 High.
5. **Variation vs in-scope** — not every NRS finding needs a variation. Check the SOW before flagging.
