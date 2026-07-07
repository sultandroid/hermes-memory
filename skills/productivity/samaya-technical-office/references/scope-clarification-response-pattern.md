# Scope Clarification Response — NRS vs SAMAYA Responsibility Pattern

When receiving a formal request (from CG/PMC/NRS) asking for a breakdown of specialist/engineering positions and who covers them between NRS and SAMAYA.

## Trigger

Email asking "which specialist positions does NRS provide vs SAMAYA?" referencing SOW §5.5 (Staffing and Deployments) or Engr. Elbaz's CG directive list. Purpose: finalize org chart, manpower plan, respond to CG comments.

## Workflow

### 1. Gather Source Documents

Cross-reference FOUR sources — SMP draft MUST be verified against live subcontractor folders before sending:

| Source | Location | What It Tells You |
|--------|----------|-------------------|
| NRS Contract (Appendex A) | `01_Contracts/02_NRS_Contract/` | NRS design scope: IFC package elements + review/stamp obligations |
| Stakeholder Mgmt Plan (SMP) | `02_Plans_and_Procedures/02.13_Stakeholder_Plan/` | Tier IDs (T1-XX/T2-XX/T3-XX), named firms, approval status |
| Subcontractor Register | `24_Subcontractors/README.md` | Engaged contractors, their status (appointed/active/pre-qual) |
| Live Subcontractor Folders | `24_Subcontractors/{NN}_{Discipline}/` | Actual current status per sub-folder — SMP may be stale |

### 2. Classify Each Position

**NRS Design Scope** — positions where NRS contract covers design/coordination:
- NRS produces design drawings (setworks=78 dwgs, showcases=17 dwgs)
- NRS provides design intent only (interactives, graphics layout)
- NRS is named party in SMP Tier 2 (T2-14 Architecture, T2-08 Setworks/Joinery)
- Accessibility consultant = NRS per SMP T3-08 (conditional)
- Principal Design Engineer = NRS Director/Associate role

**SAMAYA Positions** — everything SAMAYA must contract/employ:
- Specialist subcontractors engaged (Glasbau Hahn, Studio ZNA, etc.)
- Internal Samaya roles (BIM Manager, Tech Office)
- Roles yet to be deployed (T&C Manager, IT/Security Specialist)
- Future procurement

### 3. SMP Tier Reference Mapping

Key Aseer Museum SMP refs: T1-03 BIM Manager, T1-07 IT/Security Specialist, T2-05 AV, T2-06 Lighting, T2-07 Showcases, T2-08 Setworks/Joinery, T2-14 Architecture/Interior, T3-08 Accessibility (NRS conditional).

### 4. Build Reply Structure

Two tables:
- **Table 1: NRS Design Scope** — Position | Coverage Description | SMP Ref
- **Table 2: SAMAYA Positions** — Position | Engagement | Status | SMP Ref

### 5. Key Notes to Include

- All specialist subs under SAMAYA — no privity with NRS/CG/MoC per DMP §6.13
- NRS reviews/stamps specialist submittals per contract (72h SLA, ZD-0026)
- Breakdown aligned with SMP Rev XX and NRS Responsibility Matrix Appendex A
- Org chart + manpower plan updated and submitted via CDE Aconex

### 6. Downstream Document Updates

After sending the response, the conversations/decisions trigger a SMP rev bump and downstream plan update cycle:
- **SMP** — bump revision, update specialist status cells, fix headers/footers, deploy to samaya-factory.com/build/technical-office/
- **Resource Management Plan** — same status corrections, ensure "Synced with SMP Rev XX" in description, deploy
- **Deploy path**: `domains/samaya-factory.com/public_html/build/technical-office/`

**NRS Design Scope** — positions where NRS contract covers design/coordination:
- NRS produces design drawings (setworks=78 dwgs, showcases=17 dwgs)
- NRS provides design intent only (interactives, graphics layout)
- NRS is named party in SMP Tier 2 (T2-14 Architecture, T2-08 Setworks/Joinery)
- Accessibility consultant = NRS per SMP T3-08 (conditional)
- Principal Design Engineer = NRS Director/Associate role

**SAMAYA Positions** — everything SAMAYA must contract/employ:
- Specialist subcontractors engaged (Glasbau Hahn, Studio ZNA, etc.)
- Internal Samaya roles (BIM Manager, Tech Office)
- Roles yet to be deployed (T&C Manager, IT/Security Specialist)
- Future procurement

### 3. SMP Tier Reference Mapping

Key Aseer Museum SMP refs: T1-03 BIM Manager, T1-07 IT/Security Specialist, T2-05 AV, T2-06 Lighting, T2-07 Showcases, T2-08 Setworks/Joinery, T2-14 Architecture/Interior, T3-08 Accessibility (NRS conditional).

### 4. Build Reply Structure

Two tables:
- **Table 1: NRS Design Scope** — Position | Coverage Description | SMP Ref
- **Table 2: SAMAYA Positions** — Position | Engagement | Status | SMP Ref

### 5. Key Notes to Include

- All specialist subs under SAMAYA — no privity with NRS/CG/MoC per DMP §6.13
- NRS reviews/stamps specialist submittals per contract (72h SLA, ZD-0026)
- Breakdown aligned with SMP Rev XX and NRS Responsibility Matrix Appendex A
- Org chart + manpower plan updated and submitted via CDE Aconex

## Pitfalls

- **Accessibility = NRS** — SMP T3-08. Never mark as "TBD / to be procured."
- **MEP = split Designer + Contractor** — MEP Designer (ITC) and MEP Contractor are separate entries. Never combine.
- **Models & Props status** — "Pending — waiting object research from client" not just "pending CG/MoC approval"
- **Graphics firm name** — "Samaya-Graphic" not "Samaya Graphit". Status: pre-qual pending.
- **Setworks/Joinery fab** — Samaya Factory (not Exhibition Fit-Out Contractor). Status: pre-qual pending.
- **Cafe Terrace Shade** — Split design (NRS) + contractor (Samaya Factory, pending)
- **ICT/Security System Integrator** — TBD (not "CITC Telecom Engineer"). IT/Security Specialist (T1-07) and System Integrator (T2-15) are separate per CRS-01/CRS-06.
- **Landscaping** — Evergreen, pre-qual in progress
- **Quality team** — SAMAYA internal + subcontractor QA/QC (partial)
- **Status labels** — Named firms get status. TBC entries get none.
- **Cafe Terrace Shade** — No SMP entry. Under Exhibition Fit-Out / Landscaping.
- **IT/Security split** — CG requires TWO: (1) full-time specialist T1-07 + (2) System Integrator T2-15. Don't conflate.
- **Setworks/Joinery** — NRS does design (78 dwgs); SAMAYA contracts fabrication. Two entries.
- **Principal Design Engineer** — Maps to NRS Director/Associate (T2-14), not a separate SMP title.
- **Status labels** — Named firms get status. TBC entries get none.
- **Cafe Terrace Shade** — No SMP entry. Under Exhibition Fit-Out / Landscaping.
