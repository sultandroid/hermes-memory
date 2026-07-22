# SOW Compliance Audit — Worked Example

This reference captures the methodology used in the 21-Jul-2026 audit of 30 specialist packages against 5 governing sources.

## Source Files Read

| File | Purpose |
|------|---------|
| `03_Scope/sow_summary.md` | Project SOW summary + ZNA scope |
| `03_Scope/er_summary.md` | ER sections (MEP, electrical, HVAC) |
| `03_Plans/15_Subcontractor_Deliverables/project_sow_appendix_a_b_extraction.md` | Appendix A (106 rows) + Appendix B package map |
| `Technical_Office/Compliance_System/compliance_matrix.md` | 51 compliance rows, 13 open gaps |
| `Technical_Office/Compliance_System/compliance_gaps.md` | 18 gaps (9 open, 11 in progress, 1 resolved) |
| `01_Registers/subcontractor_sow_raci_register.md` | 21 package SOW production statuses |
| `01_Registers/subcontractor_package_register.md` | 19 package folder map |
| `03_Plans/15_Subcontractor_Deliverables/subcontractor_sow_control_system.md` | 9 issue gates, 21 package control rows |
| `03_Plans/15_Subcontractor_Deliverables/SOW_RACI_Conflict_Matrix.md` | 6 open interface conflicts |
| `Technical_Office/Specialist_Management/specialist_register.md` | 27 specialists with status |

## Key Distinction: SOW Exists vs SOW Filed in Repo

The SOW register uses "package SOW exists" to mean the SOW exists on OneDrive (`24_Subcontractors/<name>/`). The audit must distinguish:

- **✅ Filed in repo** — actual documents in `03_Scope/<name>/`
- **🟢 Approved (on OneDrive)** — SOW exists but not in repo (ZNA, Interactive, CITC, Acoustic)
- **🟡 Draft RACI only** — no formal package SOW, only draft RACI in `Draft_SOW_RACI/`
- **❌ Missing** — no SOW anywhere

## Common Gaps Found

### Against Appendix A
- ApxA 4.02: Lighting spares 1 year — not in ZNA SOW
- ApxA 2.13: Media/AV software by MoC — not documented in Rawasin SOW
- ApxA 4.01: AV hardware spares 1 year — not confirmed
- ApxA 2.12, 3.01-3.05: Content/copyright/translation by MoC — not in Graphics SOW
- ApxA 4.03: Interactive spares — not addressed

### Against ER
- ER §2.4.D: Oddy testing — Oddy Lab not appointed
- ER §3.0: MEP installation — MEP Contractor not awarded

### Against Project SOW
- PS §3: Interactives, setworks, joinery — no specialists appointed

## 3-Layer System Created

```
03_Scope/                          ← 27 folders (1 with actual SOW files)
02_Schedule/                       ← 27 folders (3 with actual plans)
Technical_Office/Submission_Tracker/ ← 27 folders (1 populated with live log)
```

## Files Updated

| File | Change |
|------|--------|
| `specialist_register.md` | Added SOW/Plan columns with folder paths for all 14 Tier 2 specialists |
| `subcontractor_sow_raci_register.md` | Updated ZNA, Graphics, MEP Designer statuses |
| `subcontractor_package_register.md` | Updated MEP Designer row with repo paths |
| `PROJECT_MEMORY.md` | AD Engineering entry with file paths |

## Audit Output

Saved to `Technical_Office/Submission_Tracker/SOW_Compliance_Audit.md` — 280 lines covering all 30 packages with per-source compliance tables, gap documentation, and priority actions.
