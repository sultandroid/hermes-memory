---
name: compliance-system
description: Manage the Aseer Museum compliance system — update compliance_matrix.md, compliance_gaps.md, and compliance_checklist.md when new specs/SOWs/materials/suppliers are approved.
---

# Compliance System — Aseer Regional Museum

## When to use

- A new supplier prequalification (PQ) is approved by CG
- A new material submittal (MA) is approved/rejected
- A new SOW or spec is approved
- A compliance gap is discovered or resolved
- Daily compliance sync (cron)

## Files

| File | Path | Purpose |
|------|------|---------|
| Compliance Matrix | `Technical_Office/Compliance_System/compliance_matrix.md` | Master spec→requirement→supplier mapping |
| Compliance Gaps | `Technical_Office/Compliance_System/compliance_gaps.md` | Open gaps tracker |
| Compliance Checklist | `Technical_Office/Compliance_System/compliance_checklist.md` | Checklist for new submissions |
| Spec List | `01_Registers/specification_list.md` | 387 specs, CSI MasterFormat |
| PQ Register | `01_Registers/prequalification_register.md` | 110 supplier prequalifications |
| MA Register | `01_Registers/material_submittal_register.md` | Material submittals |
| Specialist Register | `Technical_Office/Specialist_Management/specialist_register.md` | 27 specialists |
| Procurement Register | `01_Registers/procurement_package_register.md` | 19 procurement packages |

## How to update

### Adding a new supplier/material to the compliance matrix

1. Read `compliance_matrix.md` to find the correct Division and Req ID
2. Read `specification_list.md` to find the matching Spec No.
3. Read `prequalification_register.md` or `material_submittal_register.md` for PQ/MA ref
4. Add a new row to the compliance matrix with:
   - Req ID (from ER/SoW/DMP)
   - Requirement description
   - Spec No. (from spec_list.md)
   - Discipline code
   - Supplier/Material name
   - PQ Ref and/or MA Ref
   - Compliance status (🟢/🟡/🔴/⚪)
   - Gap ID (if non-compliant, link to compliance_gaps.md)
   - Last Checked date
   - Notes (action items, CG comments)
5. If a new gap is created, add it to `compliance_gaps.md`

### Closing a compliance gap

1. Read `compliance_gaps.md`
2. Move the gap from Open Gaps to Resolved Gaps
3. Add Closed Date and Closed By
4. Update the compliance matrix row to 🟢

### Daily sync (cron)

1. Check Aconex transmittals (Outlook noreply@aconex.com) for new approvals
2. Update compliance_matrix.md with any new approvals
3. Update compliance_gaps.md (resolve closed gaps, add new ones)
4. Recalculate roll-up counts
5. Generate report if changes found

## Compliance status codes

| Code | Meaning |
|------|---------|
| 🟢 Compliant | All requirements met |
| 🟡 Partial | Some requirements met; gaps remain |
| 🔴 Non-compliant | Critical requirements not met |
| ⚪ Not assessed | Not yet evaluated |

## CG status codes

| Code | Meaning |
|------|---------|
| A | Approved |
| B | Approved w/ comments |
| C | Revise & Resubmit |
| D | Disapproved |
| U | Under Review |

## Key rules

- Every compliance row must trace to an ER/SoW/DMP reference
- Every spec must have a CSI MasterFormat number
- Every supplier must have a PQ reference (or be flagged as not yet PQ'd)
- Every material near artefacts must have Oddy test status
- CG comments must be preserved verbatim in Notes
- Gaps must have a target date and owner
- Roll-up counts must be recalculated after every update
