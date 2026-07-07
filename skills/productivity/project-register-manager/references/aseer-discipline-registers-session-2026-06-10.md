# Aseer Discipline Submittal Registers — Session June 10, 2026

## Registers Created This Session

| # | Discipline | Ref Prefix | Items | Subcon Folder | SOW Sections |
|---|------------|-----------|-------|---------------|--------------|
| 1 | AV / IT | AV-xxx | 60 | 03_AV_IT_Contractor | 6.22.2, 6.22.4(xiii), 8.9, ER 3.2-3.5 |
| 2 | Exhibition Fit-Out | FO-xxx | 96 | 04_Exhibition_FitOut_Contractor | 6.22, 6.22.1, 6.22.4, Part 3 (8.1-8.14) |
| 3 | Graphics | GR-xxx | 34 | 08_Graphics_Contractor | 6.22.1, 6.22.4(viii)(ix)(xi), 8.14 |
| 4 | Oddy Testing Lab | OD-xxx | 16 | 10_Oddy_Testing_Lab | 8.1 |
| 5 | Structural | ST-xxx | 32 | 11_Structural_Contractor | 7.2, 7.3, 8.2, 8.3 |
| 6 | MEP | ME-xxx | 51 | 12_MEP_Contractor | 7.1, 7.3, ER 3.2-3.5, ER 5.0 |
| 7 | FLS | FL-xxx | 36 | 13_FLS_Specialist_Contractor | 6.22, ER 3.5, SBC801 |
| 8 | Model Maker / Replicas | MM-xxx | 20 | 01_Replica_Model_Contractor | 6.22, 6.22.4(iii)(iv)(vii), 8.12 |
| 9 | Lighting | LG-xxx | 31 | 20_Lighting_Designer | 6.22.3, 6.22.4(xiv), 8.8 |
| 10 | Showcases | SC-xxx | 25 | 02_Showcases_Contractor | 6.22, 6.22.4(v)(vi), 8.15 |

## Key Learnings

### Subfolder Pattern
Every register goes in a **subfolder** matching its name in all 3 deployment locations:
- `02_Submittals/<Name>/<Name>.xlsx`
- `Docs/09_Registers/<Name>/<Name>.xlsx`
- `Subcontractors/NN_xxx/<Name>/<Name>.xlsx`

Mohamed corrected after initial flat-file deployment: "you have to add to register folder not outside file like this"

### Exact SOW Wording
Mohamed corrected: "list same as SOW Listed" — descriptions must match SOW text verbatim, never paraphrased.

### References Only SOW + ER
"make your refrence only SOW and ER" — no external specs, interface matrices, or other documents.

### Appendix B Is the Subcontractor List
The authoritative subcontractor list is SOW **Appendix B** (`Subcontractors/_assets/APPendix B.pdf`), a single-page org chart. Not the project README table. Oddy Testing Lab is NOT in Appendix B. Registers already created for non-Appendix B items (Oddy) are kept but no new ones should be created for items outside Appendix B.

### Small Scope = Single Sheet
Oddy Testing (16 items) got a single-sheet register instead of package-split sheets. This is acceptable for narrow scopes.

### BIM Embedded in Discipline Registers
BIM items are added as a category within each discipline register (e.g., FO-091 to FO-096), not as a separate standalone register.

### 50% Package Must Be Substantive
Mohamed flagged when MEP 50% had only 4 items. Fix: add Basis of Design report, design programme, preliminary concept items (SLDs, load schedules, cooling loads) at 50%. Rule: 50% must include surveys + Basis of Design + preliminary concepts, not just site assessment.

### Category Header Range Bug
The generator scripts use `rn + offset` for category header ranges which can overreach into the next category. Fix: use the next category key as the exclusive upper bound. Currently latent (only manifests if stage masks are individually edited), but should be fixed.

### QC Gate Required
Mohamed reminded: "did you make review and QC?" — always delegate QC review (Kimi/Codex) before delivering register updates.

### Draft Email — No Register Contents
When sending a register by email: "without telling the register containt because we already sending the register" — attachment only, no item breakdown in body.

## Structural Coverage
- SOW 7.2 — Dilapidation survey, cloud survey, as-built review
- SOW 7.3 — Slab/weight loading assessment, engineering deliverables
- SOW 8.2 — Structural works: ceiling supports, stairs, stramp, terrace, catwalks
- SOW 8.3 — Exhibit supports: secondary steel for casework, setworks, specimens

## FLS Coverage
- SOW 6.22 — Fire escape strategy routes
- ER 3.5 — Fire alarm, PAVA, SPL calcs, interface testing
- SBC801 — Compliance matrix, Civil Defense submission
- Passive: fire stopping, fire-proofing, fire doors, glazing, dampers, cavity barriers
- Active: fire alarm, PAVA, sprinkler, clean agent, hydrant, extinguishers

## Model Maker Coverage
- SOW 6.22 — Models/replica drawings, schedule, briefs
- SOW 6.22.4(iii)(iv)(vii) — Final schedule, briefs, object mount schedule
- SOW 8.12 — Design, sketches, 3D models, foam models, fabrication, installation
- Foam/rough scale models are pre-production review (90/100%), NOT IFC

## Lighting Coverage
- SOW 6.22.3 — Plans, elevations, control system, calcs, coordination with AV and FLS
- SOW 6.22.4(xiv) — Schedule, BOQ, compliance sheets
- SOW 8.8 — Fabrication, installation, light balancing, exterior lighting
- Studio ZNA appointed as Lighting Designer (design only — install by MEP)

## Showcase Coverage
- SOW 6.22 — Showcase drawings, schedule, materials/conservation/security spec, environmental control
- SOW 6.22.4(v)(vi) — Final schedule, interior/object layout drawings
- SOW 8.15 — Display case types (standalone, floor-to-ceiling, wall-mounted, plinth-mounted), integrated systems (lighting, power/data, security, Abloy locks), object mount reinforcement
- Glasbau Hahn appointed
